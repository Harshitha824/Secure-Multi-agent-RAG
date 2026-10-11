
from backend.agents.router_agent import route_question


questions = [
    "What is feature engineering?",
    "What is the relationship between two entities?",
    "Hello!"
]

for question in questions:
    route = route_question(question)

    print(f"\nQuestion: {question}")
    print(f"Selected route: {route}")
