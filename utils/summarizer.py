from transformers import pipeline

# Dictionary of available models
AVAILABLE_MODELS = {
    "BART (facebook/bart-base)": "facebook/bart-base"
}

def summarize_text(text, model_name="t5-small"):
    summarizer = pipeline("summarization", model=model_name)
    try:
        summary = summarizer(text, max_length=150, min_length=40, do_sample=False)[0]["summary_text"]
    except Exception as e:
        summary = f"(Summarization failed: {e})"
    return summary
