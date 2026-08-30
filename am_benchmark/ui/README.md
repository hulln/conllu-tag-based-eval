# Benchmark result interface

A static, data-driven page for comparing evaluator output across systems. It reads
one generated bundle and nothing else — no CoNLL-U parsing, no metric computation,
no network calls.

## Run it

From `am_benchmark/`:

~~~text
python3 scripts/build_ui_data.py
python3 -m http.server 8000 --bind 127.0.0.1
~~~

Then open `http://127.0.0.1:8000/ui/`.

`build_ui_data.py` defaults to the 36-row authoritative spaCy/Stanza TSV. Point it
at another result file with `--input PATH_TO_RESULTS.tsv` when needed.

**Serve it over HTTP, do not open `index.html` from the file system.** A page loaded
over `file://` has an opaque origin, and Firefox and Safari refuse `history.replaceState`
there with `SecurityError: The operation is insecure.` The interface still works —
tables, sorting, selection and detail are unaffected — but it cannot update the address
bar, so links are neither shareable nor bookmarkable. When that happens the page says so
once in the footer rather than reporting a failure. The same degradation applies to any
context that blocks History API writes, such as a sandboxed preview frame.

## What the page does

The benchmark is comparative, so the comparison table is the interface.

**Context** — Language and Test data are fixed at the top. A dimension with four
or fewer values renders as a segmented control, more as a select. Options come
from rows that exist; the benchmark is not a full cross-product and no
combination is ever offered without a backing row.

**Comparison table** — every system × training-condition run in that context, with
F1 for UPOS, XPOS, Lemmas (Tagging), UAS, LAS (Dependencies) and MLAS, BLEX
(Content words). Column groups follow the evaluator's own metric semantics.
Any header sorts; the highest value in each column is bold. Rows without a usable
result show the reason instead of numbers — no value is ever invented. Metric
abbreviations expose concise definitions on pointer hover and keyboard focus.

**Detail** — selecting a row (click, Enter or Space) reveals the complete evaluator
output below the table: all 13 metric families × precision, recall, F1 and aligned
accuracy. Gold cohort, status and repeat-check state remain visible; implementation
paths and full SHA-256 checksums are available in a native Technical details
disclosure. The detail view is a section on the page, not a modal.

**Status** — a single line under the heading, derived from the rows. Every run
provisional gives one statement; a mix marks the unconfirmed runs with `†`; all
rows carrying `gold_status` `CONFIRMED` or `AUTHORITATIVE` with no benchmark-use
notice removes the line entirely. Nothing is hard-coded to a language.

## URL state

~~~text
?lang=SL&test=spokentest                                  context only
?lang=SL&test=spokentest&model=stanza&training=default     with a run open
~~~

`language=` from the first interface version is still accepted as an alias for `lang=`, so
older links restore the same context and run and are rewritten to the current form.
An unavailable value falls back to the nearest existing result and says so. Sort
order is deliberately not in the URL.

## Adding results

Nothing in `app.js` lists languages, systems or conditions. New rows in the result
TSV appear on their own. Only two things are optional additions:

- `LABELS` in `app.js` maps identifiers to display names (`spacy` → spaCy). An
  identifier with no entry renders as itself, which is correct until a real
  display name is known.
- `COMPARISON_GROUPS` chooses which metrics head the comparison table. Metrics
  absent from the bundle are dropped automatically.

## Files

- `index.html` — page structure, no data.
- `styles.css` — house style shared with `tables/comparison_table_v5.html`:
  system sans-serif/monospace stacks, `#161616` on `#f5f5f5`, hairline rules,
  2px radius, CJVT accent `#e12a26`. No external font request is made.
- `app.js` — UMD module. Loads in Node for testing; every pure function
  (`contextValues`, `resolveContext`, `rowsFor`, `sortRows`, `bestValues`,
  `isAuthoritative`, `unavailableReason`, `parseRequest`, `label`) is exported.
- `data/results.js` — generated bundle, gitignored. Do not edit by hand.

The local source files are kept synchronized with the deployable copy under
`../../tables/am_benchmark/`; only their generated `results.js` paths differ in
version-control policy.

## Indexing and publication

Both interface copies retain `<meta name="robots" content="noindex,nofollow">`
while this Netlify surface remains a staging/interface-development deployment.
That directive should be reconsidered before an actual CJVT/CLARIN publication.
