# results/

Evaluation outputs and analysis reports.

- `runs/<run-id>/main/`: primary aligned high-level outputs (eval summaries, model comparisons, QA report).
- `runs/<run-id>/diagnostics/`: primary aligned verbose tagged metrics and error analyses.
- `runs/<run-id>/supplementary/base/`: optional base-mode outputs, separated from main reporting.
- `../archive/runs/`: historical and verification run snapshots moved out of active reporting paths.

Current canonical reporting run:

- `runs/20260409-2248_sl-ssj-ud-test_full/`

First file to open for a run:

- `runs/<run-id>/main/qa_validation.md`