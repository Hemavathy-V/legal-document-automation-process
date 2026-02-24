from app.database.clause_collection import get_clause_collection

collection = get_clause_collection()


def store_clauses(ids, docs, embeddings, metadatas):
    collection.upsert(
        ids=ids,
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas
    )


def search_clauses(query_embedding, top_k=5):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
