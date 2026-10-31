"""
ResearchX - Research Investigator
Page for multi-paper question answering with evidence grounding.
"""

import streamlit as st

st.set_page_config(
    page_title="Research Investigator - ResearchX",
    page_icon="🔍",
    layout="wide",
)

# Sidebar Branding & Status
with st.sidebar:
    st.markdown("## 🔬 ResearchX")
    st.caption("Evidence-Based AI Research Intelligence Engine")
    st.markdown("**Version:** `0.1.0 (Hackathon Prototype)`")
    st.divider()

    corpus_size = len(st.session_state.get("uploaded_papers", {}))
    st.metric(label="Active Corpus Papers", value=corpus_size)

    st.divider()
    st.info(
        "🔍 **Investigation Mode:**\n\n"
        "Cross-document question answering with evidence grounding and verifiable citations.",
        icon="ℹ️",
    )

# Page Header
st.title("🔍 Research Investigator")
st.markdown(
    """
    Formulate cross-document questions across your research literature.
    The planned engine synthesizes multi-paper evidence and provides verbatim citations for every claim.
    """
)

# Disabled State Notice
st.info(
    "🚧 **Engine Status:** AI-powered question answering is **disabled** in this initial UI skeleton. "
    "Connecting MongoDB Atlas Vector Search and the LLM inference pipeline will take place in Phase 2. "
    "No external API calls or simulated answers are being generated.",
    icon="ℹ️",
)

st.divider()

# Question Input Section (Disabled)
st.subheader("1. Inquire Across Literature")
st.markdown("Pose a specific research question against your uploaded paper collection:")

user_query = st.text_input(
    label="Research Inquiry",
    placeholder="e.g., What are the primary trade-offs between sparse attention and state-space architectures?",
    disabled=True,
    help="Query processing is currently disabled pending backend integration.",
    label_visibility="collapsed",
)

col_action, col_status = st.columns([1, 3])
with col_action:
    st.button("🔍 Execute Investigation", disabled=True, width="stretch")
with col_status:
    st.caption("🔒 Search execution disabled — backend inference pipeline scheduled for Phase 2.")

# Illustrative Query Prompts
st.markdown("**Planned Query Types Supported:**")
st.markdown(
    """
    - *Methodology Inquiries:* "What optimization objective is used to stabilize training in low-resource settings?"
    - *Comparative Benchmarks:* "Which papers report latency improvements on ImageNet-1K, and what were the baselines?"
    - *Limitations & Constraints:* "What compute constraints or hardware assumptions are highlighted across the literature?"
    """
)

st.divider()

# Planned Evidence-Backed Workflow Section
st.subheader("2. Planned Evidence-Backed Workflow")
st.markdown(
    """
    ResearchX is designed around a rigorous, citation-first workflow to ensure all answers are verifiable and hallucination-free:
    """
)

workflow_col1, workflow_col2, workflow_col3 = st.columns(3)

with workflow_col1:
    with st.container(border=True):
        st.markdown("#### 1. Hybrid Retrieval")
        st.markdown(
            "User queries are embedded into high-dimensional vector representations and retrieved "
            "via **MongoDB Atlas Vector Search** using hybrid dense semantic and sparse keyword indexing."
        )

with workflow_col2:
    with st.container(border=True):
        st.markdown("#### 2. Evidence Grounding")
        st.markdown(
            "Retrieved candidate passages are filtered, deduplicated, and matched with exact provenance "
            "metadata, including document title, author list, section heading, and page number."
        )

with workflow_col3:
    with st.container(border=True):
        st.markdown("#### 3. Verifiable Synthesis")
        st.markdown(
            "The LLM synthesizes findings constrained strictly to the grounded evidence passages, "
            "attaching interactive citation anchors for line-by-line verification by the researcher."
        )

