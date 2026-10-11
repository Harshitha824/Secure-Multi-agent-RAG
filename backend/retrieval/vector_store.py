import chromadb


# Create a local ChromaDB client
client = chromadb.PersistentClient(
    path="chroma_db"
)


# Create or load our collection
collection = client.get_or_create_collection(
    name="technical_knowledge"
)


def add_documents(chunks, embeddings, source):
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    metadatas = [
        {
            "source": source,
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

    print(f"Added {len(chunks)} chunks to ChromaDB.")


def search_documents(query_embedding, n_results=3):
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )

    return results