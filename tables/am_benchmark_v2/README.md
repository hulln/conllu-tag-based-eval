# Benchmark interface — v2 prototype

This is a prototype of the changes from the 2026-09-25 feedback
(`am_benchmark/notes/feedback/2026-09-25-kd-table-feedback.md`). The current
interface in `../am_benchmark/` is unchanged. This version reads that
interface's data and fonts (`../am_benchmark/data/`, `../am_benchmark/fonts/`)
instead of keeping a copy.

## Run it

Serve the `tables/` directory, not this folder, so the `../am_benchmark/` paths
resolve:

~~~sh
cd tables
python3 -m http.server 8000
# http://localhost:8000/am_benchmark_v2/
# the current version, for comparison: http://localhost:8000/am_benchmark/
~~~

## What changed

| Feedback | In this version |
|---|---|
| Analysis on the same page, not a new one | Clicking a row opens its analysis in a section below the table. There is no `analysis.html`. A link to a run still works: `?lang=SL&test=spokentest&model=spacy&training=default#syntax`. |
| Remove Training data as a filter | The filter is gone. Every training setup is shown as a row, grouped by system. |
| Remove MLAS and BLEX, add feats | Columns: UPOS, XPOS, UFeats, Lemmas \| UAS, LAS. The analysis summary shows the same six values. |
| Tabs split by linguistic layer | Tabs: Morphology · Syntax · All evaluation metrics · Reproducibility. |
| Accuracy first, then errors | Both tabs have the same structure: accuracy per label (UPOS tags; relations), then an errors section with one tally line and a subsection per layer (part of speech, lemmas and features; the A/B/C error types). |
| Language-specific out | The XPOS error table is removed from the analysis. |
| All evaluation metrics shown directly | The evaluator table is no longer collapsed. |
| Compare with the other modality | Both accuracy tables have a v5-style **Compare with written/spoken** toggle (see below). |

**Compare with** works like the CJVT table (`tables/comparison_table_v5.html`):
each accuracy table has a toggle button that adds the other modality's columns
and a signed Diff column. Positive differences are in dark ink and negative
ones in red. The run being analysed has a darker bar and the other modality a
light one. There is one difference from v5. The two modalities are different
test sets, so each side shows its own gold count. For example, INTJ in
Slovenian has 580 spoken tokens but only 1 written one. A label that appears in
only one test set keeps its row, with a dash on the other side.

Switching between written and spoken test data keeps the same row open, and
the same tab.

## Interface details

- **Morphology and syntax throughout:** the overview table's column groups,
  the summary tiles and the analysis tabs all use the same two names. A reader
  interested in one layer can follow it from the table into its tab.
- **Wording:** visitors are linguists, not necessarily evaluation specialists.
  The page uses linguistic terms as they are, but spells out evaluation terms
  where they appear: a legend under the table for the metrics and the
  training setups, and a short line at the top of each layer tab. Tables say
  "Correct → predicted", "Occurrences" and "Difference". The examples panel
  names its run and says that examples follow test-set order, which is why the
  first ones often coincide across systems.
- **No repeated values:** apart from the summary tiles, a number appears once.
  Error totals are only on each tab's tally line; descriptions explain and do
  not count. The line under the run title gives only the word count. A table
  shown in full says "Showing all 16", not "16 / 16". *All evaluation metrics*
  is the exception: it is the complete evaluator output, as asked.

- **Opening and closing:** each row's action reads *Open analysis*. On the
  open row it reads *Close analysis*, and the row is highlighted. The analysis
  section also has its own *Close* button.
- **Width:** the analysis spans the same width as the table above it. Every
  row highlights on hover, so the eye can follow it from label to numbers.
  Each kind of number column (count, score with bar) keeps one width, so
  tables stacked on the page line up.
- **Row height:** every row in the overview table has the same height. Systems
  are separated by a stronger rule instead of extra padding.
- **Tab row:** on wider screens the tab row sticks to the top while a long
  panel scrolls under it, and once pinned it shows which run is open.
  Choosing a tab from further down opens that panel at its top. On a phone the
  row scrolls with the page instead.
- **Compare memory:** a table left in Compare mode stays in it when you open
  another run.
- **Reproducibility:** this tab now shows its details directly, as two
  item/value tables in the same style as the other tabs. The first covers this
  run's gold, prediction and evaluator files with their checksums. The second
  covers the benchmark result file. That second table used to sit in the
  footer under "Technical details", so the page no longer has anything to
  expand.

## Decisions made for the prototype (open questions in the feedback note)

- **Placement:** the analysis opens below the whole table, not inline under
  the clicked row.
- **XPOS:** removed only from the analysis error tables. The column stays in
  the overview table and the summary.
- **Tab navigation:** tabs replace the URL fragment instead of adding history
  entries. The table is on the same page now, so Back leaves the page instead
  of stepping through tabs.

## Lemma and feature errors, and Dutch spoken examples

The prototype shows data the current interface does not have. It is generated
into the prototype's own `data/` folder; the current interface's data is not
touched.

- **Features and lemmas:** made by `am_benchmark/scripts/build_layer_errors_v2.py`,
  into `data/layers/`, for all 36 runs. The feature table counts words whose
  universal features differ from gold, using the same word matching as the
  other error tables, and its totals match the evaluator's UFeats counts. Its
  rows list differences one feature at a time (`Case=Nom → Case=Acc`, `_` where
  one side lacks the feature). If a system predicted no features, the table
  says so.
- **Dutch spoken examples:** made by `am_benchmark/scripts/build_examples_v2.py`,
  into `data/examples/`. The page reads these together with the current
  interface's example files, so every test set has examples.
- **Rows in the feature and lemma tables** do not open example sentences.

**Before publishing:** the source corpus and licence of the Dutch spoken test
set are not confirmed (`am_benchmark/reports/testset_identification.md`). Do
not publish or push `data/examples/` or the Dutch spoken files in
`data/layers/` until they are. Rerun both scripts after the predictions or
gold change.
