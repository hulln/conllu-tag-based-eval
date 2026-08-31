# Local benchmark UI prototype notes

## Scope and status

The interface is under `tables/am_benchmark/`, alongside the other deployed tables
in the site root. It displays 36 authoritative spaCy/Stanza rows: six each for
EN/NL/SL written and spoken conditions. It began as a prototype under
`am_benchmark/ui/`; see "Files and data transformation" below for why that copy is
gone.

## Existing interface inspection

The production v5 interface consists primarily of:

- `scripts/build_interactive_comparison_table_v5.py`, which builds a JavaScript
  data bundle;
- `tables/comparison_table_v5_data.js`, which stores `window.TABLE_DATA_V5`;
- `tables/comparison_table_v5.html`, which contains the static page, styling,
  selectors, URL-hash state, metric/error tables, exports, and examples.

The v5 builder hard-codes Trankit/CLASSLA, SSJ/SST/POG, run IDs, gold and result
paths, provenance copy, and a two-model comparison. The page state is exactly
`{model, corpus}` and the URL hash is `#model/corpus`. Its generated JavaScript
bundle pattern, metric-card/table formatting, responsive layout principles,
and simple browser state are reusable. Model/corpus combinations, selector
options, status text, and result lookup need to be data-driven.

## Files and data transformation

- `scripts/build_ui_data.py` reads an evaluation-result TSV.
- `../tables/am_benchmark/data/results.js` is the generated compact browser bundle.
- `../tables/am_benchmark/index.html`, `styles.css` and `app.js` implement the page.
- `../tables/am_benchmark/README.md` contains the run instructions.

The prototype was first built under `am_benchmark/ui/` and copied to
`tables/am_benchmark/` for deployment. The two copies were folded into the single
`tables/am_benchmark/` directory once the interface stopped being provisional: five
files were being committed twice and hand-synchronised, and `tables/` is the
deployed site root, which is where `build_interactive_comparison_table_v5.py`
already writes.

The builder uses `reports/authoritative_spacy_stanza_results.tsv` by default. It validates
required identifiers, rejects duplicate
`language + model + training_condition + test_condition` keys, discovers metric
families and fields from the TSV header, converts numeric cells to numbers and
empty cells to `null`, and preserves statuses, notices, file identifiers, and
hashes. It emits 36 rows and 13 evaluator metric families. The frontend does
not load any CoNLL-U file.

## Context controls and URL logic

The controls establish a comparison context, and the table then shows the systems
inside it:

~~~text
language -> test condition -> training condition (or All)
~~~

Language and test condition cascade: at each level, options are derived from rows
matching earlier choices, so a partial cross-product cannot expose an impossible
downstream option. Training data is a filter over that context rather than a further
cascade step, and its default is **All**, which keeps every training setup visible —
the experimental structure is the thing most of these rows exist to show. Changing an
earlier control preserves still-valid later values and otherwise falls back to the
first available row.

State is represented by query parameters:

~~~text
?lang=SL&test=spokentest&training=all
~~~

`training=all` is the reserved value for "every training setup"; it cannot collide
with a manifest identifier. An invalid requested value falls back to the nearest
valid row and shows an explanatory message instead of an empty or broken page.

An earlier version of the interface used `&model=…&training=…` to open one run's
evaluator output on the overview. Those links still resolve: the training filter is
applied, while the obsolete model selection is dropped. The evaluator output itself
moved to the analysis page.

## Results and provisional handling

The overview is the comparison table and nothing else. Five headline metrics
(UPOS, XPOS, Lemmas, UAS, LAS) plus MLAS and BLEX appear as columns grouped the way
the evaluator groups them; the complete 13-family × 4-field evaluator output and the
provenance block live on the analysis page, so the overview does not carry a third
level of expandable detail. The current TSV has precision, recall, F1 and aligned
accuracy but no raw-count columns, so the analysis page says counts are unavailable
and does not fabricate them.

With Training = All the table groups each system's training runs together; with one
training setup selected it becomes a one-row-per-system leaderboard sorted by LAS.
Sorting is group-aware in All mode and never scatters a system's runs.

The warning is row-driven. It remains visible if the row is not successful
authoritative data or carries a benchmark-use warning. It disappears only when
`result_status=success`, `gold_status` is `CONFIRMED` or `AUTHORITATIVE`, and no
benchmark-use notice is present. Future rows with missing gold, excluded status,
or evaluator errors receive an appropriate empty-state message and no invented
scores.

## Adding future results

Run the evaluation wrapper with `--initial-debugging-only` for authoritative
stable output, then run `scripts/build_ui_data.py --input PATH_TO_RESULTS.tsv`.
General evaluation output keeps non-stable systems explicitly provisional. New
model or condition identifiers appear without changes to the HTML.

No HTML/JavaScript combination list needs to change. New model or condition
labels fall back to their manifest values; presentation labels can be added
separately without changing result lookup.

## Local QA

Passed checks:

- Python builder syntax and deterministic 36-row/13-metric generation.
- Exact reconciliation of every generated numeric metric and status against the
  source TSV.
- JavaScript syntax.
- State resolution for all four required selections.
- Dynamic-option membership and fallback from an invalid EN/missing-model URL.
- Authoritative classification for every current row; no provisional warning.
- HTTP 200 responses for the page, scripts, data bundle, and four parameterized
  local URLs on a loopback-only static server.
- The prior headless-browser layout pass covered selection, fallback, metric
  sections, and error-panel behavior. The current authoritative bundle preserves
  the same schema and was rechecked programmatically for all dimensions.
- A 1440-pixel desktop screenshot was inspected for hierarchy, overflow,
  selector/status readability, metric-card alignment, and table layout; no
  obvious visual defect was found. The temporary screenshot was not retained.

After the interface redesign, a headless-browser pass covered: all six
language/test contexts; grouped and leaderboard table modes; group-aware sorting;
best-value emphasis checked against the bundle's own maxima; Analyse links and
row activation; URL state, refresh and invalid/legacy links; the analysis page's
title, summary metrics, every table, the full evaluator output and provenance;
the examples panel where examples exist and its absence where they do not; four
viewport widths (1440, 1024, 768, 390) for panning, clipping, pinned columns and
panel behaviour; and keyboard operation of controls, sorting, filters, Show more,
error rows, dialog trapping and focus return.

## Before production integration

- Review language-specific XPOS terminology and user-facing labels.
- Detailed error and example data is decided and implemented: aggregate diagnostics
  per run (`build_diagnostics_data.py`, text-free for every run) plus a separate
  sentence-example layer for the redistributable cohorts (`build_examples_data.py`,
  30 of the 36 runs). What remains is review of the published wording and licences.
- Integrate only after the prototype data contract and official results are
  accepted; do not overwrite the current production table directly.
