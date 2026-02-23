from pydantic import BaseModel, Field
from typing import Dict, Any, List

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