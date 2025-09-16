import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Model Accuracy: {accuracy:.4f}")
print("Classification Report:\n", report)

# Save evaluation report
report_path = "results/reports/classification_report.txt"
with open(report_path, "w") as f:
    f.write(f"Model Accuracy: {accuracy:.4f}\n\n")
    f.write("Classification Report:\n")
    f.write(report)

# Save validation data
validation_data = pd.DataFrame({"Actual_Label": y_test, "Predicted_Label": y_pred})
validation_data.to_csv("results/reports/validation_data.csv", index=False)
