"""
ResearchX - Paper Library
Upload research papers in PDF format, extract text, and chunk documents with preserved provenance.
"""

import sys
from pathlib import Path
import streamlit as st
import pymupdf

# Ensure project root is available in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from chunking import chunk_paper_pages

st.set_page_config(
    page_title="Paper Library - ResearchX",
    page_icon="📚",
    layout="wide",
)

# Initialize session state for tracking uploaded papers
if "uploaded_papers" not in st.session_state:
    st.session_state.uploaded_papers = {}


def extract_text_from_pdf(file_bytes: bytes, filename: str) -> dict:
    """Extract text from a PDF file preserving page numbers and handling errors."""
    if not file_bytes:
        return {
            "name": filename,
            "status": "error",
            "status_label": "Invalid (0 bytes)",
            "message": "The uploaded file is empty (0 bytes).",
            "pages": [],
            "page_count": 0,
            "total_chars": 0,
        }

    try:
        doc = pymupdf.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        return {
            "name": filename,
            "status": "error",
            "status_label": "Invalid PDF",
            "message": f"Could not parse file as PDF: {str(e)}",
            "pages": [],
            "page_count": 0,
            "total_chars": 0,
        }

    if doc.is_encrypted:
        if not doc.authenticate(""):
            page_count = len(doc)
            doc.close()
            return {
                "name": filename,
                "status": "error",
                "status_label": "Password Protected",
                "message": "PDF is encrypted and requires a password to open.",
                "pages": [],
                "page_count": page_count,
                "total_chars": 0,
            }

    total_pages = len(doc)
    if total_pages == 0:
        doc.close()
        return {
            "name": filename,
            "status": "empty",
            "status_label": "Empty Document",
            "message": "PDF contains 0 pages.",
            "pages": [],
            "page_count": 0,
            "total_chars": 0,
        }

    pages = []
    total_chars = 0
    for idx in range(total_pages):
        page = doc[idx]
        text = page.get_text() or ""
        char_count = len(text.strip())
        pages.append(
            {
                "page_number": idx + 1,
                "text": text,
                "char_count": char_count,
            }
        )
        total_chars += char_count

    doc.close()

    if total_chars == 0:
        return {
            "name": filename,
            "status": "empty",
            "status_label": "No Text Found",
            "message": "No extractable text found (document may contain scanned images or blank pages).",
            "pages": pages,
            "page_count": total_pages,
            "total_chars": 0,
        }

    return {
        "name": filename,
        "status": "success",
        "status_label": "Extracted",
        "message": f"Successfully extracted text from {total_pages} page(s).",
        "pages": pages,
        "page_count": total_pages,
        "total_chars": total_chars,
    }


# Sidebar
with st.sidebar:
    st.markdown("## 🔬 ResearchX")
    st.caption("Evidence-Based AI Research Intelligence")
    st.divider()

    corpus_size = len(st.session_state.uploaded_papers)
    st.metric(label="Loaded Papers", value=corpus_size)

    if corpus_size > 0:
        if st.button("🗑️ Clear All Papers", width="stretch"):
            st.session_state.uploaded_papers = {}
            st.rerun()

# Main Header
st.title("📚 Paper Library")
st.caption("Upload multiple research PDFs to extract text, generate chunks, and inspect sample data.")

# File Uploader
uploaded_files = st.file_uploader(
    "Choose PDF files",
    type=["pdf"],
    accept_multiple_files=True,
    help="Select one or more PDF papers.",
)

# Process any newly uploaded files
if uploaded_files:
    for file in uploaded_files:
        if file.name not in st.session_state.uploaded_papers:
            size_kb = file.size / 1024
            size_formatted = f"{size_kb / 1024:.2f} MB" if size_kb >= 1024 else f"{size_kb:.1f} KB"

            file_bytes = file.read()
            extracted_data = extract_text_from_pdf(file_bytes, file.name)
            extracted_data["size_formatted"] = size_formatted

            # Generate chunks if extraction succeeded
            if extracted_data["status"] == "success":
                chunks = chunk_paper_pages(extracted_data["pages"], file.name)
                extracted_data["chunks"] = chunks
                extracted_data["chunk_count"] = len(chunks)
            else:
                extracted_data["chunks"] = []
                extracted_data["chunk_count"] = 0

            st.session_state.uploaded_papers[file.name] = extracted_data

