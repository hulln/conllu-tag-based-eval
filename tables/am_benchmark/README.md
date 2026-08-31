# Benchmark result interface

A static, data-driven page for comparing evaluator output across systems. It reads
one generated bundle and nothing else — no CoNLL-U parsing, no metric computation,
no network calls.

This directory is the interface: there is one copy of it, and it is this one. The
generators under `am_benchmark/scripts/` write their data straight into `data/`
here, the way `build_interactive_comparison_table_v5.py` writes straight into
`tables/`. `am_benchmark/` holds the tooling, the reports and the private inputs,
and no second copy of these files.

## Run it

Generate the data from `am_benchmark/`:

~~~text
python3 scripts/build_ui_data.py
python3 scripts/build_diagnostics_data.py
python3 scripts/build_examples_data.py
~~~

Then serve this directory — `tables/` is the site root, so serving it from the
repository root reproduces the deployed paths:

~~~text
python3 -m http.server 8000 --bind 127.0.0.1 --directory tables
~~~

and open `http://127.0.0.1:8000/am_benchmark/`.

`build_ui_data.py` defaults to the 36-row authoritative spaCy/Stanza TSV. Point it
at another result file with `--input PATH_TO_RESULTS.tsv` when needed; its `--output`
is contained to this directory and `am_benchmark/`, so it cannot overwrite the
production v5 bundle. `build_diagnostics_data.py` writes the per-run diagnostic set
the analysis page reads, and never touches `data/results.js`.
`build_examples_data.py` writes the sentence-example layer, and never touches the
other two.

**Serve it over HTTP, do not open `index.html` from the file system.** A page loaded
over `file://` has an opaque origin, and Firefox and Safari refuse `history.replaceState`
there with `SecurityError: The operation is insecure.` The interface still works —
tables, sorting, selection and detail are unaffected — but it cannot update the address
bar, so links are neither shareable nor bookmarkable. When that happens the page says so
once in the footer rather than reporting a failure. The same degradation applies to any
context that blocks History API writes, such as a sandboxed preview frame.

## What the page does

The benchmark is comparative, so the comparison table is the interface. The reader
never assembles a run out of four technical dimensions; they establish a comparison
context and the table shows the systems inside it.

**Context** — three lightweight filters: Language, Test data, Training data. Each
renders as a segmented control while it has five or fewer values and falls back to
a select beyond that. Options come from rows that exist, so no combination is ever
offered without a backing row. Every value is shown under a human label — `Written`,
`Written + spoken` — and the manifest identifiers appear only in the URL, the
provenance footer and the data.

**Training data = All** is the default, because the point of the benchmark is the
experiment's structure: how a system responds to the training setup is the
comparison most of these rows exist to support.

**Comparison table, All mode** — each system is one `<tbody>` and its training runs
sit inside it, with the system named once for the whole group
(`th scope="rowgroup"`, so the name is not lost on the second and third rows). A
stronger rule separates groups.

**Comparison table, one training setup** — the Training column disappears and the
table becomes a leaderboard: one row per system, sorted by LAS descending.

Metrics are F1 for UPOS, XPOS, Lemmas (Tagging), UAS, LAS (Dependencies) and MLAS,
BLEX (Content words), grouped in the header exactly as the evaluator groups them.
Rows without a usable result show the reason instead of numbers — no value is ever
invented.

**Sorting follows the CJVT table's model.** A click on a new column sorts by it; a
click on the column already sorted reverses it; a sort is never turned off by
accident. Clearing is explicit — `Clear sort` appears beside the row count and
restores the manifest order. Enter and Space do what a click does, and focus stays
on the header afterwards.

**Sorting never breaks a group.** In All mode a metric header orders the *systems*
by their best value for that metric and leaves each system's training runs in
manifest order; the Training header reorders rows *inside* every group. In
leaderboard mode rows sort freely. Headers carry `aria-sort` and respond to Enter
and Space.

**Best value** — the highest value in each column is bold, and carries a visually
hidden "(best)" so the fact is not weight-only. No tint: a wash on as many as seven
scattered cells reads as a heatmap and implies a scale the data does not have.

**Analyse** — every row ends in an `Analyse →` link to that exact run's analysis
page. The link is the row's only tab stop; clicking anywhere else in the row follows
it too. The overview carries no expandable run detail: complete evaluator output and
provenance belong to the analysis page, so the hierarchy is table → analysis rather
than table → expanded output → analysis.

**Metric definitions** are attached to the column headings themselves: a dotted rule
under each abbreviation, and the expansion on pointer hover and on keyboard focus,
announced through `aria-describedby`. There is no separate glossary block under the
table.

