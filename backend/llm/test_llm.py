from backend.llm.llm_service import generate_answer


context = """
A feature, also called a predictor variable or input variable,
is an attribute used by a machine learning model to make a prediction.
"""


question = "What is a feature or predictor variable?"


answer = generate_answer(
    question,
    context
)


print("\n" + "=" * 70)
print("QUESTION")
print("=" * 70)

print(question)

print("\n" + "=" * 70)
print("LLM ANSWER")
print("=" * 70)

print(answer)

print("=" * 70)