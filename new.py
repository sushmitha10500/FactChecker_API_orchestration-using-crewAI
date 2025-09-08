import os
import sys
import tempfile
import streamlit as st
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Add src to sys.path for importing crew
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

try:
    from fact_checker.crew import FactChecker
except ImportError as e:
    st.error(f"Could not import FactChecker: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="VERIFACT - Professional AI Fact Verification",
    layout="wide",
    page_icon="🔍",
    initial_sidebar_state="collapsed"
)

# ------------------------------
# 3. Custom CSS for Unique Theme
# ------------------------------
st.markdown("""
<style>
/* Force Light Mode */
:root {
    color-scheme: light;
}

/* Sidebar with soft glass effect */
section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid #e0e0e0;
}

/* App title */
h1 {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #1a1a1a !important;
}

/* Radio buttons → pill style */
div[role="radiogroup"] label {
    border: 1px solid #ccc !important;
    border-radius: 25px !important;
    padding: 6px 14px !important;
    margin: 4px !important;
    background-color: #f9f9f9 !important;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
}
div[role="radiogroup"] label:hover {
    background-color: #ececec !important;
}
div[role="radiogroup"] input:checked + div {
    background-color: #2b6cb0 !important;
    color: white !important;
    border-color: #2b6cb0 !important;
}

/* Buttons → flat pastel */
.stButton>button {
    background-color: #2b6cb0 !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.4rem !important;
    font-weight: 600 !important;
    border: none !important;
    transition: transform 0.2s ease, background 0.2s ease;
}
.stButton>button:hover {
    background-color: #1e4e8c !important;
    transform: translateY(-2px);
}

/* Text area & inputs */
textarea, input[type="text"] {
    border-radius: 10px !important;
    border: 1px solid #d0d0d0 !important;
    padding: 0.6rem !important;
}

/* File uploader box */
.stFileUploader {
    border: 2px dashed #b0b0b0 !important;
    border-radius: 12px !important;
    background: #fafafa !important;
}

/* Fact check results → card style */
.result-card {
    border: 1px solid #e0e0e0;
    border-radius: 14px;
    padding: 1rem;
    margin-top: 1rem;
    background: white;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

/* Footer */
.footer {
    margin-top: 40px;
    text-align: center;
    font-size: 0.85rem;
    color: #777;
}
.footer a {
    text-decoration: none;
    color: #2b6cb0;
}
.footer a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)


# Company logo at the top center - NO BOX
try:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image("src/fact_checker/assets/ramanasoftware_logo.png", width=600)
    st.markdown('</div>', unsafe_allow_html=True)
except:
    # Fallback if image is not found
    st.markdown("""
    <div class="logo-container">
        <h1 style="color: #667eea; font-size: 4rem; margin: 0;">RAMANA SOFTWARE</h1>
        <p style="color: #666; font-size: 1.5rem; margin: 0;">Consulting Services</p>
    </div>
    """, unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">VERIFACT</h1>
    <p class="main-subtitle">Professional AI-Powered Fact Verification System</p>
</div>
""", unsafe_allow_html=True)

# Environment check
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ **Configuration Error:** Please set your OPENAI_API_KEY in the .env file")
    st.stop()


# Input section
st.markdown("""
<div class="input-section">
""", unsafe_allow_html=True)

st.markdown('<h3 class="section-header">🎯 Select Verification Method</h3>', unsafe_allow_html=True)

# Input mode selection
mode = st.radio(
    "",
    ["📝 Text Claim", "🌐 Website URL", "📺 YouTube Video", "📄 Document Upload"],
    horizontal=True,
    key="input_mode"
)

st.markdown("<br>", unsafe_allow_html=True)

user_input = ""
claim, url, youtube_url, uploaded_file = "", "", "", None

# Input forms based on selected mode
if mode == "📝 Text Claim":
    st.markdown("**Enter the factual claim you want to verify:**")
    claim = st.text_area(
        "",
        height=120,
        placeholder="Enter the statement or claim you want to fact-check...",
        key="claim_input"
    )
    user_input = claim

elif mode == "🌐 Website URL":
    st.markdown("**Enter the website URL to analyze:**")
    url = st.text_input(
        "",
        placeholder="https://example.com/article",
        key="url_input"
    )
    user_input = url

elif mode == "📺 YouTube Video":
    st.markdown("**Enter the YouTube video URL:**")
    youtube_url = st.text_input(
        "",
        placeholder="https://www.youtube.com/watch?v=...",
        key="youtube_input"
    )
    if youtube_url:
        if re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?#]+)', youtube_url):
            st.success("✅ Valid YouTube URL detected")
        else:
            st.warning("⚠️ Please enter a valid YouTube URL")
    user_input = youtube_url

elif mode == "📄 Document Upload":
    st.markdown("**Upload a document for analysis:**")
    uploaded_file = st.file_uploader(
        "",
        type=["pdf", "docx", "txt"],
        help="Supported formats: PDF, Word Document (.docx), Text File (.txt)"
    )
    if uploaded_file:
        st.success(f"✅ File uploaded: **{uploaded_file.name}** ({round(uploaded_file.size / 1024, 1)} KB)")

st.markdown("</div>", unsafe_allow_html=True)

# Analysis button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button(
        "🚀 Launch Professional Analysis",
        use_container_width=True,
        key="analyze_btn"
    )

