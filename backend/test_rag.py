
from backend.rag_pipeline import rag_pipeline


question = "What is a feature or predictor variable?"

answer, sources = rag_pipeline(question)

print("\n" + "=" * 70)
print("QUESTION")
print("=" * 70)
print(question)

print("\n" + "=" * 70)
print("ANSWER")
print("=" * 70)
print(answer)

print("\n" + "=" * 70)
print("SOURCE CITATIONS")
print("=" * 70)

for i, source in enumerate(sources, start=1):
    print(f"\nSource {i}")
    print("Document:", source["document"])
    print("Chunk ID:", source["chunk_id"])
    print("Retrieved text:", source["text"][:300])
    print("-" * 70)
