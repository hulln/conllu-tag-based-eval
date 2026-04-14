# predictions/

Generated model outputs in CoNLL-U format.

- `output/`: canonical public aligned prediction outputs
- `../archive/local/`: local-only historical outputs (gitignored)

Supplementary base-mode outputs are local-only (gitignored).

Current active canonical aligned files:

- `output/20260414-1819_sl-ssj-ud-test_full_classla_aligned_predicted.conllu`
- `output/20260414-1819_sl-ssj-ud-test_full_trankit_aligned_predicted.conllu`

Aligned predictions preserve gold `sent_id` values and sentence-level metadata where available.

Use `scripts/verify_canonical_run.py` with `references/canonical_run_manifest.json` to check these aligned prediction files against canonical hashes.

These files are produced by `scripts/run_pipeline.py`, `scripts/predict_classla.py`, and `scripts/predict_trankit.py`.
