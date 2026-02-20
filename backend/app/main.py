from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.collect_inputs.dynamic_questions import ContractProcessor


class ContractRequest(BaseModel):
    template_name: str = Field(..., min_length=1)
    data: Dict[str, Any]


class TemplatesResponse(BaseModel):
    templates: List[str]


class PlaceholdersResponse(BaseModel):
    template_name: str
    simple_fields: List[str]
    loop_fields: Dict[str, List[str]]


class GenerateContractResponse(BaseModel):
    message: str
    template_name: str
    file: str
    generated_at: str
    total_fields: int


app = FastAPI(title="Legal Document Automation API", version="1.0.0")

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent
TEMPLATES_DIR = PROJECT_ROOT / "sample_templates"
OUTPUT_DIR = BASE_DIR / "output"

processor = ContractProcessor(templates_dir=TEMPLATES_DIR, output_dir=OUTPUT_DIR)


@app.get("/templates", response_model=TemplatesResponse)
def list_templates() -> TemplatesResponse:
    templates = processor.list_template_names()
    return TemplatesResponse(templates=templates)


@app.get("/templates/{template_name}/placeholders", response_model=PlaceholdersResponse)
def get_placeholders(template_name: str) -> PlaceholdersResponse:
    try:
        simple_fields, loop_fields = processor.get_template_placeholders(template_name)
        return PlaceholdersResponse(
            template_name=template_name,
            simple_fields=simple_fields,
            loop_fields=loop_fields,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unable to parse template: {exc}") from exc


@app.post("/contracts/data", response_model=GenerateContractResponse)
def generate_contract(request: ContractRequest) -> GenerateContractResponse:
    try:
        output_path = processor.save_contract_data(request.template_name, request.data)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unable to save contract data: {exc}") from exc

    return GenerateContractResponse(
        message="Contract data saved successfully",
        template_name=request.template_name,
        file=str(output_path),
        generated_at=datetime.now().isoformat(),
        total_fields=processor._count_fields(request.data),
    )
