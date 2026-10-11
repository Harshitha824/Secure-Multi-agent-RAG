from embedder import create_embeddings


texts = [
    "Machine learning uses input features.",
    "A feature is an input variable used by a model.",
    "The weather is sunny today."
]


embeddings = create_embeddings(texts)


print("\nEmbeddings created successfully!")
print("-" * 50)

print("Number of texts:", len(embeddings))
print("Vector dimensions:", len(embeddings[0]))

print("\nFirst vector:")
print(embeddings[0])

print("-" * 50)