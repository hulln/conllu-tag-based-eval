# Slovenian UD Evaluation (CLASSLA vs Trankit)

Reproducible evaluation of CLASSLA and Trankit on Slovenian UD SSJ.

## What Is Canonical

- Primary method: aligned mode only (gold sentence/token boundaries are fixed).
- Public canonical run: 20260414-1323_sl-ssj-ud-test_full
- Old and non-canonical outputs: local-only under archive/local/ (gitignored).

## Quick Setup

1. Create environment and install dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Put the local gold file at:

- data/gold/sl_ssj-ud-test.conllu

Gold file hash used for canonical run:

- c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0

## Rerun (Aligned Canonical Path)

Run the pipeline in aligned mode:

```bash
python scripts/run_pipeline.py --modes aligned --run-stamp <run-stamp> --download-classla-models
```

Main outputs:

- predictions/runs/<run-stamp>_sl-ssj-ud-test_full_classla_aligned_predicted.conllu
- predictions/runs/<run-stamp>_sl-ssj-ud-test_full_trankit_aligned_predicted.conllu
- results/runs/<run-stamp>_sl-ssj-ud-test_full/main/

## Verify Rerun

Run both checks:

```bash
python scripts/qa_validate_run.py --run-stamp <run-stamp> --modes aligned
python scripts/verify_canonical_run.py --run-stamp <run-stamp>
```

- qa_validate_run.py checks run integrity and aligned structure.
- verify_canonical_run.py checks canonical file hashes and key metric values from references/canonical_run_manifest.json.

## Repository Guide

- data/: local inputs and dataset helpers
- scripts/: pipeline, prediction, QA, and verification scripts
- predictions/: canonical public prediction artifacts
- results/: canonical public evaluation artifacts
- archive/: local-only historical artifacts
- references/: paper link and canonical verification manifest

## Optional Non-Canonical Mode

Base mode remains available for local supplementary analysis:

```bash
python scripts/run_pipeline.py --modes both --run-stamp <run-stamp>
```

Supplementary outputs are intentionally local-only (gitignored).

## Reference

- DOI: https://doi.org/10.4312/slo2.0.2023.1.218-246
