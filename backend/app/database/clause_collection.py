from app.database.chroma_client import get_chroma_client
from app.config import CHROMA_COLLECTION_NAME

def get_clause_collection():
    client = get_chroma_client()

    return client.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME
    )