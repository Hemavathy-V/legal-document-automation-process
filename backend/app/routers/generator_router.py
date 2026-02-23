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

from app.collect_inputs.dynamic_questions import ContractProcessor
from app.core.logger import get_logger
from app.schemas import (
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
