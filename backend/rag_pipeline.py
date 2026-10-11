from backend.retrieval.embedder import create_embeddings
from backend.retrieval.vector_store import search_documents
from backend.llm.llm_service import generate_answer
from backend.graph.neo4j_graph import Neo4jKnowledgeGraph


def rag_pipeline(question, n_results=3):
    """
    Retrieve relevant information from ChromaDB and Neo4j,
    combine the context, and generate a single answer.

    Returns:
        answer (str): Generated answer.
        sources (list): Sources from documents and the knowledge graph.
    """

    # Step 1: Initialize context and source collections.
    context_parts = []
    sources = []

    # Step 2: Retrieve relevant document chunks from ChromaDB.
    query_embedding = create_embeddings([question])[0]

    results = search_documents(
        query_embedding,
        n_results=n_results
    )

    documents = results.get("documents", [[]])
    metadatas = results.get("metadatas", [[]])

    documents = documents[0] if documents else []
    metadatas = metadatas[0] if metadatas else []

    # Step 3: Add document chunks to the context.
    for i, document in enumerate(documents):
        metadata = (
            metadatas[i]
            if i < len(metadatas) and metadatas[i]
            else {}
        )

        source = metadata.get("source", "Unknown")
        chunk_id = metadata.get("chunk_id", "Unknown")

        context_parts.append(
            f"[Document Source: {source}, Chunk: {chunk_id}]\n"
            f"{document}"
        )

        sources.append({
            "source_type": "document",
            "document": source,
            "chunk_id": chunk_id,
            "text": document
        })

    # Step 4: Retrieve relevant knowledge graph relationships.
    kg = None
    relationships = []

    try:
        kg = Neo4jKnowledgeGraph()

        relationships = kg.search_relationships(
            question,
            limit=10
        )

    except Exception as exc:
        # Preserve document-based RAG if Neo4j is unavailable.
        print(
            "Knowledge graph retrieval failed:",
            type(exc).__name__
        )

    finally:
        if kg is not None:
            kg.close()

    # Step 5: Add graph relationships to the context and sources.
    if relationships:
        graph_context = "\n".join(
            (
                f"{item['source']} "
                f"--{item['relationship']}--> "
                f"{item['target']}"
            )
            for item in relationships
        )

        context_parts.append(
            "[Knowledge Graph Relationships]\n" + graph_context
        )

        for item in relationships:
            sources.append({
                "source_type": "knowledge_graph",
                "source": item["source"],
                "relationship": item["relationship"],
                "target": item["target"]
            })

    # Step 6: Combine document and graph context.
    context = "\n\n".join(context_parts)

    # Step 7: Handle the case where no information was retrieved.
    if not context.strip():
        return (
            "I could not find enough information in the provided "
            "documents or knowledge graph."
        ), []

    # Step 8: Generate one answer using the combined context.
    answer = generate_answer(
        question,
        context
    )

    # Step 9: Return the answer and its sources.
    return answer, sources