import os

CHROMA_COLLECTION_NAME = "clause_library"
CHROMA_PERSIST_DIR = os.path.abspath("app/database/chroma_DB")

os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)