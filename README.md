# Slovenian UD Evaluation (SPOT-Trankit vs CLASSLA-Stanza)

Reproducible evaluation of SPOT-Trankit and CLASSLA-Stanza on Slovenian UD test sets (SSJ and SST).

## Interactive Tables

**v4 (combined, recommended):** [comparison_table_v4.html](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v4.html) — a single page with a two-layer selector: pick a **model** (SPOT-Trankit / CLASSLA-Stanza), then a **corpus** (SSJ-UD / SST-UD). Every section then shows that one model's accuracy and errors. The accuracy tables default to a single-model view, with a "Compare with …" toggle that reveals the other model's column and the difference on demand. Deep-linkable via URL hash, e.g. `#classla/sst`.

Per-corpus single-model tables (SPOT-Trankit only) remain available:

| Dataset | Table | Canonical run |
|---------|-------|---------------|
| SSJ-UD (written) | [comparison_table_v2_ssj.html](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v2_ssj.html) | `20260414-1819_sl-ssj-ud-test_full` |
| SST-UD (spoken) | [comparison_table_v3_sst.html](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v3_sst.html) | `20260420-1105_sl-sst-ud-test_full` |

A legacy Slovenian-language v1 table is also available at [comparison_table_v1_ssj.html](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v1_ssj.html).

## What Is Canonical

- Primary method: aligned mode only (gold sentence/token boundaries are fixed).
- SSJ canonical run: `20260414-1819_sl-ssj-ud-test_full`
- SST canonical run: `20260420-1105_sl-sst-ud-test_full`
- Old and non-canonical outputs: local-only under [archive/local](archive/local/) (gitignored).

### Additional evaluation: Trankit 1.3 (non-standard Slovenian)

A supplementary run evaluates the newer Trankit model **CLARIN `11356/2201`**
(*"Trankit model for linguistic processing of written and spoken Slovenian 1.3"*,
issued 2026-05-25), which adds non-standard / colloquial spoken transcriptions to
the SST training data and replaces the canonical 1.2 model (`11356/1997`).

- Run stamp: `20260604-0859-tk13` — SSJ ([results](results/output/20260604-0859-tk13_sl-ssj-ud-test_full/)) and SST ([results](results/output/20260604-0859-tk13_sl-sst-ud-test_full/)).
- CLASSLA is unchanged (default for SSJ, spoken for SST) and its metrics match the canonical runs exactly; only the Trankit rows differ.
- On SST, Trankit 1.3 shows small consistent gains over 1.2 (e.g. LAS 86.70→86.86, CLAS 83.72→83.91); SSJ is essentially unchanged.
- This run does **not** replace the canonical 1.2 results: the [manifest](references/canonical_run_manifest.json) and interactive tables remain anchored to the April runs.
- Reproduce with the Docker setup in [docker/README.md](docker/README.md) and [scripts/run_trankit13_eval.sh](scripts/run_trankit13_eval.sh).

## Quick Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Gold files (add locally):

- [data/gold/sl_ssj-ud-test.conllu](data/gold/sl_ssj-ud-test.conllu) — source: https://github.com/UniversalDependencies/UD_Slovenian-SSJ
- [data/gold/sl_sst-ud-test.conllu](data/gold/sl_sst-ud-test.conllu) — source: https://github.com/UniversalDependencies/UD_Slovenian-SST

## Rerun

**SSJ (written):**

```bash
python scripts/run_pipeline.py --modes aligned --gold data/gold/sl_ssj-ud-test.conllu --run-stamp <run-stamp>
```

**SST (spoken):**

```bash
python scripts/run_pipeline.py --modes aligned --gold data/gold/sl_sst-ud-test.conllu --classla-type spoken --run-stamp <run-stamp>
```

Main outputs land in [predictions/output](predictions/output/) and [results/output](results/output/).

To regenerate the interactive table after a run:

```bash
python scripts/build_interactive_comparison_table_v2.py \
  data/gold/sl_<dataset>-ud-test.conllu \
  predictions/output/<run-id>_trankit_aligned_predicted.conllu \
  predictions/output/<run-id>_classla_aligned_predicted.conllu \
  results/output/<run-id>/diagnostics/trankit_aligned_eval-tagged.txt \
  results/output/<run-id>/diagnostics/classla_aligned_eval-tagged.txt \
  tables/comparison_table_v2_ssj.html \
  tables/comparison_table_v2_ssj_data.js \
  --run-id <run-id>
```

To regenerate the combined two-layer v4 table (the HTML page is static; only its
data bundle is generated, from the canonical SSJ and SST runs):

```bash
python scripts/build_interactive_comparison_table_v4.py
```

This writes [tables/comparison_table_v4_data.js](tables/comparison_table_v4_data.js) (`window.TABLE_DATA_V4`,
both corpora × both models, with error rows and example sentences for each model).
The corpora/runs are configured in `CORPORA` at the top of the script. Use
`--examples-per-item N` to cap stored examples per error pattern (default 25; `0` stores all).

## Verify Rerun

```bash
python scripts/qa_validate_run.py --run-stamp <run-stamp> --modes aligned
python scripts/verify_canonical_run.py --run-stamp <run-stamp>
```

- [scripts/qa_validate_run.py](scripts/qa_validate_run.py) — checks run integrity and aligned structure.
- [scripts/verify_canonical_run.py](scripts/verify_canonical_run.py) — checks canonical file hashes and key metrics against [references/canonical_run_manifest.json](references/canonical_run_manifest.json).

## Repository Guide

- [data](data/) — gold files and dataset helpers
- [scripts](scripts/) — pipeline, prediction, QA, and verification scripts
- [predictions](predictions/) — canonical prediction artifacts
- [results](results/) — canonical evaluation artifacts
- [tables](tables/) — interactive comparison table bundles (HTML + JS data)
- [archive](archive/) — local-only historical artifacts (not public)
- [references](references/) — paper link and canonical verification manifest

## Optional Non-Canonical Mode

Base mode remains available for local supplementary analysis:

```bash
python scripts/run_pipeline.py --modes both --run-stamp <run-stamp>
```

Supplementary outputs are intentionally local-only (gitignored).

## Reference

- DOI: https://doi.org/10.4312/slo2.0.2023.1.218-246
