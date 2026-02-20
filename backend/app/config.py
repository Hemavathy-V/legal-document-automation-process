import os

CHROMA_COLLECTION_NAME = "terminology_library"
CHROMA_PERSIST_DIR = "./chroma_storage"

os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
