import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import xgboost as xgb

def generate_synthetic_data(num_samples=5000):
    np.random.seed(42)
    
    # Generate features
    income = np.random.normal(60000, 20000, num_samples)
    income = np.clip(income, 20000, 200000)
    
    employment_duration = np.random.normal(5, 3, num_samples)
    employment_duration = np.clip(employment_duration, 0, 40)
    
    existing_loan_balance = np.random.normal(15000, 10000, num_samples)
    existing_loan_balance = np.clip(existing_loan_balance, 0, 100000)
    
    credit_inquiries = np.random.poisson(1.5, num_samples)
    
    # payment_status: 0 for good standing, 1 for past-due/high-risk
    payment_status = np.random.choice([0, 1], size=num_samples, p=[0.8, 0.2])
    
    # Create DataFrame
    df = pd.DataFrame({
        'income': income,
        'employment_duration': employment_duration,
        'existing_loan_balance': existing_loan_balance,
        'credit_inquiries': credit_inquiries,
        'payment_status': payment_status
    })
    
    # Define Target Logic (Approval Probability)
    # Higher income -> better
    # Longer employment -> better
    # Higher loan balance -> worse
    # More credit inquiries -> worse
    # Past due (payment_status=1) -> significantly worse
    score = (
        (df['income'] / 60000) * 2 + 
        (df['employment_duration'] / 5) * 1.5 - 
        (df['existing_loan_balance'] / 15000) * 1.5 - 
        df['credit_inquiries'] * 1.0 - 
        df['payment_status'] * 4.0
    )
    
    # Add some noise
    score += np.random.normal(0, 1.5, num_samples)
    
    # Convert to binary target
    df['approved'] = (score > 1.0).astype(int)
    
    return df

def train_and_evaluate():
    print("Generating synthetic data...")
    df = generate_synthetic_data()
    
    X = df.drop('approved', axis=1)
    y = df['approved']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'XGBoost': xgb.XGBClassifier(eval_metric='logloss', random_state=42)
    }
    
    best_model = None
    best_accuracy = 0
    best_model_name = ""
    
    print("\nTraining models...")
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"{name} Accuracy: {acc:.4f}")
        
        if acc > best_accuracy:
            best_accuracy = acc
            best_model = model
            best_model_name = name
            
    print(f"\nBest Model: {best_model_name} with Accuracy: {best_accuracy:.4f}")
    
    # Save the best model
    # We will save it in the backend directory so the Flask app can access it
    backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
    model_path = os.path.join(backend_dir, 'model.pkl')
    
    with open(model_path, 'wb') as f:
        pickle.dump(best_model, f)
        
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_evaluate()
