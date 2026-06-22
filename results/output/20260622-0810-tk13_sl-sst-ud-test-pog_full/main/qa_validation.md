# QA Validation Report: 20260622-0810-tk13_sl-sst-ud-test-pog_full

- Status: **PASS**
- Modes validated: aligned
- Gold file: data/gold/sl_sst-ud-test-pog.conllu
- Predictions root: predictions/output
- Results root: results/output/20260622-0810-tk13_sl-sst-ud-test-pog_full
- Aligned results root: results/output/20260622-0810-tk13_sl-sst-ud-test-pog_full/main
- Supplementary base results root: results/output/20260622-0810-tk13_sl-sst-ud-test-pog_full/supplementary/base

## Gold Reference Counts
- Sentences (evaluator): 420
- Tokens (evaluator): 11443
- Words (evaluator): 11443
- Sentence blocks (raw split): 420
- # sent_id present: 420/420
- # text present: 420/420
- First sent_id values: ['Gos160.s150', 'Gos160.s151', 'Gos160.s153', 'Gos160.s154', 'Gos160.s155']

## Prediction File Checks
### trankit_aligned
- Path: predictions/output/20260622-0810-tk13_sl-sst-ud-test-pog_full_trankit_aligned_predicted.conllu
- Exists: True
- Evaluator parse OK: True
- Sentences (evaluator): 420
- Tokens (evaluator): 11443
- Words (evaluator): 11443
- Sentence blocks (raw split): 420
- Malformed token rows: 0
- # sent_id present: 420/420
- # text present: 420/420
- Unique sent_id count: 420
- First sent_id values: ['Gos160.s150', 'Gos160.s151', 'Gos160.s153', 'Gos160.s154', 'Gos160.s155']
- Ends with blank line: True

### classla_aligned
- Path: predictions/output/20260622-0810-tk13_sl-sst-ud-test-pog_full_classla_aligned_predicted.conllu
- Exists: True
- Evaluator parse OK: True
- Sentences (evaluator): 420
- Tokens (evaluator): 11443
- Words (evaluator): 11443
- Sentence blocks (raw split): 420
- Malformed token rows: 0
- # sent_id present: 420/420
- # text present: 420/420
- Unique sent_id count: 420
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
- LAS: 83.76
- UAS: 86.45
- UPOS: 97.88
- XPOS: 95.58
- Lemmas: 95.84
- MLAS: 74.62

### classla_aligned
- Sentences: 100.00
- Tokens: 100.00
- Words: 100.00
- LAS: 73.96
- UAS: 78.97
- UPOS: 93.25
- XPOS: 89.66
- Lemmas: 89.38
- MLAS: 61.04

## Model-vs-Model LAS Difference Snapshot
### aligned
- Trankit aligned correct, CLASSLA aligned wrong: 1652 (14.44%)
- Trankit aligned wrong, CLASSLA aligned correct: 530 (4.63%)
- Both correct: 7933 (69.33%)
- Both wrong: 1328 (11.61%)

## Failures
- None

## Warnings
- None
