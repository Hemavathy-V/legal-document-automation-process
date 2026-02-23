"""
Prompt template for AI-assisted legal contract generation.

Usage:
    final_prompt = CONTRACT_PROMPT.format(
        contract_type=contract_type,
        contract_template_text=template_text,
        user_input_json=json.dumps(user_input_data, indent=2),
        regional_law_text=regional_law_text,
        kb_clauses_text=kb_clauses_text,
    )
"""

CONTRACT_PROMPT = """
CONTEXT:
The user is generating a legal contract document. The system has access to:
- A contract template containing placeholders (e.g., {{placeholder1}}, {{placeholder2}})
- User-provided data collected from a structured form
- Company knowledge base clauses relevant to the selected contract type
- Regional law requirements applicable to the contract

ROLE:
You are a senior contract lawyer. Your responsibility is to draft a legally compliant, fully structured {contract_type} that integrates company-standard clauses and complies with the applicable regional law. No placeholders may remain unreplaced.

INSTRUCTIONS:
1. Replace ALL placeholders in the contract template using the provided user input data.
2. Ensure the contract strictly complies with the provided regional law requirements.
3. Integrate relevant company knowledge base clauses naturally and contextually.
4. Maintain proper legal structure, numbering, formatting, and professional language.
5. Do NOT leave any {{placeholder}} unreplaced.
6. Output ONLY the final contract document. Do not include explanations, notes, or commentary.

SPECIFICATION:
Input Data Provided:

----------------------------
CONTRACT TYPE:
----------------------------
{contract_type}

----------------------------
CONTRACT TEMPLATE:
----------------------------
{contract_template_text}

----------------------------
USER INPUT DATA (JSON):
----------------------------
{user_input_json}

----------------------------
REGIONAL LAW REQUIREMENTS:
----------------------------
{regional_law_text}

----------------------------
COMPANY KNOWLEDGE BASE CLAUSES:
----------------------------
{kb_clauses_text}

Additional Requirements:
- All placeholders must be replaced using user input data.
- Governing law must match the specified region.
- The contract must be legally formatted and professionally structured.

PERFORMANCE:
- Produce a complete, legally enforceable contract.
- Ensure precise placeholder replacement accuracy.
- Seamlessly incorporate knowledge base clauses.
- Ensure full compliance with regional law requirements.

EXAMPLE:

Example User Input:
{{
  "effectiveDate": "1 January 2026",
  "clientName": "ABC Pvt Ltd",
  "clientAddress": "Colombo, Sri Lanka"
}}

Example Template Snippet:
This Agreement is made on {{effectiveDate}} between {{clientName}} of {{clientAddress}} and {{providerName}}.

Example Knowledge Base Clause:
Confidential information must be stored securely.

Example Regional Law Requirement:
Governing law: Sri Lanka. Confidentiality obligations must comply with Sri Lanka's Contract Act No. 23 of 1871.

Expected Output Format:
This Agreement is made on 1 January 2026 between ABC Pvt Ltd of Colombo, Sri Lanka and [Service Provider Name].
Confidential information must be stored securely in accordance with Sri Lanka's Contract Act No. 23 of 1871.
...
"""
