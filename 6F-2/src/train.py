# src/train.py
import pandas as pd
import os
import joblib
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score
from xgboost import XGBClassifier

OUT_DIR = "models"
DATA_DIR = "data/processed"
RANDOM_STATE = 42

def load_data():
    X_train = pd.read_csv(os.path.join(DATA_DIR, "X_train.csv"))
    X_test = pd.read_csv(os.path.join(DATA_DIR, "X_test.csv"))
    y_train = pd.read_csv(os.path.join(DATA_DIR, "y_train.csv")).squeeze()
    y_test = pd.read_csv(os.path.join(DATA_DIR, "y_test.csv")).squeeze()
    return X_train, X_test, y_train, y_test

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    X_train, X_test, y_train, y_test = load_data()

    # Baseline RandomForest with grid search
    param_grid = {
        "n_estimators": [100, 200],
        "max_depth": [None, 6, 12],
        "min_samples_split": [2, 5]
    }
    rf = RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1)

    # Determine scoring based on the number of unique classes in y_train
    if len(y_train.unique()) > 1:
        scorer_metric = 'roc_auc'
    else:
        scorer_metric = 'accuracy'
        print("Warning: y_train contains only one class. Using 'accuracy' for GridSearchCV scoring instead of 'roc_auc'.")

    grid = GridSearchCV(rf, param_grid, cv=5, scoring=scorer_metric, n_jobs=-1, verbose=1)
    grid.fit(X_train, y_train)

    best = grid.best_estimator_
    print("Best params:", grid.best_params_)
    preds = best.predict(X_test)

    # Handle predict_proba output for single-class cases
    if best.predict_proba(X_test).shape[1] > 1:
        probs = best.predict_proba(X_test)[:, 1]
    else:
        probs = best.predict_proba(X_test).flatten()

    # Calculate AUC only if y_test has at least two unique classes
    if len(y_test.unique()) > 1:
        auc = roc_auc_score(y_test, probs)
    else:
        auc = None # Or some other appropriate placeholder

    report = classification_report(y_test, preds, output_dict=True)
    report['roc_auc'] = auc

    # Save model and metrics
    joblib.dump(best, os.path.join(OUT_DIR, "best_model.joblib"))
    with open(os.path.join(OUT_DIR, "metrics.json"), "w") as fh:
        json.dump(report, fh)

    # Optional: train XGBoost with default params to compare
    try:
        xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=RANDOM_STATE)
        xgb.fit(X_train, y_train)

        if xgb.predict_proba(X_test).shape[1] > 1:
            xgb_probs = xgb.predict_proba(X_test)[:, 1]
        else:
            xgb_probs = xgb.predict_proba(X_test).flatten()

        if len(y_test.unique()) > 1:
            xgb_auc = roc_auc_score(y_test, xgb_probs)
            print("XGBoost ROC-AUC:", xgb_auc)
        else:
            print("XGBoost ROC-AUC: Not applicable (single class in y_test)")

    except Exception as e:
        print("XGBoost not available or failed to run:", e)

    print("Training complete. Model saved to", OUT_DIR)

if __name__ == "__main__":
    main()
