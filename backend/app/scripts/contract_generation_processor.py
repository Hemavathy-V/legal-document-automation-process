import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from docx import Document

from backend.app.core.logger import get_logger
from backend.app.database.db_connection import get_connection
from backend.app.services.retriever import retrieve_clauses


logger = get_logger(__name__)


class ContractGenerationProcessor:
    def __init__(self, templates_dir: Path, output_dir: Path):
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)

    def _count_fields(self, data: Dict[str, Any]) -> int:
        count = 0
        for value in data.values():
            if isinstance(value, list):
                count += sum(len(item) if isinstance(item, dict) else 1 for item in value)
            else:
                count += 1
        return count

    def get_template_path(self, template_name: str) -> Optional[Path]:
        normalized_name = template_name.strip()
        if not normalized_name:
            return None

        normalized_name = normalized_name.replace(" ", "-")
        template_file = normalized_name if normalized_name.lower().endswith(".docx") else f"{normalized_name}.docx"
        template_path = self.templates_dir / template_file
        if template_path.exists():
            return template_path
        return None

    def get_template_path_by_contract_type(self, contract_type: str) -> Optional[Path]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT file_path
                FROM contract_templates
                WHERE UPPER(template_type) = UPPER(%s)
                ORDER BY id DESC
                LIMIT 1
                """,
                (contract_type,),
            )
            row = cursor.fetchone()
            if row and row.get("file_path"):
                db_path = Path(row["file_path"])
                if db_path.is_absolute() and db_path.exists():
                    return db_path

                repo_root = self.templates_dir.parent
                resolved = (repo_root / db_path).resolve()
                if resolved.exists():
                    return resolved

            return self.get_template_path(contract_type)
        finally:
            cursor.close()
            conn.close()

    def get_filename_by_id(self, contract_id: int) -> Tuple[str, str]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT ct.lookup_value AS contract_type
                FROM contracts c
                JOIN look_up ct ON c.contract_type_id = ct.lookup_id
                WHERE c.contract_id = %s
                """,
                (contract_id,),
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Contract ID {contract_id} not found")

            contract_type = row["contract_type"]

            cursor.execute(
                """
                SELECT json_file_path, json_file_name
                FROM contract_input_json_metadata
                WHERE contract_id = %s
                ORDER BY is_latest DESC, created_at DESC, metadata_id DESC
                LIMIT 1
                """,
                (contract_id,),
            )
            metadata_row = cursor.fetchone()
            if metadata_row:
                metadata_name = metadata_row.get("json_file_name")
                metadata_path = metadata_row.get("json_file_path")

                if metadata_name:
                    metadata_file = self.output_dir / metadata_name
                    if metadata_file.exists():
                        logger.info(
                            f"Resolved JSON from metadata for contract_id={contract_id} | "
                            f"filename={metadata_file.name}"
                        )
                        return metadata_file.name, contract_type

                if metadata_path:
                    path_obj = Path(metadata_path)
                    if path_obj.is_absolute() and path_obj.exists():
                        logger.info(
                            f"Resolved JSON from metadata absolute path for contract_id={contract_id} | "
                            f"filename={path_obj.name}"
                        )
                        return path_obj.name, contract_type

                    rel_candidate = (self.templates_dir.parent / path_obj).resolve()
                    if rel_candidate.exists():
                        logger.info(
                            f"Resolved JSON from metadata relative path for contract_id={contract_id} | "
                            f"filename={rel_candidate.name}"
                        )
                        return rel_candidate.name, contract_type

            cursor.execute(
                """
                SELECT file_path
                FROM contract_templates
                WHERE UPPER(template_type) = UPPER(%s)
                ORDER BY id DESC
                LIMIT 1
                """,
                (contract_type,),
            )
            template_row = cursor.fetchone()

            candidate_files: List[Path] = []
            if template_row and template_row.get("file_path"):
                stem = Path(template_row["file_path"]).stem
                candidate_files.extend(sorted(self.output_dir.glob(f"{stem}_*.json"), reverse=True))

            if not candidate_files:
                normalized_type = contract_type.replace(" ", "-")
                candidate_files.extend(sorted(self.output_dir.glob(f"*{normalized_type}*.json"), reverse=True))

            if not candidate_files:
                candidate_files.extend(sorted(self.output_dir.glob("*.json"), reverse=True))

            if not candidate_files:
                raise FileNotFoundError("No saved contract JSON files found in output directory")

            selected = candidate_files[0]
            logger.info(
                f"Resolved contract JSON for contract_id={contract_id} | "
                f"contract_type={contract_type} | filename={selected.name}"
            )
            return selected.name, contract_type
        finally:
            cursor.close()
            conn.close()

    def save_json_metadata(
        self,
        contract_id: int,
        template_name: str,
        output_path: Path,
        data: Dict[str, Any],
    ) -> None:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT ct.lookup_value AS contract_type, c.created_by
                FROM contracts c
                JOIN look_up ct ON c.contract_type_id = ct.lookup_id
                WHERE c.contract_id = %s
                """,
                (contract_id,),
            )
            contract_row = cursor.fetchone()
            if not contract_row:
                raise ValueError(f"Contract ID {contract_id} not found for metadata save")

            contract_type_from_contract = contract_row["contract_type"]
            created_by = contract_row["created_by"]

            normalized_template_name = template_name.strip()

            cursor.execute(
                """
                SELECT id, template_type
                FROM contract_templates
                WHERE UPPER(template_name) = UPPER(%s)
                   OR UPPER(REPLACE(template_name, ' ', '-')) = UPPER(%s)
                ORDER BY id DESC
                LIMIT 1
                """,
                (normalized_template_name, normalized_template_name),
            )
            template_row = cursor.fetchone()

            if not template_row:
                cursor.execute(
                    """
                    SELECT id, template_type
                    FROM contract_templates
                    WHERE UPPER(REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(file_path, '/', -1), '.', 1), ' ', '-')) = UPPER(%s)
                    ORDER BY id DESC
                    LIMIT 1
                    """,
                    (normalized_template_name,),
                )
                template_row = cursor.fetchone()

            template_id = template_row["id"] if template_row else None
            contract_type = (
                template_row["template_type"]
                if template_row and template_row.get("template_type")
                else contract_type_from_contract
            )

            if contract_type != contract_type_from_contract:
                logger.warning(
                    f"Contract type mismatch for contract_id={contract_id}: "
                    f"contracts.type={contract_type_from_contract}, template.type={contract_type}. "
                    f"Using template.type for metadata save."
                )

            json_file_name = output_path.name
            json_file_path = str(output_path)
            payload_sha256 = hashlib.sha256(
                json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")
            ).hexdigest()
            total_fields = self._count_fields(data)

            cursor.execute(
                """
                UPDATE contract_input_json_metadata
                SET is_latest = 0
                WHERE contract_id = %s
                """,
                (contract_id,),
            )

            cursor.execute(
                """
                INSERT INTO contract_input_json_metadata (
                    contract_id,
                    template_id,
                    created_by,
                    template_name,
                    contract_type,
                    json_file_name,
                    json_file_path,
                    input_payload_json,
                    total_fields,
                    payload_sha256,
                    is_latest
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
                """,
                (
                    contract_id,
                    template_id,
                    created_by,
                    template_name,
                    contract_type,
                    json_file_name,
                    json_file_path,
                    json.dumps(data, ensure_ascii=False),
                    total_fields,
                    payload_sha256,
                ),
            )
            conn.commit()
            logger.info(
                f"Saved JSON metadata for contract_id={contract_id} | file={json_file_name} | "
                f"fields={total_fields}"
            )
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def update_contract_status(self, contract_id: int, status: str) -> None:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT lookup_id
                FROM look_up
                WHERE lookup_type = 'status' AND LOWER(lookup_value) = LOWER(%s)
                LIMIT 1
                """,
                (status,),
            )
            status_row = cursor.fetchone()

            if status_row:
                status_id = status_row["lookup_id"]
            else:
                cursor.execute(
                    """
                    INSERT INTO look_up (lookup_type, lookup_value)
                    VALUES ('status', %s)
                    """,
                    (status,),
                )
                status_id = cursor.lastrowid

            cursor.execute(
                """
                UPDATE contracts
                SET status_id = %s
                WHERE contract_id = %s
                """,
                (status_id, contract_id),
            )

            if cursor.rowcount == 0:
                raise ValueError(f"Contract ID {contract_id} not found for status update")

            conn.commit()
            logger.info(f"Updated contract_id={contract_id} status to '{status}'")
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def extract_template_text(self, template_path: Path) -> str:
        document = Document(template_path)
        text = "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text)
        return text.strip()

    def get_regional_law_text(self, contract_type: str) -> str:
        law_map = {
            "NDA": "Ensure confidentiality, term, remedies, and governing law provisions are legally enforceable in the applicable jurisdiction.",
            "MSA": "Ensure scope, payment terms, liability limitations, IP ownership, and dispute resolution are compliant with applicable commercial contract law.",
            "SOW": "Ensure deliverables, milestones, acceptance criteria, and change-control terms are precise and legally enforceable.",
            "Service Agreement": "Ensure services scope, service levels, payment obligations, confidentiality, and termination rights comply with contract law.",
            "Termination Agreement": "Ensure release terms, surviving obligations, and final settlement clauses are enforceable and clear.",
        }
        return law_map.get(
            contract_type,
            "Ensure the contract complies with applicable commercial and contract law in the chosen jurisdiction.",
        )

    def get_kb_clauses(self, contract_type: str) -> str:
        try:
            retrieved = retrieve_clauses(f"{contract_type} legal company clause", top_k=5)
            if not retrieved:
                return ""
            return "\n\n".join(retrieved)
        except Exception as exc:
            logger.warning(f"KB clause retrieval failed for {contract_type}: {str(exc)}")
            return ""
