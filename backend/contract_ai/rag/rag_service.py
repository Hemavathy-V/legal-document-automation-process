from .retrievers.sql_retriever import SQLRetriever
from .prompt_builder import build_prompt
from .llm_client import generate_response

class RAGService:

    def __init__(self):
        self.retriever = SQLRetriever()

    def run(self, user_query: str):

        clauses = self.retriever.retrieve(user_query)

        prompt = build_prompt(user_query, clauses)

        result = generate_response(prompt)

        return result
