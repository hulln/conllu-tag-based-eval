# QA Validation Report: 20260409-2248_sl-ssj-ud-test_full

- Status: **PASS**
- Gold file: data/gold/sl_ssj-ud-test.conllu
- Predictions root: predictions/runs
- Results root: results/runs/20260409-2248_sl-ssj-ud-test_full

## Prediction File Checks
### classla_aligned
- Path: predictions/runs/20260409-2248_sl-ssj-ud-test_full_classla_aligned_predicted.conllu
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
- First sent_id values: ['1', '2', '3', '4', '5']
- Ends with blank line: True

### classla_base
- Path: predictions/runs/20260409-2248_sl-ssj-ud-test_full_classla_base_predicted.conllu
- Exists: True
- Evaluator parse OK: True
- Sentences (evaluator): 1287
- Tokens (evaluator): 25448
- Words (evaluator): 25448
- Sentence blocks (raw split): 1287
- Malformed token rows: 0
- # sent_id present: 1287/1287
- # text present: 1287/1287
- Unique sent_id count: 1287
- First sent_id values: ['1', '2', '3', '4', '5']
- Ends with blank line: True

### trankit_aligned
- Path: predictions/runs/20260409-2248_sl-ssj-ud-test_full_trankit_aligned_predicted.conllu
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
- First sent_id values: ['1', '2', '3', '4', '5']
- Ends with blank line: True

### trankit_base
- Path: predictions/runs/20260409-2248_sl-ssj-ud-test_full_trankit_base_predicted.conllu
- Exists: True
- Evaluator parse OK: True
- Sentences (evaluator): 1291
- Tokens (evaluator): 25434
- Words (evaluator): 25434
- Sentence blocks (raw split): 1291
- Malformed token rows: 0
- # sent_id present: 1291/1291
- # text present: 1291/1291
- Unique sent_id count: 1291
- First sent_id values: ['1', '2', '3', '4', '5']
- Ends with blank line: True

## Result File Checks
- Expected main files: 6
- Expected diagnostics files: 8
- Missing result files: 0
- Traceback-leading result files: 0

## Core Metrics (F1 from eval summaries)
### classla_aligned
- LAS: 90.48
- UAS: 92.12
- UPOS: 98.60
- XPOS: 97.08
- Lemmas: 98.94
- MLAS: 84.99

### trankit_aligned
- LAS: 91.07
- UAS: 92.98
- UPOS: 98.81
- XPOS: 96.52
- Lemmas: 97.41
- MLAS: 83.83

### classla_base
- LAS: 90.39
- UAS: 92.02
- UPOS: 98.52
- XPOS: 97.01
- Lemmas: 98.87
- MLAS: 84.91

### trankit_base
- LAS: 90.90
- UAS: 92.78
- UPOS: 98.67
- XPOS: 96.40
- Lemmas: 97.27
- MLAS: 83.70

## Model-vs-Model LAS Difference Snapshot
### aligned
- CLASSLA aligned correct, Trankit aligned wrong: 1195 (4.70%)
- Trankit aligned correct, CLASSLA aligned wrong: 1345 (5.29%)
- Both correct: 21826 (85.79%)
- Both wrong: 1076 (4.23%)

### base
- CLASSLA base correct, Trankit base wrong: 1085 (4.45%)
- Trankit base correct, CLASSLA base wrong: 1292 (5.30%)
- Both correct: 20990 (86.15%)
- Both wrong: 997 (4.09%)

## Failures
- None

## Warnings
- None
