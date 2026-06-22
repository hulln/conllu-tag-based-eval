# QA Validation Report: 20260622-0810-tk13_sl-ssj-ud-test_full

- Status: **PASS**
- Modes validated: aligned
- Gold file: data/gold/sl_ssj-ud-test.conllu
- Predictions root: predictions/output
- Results root: results/output/20260622-0810-tk13_sl-ssj-ud-test_full
- Aligned results root: results/output/20260622-0810-tk13_sl-ssj-ud-test_full/main
- Supplementary base results root: results/output/20260622-0810-tk13_sl-ssj-ud-test_full/supplementary/base

## Gold Reference Counts
- Sentences (evaluator): 1282
- Tokens (evaluator): 25442
- Words (evaluator): 25442
- Sentence blocks (raw split): 1282
- # sent_id present: 1282/1282
- # text present: 1282/1282
- First sent_id values: ['ssj562.2919.10333', 'ssj562.2919.10334', 'ssj562.2919.10335', 'ssj562.2919.10336', 'ssj562.2920.10337']

## Prediction File Checks
### trankit_aligned
- Path: predictions/output/20260622-0810-tk13_sl-ssj-ud-test_full_trankit_aligned_predicted.conllu
- Exists: True
- Evaluator parse OK: True
- Sentences (evaluator): 1282
- Tokens (evaluator): 25442
- Words (evaluator): 25442
- Sentence blocks (raw split): 1282
- Malformed token rows: 0
- # sent_id present: 1282/1282
- # text present: 1282/1282
- Unique sent_id count: 1282
- First sent_id values: ['ssj562.2919.10333', 'ssj562.2919.10334', 'ssj562.2919.10335', 'ssj562.2919.10336', 'ssj562.2920.10337']
- Ends with blank line: True

### classla_aligned
- Path: predictions/output/20260622-0810-tk13_sl-ssj-ud-test_full_classla_aligned_predicted.conllu
- Exists: True
- Evaluator parse OK: True
- Sentences (evaluator): 1282
- Tokens (evaluator): 25442
- Words (evaluator): 25442
- Sentence blocks (raw split): 1282
- Malformed token rows: 0
- # sent_id present: 1282/1282
- # text present: 1282/1282
- Unique sent_id count: 1282
- First sent_id values: ['ssj562.2919.10333', 'ssj562.2919.10334', 'ssj562.2919.10335', 'ssj562.2919.10336', 'ssj562.2920.10337']
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
- LAS: 94.48
- UAS: 95.72
- UPOS: 98.99
- XPOS: 97.43
- Lemmas: 97.95
- MLAS: 89.18

### classla_aligned
- Sentences: 100.00
- Tokens: 100.00
- Words: 100.00
- LAS: 90.48
- UAS: 92.12
- UPOS: 98.60
- XPOS: 97.08
- Lemmas: 98.94
- MLAS: 84.99

## Model-vs-Model LAS Difference Snapshot
### aligned
- Trankit aligned correct, CLASSLA aligned wrong: 1543 (6.06%)
- Trankit aligned wrong, CLASSLA aligned correct: 527 (2.07%)
- Both correct: 22494 (88.41%)
- Both wrong: 878 (3.45%)

## Failures
- None

## Warnings
- None
