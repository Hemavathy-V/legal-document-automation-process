from fastapi import APIRouter
from app.services.excel_loader import load_clauses_from_excel
from app.services.preprocessor import preprocess_clause
from app.services.embedding_service import generate_embeddings
from app.services.vector_store import store_clauses, search_clauses

router = APIRouter()

@router.post("/ingest-clauses")
def ingest_clauses():
    clauses = load_clauses_from_excel("data/clause_lib.xlsx")

    ids = []
    texts = []
    metadatas = []

    for clause in clauses:
        formatted_text = preprocess_clause(clause)

        ids.append(clause["id"])
        texts.append(formatted_text)

        metadatas.append({
            "term": clause.get("term"),
            "suggested_term": clause.get("suggested_term"),
        })

    embeddings = generate_embeddings(texts)

    store_clauses(
        ids=ids,
        texts=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return {"message": f"{len(ids)} rows embedded and stored successfully"}

@router.get("/search")
def search(query: str):
    query_embedding = generate_embeddings([query])[0]
    results = search_clauses(query_embedding)
    return results
