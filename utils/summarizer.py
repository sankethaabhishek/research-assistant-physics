from transformers import pipeline

# Dictionary of available models
AVAILABLE_MODELS = {
    "T5 (Small & Fast)": "t5-small",
    "BART (Accurate, Larger)": "facebook/bart-large-cnn"
}

def summarize_text(text, model_name="t5-small"):
    summarizer = pipeline("summarization", model=model_name)
    try:
        summary = summarizer(text, max_length=150, min_length=40, do_sample=False)[0]["summary_text"]
    except Exception as e:
        summary = f"(Summarization failed: {e})"
    return summary
