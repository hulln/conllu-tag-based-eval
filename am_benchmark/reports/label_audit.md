# Label audit: spaCy scores that do not measure what they claim

Audit of 2026-09-26. Rerun with `python3 am_benchmark/scripts/audit_labels.py`.
It reads the files only and modifies nothing.

## Summary

23 of the 78 usable prediction runs contain labels that the evaluator cannot
match against gold. 18 of them are spaCy runs shown in the current benchmark
table. All 12 Stanza runs are clean. The evaluator is not at fault: it compares
labels as exact strings, as the official CoNLL 2018 script does. The problem is
in the supplied prediction files, and no step before the evaluation checked for
it.

The same numbers appear in KD's reference Table 3 (written test set). Our table
matches it exactly (`kd_written_table_crosscheck.md`, 30/30), so the issue
predates this repository's pipeline and may affect that table as well.

## Findings

### 1. spaCy default: root relation written as `ROOT` (6 runs, all shown)

The pretrained spaCy pipelines label the root `ROOT`; UD and all six gold files
use `root`. Every root attachment therefore scores as a wrong label. This lowers
LAS, CLAS, MLAS and BLEX, and shows `root` at 0.00 LAS in the per-relation
table. UAS is unaffected, because it compares heads only.

Re-evaluated with the unchanged evaluator, on temporary copies where only
`ROOT` was changed to `root`:

| Run | LAS as published | LAS with `root` | Difference |
|---|---:|---:|---:|
| NL spoken | 53.08 | 61.42 | +8.34 |
| NL written | 77.56 | 82.95 | +5.39 |
| SL written | 88.06 | 92.81 | +4.75 |
| SL spoken | 71.51 | 74.37 | +2.86 |
| EN written | 37.92 | 41.72 | +3.80 |
| EN spoken | 38.17 | 41.99 | +3.82 |

The top system in each context does not change. spaCy default in SL written
moves from 6th to 4th of 6 by LAS.

### 2. spaCy default, English: not a UD label scheme at all (2 runs, shown)

The English pipeline is trained on OntoNotes with ClearNLP dependency labels:
`prep`, `pobj`, `dobj`, `poss`, `relcl`, `attr`, `nsubjpass` and others. 36–39%
of words carry a label that does not exist in UD. The scheme also attaches
words differently, for example a preposition heads its noun, where UD does the
reverse. English spaCy default LAS and UAS (about 38 and 56) are therefore not
comparable with any other row. Fixing the case of `root` does not repair this.

### 3. spaCy trained on written / written+spoken: no features predicted (12 runs, shown)

FEATS is `_` on 100% of words in every EN, NL and SL run trained on written or
written+spoken data. The pipelines evidently had no morphologizer, or its
output was not written out. The UFeats and AllTags scores for these runs (for
example 24.5 in SL written, and 38.86 in SL spoken) are the share of gold words
that happen to have no features. They say nothing about feature prediction.
MLAS is affected in the same way.

### 4. Provisional runs (not shown yet)

- **NL Trankit** (1, 2 and 50 epochs, written+spoken training): LEMMA is empty
  on 100% of words.
- **NL Trankit 50 epochs:** DEPREL is `_` on 1.6–2.6% of words.
- **NL Trankit 2 epochs, written test:** FEATS is empty on 64% of words
  (gold: 42%).

These need the same treatment before they are promoted to the stable subset.

### 5. Dutch gold: spoken and written use different feature conventions

This came up in the per-feature error table of the v2 prototype
(`build_layer_errors_v2.py`). The two Dutch gold files do not annotate the
same features:

| Gold file | Words | `Mood=Ind` | `PronType=Art` |
|---|---:|---:|---:|
| NL written | 40,041 | 0 | 0 |
| NL spoken | 53,069 | 6,275 | 2,861 |

A model trained on the written conventions never predicts these two features.
Stanza default predicts `Mood=Ind` on 4 words of the spoken test set and
`PronType=Art` on none. So for Dutch spoken, the UFeats scores (and the
written-vs-spoken gap) partly measure this annotation difference, not
feature tagging. This is a question about the gold data, not the
predictions. Other features and other layers were not compared between the
two gold files.

## How it came about

1. **Supplied files:** the prediction files are the systems' raw output. spaCy
   writes its own conventions (`ROOT`; ClearNLP labels for English), and the
   custom spaCy pipelines did not output features.
2. **Evaluator:** the CoNLL 2018 script scores exact label strings by design.
   It raises no error for a label it has never seen; the word simply counts as
   wrong.
3. **Our checks:** the source audit (`audit_source.py`) and the gold
   compatibility checks verify structure: columns, token IDs, HEADs, sentence
   spans and text. They never compared label vocabularies with gold. So these
   runs passed as "structurally usable" and were scored as "authoritative".
   That label describes the gold, not the predictions.
4. **Cross-check:** the cross-check with KD's table confirmed that we reproduce
   the upstream numbers. Because both sides share the error, the agreement
   looked like validation.

## Where the affected numbers are visible

- `tables/am_benchmark/` and its data bundle. These are committed to the
  **public** GitHub repository `hulln/conllu-tag-based-eval`.
- The v2 prototype (`tables/am_benchmark_v2/`). It reads the same bundle and
  shows UFeats in the overview table, so finding 3 is prominent there.
- KD's Table 3, and probably the corresponding spoken table.

## Decisions needed

- **spaCy default, `ROOT`:** change it to `root` before evaluating (a spelling
  difference of the same relation), rerun, and rebuild the UI data? Or keep the
  raw output and say so beside the scores?
- **spaCy default, English:** exclude its dependency scores, mark them as not
  comparable, or map ClearNLP labels to UD? A mapping is lossy and does not fix
  the head conventions.
- **spaCy written / written+spoken:** show UFeats, AllTags and MLAS as "not
  predicted" instead of a number, or ask Aaron whether features exist elsewhere?
- **KD and Aaron:** tell them, because the same numbers are in their table.
- **Pipeline:** add `audit_labels.py` to the preparation steps, so a run with
  flagged labels cannot become authoritative without a decision.
