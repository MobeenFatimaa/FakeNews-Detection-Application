import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import time
from datasets import Dataset

from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments
)
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

print("=" * 50)
print("Device :", device)
print("=" * 50)
# ==========================================
# Project Paths
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")

MODEL_DIR = os.path.join(BASE_DIR, "models", "distilbert_model")

os.makedirs(MODEL_DIR, exist_ok=True)


# ==========================================
# Load Combined Dataset
# ==========================================

print("Loading dataset...")

data = pd.read_csv(os.path.join(DATA_DIR, "news_dataset.csv"))

# Combine title and text into one field
data["content"] = (
    data["title"].fillna("") + " " + data["text"].fillna("")
)

# Keep only the columns we need
data = data[["content", "label"]]

# Shuffle dataset
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

print("Total Articles :", len(data))


print("\nDataset Information")
print("-" * 40)

print(data["label"].value_counts())

print("-" * 40)

# ==========================================
# Train Test Split
# ==========================================

train_texts, test_texts, train_labels, test_labels = train_test_split(

    data["content"],

    data["label"],

    test_size=0.2,

    random_state=42,

    stratify=data["label"]

)

print("Training Articles :", len(train_texts))
print("Testing Articles  :", len(test_texts))

# ==========================================
# Tokenizer
# ==========================================

print("\nLoading DistilBERT Tokenizer...\n")

tokenizer = DistilBertTokenizerFast.from_pretrained(
    "distilbert-base-uncased"
)

train_encodings = tokenizer(

    train_texts.tolist(),

    truncation=True,

   padding="max_length",

    max_length=128

)

test_encodings = tokenizer(

    test_texts.tolist(),

    truncation=True,

    padding="max_length",

    max_length=128

)

# ==========================================
# HuggingFace Dataset
# ==========================================

train_dataset = Dataset.from_dict({

    "input_ids": train_encodings["input_ids"],

    "attention_mask": train_encodings["attention_mask"],

    "labels": train_labels.tolist()

})

test_dataset = Dataset.from_dict({

    "input_ids": test_encodings["input_ids"],

    "attention_mask": test_encodings["attention_mask"],

    "labels": test_labels.tolist()

})

# ==========================================
# Load DistilBERT
# ==========================================

print("Loading DistilBERT Model...\n")

model = DistilBertForSequenceClassification.from_pretrained(

    "distilbert-base-uncased",

    num_labels=2

)

# ==========================================
# Metrics
# ==========================================

def compute_metrics(pred):

    labels = pred.label_ids

    preds = np.argmax(pred.predictions, axis=1)

    precision, recall, f1, _ = precision_recall_fscore_support(

        labels,

        preds,

        average="binary"

    )

    acc = accuracy_score(labels, preds)

    return {

        "accuracy": acc,

        "precision": precision,

        "recall": recall,

        "f1": f1

    }

# ==========================================
# Training Arguments
# ==========================================
# ==========================================
# Training Arguments
# ==========================================
training_args = TrainingArguments(

    output_dir=MODEL_DIR,

    overwrite_output_dir=True,

    num_train_epochs=2,

    per_device_train_batch_size=2,

    per_device_eval_batch_size=2,

    learning_rate=2e-5,

    logging_steps=100,

    eval_strategy="epoch",

    save_strategy="epoch",

    load_best_model_at_end=True,

    metric_for_best_model="accuracy",

    greater_is_better=True,

    save_total_limit=1,

    report_to="none",

    fp16=False
)
   
# ==========================================
# Trainer
# ==========================================
trainer = Trainer(

    model=model,

    args=training_args,

    train_dataset=train_dataset,

    eval_dataset=test_dataset,

    compute_metrics=compute_metrics

)

# ==========================================
# Train
# ==========================================

print("\nTraining Started...\n")
start = time.time()
trainer.train()
end = time.time()

print("\nTraining Time:")
print(round((end - start) / 60, 2), "minutes")
print("\nEvaluating...\n")

metrics = trainer.evaluate()


print("\nFinal Results")
print("=" * 40)

print(f"Accuracy : {metrics['eval_accuracy']:.4f}")
print(f"Precision: {metrics['eval_precision']:.4f}")
print(f"Recall   : {metrics['eval_recall']:.4f}")
print(f"F1 Score : {metrics['eval_f1']:.4f}")

print("=" * 40)

# ==========================================
# Save Model
# ==========================================

print("\nSaving Model...\n")

trainer.save_model(MODEL_DIR)

tokenizer.save_pretrained(MODEL_DIR)

print("\n===================================")
print("DistilBERT Model Saved Successfully")
print("Location :", MODEL_DIR)
print("===================================")