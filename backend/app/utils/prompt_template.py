def build_prompt(user_input, clauses):

    context = "\n\n".join(clauses)

    return f"""
You are a legal document drafting assistant.

Use the provided clauses to generate a professional legal document.

User Request:
{user_input}

Relevant Clauses:
{context}

Generate a structured legal document:
"""
