# AM benchmark source resolution

Generated 2026-08-30T15:25:03+02:00. This is a read-only source-data investigation; no model evaluation was run.

## A. Executive conclusion

The 261 physical prediction files encode **80 source-named runs** and resolve to **78 canonical logical prediction runs** after Aaron's NL naming clarification. AM's `_clean` choice is available for every run, and **80/80 clean files pass** the strengthened CoNLL-U/evaluator structural gate.

**Use 78 canonical clean predictions structurally:** 36 spaCy/Stanza runs are the recommended initial-debugging subset, while 42 other structurally usable runs remain provisional because their results may change. The known NL Trankit English-content source file remains excluded, while its valid dialect-named counterpart supplies the canonical NL spoken run.

Aaron's six supplied gold files are authoritative for this handoff. All six canonical language/test cohorts are therefore gold-ready.

## B. Physical source-file inventory

A logical run is the language plus model, training condition, and test condition encoded in a filename; raw, clean, numbered, and nonstandard variants are physical representations of that run.

| Language | All regular files | `.conllu` | Logical runs | Numbered copies | `.conllu_` alternates |
|---|---:|---:|---:|---:|---:|
| EN | 53 | 49 | 24 | 1 | 4 |
| NL | 118 | 118 | 30 | 58 | 0 |
| SL | 90 | 90 | 26 | 38 | 0 |
| **Total** | **261** | **257** | **80** | **97** | **4** |

The complete one-row-per-run inventory and selection decision is in `canonical_predictions.tsv`.
The two source-name collisions created by NL normalisation are recorded in `excluded_or_ambiguous_files.tsv`; no distinct usable output was silently discarded.

## C. Duplicate and copy analysis

All **97 numbered copies** are byte-identical to their same-directory unnumbered counterparts; mismatches found: **0**. They are download/copy artifacts, not independent model runs.

Cross-language exact SHA-256 groups found: **1**.

- `e05d37ad51bb680b07ff7fbcc4cdd711d6a1bf73a1d629ca34e3796352418238`
  - `source/EN/trankit_writtenandspokentrain_spokentest.conllu`
  - `source/EN/trankit_writtenandspokentrain_spokentest_clean.conllu`
  - `source/NL/trankit_writtenandspokentrain_spokentest.conllu`
  - `source/NL/trankit_writtenandspokentrain_spokentest_clean.conllu`

Cross-language exact ID/FORM surface groups found: **1**. Surface identity is used as corroborating evidence, not as a general language detector.

## D. Raw versus clean findings

Across 80 raw/clean pairs: **47 are byte-identical**, **26 have annotation-only changes**, and **7 change sentence/token ID structure**.

The structural cleaning is concentrated in these runs:

| Language | Model | Training | Test | Changed fields |
|---|---|---|---|---|
| NL | diaparser | writtenanddialecttrain | spokentest | ID=68, HEAD=229, DEPREL=156 |
| NL | diaparser | writtentrain | spokentest | ID=68, HEAD=438, DEPREL=361 |
| NL | singletaskXPOS | writtenandspokentrain | spokentest | ID=68, HEAD=63 |
| NL | singletaskXPOSclassification | writtenandspokentrain | spokentest | ID=68, HEAD=63 |
| NL | spacy | default | spokentest | ID=68, HEAD=1011, DEPREL=962 |
| NL | stanza | default | spokentest | ID=68, HEAD=69, DEPREL=15 |
| NL | stanza | default | spokentest | ID=68, HEAD=69, DEPREL=15 |

The raw structural gate flags 33 logical raw files, while their clean counterparts pass. Raw finding counts by rule: **dependency_cycle=605, duplicate_ordinary_id=21, missing_head_target=10, ordinary_id_gap=56, root_count=1723, self_loop=69**. Cleaning therefore includes evaluator formatting, meaningful token renumbering, and dependency repair; it is not merely whitespace normalization.

## E. Selected clean predictions pass the strengthened structural gate

The gate checks UTF-8 and 10 columns; ordinary, MWT, and empty-node ID syntax (including legal `0.1`); sequential ordinary IDs; valid/non-dangling HEAD values; self-loops; longer dependency cycles; exactly one root; MWT component placement; empty-node base/order consistency; non-empty FORM values; and the final blank line required by the existing evaluator.

**Result: 80/80 unnumbered clean candidates pass with zero findings.** This establishes evaluator-oriented structural safety, not full Universal Dependencies conformance and not correctness against gold annotations.

Independent parser cross-check: the repository's existing CoNLL-U evaluator loader accepted **80/80** clean candidates. Only its load/validation path was called; no evaluation or scoring function was run.

## F. Dutch normalisation, duplicates, and invalid files

Aaron confirmed that NL `dialecttest` and `spokentest` name the same test cohort, so both are canonicalised to `spokentest`. This creates two duplicate logical keys:

- Stanza/default: the dialect- and spoken-named clean files are byte-identical; the spoken-named file is retained and the dialect-named copy is an audited exact alias.
- Trankit/written+spoken training: the spoken-named file is the known English-content invalid file; the distinct, valid Dutch dialect-named file is retained as the canonical spoken run.

