# Slovenian UD Evaluation (CLASSLA vs Trankit)

Compact, reproducible evaluation of two Slovenian UD pipelines on the SSJ test set.

- CLASSLA-Stanza 2.2.1 (with lexicon)
- Trankit
- Evaluator: `evaluation/conll18_ud_eval_tag-based.py`

## What This Repo Produces

Primary workflow (main task):

- `aligned`: sentence and token boundaries are fixed to gold

Optional supplementary workflow:

- `base`: full-text processing (model sentence splitting/tokenization can differ)

When `--modes both` is used, you get four prediction files per run:

1. classla aligned
2. classla base
3. trankit aligned
4. trankit base

All predictions are evaluated against gold. Aligned outputs are the primary reporting target; base outputs are supplementary.

## Repository Map

- `data/` input datasets and subsets ([details](data/README.md))
- `scripts/` prediction, evaluation, analysis, QA ([details](scripts/README.md))
- `predictions/` generated CoNLL-U predictions ([details](predictions/README.md))
- `results/` evaluation outputs and diagnostics ([details](results/README.md))
- `references/` papers, links, and project instructions ([details](references/README.md))
- `archive/` older or legacy experiment outputs ([details](archive/README.md))

## Data Provenance

- Local gold files in `data/gold/` are intentionally gitignored.
- SSJ source repository: https://github.com/UniversalDependencies/UD_Slovenian-SSJ
- Local copy obtainment date: 2026-04-10

## Reference Article

- Dobrovoljc, K., Terčon, L., Ljubešić, N. (2023). *Universal Dependencies za slovenščino: nove smernice, ročno označeni podatki in razčlenjevalni model.*
- DOI: https://doi.org/10.4312/slo2.0.2023.1.218-246

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Small sanity run (fast):

```bash
python scripts/run_pipeline.py --sample-lines 20 --download-classla-models
```

Full run:

```bash
python scripts/run_pipeline.py --download-classla-models
```

Full run with supplementary base outputs:

```bash
python scripts/run_pipeline.py --modes both --download-classla-models
```

Evaluation only (reuse existing predictions):

```bash
python scripts/run_pipeline.py --skip-prediction
```

Evaluation only with supplementary base outputs:

```bash
python scripts/run_pipeline.py --modes both --skip-prediction
```

## Where To Look First (External Reader)

1. Latest QA summary: `results/runs/<run-id>/main/qa_validation.md`
2. Main aligned metrics: `results/runs/<run-id>/main/*_aligned_eval.txt`
3. Main aligned comparison: `results/runs/<run-id>/main/classla-vs-trankit_aligned_comparison.md`
4. Detailed aligned diagnostics: `results/runs/<run-id>/diagnostics/`
5. Supplementary base outputs (if enabled): `results/runs/<run-id>/supplementary/base/`

## Naming Conventions

- Prediction file format:
  `<timestamp>_<dataset>_<run-label>_<model>_<mode>_predicted.conllu`
- Results are split into:
  - `main/` and `diagnostics/` for aligned primary outputs
  - `supplementary/base/` for base-mode outputs

## Reproducibility Notes

- Keep aligned primary outputs and base supplementary outputs separate.
- Use run-stamped filenames/folders; do not overwrite historical runs.
- Run `scripts/qa_validate_run.py` before reporting final numbers.
