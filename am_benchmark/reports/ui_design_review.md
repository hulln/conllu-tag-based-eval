# Benchmark UI design review

Assessment written before the redesign, from the running prototype and from the
repository's existing interactive tables.

## What was useful in the first prototype

- The data contract. A generated `window.AM_BENCHMARK_RESULTS` bundle with
  `dimensions`, `metrics`, and `rows` is the right shape and is kept unchanged.
- Deriving selector options from actual rows instead of a hard-coded
  cross-product. This must survive, because the benchmark is not a full
  cross-product.
- Row-driven provisional status rather than a hard-coded "Slovenian is
  provisional" string.
- Restoring state from the URL.
- Refusing to fabricate raw counts when the TSV has no count columns.

## What looked generic or artificial

- A hero title at ~54px with an uppercase red eyebrow above it. This is landing-page
  furniture, not research infrastructure.
- Five metric cards in a grid. The single most recognisable AI/SaaS dashboard
  trope, and they duplicated numbers that the table below already showed.
- A large sticky yellow warning banner with a drop shadow. It reads as an alarm.
  The provisional caveat is a permanent, ordinary property of the current data,
  not an incident.
- Redundant micro-headings — "Selection", "Selected run", "Compact comparison" —
  each wrapped in its own bordered panel with a rounded status pill in the corner.
- The vertical rhythm. On a 1440px screen the comparison table started at roughly
  y=1550. The one view that supports actual comparison was last.
- Conceptually: the page was built around *one selected run*. Four cascading
  dropdowns produced a single result, and comparison was an afterthought.

## What should become the primary interaction

The benchmark is comparative, so the comparison table is the page.

Fix a comparison context — **language** and **test data** — and show every
model × training-condition row that exists for it. One screen should answer
"does written+spoken training beat written-only for Stanza on spoken Slovenian,
and who has the best LAS?" without any navigation.

Selecting a single run stays available but becomes secondary: a row click
reveals full evaluator output underneath the table, in place, with no modal.

## Repository conventions worth retaining

`tables/comparison_table_v5.html` is the existing production interface and already
has a considered house style. Reused rather than reinvented:

- IBM Plex Sans at 13px with IBM Plex Mono for all numerals and control labels.
- Palette: `#161616` ink, `#f5f5f5` page, `#fff` surfaces, `#e0e0e0` hairlines,
  `#666` secondary text, CJVT accent `#e12a26` used sparingly.
- `border-radius: 2px` at most; hairline `0 1px 1px 0 #e0e0e0` instead of shadows.
- Solid `#161616` table header with white text — institutional, and the single
  strongest visual anchor available without adding decoration.
- Compact `4px 10px` cells, `1px solid #e0e0e0` row rules, `#fafafa` hover.
- `table-layout: fixed` so sorting never shifts columns; sticky header with
  `box-shadow: 0 1px 0 #161616`.
- `↳` marker and `#f5f5f5` background for clickable/selected rows.
- Section headings at 15px/600 with a bottom hairline, not oversized type.
- `outline: 2px solid rgba(22,22,22,0.22)` for focus-visible.

## Proposed information hierarchy

1. One compact header line: title, then provenance meta (source file, row count,
   SHA-256) as small monospace text.
2. Context controls on one line: Language, Test data. Segmented where the
   dimension has few values, a select where it has many.
3. The comparison table, immediately — grouped column headers
   (Tagging / Dependencies / Content words), sortable, best value per column in
   bold, model groups separated by a rule.
4. A single restrained provisional line directly under the table heading,
   derived from the visible rows.
5. Full evaluator output for one run, revealed below the table on row selection,
   including gold/prediction provenance and hashes.

---

# What was built

## Information architecture

Context (Language, Test data) → comparison table of every system × training run in
that context → optional detail for one selected run. The first prototype's four
cascading selectors collapsed to two, and the single-run view moved from the top of
the page to a section revealed on demand.

## The table

Nine columns: System, Training, then F1 for UPOS, XPOS, Lemmas / UAS, LAS /
MLAS, BLEX, under grouped headers named for the evaluator's own metric semantics
(Tagging, Dependencies, Content words — the last three are the content-DEPREL
metrics). Fixed layout so sorting never shifts a column; numerals right-aligned in
IBM Plex Mono with tabular figures; hairline rules; a slightly stronger rule
between model groups, suppressed while a metric sort is active.

Best value per column is bold. This is the ordinary convention in shared-task
result tables, it answers "which system has the best LAS" directly, and it is not
a heatmap: no colour is used, and a context with only one comparable row gets no
emphasis at all. Sorting is available on every header for the same reason.

The table is capped at 950px and the page column matches it, so headings, rules
and counts all align to one measure rather than stretching across the viewport.

## Status

One line under the heading, computed from the visible rows. All-provisional states
it plainly; a mixed context marks the unconfirmed runs with `†`; a fully confirmed
context removes the line. Verified against a synthetic bundle carrying confirmed EN
gold, provisional SL and NL gold, and a failed run — the warning disappeared for EN
only, and the failed run rendered its evaluator error instead of numbers.

## Deliberately not used

No metric cards, status pills, eyebrow labels, hero title, boxed panels, gradients,
shadows beyond the house hairline, or animation beyond a 0.14s control hover. The
provisional notice is a rule-and-text line, not a banner. The `↳` row affordance is
inked only on hover, focus or open, so a fully selectable table does not carry an
arrow on every row.

## Two frontend defects fixed

- `Unavailable` no longer receives a success class: the status pill is gone
  entirely, and unusable rows render through `tr.no-data` with the evaluator's own
  reason.
- `label()` now resolves through an own-property lookup, so an identifier such as
  `constructor` or `toString` returns itself instead of an inherited function.

A stray NUL byte introduced while authoring `app.js` was also found and removed;
the file is UTF-8 text again.

## Verification

- 331 browser assertions reconciling the rendered DOM against
  `reports/smoke_test/sl_spacy_stanza_results.tsv`: every comparison cell in both
  SL contexts, and all 13 metrics × 4 fields plus provenance paths and hashes for
  four representative runs. 0 failures.
- 20 Node assertions covering the two fixes, sorting, best-value selection,
  context resolution and URL parsing.
- Driven interaction check: header click and Enter sort and toggle direction, row
  Space opens and closes the detail, the segmented control switches context and
  preserves sort, Close clears the run from the URL. No console errors.
- Rendered at 1440px, 760px and 520px.

## Runtime fix: SecurityError from the History API

Reported symptom: the table rendered, then a fatal panel appeared at the foot of the
page reading *"The interface could not start: The operation is insecure."*

`writeUrl()` was the last statement of `render()`, and its
`history.replaceState(...)` call was unguarded. It is also the only call in `start()`
able to raise a `SecurityError` after painting — `location.search` is read before any
render, so a failure there would have produced an empty page instead. The exception
therefore escaped `start()` into the fatal boundary, reporting a failed startup for an
interface that had already drawn correctly. "The operation is insecure." is Gecko and
WebKit wording for `SecurityError`; Chromium phrases it differently, so the reporting
browser is Firefox or Safari, in a context whose origin is opaque — most commonly a
page opened over `file://`.

The address bar is a convenience, not part of rendering a result, so the call is now
isolated: on refusal it is disabled rather than retried on every render, the state
query is still published to `document.body.dataset.stateUrl`, and the footer states
once that links cannot be shared here. Normal HTTP behaviour is untouched — verified
that the address bar still updates on selection, opening, closing and context switch.
