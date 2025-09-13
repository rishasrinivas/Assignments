
# Bioinformatics Machine Learning Pipeline for Variant Classification

This project implements an end-to-end machine learning pipeline to predict the clinical significance of genetic variants from the ClinVar dataset. The pipeline is built using Python for data processing and model training, and orchestrated with Nextflow to ensure reproducibility and scalability.

## Project Structure

```
.
├── LICENSE
├── README.md
├── nextflow.config
├── main.nf
├── .gitignore
│
├── bin/
│   ├── preprocess_data.py
│   ├── train_model.py
│   └── evaluate_model.py
│
├── data/
│   ├── raw/                         
│   │   └── clinvar_conflicting.csv
│   └── interim/
│       ├── features.csv
│       ├── X_test.csv
│       └── y_test.csv
│
├── results/
│   ├── reports/
│   │   └── evaluation_report.txt
│   ├── visualizations/
│   │   ├── confusion_matrix.png
│   │   └── roc_curve.png
│   └── models/
│       └── random_forest_model.joblib
│
├── docs/
│   └── pipeline_details.md
│
└── workflows/
    └── subworkflow_name.nf
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-link>
    cd <your-repo-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required Python libraries:**
    ```bash
    pip install pandas scikit-learn matplotlib seaborn
    ```

4.  **Install Nextflow:**
    Follow the instructions at [nextflow.io](https://www.nextflow.io/docs/latest/getstarted.html) to install Nextflow.

## How to Run the Pipeline

With the environment set up and Nextflow installed, you can run the entire pipeline with a single command:

```bash
nextflow run main.nf
```

The pipeline will execute the following steps:
1.  **Data Preprocessing:** Cleans the raw data and engineers features for the model.
2.  **Model Training:** Trains a Random Forest classifier on the processed data.
3.  **Model Evaluation:** Evaluates the model's performance and generates a report and visualizations.

## Pipeline Outputs

The results of the pipeline are saved in the `results/` directory:

*   **Trained Model:** `results/models/random_forest_model.joblib`
*   **Evaluation Report:** `results/reports/evaluation_report.txt`
*   **Visualizations:**
    *   `results/visualizations/confusion_matrix.png`
    *   `results/visualizations/roc_curve.png`
