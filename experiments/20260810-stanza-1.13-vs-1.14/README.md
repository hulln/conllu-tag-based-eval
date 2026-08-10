# Stanza 1.13.0 vs 1.14.0 on UD Slovenian SSJ

Run stamp `20260810-stanza-1.13-vs-1.14` · CJVT GPU server · 2026-08-10

## Purpose

Does upgrading Stanza from **1.13.0** to **1.14.0** change Slovenian annotation
quality on the SSJ-UD test set, and how does that compare to the effect of
choosing the `default_accurate` model package over `default`?

The evaluation covers lemma, POS/morphology and dependency annotation. Sentence
and token boundaries are fixed, so tokenisation quality is deliberately out of
scope.

## Conditions

| # | Stanza | Package |
|---|---|---|
| 1 | 1.13.0 | `default` |
| 2 | 1.13.0 | `default_accurate` |
| 3 | 1.14.0 | `default` |
| 4 | 1.14.0 | `default_accurate` |

Slovenian packages available in the Stanza 1.14 `resources.json` at the time of
the run: `default`, `default_fast`, `default_accurate`, `combined`, `ssj`, `sst`.

## Dataset and fixed-boundary methodology

**UD Slovenian SSJ**, release `r2.17` / UD v2.17
([upstream](https://github.com/UniversalDependencies/UD_Slovenian-SSJ)),
local file `data/gold/sl_ssj-ud-test.conllu` (gitignored, as elsewhere in this
repository).

```text
SHA-256              c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0
Sentences            1,282
Syntactic word rows  25,442
Multiword tokens     0
Empty nodes          0
```

This is the same SSJ test file used by the canonical run pinned in
[references/canonical_run_manifest.json](../../references/canonical_run_manifest.json).

The prediction script feeds Stanza the **gold token sequence** of each sentence.
For every word the output file keeps gold `ID`, `FORM` and `MISC`, and replaces
`LEMMA`, `UPOS`, `XPOS`, `FEATS`, `HEAD` and `DEPREL` with Stanza's predictions.
`DEPS` is written as `_`.

This is an **aligned** evaluation in the sense used throughout this repository:
differences in sentence splitting or tokenisation cannot affect the scores.
Consequently the evaluator's `Sentences`, `Tokens` and `Words` rows are **100.00
by construction** — they are an integrity check that the alignment held, not a
quality result.

## Environment

Containerised so that the Stanza and PyTorch versions are explicit and isolated
from the host. Build files: [docker/Dockerfile.stanza](../../docker/Dockerfile.stanza)
and [docker-compose.stanza.yml](../../docker-compose.stanza.yml).

| | Stanza 1.13 (`stanza113`) | Stanza 1.14 (`stanza114`) |
|---|---|---|
| stanza | 1.13.0 | 1.14.0 |
| torch | 2.0.1+cu118 | 2.6.0+cu118 |
| image | `conllu-stanza:1.13.0` | `conllu-stanza:1.14.0` |
| cache | `/mnt/local-hddpool/niveshull/stanza-eval/1.13` | `…/1.14` |

Base image `python:3.10-slim`, resolved at build time to
`sha256:63669fd2563fa90b0442fa7b568e66e3667755636cda086d7bcaaa895f66fe39`
(the Dockerfile refers to the tag, not the digest).

Common pins in both images: `numpy==1.26.4`, `typing-extensions==4.10.0`,
`transformers==4.35.2`, `huggingface-hub==0.19.4`, `accelerate==0.24.1`,
`peft==0.6.2`. Complete snapshots: [`environment/`](environment/).

Server: 2 × NVIDIA GeForce GTX 1080 Ti, driver 560.35.05, host CUDA 12.6,
Docker Compose v5.4.0. Caches are mounted at `/cache` per version, with
`STANZA_RESOURCES_DIR=/cache/stanza`, `HF_HOME=/cache/huggingface`,
`TORCH_HOME=/cache/torch`. The 1.13 and 1.14 caches are deliberately separate so
neither release can reuse the other's model files or transformer downloads.

### Why the two releases run on different PyTorch versions

Stanza 1.14 ships a new Slovenian lemmatizer checkpoint that is loaded with
`torch.load(..., weights_only=True)`. Under `torch 2.0.1+cu118` this failed with
`_pickle.UnpicklingError: Weights only load failed. Unsupported class
_codecs.encode`, and that PyTorch version has no
`torch.serialization.add_safe_globals`. The 1.14 image was therefore built on
`torch 2.6.0+cu118`; the already-validated 1.13 image was left on 2.0.1+cu118.

This is a confound between the two arms, so it was controlled for — see
[control-torch2.6.md](control-torch2.6.md).

### Other setup constraints

- An unconstrained transformer install pulled a PyTorch/CUDA build unsuitable for
  the server's driver, so CUDA 11.8 wheels are pinned explicitly.
- `peft==0.6.2` without an Accelerate pin pulled a version that failed importing
  `split_torch_state_dict_into_shards` against `huggingface-hub==0.19.4`; hence
  `accelerate==0.24.1`.
- `default_accurate` requires the external transformer `EMBEDDIA/crosloengual-bert`
  (~499 MB), downloaded into each version's Hugging Face cache before prediction.
- Transformers emits non-fatal `torch.utils._pytree` deprecation warnings under
  the 1.14 environment.

## Reproducing

```bash
# 1. gold data — must match the SHA-256 above
sha256sum data/gold/sl_ssj-ud-test.conllu

# 2. build
docker compose -f docker-compose.stanza.yml build stanza113 stanza114

# 3. models, per version (repeat with stanza114)
docker compose -f docker-compose.stanza.yml run --rm stanza113 \
  python -c "import stanza; stanza.download('sl')"
docker compose -f docker-compose.stanza.yml run --rm stanza113 \
  python -c "import stanza; stanza.download('sl', package='default_accurate')"

# for a fresh default_accurate cache, also pre-fetch the transformer:
docker compose -f docker-compose.stanza.yml run --rm stanza114 \
  python -c "from transformers import AutoModel, AutoTokenizer; \
  AutoTokenizer.from_pretrained('EMBEDDIA/crosloengual-bert'); \
  AutoModel.from_pretrained('EMBEDDIA/crosloengual-bert')"

# 4. predict — 4×, varying service (stanza113|stanza114) and --package
#    (default|default_accurate) to match the output filename
docker compose -f docker-compose.stanza.yml run --rm stanza113 \
  python scripts/predict_stanza.py \
  --gold data/gold/sl_ssj-ud-test.conllu \
  --package default \
  --output predictions/output/20260810-stanza-1.13-vs-1.14_sl-ssj-ud-test_full_stanza-1.13.0-default_aligned_predicted.conllu

# 5. evaluate — 4×, one per prediction file
python3 scripts/conll18_ud_eval_tag-based.py -v \
  data/gold/sl_ssj-ud-test.conllu \
  predictions/output/20260810-stanza-1.13-vs-1.14_sl-ssj-ud-test_full_stanza-1.13.0-default_aligned_predicted.conllu \
  | tee results/output/20260810-stanza-1.13-vs-1.14_sl-ssj-ud-test_full/main/stanza-1.13.0-default_aligned_eval.txt

# 6. token-level version diff (regenerates the change review)
python3 scripts/compare_stanza_versions.py
```

Naming: `…_stanza-<version>-<default|accurate>_aligned_predicted.conllu` for
predictions, `stanza-<version>-<default|accurate>_aligned_eval.txt` for evaluator
output.

## Implementation details

[scripts/predict_stanza.py](../../scripts/predict_stanza.py) builds the pipeline as:

```python
stanza.Pipeline("sl", package=args.package,
                processors="tokenize,pos,lemma,depparse",
                tokenize_pretokenized=True, use_gpu=True,
                download_method=None)
```

- `tokenize_pretokenized=True` — Stanza annotates the existing token sequence
  instead of tokenising freely.
- `download_method=None` — prediction never refreshes resources, so a run depends
  on the explicitly prepared cache rather than silently changing mid-evaluation.
- Sentences are submitted one at a time; the script aborts if Stanza returns a
  different sentence or token count, so a silent misalignment cannot occur.
- The gold reader keeps only rows with integer CoNLL-U IDs. **This assumes a
  treebank with no multiword tokens and no empty nodes** — verified true for SSJ
  test (0 and 0). Do not reuse the script unchanged on an MWT treebank.
- Gold `MISC` is copied through, which includes SSJ's `NER=` values. Those are
  **gold annotation, not Stanza output**; the evaluator ignores `MISC` entirely.
- Stanza sorts `FEATS` case-sensitively, so ~173 rows per file are not in UD's
  canonical feature order (e.g. `NumForm` before `Number`). The evaluator
  re-sorts `FEATS` at load, so official metrics are unaffected — but normalise
  before comparing `FEATS` as raw strings outside the evaluator.

## Headline result

On this test set the release upgrade changes very little, while the package
choice matters a lot:

- `default`: **LAS 90.73** under both releases. `default_accurate`: **94.85 →
  94.86**.
- `UPOS`, `XPOS` and `FEATS` output is **byte-identical between 1.13.0 and
  1.14.0 in both packages** (25,442/25,442 tokens).
- Only **61** (`default`) and **57** (`default_accurate`) token rows out of
  25,442 differ between the releases at all.
- `default_accurate` gains roughly **+4.1 LAS** over `default` in both releases.

These counts are descriptive. **No significance test was performed**, and the
per-token fix/regression tallies are far too small to support a claim that
either release is better.

Full metrics and the complete token-level analysis:
[`results/output/20260810-stanza-1.13-vs-1.14_sl-ssj-ud-test_full/main/`](../../results/output/20260810-stanza-1.13-vs-1.14_sl-ssj-ud-test_full/main/)

## Files

Generated predictions — [`predictions/output/`](../../predictions/output/), prefix
`20260810-stanza-1.13-vs-1.14_sl-ssj-ud-test_full_`:

- `…_stanza-1.13.0-default_aligned_predicted.conllu`
- `…_stanza-1.13.0-accurate_aligned_predicted.conllu`
- `…_stanza-1.14.0-default_aligned_predicted.conllu`
- `…_stanza-1.14.0-accurate_aligned_predicted.conllu`

Generated results — [`results/output/20260810-stanza-1.13-vs-1.14_sl-ssj-ud-test_full/main/`](../../results/output/20260810-stanza-1.13-vs-1.14_sl-ssj-ud-test_full/main/):

- `stanza-1.13.0-default_aligned_eval.txt`, `stanza-1.13.0-accurate_aligned_eval.txt`
- `stanza-1.14.0-default_aligned_eval.txt`, `stanza-1.14.0-accurate_aligned_eval.txt`
- `stanza-1.13-vs-1.14-change-review.md` — every token whose prediction changed
  between the releases, classified against gold

Code — [scripts/predict_stanza.py](../../scripts/predict_stanza.py),
[scripts/compare_stanza_versions.py](../../scripts/compare_stanza_versions.py),
[scripts/conll18_ud_eval_tag-based.py](../../scripts/conll18_ud_eval_tag-based.py).

## Provenance

[manifest.json](manifest.json) is the machine-readable record: dataset identity,
evaluation design, server and Docker environment, package conditions, SHA-256 for
every input, script and output, and the expected metrics.

Local Docker image IDs for the completed run are recorded there and in the
environment table above. They change on rebuild, so the Dockerfile, Compose file
and [`environment/`](environment/) pip-freeze snapshots are the portable record.

## Verification / QA

This run does not go through `scripts/run_pipeline.py`, so it has no generated
`main/qa_validation.md` — that validator expects the Trankit/CLASSLA filename
contract.

Before the full runs, two-sentence smoke tests were used to verify pipeline
loading, GPU inference, package selection, CoNLL-U output, alignment and
evaluator compatibility. These were functional preflight checks only, and **their
prediction files were not retained**; their scores are not evaluation results.

The following were checked directly against the committed artifacts:

- All 17 manifest `file_hashes` recomputed and matched; `expected_metrics`
  reproduced exactly by re-running the evaluator on all four prediction files.
- Gold parsed independently: 1,282 sentences / 25,442 words / 0 MWT / 0 empty
  nodes, every row 10 columns.
- All four prediction files: `ID`, `FORM` and `MISC` identical to gold on
  25,442/25,442 rows; `DEPS` `_` throughout; sentence comments identical; the six
  predicted fields all well below 100% agreement with gold, i.e. **no gold-label
  leakage**.
- All four are valid dependency trees: exactly one `HEAD=0` per sentence, no
  cycles, no self-loops, heads in range, `root` label consistent with `HEAD=0`.
- `stanza-1.13-vs-1.14-change-review.md` regenerates byte-identically from
  `scripts/compare_stanza_versions.py`; all 118 entries (143 field rows) were
  re-derived from gold and both prediction files with no mismatches.

## Known limitations

1. **Model artifacts are not pinned.** The manifest records the Stanza *library*
   versions and packages, but not which model files each condition loaded — no
   `resources.json` version, no model filenames or hashes. This comparison is
   therefore "1.13 vs 1.14 as they resolved on 2026-08-10". Closing this needs
   information from the CJVT server; see `model_artifacts_todo` in
   [manifest.json](manifest.json).
2. **The byte-identical POS output is unexplained.** `UPOS`/`XPOS`/`FEATS` do not
   differ at all between releases, which suggests the tagger artifacts may be the
   same files. Item 1 would settle it.
3. **The lemmatizer asymmetry is unexplained.** Stanza 1.14 ships a new Slovenian
   lemmatizer checkpoint, yet lemma output changed in 43 tokens under
   `default_accurate` and in **zero** tokens under `default`.
4. **The PyTorch confound is only controlled in one direction.** 1.13 was rerun
   under torch 2.6.0 with identical output; 1.14 cannot run under torch 2.0.1 at
   all. The control's own outputs were not retained — see
   [control-torch2.6.md](control-torch2.6.md).
5. **Single run per condition**, no seed/determinism statement. The control run
   is the only evidence of run-to-run stability.
6. **No statistical testing.** See the headline note above.
