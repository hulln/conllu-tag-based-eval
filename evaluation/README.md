# evaluation/

This folder contains the scoring script used by the pipeline.

- `conll18_ud_eval_tag-based.py` is the evaluator script provided for this project.
- It is treated as a reference evaluator (not project business logic).
- Main pipeline calls it to produce eval tables in `results/output/`.
