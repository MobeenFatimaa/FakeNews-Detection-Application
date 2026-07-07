import os
import joblib
from preprocess import clean_text

model_path = "../models/fake_news_model.pkl"

if not os.path.exists(model_path):
    print("Model not found! Train the model first.")
    exit()

model = joblib.load(model_path)

print("Fake News Detector")
print("Type 'exit' to quit.\n")

while True:
    text = input("Enter news text: ")

    if text.lower() == "exit":
        break

    cleaned = clean_text(text)
    prediction = model.predict([cleaned])[0]

    print("Prediction:", prediction)