**Status** — a single line above the table, derived from the rows. Every run
provisional gives one statement; a mix marks the unconfirmed runs with `†`; all rows
carrying `gold_status` `CONFIRMED` or `AUTHORITATIVE` with no benchmark-use notice
removes the line entirely. Nothing is hard-coded to a language.

**Two decimals, not one.** Rounding scores to a single decimal collapses genuinely
different values into a tie in thirteen of this bundle's context/metric combinations
— Slovenian written LAS reaches both 93.38 and 93.40 — which would make the
best-value emphasis arbitrary. Numeric cells are `tabular-nums` and right-aligned.

## URL state

~~~text
?lang=SL&test=spokentest&training=all        every training setup, grouped
?lang=SL&test=spokentest&training=default    one training setup, as a leaderboard
~~~

`language=` from the first interface version is still accepted as an alias for
`lang=`. A link from the version that opened a run's detail on this page
(`&model=stanza&training=default`) still resolves: the training filter is applied,
while the obsolete model selection is dropped because detail now lives on the
analysis page.
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

`analysis.html` is the second surface: one run, read as a short scientific report. It
deliberately does not repeat the comparison table, and it is subordinate to it — a
URL that names no run returns to the overview rather than becoming a second picker.

The run is named in the reader's words: **English · Written test data** as the
heading, **Stanza · Written + spoken training** as the subtitle, and one quiet line
of scale (gold words, aligned words, relations and tags attested). No cohort
identifier or checksum appears above the results.

Five summary metrics — UPOS, XPOS, Lemmas, UAS and LAS, with LAS in the accent —
remain above the report. Below them, the analysis and reference areas are true
in-page tabs, with exactly one shown at a time:

1. **Accuracy by category** — LAS by dependency relation, then UPOS accuracy;
2. **Dependency errors** — the three CJVT categories;
3. **Tagging errors** — UPOS and XPOS confusions, and the lemma error count;
4. **All evaluation metrics** — the complete evaluator output, all 13 metric families
   × precision, recall, F1 and aligned accuracy, collapsed by default;
5. **Reproducibility** — gold cohort and status, files, checksums and
   evaluator, collapsed by default.

The selected view is preserved in the URL hash (`#accuracy`,
`#dependency-errors`, `#tagging-errors`, `#all-metrics` or `#reproducibility`), so
it can be shared and restored with browser Back/Forward. An examples deep link
activates its required tab before revealing and opening the requested row, even if
the hash originally named a different view.

The last two moved here from the overview. Reference material sits after the
interpretive sections, and long SHA-256 strings sit behind a disclosure rather than
in front of the science.

Every table sorts by any header on click, Enter or Space. Tables longer than 20 rows
open truncated with a control that names how many rows are folded.

It loads `app.js` for display names, the metric vocabulary, URL parsing and score
formatting, so the two pages cannot disagree about what `writtenandspokentrain` is
called. It also loads `data/results.js` — the same bundle the overview reads — for
the complete evaluator table, so a number can never differ between the two surfaces;
the error and accuracy breakdowns still come from the run's own diagnostic file.
`app.js` starts the comparison interface only on a page marked `data-ui="overview"`.

### Visual system

The interface has its own visual language; it is no longer styled as a sibling of
`tables/comparison_table_v5.html`. Tokens live at the top of `styles.css`.

**Colour.** A warm off-white page (`#f7f7f4`) with white surfaces, near-black text
(`#17191d`, 16.4:1) and one muted grey for secondary text (`#626a73`, 5.1:1). One
accent — a desaturated ink blue, `#315b7d`, 7.2:1 on white — used only where it
carries meaning: the selected control, links, focus, the active sort, the current
section tab, the `A.`/`B.`/`C.` letters that index the dependency categories, the LAS
header and summary value, and the selected error row. Section headings themselves stay
charcoal — a heading is not a link, and the marker beside it carries the structure. There is no second accent and no metric
colour-coding: the best value in a column is marked by weight alone. Ordinary model
errors are data, not UI errors, so nothing in the error tables is red; the one warm
colour, `#8a5a17`, is reserved for the provisional-gold flag. A third grey,
`#89919a`, exists for separator dots only — it is decoration, never text.

**Type: two faces, three roles.** The split is deliberate — the interface is set in a
humanist sans, the material it presents is not. A relation name and a corpus sentence
are objects of study; setting them in the page's own voice would make them read as
prose about the data rather than as the data.

