"""
Application configuration and settings.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CHROMA_COLLECTION_NAME = "clause_library"
CHROMA_PERSIST_DIR = os.path.join(BASE_DIR, "chroma_DB")

os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)