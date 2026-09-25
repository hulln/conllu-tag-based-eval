# Benchmark table feedback — KD, 2026-09-25

Feedback on the multilingual benchmark UI in `tables/am_benchmark/`: the
overview table (`index.html`) and the detailed analysis (`analysis.html`).

A first prototype of these changes is in `tables/am_benchmark_v2/` (see its
README).

## Summary

Make the table smaller and organise the analysis by linguistic layer:

- The overview table gets fewer controls and columns.
- The analysis opens below the table instead of on a separate page.
- The analysis tabs are grouped by layer (morphology, syntax). Each tab shows
  accuracy first, then errors.
- A run can be compared with the same run on the other test modality.

## Overview table

- **Remove the Training data selector.** Training condition stays visible in
  the rows, but it is no longer a filter.
- **Remove MLAS and BLEX.** This drops the whole "Content words" column group.
- **Add UFeats** (morphological features) to the Tagging group. Resulting
  columns: UPOS, XPOS, UFeats, Lemmas | UAS, LAS.
- **Expect about 4 tools in the final benchmark.** The current source has 12
  system names, counting the Trankit epoch variants separately. The final table
  will be much smaller.

## Detailed analysis

### Placement

Open the analysis on the same page, in a section that expands below the table.
Don't navigate to a separate `analysis.html` page.

### Tabs by linguistic layer

The current tabs split by kind of number (accuracy vs. errors). The new tabs
split by layer, and each layer tab follows the same order: accuracy per
label first, then errors.

| Current tab | Proposed tab |
|---|---|
| Accuracy by category, POS part | **Morphology** |
| Tagging errors | **Morphology** |
| Accuracy by category, relation part | **Syntax** |
| Dependency errors | **Syntax** |
| All evaluation metrics | **Evaluation** |
| Reproducibility | **Reproducibility** (unchanged) |

**Morphology**

1. Accuracy per UPOS tag (the current "Part-of-speech tag scores" table).
2. Most frequent errors for UPOS, lemmas and features. Features possibly later.

**Syntax**

1. LAS per dependency relation (the current "Dependency relation scores"
   table).
2. The three error types: A. wrong head and relation, B. wrong relation only,
   C. wrong head only.

**Language-specific (XPOS) errors: remove** from the analysis.

**Evaluation:** show the full evaluator table directly, not collapsed behind
"Show the full evaluator table".

### Compare with

When analysing a specific run, offer a "compare with" option. It always
compares with the same row (same system and training condition) on the other
test modality, written ↔ spoken. There are no other comparison targets.

The display should follow the CJVT table (`tables/comparison_table_v5.html`,
`makeAccTable`):

- Each accuracy table (LAS per relation, accuracy per UPOS tag) gets a
  "Compare with …" toggle button. Here it would read e.g. "Compare with
  spoken".
- Off (default): Label | Gold count | score.
- On: Label | Gold count | this run | other modality | Diff. Diff is this run
  minus the other modality, signed and coloured. Each score has its own bar,
  rows are shaded by which side is better, and the note under the table
  states what the difference means.
- Error tables have no compare mode in v5.

## Implementation notes

- **Lemma error table conflicts with the current data policy.**
  `build_diagnostics_data.py` deliberately reduces lemmas to a single error
  count, because gold/predicted lemma pairs are corpus text. That matters most
  for test sets whose redistribution rights are not established. Before
  building this table, decide whether to show lemma pairs, show them only for
  some test sets, or keep counts only.
- **Feature error pairs are labels** (e.g. `Case=Nom → Case=Acc`), so they
  don't raise the same problem. The diagnostics script doesn't produce them yet.
- **Compare with** assumes the other modality exists for that run. Check this
  for every remaining run once the 4 final tools are fixed.

## Open questions

- **Placement:** does the analysis open below the whole table, or expand inline
  under the clicked row? Should a direct link to a run's analysis still work?
- **Training data:** with the selector gone, are all training conditions always
  shown, grouped by system? Or does each tool end up with one condition?
- **Tools:** which 4 tools are in the final benchmark?
- **XPOS:** does "remove language-specific" apply only to the XPOS error table
  in the analysis? Or also to the XPOS column in the overview and the analysis
  summary?
- **"Maybe later":** does it cover only features, or lemmas as well?

## Original notes (verbatim)

> Analyse – ne bi v novi strani, ampak na isti strani, spodaj da bi se odprla tabela
> Training data odstraniti kot izbiro
>
> 4 orodja skupno bodo na koncu verjetno
>
> V tabeli odstraniti mlax in blex
> Dodati feats v tabelo
>
> Poenostaviti, semantično delitev tabov
> Tagging, dependencies morphology, syntax, eval, repro
> Logika: prvi del natančnost po oznakah, potem pa napake
> Najprej natančnost po kategorijah, to kar je zdaj acc in pos, potem naj napake, spodaj pa še tabelo najpogostejših napak za pos, leme in feats (morda kasneje)
> Pod syntax ista logika: natančnost po relacijah in potem te 3 najpogostejši tipi napak
> Lang specific dajmo kar ven
> All evaluarion naj se kar pokaže
>
> Možnost compare with – vedno samo druga modalnost (ista vrstica samo na drugi modalnosti), pri analizi konkretnih rezultatov
