import pandas as pd
import uuid

def load_clauses_from_excel(file_path: str):
    df = pd.read_excel(file_path)

    clauses = []
    for _, row in df.iterrows():
        clause = {
            "id": str(uuid.uuid4()),
            "term": row.get("Term"),
            "suggested_term": row.get("Suggested term"),
            "comments": row.get("Comments"),
            "tooltip": row.get("Suggested tooltip"),
        }
        clauses.append(clause)

    return clauses
