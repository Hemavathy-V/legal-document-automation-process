from backend.app.database.chroma_client import get_chroma_client
from backend.app.core.config import CHROMA_COLLECTION_NAME

COLLECTION_NAME = "clause_library"

def get_clause_collection():
    client = get_chroma_client()

    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME
    )
    
    return collection
