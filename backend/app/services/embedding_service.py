"""
Text embedding generation service.
"""
import ollama

MODEL = "nomic-embed-text"

def generate_embedding(text: str):

    if not text.strip():
        raise ValueError("Empty text")

    response = ollama.embeddings(
        model=MODEL,
        prompt=text.strip()
    )

    return response["embedding"]
