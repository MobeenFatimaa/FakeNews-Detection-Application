
import re
import nltk

nltk.data.path.append("/tmp/nltk_data")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", download_dir="/tmp/nltk_data")
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]',' ',text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)
import re
import nltk
from nltk.corpus import stopwords

# Download stopwords only once
try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))


def clean_text(text):
    """
    Clean news article text for TF-IDF + Logistic Regression.
    """

    if not isinstance(text, str):
        text = str(text)

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Remove HTML
    text = re.sub(r"<.*?>", " ", text)

    # Remove punctuation and numbers
    text = re.sub(r"[^a-z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Remove stopwords
    words = [word for word in text.split() if word not in stop_words]

    return " ".join(words)
