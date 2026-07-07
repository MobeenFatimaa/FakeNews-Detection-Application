import re
import nltk
from nltk.corpus import stopwords

# Use writable directory on Vercel
NLTK_DATA = "/tmp/nltk_data"
nltk.data.path.append(NLTK_DATA)

try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords", download_dir=NLTK_DATA)
    stop_words = set(stopwords.words("english"))


def clean_text(text):
    if not isinstance(text, str):
        text = str(text)

    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    words = [word for word in text.split() if word not in stop_words]

    return " ".join(words)
