# scripts/

Pipeline and analysis entry points.

- `run_pipeline.py`: end-to-end orchestration. Aligned mode is primary by default; base mode is optional. Runs QA validation at the end unless `--skip-qa` is used.
- `predict_classla.py`: CLASSLA prediction export. In aligned mode it consumes gold CoNLL-U segmentation/tokenization and preserves gold sentence metadata.
- `predict_trankit.py`: Trankit prediction export with the same aligned-mode contract as CLASSLA.
- `qa_validate_run.py`: strict mode-aware run validation for aligned-only or aligned+base runs.
- `analyze_errors.py`: model-vs-gold HEAD/DEPREL error summaries.
- `compare_models.py`: token-level CLASSLA-vs-Trankit comparison.
- `export_raw_sentences.py`: helper for deriving raw sentence input from gold CoNLL-U when base mode is needed.
- `compare_conllu_files.py`: utility for CoNLL-U comparison/debugging.
