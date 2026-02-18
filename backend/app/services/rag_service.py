from app.services.embedding_service import get_embedding
from app.database.chroma_db import collection
from app.services.ollama_service import generate_response
from app.utils.prompt_template import build_prompt


def generate_legal_document(user_input: str):

    # Step 1: Embed user query
    query_embedding = get_embedding(user_input)

    # Step 2: Retrieve relevant clauses
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    retrieved_clauses = results["documents"][0]

    # Step 3: Build prompt
    prompt = build_prompt(user_input, retrieved_clauses)

    # Step 4: Generate response
    return generate_response(prompt)
