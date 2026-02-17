import pandas as pd

def load_clauses_from_excel(file_path: str):
    df = pd.read_excel(file_path)

    clauses = []
    for _, row in df.iterrows():
        clause = {
            "id": str(row.get("id")),
            "clause_type": row.get("clause_type"),
            "title": row.get("title"),
            "jurisdiction": row.get("jurisdiction"),
            "text": row.get("text"),
            "tags": row.get("tags"),
        }
        clauses.append(clause)

    return clauses
