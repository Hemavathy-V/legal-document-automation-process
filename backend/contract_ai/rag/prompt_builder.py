def build_prompt(user_query, clauses):

    context = ""

    for i, clause in enumerate(clauses):
        context += f"""
Clause {i+1}
Title: {clause[0]}
Category: {clause[2]}
Text:
{clause[1]}

"""

    prompt = f"""
You are a senior legal contract drafting assistant.

User Requirement:
{user_query}

Retrieved Clauses:
{context}

Instructions:
- Adapt clauses properly
- Ensure legal consistency
- Avoid contradictions
- Maintain professional format

Generate final contract section:
"""

    return prompt
