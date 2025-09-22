# Verifact: AI-Powered Fact-Checking System
**Verifact**, is essentially a **multi-agent, AI-powered fact-checking system** that orchestrates multiple tools and APIs to verify content from various formats—text, URLs, YouTube videos, or documents. Here’s a concise technical summary of what your system does and how it works:

---

## Key Highlights of Your Project

### 1. **Core Functionality**

* Accepts **multiple content formats**:

  * Text claims
  * URLs (web pages)
  * YouTube videos (transcripts)
  * Documents (PDF, Word)
* Automatically **extracts claims** from content.
* **Verifies claims** against authoritative sources.
* Returns **truth labels**: TRUE, FALSE, UNCERTAIN, UNVERIFIABLE.
* Provides **evidence and confidence scores** for transparency.

### 2. **Architecture**

* **Frontend:** Streamlit app for easy user interaction.
* **Multi-Agent Backend:** Using **CrewAI** for orchestrating agents:

  * **Fact Researcher Agent:** Collects content using tools like WebScrapingTool, YouTubeTranscriptTool, SerperDevTool.
  * **Content Analyzer Agent:** Extracts and structures claims using NLP, NER, and semantic analysis.
  * **Fact Verifier Agent:** Cross-references claims with reliable sources and assigns truth labels.
* **External Integrations:** APIs for web search, YouTube transcripts, documents parsing.

### 3. **Task-Oriented Workflow**

* Tasks are defined in **YAML configuration**:

  * `research_task` → gather content
  * `analysis_task` → extract and structure claims
  * `verification_task` → verify claims
* Agents execute **sequentially with context passing**.

### 4. **Tools & Libraries**

* **Web:** `requests`, `BeautifulSoup`, `lxml`
* **YouTube:** `youtube_transcript_api`
* **Documents:** `PyPDF2`, `pdfplumber`, `python-docx`
* **AI/NLP:** `langchain`, `transformers`, `openai`
* **Data Handling:** `pandas`, `numpy`, `json`, `yaml`
* **Frontend:** `Streamlit`

### 5. **Workflow**

```
User Input → Input Validation → Fact Researcher → Content Analyzer → Fact Verifier → Results
```

* Handles errors gracefully.
* Provides **real-time feedback** to users.
* Can **export verification reports**.

### 6. **Strengths**

* **Modular & Extensible**: Easy to add new input types or verification sources.
* **Transparent**: Provides evidence and confidence scores.
* **Scalable**: Asynchronous processing with multi-agent orchestration.
* **Multi-format Support**: Text, URL, video, documents.

### 7. **Future Enhancements**

* Multi-language support
* Image/video verification
* Batch processing and API access
* Blockchain for immutable verification records
* Community-driven validation

---

## Conclusion

💡 Verifact is a **fact-checking API orchestration platform** that leverages multi-agent AI to process, analyze, and verify claims from various content types, providing trustworthy evidence-backed results.

Verifact represents a significant advancement in automated fact-checking technology, combining the power of multi-agent AI systems with comprehensive content processing capabilities. The system's modular architecture ensures scalability and maintainability while providing accurate, evidence-based verification across multiple content formats.

The project demonstrates the practical application of modern AI frameworks like CrewAI for complex, multi-step workflows, and showcases how different technologies can be integrated to solve real-world problems in information verification and misinformation detection.

With its robust architecture and comprehensive feature set, Verifact is positioned to make a meaningful impact in the fight against misinformation while providing valuable tools for researchers, journalists, and the general public.

<img width="1920" height="1080" alt="frnt_nd_youtube_claim" src="https://github.com/user-attachments/assets/fa4d774c-20cd-4de9-a2c5-9676556a8a18" />
<img width="1920" height="1080" alt="youtube_verdict" src="https://github.com/user-attachments/assets/e08c094f-7d2e-48b7-be8a-3bd27918f742" />


