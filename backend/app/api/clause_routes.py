from fastapi import APIRouter
from app.services.rag_service import generate_legal_document

router = APIRouter()

@router.post("/generate")
def generate_doc(request: dict):
    user_input = request["query"]

    result = generate_legal_document(user_input)

    return {"generated_document": result}
