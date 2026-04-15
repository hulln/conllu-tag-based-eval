# Slovenian UD Evaluation (CLASSLA vs Trankit)

Reproducible evaluation of CLASSLA and Trankit on Slovenian UD SSJ.

## What Is Canonical

- Primary method: aligned mode only (gold sentence/token boundaries are fixed).
- Public canonical run: 20260414-1819_sl-ssj-ud-test_full
- Old and non-canonical outputs: local-only under [archive/local](archive/local/) (gitignored).

## Quick Setup

1. Create environment and install dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Put the local gold file at:

- [data/gold/sl_ssj-ud-test.conllu](data/gold/sl_ssj-ud-test.conllu)
- Source: https://github.com/UniversalDependencies/UD_Slovenian-SSJ

## Rerun (Aligned Canonical Path)

Run the pipeline in aligned mode:

```bash
python scripts/run_pipeline.py --modes aligned --run-stamp <run-stamp> --download-classla-models
```

Main outputs:

- [predictions/output](predictions/output/) for prediction artifacts
- [results/output](results/output/) for run results
- [results/output/20260414-1819_sl-ssj-ud-test_full/main](results/output/20260414-1819_sl-ssj-ud-test_full/main) for canonical aligned summaries
- [results/output/20260414-1819_sl-ssj-ud-test_full/diagnostics](results/output/20260414-1819_sl-ssj-ud-test_full/diagnostics) for canonical diagnostics
- [results/output/20260414-1819_sl-ssj-ud-test_full/main/classla-vs-trankit_aligned_content-comparison.md](results/output/20260414-1819_sl-ssj-ud-test_full/main/classla-vs-trankit_aligned_content-comparison.md) (table-style content comparison)

If the public interactive table should be refreshed from that run, use:

```bash
python scripts/run_pipeline.py --modes aligned --run-stamp <run-stamp> --publish-interactive-table
```

This updates:

- [tables/comparison_table.html](tables/comparison_table.html)
- [tables/comparison_table_data.js](tables/comparison_table_data.js)

## Verify Rerun

Run both checks:

```bash
python scripts/qa_validate_run.py --run-stamp <run-stamp> --modes aligned
python scripts/verify_canonical_run.py --run-stamp <run-stamp>
```

- qa_validate_run.py checks run integrity and aligned structure.
- [scripts/qa_validate_run.py](scripts/qa_validate_run.py) checks run integrity and aligned structure.
- [scripts/verify_canonical_run.py](scripts/verify_canonical_run.py) checks canonical file hashes and key metric values from [references/canonical_run_manifest.json](references/canonical_run_manifest.json).

## Repository Guide

- [data](data): local inputs and dataset helpers
- [scripts](scripts): pipeline, prediction, QA, and verification scripts
- [predictions](predictions): canonical public prediction artifacts
- [results](results): canonical public evaluation artifacts
- [tables](tables): canonical public interactive comparison table bundle
- [archive](archive): local-only historical artifacts (not public)
- [references](references): paper link and canonical verification manifest

## Optional Non-Canonical Mode

Base mode remains available for local supplementary analysis:

```bash
python scripts/run_pipeline.py --modes both --run-stamp <run-stamp>
```

Supplementary outputs are intentionally local-only (gitignored).

## Reference

- DOI: https://doi.org/10.4312/slo2.0.2023.1.218-246
