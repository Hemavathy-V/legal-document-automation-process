def build_prompt(query, clauses):

    context = "\n\n".join(clauses)

    return f"""
You are a legal drafting assistant.

User request:
{query}

Relevant clauses:
{context}

Generate a professional legal clause.
"""