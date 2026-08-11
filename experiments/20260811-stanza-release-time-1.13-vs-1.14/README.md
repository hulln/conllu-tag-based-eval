# Stanza 1.13.0 vs 1.14.0: release-time Slovenian models

Run stamp `20260811-stanza-release-time-1.13-vs-1.14` · CJVT GPU server · 2026-08-11

## Why this experiment exists

Stanza resolves its models through versioned `resources.json` files that upstream
keeps editing after a release. The original 2026-08-10 comparison
([SSJ](../20260810-stanza-1.13-vs-1.14-ssj/),
[SST](../20260810-stanza-1.13-vs-1.14-sst/)) ran into the consequence: a
present-day Stanza 1.13 installation resolves Slovenian `default` /
`default_accurate` to the later `combined_*` models, not to the `ssj_*` models
that 1.13.0 resolved to on its release date.

This experiment reconstructs the Slovenian model configuration that each release
resolved to **at its own release date**, and evaluates both on the same aligned
UD Slovenian **SSJ** (written) and **SST** (spoken) test sets with `default` and
`default_accurate`. The 2026-08-10 runs are preserved unchanged.

The upstream chronology, the commits that moved the Slovenian defaults, and the
artifact cross-checks are documented in
[`references/stanza-1.13-vs-1.14-model-provenance.md`](../../references/stanza-1.13-vs-1.14-model-provenance.md).

## Release-time configurations

| Release | Historical resources commit | Package | Resolved processors |
|---|---|---|---|
| 1.13.0 (2026-06-18) | `9b46b7fe61df0ef466240f0ee19825cdc352af65` | `default` | `tokenize=ssj`, `lemma=ssj_nocharlm`, `pos=ssj_nocharlm`, `depparse=ssj_nocharlm` |
| 1.13.0 (2026-06-18) | `9b46b7fe61df0ef466240f0ee19825cdc352af65` | `default_accurate` | `tokenize=ssj`, `lemma=ssj_nocharlm`, `pos=ssj_crosloengual-bert`, `depparse=ssj_crosloengual-bert` |
| 1.14.0 (2026-07-15) | `f016b8e92f0ae9dd76729db44c4a582a72db2252` | `default` | `tokenize=combined_nocharlm`, `lemma=combined_nocharlm`, `pos=combined_charlm`, `depparse=combined_nocharlm` |
| 1.14.0 (2026-07-15) | `f016b8e92f0ae9dd76729db44c4a582a72db2252` | `default_accurate` | `tokenize=combined_charlm`, `lemma=combined_charlm`, `pos=combined_crosloengual-bert`, `depparse=combined_crosloengual-bert` |

Historical `resources.json` SHA-256:

- Stanza 1.13.0: `77a07c185dd875edae3b15cf62be01491ae37477f8902275276f7bfa91f7a22b`
- Stanza 1.14.0: `dbaf5f0c740072df4f0c571c750073c21e5af4d23b277ca590f2b64400a58a84`

Every required model and dependency was checked against the MD5 that its pinned
resource file declares. SHA-256 values and byte sizes are in
[`model-artifacts.json`](model-artifacts.json).

`default_accurate` additionally uses `EMBEDDIA/crosloengual-bert` pinned to
revision `750255b6915cf42623143690d8ea79ceab8ee2e8`. The transformer is loaded
during **prediction**, not by the CoNLL evaluator; the `default_accurate`
prediction runs used the pinned snapshot in an isolated Hugging Face cache with
the hub forced offline.

## Data and evaluation design

Both treebanks are evaluated with **gold sentence and token boundaries**. Stanza
predicts `LEMMA`, `UPOS`, `XPOS`, `FEATS`, `HEAD` and `DEPREL`; gold `ID`, `FORM`
and `MISC` are preserved. Tokenisation quality is therefore out of scope.

- **SSJ:** 1,282 sentences,
  25,442 syntactic words,
  SHA-256 `c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0`.
- **SST:** 432 sentences,
  11,443 syntactic words,
  SHA-256 `6824234edf98cbbedb2e981644c324a3058c2920ed6cdcd7f467e835cfe25eeb`. The
  r2.16 and r2.17 copies of this test file are byte-identical; this experiment
  must not be silently migrated to r2.18.

