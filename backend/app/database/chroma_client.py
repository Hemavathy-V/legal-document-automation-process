"""
ChromaDB client initialisation.
"""
import chromadb
from backend.app.core.config import CHROMA_PERSIST_DIR

def get_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
