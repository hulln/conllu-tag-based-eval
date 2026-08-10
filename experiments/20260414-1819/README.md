# Canonical SSJ run — SPOT-Trankit vs CLASSLA-Stanza

Run stamp `20260414-1819` · 2026-04-14

## What this is

The reference aligned evaluation on the written Slovenian **SSJ-UD** test set,
comparing SPOT-Trankit against CLASSLA-Stanza. This is the repository's
**reproducibility anchor**: its inputs, scripts and outputs are hash-pinned in
[references/canonical_run_manifest.json](../../references/canonical_run_manifest.json)
and verified by [scripts/verify_canonical_run.py](../../scripts/verify_canonical_run.py).

| Dataset | Run ID | Systems |
|---|---|---|
| SSJ written (UD `r2.17`) | `20260414-1819_sl-ssj-ud-test_full` | SPOT-Trankit 1.2 (CLARIN `11356/1997`), CLASSLA-Stanza (`pos_use_lexicon=True`) |

Aligned mode: gold sentence and token boundaries fixed; the systems predict
lemma, POS/morphology and dependency annotation.

## Outputs

- Predictions: [`predictions/output/`](../../predictions/output/), prefix
  `20260414-1819_sl-ssj-ud-test_full_{trankit,classla}_aligned_predicted.conllu`
- Results: [`results/output/20260414-1819_sl-ssj-ud-test_full/`](../../results/output/20260414-1819_sl-ssj-ud-test_full/)
  — `main/` (eval summaries, Trankit-vs-CLASSLA comparisons, `qa_validation.md`),
  `diagnostics/` (tagged metrics, error analyses)
- Published as the v2 SSJ interactive table in [`tables/`](../../tables/)

## Notes

- Provenance for this run lives in the repository-level
  `references/canonical_run_manifest.json` rather than in a local `manifest.json`.
  That file is the default input of `verify_canonical_run.py` and is intentionally
  left in `references/`; run `verify_canonical_run.py` after any rerun.
- Later runs re-evaluate the same data with newer models; see
  [`20260604-0859-tk13`](../20260604-0859-tk13/) and
  [`20260622-0810-tk13`](../20260622-0810-tk13/).
