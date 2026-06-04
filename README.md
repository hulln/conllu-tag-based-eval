# Slovenian UD Evaluation (SPOT-Trankit vs CLASSLA-Stanza)

Reproducible, tag-based evaluation of SPOT-Trankit and CLASSLA-Stanza on the
Slovenian UD test sets: **SSJ** (standard, written) and **SST** (spoken /
non-standard). All results use **aligned mode** — gold sentence and token
boundaries are fixed and predictions are run on pre-tokenised text.

## Current results (recommended)

**[comparison_table_v4.html](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v4.html)** —
the combined interactive table. Pick a **model** (SPOT-Trankit / CLASSLA-Stanza),
then a **corpus** (SSJ-UD / SST-UD); each section shows that model's accuracy and
errors, with a "Compare with …" toggle for the other model's column and the
difference. Deep-linkable via URL hash, e.g. `#classla/sst`.

The table reports the **most domain-appropriate model per corpus** — the same
principle applied to both tools:

| Corpus | SPOT-Trankit | CLASSLA-Stanza | Run |
|--------|--------------|----------------|-----|
| **SSJ-UD** (written) | model **1.2** — [CLARIN 11356/1997](https://www.clarin.si/repository/xmlui/handle/11356/1997), `trankit-sl-ssj+sst.zip` | `default` pipeline, `pos_use_lexicon=True` | `20260414-1819_sl-ssj-ud-test_full` |
| **SST-UD** (spoken) | model **1.3** — [CLARIN 11356/2201](https://www.clarin.si/repository/xmlui/handle/11356/2201), `trankit-sl-ssj+sststand+sstpog.zip` (adds non-standard spoken) | `type='spoken'`, lexicon disabled | `20260604-0859-tk13_sl-sst-ud-test_full` |

For SST, Trankit **1.3** beats 1.2 on every metric except UPOS (unchanged) and
lemmatisation (−0.05), so it is used for spoken text; for SSJ, 1.2 is marginally
better on every metric and is kept for written text. CLASSLA likewise uses its
spoken model for SST and the standard (lexicon-backed) model for SSJ.

### Fixed settings (both corpora)

- **Method:** aligned mode — gold sentence/token boundaries supplied; predictions on pre-tokenised text.
- **SPOT-Trankit:** [trankit==1.1.2](https://pypi.org/project/trankit/1.1.2/), embeddings `xlm-roberta-base`.
- **CLASSLA-Stanza:** [classla==2.2.1](https://pypi.org/project/classla/2.2.1/).
- **Full pinned environment:** [requirements.txt](requirements.txt).
- **Gold data:**
  - SSJ — [UD Slovenian-SSJ](https://github.com/UniversalDependencies/UD_Slovenian-SSJ) test set, v2.17 (2025-10-22).
  - SST — [UD Slovenian-SST](https://github.com/UniversalDependencies/UD_Slovenian-SST) test set, v2.16 (2024-12-20).

## Reproducibility & canonical runs

- **Hash-pinned anchor:** the SSJ 1.2 run `20260414-1819_sl-ssj-ud-test_full` is
  verified byte-for-byte (file hashes + key metrics) against
  [references/canonical_run_manifest.json](references/canonical_run_manifest.json).
- **SST baseline (Trankit 1.2):** `20260420-1105_sl-sst-ud-test_full` — the earlier
  spoken run, before model 1.3.
- **SST current (Trankit 1.3):** `20260604-0859-tk13_sl-sst-ud-test_full` — produced
  with the Docker setup in [docker/README.md](docker/README.md) /
  [scripts/run_trankit13_eval.sh](scripts/run_trankit13_eval.sh). CLASSLA there is
  identical to the 1.2 baseline (spoken model); only Trankit changed.
- Old and non-canonical outputs: local-only under [archive/local](archive/local/) (gitignored).

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

**SSJ (written), Trankit 1.2:**

```bash
python scripts/run_pipeline.py --modes aligned --gold data/gold/sl_ssj-ud-test.conllu --run-stamp <run-stamp>
```

**SST (spoken), Trankit 1.2 baseline:**

```bash
python scripts/run_pipeline.py --modes aligned --gold data/gold/sl_sst-ud-test.conllu --classla-type spoken --run-stamp <run-stamp>
```

**SST (spoken), Trankit 1.3** — needs the model URL/MD5/cache flags; the Docker
helper wraps both corpora end to end (see [docker/README.md](docker/README.md)):

```bash
bash scripts/run_trankit13_eval.sh        # GPU=1 to use a GPU; runs SSJ then SST
```

Main outputs land in [predictions/output](predictions/output/) and [results/output](results/output/).

To regenerate the combined v4 table (the HTML page is static; only its data
bundle is generated, with corpora/runs configured in `CORPORA` at the top of the
script):

```bash
python scripts/build_interactive_comparison_table_v4.py
```

This writes [tables/comparison_table_v4_data.js](tables/comparison_table_v4_data.js)
(`window.TABLE_DATA_V4`, both corpora × both models, with error rows and example
sentences). Use `--examples-per-item N` to cap stored examples per error pattern
(default 25; `0` stores all).

## Verify Rerun

```bash
python scripts/qa_validate_run.py --run-stamp <run-stamp> --modes aligned
python scripts/verify_canonical_run.py --run-stamp <run-stamp>
```

- [scripts/qa_validate_run.py](scripts/qa_validate_run.py) — checks run integrity and aligned structure.
- [scripts/verify_canonical_run.py](scripts/verify_canonical_run.py) — checks canonical file hashes and key metrics against [references/canonical_run_manifest.json](references/canonical_run_manifest.json).

## Earlier per-corpus tables (archived)

Single-model (SPOT-Trankit only) per-corpus tables predate the combined v4 table
and are kept for reference. **They still reflect Trankit 1.2**; the recommended,
up-to-date comparison — including Trankit 1.3 for SST — is the v4 table above.

| Dataset | Table | Run |
|---------|-------|-----|
| SSJ-UD (written) | [comparison_table_v2_ssj.html](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v2_ssj.html) | `20260414-1819_sl-ssj-ud-test_full` (Trankit 1.2) |
| SST-UD (spoken) | [comparison_table_v3_sst.html](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v3_sst.html) | `20260420-1105_sl-sst-ud-test_full` (Trankit 1.2) |

A legacy Slovenian-language v1 table is also available at [comparison_table_v1_ssj.html](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v1_ssj.html).

These per-corpus tables are produced by [scripts/build_interactive_comparison_table_v2.py](scripts/build_interactive_comparison_table_v2.py); see its header for the argument order.

## Repository Guide

- [data](data/) — gold files and dataset helpers
- [scripts](scripts/) — pipeline, prediction, QA, and verification scripts
- [predictions](predictions/) — canonical prediction artifacts
- [results](results/) — canonical evaluation artifacts
- [tables](tables/) — interactive comparison table bundles (HTML + JS data)
- [docker](docker/) — containerised run setup (used for the Trankit 1.3 SST run)
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
