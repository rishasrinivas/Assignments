# src/serve/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib
import pandas as pd
import os

MODEL_PATH = os.path.join("..","..","models","best_model.joblib")  # adjust if running from root
app = FastAPI(title="miRNA Interaction Predictor")

class Instance(BaseModel):
    data: List[dict]  # list of feature dicts

@app.on_event("startup")
def load_model():
    global model
    model = joblib.load("models/best_model.joblib")  # in container/workdir models/ should be present

@app.post("/predict")
def predict(inst: Instance):
    X = pd.DataFrame(inst.data)
    preds = model.predict(X).tolist()
    if len(model.classes_) == 1:
        if model.classes_[0] == 1:
            probs = model.predict_proba(X)[:, 0].tolist()
        else: # model.classes_[0] == 0
            probs = [0.0] * len(X) # Probability of class 1 is 0
    else:
        probs = model.predict_proba(X)[:, 1].tolist()
    return {"predictions": preds, "probabilities": probs}
