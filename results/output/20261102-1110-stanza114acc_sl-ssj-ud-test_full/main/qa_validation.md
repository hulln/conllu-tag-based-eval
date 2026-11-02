# QA Validation Report: 20261102-1110-stanza114acc_sl-ssj-ud-test_full

- Status: **PASS**
- System: stanza
- Modes validated: aligned
- Gold file: data/gold/sl_ssj-ud-test.conllu
- Predictions root: predictions/output
- Results root: results/output/20261102-1110-stanza114acc_sl-ssj-ud-test_full
- Validator: scripts/qa_validate_system_run.py (check functions from scripts/qa_validate_run.py)

## Gold Reference Counts
- Sentences (evaluator): 1282
- Tokens (evaluator): 25442
- Words (evaluator): 25442
- Sentence blocks (raw split): 1282
- # sent_id present: 1282/1282
- # text present: 1282/1282
- First sent_id values: ['ssj562.2919.10333', 'ssj562.2919.10334', 'ssj562.2919.10335', 'ssj562.2919.10336', 'ssj562.2920.10337']

## Prediction File Checks
### stanza_aligned
- Path: predictions/output/20261102-1110-stanza114acc_sl-ssj-ud-test_full_stanza_aligned_predicted.conllu
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

## Tree Structure Checks
- sentences: 1282
- gold_sentences: 1282
- multiple_roots: 0
- no_root: 0
- cycles: 0
- head_out_of_range: 0
- head_not_integer: 0
- root_label_mismatch: 0
- id_mismatch: 0
- form_mismatch: 0
- length_mismatch: 0
- blocking_problems: 0

## Result File Checks
- Expected files: 3
- Missing result files: 0
- Traceback-leading result files: 0

## Core Metrics (F1 from eval summary)
### stanza_aligned
- Sentences: 100.00
- Tokens: 100.00
- Words: 100.00
- LAS: 94.86
- UAS: 95.98
- UPOS: 99.14
- XPOS: 97.98
- Lemmas: 98.89
- MLAS: 90.49

## Failures
- None

## Warnings
- None
