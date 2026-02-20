from app.services.embedding_service import generate_embedding
from app.services.clause_service import search_clauses
from app.services.ollama_service import generate_response
from app.utils.prompt_template import build_prompt


def generate_legal_document(query: str):

    # embed query
    emb = generate_embedding(query)

    # retrieve
    results = search_clauses(emb, top_k=3)

    clauses = results["documents"][0] if results["documents"] else []

    if not clauses:
        return "No relevant clauses found."

    # prompt
    prompt = build_prompt(query, clauses)

    # generate
    return generate_response(prompt)