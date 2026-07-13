# Credit Card Approval Prediction System

An automated, full-stack machine learning solution designed to evaluate credit card applications instantly. This project streamlines the decision-making process for banks by analyzing applicant financial and demographic data using predictive models, classifying them into approved or rejected states just like real financial institutions.

## 🌟 Overview

Banks receive thousands of credit card applications daily. Manual review is slow and prone to human error. This system automates the process using a trained machine learning model (Logistic Regression) to evaluate inputs like income, employment duration, loan balance, and credit history.

The best-performing model has been integrated into a lightweight **Flask web application**, featuring a premium, responsive frontend. It is configured for easy cloud deployment on **Render**, providing a scalable, real-time prediction endpoint with an intuitive UI.

## 🚀 Key Scenarios & Features

1. **Automated Credit Card Application Screening:**
   Credit analysts can input an applicant's profile to receive an instant prediction, allowing them to prioritize applications requiring manual review.

2. **High-Risk Applicant Identification:**
   Compliance officers can easily batch-screen applicants. The model penalizes high-risk markers (like past-due records), classifying those applicants as ineligible to maintain strict financial compliance.

3. **Customer Self-Service Eligibility Check:**
   Prospective customers can use the sleek web interface to enter their financial details and gauge their likelihood of approval *before* submitting a formal application, reducing unnecessary rejections.

## 🛠️ Technology Stack

- **Machine Learning:** Scikit-Learn, XGBoost, Pandas, Numpy (Logistic Regression, Random Forest, Decision Tree, XGBoost)
- **Backend:** Python, Flask, Gunicorn, Flask-CORS
- **Frontend:** HTML5, Vanilla JavaScript, CSS3 (Glassmorphism UI, Responsive Design)
- **Deployment:** Pre-configured for seamless deployment on [Render](https://render.com)

## 📁 Project Structure

```
├── backend/
│   ├── app.py               # Flask REST API & Static File Server
│   ├── model.pkl            # Trained Logistic Regression Model
│   └── requirements.txt     # Backend specific dependencies
├── frontend/
│   ├── index.html           # Main UI 
│   ├── main.js              # API interaction and UI logic
│   └── style.css            # Premium styles and animations
├── ml_pipeline/
│   └── train_model.py       # Script to generate synthetic data & train models
├── main.py                  # Entry point for Render deployment (Gunicorn)
└── requirements.txt         # Root dependencies for Render auto-build
```

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/thollikondavasavi-max/Credit-Card-Approval-Prediction-System
   cd Credit-Card-Approval-Prediction
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the Model (Optional):**
   *A pre-trained `model.pkl` is already included, but you can retrain it on synthetic data by running:*
   ```bash
   python ml_pipeline/train_model.py
   ```

4. **Start the Application:**
   Because the Flask backend is configured to serve the frontend files directly, you only need to start one server:
   ```bash
   python backend/app.py
   ```
   *Navigate to `http://127.0.0.1:5000` in your web browser to view the application.*


## ☁️ Deployment (Render)

This project is fully configured for deployment on Render as a Web Service.

1. Connect your GitHub repository to Render.
2. Ensure the **Build Command** is set to: `pip install -r requirements.txt`
3. Ensure the **Start Command** is set to: `gunicorn main:app` (Render's default)
4. Render will automatically detect the `main.py` entry point, install dependencies, and serve the full-stack application on a public URL.
