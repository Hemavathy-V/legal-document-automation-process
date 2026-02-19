from app.database.chroma_client import get_chroma_client

COLLECTION_NAME = "clause_library"

def get_clause_collection():
    client = get_chroma_client()
    
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )
    
    return collection
