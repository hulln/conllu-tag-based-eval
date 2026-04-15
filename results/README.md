# results/

Evaluation outputs and analysis reports.

- `output/<run-id>/main/`: primary aligned outputs, including eval summaries, model comparison, and `qa_validation.md`
- `output/<run-id>/diagnostics/`: primary aligned verbose tagged metrics and error analyses
- [archive/local](../archive/local/): local-only legacy output layouts and historical comparisons (gitignored)

Supplementary base-mode outputs are local-only (gitignored).

Current active canonical run:

- [output/20260414-1819_sl-ssj-ud-test_full](output/20260414-1819_sl-ssj-ud-test_full/)

Strict rerun verification:

- Run [scripts/verify_canonical_run.py](../scripts/verify_canonical_run.py) after a rerun.
- Source of truth is [references/canonical_run_manifest.json](../references/canonical_run_manifest.json).

First file to open for a run:

- [output/20260414-1819_sl-ssj-ud-test_full/main/qa_validation.md](output/20260414-1819_sl-ssj-ud-test_full/main/qa_validation.md)

Public interactive table for the active canonical aligned run:

- [tables/comparison_table.html](../tables/comparison_table.html)
