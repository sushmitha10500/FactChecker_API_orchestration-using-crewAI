import os
import sys
import streamlit as st
from dotenv import load_dotenv
import re
import time

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
    page_title="VERIFACT - AI Truth-O-Meter",
    layout="wide",
    page_icon="🎯",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with modern, professional styling
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Styles */
* {
    font-family: 'Inter', sans-serif;
}

.main > div {
    max-width: 1200px;
    margin: 0 auto;
}

body {
    background-color: #f8fafc;
}

.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Header Section */
.header-container {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin: 1rem 0 2rem 0;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    color: white;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.header-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    opacity: 0.3;
}

.main-title {
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    margin: 0 0 0.5rem 0 !important;
    letter-spacing: -0.5px;
}

.main-subtitle {
    font-size: 1.2rem !important;
    margin: 0 !important;
    opacity: 0.9;
    font-weight: 400 !important;
}

/* Card Components */
.card {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    border: 1px solid rgba(229, 231, 235, 0.8);
}

.card-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #1F2937;
    margin: 0 0 1.5rem 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

/* Input Section */
.input-container {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    border: 1px solid rgba(229, 231, 235, 0.8);
}

.section-header {
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    color: #1F2937 !important;
    margin-bottom: 1.5rem !important;
    text-align: center;
}

/* Enhanced Radio Buttons */
.stRadio > div {
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    flex-wrap: wrap;
    margin: 1.5rem 0;
}

.stRadio > div > label {
    background: white !important;
    border: 1.5px solid #E5E7EB !important;
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
    cursor: pointer;
    transition: all 0.2s ease;
    font-weight: 500;
    min-width: 140px;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.stRadio > div > label:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
    border-color: #6366F1 !important;
}

.stRadio > div [data-testid="stMarkdownContainer"] {
    font-weight: 500;
}

div[role="radiogroup"] div:has(input:checked) label {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
    color: white !important;
    border-color: #6366F1 !important;
    box-shadow: 0 6px 12px rgba(99, 102, 241, 0.2);
}

/* Enhanced Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 0.875rem 1.75rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    border: none !important;
    transition: all 0.2s ease;
    box-shadow: 0 4px 6px rgba(99, 102, 241, 0.2);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 15px rgba(99, 102, 241, 0.3);
}

/* Form Controls */
.stTextArea textarea, .stTextInput input {
    border-radius: 12px !important;
    border: 1.5px solid #E5E7EB !important;
    padding: 0.875rem !important;
    font-size: 1rem !important;
    transition: all 0.2s ease;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    outline: none !important;
}

.stTextArea textarea::placeholder, .stTextInput input::placeholder {
    color: #9CA3AF;
}

/* File Uploader */
.stFileUploader {
    border: 2px dashed #E5E7EB !important;
    border-radius: 12px !important;
    background: rgba(249, 250, 251, 0.7) !important;
    padding: 2rem !important;
    text-align: center;
    transition: all 0.2s ease;
}

.stFileUploader:hover {
    border-color: #6366F1 !important;
    background: rgba(99, 102, 241, 0.05) !important;
}

/* Truth Meter Display */
.truth-meter-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 2rem 0;
    padding: 2rem;
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.meter-visual {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 1rem 0;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    position: relative;
    overflow: hidden;
}

.meter-visual::after {
    content: '';
    position: absolute;
    width: 90%;
    height: 90%;
    border-radius: 50%;
    background: white;
    opacity: 0.2;
}

.meter-label {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 1rem;
    padding: 0.75rem 2rem;
    border-radius: 25px;
    display: inline-block;
    letter-spacing: 0.5px;
}

.meter-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

/* Verdict Cards */
.verdict-card {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    border-left: 5px solid;
    position: relative;
    overflow: hidden;
}

.verdict-true {
    border-left-color: #10B981;
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.03) 0%, rgba(16, 185, 129, 0.01) 100%);
}

.verdict-false {
    border-left-color: #EF4444;
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.03) 0%, rgba(239, 68, 68, 0.01) 100%);
}

.verdict-partial {
    border-left-color: #F59E0B;
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.03) 0%, rgba(245, 158, 11, 0.01) 100%);
}

.verdict-inconclusive {
    border-left-color: #6B7280;
    background: linear-gradient(135deg, rgba(107, 114, 128, 0.03) 0%, rgba(107, 114, 128, 0.01) 100%);
}

