import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Train a random forest model.')
parser.add_argument('--input', type=str, required=True, help='Input features CSV file path')
parser.add_argument('--model', type=str, required=True, help='Output model file path')
parser.add_argument('--x_test', type=str, required=True, help='Output X_test CSV file path')
parser.add_argument('--y_test', type=str, required=True, help='Output y_test CSV file path')
args = parser.parse_args()

# Load the processed data
df = pd.read_csv(args.input)

# Separate features (X) and target (y)
X = df.drop('CLASS', axis=1)
y = df['CLASS']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Initialize and train the Random Forest model
# TODO: Implement genetic algorithm for hyperparameter tuning
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Save the trained model and the test set for evaluation
joblib.dump(model, args.model)
X_test.to_csv(args.x_test, index=False)
y_test.to_csv(args.y_test, index=False)

print(f"Model training complete. Model saved to {args.model}")
print(f"Test data saved to {args.x_test} and {args.y_test}")