"""
ResearchX - Evidence-Based AI Research Intelligence Engine
Main Application Landing Page
"""

import streamlit as st

st.set_page_config(
    page_title="ResearchX - Research Intelligence Engine",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar Branding
with st.sidebar:
    st.markdown("## 🔬 ResearchX")
    st.caption("Evidence-Based AI Research Intelligence Engine")
    st.markdown("**Version:** `0.1.0 (Hackathon Prototype)`")
    st.divider()

    uploaded_count = len(st.session_state.get("uploaded_papers", {}))
    st.markdown(f"**Session Corpus:** `{uploaded_count}` papers loaded")

    st.divider()
    st.info(
        "📌 **Phase 1 Prototype:**\n\n"
        "Interactive UI skeleton. Vector indexing and LLM reasoning will be connected in Phase 2.",
        icon="ℹ️",
    )

# Header Section
st.title("🔬 ResearchX")
st.subheader("Evidence-Based AI Research Intelligence Engine")

st.markdown(
    """
    **ResearchX** is an academic investigation platform built for researchers, scholars, and technical teams.
    It streamlines literature exploration by enabling multi-document synthesis, verifiable citation extraction,
    and structured methodology comparison across research collections.
    """
)

st.divider()

# Feature Cards Section
st.markdown("### Core Capabilities")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("### 📚 Paper Library")
        st.markdown(
            "Upload, organize, and inspect academic research papers in PDF format. "
            "Build focused document collections for literature reviews and investigative synthesis."
        )
        st.markdown("---")
        st.page_link(
            "pages/1_Paper_Library.py",
            label="Open Paper Library",
            icon="📚",
        )

with col2:
    with st.container(border=True):
        st.markdown("### 🔍 Research Investigator")
        st.markdown(
            "Interrogate your paper corpus with multi-hop research questions. "
            "Examine answers grounded in direct textual citations and extracted evidence."
        )
        st.markdown("---")
        st.page_link(
            "pages/2_Research_Investigator.py",
            label="Launch Investigator",
            icon="🔍",
        )

with col3:
    with st.container(border=True):
        st.markdown("### ⚖️ Compare & Discover")
        st.markdown(
            "Systematically contrast study architectures, benchmark datasets, and empirical outcomes. "
            "Identify unexplored gaps and contradictions across the literature."
        )
        st.markdown("---")
        st.page_link(
            "pages/3_Compare_and_Discover.py",
            label="Compare & Discover",
            icon="⚖️",
        )

st.divider()

# Getting Started Section
st.markdown("### 🚀 Getting Started")
st.markdown(
    """
    Follow this investigation workflow to explore the application:

    1. **Step 1: Ingest Literature (`Paper Library`)**  
       Navigate to the **Paper Library** page to upload research papers (PDF). Verify document names and inspect session corpus status.
    
    2. **Step 2: Formulate Inquiries (`Research Investigator`)**  
       Visit the **Research Investigator** page to explore the planned citation-backed question-answering workflow and query interface.
    
    3. **Step 3: Contrast & Synthesize (`Compare & Discover`)**  
       Open **Compare & Discover** to view the structured methodology matrix preview and examine the planned research-gap analysis engine.
    """
)

# System Architecture & Roadmap Overview
with st.expander("ℹ️ Prototype Architecture & Integration Roadmap", expanded=False):
    st.markdown(
        """
        - **Current Stage:** Phase 1 — UI Skeleton & Multi-Page Session Architecture
        - **Document Parser (Planned):** PyMuPDF for section-aware text extraction and layout preservation
        - **Database & Search (Planned):** MongoDB Atlas Vector Search for dense and hybrid semantic retrieval
        - **Inference Engine (Planned):** Embedding generation and LLM-powered synthesis with verifiable page references
        """
    )

