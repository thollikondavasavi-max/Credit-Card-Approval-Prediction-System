"""
Credit Card Approval - Model Training & Evaluation Script
Generates metric graphs, confusion matrices, ROC curves,
feature importance plots, and training results for the UI.
"""

import warnings
warnings.filterwarnings('ignore')

import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc,
    roc_auc_score
)

# Set encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
MODEL_DIR = os.path.join(BASE_DIR, 'model')
SCREENSHOTS_DIR = os.path.join(BASE_DIR, 'static', 'screenshots')
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

CHECK = "[OK]"

print("=" * 60)
print("CREDIT CARD APPROVAL - MODEL TRAINING")
print("=" * 60)

print(f"\n[1/13] Loading datasets...")
application = pd.read_csv(os.path.join(DATASET_DIR, 'application_record.csv'))
credit = pd.read_csv(os.path.join(DATASET_DIR, 'credit_record.csv'))
print(f"  {CHECK} Application: {application.shape}")
print(f"  {CHECK} Credit: {credit.shape}")

print(f"\n[2/13] Creating target variable...")
bad_status = ['2', '3', '4', '5']
credit['TARGET'] = credit['STATUS'].apply(lambda x: 1 if x in bad_status else 0)
target = credit.groupby('ID')['TARGET'].max().reset_index()
print(f"  {CHECK} Total customers: {len(target)}")

print(f"\n[3/13] Merging datasets...")
df = application.merge(target, on='ID', how='inner')
print(f"  {CHECK} Merged shape: {df.shape}")

print(f"\n[4/13] Handling missing values...")
df['OCCUPATION_TYPE'] = df['OCCUPATION_TYPE'].fillna('Unknown')
print(f"  {CHECK} Missing values filled")

print(f"\n[5/13] Feature engineering...")
df['AGE'] = (-df['DAYS_BIRTH'] / 365).astype(int)
df['DAYS_EMPLOYED'] = df['DAYS_EMPLOYED'].replace(365243, 0)
df['YEARS_EMPLOYED'] = (abs(df['DAYS_EMPLOYED']) / 365).astype(int)
df.drop(columns=['ID', 'DAYS_BIRTH', 'DAYS_EMPLOYED'], inplace=True)
print(f"  {CHECK} Shape: {df.shape}")

print(f"\n[6/13] Removing duplicates...")
before = df.shape[0]
df = df.drop_duplicates()
print(f"  {CHECK} Removed {before - df.shape[0]} duplicates, shape: {df.shape}")

print(f"\n[7/13] Class distribution:")
target_counts = df['TARGET'].value_counts()
print(f"  Approved (0): {target_counts.get(0, 0)}")
print(f"  Rejected (1): {target_counts.get(1, 0)}")
rej_pct = round(target_counts.get(1, 0) / len(df) * 100, 2)
print(f"  Rejection rate: {rej_pct}%")

print(f"\n[8/13] Encoding categorical variables...")
categorical_columns = df.select_dtypes(include='object').columns.tolist()
label_encoders = {}
for column in categorical_columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le
print(f"  {CHECK} {len(categorical_columns)} columns encoded")

print(f"\n[9/13] Splitting dataset...")
X = df.drop('TARGET', axis=1)
y = df['TARGET']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
print(f"  {CHECK} Training: {X_train.shape}, Testing: {X_test.shape}")

print(f"\n[10/13] Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
joblib.dump(scaler, os.path.join(MODEL_DIR, 'scaler.pkl'))
print(f"  {CHECK} Scaler saved")

print(f"\n[11/13] Training models...")
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=200, random_state=42)
}
results = {}

for name, model in models.items():
    print(f"\n  Training {name}...")
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_prob)
    results[name] = {'accuracy': round(acc, 4), 'precision': round(prec, 4), 'recall': round(rec, 4), 'f1_score': round(f1, 4), 'roc_auc': round(roc_auc, 4), 'model': model, 'y_pred': y_pred, 'y_prob': y_prob}
    print(f"    Accuracy:  {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}, ROC-AUC: {roc_auc:.4f}")

print(f"\n[12/13] Selecting best model...")
best_model_name = max(results, key=lambda k: results[k]['accuracy'])
best_model = results[best_model_name]['model']
print(f"  {CHECK} Best: {best_model_name} ({results[best_model_name]['accuracy']:.4f})")
joblib.dump(best_model, os.path.join(MODEL_DIR, 'best_model.pkl'))

