# docker/

Container build files and generic instructions for running evaluations in a
container. Experiment-specific instructions live with the experiment, under
[`experiments/`](../experiments/).

## Images

| Image | Built from | Compose file | Used by |
|---|---|---|---|
| `conllu-tag-based-eval:latest` | [`Dockerfile`](../Dockerfile) (repo root) | [`docker-compose.yml`](../docker-compose.yml), service `eval` | SPOT-Trankit / CLASSLA-Stanza runs |
| `conllu-stanza:<version>` | [`Dockerfile.stanza`](Dockerfile.stanza) | [`docker-compose.stanza.yml`](../docker-compose.stanza.yml), services `stanza113` / `stanza114` | Stanza version comparison |

Both mount the project directory at `/project`, so predictions, results and
caches are written back to the host and survive the container exiting.

The root `Dockerfile` stays at the repository root because `docker-compose.yml`
uses the root build context; `Dockerfile.stanza` lives here because it is
selected explicitly by path.

## Getting the project onto a server

Clone or `rsync` the repository to the target machine and `cd` into it — all
commands below assume the repository root as the working directory.

## Trankit / CLASSLA image

```bash
docker compose build
```

One image works on CPU or GPU (the pinned `torch==2.0.1` ships CUDA libraries).

### Preflight

[`preflight_check.sh`](preflight_check.sh) resolves the two things that vary by
host — GPU visibility and outbound network access:

```bash
# CPU-only probe, also checks that model download URLs are reachable
docker compose run --rm eval bash docker/preflight_check.sh

# with nvidia-container-toolkit present, confirm GPU visibility too
docker compose run --rm --gpus all eval bash docker/preflight_check.sh
```

- **GPU** is usable only if it prints `CUDA available: True`. If so, enable the
  `deploy.resources` block in [`docker-compose.yml`](../docker-compose.yml) and
  pass `--gpus all -e GPU=1` when running.
- **Network**: HTTP `200/30x` for the CLARIN and Hugging Face URLs means models
  can be downloaded. If it fails, fetch the model archive on a networked machine
  and copy the populated cache directory across — the archive MD5 is verified, so
  a stale or partial file is caught.

### Running an evaluation

```bash
docker compose run --rm eval \
  python scripts/run_pipeline.py --modes aligned --gold data/gold/<file>.conllu
```

Outputs land in `predictions/output/` and `results/output/<run_id>/` on the host.
See [`scripts/README.md`](../scripts/README.md) for the available entry points.

## Stanza image

Two services, one per Stanza release, with separate model caches so neither
release can reuse the other's model files:

```bash
docker compose -f docker-compose.stanza.yml build stanza113 stanza114
docker compose -f docker-compose.stanza.yml run --rm stanza113 \
  python -c "import stanza, torch; print(stanza.__version__, torch.__version__, torch.cuda.is_available())"
```

The cache mount paths in that Compose file are CJVT/user-specific; adjust the
host side of the volume on another machine.

## Caches

Model and embedding downloads are kept in mounted directories so a rebuilt
container does not re-download them:

- `cache/` (repo-local, gitignored) for the Trankit/CLASSLA image
- `HF_HOME`, `TORCH_HOME`, `STANZA_RESOURCES_DIR` under the mounted `/cache` for
  the Stanza images

Keep caches separate per model version. Reusing one model release's cache for
another is the easiest way to silently invalidate a comparison.
