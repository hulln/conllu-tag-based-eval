# Slovenian UD Evaluation (SPOT-Trankit vs CLASSLA-Stanza)

Tag-based evaluation of SPOT-Trankit and CLASSLA-Stanza on the Slovenian UD test
sets **SSJ** (written) and **SST** (spoken / non-standard), in aligned mode (gold
sentence/token boundaries fixed, predictions on pre-tokenised text).

## Results

**Current table (v6):** published at https://orodja.cjvt.si/oznacevalnik/eval/
([EN](https://orodja.cjvt.si/oznacevalnik/eval/en/) · [SL](https://orodja.cjvt.si/oznacevalnik/eval/sl/));
local files [EN](tables/comparison_table_v6.html) · [SL](tables/comparison_table_v6_sl.html).
It combines SSJ written, SST standardised, and supplied SST colloquial (`pog`)
evaluation for three tools, with per-tool metric summaries, per-tag F1 tables,
error tables with examples, compare mode, deep links, and CSV/Markdown export.
Both pages use the same generated data bundle.

v6 is v5 with Stanza 1.14 (`default_accurate`) as a third tool; how it was run:
[docker/README.stanza114-eval.md](docker/README.stanza114-eval.md). SPOT-Trankit
and CLASSLA-Stanza results are v5's: v5 uses [SPOT-Trankit 1.3](https://www.clarin.si/repository/xmlui/handle/11356/2201)
for all test sets and [CLASSLA-Stanza 2.2.1](https://pypi.org/project/classla/2.2.1/).
Evaluation is aligned: gold sentence and token boundaries are fixed, and the
models predict lemma, POS/morphology, and dependency annotation.

| Test set | Gold data | SPOT-Trankit | CLASSLA-Stanza | Stanza (v6) |
|---|---|---|---|---|
| SSJ written | UD Slovenian SSJ `r2.17` | 1.3 | `classla.Pipeline('sl', pos_use_lexicon=True)` | 1.14.0 `default_accurate` |
| SST standardised | UD Slovenian SST `r2.16` / `r2.17` | 1.3 | `classla.Pipeline('sl', type='spoken')` | 1.14.0 `default_accurate` |
| SST colloquial | supplied `pog` test file | 1.3 | `classla.Pipeline('sl', type='spoken')` | 1.14.0 `default_accurate` |

The supplied paired `stan` file is present locally but is not evaluated in v5 or v6.
See [references/v5_publication_qa_2026-06-22.md](references/v5_publication_qa_2026-06-22.md)
and [references/sst_vs_pog_comparison_2026-06-22.md](references/sst_vs_pog_comparison_2026-06-22.md)
for the data audit.

Previous table versions are kept for traceability: [v5](https://wip.nhull.eu/eval/comparison_table_v5.html)
([SL](https://wip.nhull.eu/eval/comparison_table_v5_sl.html)), [v4](https://wip.nhull.eu/eval/comparison_table_v4.html),
[v3 SST](https://wip.nhull.eu/eval/comparison_table_v3_sst.html),
[v2 SSJ](https://wip.nhull.eu/eval/comparison_table_v2_ssj.html),
and [v1 legacy](https://wip.nhull.eu/eval/comparison_table_v1_ssj.html).

## Publishing

**CJVT:** the current pages (EN + SL) are published at
https://orodja.cjvt.si/oznacevalnik/eval/. Only the files needed to serve them
are copied to a separate deploy repository on the CJVT Gitea
(`webapps/oznacevalnik-eval`), under version-neutral names (`en.html`, `sl.html`,
`data.js`, favicons, logos); this repository remains the development workspace.
The deploy is not automatic: after a push to Gitea, CJVT pulls the repository
onto the server, so they need to be told.

```bash
python3 scripts/export_cjvt_deploy.py ../oznacevalnik-eval   # then commit and push there
```

**Drafts and earlier versions** are at https://wip.nhull.eu/eval/. The `wip`
site fetches `tables/` from this repository's `main` on every build, so only what
git tracks goes online. A push that changes `tables/` on `main` triggers the
rebuild ([.github/workflows/update-wip.yml](.github/workflows/update-wip.yml)).

## Setup & rerun

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

Add gold files to `data/gold/` (gitignored; see [data/README.md](data/README.md)),
then run the aligned pipeline or the dedicated Trankit 1.3 Docker workflow:

```bash
# General aligned run
python3 scripts/run_pipeline.py --modes aligned --gold data/gold/sl_ssj-ud-test.conllu --run-stamp <stamp>
# Trankit 1.3 workflow; see docker/README.md
bash scripts/run_trankit13_eval.sh        # GPU=1 to use a GPU
```

Regenerate the v5 data bundle, or the v6 data bundle and pages (the v6 pages
are made from the v5 pages by exact-match edits):

```bash
python3 scripts/build_interactive_comparison_table_v5.py
python3 scripts/build_interactive_comparison_table_v6.py && python3 scripts/make_comparison_table_v6_pages.py
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
