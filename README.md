# Slovenian UD Evaluation (SPOT-Trankit vs CLASSLA-Stanza)

Tag-based evaluation of SPOT-Trankit and CLASSLA-Stanza on the Slovenian UD test
sets **SSJ** (written) and **SST** (spoken / non-standard), in aligned mode (gold
sentence/token boundaries fixed, predictions on pre-tokenised text).

## Results

**[comparison_table_v4.html](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v4.html)** —
interactive table: pick a model, then a corpus; accuracy and errors per model,
with a toggle to compare. Deep-linkable, e.g. `#classla/sst`.

Each corpus uses the most domain-appropriate model:

| Corpus | SPOT-Trankit | CLASSLA-Stanza | Run |
|--------|--------------|----------------|-----|
| **SSJ-UD** (written) | 1.2 — [CLARIN 11356/1997](https://www.clarin.si/repository/xmlui/handle/11356/1997) | `default`, `pos_use_lexicon=True` | `20260414-1819_sl-ssj-ud-test_full` |
| **SST-UD** (spoken) | 1.3 — [CLARIN 11356/2201](https://www.clarin.si/repository/xmlui/handle/11356/2201) (adds non-standard spoken) | `type='spoken'` | `20260604-0859-tk13_sl-sst-ud-test_full` |

Trankit 1.3 wins on SST (every metric but UPOS and lemmas); 1.2 stays on SSJ, where it is marginally better.

Settings: [trankit==1.1.2](https://pypi.org/project/trankit/1.1.2/) (`xlm-roberta-base`),
[classla==2.2.1](https://pypi.org/project/classla/2.2.1/), full env in [requirements.txt](requirements.txt).
Gold: [UD SSJ](https://github.com/UniversalDependencies/UD_Slovenian-SSJ) v2.17, [UD SST](https://github.com/UniversalDependencies/UD_Slovenian-SST) v2.16.

Older per-corpus tables ([v2 SSJ](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v2_ssj.html),
[v3 SST](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v3_sst.html),
[v1 legacy](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v1_ssj.html)) predate v4 and still show Trankit 1.2.

## Setup & rerun

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

Add gold files to [data/gold/](data/gold/) (sources above), then:

```bash
# SSJ (Trankit 1.2)
python scripts/run_pipeline.py --modes aligned --gold data/gold/sl_ssj-ud-test.conllu --run-stamp <stamp>
# SST (Trankit 1.3) — both corpora end-to-end via Docker; see docker/README.md
bash scripts/run_trankit13_eval.sh        # GPU=1 to use a GPU
```

Regenerate the v4 table data bundle (runs configured in `CORPORA` at the top of the script):

```bash
python scripts/build_interactive_comparison_table_v4.py
```

## Reproducibility

The SSJ 1.2 run is hash- and metric-pinned in [references/canonical_run_manifest.json](references/canonical_run_manifest.json):

```bash
python scripts/qa_validate_run.py --run-stamp <stamp> --modes aligned
python scripts/verify_canonical_run.py --run-stamp <stamp>
```

## Repository guide

- [scripts/](scripts/) — pipeline, prediction, QA, verification
- [data/](data/) — gold files and dataset notes
- [predictions/](predictions/), [results/](results/) — run artifacts
- [tables/](tables/) — interactive table bundles (HTML + JS)
- [docker/](docker/) — containerised run (used for the Trankit 1.3 SST run)
- [references/](references/) — paper link and verification manifest

## Reference

DOI: https://doi.org/10.4312/slo2.0.2023.1.218-246
