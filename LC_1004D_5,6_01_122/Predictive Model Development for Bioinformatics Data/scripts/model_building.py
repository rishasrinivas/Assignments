import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

cleaned_data = pd.read_csv(cleaned_data_path)
X = cleaned_data.drop(["SampleID", "Label"], axis=1)
y = cleaned_data["Label"].map({"Disease": 1, "Control": 0})

# Drop rows with missing values
combined_data = pd.concat([X, y], axis=1).dropna()
X = combined_data.drop("Label", axis=1)
y = combined_data["Label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
