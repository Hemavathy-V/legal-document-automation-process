"""
Clause collection management in ChromaDB.
"""
from app.database.chroma_client import get_chroma_client
from backend.app.core.config import CHROMA_COLLECTION_NAME

def get_clause_collection():
    client = get_chroma_client()

    return client.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME
    )
