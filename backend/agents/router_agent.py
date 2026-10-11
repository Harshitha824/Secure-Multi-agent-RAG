
def route_question(question: str) -> str:
    """
    Decide which processing path should handle a question.
    """

    question = question.lower().strip()

    graph_keywords = [
        "relationship",
        "relationships",
        "related to",
        "related entities",
        "connected to",
        "connection between",
        "connections between",
        "how is",
        "dependency",
        "dependencies",
        "knowledge graph",
        "graph",
        "entity",
        "entities",
        "networkx",
    ]

    document_keywords = [
        "document",
        "pdf",
        "according to",
        "in the file",
        "uploaded file",
        "uploaded document",
        "what is",
        "explain",
        "define",
        "describe",
    ]

    if any(keyword in question for keyword in graph_keywords):
        return "graph"

    if any(keyword in question for keyword in document_keywords):
        return "rag"

    return "general"
