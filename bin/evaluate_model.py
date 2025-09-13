import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Evaluate the trained model.')
parser.add_argument('--model', type=str, required=True, help='Input model file path')
parser.add_argument('--x_test', type=str, required=True, help='Input X_test CSV file path')
parser.add_argument('--y_test', type=str, required=True, help='Input y_test CSV file path')
parser.add_argument('--report', type=str, required=True, help='Output report file path')
parser.add_argument('--cm', type=str, required=True, help='Output confusion matrix image path')
parser.add_argument('--roc', type=str, required=True, help='Output ROC curve image path')
args = parser.parse_args()

# Load the model and test data
model = joblib.load(args.model)
X_test = pd.read_csv(args.x_test)
y_test = pd.read_csv(args.y_test)

# Make predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# --- Save Classification Report ---
report = classification_report(y_test, y_pred, target_names=['Benign', 'Pathogenic'])
with open(args.report, 'w') as f:
    f.write(report)
print(f"Classification report saved to {args.report}")

# --- Generate and Save Confusion Matrix ---
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Benign', 'Pathogenic'], yticklabels=['Benign', 'Pathogenic'])
plt.title('Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.savefig(args.cm)
print(f"Confusion matrix saved to {args.cm}")

# --- Generate and Save ROC Curve ---
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.savefig(args.roc)
print(f"ROC curve saved to {args.roc}")