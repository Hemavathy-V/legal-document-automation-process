from backend.contract_ai.rag.rag_service import RAGService

if __name__ == "__main__":
    rag = RAGService()
    user_input = input("Enter contract requirement: ")
    output = rag.run(user_input)
    print(output)
