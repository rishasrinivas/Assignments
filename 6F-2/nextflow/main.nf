#!/usr/bin/env nextflow

params.input = "data/Gastric.csv"
params.outdir = "work"

process PREPARE {
    publishDir "${params.outdir}/data", mode: 'copy'
    input:
    path input_csv
    path 'src'

    output:
    path "data", emit: data_ch

    script:
    """
    mkdir -p processed
    python3 src/data_prep.py
    """
}

process TRAIN {
    publishDir "${params.outdir}/models", mode: 'copy'
    input:
    path data_dir
    path 'src'

    output:
    path "models/best_model.joblib", emit: best_model_ch
    path "models/metrics.json", emit: metrics_ch

    script:
    """
    python3 src/train.py
    """
}

process EVAL {
    publishDir "${params.outdir}/results", mode: 'copy'
    input:
    path best_model
    path metrics
    path data_dir
    path 'src'

    output:
    path "results/evaluation_metrics.json", emit: eval_metrics_ch
    path "results/confusion_matrix.png", emit: confusion_matrix_ch
    path "results/roc_curve.png", emit: roc_curve_ch

    script:
    """
    python3 src/evaluate.py
    """
}

workflow {
    data_ch = PREPARE(file(params.input), file("src"))
    models_ch = TRAIN(data_ch, file("src"))
    EVAL(models_ch.best_model_ch, models_ch.metrics_ch, data_ch, file("src"))
}
