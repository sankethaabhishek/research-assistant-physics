import streamlit as st
import os
from utils.parser import extract_text_from_pdf
from utils.section_splitter import split_into_sections
from utils.summarizer import summarize_text, AVAILABLE_MODELS
from utils.qa import answer_question

# --- Load Custom CSS ---
def load_custom_css(css_file):
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            print("✅ CSS loaded successfully")
    else:
        st.warning(f"⚠️ CSS file '{css_file}' not found!")
        print(f"❌ CSS file '{css_file}' not found!")

load_custom_css("streamlit_theme.css")

# --- Page Configuration ---
st.set_page_config(page_title="Physics Research Assistant", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.title("🔬 Physics AI Assistant")
    st.markdown("Upload a PDF of a physics research paper and get AI-generated summaries by section.")
    selected_model_label = st.selectbox("🧠 Choose summarization model:", list(AVAILABLE_MODELS.keys()))
    selected_model = AVAILABLE_MODELS[selected_model_label]
    st.markdown("---")
    st.markdown("🧑‍🔬 Built by Sanketha Abhishek")
    st.markdown("📝 Works best with clean, text-based PDFs.")

# --- Main Area ---
st.title("📄 Research Paper Summarizer")

uploaded_file = st.file_uploader("📁 Upload a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("⏳ Extracting and summarizing..."):
        # Save uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        full_text = extract_text_from_pdf("temp.pdf")
        sections = split_into_sections(full_text)

    st.success("✅ Summary ready!")

    summaries = {}

    for title, content in sections.items():
        with st.expander(f"📌 {title.upper()}"):
            summary = summarize_text(content, model_name=selected_model)
            st.markdown(summary)
            summaries[title] = summary

    summary_text = "\n".join([f"### {title.upper()}\n{content}" for title, content in summaries.items()])

    st.download_button(
        label="💾 Download Summary as .txt",
        data=summary_text,
        file_name="physics_summary.txt",
        mime="text/plain"
    )

# --- PDF Compatibility Notice ---
with st.expander("ℹ️ About PDF compatibility"):
    st.markdown("""
    - Works best with **text-based PDFs** (not scanned images).
    - Heavy LaTeX math can reduce summarization accuracy.
    - Try papers from [arXiv.org](https://arxiv.org/) for best results.
    """)

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