print(f"\n[13/13] Generating metric graphs...")

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# 1. Model Comparison Bar Chart
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Model Performance Comparison', fontsize=18, fontweight='bold')
metrics_to_plot = ['accuracy', 'precision', 'recall', 'f1_score']
titles = ['Accuracy Comparison', 'Precision Comparison', 'Recall Comparison', 'F1-Score Comparison']
for idx, (metric, title) in enumerate(zip(metrics_to_plot, titles)):
    ax = axes[idx // 2][idx % 2]
    names = list(results.keys())
    values = [results[n][metric] for n in names]
    colors = ['#2563eb', '#16a34a', '#dc2626']
    bars = ax.bar(names, values, color=colors, edgecolor='white', linewidth=1.5)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_ylim(0, 1.1)
    ax.set_ylabel('Score')
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{val:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    ax.tick_params(axis='x', rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(SCREENSHOTS_DIR, 'model_comparison.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"  1/6 Model comparison chart saved")

# 2. Confusion Matrices
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
fig.suptitle('Confusion Matrices', fontsize=18, fontweight='bold')
for idx, (name, result) in enumerate(results.items()):
    ax = axes[idx]
    cm = confusion_matrix(y_test, result['y_pred'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax, xticklabels=['Approved', 'Rejected'], yticklabels=['Approved', 'Rejected'])
    ax.set_title(f'{name}', fontsize=13, fontweight='bold')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
plt.tight_layout()
plt.savefig(os.path.join(SCREENSHOTS_DIR, 'confusion_matrices.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"  2/6 Confusion matrices saved")

# 3. ROC Curves
fig, ax = plt.subplots(figsize=(8, 6))
for name, result in results.items():
    fpr, tpr, _ = roc_curve(y_test, result['y_prob'])
    roc_auc = result['roc_auc']
    ax.plot(fpr, tpr, lw=2.5, label=f'{name} (AUC = {roc_auc:.4f})')
ax.plot([0, 1], [0, 1], 'k--', lw=1, label='Random Classifier')
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel('False Positive Rate', fontsize=13)
ax.set_ylabel('True Positive Rate', fontsize=13)
ax.set_title('ROC Curves Comparison', fontsize=16, fontweight='bold')
ax.legend(loc='lower right', fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(SCREENSHOTS_DIR, 'roc_curves.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"  3/6 ROC curves saved")

# 4. Feature Importance (Random Forest)
rf_model = results['Random Forest']['model']
if hasattr(rf_model, 'feature_importances_'):
    fig, ax = plt.subplots(figsize=(10, 7))
    feature_names = X.columns.tolist()
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[::-1][:15]
    colors = plt.cm.Blues(np.linspace(0.4, 1, len(indices)))
    bars = ax.barh(range(len(indices)), importances[indices][::-1], color=colors[::-1], edgecolor='white')
    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels([feature_names[i] for i in indices][::-1])
    ax.set_xlabel('Importance', fontsize=13)
    ax.set_title('Random Forest - Feature Importance (Top 15)', fontsize=16, fontweight='bold')
    ax.invert_yaxis()
    for bar, val in zip(bars, importances[indices][::-1]):
        ax.text(val + 0.002, bar.get_y() + bar.get_height()/2, f'{val:.3f}', ha='left', va='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(SCREENSHOTS_DIR, 'feature_importance.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  4/6 Feature importance chart saved")

# 5. Classification Report Table
fig, ax = plt.subplots(figsize=(14, 5))
ax.axis('off')
table_data = []
col_labels = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
for name in results:
    r = results[name]
    table_data.append([name, f"{r['accuracy']:.4f}", f"{r['precision']:.4f}", f"{r['recall']:.4f}", f"{r['f1_score']:.4f}", f"{r['roc_auc']:.4f}"])
table = ax.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.8)
for j in range(len(col_labels)):
    table[0, j].set_facecolor('#2563eb')
    table[0, j].set_text_props(color='white', fontweight='bold')
colors_row = ['#f0f4ff', '#ffffff']
for i in range(len(table_data)):
    for j in range(len(col_labels)):
        table[i+1, j].set_facecolor(colors_row[i % 2])
ax.set_title('Model Performance Summary', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(os.path.join(SCREENSHOTS_DIR, 'classification_report.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"  5/6 Classification report table saved")

# 6. Data Distribution Pie Chart
fig, ax = plt.subplots(figsize=(7, 7))
labels = ['Approved (0)', 'Rejected (1)']
sizes = [target_counts.get(0, 0), target_counts.get(1, 0)]
colors_pie = ['#22c55e', '#ef4444']
explode = (0.02, 0.08)
wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors_pie, autopct='%1.1f%%', startangle=90, shadow=True, textprops={'fontsize': 13, 'fontweight': 'bold'})
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(14)
ax.set_title('Data Distribution', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(SCREENSHOTS_DIR, 'data_distribution.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"  6/6 Data distribution chart saved")

# Save training metrics as JSON
metrics_summary = {}
for name in results:
    metrics_summary[name] = {
        'accuracy': results[name]['accuracy'],
        'precision': results[name]['precision'],
        'recall': results[name]['recall'],
        'f1_score': results[name]['f1_score'],
        'roc_auc': results[name]['roc_auc']
    }
metrics_summary['best_model'] = best_model_name
metrics_summary['training_samples'] = int(X_train.shape[0])
metrics_summary['testing_samples'] = int(X_test.shape[0])
metrics_summary['total_samples'] = int(len(df))
metrics_summary['rejection_rate'] = rej_pct
metrics_summary['feature_count'] = int(X.shape[1])

with open(os.path.join(SCREENSHOTS_DIR, 'metrics.json'), 'w') as f:
    json.dump(metrics_summary, f, indent=2)
print(f"  Metrics saved to JSON")

# -----------------------------
# Build and save sklearn Pipeline (matching original format)
# -----------------------------
print(f"\n[14/14] Building sklearn Pipeline for deployment...")

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

# Reload data with original categorical values
application = pd.read_csv(os.path.join(DATASET_DIR, 'application_record.csv'))
credit = pd.read_csv(os.path.join(DATASET_DIR, 'credit_record.csv'))

# Recreate target
credit['TARGET'] = credit['STATUS'].apply(lambda x: 1 if x in bad_status else 0)
target = credit.groupby('ID')['TARGET'].max().reset_index()
df_pipe = application.merge(target, on='ID', how='inner')
df_pipe['OCCUPATION_TYPE'] = df_pipe['OCCUPATION_TYPE'].fillna('Unknown')

# Feature engineering
df_pipe['AGE'] = (-df_pipe['DAYS_BIRTH'] / 365).astype(int)
df_pipe['DAYS_EMPLOYED'] = df_pipe['DAYS_EMPLOYED'].replace(365243, 0)
df_pipe['YEARS_EMPLOYED'] = (abs(df_pipe['DAYS_EMPLOYED']) / 365).astype(int)
df_pipe.drop(columns=['ID', 'DAYS_BIRTH', 'DAYS_EMPLOYED'], inplace=True)
df_pipe = df_pipe.drop_duplicates()

X_pipe = df_pipe.drop('TARGET', axis=1)
y_pipe = df_pipe['TARGET']

# Define column types for the pipeline
numeric_features = ['CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'FLAG_MOBIL', 
                    'FLAG_WORK_PHONE', 'FLAG_PHONE', 'FLAG_EMAIL', 
                    'CNT_FAM_MEMBERS', 'AGE', 'YEARS_EMPLOYED']
categorical_features = ['CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY',
                       'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 
                       'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE', 
                       'OCCUPATION_TYPE']

# Build the pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', best_model)
])

pipeline.fit(X_pipe, y_pipe)

# Save pipeline (overwrites old one with version-compatible version)
pipeline_path = os.path.join(MODEL_DIR, 'credit_card_pipeline.pkl')
joblib.dump(pipeline, pipeline_path)
print(f"  Pipeline saved to {pipeline_path}")

print(f"\n{'=' * 60}")
print("TRAINING COMPLETE!")
print(f"{'=' * 60}")
print(f"Best Model: {best_model_name}")
print(f"Best Accuracy: {results[best_model_name]['accuracy']:.4f}")
print(f"Generated 6 metric graphs + JSON data + Pipeline")
