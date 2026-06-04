# Running the Trankit 1.3 evaluation on the CJVT server (Docker)

Additional evaluation on the **Trankit 1.3** model — CLARIN **`11356/2201`**,
*"Trankit model for linguistic processing of written and spoken Slovenian 1.3"*,
which adds **non-standard / colloquial spoken Slovenian** transcriptions to the
SST training data (it replaces `11356/1997`, the 1.2 model used in the earlier runs).

It runs **the same pipeline as the previous full runs** — aligned mode, Trankit
vs CLASSLA, on both the standard **SSJ** and the spoken/non-standard **SST** test
sets — only with the new Trankit model swapped in.

## 1. Get the project onto the server

Clone (or `rsync`) this repo to the CJVT box, e.g. under
`/mnt/local-hddpool/niveshull/conllu-tag-based-eval`, same as the STARK/SVO task.
`cd` into it for all commands below.

## 2. Build the image

```bash
docker compose build
```

Single image works on CPU or GPU (pinned `torch==2.0.1` ships CUDA libs).

## 3. Preflight — resolve the two unknowns

```bash
# CPU-only probe (also checks network reachability):
docker compose run --rm eval bash docker/preflight_check.sh

# If the host has nvidia-container-toolkit, also confirm GPU visibility:
docker compose run --rm --gpus all eval bash docker/preflight_check.sh
```

- **GPU**: usable only if it prints `CUDA available: True`. If so, uncomment the
  `deploy.resources` block in [docker-compose.yml](../docker-compose.yml) and run
  step 4 with `GPU=1`. Otherwise leave it CPU (works, just slower).
- **Network**: HTTP `200/30x` for the clarin.si + huggingface URLs means the
  container can download the model. If it `FAIL`s, see "Firewalled" below.

## 4. Run the evaluation

CPU:
```bash
docker compose run --rm eval bash scripts/run_trankit13_eval.sh
```

GPU (only if preflight confirmed it + compose GPU block uncommented):
```bash
docker compose run --rm --gpus all -e GPU=1 eval bash scripts/run_trankit13_eval.sh
```

This runs SSJ then SST. Outputs land on the host (project is volume-mounted):
- predictions: `predictions/output/` (run stamp `<date>-tk13`, e.g. `20260604-1432-tk13`)
- results: `results/output/<stamp>_sl-ssj-ud-test_full/` and `..._sl-sst-ud-test_full/`
- model cache: `cache/trankit-11356-2201/` (kept **separate** from the 1.2
  `cache/trankit/` so the old `customized/` model is never reused)

The first run downloads the ~2–5 GB model + XLM-RoBERTa embeddings into the
mounted cache, so subsequent runs are fast.

## Firewalled server (no outbound network)

Download the zip on a machine that has access and drop it where the helper
expects it, then re-run step 4 — the MD5 is verified, so a stale/partial file
is caught:

```bash
# on a networked machine:
curl -L -o trankit-sl-ssj+sststand+sstpog.zip \
  'https://www.clarin.si/repository/xmlui/bitstream/handle/11356/2201/trankit-sl-ssj%2bsststand%2bsstpog.zip'
md5sum trankit-sl-ssj+sststand+sstpog.zip   # must be ff1f3b86a4996fd5944db14725c602d8
```

predict_trankit.py reuses an already-extracted model under the cache dir, so the
cleanest offline path is to run step 4 once on a networked host (populating
`cache/trankit-11356-2201/`) and copy that cache dir to the server. The XLM-R
embeddings come from HuggingFace; setting `HF_HOME=/project/cache/hf` (already in
the compose file) keeps them in the mounted cache too.

## Comparing 1.3 vs 1.2

The earlier 1.2 runs are still in `results/output/` (`20260414-1819_*` SSJ,
`20260420-1105_*` SST). After the 1.3 run completes you have matching
`*_tk13` results to diff against them — most relevant on **SST**, where the new
non-standard training data should move the numbers.
