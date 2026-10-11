import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_answer(question, context):

    prompt = f"""
You are a helpful technical knowledge assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I could not find enough information in the provided documents."

Do not invent facts.

Context:
{context}

Question:
{question}
"""

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )

    return response.output_text