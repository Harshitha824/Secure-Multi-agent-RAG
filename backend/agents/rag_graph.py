
from typing import TypedDict, Literal

from langgraph.graph import StateGraph, START, END

from backend.agents.router_agent import route_question
from backend.rag_pipeline import rag_pipeline
from backend.graph.neo4j_graph import Neo4jKnowledgeGraph


class AgentState(TypedDict, total=False):
    question: str
    route: str
    answer: str
    sources: list


def router_node(state: AgentState):
    """Choose the processing path for a question."""

    route = route_question(state["question"])

    return {
        "route": route
    }


def rag_node(state: AgentState):
    """Answer a question using the existing RAG pipeline."""

    answer, sources = rag_pipeline(state["question"])

    return {
        "answer": answer,
        "sources": sources
    }


def graph_node(state: AgentState):
    """Answer questions using Neo4j knowledge graph relationships."""

    kg = Neo4jKnowledgeGraph()

    try:
        relationships = kg.search_relationships(state["question"])
    finally:
        kg.close()

    if not relationships:
        return {
            "answer": (
                "I couldn't find a matching relationship in the "
                "knowledge graph. Try uploading relevant documents "
                "or asking a more specific question."
            ),
            "sources": []
        }

    details = [
        f"{item['source']} --{item['relationship']}--> {item['target']}"
        for item in relationships
    ]

    return {
    "answer": "Relevant knowledge graph relationships:\n"
              + "\n".join(details),
    "sources": [
        {
            "source_type": "knowledge_graph",
            "source": item["source"],
            "relationship": item["relationship"],
            "target": item["target"]
        }
        for item in relationships
    ]
}



def general_node(state: AgentState):
    """Handle general questions without document retrieval."""

    return {
        "answer": (
            "Hello! I am your technical knowledge assistant. "
            "Ask me a question about your uploaded documents."
        ),
        "sources": []
    }



def select_route(state: AgentState) -> Literal["rag", "graph", "general"]:
    """Select the next workflow node."""

    if state["route"] == "graph":
        return "graph"

    if state["route"] == "rag":
        return "rag"

    return "general"




workflow = StateGraph(AgentState)

workflow.add_node("router", router_node)
workflow.add_node("rag", rag_node)
workflow.add_node("graph", graph_node)
workflow.add_node("general", general_node)

workflow.add_edge(START, "router")

workflow.add_conditional_edges(
    "router",
    select_route,
    {
        "rag": "rag",
        "graph": "graph",
        "general": "general"
    }
)

workflow.add_edge("rag", END)
workflow.add_edge("graph", END)
workflow.add_edge("general", END)

rag_agent_graph = workflow.compile()



def run_agent(question: str):
    """Run the LangGraph workflow."""

    result = rag_agent_graph.invoke({
        "question": question
    })

    return result