`--font-ui` is **IBM Plex Sans**, self-hosted from `fonts/` in three weights: Regular
for text, Medium for headings and the summary metrics, SemiBold for the two small
uppercase label roles. Nothing is fetched from a third party, so the page loads
identically offline and makes no external request; the files are subset to Latin plus
the punctuation and marks the interface uses, 24–25 kB each, with `font-display: swap`
and `"Segoe UI", Arial, sans-serif` behind them. One stylistic set is kept and enabled
on `body`, `font-feature-settings: "ss02" 1` — Plex's single-storey `g`. ss01 and
ss03–ss05 are subset out so they cannot be switched on by accident. Plex's figures are
tabular by construction — every digit advances 600/1000 em — so score columns align on
the glyph metrics; `font-variant-numeric: tabular-nums lining-nums` is declared for the
fallback faces.

`--font-data` is the reader's own monospace, used for the technical register the page
quotes rather than speaks: all values in the Detailed analysis tables, including
relations, tagset labels, error pairs, counts and scores. In the examples panel only
the compact sentence metadata uses this technical face; the corpus sentence and its
annotation values retain the interface sans. `--font-mono` is the same stack under a
second name, for checksums,
paths and filenames — where the reason is character-by-character comparison rather than
a change of register. There is no third face. The overview comparison table stays in
`--font-ui`: its columns are scores, and Plex already sets them tabular.

**Weight is scarce.** 400 for everything ordinary, including every table value, system
name, tagset label and corpus sentence; 500 for headings, the summary metrics, table
headers and counts; 600 only for the small uppercase labels and the best value in an
overview column. Nothing is 700, and no weight is synthesised. Scale: h1 34px/40,
page-head h1 30px/36, h2 22–23px/29–30, h3 17px/24, body 15px/22.8, overview tables
14px/19.6, Detailed analysis tables 12.5px/18, analysis table headers 12px/16,
corpus sentences 14px/22, metadata 11.5–13px, uppercase labels 11.5px/600 at 0.05em.

**Structure.** 1px rules, whitespace and a 4/8/12/16/24/32/48/64 spacing scale do the
work. No shadows, no floating cards, no gradients; radii are 4px on controls and 6px
on panels, and tables have none. The page is capped at 1320px (1120px on the analysis
page, which is prose-shaped). Short interface explanations use the table/content
field; genuinely long prose is capped at roughly 108 characters for readability.

**Tables** are the product. Both pages keep horizontal rules only, precise numeric
alignment and hover only where a row is actionable, but their jobs differ. The
overview retains a light two-row grouped header and humanist-sans values for its
publication-style comparison. Detailed analysis uses a deep-blue technical header,
regular-weight monospace values and compact ~30px rows. Any aggregate row that can
open sentence evidence carries CJVT's small `↳` branch marker; non-interactive score
rows do not.

**One edge outside a table.** Every section-level element — headings, notes, counts,
tallies, availability notes and the filter/export toolbar — starts and ends on the
table field's own edge. Cells keep their internal padding, so the column text sits
one cell-padding inside that line. Prose is never aligned to the first cell's inset.

Retained from the CJVT table because they work: the controls block (filter field with
its clear affordance, `↓ CSV`, `⎘ MD`), the count toolbar with `Show more` /
`Show less` and its sticky-header expanded scroll, the `Merge (A⇔B)` toggle, the `↳`
clickable-row marker, the lettered A/B/C dependency buckets, and the examples side
panel as a concept. Deliberately different:

- no two-model Compare column — the overview page is where systems are compared;
- no MULTEXT-East decoding: the XPOS tagset differs by language here, so the filter
  placeholder is taken from the run's own most frequent gold tags instead;
- no lemma confusion table — the diagnostic data carries only a total;
- the examples panel is corpus evidence rather than a developer inspector: a white
  sheet, the sentence at 15.5px as the largest thing in it, one pale amber token
  highlight instead of red, and the annotations under it as quiet metadata.

### Responsive and accessible

Desktop-first, but a phone gets the whole benchmark rather than a reduced one. Above
1000px the full metric table is visible. Below that it scrolls horizontally inside
its wrap — never converted to cards, because a benchmark row only means something as
a row — with **both** label columns pinned, since a score whose system or training
setup has scrolled away is unreadable. No metric is ever hidden. The analysis page's
summary metrics wrap 5 → 3 → 2, and the examples panel becomes a full-width sheet
below 900px.

The wrap sets `contain: paint`: without it Chromium counts the table's full width
towards the root scroll area and the whole page pans sideways on a phone even though
the wrap clips correctly.

Accessibility is part of the design: semantic tables with `th scope` (including
`scope="rowgroup"` for the grouped systems), `aria-sort` on sortable headers,
segmented controls as buttons exposing `aria-pressed`, a visible 2px focus ring on
everything focusable, ≥38px control targets, the "(best)" fact given as text and not
only as weight, `prefers-reduced-motion` honoured, and the examples dialog trapping
Tab, closing on Escape and returning focus to the row that opened it.

### Sentence examples

