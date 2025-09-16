import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Feature importance
feature_importance = pd.DataFrame({
    "feature": X_train.columns,
    "importance": model.coef_[0]
})
feature_importance["abs_importance"] = abs(feature_importance["importance"])
top_features = feature_importance.sort_values(by="abs_importance", ascending=False).head(20)

# Bar plot of top features
plt.figure(figsize=(10, 6))
sns.barplot(x="importance", y="feature", data=top_features)
plt.title("Top 20 Feature Importance (Logistic Regression)")
plt.savefig("results/plots/feature_importance.png")
plt.close()

# Save top features list
with open("results/reports/top_features.txt", "w") as f:
    for _, row in top_features.iterrows():
        f.write(f"{row['feature']}: {row['importance']:.4f}\n")

# Distribution of labels
plt.figure(figsize=(6, 4))
sns.countplot(x="Label", data=cleaned_data)
plt.title("Distribution of Labels")
plt.savefig("results/plots/label_distribution.png")
plt.close()

# Correlation heatmap
features_corr = cleaned_data[top_features["feature"].tolist() + ["Label"]].copy()
features_corr["Label"] = features_corr["Label"].map({"Disease": 1, "Control": 0})
plt.figure(figsize=(12, 10))
sns.heatmap(features_corr.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation of Top Features with Label")
plt.savefig("results/plots/top_features_correlation_heatmap.png")
plt.close()

print("Plots and reports generated successfully.")

