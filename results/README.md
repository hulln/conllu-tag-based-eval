# results/

Evaluation outputs and analysis reports.

- `output/<run-id>/main/`: primary aligned outputs, including eval summaries, model comparison, and `qa_validation.md`
- `output/<run-id>/diagnostics/`: primary aligned verbose tagged metrics and error analyses
- `../archive/local/`: local-only legacy output layouts and historical comparisons (gitignored)

Supplementary base-mode outputs are local-only (gitignored).

Current active canonical run:

- `output/20260414-1323_sl-ssj-ud-test_full/`

Strict rerun verification:

- Run `scripts/verify_canonical_run.py` after a rerun.
- Source of truth is `references/canonical_run_manifest.json`.

First file to open for a run:

- `output/<run-id>/main/qa_validation.md`