# Display Uploaded Papers & Text Previews
if st.session_state.uploaded_papers:
    st.divider()
    st.subheader(f"Papers ({len(st.session_state.uploaded_papers)})")

    # Overview table with Chunks column
    summary_rows = []
    for doc in st.session_state.uploaded_papers.values():
        if doc["status"] == "success":
            status_display = f"✅ Extracted ({doc['page_count']} pages, {doc['total_chars']:,} chars)"
        elif doc["status"] == "empty":
            status_display = f"⚠️ {doc['status_label']} ({doc['page_count']} pages)"
        else:
            status_display = f"❌ {doc['status_label']}"

        summary_rows.append(
            {
                "Filename": doc["name"],
                "Size": doc["size_formatted"],
                "Pages": doc["page_count"],
                "Chunks": doc.get("chunk_count", 0),
                "Status": status_display,
            }
        )
    st.dataframe(summary_rows, width="stretch", hide_index=True)

    st.markdown("### Document Inspection")

    for doc_name, doc in st.session_state.uploaded_papers.items():
        chunk_count = doc.get("chunk_count", 0)
        if doc["status"] == "success":
            expander_title = (
                f"📄 {doc_name} — {doc['page_count']} page(s) • {chunk_count} chunk(s)"
            )
        elif doc["status"] == "empty":
            expander_title = f"⚠️ {doc_name} — {doc['status_label']}"
        else:
            expander_title = f"❌ {doc_name} — {doc['status_label']}"

        with st.expander(
            expander_title,
            expanded=(doc["status"] == "success" and len(st.session_state.uploaded_papers) == 1),
        ):
            if doc["status"] == "error":
                st.error(doc["message"])
            elif doc["status"] == "empty":
                st.warning(doc["message"])
            else:
                st.caption(
                    f"**Size:** {doc['size_formatted']} &nbsp;|&nbsp; "
                    f"**Total Pages:** {doc['page_count']} &nbsp;|&nbsp; "
                    f"**Generated Chunks:** {chunk_count} &nbsp;|&nbsp; "
                    f"**Total Characters:** {doc['total_chars']:,}"
                )

                # Expandable Sample Chunk Inspector
                if doc.get("chunks"):
                    with st.expander("🧩 Inspect Sample Chunk", expanded=True):
                        total_chunks = len(doc["chunks"])
                        if total_chunks > 1:
                            selected_idx = st.selectbox(
                                "Select chunk to inspect:",
                                options=list(range(total_chunks)),
                                format_func=lambda i: (
                                    f"Chunk {i + 1} of {total_chunks} "
                                    f"(Page(s) {', '.join(map(str, doc['chunks'][i]['page_numbers']))})"
                                ),
                                key=f"chunk_select_{doc_name}",
                            )
                            sample_chunk = doc["chunks"][selected_idx]
                        else:
                            sample_chunk = doc["chunks"][0]

                        pages_display = ", ".join(map(str, sample_chunk["page_numbers"]))
                        st.markdown(
                            f"**Chunk Index:** `{sample_chunk['chunk_index']}` &nbsp;|&nbsp; "
                            f"**Source Page(s):** `{pages_display}` &nbsp;|&nbsp; "
                            f"**Approx. Tokens:** `{sample_chunk['token_count_approx']}` &nbsp;|&nbsp; "
                            f"**Characters:** `{sample_chunk['char_count']}`"
                        )
                        st.text_area(
                            label=f"Chunk {sample_chunk['chunk_index']} text",
                            value=sample_chunk["text"],
                            height=160,
                            disabled=True,
                            key=f"sample_chunk_text_{doc_name}_{sample_chunk['chunk_index']}",
                            label_visibility="collapsed",
                        )

                # Expandable Raw Page-by-Page View
                with st.expander("📄 Page-by-Page Raw Text", expanded=False):
                    for page in doc["pages"]:
                        st.markdown(f"**Page {page['page_number']}** ({page['char_count']:,} characters)")
                        if page["text"].strip():
                            st.text_area(
                                label=f"Page {page['page_number']} content",
                                value=page["text"],
                                height=160,
                                disabled=True,
                                key=f"preview_{doc_name}_p{page['page_number']}",
                                label_visibility="collapsed",
                            )
                        else:
                            st.caption("*(Blank or non-text page)*")
else:
    st.info("No papers uploaded yet. Select PDF files above to extract text.", icon="ℹ️")
