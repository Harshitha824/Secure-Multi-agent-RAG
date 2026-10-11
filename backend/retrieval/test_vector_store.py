from pathlib import Path

from backend.ingestion.pdf_loader import extract_text
from backend.ingestion.chunker import create_chunks
from backend.retrieval.embedder import create_embeddings
from backend.retrieval.vector_store import add_documents, search_documents


# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# PDF location
PDF_PATH = PROJECT_ROOT / "data" / "documents" / "sample.pdf"


# --------------------------------------------------
# 1. Extract text
# --------------------------------------------------

text = extract_text(str(PDF_PATH))


# --------------------------------------------------
# 2. Create chunks
# --------------------------------------------------

chunks = create_chunks(text)


print("\nPDF processed successfully!")
print("Total chunks:", len(chunks))


# --------------------------------------------------
# 3. Create embeddings
# --------------------------------------------------

embeddings = create_embeddings(chunks)


print("Embeddings created successfully!")
print("Embedding dimensions:", len(embeddings[0]))


# --------------------------------------------------
# 4. Store in ChromaDB
# --------------------------------------------------

add_documents(
    chunks,
    embeddings,
    source="sample.pdf"
)


# --------------------------------------------------
# 5. Test semantic search
# --------------------------------------------------

query = "What is a feature or predictor variable?"


query_embedding = create_embeddings([query])[0]


results = search_documents(
    query_embedding,
    n_results=3
)


# --------------------------------------------------
# 6. Display results
# --------------------------------------------------

print("\n")
print("=" * 70)
print("SEARCH QUERY:")
print(query)
print("=" * 70)


for i, document in enumerate(results["documents"][0]):

    print(f"\nRESULT {i + 1}")
    print("-" * 70)
    print(document)
    print("-" * 70)