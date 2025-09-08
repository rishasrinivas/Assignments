import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler

def build_and_evaluate_logistic_regression(filepath):
    
    try:
        # Load the dataset
        df = pd.read_csv(filepath)

        # The target variable is 'DEATH_EVENT'
        X = df.drop('DEATH_EVENT', axis=1)
        y = df['DEATH_EVENT']

        # Split the data into training and testing sets (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        print("Data Split:")
        print(f"Training set size: {X_train.shape[0]} samples")
        print(f"Testing set size: {X_test.shape[0]} samples")

        # Scale the data to potentially improve convergence
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)


        # Initialize and train the Logistic Regression model
        # Increasing max_iter to ensure convergence and using a different solver
        model = LogisticRegression(max_iter=2000, solver='liblinear') # Increased max_iter and changed solver
        print("\nTraining Logistic Regression model...")
        model.fit(X_train_scaled, y_train)

        # Make predictions on the test set
        y_pred = model.predict(X_test_scaled)

        # Evaluate the model
        print("\n--- Model Evaluation ---")

        # Calculate and print Accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.4f}")

        # Print Classification Report
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Survived', 'Died']))

        # Print Confusion Matrix
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

    except FileNotFoundError:
        print(f"Error: The file at '{filepath}' was not found. Please ensure the path is correct.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    build_and_evaluate_logistic_regression("heart_failure_clinical_records_dataset.csv")
