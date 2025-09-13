
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Preprocess clinvar data.')
parser.add_argument('--input', type=str, required=True, help='Input CSV file path')
parser.add_argument('--output', type=str, required=True, help='Output CSV file path')
args = parser.parse_args()

# Load the raw data
df = pd.read_csv(args.input, low_memory=False)

# The 'CLASS' column is already our numerical target variable (0 for Benign, 1 for Pathogenic)
# We will select features and use 'CLASS' as the target

# Select feature columns
feature_cols = [
    'AF_ESP', 'AF_EXAC', 'AF_TGP', 'Consequence', 'IMPACT',
    'SIFT', 'PolyPhen', 'CADD_PHRED', 'BLOSUM62', 'SYMBOL'
]

# Ensure all selected feature columns exist in the dataframe
existing_feature_cols = [col for col in feature_cols if col in df.columns]

df_features = df[existing_feature_cols + ['CLASS']].copy()

# Handle missing values in numerical columns
numerical_cols = ['AF_ESP', 'AF_EXAC', 'AF_TGP', 'CADD_PHRED', 'BLOSUM62']
existing_numerical_cols = [col for col in numerical_cols if col in df_features.columns]

for col in existing_numerical_cols:
    df_features[col] = pd.to_numeric(df_features[col], errors='coerce').fillna(0)

# Handle categorical features
# One-hot encode 'Consequence' and 'IMPACT'
categorical_features = ['Consequence', 'IMPACT']
existing_categorical_features = [col for col in categorical_features if col in df_features.columns]
df_features = pd.get_dummies(df_features, columns=existing_categorical_features, dummy_na=True)

# Label encode 'SYMBOL', 'SIFT', and 'PolyPhen'
label_encode_cols = ['SYMBOL', 'SIFT', 'PolyPhen']
existing_label_encode_cols = [col for col in label_encode_cols if col in df_features.columns]

for col in existing_label_encode_cols:
    le = LabelEncoder()
    df_features[col] = le.fit_transform(df_features[col].astype(str))

# Drop rows where CLASS is not 0 or 1
df_features = df_features[df_features['CLASS'].isin([0, 1])]

# Save the processed data
df_features.to_csv(args.output, index=False)

print(f"Preprocessing complete. Processed data saved to {args.output}")
