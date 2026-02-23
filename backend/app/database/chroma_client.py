import chromadb
from app.config import CHROMA_PERSIST_DIR

def get_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
