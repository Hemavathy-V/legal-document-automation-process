from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.services.rag_service import generate_legal_document

router = APIRouter()

class Request(BaseModel):
    query: str


@router.post("/generate")
def generate(req: Request):
    return {"result": generate_legal_document(req.query)}
