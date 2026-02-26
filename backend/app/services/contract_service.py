from pathlib import Path
from datetime import datetime
from backend.app.scripts.dynamic_questions import ContractProcessor

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

TEMPLATES_DIR = PROJECT_ROOT / "sample_templates"
OUTPUT_DIR = BASE_DIR / "output"

processor = ContractProcessor(
    templates_dir=TEMPLATES_DIR,
    output_dir=OUTPUT_DIR
)


def list_templates():
    return processor.list_template_names()


def get_placeholders(template_name):
    return processor.get_template_placeholders(template_name)


def generate_contract(template_name, data):
    output_path = processor.save_contract_data(template_name, data)

    return {
        "message": "Contract data saved successfully",
        "template_name": template_name,
        "file": str(output_path),
        "generated_at": datetime.now().isoformat(),
        "total_fields": processor._count_fields(data),
    }