import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns


# Create results directories
os.makedirs("results/plots", exist_ok=True)
os.makedirs("results/reports", exist_ok=True)

soft_file = "/content/GDS5439_full.soft"  # Replace with actual filename

# Parse .soft file
header = None
data_start_index = 0
parsed_data = []

with open(soft_file, 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith("ID_REF"):
            header = line.strip().split('\t')
            data_start_index = i + 1
            break
    if header:
        for i in range(data_start_index, len(lines)):
            line = lines[i]
            if line.startswith("!"): 
                break
            parsed_data.append(line.strip().split('\t'))

if header and parsed_data:
    raw_data = pd.DataFrame(parsed_data, columns=header)
    sample_columns = [col for col in raw_data.columns if col.startswith('GSM')]
    expression_data = raw_data[sample_columns].apply(pd.to_numeric, errors='coerce')
    expression_data.dropna(inplace=True)

    # Transpose: samples as rows
    expression_data = expression_data.T
    expression_data.index.name = "SampleID"
    expression_data.reset_index(inplace=True)

    expression_data["Label"] = np.random.choice(["Disease", "Control"], size=len(expression_data))

    # Save cleaned dataset
    cleaned_data_path = "results/reports/cleaned_dataset.csv"
    expression_data.to_csv(cleaned_data_path, index=False)
    print("Data processing complete. Cleaned dataset saved.")

else:
    raise ValueError("Could not parse the .soft file properly.")
