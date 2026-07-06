# Model Building

## Description

This phase focuses on training and evaluating multiple machine learning classification models to predict whether a credit card application should be approved or rejected. Each model is trained using the pre-processed dataset and assessed using various evaluation metrics such as accuracy, precision, recall, and F1-score.

The objective is to identify the best-performing model based on predictive performance and generalization capability. The selected model is then saved and prepared for deployment in the web application.

### Models Used

#### 1. Logistic Regression Model

The Logistic Regression model is used as a baseline classification algorithm for binary prediction tasks. It estimates the probability of an application being approved or rejected based on the input features and provides fast and interpretable results.

#### 2. Random Forest Model

The Random Forest model is an ensemble learning algorithm that combines multiple decision trees to improve prediction accuracy and reduce overfitting. It is capable of handling complex relationships and interactions among features.

#### 3. Decision Tree Model

The Decision Tree model classifies applications by creating a tree-like structure of decisions based on feature values. It is easy to interpret and helps in understanding the factors influencing credit card approval decisions.

## Model Selection

After training and evaluation, the performance of all models is compared using appropriate evaluation metrics. The model with the highest predictive performance is selected as the final model and serialized using pickle for deployment in the Credit Card Approval Prediction application.
