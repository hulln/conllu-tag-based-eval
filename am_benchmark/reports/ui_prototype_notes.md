# Local benchmark UI prototype notes

## Scope and status

The prototype is under `am_benchmark/ui/` and is separate from the deployed
tables in the repository root. It displays 36 authoritative spaCy/Stanza rows:
six each for EN/NL/SL written and spoken conditions.

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
- `ui/data/results.js` is the generated compact browser bundle.
- `ui/index.html`, `ui/styles.css`, and `ui/app.js` implement the local page.
- `ui/README.md` contains local run instructions.

The builder uses `reports/authoritative_spacy_stanza_results.tsv` by default. It validates
required identifiers, rejects duplicate
`language + model + training_condition + test_condition` keys, discovers metric
families and fields from the TSV header, converts numeric cells to numbers and
empty cells to `null`, and preserves statuses, notices, file identifiers, and
hashes. It emits 36 rows and 13 evaluator metric families. The frontend does
not load any CoNLL-U file.

## Selector and URL logic

The controls follow:

~~~text
language -> model -> training condition -> test condition
~~~

At each level, options are derived from rows matching earlier choices. A future
partial cross-product therefore cannot expose an impossible downstream option.
Changing an earlier selector preserves only still-valid later values and
otherwise falls back to the first available row.

State is represented by query parameters:

~~~text
?language=SL&model=stanza&training=default&test=spokentest
~~~

Refreshes preserve valid selections. An invalid requested value falls back to
the nearest valid row and shows an explanatory message instead of an empty or
broken page.

## Results and provisional handling

The selected view shows five compact F1 cards matching the current interface's
overview (Lemmas, UPOS, XPOS, UAS, LAS), followed by a complete table of all 13
evaluator metrics and every score/count field present in the source schema. The
current TSV has precision, recall, F1, and aligned accuracy but no raw-count
columns, so the page says counts are unavailable and does not fabricate them.

A compact comparison table contains all successful rows with the selected
language and test condition, making spaCy/Stanza and training-condition
comparisons visible without a separate dashboard.

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

## Before production integration

- Complete manual visual, accessibility, keyboard, and narrow-width review.
- Review language-specific XPOS terminology and user-facing labels.
- Decide how detailed error/example data will be generated and represented.
- Integrate only after the prototype data contract and official results are
  accepted; do not overwrite the current production table directly.
