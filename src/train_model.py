import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

from preprocess import clean_text


print("=" * 50)
print("FAKE NEWS DETECTION MODEL TRAINING")
print("=" * 50)

# -------------------------
# Load Dataset
# -------------------------

dataset_path = os.path.join("data", "news_dataset.csv")

df = pd.read_csv(dataset_path)

print(f"Dataset Loaded Successfully")
print(f"Total Articles : {len(df)}")

# -------------------------
# Combine Title + Text
# -------------------------

df["title"] = df["title"].fillna("")
df["text"] = df["text"].fillna("")

df["content"] = df["title"] + " " + df["text"]

# -------------------------
# Clean Text
# -------------------------

print("Cleaning Articles...")

df["content"] = df["content"].apply(clean_text)

# -------------------------
# Features & Labels
# -------------------------

X = df["content"]
y = df["label"]

# -------------------------
# Train/Test Split
# -------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# -------------------------
# Build Pipeline
# -------------------------

print("Training Logistic Regression...")

pipeline = Pipeline([

    (
        "tfidf",
        TfidfVectorizer(
            stop_words="english",
            lowercase=True,
            max_features=20000,
            ngram_range=(1,2)
        )
    ),

    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            random_state=42
        )
    )

])

pipeline.fit(X_train, y_train)

# -------------------------
# Evaluate
# -------------------------

predictions = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nTraining Completed Successfully!")
print(f"\nAccuracy : {accuracy*100:.2f}%\n")

print(classification_report(y_test, predictions))

# -------------------------
# Save Model
# -------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(pipeline, "models/fake_news_model.pkl")

print("\nModel Saved Successfully!")
print("models/fake_news_model.pkl")