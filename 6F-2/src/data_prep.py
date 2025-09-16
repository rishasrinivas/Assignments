# src/data_prep.py
import pandas as pd
import numpy as np
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

DATA_IN = "Gastric.csv"
OUT_DIR = "data/processed"
RANDOM_STATE = 42

def create_label(df, col='all.sum', thresh=1):
    # label = 1 if at least 'thresh' predictions agree
    return (df[col].fillna(0) >= thresh).astype(int)

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    df = pd.read_csv(DATA_IN)
    # drop unnamed index if present
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    # create label
    df['interaction'] = create_label(df, col='all.sum', thresh=1)

    # choose features: use prediction method columns (binary/numeric)
    predict_cols = ['diana_microt','elmmo','microcosm','miranda','mirdb','pictar','pita','targetscan','predicted.sum','all.sum']
    # keep only those that exist in df
    features = [c for c in predict_cols if c in df.columns]
    print("Using features:", features)

    X = df[features].copy()
    y = df['interaction'].copy()

    # simple imputation (median)
    imputer = SimpleImputer(strategy='median')
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=features)

    # save imputer stats
    imputer_stats = {f: float(np.nanmedian(X[f])) for f in features}
    with open(os.path.join(OUT_DIR, "imputer_stats.json"), "w") as fh:
        json.dump(imputer_stats, fh)

    # train/test split stratified
    X_train, X_test, y_train, y_test = train_test_split(
        X_imputed, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    X_train.to_csv(os.path.join(OUT_DIR, "X_train.csv"), index=False)
    X_test.to_csv(os.path.join(OUT_DIR, "X_test.csv"), index=False)
    y_train.to_csv(os.path.join(OUT_DIR, "y_train.csv"), index=False)
    y_test.to_csv(os.path.join(OUT_DIR, "y_test.csv"), index=False)

    # Save features list
    with open(os.path.join(OUT_DIR, "features.json"), "w") as fh:
        json.dump(features, fh)

    print("Saved processed data to", OUT_DIR)

if __name__ == "__main__":
    main()
