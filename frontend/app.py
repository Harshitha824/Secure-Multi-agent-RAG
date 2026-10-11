
import os

import requests
import streamlit as st

# Chat history for the current session
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Initialize conversation history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Secure Multi-Agent RAG",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. CONFIGURATION
# ============================================================

API_BASE_URL = os.getenv(
    "RAG_API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

REQUEST_TIMEOUT = 120


# ============================================================
# 3. CUSTOM THEME AND CSS
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --soft-white: #E8E9DF;
        --sage-green: #A9B887;
        --deep-olive: #2E3D28;
        --card-white: #F5F5ED;
        --muted-olive: #647254;
    }

    /* Main application */
    .stApp {
        background-color: var(--soft-white);
        color: var(--deep-olive);
    }

    [data-testid="stHeader"] {
        background-color: var(--soft-white);
    }

    [data-testid="stMain"] {
        background-color: var(--soft-white);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--sage-green);
        border-right: 1px solid rgba(46, 61, 40, 0.15);
    }

    section[data-testid="stSidebar"] * {
        color: var(--deep-olive);
    }

    /* Headings */
    h1, h2, h3 {
        color: var(--deep-olive) !important;
        letter-spacing: -0.5px;
    }

    p, label, li {
        color: var(--deep-olive);
    }

    /* Custom logo */
    .brand {
        display: flex;
        align-items: center;
        gap: 16px;
        margin: 8px 0 10px 0;
    }

    .brand-icon {
        width: 62px;
        height: 62px;
        min-width: 62px;
        border-radius: 17px;
        background: var(--deep-olive);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 5px 12px rgba(46, 61, 40, 0.12);
    }

    .brand-title {
        color: var(--deep-olive);
        font-size: clamp(1.45rem, 3vw, 2.15rem);
        font-weight: 750;
        line-height: 1.2;
        margin: 0;
    }

    .brand-subtitle {
        color: var(--muted-olive);
        font-size: 0.94rem;
        margin: 7px 0 0 0;
    }

    /* Cards */
    .info-card {
        background: var(--card-white);
        border: 1px solid rgba(46, 61, 40, 0.12);
        border-radius: 15px;
        padding: 18px 20px;
        margin: 10px 0 18px 0;
    }

    .section-label {
        color: var(--deep-olive);
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .muted-text {
        color: var(--muted-olive);
        font-size: 0.9rem;
    }

    /* Upload area */
    section[data-testid="stFileUploader"] {
        background: var(--card-white);
        border-radius: 14px;
        padding: 12px;
        border: 1px solid rgba(46, 61, 40, 0.12);
    }

    section[data-testid="stFileUploaderDropzone"] {
        background: var(--soft-white);
        border: 2px dashed var(--deep-olive);
        border-radius: 12px;
    }

    section[data-testid="stFileUploaderDropzone"] * {
        color: var(--deep-olive) !important;
    }

    /* Text input and question box */
    .stTextArea textarea,
    .stTextInput input {
        background: var(--card-white) !important;
        color: var(--deep-olive) !important;
        border: 1px solid var(--sage-green) !important;
        border-radius: 11px !important;
    }

    .stTextArea textarea:focus,
    .stTextInput input:focus {
        border-color: var(--deep-olive) !important;
        box-shadow: 0 0 0 1px var(--deep-olive) !important;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {
        background: var(--deep-olive);
        color: var(--soft-white) !important;
        border: 1px solid var(--deep-olive);
        border-radius: 10px;
        min-height: 42px;
        font-weight: 650;
        transition: 0.2s ease;
    }

    .stButton > button p,
    .stDownloadButton > button p {
        color: var(--soft-white) !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: var(--sage-green);
        color: var(--deep-olive) !important;
        border-color: var(--deep-olive);
    }

    .stButton > button:hover p,
    .stDownloadButton > button:hover p {
        color: var(--deep-olive) !important;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background: var(--card-white);
        border: 1px solid rgba(46, 61, 40, 0.15);
        border-radius: 12px;
    }

    /* Alerts */
    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Divider and footer */
    hr {
        border-color: var(--sage-green);
    }

    .app-footer {
        color: var(--muted-olive);
        font-size: 0.82rem;
        text-align: center;
        padding: 20px 0 8px 0;
    }

    /* Hide Streamlit's default footer */
    footer {
        visibility: hidden;
    }

    /* Responsive logo */
    @media (max-width: 600px) {
        .brand {
            align-items: flex-start;
            gap: 12px;
        }

        .brand-icon {
            width: 48px;
            height: 48px;
            min-width: 48px;
            border-radius: 13px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. CUSTOM LOGO AND BRANDING
# ============================================================

def render_logo():
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">
                <svg
                    width="39"
                    height="39"
                    viewBox="0 0 40 40"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <g
                        stroke="#E8E9DF"
                        stroke-width="2"
                        stroke-linecap="round"
                    >
                        <path d="M10 10 L20 20 L30 10"/>
                        <path d="M10 10 L10 30 L20 20"/>
                        <path d="M20 20 L30 30 L10 30"/>
                        <path d="M20 20 L20 35"/>
                    </g>
                    <g fill="#A9B887">
                        <circle cx="10" cy="10" r="4"/>
                        <circle cx="30" cy="10" r="4"/>
                        <circle cx="20" cy="20" r="4"/>
                        <circle cx="10" cy="30" r="4"/>
                        <circle cx="30" cy="30" r="4"/>
                        <circle cx="20" cy="35" r="3"/>
                    </g>
                </svg>
            </div>
            <div>
                <div class="brand-title">
                    Secure Multi-Agent RAG
                </div>
                <div class="brand-subtitle">
                    Intelligent Technical Knowledge Management
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 5. API HELPERS
# ============================================================

def upload_document(uploaded_file):
    """Send a PDF to the FastAPI document upload endpoint."""

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf",
        )
    }

    return requests.post(
        f"{API_BASE_URL}/upload",
        files=files,
        timeout=REQUEST_TIMEOUT,
    )


def ask_question(question):
    """Send a question to the FastAPI RAG/agent endpoint."""

    return requests.post(
        f"{API_BASE_URL}/ask",
        json={"question": question},
        timeout=REQUEST_TIMEOUT,
    )


def get_documents():
    """Retrieve the document list when the backend supports it."""

    return requests.get(
        f"{API_BASE_URL}/documents",
        timeout=30,
    )


def extract_error_message(response):
    """Return a readable API error message."""

    try:
        data = response.json()

        if isinstance(data, dict):
            detail = data.get("detail") or data.get("message")

            if detail:
                return str(detail)

        return str(data)

    except (ValueError, requests.exceptions.JSONDecodeError):
        return response.text or "The server returned an error."


# ============================================================
# 6. SIDEBAR: DOCUMENT MANAGEMENT
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 8px 0 16px 0;">
            <div style="
                font-size: 1.35rem;
                font-weight: 750;
                color: #2E3D28;
            ">
                Document Management
            </div>
            <div style="
                font-size: 0.88rem;
                color: #2E3D28;
                margin-top: 6px;
            ">
                Add technical PDFs to your knowledge base.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Upload a document")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        accept_multiple_files=False,
        help="Select a PDF document to add to your knowledge base.",
        key="pdf_uploader",
    )

    st.caption("PDF files only. The backend enforces the actual size limit.")

    upload_clicked = st.button(
        "Upload PDF",
        use_container_width=True,
        disabled=uploaded_file is None,
        key="upload_pdf_button",
    )

    if upload_clicked and uploaded_file is not None:
        if not uploaded_file.name.lower().endswith(".pdf"):
            st.error("Please select a PDF file.")
        else:
            try:
                with st.spinner("Uploading and processing your PDF..."):
                    response = upload_document(uploaded_file)

                if response.ok:
                    try:
                        upload_result = response.json()
                    except ValueError:
                        upload_result = {}

                    st.success("Document uploaded successfully!")

                    if isinstance(upload_result, dict):
                        message = (
                            upload_result.get("message")
                            or upload_result.get("filename")
                            or upload_result.get("document")
                        )

                        if message:
                            st.caption(str(message))

                    st.session_state["last_uploaded_file"] = uploaded_file.name

                else:
                    st.error(
                        f"Upload failed ({response.status_code}): "
                        f"{extract_error_message(response)}"
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to the backend. "
                    "Make sure the FastAPI server is running on port 8000."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "The upload took too long. Check the backend terminal "
                    "before trying again."
                )

            except requests.exceptions.RequestException as exc:
                st.error(f"Upload request failed: {exc}")

    st.divider()

    st.markdown("#### Knowledge base")

    if st.button(
    "↻ Refresh document list",
    use_container_width=True,
    key="refresh_documents",
):
        st.session_state["should_refresh_documents"] = True

    if st.session_state.get("should_refresh_documents", False):
        try:
            with st.spinner("Loading documents..."):
                documents_response = get_documents()

            if documents_response.ok:
                documents_data = documents_response.json()

                st.success("Document list loaded.")

                if isinstance(documents_data, dict):
                    document_items = (
                        documents_data.get("documents")
                        or documents_data.get("items")
                        or documents_data.get("files")
                    )
                else:
                    document_items = documents_data

                if isinstance(document_items, list) and document_items:
                    for index, document in enumerate(document_items, start=1):
                        with st.expander(f"Document {index}"):
                            if isinstance(document, dict):
                                st.json(document)
                            else:
                                st.write(document)

                elif document_items == []:
                    st.info("No documents are listed yet.")

                else:
                    st.json(documents_data)

            else:
                st.warning(
                    "The document-list endpoint did not return a successful "
                    f"response ({documents_response.status_code})."
                )

        except requests.exceptions.RequestException:
            st.warning(
                "Could not load the document list. "
                "You can still use the upload and question sections."
            )

    st.markdown("---")

    st.markdown(
        """
        <div style="
            font-size: 0.82rem;
            line-height: 1.8;
            color: #2E3D28;
        ">
            <strong>System components</strong><br>
            FastAPI · ChromaDB · Neo4j<br>
            Sentence Transformers · LangGraph
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 7. MAIN PAGE HEADER
# ============================================================

render_logo()

st.markdown(
    """
    <div class="info-card">
        <div class="section-label">
            Your technical knowledge, connected.
        </div>
        <div class="muted-text">
            Upload technical documents and ask questions.
            The assistant retrieves relevant information and returns
            an answer with supporting sources when available.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Start a fresh conversation
if st.button("New Chat", key="new_chat"):
    st.session_state["question_input"] = ""
    st.session_state.pop("last_question", None)
    st.session_state.pop("last_answer", None)
    st.session_state.pop("last_sources", None)
    st.session_state.pop("last_route", None)
    st.rerun()

# ============================================================
# 8. ASK A QUESTION
# ============================================================

st.markdown("## Ask a Question")

question = st.text_area(
    "Enter your technical question",
    placeholder=(
        "Example: What is the relationship between "
        "machine learning and classification?"
    ),
    height=115,
    key="question_input",
)

ask_clicked = st.button(
    "Get Answer",
    type="primary",
    use_container_width=False,
    key="ask_question_button",
)


# ============================================================
# 9. DISPLAY ANSWER AND SOURCES
# ============================================================

if ask_clicked:
    cleaned_question = question.strip()

    if not cleaned_question:
        st.warning("Please enter a question first.")

    else:
        try:
            with st.spinner(
                "Analyzing your question and retrieving relevant knowledge..."
            ):
                response = ask_question(cleaned_question)

            if not response.ok:
                st.error(
                    f"Request failed ({response.status_code}): "
                    f"{extract_error_message(response)}"
                )

            else:
                try:
                    result = response.json()
                except ValueError:
                    result = {}

                if not isinstance(result, dict):
                    st.error("The backend returned an unexpected response.")
                else:
                    answer = result.get("answer", "No answer was returned.")
                    sources = result.get("sources", [])
                    route = result.get("route")

                    st.session_state["last_question"] = cleaned_question
                    st.session_state["last_answer"] = answer
                    st.session_state["last_sources"] = sources
                    st.session_state["last_route"] = route

                    # Save this conversation to chat history
                    if "chat_history" not in st.session_state:
                        st.session_state["chat_history"] = []

                    st.session_state["chat_history"].append({
                        "question": cleaned_question,
                        "answer": answer,
                        "sources": sources,
                        "route": route,
                    })

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to FastAPI. Start the backend first, "
                "then try again."
            )

        except requests.exceptions.Timeout:
            st.error(
                "The answer request timed out. The model may still be "
                "processing your question. Check the backend terminal."
            )

        except requests.exceptions.RequestException as exc:
            st.error(f"Question request failed: {exc}")


# Show the most recent answer, including after Streamlit reruns.
if "last_answer" in st.session_state:
    st.divider()

    st.markdown("### Answer")

    answer = st.session_state["last_answer"]

    if isinstance(answer, str):
        st.markdown(answer)
    else:
        st.write(answer)

    route = st.session_state.get("last_route")

    if route:
        st.caption(f"Processing route: {route}")

    sources = st.session_state.get("last_sources", [])

    st.markdown("### Supporting Sources")

    if isinstance(sources, list) and sources:
        st.caption(f"{len(sources)} source item(s) returned.")

        for index, source in enumerate(sources, start=1):
            if isinstance(source, dict):
                if source.get("source_type") == "knowledge_graph":
                    title = (
                        f"Source {index}: "
                        f"{source.get('source', 'Knowledge graph')} "
                        f"→ {source.get('target', 'Related entity')}"
                    )
                else:
                    title = (
                        f"Source {index}: "
                        f"{source.get('document', source.get('source', 'Document'))}"
                    )

                with st.expander(title):
                    st.json(source)

            else:
                with st.expander(f"Source {index}"):
                    st.write(source)

    else:
        st.info("No sources were returned for this answer.")


# ============================================================
# 10. FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div class="app-footer">
        Secure Multi-Agent RAG
        &nbsp;·&nbsp; FastAPI
        &nbsp;·&nbsp; ChromaDB
        &nbsp;·&nbsp; Neo4j
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================
# 10. CHAT HISTORY
# ==============================

st.divider()
st.subheader("Chat History")

chat_history = st.session_state.get("chat_history", [])
if chat_history:
    if st.button("🗑️ Clear Chat History", key="clear_chat_history"):
        st.session_state["chat_history"] = []
        st.rerun()

if chat_history:
    for index, chat in enumerate(reversed(chat_history), start=1):
        with st.expander(
            f"Conversation {index}: {chat['question'][:60]}"
        ):
            st.markdown("**Your Question**")
            st.write(chat["question"])

            st.markdown("**Answer**")
            st.write(chat["answer"])

            sources = chat.get("sources", [])

            if sources:
                st.markdown("**Supporting Sources**")
                for source_index, source in enumerate(sources, start=1):
                    with st.expander(f"Source {source_index}"):
                        st.json(source)
            else:
                st.caption("No supporting sources were returned.")
else:
    st.info("Your previous questions will appear here.")