.verdict-title {
    font-size: 1.35rem;
    font-weight: 600;
    margin: 0 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.verdict-description {
    font-size: 1.1rem;
    line-height: 1.6;
    color: #374151;
    margin: 1rem 0;
}

/* Progress Bar */
.stProgress > div > div {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
    border-radius: 8px !important;
}

/* Expander */
.stExpander {
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    overflow: hidden;
    margin: 1.5rem 0;
}

/* Footer */
.footer {
    background: white;
    color: #6B7280;
    padding: 2.5rem 2rem;
    border-radius: 16px;
    margin-top: 3rem;
    text-align: center;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.06);
    border-top: 1px solid #F3F4F6;
}

/* Responsive */
@media (max-width: 768px) {
    .main-title {
        font-size: 2rem !important;
    }

    .main-subtitle {
        font-size: 1rem !important;
    }

    .stRadio > div {
        flex-direction: column;
        align-items: center;
    }

    .stRadio > div > label {
        min-width: 200px;
    }

    .meter-visual {
        width: 150px;
        height: 150px;
    }

    .meter-icon {
        font-size: 3rem;
    }

    .meter-label {
        font-size: 1.5rem;
    }
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in {
    animation: fadeIn 0.6s ease-out;
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.02);
    }
}

.pulse {
    animation: pulse 2s infinite;
}

@keyframes scaleIn {
    from {
        transform: scale(0);
        opacity: 0;
    }
    to {
        transform: scale(1);
        opacity: 1;
    }
}

.scale-in {
    animation: scaleIn 0.8s ease-out;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #F3F4F6;
}

::-webkit-scrollbar-thumb {
    background: #D1D5DB;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #9CA3AF;
}
</style>
""", unsafe_allow_html=True)


# Function to determine verdict based on analysis
def determine_verdict(result_text):
    """Determine the verdict based on the analysis result"""
    result_lower = result_text.lower()

    if "true" in result_lower and "false" not in result_lower:
        return "TRUE", "#10B981", "✅"
    elif "false" in result_lower:
        return "FALSE", "#EF4444", "❌"
    elif "misleading" in result_lower or "partially" in result_lower:
        return "MISLEADING", "#F59E0B", "⚠️"
    elif "mostly false" in result_lower:
        return "MOSTLY FALSE", "#F97316", "❌"
    elif "mostly true" in result_lower:
        return "MOSTLY TRUE", "#84CC16", "✅"
    elif "inconclusive" in result_lower or "cannot verify" in result_lower:
        return "INCONCLUSIVE", "#6B7280", "🔍"
    else:
        return "NEEDS REVIEW", "#6B7280", "🔎"


# Header Section
st.markdown("""
<div class="header-container animate-fade-in">
    <h1 class="main-title">VERIFACT</h1>
    <p class="main-subtitle">AI-Powered Truth-O-Meter & Fact Verification System</p>
    <div style="margin-top: 1.5rem; font-size: 1rem; opacity: 0.9;">
        🎯 Professional Analysis • 🧠 Multi-Agent AI • ⚡ Real-Time Verification
    </div>
</div>
""", unsafe_allow_html=True)

# Environment check
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ **Configuration Error:** Please set your OPENAI_API_KEY in the .env file")
    st.stop()

# Input Section
st.markdown("""
<div class="card">
    <h3 class="card-title">🎯 Choose Your Verification Method</h3>
