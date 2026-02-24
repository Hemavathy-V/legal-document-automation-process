import ollama
import requests

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
MODEL = "nomic-embed-text"

def get_embedding(text: str):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )

    if not text.strip():
        raise ValueError("Empty text")

    response = ollama.embeddings(
        model=MODEL,
        prompt=text.strip()
    )

    return response["embedding"]
