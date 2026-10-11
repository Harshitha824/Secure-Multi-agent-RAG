
from pathlib import Path
import uuid

from backend.ingestion.pdf_loader import extract_text
from backend.ingestion.chunker import create_chunks
from backend.retrieval.embedder import create_embeddings
from backend.retrieval.vector_store import collection
from backend.graph.graph_extractor import extract_knowledge
from backend.graph.neo4j_graph import Neo4jKnowledgeGraph


PROJECT_ROOT = Path(__file__).resolve().parents[2]
UPLOAD_DIR = PROJECT_ROOT / "data" / "documents"


def ingest_pdf(file_path: str, original_filename: str):
    """
    Extract a PDF's text, split it into chunks,
    create embeddings, and store it in ChromaDB.
    """

    text = extract_text(file_path)

    if not text.strip():
        raise ValueError("The PDF contains no extractable text.")

    chunks = create_chunks(text)

    embeddings = create_embeddings(chunks)

    document_id = str(uuid.uuid4())

    ids = [
        f"{document_id}_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "source": original_filename,
            "document_id": document_id,
            "chunk_id": i
        }
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    
    # Extract knowledge from the PDF and store it in Neo4j.
    graph_status = "not attempted"
    kg = None

    try:
        knowledge = extract_knowledge(text)

        kg = Neo4jKnowledgeGraph()
        kg.add_knowledge(knowledge)

        graph_status = "success"

    except Exception as exc:
        # Keep successful vector ingestion even if graph extraction fails.
        graph_status = f"failed: {type(exc).__name__}"

    finally:
        if kg is not None:
            kg.close()

    return {
        "message": "PDF processed successfully.",
        "document_id": document_id,
        "filename": original_filename,
        "chunks_created": len(chunks),
        "graph_status": graph_status
    }