- **NL / trankit / writtenandspokentrain / spokentest — EXCLUDE WRONG-LANGUAGE / CORRUPT**
  - Clean file: `source/NL/trankit_writtenandspokentrain_spokentest_clean.conllu`
  - Evidence: byte-identical to EN prediction content; sample: Are you — do they still teach at Bahia on Sunday ?
  - Opening token sample: `Are you — do they still teach at Bahia on Sunday ?`
  - Action: keep excluded under Aaron's invalid-file decision; do not repair or evaluate this file as NL.

The seven NL raw files with malformed sentence numbering are retained as immutable evidence but are superseded by structurally clean `_clean` versions. Every noncanonical physical file and its reason is listed in `excluded_or_ambiguous_files.tsv`.

## G. The four EN `.conllu_` files are unexplained alternates

None is selected. Each has a normal raw and clean counterpart, and the normal raw equals clean.

| Alternate | Equals raw/clean | Same ID structure | Differences from raw |
|---|---|---|---|
| `source/EN/stanza_writtenandspokentrain_spokentest.conllu_` | False | True | LEMMA=21 |
| `source/EN/stanza_writtenandspokentrain_writtentest.conllu_` | False | True | LEMMA=42 |
| `source/EN/stanza_writtentrain_spokentest.conllu_` | False | True | LEMMA=31 |
| `source/EN/stanza_writtentrain_writtentest.conllu_` | False | True | LEMMA=72, HEAD=1 |

Because these versions change real annotations—including a HEAD change in one file—renaming them or treating them as canonical would destroy provenance rather than resolve it.

## H. Gold-file readiness

The six files under `source/gold/` are Aaron's authoritative benchmark handoff. Existing repository gold files are retained below only for comparison.

| Candidate | Intended cohort inferred from repository docs | Sentences | Ordinary tokens | Structure matches | ID/FORM surface matches | `sent_id` matches |
|---|---|---:|---:|---:|---:|---:|
| `../data/gold/sl_ssj-ud-test.conllu` | SL writtentest (13 selected runs) | 1282 | 25442 | 13 | 13 | 8 |
| `../data/gold/sl_sst-ud-test-pog.conllu` | SL spokentest (13 selected runs) | 420 | 11443 | 0 | 0 | 0 |
| `../data/gold/sl_sst-ud-test-stan.conllu` | SL spokentest (13 selected runs) | 420 | 11443 | 0 | 0 | 0 |
| `../data/gold/sl_sst-ud-test.conllu` | SL spokentest (13 selected runs) | 432 | 11443 | 13 | 13 | 8 |
| `source/gold/en_gold_test_spoken_final_clean.conllu` | EN spokentest (12 selected runs) | 583 | 11112 | 7 | 7 | 7 |
| `source/gold/en_gold_test_written_final_clean.conllu` | EN writtentest (12 selected runs) | 881 | 17285 | 7 | 7 | 7 |
| `source/gold/nl_gold_test_spoken_final_clean.conllu` | NL spokentest (13 selected runs) | 6196 | 53069 | 6 | 6 | 6 |
| `source/gold/nl_gold_test_written_final_clean.conllu` | NL writtentest (15 selected runs) | 2357 | 40041 | 7 | 7 | 7 |
| `source/gold/sl_gold_test_spoken_final_clean.conllu` | SL spokentest (13 selected runs) | 432 | 11443 | 13 | 13 | 8 |
| `source/gold/sl_gold_test_written_final_clean.conllu` | SL writtentest (13 selected runs) | 1282 | 25442 | 13 | 13 | 8 |

The handoff itself establishes benchmark authority. Dataset identities and exact/compatible alignment evidence are recorded more fully by `build_gold_requirements.py`.

## I. Exact recommendation for what to use

1. Use the **36 selected spaCy/Stanza `_clean.conllu` files** marked `USE FOR INITIAL DEBUGGING` in `canonical_predictions.tsv` for the authoritative stable evaluation.
2. Retain the **42 other selected clean files** as structurally usable but provisional; their status is `DEFER / RESULT MAY CHANGE` pending result-stability confirmation.
3. Exclude every numbered copy, every raw file, and every `.conllu_` alternate from canonical selection.
4. Keep the English-content NL Trankit source file excluded; use its valid dialect-named counterpart for the canonical NL spoken run.
5. Use the six Aaron-supplied gold files for authoritative evaluation.

## J. Resolved decisions and remaining metadata

Gold availability, NL spoken/dialect naming, and treatment of the wrong-language Trankit file are resolved. The exact source release for EN and NL gold remains descriptive metadata rather than an evaluation blocker; the handoff files and their checksums are authoritative. The four EN `.conllu_` alternates remain excluded, and non-spaCy/Stanza families remain provisional.

### Reproducibility note

Run `python3 scripts/resolve_source.py` from `am_benchmark/`. The script reads source and gold candidates, writes only these reports, and performs no evaluation or repair.
