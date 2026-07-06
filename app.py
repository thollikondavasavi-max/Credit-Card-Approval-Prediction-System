import warnings
warnings.filterwarnings('ignore')

import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import joblib

app = Flask(__name__)

# -----------------------------
# Load trained pipeline & metadata
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "credit_card_pipeline.pkl")
METRICS_PATH = os.path.join(BASE_DIR, "static", "screenshots", "metrics.json")

# Load model with error handling
pipeline = None
try:
    pipeline = joblib.load(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"Warning: Could not load model: {e}")

# Load training metrics
metrics_data = {}
if os.path.exists(METRICS_PATH):
    try:
        with open(METRICS_PATH, 'r') as f:
            metrics_data = json.load(f)
        print(f"Metrics loaded: {len(metrics_data)} entries")
    except Exception as e:
        print(f"Warning: Could not load metrics: {e}")

# Dynamically list screenshot images from the folder
def get_screenshots():
    screenshot_extensions = ('.png', '.jpg', '.jpeg')
    screenshots_dir = os.path.join(BASE_DIR, 'static', 'screenshots')
    screenshots = []
    descriptions = {
        'model_comparison': 'Compares Accuracy, Precision, Recall, and F1-Score across all three models.',
        'confusion_matrices': 'Shows confusion matrices for all models.',
        'roc_curves': 'ROC curves showing the trade-off between True Positive Rate and False Positive Rate.',
        'feature_importance': 'Random Forest feature importance ranking showing which features most influence predictions.',
        'classification_report': 'Tabular summary of all model performance metrics.',
        'data_distribution': 'Pie chart showing approved vs rejected applications in the dataset.'
    }
    if os.path.exists(screenshots_dir):
        for fname in sorted(os.listdir(screenshots_dir)):
            if fname.lower().endswith(screenshot_extensions):
                name = os.path.splitext(fname)[0]
                title = ' '.join(word.capitalize() for word in name.replace('_', ' ').split())
                desc = descriptions.get(name, f'{title} visualization from model training.')
                ext = os.path.splitext(fname)[1].upper()
                screenshots.append({'filename': fname, 'title': title, 'desc': desc, 'format': ext})
    return screenshots

screenshots_list = get_screenshots()

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html", metrics=metrics_data, screenshots=screenshots_list)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        if pipeline is None:
            return render_template("index.html",
                prediction="Model Not Available",
                confidence=0, rejection=0, risk="ERROR",
                risk_color="#dc2626",
                analysis="The prediction model is not loaded. Please ensure the model file exists and restart the server.",
                metrics=metrics_data)

        user_data = {
            "CODE_GENDER": request.form["gender"],
            "FLAG_OWN_CAR": request.form["car"],
            "FLAG_OWN_REALTY": request.form["realty"],
            "CNT_CHILDREN": int(request.form["children"]),
            "AMT_INCOME_TOTAL": float(request.form["income"]),
            "NAME_INCOME_TYPE": request.form["income_type"],
            "NAME_EDUCATION_TYPE": request.form["education"],
            "NAME_FAMILY_STATUS": request.form["family_status"],
            "NAME_HOUSING_TYPE": request.form["housing_type"],
            "FLAG_MOBIL": int(request.form["mobile"]),
            "FLAG_WORK_PHONE": int(request.form["work_phone"]),
            "FLAG_PHONE": int(request.form["phone"]),
            "FLAG_EMAIL": int(request.form["email"]),
            "OCCUPATION_TYPE": request.form["occupation"],
            "CNT_FAM_MEMBERS": float(request.form["family_members"]),
            "AGE": int(request.form["age"]),
            "YEARS_EMPLOYED": int(request.form["years_employed"])
        }

        input_df = pd.DataFrame([user_data])
        prediction = pipeline.predict(input_df)[0]
        probability = pipeline.predict_proba(input_df)[0]

        # Class 0 = Approved, Class 1 = Rejected
        approval_probability = round(probability[0] * 100, 2)
        rejection_probability = round(probability[1] * 100, 2)

        if prediction == 0:
            decision = "CREDIT CARD APPROVED"
        else:
            decision = "CREDIT CARD REJECTED"

        if approval_probability >= 85:
            risk = "LOW RISK"
            risk_color = "#16a34a"
            recommendation = (
                "Applicant has a stable financial profile with "
                "a low probability of default. "
                "Credit card approval is recommended."
            )
        elif approval_probability >= 60:
            risk = "MEDIUM RISK"
            risk_color = "#f59e0b"
            recommendation = (
                "Applicant satisfies most approval criteria. "
                "Manual verification is recommended before approval."
            )
        else:
            risk = "HIGH RISK"
            risk_color = "#dc2626"
            recommendation = (
                "Applicant has a high probability of default. "
                "Credit card approval is not recommended."
            )

        return render_template(
            "index.html",
            prediction=decision,
            confidence=approval_probability,
            rejection=rejection_probability,
            risk=risk,
            risk_color=risk_color,
            analysis=recommendation,
            metrics=metrics_data, screenshots=screenshots_list
        )

    except Exception as e:
        return render_template(
            "index.html",
            prediction="Prediction Error",
            confidence=0,
            rejection=0,
            risk="N/A",
            risk_color="#dc2626",
            analysis=f"An error occurred: {str(e)}. Please check your inputs and try again.",
            metrics=metrics_data, screenshots=screenshots_list
        )


@app.route("/api/metrics")
def api_metrics():
    return jsonify(metrics_data)


@app.route("/screenshots/<filename>")
def screenshots(filename):
    return send_from_directory(
        os.path.join(BASE_DIR, "static", "screenshots"),
        filename
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
