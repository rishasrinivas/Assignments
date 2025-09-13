#!/usr/bin/env nextflow
nextflow.enable.dsl=2

// Define the processes

process preprocess_data {
    output:
        path("features.csv")

    script:
    """
    ${params.python_interpreter} ${projectDir}/bin/preprocess_data.py --input ${params.input_csv} --output features.csv
    """
}

process train_model {
    input:
        path features

    output:
        path("random_forest_model.joblib"), emit: model
        path("X_test.csv"), emit: x_test
        path("y_test.csv"), emit: y_test

    script:
    """
    ${params.python_interpreter} ${projectDir}/bin/train_model.py --input ${features} --model random_forest_model.joblib --x_test X_test.csv --y_test y_test.csv
    """
}

process evaluate_model {
    input:
        path model
        path x_test
        path y_test

    output:
        path("evaluation_report.txt")
        path("confusion_matrix.png")
        path("roc_curve.png")

    script:
    """
    ${params.python_interpreter} ${projectDir}/bin/evaluate_model.py --model ${model} --x_test ${x_test} --y_test ${y_test} --report evaluation_report.txt --cm confusion_matrix.png --roc roc_curve.png
    """
}

// Define the workflow
workflow {
    // Step 1: Preprocess the data
    features_ch = preprocess_data()

    // Step 2: Train the model
    model_results_ch = train_model(features_ch)

    // Step 3: Evaluate the model
    evaluate_model(model_results_ch.model, model_results_ch.x_test, model_results_ch.y_test)
}