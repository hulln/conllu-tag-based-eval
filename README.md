# Slovenian UD Evaluation (SPOT-Trankit vs CLASSLA-Stanza)

Tag-based evaluation of SPOT-Trankit and CLASSLA-Stanza on the Slovenian UD test
sets **SSJ** (written) and **SST** (spoken / non-standard), in aligned mode (gold
sentence/token boundaries fixed, predictions on pre-tokenised text).

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

A separate aligned evaluation compares **Stanza 1.13.0** and **Stanza 1.14.0**
on the same SSJ-UD test set, using both `default` and `default_accurate`
packages.

The complete reproducibility record, including Docker environments, exact
package versions, model caches, encountered compatibility issues, run commands
and results, is in
[docker/README_stanza_versions.md](docker/README_stanza_versions.md).

## Setup & rerun

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

Add gold files to [data/gold/](data/gold/) (see [data/README.md](data/README.md)),
then run the aligned pipeline or the dedicated Trankit 1.3 Docker workflow:

```bash
# General aligned run
python3 scripts/run_pipeline.py --modes aligned --gold data/gold/sl_ssj-ud-test.conllu --run-stamp <stamp>
# Trankit 1.3 workflow; see docker/README.md
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

- [scripts/](scripts/) — pipeline, prediction, QA, verification
- [data/](data/) — gold files and dataset notes
- [predictions/](predictions/), [results/](results/) — run artifacts
- [tables/](tables/) — interactive table bundles (HTML + JS)
- [tables/logos/](tables/logos/) — local logo assets and source URLs
- [docker/](docker/) — containerised run (used for the Trankit 1.3 SST run)
- [references/](references/) — paper link and verification manifest

## Reference

DOI: https://doi.org/10.4312/slo2.0.2023.1.218-246
