def preprocess_clause(clause: dict) -> str:
    text = clause["text"] if clause["text"] else ""

    formatted_text = f"""
Clause Type: {clause.get('clause_type')}
Title: {clause.get('title')}
Jurisdiction: {clause.get('jurisdiction')}

Content:
{text.strip()}
"""
    return formatted_text
