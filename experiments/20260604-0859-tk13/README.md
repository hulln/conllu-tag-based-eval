# Trankit 1.3 upgrade — SSJ and SST

Run stamp `20260604-0859-tk13` · CJVT server · 2026-06-04

## Purpose

Rerun the standing SPOT-Trankit vs CLASSLA-Stanza evaluation with the **Trankit
1.3** model — CLARIN [`11356/2201`](https://www.clarin.si/repository/xmlui/handle/11356/2201),
*"Trankit model for linguistic processing of written and spoken Slovenian 1.3"*.

1.3 replaces `11356/1997` (the 1.2 model used in the canonical
[`20260414-1819`](../20260414-1819/) and [`20260420-1105`](../20260420-1105/)
runs) and adds **non-standard / colloquial spoken Slovenian** transcriptions to
the SST training data. Everything else is held constant: same aligned mode, same
gold data, same evaluator, same CLASSLA configuration — only the Trankit model
is swapped in. The effect is expected mainly on SST.

## Datasets and systems

| Dataset | Run ID | Systems |
|---|---|---|
| SSJ written | `20260604-0859-tk13_sl-ssj-ud-test_full` | SPOT-Trankit 1.3, CLASSLA-Stanza |
| SST spoken | `20260604-0859-tk13_sl-sst-ud-test_full` | SPOT-Trankit 1.3, CLASSLA-Stanza |

Aligned mode: gold sentence and token boundaries are fixed; the systems predict
lemma, POS/morphology and dependency annotation on top of that structure.

## Running it

Container setup, preflight and GPU notes are generic — see
[docker/README.md](../../docker/README.md). With the image built and preflight
passing:

```bash
# CPU
docker compose run --rm eval bash scripts/run_trankit13_eval.sh

# GPU (only if preflight confirmed it and the compose GPU block is enabled)
docker compose run --rm --gpus all -e GPU=1 eval bash scripts/run_trankit13_eval.sh
```

Outputs are written back to the host through the mounted project directory; the
run stamp is set inside the script.

`scripts/run_trankit13_eval.sh` now runs three test sets — SSJ, standardised SST
and colloquial SST. The third block was added later for
[`20260622-0810-tk13`](../20260622-0810-tk13/); this stamp predates it and has run
directories for SSJ and SST only.

### Model provenance

The 1.3 model is cached under `cache/trankit-11356-2201/`, deliberately
**separate from the 1.2 cache** `cache/trankit/`, so the older `customized/`
model can never be reused by accident. `predict_trankit.py` verifies the archive
MD5 before extraction.

```text
archive  trankit-sl-ssj+sststand+sstpog.zip
MD5      ff1f3b86a4996fd5944db14725c602d8
URL      https://www.clarin.si/repository/xmlui/bitstream/handle/11356/2201/trankit-sl-ssj%2bsststand%2bsstpog.zip
```

On a firewalled server, download the archive elsewhere, verify the MD5, and place
it where the helper expects it — or populate `cache/trankit-11356-2201/` on a
networked host and copy the cache directory across. XLM-RoBERTa embeddings come
from Hugging Face; `HF_HOME=/project/cache/hf` (already set in the Compose file)
keeps them in the mounted cache too.

## Outputs

Predictions — [`predictions/output/`](../../predictions/output/), prefix
`20260604-0859-tk13_sl-{ssj,sst}-ud-test_full_{trankit,classla}_aligned_predicted.conllu`.

Results — [`results/output/20260604-0859-tk13_sl-ssj-ud-test_full/`](../../results/output/20260604-0859-tk13_sl-ssj-ud-test_full/)
and [`…_sl-sst-ud-test_full/`](../../results/output/20260604-0859-tk13_sl-sst-ud-test_full/),
each with `main/` (eval summaries, Trankit-vs-CLASSLA comparisons,
`qa_validation.md`) and `diagnostics/` (tagged metrics, error analyses).

The SST prediction from this run is the one shown in the v4 comparison table.
The CLASSLA outputs are identical to the canonical runs, since only the Trankit
model changed.

## Notes

- This run is **not** part of the hash-pinned canonical anchor in
  [references/canonical_run_manifest.json](../../references/canonical_run_manifest.json),
  which pins `20260414-1819`.
- Earlier same-day trial stamps (`20260604-0837-tk13`, `20260604-0843-tk13`) were
  superseded by this run and are excluded from Git.
- The later [`20260622-0810-tk13`](../20260622-0810-tk13/) run reuses this
  workflow and adds the supplied colloquial SST test file.
