from flask import Flask, render_template, request, jsonify
import joblib
import os

from src.preprocess import clean_text

app = Flask(__name__)

# -----------------------------
# Load Model
# -----------------------------
MODEL_PATH = os.path.join("models", "fake_news_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("Model Loaded Successfully")
except Exception as e:
    print("Error Loading Model:", e)
    model = None


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Prediction Route
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    if model is None:
        return jsonify({
            "prediction": "Error",
            "message": "Model not loaded."
        })

    news = request.form.get("news", "").strip()

    if news == "":
        return jsonify({
            "prediction": "Error",
            "message": "Please enter news."
        })

    try:

        cleaned = clean_text(news)

        prediction = model.predict([cleaned])[0]

        # Logistic Regression Probability
        probability = model.predict_proba([cleaned])[0]

        confidence = float(max(probability))

        if str(prediction) in ["1", "Real", "real"]:
            result = "Real"
        else:
            result = "Fake"

        return jsonify({
            "prediction": result,
            "confidence": confidence
        })

    except Exception as e:

        return jsonify({
            "prediction": "Error",
            "message": str(e)
        })


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)