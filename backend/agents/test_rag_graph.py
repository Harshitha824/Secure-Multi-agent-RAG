
from backend.agents.rag_graph import run_agent


questions = [
    "What is feature engineering?",
    "Hello!"
]

for question in questions:
    print("\n" + "=" * 60)
    print("QUESTION:", question)

    result = run_agent(question)

    print("ROUTE:", result["route"])
    print("ANSWER:", result["answer"])
    print("SOURCES:", len(result.get("sources", [])))
