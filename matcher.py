import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Words that show up in job posts but say nothing about skills.
EXTRA_STOPWORDS = {
    "experience", "work", "team", "role", "will", "ability", "strong", "good",
    "build", "create", "intern", "developer", "knowledge", "communication",
    "clean", "required", "preferred", "plus", "needed", "looking",
}


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


def missing_keywords(resume_text, job_text, top_n=8):
    """Important words in the job post that never appear in the resume."""
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform([clean_text(job_text)])
    terms = vectorizer.get_feature_names_out()
    weights = tfidf.toarray()[0]
    resume_words = set(clean_text(resume_text).split())
    candidates = sorted(zip(terms, weights), key=lambda x: x[1], reverse=True)
    missing = [t for t, _ in candidates if t not in resume_words and t not in EXTRA_STOPWORDS]
    return missing[:top_n]
