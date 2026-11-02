# QA Validation Report: 20261102-1110-stanza114acc_sl-sst-ud-test-pog_full

- Status: **PASS**
- System: stanza
- Modes validated: aligned
- Gold file: data/gold/sl_sst-ud-test-pog.conllu
- Predictions root: predictions/output
- Results root: results/output/20261102-1110-stanza114acc_sl-sst-ud-test-pog_full
- Validator: scripts/qa_validate_system_run.py (check functions from scripts/qa_validate_run.py)

## Gold Reference Counts
- Sentences (evaluator): 420
- Tokens (evaluator): 11443
- Words (evaluator): 11443
- Sentence blocks (raw split): 420
- # sent_id present: 420/420
- # text present: 420/420
- First sent_id values: ['Gos160.s150', 'Gos160.s151', 'Gos160.s153', 'Gos160.s154', 'Gos160.s155']

## Prediction File Checks
### stanza_aligned
- Path: predictions/output/20261102-1110-stanza114acc_sl-sst-ud-test-pog_full_stanza_aligned_predicted.conllu
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

## Tree Structure Checks
- sentences: 420
- gold_sentences: 420
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
- LAS: 80.48
- UAS: 84.82
- UPOS: 94.24
- XPOS: 91.04
- Lemmas: 90.45
- MLAS: 67.94

## Failures
- None

## Warnings
- None
