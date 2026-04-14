# predictions/

Generated model outputs in CoNLL-U format.

- `runs/`: canonical run outputs with timestamped filenames.
- aligned outputs are primary and stored directly under `runs/`
- base outputs are optional supplementary artifacts under `runs/supplementary/base/`
- `samples/`: local-only prediction outputs from small smoke-test runs
- `../archive/local/`: local-only historical backups (gitignored)

Current active canonical aligned files:

- `runs/20260414-1323_sl-ssj-ud-test_full_classla_aligned_predicted.conllu`
- `runs/20260414-1323_sl-ssj-ud-test_full_trankit_aligned_predicted.conllu`

Aligned predictions preserve gold `sent_id` values and sentence-level metadata where available.

These files are produced by `scripts/run_pipeline.py`, `scripts/predict_classla.py`, and `scripts/predict_trankit.py`.
