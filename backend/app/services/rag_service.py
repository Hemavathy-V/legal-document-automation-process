def preprocess_clause(clause: dict) -> str:
    formatted_text = f"""
Term: {clause.get('term')}
Suggested Term: {clause.get('suggested_term')}
Comments: {clause.get('comments')}
Tooltip: {clause.get('tooltip')}
""".strip()

    return formatted_text
