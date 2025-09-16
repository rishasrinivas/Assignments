import json
import os

def generate_report(results_dir="work/results", models_dir="work/models"):
    report_content = "# Machine Learning Pipeline Report\n\n"
    report_content += "## 1. Pipeline Overview\n"
    report_content += "This report summarizes the results of the machine learning pipeline for bioinformatics. The pipeline consists of three main stages:\n"
    report_content += "1.  **Data Preparation (PREPARE):** Raw data is processed, features are selected, and data is split into training and testing sets.\n"
    report_content += "2.  **Model Training (TRAIN):** A RandomForestClassifier model is trained and tuned using GridSearchCV.\n"
    report_content += "3.  **Model Evaluation (EVAL):** The trained model is evaluated on a test set, and performance metrics are calculated.\n\n"

    # Load training metrics
    train_metrics_path = os.path.join(models_dir, "metrics.json")
    if os.path.exists(train_metrics_path):
        with open(train_metrics_path, "r") as f:
            train_metrics = json.load(f)
        report_content += "## 2. Training Metrics\n"
        report_content += "Metrics from the training phase (RandomForestClassifier with GridSearchCV):\n"
        for key, value in train_metrics.items():
            report_content += f"- **{key.replace('_', ' ').title()}:** {value:.4f}\n" if isinstance(value, (int, float)) else f"- **{key.replace('_', ' ').title()}:** {value}\n"
        report_content += "\n"
    else:
        report_content += "## 2. Training Metrics\n"
        report_content += "Training metrics file not found.\n\n"

    # Load evaluation metrics
    eval_metrics_path = os.path.join(results_dir, "evaluation_metrics.json")
    if os.path.exists(eval_metrics_path):
        with open(eval_metrics_path, "r") as f:
            eval_metrics = json.load(f)
        report_content += "## 3. Evaluation Metrics\n"
        report_content += "Metrics from the evaluation phase (on the test set):\n"
        for key, value in eval_metrics.items():
            report_content += f"- **{key.replace('_', ' ').title()}:** {value:.4f}\n" if isinstance(value, (int, float)) else f"- **{key.replace('_', ' ').title()}:** {value}\n"
        report_content += "\n"
    else:
        report_content += "## 3. Evaluation Metrics\n"
        report_content += "Evaluation metrics file not found.\n\n"

    # Add plots
    report_content += "## 4. Visualizations\n"
    report_content += "### Confusion Matrix\n"
    report_content += f"![Confusion Matrix]({os.path.join(results_dir, 'confusion_matrix.png')})\n\n"
    report_content += "### ROC Curve\n"
    report_content += f"![ROC Curve]({os.path.join(results_dir, 'roc_curve.png')})\n\n"

    # Save the report
    report_path = os.path.join(results_dir, "final_report.md")
    with open(report_path, "w") as f:
        f.write(report_content)
    print(f"Final report generated at: {report_path}")

if __name__ == "__main__":
    generate_report()
