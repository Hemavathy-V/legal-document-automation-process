from fastapi import APIRouter
from app.services.excel_loader import load_clauses_from_excel
from app.services.preprocessor import preprocess_clause
from app.services.embedding_service import generate_embedding
from app.services.vector_store import store_clause, search_clauses

router = APIRouter()

@router.post("/ingest-clauses")
def ingest_clauses():
    clauses = load_clauses_from_excel("data/clause.xlsx")

    for clause in clauses:
        formatted_text = preprocess_clause(clause)
        embedding = generate_embedding(formatted_text)

        metadata = {
            "clause_type": clause.get("clause_type"),
            "jurisdiction": clause.get("jurisdiction"),
            "title": clause.get("title"),
        }

        store_clause(
            clause_id=clause["id"],
            text=formatted_text,
            embedding=embedding,
            metadata=metadata,
        )

    return {"message": "Clauses successfully ingested into vector DB"}


@router.get("/search")
def search(query: str):
    results = search_clauses(query)
    return results
