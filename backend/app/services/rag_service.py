import json
from backend.app.services.embedding_service import get_embedding
from backend.app.services.clause_service import search_clauses
from backend.app.services.ollama_service import generate_response
from backend.app.prompts.legal_contract_prompt import CONTRACT_PROMPT
from backend.app.core.logger import get_logger

logger = get_logger(__name__)


def generate_legal_document(
    contract_type: str,
    contract_template_text: str,
    user_input_data: dict,
    regional_law_text: str,
):
    try:
        logger.info("rag_request_started", extra={"contract_type": contract_type})

        # ---------------- EMBEDDING ----------------
        logger.info("embedding_started")

        # Embed structured context for better semantic retrieval
        retrieval_context = (
            f"Contract Type: {contract_type}\n"
            f"User Data: {json.dumps(user_input_data)}\n"
            f"Regional Law: {regional_law_text}"
        )

        query_embedding = get_embedding(retrieval_context)

        # ---------------- RETRIEVAL ----------------
        logger.info("retrieval_started")
        results = search_clauses(query_embedding, top_k=5)

        documents = results.get("documents", [[]])[0]

        if not documents:
            logger.warning("no_clauses_found")
            kb_clauses_text = "No additional company clauses were retrieved."
        else:
            kb_clauses_text = "\n\n".join(
                f"Clause {i+1}:\n{doc}"
                for i, doc in enumerate(documents)
            )

        # ---------------- PROMPT BUILDING ----------------
        logger.info("prompt_building_started")

        final_prompt = CONTRACT_PROMPT.format(
            contract_type=contract_type,
            contract_template_text=contract_template_text,
            user_input_json=json.dumps(user_input_data, indent=2),
            regional_law_text=regional_law_text,
            kb_clauses_text=kb_clauses_text,
        )

        # ---------------- GENERATION ----------------
        logger.info("generation_started")

        result = generate_response(final_prompt)

        logger.info("rag_success")
        return result

    except Exception as e:
        logger.error("rag_failed", extra={"error": str(e)})
        raise
