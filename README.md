#  Secure Multi-Agent RAG Framework

### Intelligent Technical Knowledge Management

A document-based question-answering system that combines **Retrieval-Augmented Generation (RAG), multi-agent orchestration, vector search, and knowledge graphs** to help users retrieve relevant information from technical documents.

##  Overview

The Secure Multi-Agent RAG Framework allows users to upload technical PDF documents and ask natural-language questions. The system retrieves relevant document content and returns answers with supporting source references.

It uses a multi-agent workflow to route questions and integrates vector-based retrieval with knowledge-graph capabilities for structured relationship discovery.

##  Key Features

- **PDF Document Upload:** Upload technical PDF files to build a searchable knowledge base.
- **Intelligent Question Answering:** Ask natural-language questions about uploaded documents.
- **Retrieval-Augmented Generation:** Retrieve relevant document chunks to ground answers in available information.
- **Multi-Agent Routing:** Route questions through a LangGraph-based workflow.
- **Semantic Search:** Generate embeddings using Sentence Transformers and search using ChromaDB.
- **Knowledge Graph:** Represent entities and relationships using NetworkX and Neo4j.
- **Source References:** Display document sources associated with retrieved answers.
- **Interactive Interface:** Use a Streamlit frontend to upload documents and interact with the assistant.
- **REST API:** Use FastAPI endpoints for document ingestion, retrieval, and question answering.

##  System Architecture

```text
                 User
                   |
                   v
          Streamlit Frontend
                   |
                   v
             FastAPI Backend
                   |
                   v
            Question Router
                   |
          +--------+--------+
          |                 |
          v                 v
     RAG Pipeline      General Agent
          |
          v
   Document Retrieval
          |
          v
       ChromaDB
          |
          v
   Answer + Sources

  Knowledge Graph Layer
     NetworkX / Neo4j
```

*The architecture illustrates the intended system components; graph-based retrieval and agent routing depend on their implemented integration.*

##  Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend API | FastAPI |
| Agent Orchestration | LangGraph |
| Embeddings | Sentence Transformers |
| Vector Database | ChromaDB |
| Knowledge Graph | NetworkX, Neo4j |
| Document Processing | PDF parsing and text chunking |
| Version Control | Git and GitHub |

##  Project Structure

```text
secure-multi-agent-rag/
├── backend/
│   ├── agents/
│   ├── graph/
│   ├── ingestion/
│   ├── llm/
│   ├── retrieval/
│   ├── main.py
│   └── rag_pipeline.py
├── frontend/
│   └── app.py
├── data/
├── chroma_db/
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

##  Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Harshitha824/Secure-Multi-agent-RAG.git
cd Secure-Multi-agent-RAG
```

### 2. Create and activate a virtual environment

**Windows:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add the configuration required by your setup.

```env
OPENAI_API_KEY=your_api_key
NEO4J_URI=your_neo4j_uri
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password
```

Only configure credentials for services your current setup uses. Never commit `.env` or expose API keys and database passwords.

### 5. Start the backend

From the project root:

```bash
uvicorn backend.main:app --reload
```

The FastAPI service should be available at:

`http://127.0.0.1:8000`

API documentation is available at:

`http://127.0.0.1:8000/docs`

### 6. Start the frontend

Open a second terminal in the project root:

```bash
streamlit run frontend/app.py
```

Open the local URL printed in the terminal, usually:

`http://localhost:8501`

##  How to Use

1. Start the FastAPI backend and Streamlit frontend.
2. Upload a technical PDF through the document-management sidebar.
3. Refresh the knowledge-base document list if necessary.
4. Enter a question about the uploaded material.
5. Submit the question and review the generated answer.
6. Inspect the supporting source references.

##  Security Considerations

- Store API keys and database credentials in environment variables.
- Exclude `.env`, virtual environments, and generated databases from version control where appropriate.
- Validate uploaded file types and sizes.
- Avoid logging sensitive document content or credentials.
- Apply authentication and access controls before exposing the application publicly.

##  Testing

The repository includes test modules for selected components, such as document chunking, retrieval, the RAG pipeline, and question routing.

Run the applicable tests from the project root:

```bash
python -m pytest
```

Some tests may require configured environment variables, external services, or additional dependencies.

##  Future Improvements

- Complete knowledge-graph retrieval integration.
- Extract entities and relationships automatically from uploaded documents.
- Combine vector similarity search with graph-based retrieval.
- Improve answer evaluation, retrieval accuracy, and source attribution.
- Add authentication, authorization, and secure deployment.
- Evaluate performance across different document collections and question types.

##  Project Objective

To develop a modular, secure, and extensible technical knowledge assistant that combines semantic document retrieval and multi-agent workflows, with knowledge-graph capabilities for richer contextual understanding.

##  Author

**Harshitha S.**

GitHub: [Harshitha824](https://github.com/Harshitha824)

---

*Built with Python, FastAPI, Streamlit, LangGraph, ChromaDB, and Neo4j.*
