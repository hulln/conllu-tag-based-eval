# QA Validation Report: 20260622-0810-tk13_sl-sst-ud-test_full

- Status: **PASS**
- Modes validated: aligned
- Gold file: data/gold/sl_sst-ud-test.conllu
- Predictions root: predictions/output
- Results root: results/output/20260622-0810-tk13_sl-sst-ud-test_full
- Aligned results root: results/output/20260622-0810-tk13_sl-sst-ud-test_full/main
- Supplementary base results root: results/output/20260622-0810-tk13_sl-sst-ud-test_full/supplementary/base

## Gold Reference Counts
- Sentences (evaluator): 432
- Tokens (evaluator): 11443
- Words (evaluator): 11443
- Sentence blocks (raw split): 432
- # sent_id present: 432/432
- # text present: 432/432
- First sent_id values: ['Gos160.s150', 'Gos160.s151', 'Gos160.s153', 'Gos160.s154', 'Gos160.s155']

## Prediction File Checks
### trankit_aligned
- Path: predictions/output/20260622-0810-tk13_sl-sst-ud-test_full_trankit_aligned_predicted.conllu
- Exists: True
- Evaluator parse OK: True
- Sentences (evaluator): 432
- Tokens (evaluator): 11443
- Words (evaluator): 11443
- Sentence blocks (raw split): 432
- Malformed token rows: 0
- # sent_id present: 432/432
- # text present: 432/432
- Unique sent_id count: 432
- First sent_id values: ['Gos160.s150', 'Gos160.s151', 'Gos160.s153', 'Gos160.s154', 'Gos160.s155']
- Ends with blank line: True

### classla_aligned
- Path: predictions/output/20260622-0810-tk13_sl-sst-ud-test_full_classla_aligned_predicted.conllu
- Exists: True
- Evaluator parse OK: True
- Sentences (evaluator): 432
- Tokens (evaluator): 11443
- Words (evaluator): 11443
- Sentence blocks (raw split): 432
- Malformed token rows: 0
- # sent_id present: 432/432
- # text present: 432/432
- Unique sent_id count: 432
- First sent_id values: ['Gos160.s150', 'Gos160.s151', 'Gos160.s153', 'Gos160.s154', 'Gos160.s155']
- Ends with blank line: True

## Result File Checks
- Expected main files: 3
- Expected diagnostics files: 4
- Missing result files: 0
- Traceback-leading result files: 0

## Core Metrics (F1 from eval summaries)
### trankit_aligned
- Sentences: 100.00
- Tokens: 100.00
- Words: 100.00
- LAS: 86.86
- UAS: 89.20
- UPOS: 98.78
- XPOS: 97.43
- Lemmas: 98.71
- MLAS: 80.00

### classla_aligned
- Sentences: 100.00
- Tokens: 100.00
- Words: 100.00
- LAS: 82.08
- UAS: 85.24
- UPOS: 98.16
- XPOS: 96.75
- Lemmas: 99.23
- MLAS: 73.61

## Model-vs-Model LAS Difference Snapshot
### aligned
- Trankit aligned correct, CLASSLA aligned wrong: 975 (8.52%)
- Trankit aligned wrong, CLASSLA aligned correct: 428 (3.74%)
- Both correct: 8964 (78.34%)
- Both wrong: 1076 (9.40%)

## Failures
- None

## Warnings
- None
