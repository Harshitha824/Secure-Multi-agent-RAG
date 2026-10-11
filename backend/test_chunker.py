from pathlib import Path

from ingestion.pdf_loader import extract_text
from ingestion.chunker import create_chunks


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PDF_PATH = PROJECT_ROOT / "data" / "documents" / "sample.pdf"


# Extract text from PDF
text = extract_text(str(PDF_PATH))


# Create chunks
chunks = create_chunks(text)


print("\nPDF processed successfully!")
print(f"Total characters: {len(text)}")
print(f"Total chunks: {len(chunks)}")

print("\nFirst chunk:")
print("-" * 60)
print(chunks[0])
print("-" * 60)

print("\nSecond chunk:")
print("-" * 60)
print(chunks[1])
print("-" * 60)