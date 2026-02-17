import chromadb
from chromadb.config import Settings
from app.config import CHROMA_COLLECTION_NAME, CHROMA_PERSIST_DIR

# Persistent client
client = chromadb.Client(
    Settings(persist_directory=CHROMA_PERSIST_DIR)
)

collection = client.get_or_create_collection(CHROMA_COLLECTION_NAME)


def store_clause(clause_id: str, text: str, embedding: list, metadata: dict):
    collection.add(
        ids=[clause_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata]
    )


def search_clauses(query: str, n_results: int = 5):
    return collection.query(
        query_texts=[query],
        n_results=n_results
    )
