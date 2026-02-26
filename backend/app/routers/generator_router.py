"""
Dynamic Contract Generation Router
Endpoints for fetching template placeholders and saving user-provided contract data
Routes: 
  - GET /api/templates/names - List available DOCX templates
  - GET /api/templates/{template_name}/placeholders - Get placeholders for a template
  - POST /api/contracts/data - Save contract data submitted by user
"""
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status

from backend.app.scripts.dynamic_questions import ContractProcessor
from backend.app.core.logger import get_logger
from backend.app.schemas.schemas import (
    ContractDataRequest,
    ContractDataResponse,
    TemplatePlaceholdersResponse,
    TemplateNamesResponse,
)

logger = get_logger(__name__)

router = APIRouter(tags=["generator"])

# Initialize the ContractProcessor
# Note: Templates should be in PROJECT_ROOT/sample_templates directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "sample_templates"
OUTPUT_DIR = PROJECT_ROOT / "backend" / "output"

processor = ContractProcessor(templates_dir=TEMPLATES_DIR, output_dir=OUTPUT_DIR)
logger.info(f"ContractProcessor initialized for generator_router | templates={TEMPLATES_DIR} | output={OUTPUT_DIR}")


@router.get("/templates/names", response_model=TemplateNamesResponse)
def list_template_names():
    """
    Get list of available DOCX contract templates.
    Returns template names without .docx extension.
    """
    logger.info("Request: List available template names")
    try:
        names = processor.list_template_names()
        logger.info(f"Retrieved {len(names)} template names: {names}")
        return TemplateNamesResponse(templates=names)
    except Exception as e:
        logger.error(f"Error listing template names: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to list templates: {str(e)}"
        ) from e


@router.get("/templates/{template_name}/placeholders", response_model=TemplatePlaceholdersResponse)
def get_template_placeholders(template_name: str):
    """
    Get placeholder fields for a specific template.
    
    Returns:
      - simple_fields: List of single-value fields (e.g., {{partyName}})
      - loop_fields: Dictionary of repeating sections (e.g., {{#signatories}}...{{/signatories}})
    
    This response is used to dynamically generate form fields on the frontend.
    """
    logger.info(f"Request: Get placeholders for template '{template_name}'")
    try:
        simple_fields, loop_fields = processor.get_template_placeholders(template_name)
        logger.info(
            f"Placeholders retrieved for '{template_name}': "
            f"simple={len(simple_fields)}, loops={len(loop_fields)}"
        )
        return TemplatePlaceholdersResponse(
            template_name=template_name,
            simple_fields=simple_fields,
            loop_fields=loop_fields,
        )
    except FileNotFoundError as e:
        logger.warning(f"Template not found: {template_name}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_name}' not found"
        ) from e
    except Exception as e:
        logger.error(f"Error getting placeholders for '{template_name}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to parse template: {str(e)}"
        ) from e


@router.get("/templates/{template_name}/content")
def get_template_content(template_name: str):
    """
    Get the full text content of a template document.
    
    Returns:
      - content: The full text extracted from the DOCX template
    """
    logger.info(f"Request: Get content for template '{template_name}'")
    try:
        template_path = processor.get_template_path(template_name)
        if not template_path:
            logger.warning(f"Template not found: {template_name}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template '{template_name}' not found"
            )
        
        from docx import Document
        doc = Document(template_path)
        
        # Build HTML content with proper formatting
        html_content = '<div class="document-view">'
        
        for para in doc.paragraphs:
            # Get paragraph style for formatting
            style_name = para.style.name
            style_class = f"para-{style_name.lower().replace(' ', '-')}"
            
            # Build paragraph with run formatting
            para_html = ''
            for run in para.runs:
                text = run.text
                if text:
                    # Apply text formatting
                    if run.bold:
                        text = f'<strong>{text}</strong>'
                    if run.italic:
                        text = f'<em>{text}</em>'
                    if run.underline:
                        text = f'<u>{text}</u>'
                    para_html += text
            
            # Determine paragraph element
            if style_name.startswith('Heading'):
                level = style_name.split()[-1] if style_name.split()[-1].isdigit() else '2'
                html_content += f'<h{level} class="{style_class}">{para_html if para_html else para.text}</h{level}>'
            elif style_name == 'List Bullet':
                html_content += f'<li class="{style_class}">{para_html if para_html else para.text}</li>'
            else:
                html_content += f'<p class="{style_class}">{para_html if para_html else para.text}</p>'
        
        html_content += '</div>'
        
        logger.info(f"Template content retrieved for '{template_name}' as HTML")
        return {
            "template_name": template_name,
            "content": html_content,
            "format": "html"
        }
    except FileNotFoundError as e:
        logger.warning(f"Template file not found: {template_name}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_name}' not found"
        ) from e
    except Exception as e:
        logger.error(f"Error getting content for '{template_name}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to read template: {str(e)}"
        ) from e


@router.post("/contracts/data", response_model=ContractDataResponse)
def save_contract_data(request: ContractDataRequest):
    """
    Save user-provided contract data to a JSON file.
    
    Request body:
      - template_name: Name of the template to use
      - data: Dictionary containing user-provided values for all placeholders
    
    Response includes the path to the saved JSON file for later retrieval.
    """
    logger.info(f"Request: Save contract data for template '{request.template_name}'")
    try:
        output_path = processor.save_contract_data(
            request.template_name,
            request.data
        )
        fields_count = processor._count_fields(request.data)
        logger.info(
            f"Contract data saved successfully | "
            f"template={request.template_name} | "
            f"path={output_path} | fields={fields_count}"
        )
        return ContractDataResponse(
            message="Contract data saved successfully",
            template_name=request.template_name,
            file_path=str(output_path),
            total_fields=fields_count,
        )
    except FileNotFoundError as e:
        logger.warning(f"Template not found while saving data: {request.template_name}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{request.template_name}' not found"
        ) from e
    except Exception as e:
        logger.error(f"Error saving contract data for '{request.template_name}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to save contract data: {str(e)}"
        ) from e
