# Slovenian UD Evaluation (SPOT-Trankit vs CLASSLA-Stanza)

Tag-based evaluation of SPOT-Trankit and CLASSLA-Stanza on the Slovenian UD test
sets **SSJ** (written) and **SST** (spoken / non-standard), in aligned mode (gold
sentence/token boundaries fixed, predictions on pre-tokenised text).

Each evaluation run is documented in [experiments/](experiments/) — start there
to see what has been run, why, and where its outputs are.

## Results

**Current table:** [live v5 table](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v5.html)
([local file](tables/comparison_table_v5.html)) combines SSJ written, SST
standardised, and supplied SST colloquial (`pog`) evaluation. It provides per-tool
metric summaries, accuracy/error tables, examples, compare mode, deep links, and
CSV/Markdown export.

**Slovenian version:** [live v5 table](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v5_sl.html)
([local file](tables/comparison_table_v5_sl.html)). Both pages use the same generated
data bundle.

v5 uses [SPOT-Trankit 1.3](https://www.clarin.si/repository/xmlui/handle/11356/2201)
for all test sets and [CLASSLA-Stanza 2.2.1](https://pypi.org/project/classla/2.2.1/).
Evaluation is aligned: gold sentence and token boundaries are fixed, and the
models predict lemma, POS/morphology, and dependency annotation.

| Test set | Gold data | SPOT-Trankit | CLASSLA-Stanza |
|---|---|---|---|
| SSJ written | UD Slovenian SSJ `r2.17` | 1.3 | `classla.Pipeline('sl', pos_use_lexicon=True)` |
| SST standardised | UD Slovenian SST `r2.16` / `r2.17` | 1.3 | `classla.Pipeline('sl', type='spoken')` |
| SST colloquial | supplied `pog` test file | 1.3 | `classla.Pipeline('sl', type='spoken')` |

The supplied paired `stan` file is present locally but is not evaluated in v5.
See [references/v5_publication_qa_2026-06-22.md](references/v5_publication_qa_2026-06-22.md)
and [references/sst_vs_pog_comparison_2026-06-22.md](references/sst_vs_pog_comparison_2026-06-22.md)
for the data audit.

Previous table versions are kept for traceability: [v4](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v4.html),
[v3 SST](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v3_sst.html),
[v2 SSJ](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v2_ssj.html),
and [v1 legacy](https://conllu-tag-based-eval-table.netlify.app/comparison_table_v1_ssj.html).

## Publishing (CJVT)

The v5 pages (EN + SL) are being published on CJVT infrastructure at
https://orodja.cjvt.si/oznacevalnik/eval/ (in progress, July 2026). Only the
files needed to serve the pages (the two v5 HTMLs, the shared data bundle,
favicons, and logos) are mirrored to a separate deploy repository on the CJVT
Gitea (`webapps/oznacevalnik-eval`); this repository remains the development
workspace.

## Stanza 1.13 vs 1.14 comparison

A separate aligned evaluation compares **Stanza 1.13.0** and **Stanza 1.14.0** on
both Slovenian test sets, using the `default` and `default_accurate` packages. On
each test set the release upgrade changes very little, while choosing
`default_accurate` over `default` makes a clear difference (about +4 LAS).

| Arm | Documentation | Results |
|---|---|---|
| SSJ written | [experiments/20260810-stanza-1.13-vs-1.14-ssj/](experiments/20260810-stanza-1.13-vs-1.14-ssj/) | [results …_sl-ssj-ud-test_full/main/](results/output/20260810-stanza-1.13-vs-1.14_sl-ssj-ud-test_full/main/) |
| SST spoken | [experiments/20260810-stanza-1.13-vs-1.14-sst/](experiments/20260810-stanza-1.13-vs-1.14-sst/) | [results …_sl-sst-ud-test_full/main/](results/output/20260810-stanza-1.13-vs-1.14_sl-sst-ud-test_full/main/) |

**Important provenance note:** a follow-up audit found that the current Stanza
1.13 and 1.14 resources resolve to byte-identical Slovenian POS and
dependency-parser checkpoints. These runs therefore do not reconstruct the
original 1.13 default model configuration; the Stanza library versions and
lemmatizer checkpoints still differ. See
[model provenance audit](references/stanza-1.13-vs-1.14-model-provenance.md).
No significance testing was performed.

## Setup & rerun

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

Add gold files to [data/gold/](data/gold/) (see [data/README.md](data/README.md)),
then run the aligned pipeline or the dedicated Trankit 1.3 Docker workflow:

```bash
# General aligned run
python3 scripts/run_pipeline.py --modes aligned --gold data/gold/sl_ssj-ud-test.conllu --run-stamp <stamp>
# Trankit 1.3 workflow; see experiments/20260604-0859-tk13/README.md
bash scripts/run_trankit13_eval.sh        # GPU=1 to use a GPU
```

Regenerate the v5 data bundle:

```bash
python3 scripts/build_interactive_comparison_table_v5.py
```

## Reproducibility

Every run writes a `qa_validation.md` integrity report; the canonical run is also
pinned (file hashes + metrics) in [references/canonical_run_manifest.json](references/canonical_run_manifest.json)
for exact-match verification:

```bash
python3 scripts/qa_validate_run.py --run-stamp <stamp> --modes aligned   # any run: integrity
python3 scripts/verify_canonical_run.py --run-stamp <stamp>              # canonical: exact match
```

## Repository guide

- [experiments/](experiments/) — one directory per run: what was done, how, and with what environment
- [scripts/](scripts/) — reusable code: pipeline, prediction, evaluation, QA, verification
- [data/](data/) — gold files and dataset notes
- [predictions/](predictions/), [results/](results/) — generated run artifacts
- [tables/](tables/) — interactive table bundles (HTML + JS); [tables/logos/](tables/logos/) for logo assets
- [docker/](docker/) — container build files and generic container instructions
- [references/](references/) — canonical verification manifest, cross-run notes, external sources

## Reference

DOI: https://doi.org/10.4312/slo2.0.2023.1.218-246
