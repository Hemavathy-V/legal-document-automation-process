import chromadb
from chromadb.config import Settings
import os

def get_chroma_client():
    persist_path = os.path.abspath("app\database\chroma_DB")

    return chromadb.PersistentClient(path=persist_path)
