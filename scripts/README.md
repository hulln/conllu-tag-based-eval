# scripts/

Pipeline and analysis entry points.

- `run_pipeline.py`: end-to-end orchestration (prediction + eval + reporting).
- `predict_classla.py`: CLASSLA prediction export (aligned/base).
- `predict_trankit.py`: Trankit prediction export (aligned/base).
- `analyze_errors.py`: model-vs-gold HEAD/DEPREL error summaries.
- `compare_models.py`: token-level CLASSLA-vs-Trankit comparison.
- `qa_validate_run.py`: strict run-level validation checks.
- `export_raw_sentences.py`: helper for exporting sentence text input.
- `compare_conllu_files.py`: utility for CoNLL-U comparison/debugging.