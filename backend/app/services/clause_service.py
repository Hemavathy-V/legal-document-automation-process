import chromadb
from chromadb.config import Settings
from app.config import CHROMA_COLLECTION_NAME, CHROMA_PERSIST_DIR

client = chromadb.Client(
    Settings(
        persist_directory=CHROMA_PERSIST_DIR,
        is_persistent=True
    )
)

collection = client.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME
)

def store_clauses(ids, texts, embeddings, metadatas):
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

def search_clauses(query_embedding, n_results: int = 5):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
