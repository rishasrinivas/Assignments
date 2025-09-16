# src/evaluate.py
import pandas as pd
import os
import joblib
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, auc, ConfusionMatrixDisplay, RocCurveDisplay, classification_report

MODEL_PATH = "best_model.joblib"
DATA_DIR = "data/processed"
OUT_DIR = "results"
os.makedirs(OUT_DIR, exist_ok=True)

def main():
    clf = joblib.load(MODEL_PATH)
    X_test = pd.read_csv(os.path.join(DATA_DIR, "X_test.csv"))
    y_test = pd.read_csv(os.path.join(DATA_DIR, "y_test.csv")).squeeze()

    # Make predictions
    y_pred = clf.predict(X_test)

    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, zero_division=0),
        'recall': recall_score(y_test, y_pred, zero_division=0),
        'f1_score': f1_score(y_test, y_pred, zero_division=0)
    }

    # Handle single class case for roc_auc_score
    if len(np.unique(y_test)) == 1 or len(clf.classes_) == 1:
        print("Warning: Cannot calculate ROC AUC score. Either y_test or the model was trained on a single class.")
        metrics['roc_auc'] = None
    else:
        probs = clf.predict_proba(X_test)[:, 1]
        metrics['roc_auc'] = roc_auc_score(y_test, probs)

    # Save evaluation metrics
    with open(os.path.join(OUT_DIR, "evaluation_metrics.json"), "w") as fh:
        json.dump(metrics, fh)

    # Generate and save Confusion Matrix plot
    cm_display = ConfusionMatrixDisplay.from_predictions(y_test, y_pred, cmap=plt.cm.Blues)
    plt.figure(figsize=(8, 6))
    cm_display.plot()
    plt.title("Confusion Matrix")
    plt.savefig(os.path.join(OUT_DIR, "confusion_matrix.png"))
    plt.close()

    # Generate and save ROC Curve plot
    if metrics['roc_auc'] is not None:
        roc_display = RocCurveDisplay.from_predictions(y_test, probs)
        plt.figure(figsize=(8, 6))
        roc_display.plot()
        plt.title("ROC Curve")
        plt.savefig(os.path.join(OUT_DIR, "roc_curve.png"))
        plt.close()
    else:
        # Create a placeholder image if ROC AUC cannot be calculated
        plt.figure(figsize=(8, 6))
        plt.text(0.5, 0.5, "ROC Curve Not Applicable (Single Class)",
                 horizontalalignment='center', verticalalignment='center',
                 fontsize=12, color='red')
        plt.title("ROC Curve")
        plt.savefig(os.path.join(OUT_DIR, "roc_curve.png"))
        plt.close()

    print("Evaluation artifacts saved to", OUT_DIR)

if __name__ == "__main__":
    main()
