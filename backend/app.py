from flask import Flask, request, jsonify
import io
from flask_cors import CORS
import pickle
import os
import pandas as pd

# Get the absolute path to the frontend directory
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')
app = Flask(__name__, static_folder=frontend_dir, static_url_path='/')
CORS(app)  # Enable CORS for all routes

@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

# Global variable to hold the model
model = None

def load_model():
    global model
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.pkl')
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            print("Model loaded successfully.")
    else:
        print("Warning: model.pkl not found. Please run the ML pipeline first.")

@app.before_request
def before_first_request():
    if model is None:
        load_model()

@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500
        
    try:
        # Get JSON data from the request
        data = request.json
        
        # Expected features: income, employment_duration, existing_loan_balance, credit_inquiries, payment_status
        # Validate data
        required_fields = ['income', 'employment_duration', 'existing_loan_balance', 'credit_inquiries', 'payment_status']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
                
        # Prepare data for prediction
        input_data = pd.DataFrame([{
            'income': float(data['income']),
            'employment_duration': float(data['employment_duration']),
            'existing_loan_balance': float(data['existing_loan_balance']),
            'credit_inquiries': int(data['credit_inquiries']),
            'payment_status': int(data['payment_status'])
        }])
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0]
        
        # Format response
        result = {
            'approved': bool(prediction == 1),
            'probability': {
                'reject': float(probability[0]),
                'approve': float(probability[1])
            }
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Received data:", data)
        return jsonify({"error": str(e)}), 400
    





@app.route('/api/upload_csv', methods=['POST'])
def upload_csv():

    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    try:
        df = pd.read_csv(file)

        required = [
            'income',
            'employment_duration',
            'existing_loan_balance',
            'credit_inquiries',
            'payment_status'
        ]

        for col in required:
            if col not in df.columns:
                return jsonify({'error': f'Missing column: {col}'}), 400

        X = df[required]

        predictions = model.predict(X)
        probabilities = model.predict_proba(X)

        results = []

        for i in range(len(df)):
            row = df.iloc[i].to_dict()

            row["approved"] = bool(predictions[i] == 1)
            row["approval_probability"] = round(float(probabilities[i][1]) * 100, 2)

            results.append(row)

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None}), 200

if __name__ == '__main__':
    load_model()
    app.run(debug=True, host='0.0.0.0', port=5000)
