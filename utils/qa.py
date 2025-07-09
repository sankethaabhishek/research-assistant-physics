from transformers import pipeline
from typing import List, Tuple
import re

# Load QA pipeline once
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Split long text into smaller overlapping chunks
def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(len(words), start + chunk_size)
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def answer_question(question: str, context_text: str) -> Tuple[str, float]:
    chunks = chunk_text(context_text)
    best_answer = ""
    best_score = 0.0

    for chunk in chunks:
        result = qa_pipeline(question=question, context=chunk)
        if result["score"] > best_score:
            best_score = result["score"]
            best_answer = result["answer"]

    return best_answer, best_score