Because the boundaries come from gold, the evaluator's `Sentences`, `Tokens` and
`Words` scores are 100.00 by construction and serve as alignment checks rather
than quality metrics.

## Results

| Test set | Package | 1.13.0 release LAS | 1.14.0 release LAS | Delta |
|---|---|---:|---:|---:|
| SSJ | `default` | 90.55 | 90.73 | +0.18 |
| SSJ | `default_accurate` | 95.04 | 94.86 | -0.18 |
| SST | `default` | 68.90 | 81.95 | +13.05 |
| SST | `default_accurate` | 78.33 | 86.13 | +7.80 |

On **SSJ** the release-to-release changes are small and mixed. On **SST** the
release-time 1.14.0 configuration scores much higher, especially for dependency
parsing and the morphosyntax-sensitive composite metrics.

The same pattern is visible in tagging alone: under release-time 1.13.0 the
`default` UPOS score falls from 98.29 on SSJ to 92.05 on SST, while under
release-time 1.14.0 it falls only from 98.59 to 97.90.

### How to read the SST gap

The two arms differ in more than the library version. Release-time 1.13.0
defaults resolve to `ssj_*` models — trained on the written SSJ treebank —
while release-time 1.14.0 defaults resolve to the `combined_*` set.

For Slovenian, `combined` is a training-data fact, not only a naming one. In
Stanza 1.14.0 the dataset-preparation code builds `sl_combined` by concatenating
the **train** splits of `UD_Slovenian-SSJ` and `UD_Slovenian-SST` (dev and test
come from SSJ only), and POS, lemma and dependency-parser preparation all route
through the same dispatch. The SSJ+SST merge therefore applies to **POS, lemma
and dependency parsing alike**, not to the parser alone. On top of that,
`build_extra_combined_slovenian_dataset` supplies extra Slovene data (SUK:
`ssj500k-tag.ud.conllu`, `ambiga.ud.conllu`) for the **POS and lemma** model
types only. The code paths and file references are in
[the provenance document](../../references/stanza-1.13-vs-1.14-model-provenance.md#what-combined-means-for-slovenian--training-data-not-just-resolution).

So the release-time 1.13.0 defaults are written-treebank models applied to spoken
text across all three components, while the release-time 1.14.0 defaults have
seen spoken training data in all three, plus extra Slovene resources for POS and
lemma.

Checkpoint resolution is a separate axis from training data: the pinned resource
files also show that the 1.14.0 POS checkpoints (both packages) and the
`default_accurate` lemmatizer declare `oscar2023` forward/backward charLM
dependencies that their 1.13.0 counterparts do not. Those are release-time facts
read from the pinned files themselves; the per-component listing is in
[the provenance document](../../references/stanza-1.13-vs-1.14-model-provenance.md#release-time-declared-dependencies)
and under `comparisons.main.co_varying_factors` in
[`manifest.json`](manifest.json). They are not the whole POS/lemma story — the
training-data change above applies to those components too.

**What this does not show.** Several things change together between the two arms
— library version, resolved model set, the checkpoints' declared dependencies and
PyTorch version — and none of these factors was tested separately, so their individual effects cannot be
separated here. The move from SSJ-treebank-based `ssj_*` models to SSJ+SST-trained
`combined_*` models is consistent with the large SST gains, but this experiment
does not quantify its contribution, and no significance testing was performed.

### The three comparisons

[`comparison.txt`](comparison.txt) has all metrics for three explicitly separated
comparisons, generated by
[`scripts/compare_stanza_release_time.py`](../../scripts/compare_stanza_release_time.py).
In that file the short label `accurate` denotes Stanza's `default_accurate`
package.

1. **Release-time 1.13 → release-time 1.14** — the primary historical
   comparison, reported above.
2. **Release-time 1.13 → present-day-resource 1.13** — the post-release
   resource change alone, with the Stanza library (1.13.0), the Docker image
   (`sha256:dbbc66d6…`) and PyTorch (`2.0.1+cu118`) all held constant. Only the
   resolved Slovenian model set differs, which makes it a cleaner contrast for
   the effect of post-release resource resolution than comparison 1. It still
   does not attribute the difference to any individual model change.
3. **Present-day-resource 1.13 → 1.14** — what the original 2026-08-10
   experiment measured. It is not a library-only comparison either: its two arms
   differ in lemmatizer checkpoints and in PyTorch version.

## Verification

Reconstructed release-time 1.14 outputs were compared with the original
2026-08-10 Stanza 1.14 outputs: **all four prediction files and all four
evaluator output files are byte-identical** across SSJ/SST ×
`default`/`default_accurate`.

This is a reproduction check on the 1.14 side, and agreement was expected before
the runs: the Slovenian package mappings in the pinned `f016b8e9` file and in the
present-day `resources_1.14.0.json` used on 2026-08-10 are the same, so both runs
resolve to the same model binaries (every `combined_*` SHA-256 in
[`model-artifacts.json`](model-artifacts.json) matches the value recorded for the
1.14 cache in the
[2026-08-10 SSJ manifest](../20260810-stanza-1.13-vs-1.14-ssj/manifest.json)). It
confirms exact reproducibility for these four 1.14 runs; it says nothing about model quality,
and it concerns only the two 1.14 runs — the two arms of the main comparison
resolve to entirely different binaries (`ssj_*` vs `combined_*`), which this
check does not touch. The practical point is that the historical
resource-resolution problem affected the Stanza 1.13 side only.

The following checks have passed and are recorded in the manifest:

- both gold files matched their expected SHA-256;
- every required historical model artifact matched the MD5 declared by its
  pinned `resources.json`;
- both pinned `resources.json` files were re-fetched from
  `stanfordnlp/stanza-resources` at their commits, matched the SHA-256 recorded
  above, and were compared artifact-by-artifact against
  [`model-artifacts.json`](model-artifacts.json) — **7/7 MD5s match for 1.13.0
  and 11/11 for 1.14.0**, with the recorded artifact set equal to the exact
  dependency closure of both packages over `tokenize,pos,lemma,depparse`;
- the external transformer revision was pinned and prediction ran offline;
- all eight evaluations reported 100.00 for `Sentences` / `Tokens` / `Words`;
- all four reconstructed 1.14 predictions and evaluator outputs were
  byte-identical to the original 1.14 artifacts;
- `comparison.txt` was regenerated from the evaluator files and verified
  byte-for-byte.

## Environment and scope

| Release | Docker image | Image ID | torch |
|---|---|---|---|
| 1.13.0 | `conllu-stanza:1.13.0` | `sha256:dbbc66d648e4f951022c4511086b9d6cc3f663eb453bb1dfc421772154d6217c` | `2.0.1+cu118` |
| 1.14.0 | `conllu-stanza:1.14.0` | `sha256:52edf2dff5c8da66ef448be0390728ad3df7a8f9d49f19b94eb3f83d8b83fc14` | `2.6.0+cu118` |

These are the same two images as the 2026-08-10 run — the image IDs match those
recorded in the
[SSJ manifest](../20260810-stanza-1.13-vs-1.14-ssj/manifest.json) — so the torch
versions above are the ones recorded there under `python_environments`, together
with the shared pins (`numpy==1.26.4`, `transformers==4.35.2`,
`huggingface-hub==0.19.4`, `accelerate==0.24.1`, `peft==0.6.2`) and the
pip-freeze snapshots in that experiment's
[`environment/`](../20260810-stanza-1.13-vs-1.14-ssj/environment/) directory.

### The PyTorch difference

The two arms do not share a PyTorch version. In this setup, Stanza 1.14 cannot
load its Slovenian lemmatizer under torch 2.0.1 (`weights_only=True` fails on
`_codecs.encode`, and that torch version has no
`torch.serialization.add_safe_globals`), so the recorded 1.14 run uses torch
2.6.0 while the 1.13 run uses torch 2.0.1. The details are in the
[2026-08-10 SSJ README](../20260810-stanza-1.13-vs-1.14-ssj/README.md).

A PyTorch control exists, but it covers an adjacent configuration. In
[`control-torch2.6.md`](../20260810-stanza-1.13-vs-1.14-ssj/control-torch2.6.md),
Stanza 1.13.0 produced unchanged output under torch 2.0.1 vs 2.6.0, but that
control used the present-day-resource `combined_*` configuration rather than the
release-time `ssj_*` configuration used here. A common-PyTorch control for the
release-time comparison was not run. The possible contribution of the PyTorch
version difference therefore remains unisolated.

The reconstruction pins the **release-time Slovenian resource configuration and
model artifacts** under Stanza 1.13.0 and 1.14.0. It does not recreate the
operating-system/CUDA environment of the June/July 2026 release dates, and it
does not pin PyTorch to anything contemporary with them.

Model binaries and the historical `resources.json` files are not committed to
this repository. Their hashes and the exact historical resource commits are in
[`model-artifacts.json`](model-artifacts.json) and
[`manifest.json`](manifest.json).

## Files

- [`comparison.txt`](comparison.txt) — machine-generated canonical comparison.
- [`model-artifacts.json`](model-artifacts.json) — verified historical model
  mappings, MD5, SHA-256 and byte sizes.
- [`manifest.json`](manifest.json) — machine-readable experiment provenance,
  datasets, environment, expected metrics, file hashes and identity checks.
- [`scripts/compare_stanza_release_time.py`](../../scripts/compare_stanza_release_time.py)
  — regenerates the comparison and verifies 1.14 byte identity.
- Release-time predictions are under [`predictions/output/`](../../predictions/output/)
  with the corresponding `20260811-stanza-*-release-defaults_` run stamps.
- Evaluator outputs are under [`results/output/`](../../results/output/) with
  the corresponding release-time run stamps.

## Reproducing

The steps below are **reconstructed from the provenance recorded in
[`manifest.json`](manifest.json) and
[`model-artifacts.json`](model-artifacts.json)** — pinned resource commits,
resource-file SHA-256 values, cache roots, image IDs, run stamps and per-artifact
MD5/SHA-256. They are not a verbatim command log: the commands that fetched and
placed the historical `resources.json` files were not captured at run time. Treat
the hashes as authoritative and the command shapes as derived. The model binaries
and historical resource files are not committed here and the caches live on the
CJVT server, but the resource files are re-fetchable at their pinned commits, as
step 2 shows.

### 1. Gold data

```bash
sha256sum data/gold/sl_ssj-ud-test.conllu   # c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0
sha256sum data/gold/sl_sst-ud-test.conllu   # 6824234edf98cbbedb2e981644c324a3058c2920ed6cdcd7f467e835cfe25eeb
```

### 2. Pin the historical `resources.json`

Each release is pinned to a specific `stanfordnlp/stanza-resources` commit. Fetch
the versioned file at that commit and verify it against the recorded SHA-256:

```bash
# Stanza 1.13.0 — state at the 2026-06-18 release, before commit 654c7f7f
curl -fsSL https://raw.githubusercontent.com/stanfordnlp/stanza-resources/\
9b46b7fe61df0ef466240f0ee19825cdc352af65/resources_1.13.0.json -o resources_1.13.0.json
sha256sum resources_1.13.0.json  # 77a07c185dd875edae3b15cf62be01491ae37477f8902275276f7bfa91f7a22b

# Stanza 1.14.0 — state at the 2026-07-15 release, before f2976f2d and 8048f8a1
curl -fsSL https://raw.githubusercontent.com/stanfordnlp/stanza-resources/\
f016b8e92f0ae9dd76729db44c4a582a72db2252/resources_1.14.0.json -o resources_1.14.0.json
sha256sum resources_1.14.0.json  # dbaf5f0c740072df4f0c571c750073c21e5af4d23b277ca590f2b64400a58a84
```

### 2b. Place it as the cache's `resources.json`

Saving the file under its upstream name is not enough. Stanza resolves packages
through `$STANZA_RESOURCES_DIR/resources.json`, so the pinned versioned file must
*become* that file inside each release's isolated cache:

| Release | Host path the pinned file must occupy | Path inside the container |
|---|---|---|
| 1.13.0 | `/mnt/local-hddpool/niveshull/stanza-eval-release113/stanza/resources.json` | `/cache/stanza/resources.json` |
| 1.14.0 | `/mnt/local-hddpool/niveshull/stanza-eval-release114/stanza/resources.json` | `/cache/stanza/resources.json` |

```bash
install -D resources_1.13.0.json \
  /mnt/local-hddpool/niveshull/stanza-eval-release113/stanza/resources.json
install -D resources_1.14.0.json \
  /mnt/local-hddpool/niveshull/stanza-eval-release114/stanza/resources.json
```

The cache roots are deliberately separate from the 2026-08-10 caches so that
neither release can reuse the other's downloads or the present-day resource
resolution.

**The committed [`docker-compose.stanza.yml`](../../docker-compose.stanza.yml)
mounts the 2026-08-10 caches (`stanza-eval/1.13`, `stanza-eval/1.14`), not the
release-time caches above.** Running the steps below therefore requires mounting
the release-time root explicitly, for example:

```bash
docker run --rm --gpus all \
  -v "$PWD":/project -w /project \
  -v /mnt/local-hddpool/niveshull/stanza-eval-release113:/cache \
  -e STANZA_RESOURCES_DIR=/cache/stanza \
  -e HF_HOME=/cache/huggingface \
  -e TORCH_HOME=/cache/torch \
  conllu-stanza:1.13.0 <command>
```

and the same with `stanza-eval-release114` and `conllu-stanza:1.14.0`.

### 3. Models

**`download_json=False` is mandatory.** `stanza.download()` defaults to
`download_json=True`, which refreshes `resources.json` from upstream and would
overwrite the pinned file placed in step 2b, silently resolving the present-day
model set instead.

Download only the processors this evaluation uses, so that each artifact is
resolved individually through the pinned JSON and verified against the MD5 that
file declares, rather than arriving inside a prebuilt `default.zip`:

```bash
python -c "import stanza; stanza.download('sl', package='default', \
  processors='tokenize,pos,lemma,depparse', download_json=False)"
python -c "import stanza; stanza.download('sl', package='default_accurate', \
  processors='tokenize,pos,lemma,depparse', download_json=False)"
```

Run both inside the matching container from step 2b. Restricting to these four
processors also keeps the NER models out: both pinned files map `default` /
`default_accurate` to a `ner` package as well, and this experiment never runs it.

The resulting artifact set is exactly what
[`model-artifacts.json`](model-artifacts.json) records — byte size, the MD5
declared by the pinned `resources.json`, and an independent SHA-256 per file:

- **1.13.0 — 7 artifacts:** `tokenize/ssj.pt`, `lemma/ssj_nocharlm.pt`,
  `pos/ssj_nocharlm.pt`, `pos/ssj_crosloengual-bert.pt`,
  `depparse/ssj_nocharlm.pt`, `depparse/ssj_crosloengual-bert.pt`,
  `pretrain/conll17.pt`. No charLM is required on this side.
- **1.14.0 — 11 artifacts:** the `combined_*` tokenize/lemma/pos/depparse set
  (two each) plus `pretrain/conll17.pt`, `forward_charlm/oscar2023.pt` and
  `backward_charlm/oscar2023.pt`.

Both sets are the exact dependency closure of the two packages over those four
processors, computed from the pinned files themselves.

### 3b. External transformer for `default_accurate`

`default_accurate` loads `EMBEDDIA/crosloengual-bert` at revision
`750255b6915cf42623143690d8ea79ceab8ee2e8`. Per-file sizes and SHA-256 values are
under `external_transformer.snapshot_files` in [`manifest.json`](manifest.json).

The reconstruction placed the pinned snapshot in each release's isolated Hugging
Face cache (`HF_HOME=/cache/huggingface`) and resolved `refs/main` to that exact
commit SHA, so the pipeline loads the pinned revision rather than whatever `main`
currently points at. The `default_accurate` prediction runs were then executed
with the hub forced offline:

```bash
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
```

This applies to prediction, where the transformer is loaded. The CoNLL evaluator
in step 5 does not use it.

### 4. Predict — 8 runs

**The pinned resource file needs a second guard here.** `stanza.Pipeline()` does
its own resource resolution at construction time and by default refreshes
`resources.json` from upstream first, which would overwrite the pinned file after
step 3 had already placed the correct models.
[`scripts/predict_stanza.py`](../../scripts/predict_stanza.py) therefore builds
the pipeline with `download_method=None`:

```python
nlp = stanza.Pipeline(
    "sl",
    package=args.package,
    processors="tokenize,pos,lemma,depparse",
    tokenize_pretokenized=True,
    use_gpu=True,
    download_method=None,     # do not re-resolve or refresh the pinned resources.json
)
```

`download_json=False` protects the download stage and `download_method=None`
protects the prediction stage. **Both are required** for the run to resolve
through the pinned historical file; any reimplementation must keep the second one.

Two releases × two test sets × two packages, using
[`scripts/predict_stanza.py`](../../scripts/predict_stanza.py) in the matching
container. The `--package` value is Stanza's real package name; the filename
label shortens `default_accurate` to `accurate`:

```bash
python scripts/predict_stanza.py \
  --gold data/gold/sl_ssj-ud-test.conllu \
  --package default \
  --output predictions/output/20260811-stanza-1.13-release-defaults_sl-ssj-ud-test_full_stanza-1.13.0-release-default_aligned_predicted.conllu
```

Run stamps are `20260811-stanza-1.13-release-defaults` and
`20260811-stanza-1.14-release-defaults`; the eight exact output paths and their
SHA-256 values are listed under `file_hashes` in [`manifest.json`](manifest.json).

### 5. Evaluate — 8 runs

```bash
mkdir -p results/output/20260811-stanza-1.13-release-defaults_sl-ssj-ud-test_full/main
python3 scripts/conll18_ud_eval_tag-based.py -v \
  data/gold/sl_ssj-ud-test.conllu \
  predictions/output/20260811-stanza-1.13-release-defaults_sl-ssj-ud-test_full_stanza-1.13.0-release-default_aligned_predicted.conllu \
  | tee results/output/20260811-stanza-1.13-release-defaults_sl-ssj-ud-test_full/main/stanza-1.13.0-release-default_aligned_eval.txt
```

### 6. Regenerate the comparison

```bash
python3 scripts/compare_stanza_release_time.py > experiments/20260811-stanza-release-time-1.13-vs-1.14/comparison.txt
```

This also runs the 1.14 byte-identity check. The check is independent: each
comparison block reads the artifacts named in its own title, so
`--skip-identity-check` cannot change which files are compared (it only omits the
leading `VERIFY:` line, which does change the output bytes).

## Limitations

- No statistical significance testing was performed.
- One evaluation run per condition; run-to-run variation was not tested.
- Gold token boundaries mean tokenisation quality is not evaluated.
- This is a historical **model/resource reconstruction**, not a complete
  historical machine-image reconstruction.
- The two arms differ in PyTorch version (`2.0.1+cu118` vs `2.6.0+cu118`).
  A common-PyTorch control for the release-time comparison was not run — see
  [The PyTorch difference](#the-pytorch-difference).
- Library version, resolved model set, the checkpoints' declared dependencies and
  PyTorch all change together between release-time 1.13.0 and 1.14.0. None of
  these factors was tested separately, so their individual effects cannot be
  separated — see
  [How to read the SST gap](#how-to-read-the-sst-gap).
- The historical `resources.json` files and the model binaries are **not
  committed to this repository**. That is a packaging limitation, not a
  provenance gap: both pinned resource files are re-fetchable at their upstream
  commits, both match the SHA-256 recorded here, and every model MD5 in
  [`model-artifacts.json`](model-artifacts.json) has been cross-checked against
  the MD5 those files declare — see
  [the provenance document](../../references/stanza-1.13-vs-1.14-model-provenance.md).
  Rerunning still requires obtaining binaries that match the recorded hashes.
