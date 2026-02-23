import pandas as pd
from app.services.embedding_service import get_embedding
from app.database.chroma_db import collection

print("File loaded successfully")

def embed_excel(file_path: str):
    df = pd.read_excel(file_path)

    print("Columns in Excel:")
    print(df.columns.tolist())

    return

def embed_excel(file_path: str):
    df = pd.read_excel(file_path)
    
    df.columns = df.columns.str.strip()


    for index, row in df.iterrows():
        clause_text = str(row["Clause Text"])  # column name

        embedding = get_embedding(clause_text)

        collection.add(
            documents=[clause_text],
            embeddings=[embedding],
            ids=[str(index)],
            metadatas=[{
                "clause_name": str(row["Clause Name"]),
                "clause_type": str(row["Clause Type"]),
                "playbook_tier": str(row["Playbook Tier"]),
                "jurisdiction": str(row["Jurisdiction"])
            }]
        )

        print(f"Embedded clause {index}")

    print("Clauses embedded successfully!")

if __name__ == "__main__":
    print("Starting embedding process...")
    embed_excel("clause_lib.xlsx")