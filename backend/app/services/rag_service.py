from backend.app.services.embedding_service import get_embedding
from backend.app.services.clause_service import search_clauses
from backend.app.services.ollama_service import generate_response
from backend.app.prompts.prompt_template import build_prompt
from backend.app.core.logger import get_logger

logger = get_logger(__name__)


def generate_legal_document(query: str):
    try:
        logger.info("rag_request_started", extra={"query": query})

        # ---------------- EMBEDDING ----------------
        logger.info("embedding_started")
        emb = get_embedding(query)

        # ---------------- RETRIEVAL ----------------
        logger.info("retrieval_started")
        results = search_clauses(emb, top_k=3)
        clauses = results["documents"][0] if results.get("documents") else []

        if not clauses:
            logger.warning("no_clauses_found")
            return "No relevant clauses found."

        # ---------------- PROMPT BUILDING ----------------
        prompt = build_prompt(query, clauses)

        # ---------------- GENERATION ----------------
        logger.info("generation_started")
        result = generate_response(prompt)

        logger.info("rag_success")
        return result

    except Exception as e:
        logger.error("rag_failed", extra={"error": str(e)})
        raise
