
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel

from backend.agents.rag_graph import run_agent
from backend.ingestion.ingest_service import ingest_pdf
from backend.retrieval.vector_store import collection


app = FastAPI(
    title="Secure Multi-Agent RAG API",
    description="API for technical knowledge retrieval and question answering",
    version="1.0.0"
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPLOAD_DIR = PROJECT_ROOT / "data" / "documents"

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

class QuestionRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Validate the file extension
    if Path(file.filename or "").suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Generate a unique server-side filename
    document_id = str(uuid4())
    saved_path = UPLOAD_DIR / f"{document_id}.pdf"

    try:
        content = await file.read(MAX_FILE_SIZE + 1)

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="PDF must be 10 MB or smaller."
            )

        # Check the PDF file signature
        if not content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is not a valid PDF."
            )

        saved_path.write_bytes(content)

        result = ingest_pdf(
            str(saved_path),
            file.filename or "uploaded.pdf"
        )

        return result

    except HTTPException:
        raise

    except Exception:
        saved_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail="PDF processing failed. Check the backend terminal."
        )

    finally:
        await file.close()

@app.get("/documents")
def list_documents():
    records = collection.get(
        include=["metadatas"]
    )

    documents = {}

    for metadata in records["metadatas"] or []:
        if not metadata:
            continue

        document_id = metadata.get("document_id")

        # Support older chunks without document IDs
        if not document_id:
            document_id = metadata.get("source", "unknown")

        if document_id not in documents:
            documents[document_id] = {
                "document_id": document_id,
                "filename": metadata.get("source", "unknown"),
                "chunks": 0
            }

        documents[document_id]["chunks"] += 1

    return {
        "total_documents": len(documents),
        "documents": list(documents.values())
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        result = run_agent(request.question)

        answer = result["answer"]
        sources = result.get("sources", [])

        return {
            "question": request.question,
            "answer": answer,
            "sources": sources
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your question."
        )