Rows are interactive across both the score tables and the error tables wherever the
run has an example file: click, Enter or Space opens a side panel
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

**Which runs have examples is decided by the generated manifest, not by the page.**
`data/examples/index.json` lists the runs a file was written for, the attribution for
each cohort, and the reason each withheld cohort has none; the page reads it once and
keeps no allowlist of its own, so the two cannot drift. A run absent from the manifest
stays non-interactive, states the recorded reason once per error section, and makes no
request for an example file. Nothing is fetched until a reader first opens a row; the
run's file is then kept in memory. A copy served without a `data/examples/` directory
behaves exactly like a run with no examples.

Examples currently exist for 30 of the 36 runs — every English run, the six Dutch
written runs and every Slovenian run. The six Dutch *spoken* runs have none, because
that cohort's corpus is not identified with enough confidence to establish
redistribution rights; the panel's absence is explained in place rather than left
blank. The allowlist and the licences are in `am_benchmark/scripts/README.md`.

A cohort can come from more than one treebank — Dutch written is the UD Dutch
LassySmall test split followed by the UD Dutch Alpino test split — so the panel
renders the attribution from `source.parts` and names every corpus, its portion of
the split, the release and the licence.

`data/examples/` is generated by `am_benchmark/scripts/build_examples_data.py` and
is not part of the aggregate diagnostics, which remain text-free for every run.

### Diagnostic data

One JSON file per run under `data/diagnostics/`, plus `index.json`. The page fetches
the manifest and exactly the run it was asked for — about 12–56 KiB — so the overview
bundle stays untouched and nothing loads six runs to show one. A future two-run
comparison fetches two files through the same loader.

**The diagnostic files contain no corpus text.** Not because the page hides it: the
generator never derives it. Relations, tags, counts and confusion pairs only; lemma
errors are a single number, because gold and predicted lemmas are corpus text. That
holds for every run, including the ones that do have sentence examples: text lives
only in the separate `data/examples/` layer, which is written per cohort under an
explicit licensing allowlist. `am_benchmark/scripts/README.md` documents how each
generator enforces its half of that.

## Files

- `index.html` — page structure, no data.

**Asset references carry a `?v=` query.** `index.html` and `app.js` are separate
files that a browser caches independently, so without it a reader can end up running
one version's script against another version's markup — which fails as an opaque
null reference deep inside rendering. Bump the number in both HTML files whenever the
markup/script contract changes (currently `v=3`). As a net under that, each page checks up front that
the elements its script requires are present and, if not, names them and says to
hard-reload rather than failing obscurely.

- `styles.css` — the design system for both pages: tokens at the top, then the
  shared table treatment. See **Visual system** above. No external font is fetched.
- `fonts/` — IBM Plex Sans Regular, Medium and SemiBold as subset WOFF2, plus the SIL
  Open Font License they ship under. Referenced only by `styles.css`.
- `app.js` — UMD module. Loads in Node for testing; every pure function
  (`contextValues`, `resolveContext`, `rowsFor`, `sortRows`, `sortGroups`,
  `groupRows`, `bestValues`, `contextTitle`, `countSummary`, `analysisUrl`,
  `isAuthoritative`, `unavailableReason`, `parseRequest`, `label`) is exported. It
  also owns the shared vocabulary the analysis page reuses: `LABELS`,
  `METRIC_DESCRIPTIONS`, `METRIC_LAYERS` and the score/count field lists.
- `analysis.html` / `analysis.js` — the detailed-analysis page. `analysis.js` is a
  UMD module like `app.js`; `findRun`, `requestIsComplete`, `percentage`,
  `overviewUrl`, `exampleCatalogue`, `sourceText` and `renderTable` are exported for
  testing in Node.
- `data/results.js` — generated result bundle. Rebuild with
  `am_benchmark/scripts/build_ui_data.py`; do not edit by hand.
- `data/diagnostics/` — generated per-run diagnostic set, 36 runs plus `index.json`.
  Rebuild with `am_benchmark/scripts/build_diagnostics_data.py`.
- `data/examples/` — generated sentence examples for the redistributable cohorts,
  30 runs plus `index.json`. Rebuild with
  `am_benchmark/scripts/build_examples_data.py`.

Everything under `data/` is generated and committed, because this directory is what
ships: `tables/` is the deployed site root. Rebuilding is reproducible — each
generator writes byte-identical output from the same inputs — so a regenerated file
that shows up as modified means an input changed, and is worth reading before it is
committed.

## Indexing and publication

All interface copies retain `<meta name="robots" content="noindex,nofollow">`
while this Netlify surface remains a staging/interface-development deployment.
That directive should be reconsidered before an actual CJVT/CLARIN publication.
