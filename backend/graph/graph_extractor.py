
import json
import re

from backend.llm.llm_service import client


def extract_knowledge(text: str) -> dict:
    """
    Extract entities and relationships from technical text.
    Returns structured data suitable for Neo4j.
    """

    prompt = f"""
You extract knowledge from technical documents.

Identify important technical entities and explicit relationships
between them. Do not invent facts that are not supported by the text.

Return ONLY valid JSON in this exact format:
{{
    "entities": [
        {{
            "name": "Python",
            "type": "Programming Language"
        }}
    ],
    "relationships": [
        {{
            "source": "Python",
            "relation": "USED_FOR",
            "target": "Machine Learning"
        }}
    ]
}}

Rules:
- Include only entities supported by the text.
- Relationship source and target must match entity names.
- Use short, descriptive relationship labels in uppercase
  with underscores.
- If no reliable information exists, return empty lists.
- Do not include Markdown fences or extra explanations.

Document text:
{text[:10000]}
"""

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )

    result_text = response.output_text.strip()

    # Handle a response wrapped in Markdown code fences.
    result_text = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        result_text,
        flags=re.IGNORECASE
    ).strip()

    data = json.loads(result_text)

    if not isinstance(data.get("entities"), list):
        raise ValueError("Invalid entity list returned by the model.")

    if not isinstance(data.get("relationships"), list):
        raise ValueError("Invalid relationship list returned by the model.")

    return data
