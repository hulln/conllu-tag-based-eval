# predictions/

Generated model outputs in CoNLL-U format.

- [output](output/): canonical public aligned prediction outputs
- [archive/local](../archive/local/): local-only historical outputs (gitignored)

Supplementary base-mode outputs are local-only (gitignored).

Current active canonical aligned files:

SSJ (written, run `20260414-1819`):
- [output/20260414-1819_sl-ssj-ud-test_full_trankit_aligned_predicted.conllu](output/20260414-1819_sl-ssj-ud-test_full_trankit_aligned_predicted.conllu)
- [output/20260414-1819_sl-ssj-ud-test_full_classla_aligned_predicted.conllu](output/20260414-1819_sl-ssj-ud-test_full_classla_aligned_predicted.conllu)

SST (spoken, run `20260420-1105`):
- [output/20260420-1105_sl-sst-ud-test_full_trankit_aligned_predicted.conllu](output/20260420-1105_sl-sst-ud-test_full_trankit_aligned_predicted.conllu)
- [output/20260420-1105_sl-sst-ud-test_full_classla_aligned_predicted.conllu](output/20260420-1105_sl-sst-ud-test_full_classla_aligned_predicted.conllu)

Trankit 1.3 run, CLARIN `11356/2201`, run `20260604-0859-tk13` — its SST prediction is the one shown in the recommended v4 table (CLASSLA files are identical to the canonical runs above):
- [output/20260604-0859-tk13_sl-ssj-ud-test_full_trankit_aligned_predicted.conllu](output/20260604-0859-tk13_sl-ssj-ud-test_full_trankit_aligned_predicted.conllu)
- [output/20260604-0859-tk13_sl-sst-ud-test_full_trankit_aligned_predicted.conllu](output/20260604-0859-tk13_sl-sst-ud-test_full_trankit_aligned_predicted.conllu)

v5 run, CLARIN `11356/2201`, run `20260622-0810-tk13`:
- SSJ written: Trankit and CLASSLA aligned predictions for `sl_ssj-ud-test`
- SST standardised: Trankit and CLASSLA aligned predictions for official `sl_sst-ud-test`
- SST colloquial: Trankit and CLASSLA aligned predictions for supplied `sl_sst-ud-test-pog`

No v5 prediction files are currently present for the supplied paired `stan`
test file.

Aligned predictions preserve gold `sent_id` values and sentence-level metadata where available.

Use [scripts/verify_canonical_run.py](../scripts/verify_canonical_run.py) with [references/canonical_run_manifest.json](../references/canonical_run_manifest.json) to check these aligned prediction files against canonical hashes.

These files are produced by [scripts/run_pipeline.py](../scripts/run_pipeline.py), [scripts/predict_trankit.py](../scripts/predict_trankit.py), and [scripts/predict_classla.py](../scripts/predict_classla.py).
