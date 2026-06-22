# Post-processing note — pog (colloquial) Trankit prediction

Run: `20260622-0810-tk13_sl-sst-ud-test-pog_full`
Tool: SPOT-Trankit 1.3 (CLARIN 11356/2201)

## What was changed
The CoNLL18 evaluator rejects any sentence with more than one root (HEAD=0).
Trankit predicted **two roots** in 2 of the 420 colloquial sentences — both are
the very long *merged* utterances created by the pog/stan re-segmentation:

- `Artur-P-G7155-P700259.s2-s71_reseg.1933`   (434 tokens) — roots at ids 7, 362
- `Artur-P-G7155-P700259.s71-s125_reseg.1934` (379 tokens) — roots at ids 4, 350

To make the tree scoreable, the **first** root in each sentence was kept; the
**extra** root was demoted to `HEAD=<first-root id>`, `DEPREL=parataxis`.
This touches **2 tokens of 11,443** (0.017%); both were already errors (a
sentence can have only one root in gold), so the resolution does not flatter
Trankit.

## Reproducibility
- Pristine raw Trankit output is preserved at
  `predictions/output/20260622-0810-tk13_sl-sst-ud-test-pog_full_trankit_aligned_predicted.conllu.multiroot-orig`
- The fix is deterministic (keep lowest-id root, demote the rest to parataxis).
- CLASSLA pog output needed no change (single root in every sentence).
