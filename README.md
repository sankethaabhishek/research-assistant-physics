# 🔬 Physics Research Assistant

An AI-powered research assistant for physics papers. Upload a physics research PDF and get section-wise summaries and direct Q&A with an LLM.

📍 **Live App:** [research-assistant-physics.streamlit.app](https://research-assistant-physics.streamlit.app)

---

## 🚀 Features
- 📄 Upload a physics research paper (PDF)
- 🧠 Choose a summarization model (e.g., BART, T5)
- 📚 Get section-wise summaries (Abstract, Introduction, etc.)
- 💬 Ask questions about the paper using the built-in LLM
- 💾 Download generated summaries as `.txt` file

---

## ⚙️ How It Works
1. Upload your physics research paper PDF.
2. The app extracts text and splits it into logical sections.
3. Each section is summarized using the selected model.
4. You can ask questions about the content, and the app will answer them using an LLM-based QA model.

> ❗ Best used with clean, text-based PDFs (e.g., from arXiv.org). Scanned PDFs may not work properly.

---

## 🛠 Tech Stack
- [Streamlit](https://streamlit.io/)
- Hugging Face Transformers (`BART`, `T5`, etc.)
- PDFMiner / PyMuPDF for text extraction
- Custom text splitting & summarization logic
- Hosted on [Streamlit Cloud](https://streamlit.io/cloud)

---

## 💻 Run Locally
Clone the repo and install dependencies:
```bash
git clone https://github.com/sankethaabhishek/research-assistant-physics.git
cd research-assistant-physics

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

