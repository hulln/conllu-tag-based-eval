# Slovenian UD Evaluation (CLASSLA vs Trankit)

Compact, reproducible evaluation of two Slovenian UD pipelines on the SSJ test set.

- CLASSLA-Stanza 2.2.1 with lexicon
- Trankit
- Evaluator: `evaluation/conll18_ud_eval_tag-based.py`

## Primary Method

This repository reports one primary workflow:

- `aligned`: evaluation on gold sentence segmentation and gold tokenization

In aligned mode, the gold CoNLL-U file is the structural input. Sentence boundaries and token boundaries are fixed to gold, and the models predict the remaining layers:

- lemma
- UPOS
- XPOS
- FEATS
- HEAD
- DEPREL

This is the method that should be used for headline numbers and final reporting.

Optional supplementary workflow:

- `base`: full-text processing from raw sentence text, where model sentence splitting/tokenization may differ from gold

`base` remains available for supplementary analysis and legacy comparison, but it is not the primary evaluation target.

## Repository Map

- `data/` input datasets and local subsets ([details](data/README.md))
- `scripts/` pipeline, prediction, QA, and analysis entry points ([details](scripts/README.md))
- `predictions/` generated CoNLL-U predictions ([details](predictions/README.md))
- `results/` evaluation outputs and diagnostics ([details](results/README.md))
- `references/` papers, links, and project instructions ([details](references/README.md))
- `archive/` older and legacy experiment outputs ([details](archive/README.md))

## Canonical Run

Current active canonical run:

- `20260414-1323_sl-ssj-ud-test_full`

Older run snapshots are kept locally under `archive/local/` (gitignored, not public).

## Data Setup

The gold SSJ test file is intentionally not committed. Place it locally at:

- `data/gold/sl_ssj-ud-test.conllu`

Source and provenance:

- SSJ source repository: https://github.com/UniversalDependencies/UD_Slovenian-SSJ
- Local copy obtainment date used in this project: 2026-04-10

Optional raw sentence input for base mode:

```bash
python scripts/export_raw_sentences.py \
  data/gold/sl_ssj-ud-test.conllu \
  data/raw/sl_ssj-ud-test.sentences.txt
```

## Environment Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Notes:

- `CLASSLA` models can be downloaded with `--download-classla-models` on the first run.
- `Trankit` models are cached automatically under `cache/trankit/` using HTTPS sources.

## Running The Pipeline

Primary aligned run:

```bash
python scripts/run_pipeline.py --download-classla-models
```

Small aligned sanity run:

```bash
python scripts/run_pipeline.py --sample-lines 20 --download-classla-models
```

Aligned evaluation only, reusing the latest complete aligned prediction set:

```bash
python scripts/run_pipeline.py --skip-prediction
```

Optional supplementary run with both aligned and base outputs:

```bash
python scripts/run_pipeline.py --modes both --download-classla-models
```

Optional supplementary evaluation-only rerun with both modes:

```bash
python scripts/run_pipeline.py --modes both --skip-prediction
```

By default, `scripts/run_pipeline.py` also runs strict QA validation at the end and writes `qa_validation.md` for the run.

## QA And Outputs

Open these files first for a run:

1. `results/runs/<run-id>/main/qa_validation.md`
2. `results/runs/<run-id>/main/*_aligned_eval.txt`
3. `results/runs/<run-id>/main/classla-vs-trankit_aligned_comparison.md`
4. `results/runs/<run-id>/diagnostics/`

For this repository today, open these first:

1. `results/runs/20260414-1323_sl-ssj-ud-test_full/main/qa_validation.md`
2. `results/runs/20260414-1323_sl-ssj-ud-test_full/main/classla_aligned_eval.txt`
3. `results/runs/20260414-1323_sl-ssj-ud-test_full/main/trankit_aligned_eval.txt`
4. `results/runs/20260414-1323_sl-ssj-ud-test_full/diagnostics/`

If supplementary base mode was enabled, its outputs are kept separate under:

- `results/runs/<run-id>/supplementary/base/`

Prediction naming:

- `<timestamp>_<dataset>_<run-label>_<model>_<mode>_predicted.conllu`

Aligned predictions preserve gold `sent_id` values and sentence-level metadata where available.

## Manual QA

Run QA directly for an aligned run:

```bash
python scripts/qa_validate_run.py --run-stamp <run-stamp> --modes aligned
```

Run QA for a supplementary aligned+base run:

```bash
python scripts/qa_validate_run.py --run-stamp <run-stamp> --modes both
```

The validator is mode-aware. An aligned-only run is validated as aligned-only and is not required to produce base artifacts.

## Reference Article

- Dobrovoljc, K., Terčon, L., Ljubešić, N. (2023). *Universal Dependencies za slovenščino: nove smernice, ročno označeni podatki in razčlenjevalni model.*
- DOI: https://doi.org/10.4312/slo2.0.2023.1.218-246

## Reproducibility Notes

- Keep aligned outputs as the canonical reporting layer.
- Treat base outputs as supplementary only.
- Use run-stamped filenames and folders; do not overwrite historical runs intentionally.
- Review `qa_validation.md` before publishing numbers.
