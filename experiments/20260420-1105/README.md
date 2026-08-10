# Canonical SST run — SPOT-Trankit vs CLASSLA-Stanza (spoken)

Run stamp `20260420-1105` · 2026-04-20

## What this is

The counterpart of [`20260414-1819`](../20260414-1819/) on the spoken /
non-standard Slovenian **SST-UD** test set.

| Dataset | Run ID | Systems |
|---|---|---|
| SST spoken (UD `r2.16`, byte-identical to `r2.17`) | `20260420-1105_sl-sst-ud-test_full` | SPOT-Trankit 1.2 (CLARIN `11356/1997`), CLASSLA-Stanza (`type='spoken'`) |

Aligned mode: gold sentence and token boundaries fixed; the systems predict
lemma, POS/morphology and dependency annotation.

## Outputs

- Predictions: [`predictions/output/`](../../predictions/output/), prefix
  `20260420-1105_sl-sst-ud-test_full_{trankit,classla}_aligned_predicted.conllu`
- Results: [`results/output/20260420-1105_sl-sst-ud-test_full/`](../../results/output/20260420-1105_sl-sst-ud-test_full/)
  — `main/` (eval summaries, comparisons, `qa_validation.md`, `run_manifest.json`),
  `diagnostics/` (tagged metrics, error analyses)
- Published as the v3 SST interactive table in [`tables/`](../../tables/)

## Notes

- This run's machine-readable provenance is
  [`main/run_manifest.json`](../../results/output/20260420-1105_sl-sst-ud-test_full/main/run_manifest.json),
  written next to the outputs. Newer experiments put the manifest in the
  experiment directory instead; this one is left where it was generated.
- CLASSLA runs with `pos_use_lexicon=False` here: the Slovenian inflectional
  lexicon supports the default/standard models only, not the spoken `sl_sst`
  model.
- Its `file_hashes` entry for `scripts/run_pipeline.py` no longer matches the
  current file: the script was later extended with backward-compatible Trankit
  CLARIN model-source flags (`--trankit-clarin-url/-md5/-cache-dir/-gpu`) in
  commit `0f03a05`. The manifest is deliberately left unchanged because it
  records the state at run time; the refreshed hash and an explanation are in
  [references/canonical_run_manifest.json](../../references/canonical_run_manifest.json).
