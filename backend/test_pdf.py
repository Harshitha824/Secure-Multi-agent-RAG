from pathlib import Path
from ingestion.pdf_loader import extract_text


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "data" / "documents" / "sample.pdf"

text = extract_text(str(PDF_PATH))

print("\nPDF loaded successfully!")
print("-" * 50)
print(text[:2000])
print("-" * 50)