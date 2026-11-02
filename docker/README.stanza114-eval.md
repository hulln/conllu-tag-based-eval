# Stanza 1.14.0 (`default_accurate`) evaluation for the website

Aligned evaluation of Stanza 1.14.0 with `package="default_accurate"` on the three website test
sets (SSJ, SST standardised, SST colloquial). The method is the same as for SPOT-Trankit and
CLASSLA-Stanza: gold sentence and token boundaries, the unchanged evaluator, the same per-tag
evaluation and error analysis, and an aligned-mode QA report.

| File | Role |
|---|---|
| [references/stanza-1.14.0-default_accurate.json](../references/stanza-1.14.0-default_accurate.json) | Pins: gold hashes, `resources.json` and model-artifact SHA-256, transformer revision, image ID, August reference hashes |
| [scripts/run_stanza_eval.py](../scripts/run_stanza_eval.py) | Runner: preflight, prediction, evaluation (`run_pipeline.eval_and_analyze`), QA, manifest |
| [scripts/predict_stanza.py](../scripts/predict_stanza.py) | Prediction on gold tokens (from the August runs; output format unchanged) |
| [scripts/verify_stanza_artifacts.py](../scripts/verify_stanza_artifacts.py) | Read-only check of the model cache against the pins |
| [scripts/qa_validate_system_run.py](../scripts/qa_validate_system_run.py) | Single-system QA using the checks of `qa_validate_run.py`, plus tree checks |
| [docker-compose.stanza114-eval.yml](../docker-compose.stanza114-eval.yml) | Container with the August image and the release-time cache mounted read-only |

All commands below run on the CJVT GPU server, from the repository root.

## 1. Check the server state

```bash
# Gold files (gitignored; rsync them up if missing)
sha256sum data/gold/sl_ssj-ud-test.conllu data/gold/sl_sst-ud-test.conllu data/gold/sl_sst-ud-test-pog.conllu
# expected: c14d5d2f…c8b0, 6824234e…5eeb, 898fdadb…d756 (full values in the pins file)

# Image from August: expected sha256:52edf2dff5c8da66ef448be0390728ad3df7a8f9d49f19b94eb3f83d8b83fc14
docker image inspect conllu-stanza:1.14.0 --format '{{.Id}}'

# Caches from August (must exist; both are mounted read-only): the release-time Stanza cache, and
# the 2026-08-10 Stanza 1.14 cache for crosloengual-bert (the release-time cache has no copy of it)
ls -l /mnt/local-hddpool/niveshull/stanza-eval-release114/stanza/resources.json \
      /mnt/local-hddpool/niveshull/stanza-eval/1.14/huggingface/hub/models--EMBEDDIA--crosloengual-bert/refs/main

nvidia-smi
```

If the image ID differs or the image is missing, `docker compose … build` recreates it from
`docker/Dockerfile.stanza` with the same arguments, but unpinned transitive dependencies may
resolve differently. Compare the rebuilt environment with the August `pip freeze`:

```bash
docker compose -f docker-compose.stanza114-eval.yml run --rm stanza114-eval pip freeze > /tmp/stanza114-freeze.txt
python3 -c "import json; pins=set(json.load(open('references/stanza-1.14.0-default_accurate.json'))['environment']['pip_freeze']); now=set(open('/tmp/stanza114-freeze.txt').read().split()); print('missing:', sorted(pins-now)); print('extra:', sorted(now-pins))"
```

If the cache is missing, do not let Stanza download models: `stanza.download()` would resolve
today's `resources.json`. Rebuild it from the pinned `stanza-resources` commit as described in the
August release-time experiment, and check it with the preflight below.

## 2. Preflight (no model is loaded)

```bash
STAMP=$(date +%Y%m%d-%H%M)-stanza114acc
docker compose -f docker-compose.stanza114-eval.yml run --rm stanza114-eval \
  python scripts/run_stanza_eval.py --run-stamp "$STAMP" --preflight-only
```

This checks the gold hashes, that no output of this stamp exists yet, `HF_HUB_OFFLINE`/
`TRANSFORMERS_OFFLINE`, CUDA, and every pinned artifact (`verify_stanza_artifacts.py`).

## 3. Smoke test on the two longest SST-colloq sentences (optional)

SST-colloq keeps two run-on sentences of 434 and 379 tokens that the standardised SST file splits
up, so the August runs never saw sentences this long. This writes only to the container's `/tmp`:

```bash
docker compose -f docker-compose.stanza114-eval.yml run --rm stanza114-eval bash -c '
python - <<EOF
blocks = open("data/gold/sl_sst-ud-test-pog.conllu", encoding="utf-8").read().strip().split("\n\n")
longest = sorted(blocks, key=lambda b: -sum(1 for l in b.splitlines() if l[:1].isdigit()))[:2]
open("/tmp/pog_long.conllu", "w", encoding="utf-8").write("\n\n".join(longest) + "\n\n")
EOF
python scripts/predict_stanza.py --gold /tmp/pog_long.conllu --package default_accurate \
  --output /tmp/pog_long_pred.conllu --require-gpu &&
python scripts/conll18_ud_eval_tag-based.py -v /tmp/pog_long.conllu /tmp/pog_long_pred.conllu'
```

## 4. Full run

```bash
docker compose -f docker-compose.stanza114-eval.yml run --rm stanza114-eval \
  python scripts/run_stanza_eval.py --run-stamp "$STAMP"
```

The runner stops before evaluating a test set if its prediction is not a set of well-formed,
gold-aligned trees. No automatic correction is applied; compare
`results/output/20260622-0810-tk13_sl-sst-ud-test-pog_full/NORMALIZATION_NOTE.md` for the rule
used for Trankit and decide explicitly.

## 5. Outputs

For each of `sl-ssj-ud-test`, `sl-sst-ud-test` and `sl-sst-ud-test-pog`, with
`run_id = <STAMP>_<dataset>_full`:

```
predictions/output/<run_id>_stanza_aligned_predicted.conllu
results/output/<run_id>/main/stanza_aligned_eval.txt
results/output/<run_id>/main/qa_validation.md
results/output/<run_id>/main/qa_tree_checks.json
results/output/<run_id>/main/run_manifest.json
results/output/<run_id>/main/stanza_prediction_provenance.json
results/output/<run_id>/main/stanza_artifact_verification.json
results/output/<run_id>/diagnostics/stanza_aligned_eval-tagged.txt
results/output/<run_id>/diagnostics/stanza_aligned_errors.md
```

## 6. Reproducibility checks

- SSJ and SST: the runner compares the new prediction and evaluator output with the August
  release-time run (`august_reference` in the pins file) and fails if either differs. They are
  expected to be byte-identical.
- `run_manifest.json` records gold, prediction and result hashes, script hashes, the commands,
  and the artifact-verification status; `stanza_prediction_provenance.json` records library
  versions, the GPU, offline flags and the SHA-256 of each model file the pipeline loaded.
- `git` is not installed in the image, so record the commit from the host:
  `git rev-parse HEAD && git status --short`.