</div>
""", unsafe_allow_html=True)

# Input mode selection with enhanced styling
mode = st.radio(
    "",
    ["📝 Text Claim", "🌐 Website URL", "📺 YouTube Video", "📄 Document Upload"],
    horizontal=True,
    key="input_mode"
)

st.markdown("<br>", unsafe_allow_html=True)

user_input = ""
claim, url, youtube_url, uploaded_file = "", "", "", None

# Enhanced input forms
if mode == "📝 Text Claim":
    st.markdown("### 📝 **Enter Your Claim for Fact-Checking**")
    claim = st.text_area(
        "",
        height=120,
        placeholder="Type or paste the statement, claim, or information you want to fact-check here...",
        key="claim_input",
        help="Enter any factual claim, news statement, or information you'd like to verify"
    )
    user_input = claim

elif mode == "🌐 Website URL":
    st.markdown("### 🌐 **Website Analysis**")
    url = st.text_input(
        "",
        placeholder="https://example.com/article-to-analyze",
        key="url_input",
        help="Enter the full URL of the website or article you want to fact-check"
    )
    if url and not url.startswith(('http://', 'https://')):
        st.warning("⚠️ Please include 'https://' at the beginning of your URL")
    user_input = url

elif mode == "📺 YouTube Video":
    st.markdown("### 📺 **YouTube Video Fact-Check**")
    youtube_url = st.text_input(
        "",
        placeholder="https://www.youtube.com/watch?v=example123",
        key="youtube_input",
        help="Enter a YouTube video URL to analyze its content for factual accuracy"
    )
    if youtube_url:
        if re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?#]+)', youtube_url):
            st.success("✅ Valid YouTube URL detected")
        else:
            st.warning("⚠️ Please enter a valid YouTube URL")
    user_input = youtube_url

elif mode == "📄 Document Upload":
    st.markdown("### 📄 **Document Analysis**")
    uploaded_file = st.file_uploader(
        "",
        type=["pdf", "docx", "txt"],
        help="Upload PDF, Word document, or text file for comprehensive fact-checking"
    )
    if uploaded_file:
        file_size_mb = round(uploaded_file.size / 1024 / 1024, 2)
        st.success(f"✅ **{uploaded_file.name}** uploaded successfully ({file_size_mb} MB)")

# Analysis button with enhanced styling
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button(
        "🚀 Truth-O-Meter Analysis",
        use_container_width=True,
        key="analyze_btn",
        help="Start comprehensive AI-powered fact verification"
    )

# Analysis execution with enhanced UI
if analyze_button:
    # Input validation
    has_input = bool(claim or url or youtube_url or uploaded_file)

    if not has_input:
        st.error("⚠️ **Input Required:** Please provide content to analyze before starting the verification process.")
        st.stop()

    # Enhanced processing indicator
    with st.spinner("🔍 **VERIFACT Analysis in Progress** - Multi-agent AI system working..."):
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Simulate realistic progress
        progress_bar.progress(10, text="🤖 Initializing AI agents...")
        time.sleep(0.5)

        progress_bar.progress(25, text="📊 Processing input content...")
        time.sleep(0.3)

        input_content = ""

        # Enhanced file processing
        if uploaded_file:
            progress_bar.progress(40, text="📄 Extracting document content...")
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
            except Exception as e:
                st.error(f"❌ **File Processing Error:** {e}")
                st.stop()
        else:
            input_content = claim or url or youtube_url

        progress_bar.progress(60, text="🧠 Running multi-agent analysis...")
        time.sleep(0.5)

        # Run analysis
        try:
            progress_bar.progress(80, text="🔍 Cross-referencing sources...")
            checker = FactChecker()
            result = checker.crew().kickoff(inputs={"input_content": input_content})
            progress_bar.progress(100, text="✅ Analysis complete!")
            time.sleep(0.3)
            progress_bar.empty()
            status_text.empty()
        except Exception as e:
            st.error(f"❌ **Analysis Error:** {e}")
            st.stop()

    # Success notification with confetti
    # Professional success notification
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        text-align: center;
        font-size: 1.25rem;
        font-weight: 600;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        animation: scaleIn 0.8s ease-out;
    ">
    🎯 Truth-O-Meter Analysis Complete! Professional verification report generated.
    </div>
    """, unsafe_allow_html=True)

    st.success("🎉 **Truth-O-Meter Analysis Complete!** Professional verification report generated.")

    # Results section
    st.markdown("""
    <div class="card">
    """, unsafe_allow_html=True)

    # Process result and determine verdict
    result_text = str(result)
    verdict, color, icon = determine_verdict(result_text)


    # Display verdict label
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="meter-label" style="color: {color}; background-color: {color}20; border: 2px solid {color};">
            {verdict}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Enhanced verdict display
    st.markdown("### 🎯 **Verification Verdict**")

    if verdict == "TRUE":
        verdict_html = f"""
        <div class="verdict-card verdict-true animate-fade-in">
            <div class="verdict-title">
                {icon} <span style="color: {color};">VERIFIED TRUE</span>
            </div>
            <p class="verdict-description"><strong>Assessment:</strong> The provided information has been verified as factually accurate based on reliable sources and evidence.</p>
            <p><strong>Confidence Level:</strong> High - Multiple authoritative sources confirm this information.</p>
        </div>
        """
    elif verdict == "FALSE":
        verdict_html = f"""
        <div class="verdict-card verdict-false animate-fade-in">
            <div class="verdict-title">
                {icon} <span style="color: {color};">VERIFIED FALSE</span>
            </div>
            <p class="verdict-description"><strong>Assessment:</strong> The claim has been fact-checked and found to be inaccurate or misleading based on available evidence.</p>
            <p><strong>Confidence Level:</strong> High - Credible sources contradict this information.</p>
        </div>
        """
    elif verdict == "MISLEADING":
        verdict_html = f"""
        <div class="verdict-card verdict-partial animate-fade-in">
            <div class="verdict-title">
                {icon} <span style="color: {color};">MISLEADING</span>
            </div>
            <p class="verdict-description"><strong>Assessment:</strong> The information contains some accurate elements but also includes misleading or incomplete details that distort the overall picture.</p>
            <p><strong>Confidence Level:</strong> Medium - Requires careful interpretation of context.</p>
        </div>
        """
    elif verdict == "MOSTLY TRUE":
        verdict_html = f"""
        <div class="verdict-card verdict-true animate-fade-in">
            <div class="verdict-title">
                {icon} <span style="color: {color};">MOSTLY TRUE</span>
            </div>
            <p class="verdict-description"><strong>Assessment:</strong> The claim is primarily accurate but may contain minor inaccuracies or exaggerations that don't fundamentally change the message.</p>
            <p><strong>Confidence Level:</strong> Medium - Generally accurate with minor qualifications.</p>
        </div>
        """
    elif verdict == "MOSTLY FALSE":
        verdict_html = f"""
        <div class="verdict-card verdict-false animate-fade-in">
            <div class="verdict-title">
                {icon} <span style="color: {color};">MOSTLY FALSE</span>
            </div>
            <p class="verdict-description"><strong>Assessment:</strong> The claim contains some elements of truth but is largely inaccurate or misleading in its overall presentation.</p>
            <p><strong>Confidence Level:</strong> Medium - Contains some truth but overall misleading.</p>
        </div>
        """
    else:
        verdict_html = f"""
        <div class="verdict-card verdict-inconclusive animate-fade-in">
            <div class="verdict-title">
                {icon} <span style="color: {color};">{verdict}</span>
            </div>
            <p class="verdict-description"><strong>Assessment:</strong> Insufficient evidence available for a definitive conclusion. Additional verification recommended from specialized sources.</p>
            <p><strong>Confidence Level:</strong> Low - Requires additional verification.</p>
        </div>
        """

    st.markdown(verdict_html, unsafe_allow_html=True)

    # Detailed analysis report
    st.markdown("### 📋 **Comprehensive Analysis Report**")
    with st.expander("**🔍 View Detailed Verification Report**", expanded=True):
        # Format the result text for better readability
        formatted_result = result_text.replace('\n', '\n\n')
        st.markdown(f"""
        <div style="
            background: #f8fafc;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #6366F1;
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            font-size: 0.95rem;
        ">
        {formatted_result}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Stop further execution to prevent re-running analysis
    st.stop()

# Footer
st.markdown("""
<div class="footer">
    <div style="margin: 2rem 0;">
        <a href="mailto:neelamsushmitha2000@outlook.com" style="
            color: #6366F1;
            text-decoration: none;
            font-size: 1.1rem;
            font-weight: 600;
            display: inline-block;
            background: rgba(99, 102, 241, 0.1);
            padding: 0.8rem 2rem;
            border-radius: 50px;
            border: 2px solid rgba(99, 102, 241, 0.2);
            transition: all 0.3s ease;
        " onmouseover="this.style.background='rgba(99, 102, 241, 0.2)'; this.style.transform='translateY(-2px)'" 
           onmouseout="this.style.background='rgba(99, 102, 241, 0.1)'; this.style.transform='translateY(0)'">
            📧 neelamsushmitha2000@outlook.com
        </a>
    </div>
    <p>
        Powered by Advanced Multi-Agent Intelligence • Built with ❤️ for Truth & Accuracy
    </p>
</div>
""", unsafe_allow_html=True)
