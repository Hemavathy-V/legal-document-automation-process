import json
from pathlib import Path
from typing import Dict

from docx import Document

from backend.app.core.gemini_client import get_gemini_model
from backend.app.core.logger import get_logger
from backend.app.prompts.legal_contract_prompt import CONTRACT_PROMPT


logger = get_logger(__name__)


class ContractGenerationService:
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.model = get_gemini_model()

    def load_json(self, json_path: Path) -> Dict:
        with open(json_path, "r", encoding="utf-8") as file_obj:
            return json.load(file_obj)

    def build_prompt(
        self,
        contract_type: str,
        template_text: str,
        user_input_data: dict,
        regional_law_text: str,
        kb_clauses_text: str,
    ) -> str:
        return CONTRACT_PROMPT.format(
            contract_type=contract_type,
            contract_template_text=template_text,
            user_input_json=json.dumps(user_input_data, indent=2, ensure_ascii=False),
            regional_law_text=regional_law_text,
            kb_clauses_text=kb_clauses_text,
        )

    def _validate_generated_contract(self, generated_text: str) -> str:
        if not generated_text or not generated_text.strip():
            raise ValueError("Gemini returned empty response")

        cleaned_text = generated_text.strip()
        if "{{" in cleaned_text or "}}" in cleaned_text:
            raise ValueError("Generated contract still contains unresolved placeholders")

        if len(cleaned_text) < 200:
            raise ValueError("Generated contract response is too short to be valid")

        return cleaned_text

    def generate_contract(self, prompt: str) -> str:
        logger.debug(f"Prompt length: {len(prompt)}")

        last_error = None
        for attempt in range(2):
            try:
                logger.info(f"Calling Gemini for contract generation (attempt {attempt + 1}/2)")
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.2,
                        "max_output_tokens": 4096,
                    },
                )

                response_text = getattr(response, "text", None)
                if not response_text and getattr(response, "candidates", None):
                    parts = getattr(response.candidates[0].content, "parts", [])
                    response_text = "".join(getattr(part, "text", "") for part in parts)

                return self._validate_generated_contract(response_text or "")
            except Exception as exc:
                last_error = exc
                logger.warning(f"Gemini generation attempt failed: {str(exc)}")

        raise RuntimeError(f"Gemini generation failed after retries: {last_error}")

    def save_generated_contract(self, contract_id: int, text: str) -> Path:
        filename = f"generated_contract_{contract_id}.docx"
        path = self.output_dir / filename

        document = Document()
        for block in text.split("\n\n"):
            normalized = block.strip()
            if normalized:
                document.add_paragraph(normalized)

        document.save(path)
        logger.info(f"Generated contract DOCX saved at {path}")
        return path
