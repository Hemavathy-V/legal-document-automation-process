import pandas as pd
from backend.app.database.clause_collection import get_clause_collection
from backend.app.services.embedding_service import get_embedding

def store_clauses():
    df = pd.read_excel(r"D:\legal-document-automation\legal-document-automation-process\backend\app\data\clause_lib.xlsx")

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    collection = get_clause_collection()

    for index, row in df.iterrows():
        clause_text = row["clause_text"] 

        embedding = get_embedding(clause_text)
        
        collection.add(
            ids=[str(index)],
            documents=[row["clause_text"]],
            embeddings=[embedding],
            metadatas=[{
                "clause_name": row["clause_name"],
                "clause_type": row["clause_type"],
                "agreement_type": row["agreement_type"],
                "playbook_tier": row["playbook_tier"],
                "jurisdiction": row["jurisdiction"],
                "comments": row["comments"],
                "risk_level": row["risk_level"]
            }]
        )

    print("Clauses stored successfully in chroma!")

if __name__ == "__main__":
    store_clauses()
