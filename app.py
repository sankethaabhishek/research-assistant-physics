import streamlit as st
import re
from datetime import datetime

from utils.parser import extract_text_from_pdf
from utils.section_splitter import split_into_sections
from utils.summarizer import summarize_text, AVAILABLE_MODELS
from utils.qa import answer_question

st.set_page_config(page_title="Physics Research Assistant", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.title("🔬 Physics AI Assistant")
    st.markdown("Upload a PDF of a physics research paper and get AI-generated summaries by section.")
    selected_model_label = st.selectbox("🧠 Choose summarization model:", list(AVAILABLE_MODELS.keys()))
    selected_model = AVAILABLE_MODELS[selected_model_label]
    st.markdown("---")
    st.markdown("🚀 Built by Sanketha Abhishek")
    st.markdown("📝 Works best with clean, text-based PDFs.")
    st.caption("🧪 Styling provided by a custom academic CSS theme.")

# --- Main Title ---
st.title("📄 Research Paper Summarizer")

# --- Upload PDF ---
uploaded_file = st.file_uploader("📁 Upload a PDF", type=["pdf"])

# --- Helper: Extract metadata ---
def extract_metadata(text):
    lines = text.strip().split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    title = lines[0] if lines else "Unknown Title"
    author_line = next((line for line in lines[1:5] if not any(char.isdigit() for char in line)), "Unknown Authors")
    abstract_match = re.search(r'(?i)abstract\s*[:\n]*(.*?)\n(?:\s*\n|1\.|I\.|Introduction)', text, re.DOTALL)
    abstract = abstract_match.group(1).strip() if abstract_match else "Abstract not found."
    return title, author_line, abstract

# --- Helper: APA citation ---
def generate_apa_citation(title, authors_line, year=None):
    authors = [a.strip() for a in re.split(',|and', authors_line) if a.strip()]
    if len(authors) == 1:
        formatted_authors = authors[0]
    elif len(authors) == 2:
        formatted_authors = f"{authors[0]} & {authors[1]}"
    else:
        formatted_authors = ", ".join(authors[:-1]) + f", & {authors[-1]}"
    if not year:
        year = datetime.now().year
    return f"{formatted_authors} ({year}). *{title}*."

# --- Process Uploaded File ---
if uploaded_file:
    with st.spinner("⏳ Extracting and summarizing..."):
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        full_text = extract_text_from_pdf("temp.pdf")
        title, authors, abstract = extract_metadata(full_text)
        match_year = re.search(r'\b(19|20)\d{2}\b', full_text)
        year = match_year.group() if match_year else datetime.now().year
        citation = generate_apa_citation(title, authors, year)
        sections = split_into_sections(full_text)

    # --- Display Metadata ---
    st.markdown(f"""
    <div class="metadata">
        <h3>🧾 Paper Title: <i>{title}</i></h3>
        <p><strong>👥 Authors:</strong> {authors}</p>
        <p><strong>📝 Abstract:</strong><br>{abstract}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 📚 Citation (APA Style)")
    st.code(citation, language="markdown")

    st.success("✅ Summary ready!")

    # --- Section Summaries ---
    summaries = {}
    for section_title, content in sections.items():
        with st.expander(f"📌 {section_title.upper()}"):
            summary = summarize_text(content, model_name=selected_model)
            st.markdown(summary)
            summaries[section_title] = summary

    # --- Download Summary ---
    summary_text = ""
    for section_title, content in summaries.items():
        summary_text += f"### {section_title.upper()}\n{content}\n\n"

    st.download_button(
        label="💾 Download Summary as .txt",
        data=summary_text,
        file_name="physics_summary.txt",
        mime="text/plain"
    )

    # --- Q&A Section ---
    st.markdown("---")
    st.header("💬 Ask a Question About the Paper")

    question = st.text_input("Type your question here:")

    if question:
        with st.spinner("🤖 Finding the answer..."):
            combined_text = "\n".join(sections.values())
            answer, score = answer_question(question, combined_text)
        st.success(f"**Answer:** {answer}")
        st.caption(f"Confidence: {score:.2f}")

# --- PDF Compatibility Info ---
with st.expander("ℹ️ About PDF compatibility"):
    st.markdown("""
    - This app works best with **text-based PDFs**.
    - Scanned image PDFs (e.g., camera-scanned) will return little or no text.
    - Heavy LaTeX math can reduce summarization accuracy.
    - If the summary looks incomplete, try a different PDF from sources like [arXiv.org](https://arxiv.org/).
    """)

