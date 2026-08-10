# v5 run — SSJ, standardised SST and colloquial SST

Run stamp `20260622-0810-tk13` · 2026-06-22

## What this is

The run behind the **v5 comparison table**. It repeats the Trankit 1.3 vs
CLASSLA-Stanza evaluation across three test sets, adding the supplied
**colloquial (`pog`)** SST transcription alongside the official standardised one.

| Dataset | Run ID | Systems |
|---|---|---|
| SSJ written | `20260622-0810-tk13_sl-ssj-ud-test_full` | SPOT-Trankit 1.3 (CLARIN `11356/2201`), CLASSLA-Stanza 2.2.1 |
| SST standardised | `20260622-0810-tk13_sl-sst-ud-test_full` | same |
| SST colloquial (`pog`) | `20260622-0810-tk13_sl-sst-ud-test-pog_full` | same |

The workflow, model archive and cache handling are the same as
[`20260604-0859-tk13`](../20260604-0859-tk13/); container setup is in
[docker/README.md](../../docker/README.md).

## Outputs

- Predictions: [`predictions/output/`](../../predictions/output/), prefix
  `20260622-0810-tk13_sl-{ssj-ud-test,sst-ud-test,sst-ud-test-pog}_full_{trankit,classla}_aligned_predicted.conllu`
- Results: one directory per dataset under [`results/output/`](../../results/output/),
  each with `main/` and `diagnostics/`
- Published as the v5 table (EN and SL) in [`tables/`](../../tables/); both pages
  share one generated data bundle

All three runs have `qa_validation.md` status **PASS**.

## Notes

- **Colloquial SST post-processing.** Trankit predicted two roots in 2 of the 420
  colloquial sentences, which the CoNLL18 evaluator rejects. The fix and the
  affected sentence IDs are recorded in
  [`NORMALIZATION_NOTE.md`](../../results/output/20260622-0810-tk13_sl-sst-ud-test-pog_full/NORMALIZATION_NOTE.md),
  next to the outputs it describes.
- The supplied paired standardised (`stan`) test file is present locally but is
  **not** evaluated in v5. The dataset audit behind that decision is in
  [references/sst_vs_pog_comparison_2026-06-22.md](../../references/sst_vs_pog_comparison_2026-06-22.md);
  the publication check is in
  [references/v5_publication_qa_2026-06-22.md](../../references/v5_publication_qa_2026-06-22.md).
- Not part of the hash-pinned canonical anchor, which pins
  [`20260414-1819`](../20260414-1819/).
