import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text):
    """Lowercase the text and remove symbols, but keep c++, node.js, etc."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    text = re.sub(r"\.+(?=\s|$)", "", text)   # remove full stops at the end of words
    return re.sub(r"\s+", " ", text).strip()


def rank_jobs(resume_text, jobs):
    """Return (job_name, score) pairs sorted from best to worst match.

    jobs is a dict like {"data.txt": "job description text"}.
    The score is a 0-100 number.
    """
    if not jobs:
        return []
    names = list(jobs)
    docs = [clean_text(resume_text)] + [clean_text(jobs[n]) for n in names]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(docs)
    scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
    ranked = sorted(zip(names, scores), key=lambda x: x[1], reverse=True)
    return [(name, round(float(score) * 100, 1)) for name, score in ranked]
