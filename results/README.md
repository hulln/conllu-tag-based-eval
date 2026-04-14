# results/

Evaluation outputs and analysis reports.

- `runs/<run-id>/main/`: primary aligned high-level outputs (eval summaries, model comparisons, QA report).
- `runs/<run-id>/diagnostics/`: primary aligned verbose tagged metrics and error analyses.
- `runs/<run-id>/supplementary/base/`: optional base-mode outputs, separated from main reporting.
- `archive/`: legacy output layouts from earlier iterations.

First file to open for a run:

- `runs/<run-id>/main/qa_validation.md`