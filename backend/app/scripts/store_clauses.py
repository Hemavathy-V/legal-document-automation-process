"""
Script to store clauses into the vector database.
"""
import sys
import pandas as pd
from app.services.embedding_service import generate_embedding
from app.services.clause_service import store_clauses


file_path = sys.argv[1]
df = pd.read_excel(file_path)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

ids, docs, embeds, metas = [], [], [], []

for index, row in df.iterrows():
    text = row["clause_text"] 

    emb = generate_embedding(text)
        
    ids.append(str(index))
    docs.append(text)
    embeds.append(emb)
    metas.append({
        "clause_name": row["clause_name"],
        "clause_type": row["clause_type"],
        "agreement_type": row["agreement_type"],
        "playbook_tier": row["playbook_tier"],
        "jurisdiction": row["jurisdiction"],
        "comments": row["comments"],
        "risk_level": row["risk_level"]
    })

store_clauses(ids, docs, embeds, metas)

print("Clauses stored successfully in chroma!")