# Analysis execution
if analyze_button:
    # Input validation
    has_input = bool(claim or url or youtube_url or uploaded_file)

    if not has_input:
        st.error("⚠️ **Input Required:** Please provide content to analyze before starting the verification process.")
        st.stop()

    # Processing indicator
    with st.spinner(
            "🔍 **VERIFACT Analysis in Progress** - Our AI agents are researching, analyzing, and verifying your content..."):
        input_content = ""

        # File processing
        if uploaded_file:
            from pathlib import Path

            suffix = Path(uploaded_file.name).suffix.lower()
            try:
                if suffix == ".pdf":
                    import PyPDF2

                    reader = PyPDF2.PdfReader(uploaded_file)
                    input_content = "".join([page.extract_text() for page in reader.pages])
                elif suffix == ".docx":
                    from docx import Document

                    doc = Document(uploaded_file)
                    input_content = "\n".join([p.text for p in doc.paragraphs])
                elif suffix == ".txt":
                    raw = uploaded_file.read()
                    for enc in ["utf-8", "utf-16", "latin-1", "cp1252"]:
                        try:
                            input_content = raw.decode(enc)
                            break
                        except UnicodeDecodeError:
                            continue
                    else:
                        st.error(
                            "❌ **File Processing Error:** Unable to decode text file. Please ensure UTF-8 encoding.")
                        st.stop()
                else:
                    st.error("❌ **Unsupported Format:** Please upload a PDF, Word document, or text file.")
                    st.stop()
            except Exception as e:
                st.error(f"❌ **File Processing Error:** {e}")
                st.stop()
        else:
            input_content = claim or url or youtube_url

        # Run analysis
        try:
            progress = st.progress(0, text="Initializing VERIFACT system...")
            progress.progress(20, text="Loading AI agents...")
            checker = FactChecker()
            progress.progress(60, text="Executing multi-agent analysis...")
            result = checker.crew().kickoff(inputs={"input_content": input_content})
            progress.progress(100, text="Analysis complete!")
        except Exception as e:
            st.error(f"❌ **Analysis Error:** {e}")
            st.stop()

    # Success notification
    #st.balloons()
    st.success("🎉 **Analysis Complete** - Professional verification report generated successfully")

    # Results section
    st.markdown("""
    <div class="results-section">
    """, unsafe_allow_html=True)

    # Verdict analysis and display
    result_text = str(result)
    result_lower = result_text.lower()

    st.markdown("### 📊 Verification Result")

    # Determine verdict
    if "true" in result_lower and "false" not in result_lower:
        st.markdown("""
        <div class="verdict-container verdict-true">
            ✅ VERDICT: THE PROVIDED INFORMATION IS TRUE
        </div>
        """, unsafe_allow_html=True)
    elif "false" in result_lower:
        st.markdown("""
        <div class="verdict-container verdict-false">
            ❌ VERDICT: THE PROVIDED INFORMATION IS FALSE
        </div>
        """, unsafe_allow_html=True)
    elif "misleading" in result_lower or "partially" in result_lower:
        st.markdown("""
        <div class="verdict-container verdict-partial">
            ⚠️ VERDICT: THE PROVIDED INFORMATION IS PARTIALLY ACCURATE
        </div>
        """, unsafe_allow_html=True)
    elif "INCONCLUSIVE" in result_lower:
        st.markdown("""
        <div class="verdict-container verdict-inconclusive">
            🔍 VERDICT: REQUIRES FURTHER INVESTIGATION
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="verdict-container verdict-inconclusive">
            📋 DETAILED ANALYSIS AVAILABLE
        </div>
        """, unsafe_allow_html=True)

    # Detailed report
    st.markdown("### 📄 Comprehensive Analysis Report")
    with st.expander("**Click to view detailed verification report**", expanded=True):
        st.markdown(result_text)

    st.markdown("</div>", unsafe_allow_html=True)

    # Download options
    st.markdown("### 📥 Export Options")
    col1, col2 = st.columns(2)

    with col1:
        # Text report
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as f:
            report_header = f"VERIFACT PROFESSIONAL VERIFICATION REPORT\n{'=' * 50}\n\n"
            report_header += f"Input Content: {input_content[:200]}{'...' if len(input_content) > 200 else ''}\n\n"
            report_header += f"Analysis Results:\n{'-' * 20}\n\n{result_text}"
            f.write(report_header)
            temp_path = f.name

        with open(temp_path, "rb") as f:
            st.download_button(
                "📄 Download as Text Report",
                f.read(),
                "verifact_professional_report.txt",
                mime="text/plain",
                use_container_width=True
            )

    with col2:
        # Markdown report
        md_report = f"""# VERIFACT Professional Verification Report

## Input Analysis
**Content:** {input_content[:200]}{'...' if len(input_content) > 200 else ''}

## Verification Results

{result_text}

---
*Generated by VERIFACT AI Fact-Checking System*
*Powered by Multi-Agent Intelligence Architecture*
"""
        st.download_button(
            "📋 Download as Markdown",
            md_report,
            "verifact_professional_report.md",
            mime="text/markdown",
            use_container_width=True
        )

# Simple Professional Footer - Fixed Copyright Display
# Simple Professional Footer - Fixed Copyright Display
st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    padding: 2rem;
    border-radius: 15px;
    margin-top: 3rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
">
    <a href="mailto:neelamsushmitha2000@outlook.com" style="
        color: white !important;
        text-decoration: none;
        font-size: 1.2rem;
        font-weight: 600;
        display: block;
        margin-bottom: 1rem;
        background: rgba(255, 255, 255, 0.2);
        padding: 0.5rem 1rem;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    ">📧 neelamsushmitha2000@outlook.com</a>

    © 2025 RAMANA SOFT - All Rights Reserved
</div>
""", unsafe_allow_html=True)


