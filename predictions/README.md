# predictions/

Generated model outputs in CoNLL-U format.

- `runs/`: canonical run outputs with timestamped filenames.
	- aligned outputs are primary and stored directly under `runs/`
	- base outputs are supplementary and stored under `runs/supplementary/base/`
- `samples/`: prediction outputs from sample runs.
- `archive/`: historical or pre-normalization prediction backups.

These files are produced by `scripts/run_pipeline.py`.