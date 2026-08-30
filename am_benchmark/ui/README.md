# Benchmark result interface

A static, data-driven page for comparing evaluator output across systems. It reads
one generated bundle and nothing else — no CoNLL-U parsing, no metric computation,
no network calls.

## Run it

From `am_benchmark/`:

~~~text
python3 scripts/build_ui_data.py
python3 scripts/build_diagnostics_data.py
python3 -m http.server 8000 --bind 127.0.0.1
~~~

Then open `http://127.0.0.1:8000/ui/`.

`build_ui_data.py` defaults to the 36-row authoritative spaCy/Stanza TSV. Point it
at another result file with `--input PATH_TO_RESULTS.tsv` when needed.
`build_diagnostics_data.py` writes the per-run diagnostic set the analysis page
reads; it is only needed when that page is in use, and it never touches
`data/results.js`.

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

**Detailed analysis** — the detail section carries one link out, to `analysis.html`
for the open run. It is a route to a different page, not a second view of this one;
the row-click interaction is unchanged.

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

## Detailed analysis page

`analysis.html` is the second surface: aggregate error and accuracy diagnostics for
**one** run, reached from the overview's detail section. It deliberately does not
repeat the comparison table.

Sections: run summary (F1 and correct counts, plus the same reproducibility block
the overview shows), LAS by dependency relation, UPOS accuracy, dependency parsing
errors in the three CJVT categories, and tagging errors. Every table sorts by any
header on click, Enter or Space. Tables longer than 25 rows open truncated with a
control that names how many rows are folded.

It loads `app.js` for display names, URL parsing and score formatting, so the two
pages cannot disagree about what `writtenandspokentrain` is called, but it does not
load `results.js`: everything it shows comes from the run's own diagnostic file.
`app.js` starts the comparison interface only on a page marked `data-ui="overview"`.

### URL state

~~~text
?lang=NL&test=spokentest&model=stanza&training=writtenandspokentrain
~~~

The same four parameters the overview already uses, so a link carries in both
directions and the back link returns to the overview with that run open. The page
validates them against `data/diagnostics/index.json` — the runs for which a file was
actually generated — rather than against a hard-coded list. An unknown or incomplete
combination shows a plain notice and a list of the runs that do exist; it is never
reported as a failure. Opened over `file://` the page says so and points at
`python3 -m http.server`, because a document with an opaque origin cannot fetch its
own data directory.

### Relationship to the CJVT comparison table

`analysis.html` is built to read as a sibling of `tables/comparison_table_v5.html`.
Ported from it: the white page head, the five metric boxes with the accent-bordered
LAS box, the controls block (filter field with its clear affordance, `↓ CSV`,
`⎘ MD`), the count toolbar (`Showing 20 / 32` plus `Show more` / `Show less`), the
20-row limit and its sticky-header expanded scroll, the dark table chrome with a
mono label column and a 70px accuracy bar, the `Merge (A⇔B)` / `Show (A→B)` toggle,
the `↳` clickable-row marker and selected-row background, the lettered A/B/C
dependency buckets with their action buttons on the heading line, and the examples
side panel (black header, LINK/CSV/MD, backdrop, pale-red token highlight,
centred dialog on narrow screens).

Deliberately different, because this page analyses one selected run rather than
switching tool and corpus:

- no two-model Compare column — the overview page is where systems are compared;
- no MULTEXT-East decoding: the XPOS tagset differs by language here, so the filter
  placeholder is taken from the run's own most frequent gold tags instead;
- no lemma confusion table — the diagnostic data carries only a total, shown as a
  statistic;
- the run identity (language, test data, system, training) occupies v5's title slot;
- system font stacks rather than IBM Plex, since this surface makes no font request.

### Sentence examples

Slovenian rows are interactive across both the score tables and the error tables:
click, Enter or Space opens a side panel
(a centred dialog below 900px) with up to 25 sentences for that exact error
pattern, the responsible token marked, and a compact gold/predicted reading under
each. Escape closes it and focus returns to the row that opened it. `‹` and `›`
step to the neighbouring row in the same table; `LINK` copies a link to the open
panel, `CSV` downloads the shown examples, `MD` copies them as a research note.

Clicking a **relation score** row shows the LAS errors on that gold relation, each
labelled with which of the three failures it is; clicking a **tag score** row shows
the tokens where that gold tag was mistagged. Both count the exact population —
`Showing 25 of 92 LAS errors` — from `gold − correct` in the aggregate table.

The panel is deep-linkable through one extra parameter: `&ex=rel.obl`,
`&ex=upos-acc.NOUN`, `&ex=dep.both_wrong.obl__to__nmod`, `&ex=upos.NOUN__to__PROPN`,
or a merged row as `&ex=upos.merged~NOUN__to__PROPN~PROPN__to__NOUN`, which also
restores the table's merged view. The pattern is named, never a sentence. A URL
without the parameter behaves exactly as before.

Examples exist only for the two Slovenian cohorts, whose corpora may be
redistributed. English and Dutch rows stay non-interactive, say so once per error
section, and make no request for an example file. Nothing is fetched until a
reader first opens a row; the run's file is then kept in memory.

`data/examples/` is generated by `am_benchmark/scripts/build_examples_data.py` and
is not part of the aggregate diagnostics, which remain text-free for every run.

### Diagnostic data

One JSON file per run under `data/diagnostics/`, plus `index.json`. The page fetches
the manifest and exactly the run it was asked for — about 12–56 KiB — so the overview
bundle stays untouched and nothing loads six runs to show one. A future two-run
comparison fetches two files through the same loader.

**The diagnostic files contain no corpus text.** Not because the page hides it: the
generator never derives it. Relations, tags, counts and confusion pairs only; lemma
errors are a single number, because gold and predicted lemmas are corpus text.
Redistribution permission has not been established for every supplied gold source,
so embedding sentences or token context in a public bundle is out of scope for this
phase. `am_benchmark/scripts/README.md` documents how the generator enforces that.

## Files

- `index.html` — page structure, no data.
- `styles.css` — house style shared with `tables/comparison_table_v5.html`:
  system sans-serif/monospace stacks, `#161616` on `#f5f5f5`, hairline rules,
  2px radius, CJVT accent `#e12a26`. No external font request is made.
- `app.js` — UMD module. Loads in Node for testing; every pure function
  (`contextValues`, `resolveContext`, `rowsFor`, `sortRows`, `bestValues`,
  `isAuthoritative`, `unavailableReason`, `parseRequest`, `label`) is exported.
- `analysis.html` / `analysis.js` — the detailed-analysis page. `analysis.js` is a
  UMD module like `app.js`; `findRun`, `requestIsComplete`, `percentage`,
  `overviewUrl`, `analysisUrl` and `renderTable` are exported for testing in Node.
- `data/results.js` — generated bundle, gitignored. Do not edit by hand.
- `data/diagnostics/` — generated per-run diagnostic set, gitignored on the same
  policy as `results.js`. Rebuild with `scripts/build_diagnostics_data.py`.
- `data/examples/` — generated Slovenian sentence examples, deploy copy only.
  Rebuild with `scripts/build_examples_data.py`.

The local source files are kept synchronized with the deployable copy under
`../../tables/am_benchmark/`; only the generated `results.js` and `data/diagnostics/`
paths differ in version-control policy. The generator writes both copies, so the
working directory runs standalone and the deployable copy is what ships.

## Indexing and publication

All interface copies retain `<meta name="robots" content="noindex,nofollow">`
while this Netlify surface remains a staging/interface-development deployment.
That directive should be reconsidered before an actual CJVT/CLARIN publication.
