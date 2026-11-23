import re

def clean_text(text):
    """Lowercase the text and remove symbols, but keep c++, node.js, etc."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    text = re.sub(r"\.+(?=\s|$)", "", text)   # remove full stops at the end of words
    return re.sub(r"\s+", " ", text).strip()