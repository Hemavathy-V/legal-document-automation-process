from app.database.clause_collection import get_clause_collection
from app.services.embedding_service import generate_embedding

def retrieve_clauses(query: str, top_k: int = 5):

    collection = get_clause_collection()

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0] if results["documents"] else []