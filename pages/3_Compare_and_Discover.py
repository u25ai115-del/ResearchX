"""
ResearchX - Compare & Discover
Page for structured methodology comparison and research gap exploration.
"""

import streamlit as st

st.set_page_config(
    page_title="Compare & Discover - ResearchX",
    page_icon="⚖️",
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
        "⚖️ **Compare & Discover:**\n\n"
        "Structured methodology matrices and potential research-gap detection.",
        icon="ℹ️",
    )

# Page Header
st.title("⚖️ Compare & Discover")
st.markdown(
    """
    Perform multi-paper comparative analysis across methodologies, benchmark datasets, and outcomes.
    The planned engine contrasts study designs and surfaces potential research gaps across the literature.
    """
)

# Implementation Notice
st.warning(
    "⚠️ **Implementation Notice:** Automated comparative extraction and research-gap discovery "
    "are **not implemented yet**. The table below contains **clearly labeled illustrative placeholder data** "
    "to preview the future user interface. No actual research findings or literature gaps have been computed.",
    icon="⚠️",
)

st.divider()

# Comparative Matrix Preview Section
st.subheader("1. Paper Comparison Matrix (Illustrative Placeholder Data)")
st.caption(
    "Note: The data below is sample mock data demonstrating the future schema for automated cross-paper extraction."
)

mock_comparison_data = [
    {
        "Study Reference": "Paper A (Vaswani et al., 2017)",
        "Architecture / Method": "Multi-Head Self-Attention Transformer",
        "Evaluation Benchmark": "WMT 2014 En-De / En-Fr",
        "Key Metric / Result": "28.4 BLEU (En-De)",
        "Reported Limitation": "Quadratic memory scaling O(N²) with sequence length",
    },
    {
        "Study Reference": "Paper B (Gu & Dao, 2023)",
        "Architecture / Method": "Selective State Space Model (Mamba)",
        "Evaluation Benchmark": "The Pile, ImageNet, Audio",
        "Key Metric / Result": "5x throughput scaling vs Transformers",
        "Reported Limitation": "Associative memory recall challenges on continuous copying",
    },
    {
        "Study Reference": "Paper C (Dettmers et al., 2023)",
        "Architecture / Method": "4-bit NormalFloat Quantization + LoRA",
        "Evaluation Benchmark": "MMLU, Vicuna Benchmark",
        "Key Metric / Result": "99.3% performance of 16-bit full finetuning",
        "Reported Limitation": "Minor perplexity variance under extreme low-bit regimes",
    },
]

st.table(mock_comparison_data)

st.divider()

# Planned Research-Gap Analysis Section
st.subheader("2. Planned Research-Gap Discovery Engine")
st.markdown(
    """
    The planned research-gap engine will automate literature synthesis through three core analytical lenses:
    """
)

gap_col1, gap_col2, gap_col3 = st.columns(3)

with gap_col1:
    with st.container(border=True):
        st.markdown("#### 1. Methodological Divergence")
        st.markdown(
            "Detect conflicting conclusions or varying baseline assumptions between papers "
            "evaluating similar problem spaces, highlighting discrepancies that require further investigation."
        )

with gap_col2:
    with st.container(border=True):
        st.markdown("#### 2. Unaddressed Bottlenecks")
        st.markdown(
            "Systematically parse and cluster the *Limitations* and *Future Work* sections across "
            "the corpus to surface persistent, unresolved challenges across the discipline."
        )

with gap_col3:
    with st.container(border=True):
        st.markdown("#### 3. Cross-Domain Transfer Gaps")
        st.markdown(
            "Identify proven algorithmic techniques in one subdiscipline that have not yet been "
            "empirically benchmarked on problems in related domains."
        )

st.info(
    "ℹ️ **Gap Analysis Offline:** Real-time hypothesis generation and gap synthesis will be enabled "
    "once the MongoDB Atlas vector graph and multi-document reasoning agent are integrated in Phase 2.",
    icon="ℹ️",
)

