import ollama

MODEL = "nomic-embed-text"

def get_embedding(text: str):
    if not text.strip():
        raise ValueError("Empty text")

    response = ollama.embeddings(
        model=MODEL,
        prompt=text.strip()
    )

    return response["embedding"]
