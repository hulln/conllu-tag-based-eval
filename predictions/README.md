# predictions/

Generated model outputs in CoNLL-U format.

- `runs/`: active canonical outputs used for main reporting.
- Current canonical aligned files:
  - `20260409-2248_sl-ssj-ud-test_full_classla_aligned_predicted.conllu`
  - `20260409-2248_sl-ssj-ud-test_full_trankit_aligned_predicted.conllu`
- Base outputs are supplementary and stored under `runs/supplementary/base/`.
- `samples/`: prediction outputs from sample runs.
- `../archive/runs/`: historical and verification run snapshots moved out of active reporting paths.

These files are produced by `scripts/run_pipeline.py`.