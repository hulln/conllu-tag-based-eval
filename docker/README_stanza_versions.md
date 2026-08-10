# Stanza 1.13.0 vs 1.14.0 on SSJ-UD

Reproducible comparison of **Stanza 1.13.0** and **Stanza 1.14.0** on the
Slovenian **SSJ-UD test set**, using fixed gold sentence/token boundaries and
the same CoNLL-U evaluator already used elsewhere in this repository.

The comparison was run on the **CJVT GPU server** on **2026-08-10**.

The main purpose was to compare the two Stanza releases under two package
configurations:

1. Stanza 1.13.0 — `default`
2. Stanza 1.13.0 — `default_accurate`
3. Stanza 1.14.0 — `default`
4. Stanza 1.14.0 — `default_accurate`

The evaluation covers lemma, POS/morphology and dependency annotation. Gold
sentence segmentation and tokenisation are fixed.

---

## 1. Evaluation design

All four systems are evaluated on exactly the same SSJ test set.

The prediction pipeline receives the gold token sequence for each sentence.
Stanza therefore does **not** decide sentence or token boundaries in this
evaluation.

For each syntactic word, the prediction file keeps:

* gold `ID`;
* gold `FORM`;
* gold `MISC`;

and replaces the evaluated linguistic annotation with Stanza predictions:

* `LEMMA`;
* `UPOS`;
* `XPOS`;
* `FEATS`;
* `HEAD`;
* `DEPREL`.

`DEPS` is written as `_`.

This is therefore an **aligned evaluation**: differences in sentence splitting
or tokenisation do not affect the scores.

The prediction script is:

```text
scripts/predict_stanza.py
```

Evaluation uses the existing repository evaluator:

```text
scripts/conll18_ud_eval_tag-based.py
```

---

## 2. Gold data

Dataset:

**UD Slovenian SSJ**

Repository:

```text
https://github.com/UniversalDependencies/UD_Slovenian-SSJ
```

Release used:

```text
r2.17 / UD v2.17
```

Local file:

```text
data/gold/sl_ssj-ud-test.conllu
```

The gold directory is local-only / gitignored, as in the other evaluation
workflows in this repository.

### Verified properties

Number of sentences:

```text
1,282
```

Number of syntactic word rows:

```text
25,442
```

Multiword-token rows:

```text
0
```

Empty-node rows:

```text
0
```

SHA-256:

```text
c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0
```

This hash is the same SSJ test file already used by the canonical evaluation
run in this repository.

The hash was checked with:

```bash
sha256sum data/gold/sl_ssj-ud-test.conllu
```

Sentence count was checked from `sent_id` comments, and syntactic words were
counted from rows with integer CoNLL-U IDs.

---

## 3. Server environment

The comparison was run on the CJVT server rather than in the host Python
environment.

Repository checkout during this run:

```text
/home/niveshull/conllu-tag-based-eval
```

Git branch:

```text
stanza-1.13-vs-1.14
```

The repository itself is small and may live in the user home directory.

Large models and caches are kept on the server HDD pool:

```text
/mnt/local-hddpool/niveshull/stanza-eval/
```

with separate directories for the two Stanza versions:

```text
/mnt/local-hddpool/niveshull/stanza-eval/1.13
/mnt/local-hddpool/niveshull/stanza-eval/1.14
```

This separation is intentional. It prevents one Stanza release from
accidentally reusing model files or transformer caches downloaded for the other
release.

### GPU

Server GPUs observed during setup:

```text
2 × NVIDIA GeForce GTX 1080 Ti
```

Observed NVIDIA driver:

```text
560.35.05
```

Host-reported CUDA version:

```text
12.6
```

The containers use CUDA-enabled PyTorch wheels and access the GPU through
Docker.

Docker Compose GPU access is configured with:

```yaml
gpus: all
```

GPU availability was explicitly verified inside the containers with
`torch.cuda.is_available()`.

Observed GPU device inside Docker:

```text
NVIDIA GeForce GTX 1080 Ti
```

Docker Compose observed during setup:

```text
Docker Compose v5.4.0
```

---

## 4. Why Docker is used

The comparison is containerised so that the Stanza and PyTorch versions are
explicit and isolated from the host environment.

No host-level Python packages are required for Stanza inference.

The Docker build is defined in:

```text
docker/Dockerfile.stanza
```

and the two evaluation environments are defined in:

```text
docker-compose.stanza.yml
```

The project directory is mounted into the container as:

```text
/project
```

The version-specific HDD-pool directory is mounted as:

```text
/cache
```

Within each cache:

```text
/cache/stanza
/cache/huggingface
/cache/torch
```

are used for Stanza resources, Hugging Face models and PyTorch resources.

Corresponding environment variables are:

```text
STANZA_RESOURCES_DIR=/cache/stanza
HF_HOME=/cache/huggingface
TORCH_HOME=/cache/torch
```

---

## 5. Software versions

Both images use:

```text
python:3.10-slim
```

The base image resolved during the 2026-08-10 build to:

```text
sha256:63669fd2563fa90b0442fa7b568e66e3667755636cda086d7bcaaa895f66fe39
```

The Dockerfile currently refers to the `python:3.10-slim` tag rather than
pinning that digest directly.

Common Python dependencies:

```text
numpy              1.26.4
typing-extensions  4.10.0
transformers       4.35.2
huggingface-hub    0.19.4
accelerate         0.24.1
peft               0.6.2
```

### Stanza 1.13 environment

```text
stanza  1.13.0
torch   2.0.1+cu118
```

### Stanza 1.14 environment

```text
stanza  1.14.0
torch   2.6.0+cu118
```

The different PyTorch versions are intentional and are explained below.

---

## 6. Docker configuration

The Dockerfile accepts the Stanza and PyTorch versions as build arguments.

Conceptually:

```dockerfile
FROM python:3.10-slim

ARG STANZA_VERSION
ARG TORCH_VERSION="2.0.1+cu118"

RUN pip install --no-cache-dir numpy==1.26.4 typing-extensions==4.10.0 \
    && pip install --no-cache-dir "torch==${TORCH_VERSION}" \
       --extra-index-url https://download.pytorch.org/whl/cu118 \
    && pip install --no-cache-dir \
       transformers==4.35.2 \
       huggingface-hub==0.19.4 \
       accelerate==0.24.1 \
       peft==0.6.2 \
    && pip install --no-cache-dir "stanza==${STANZA_VERSION}"

WORKDIR /project
CMD ["bash"]
```

The Compose services build two images:

```text
conllu-stanza:1.13.0
conllu-stanza:1.14.0
```

The 1.13 service uses the Dockerfile default:

```text
TORCH_VERSION=2.0.1+cu118
```

The 1.14 service overrides it with:

```text
TORCH_VERSION=2.6.0+cu118
```

---

## 7. Dependency issues encountered during setup

Several dependency problems were encountered while creating a reproducible
environment. They are documented here because the final pins are not arbitrary.

### 7.1 Initial Stanza transformer installation selected an unsuitable PyTorch build

An initial attempt using Stanza's transformer dependencies allowed pip to pull
a much newer PyTorch/CUDA combination.

That environment ended up with a CUDA build which was not appropriate for the
server's NVIDIA driver environment, and GPU inference was unavailable.

The Docker setup was therefore changed to install an explicit CUDA 11.8
PyTorch wheel.

For the original Stanza 1.13 setup, the working version was:

```text
torch==2.0.1+cu118
```

This matched the generation of the PyTorch stack already used in earlier CJVT
evaluation work and successfully detected the GTX 1080 Ti.

---

### 7.2 `peft` / `accelerate` / `huggingface-hub` incompatibility

The transformer stack was initially pinned to:

```text
transformers==4.35.2
huggingface-hub==0.19.4
peft==0.6.2
```

Installing `peft==0.6.2` without an explicit Accelerate pin pulled a newer
Accelerate version.

That version expected a newer `huggingface-hub` API and failed with an import
error involving:

```text
split_torch_state_dict_into_shards
```

The compatible Accelerate version was therefore explicitly pinned:

```text
accelerate==0.24.1
```

This satisfies the PEFT requirement while remaining compatible with the pinned
Hugging Face Hub version.

---

### 7.3 `default_accurate` requires an external transformer model

The Slovenian `default_accurate` package uses:

```text
EMBEDDIA/crosloengual-bert
```

The Stanza model download does not by itself guarantee that all Hugging Face
transformer files required at runtime are already present in a fresh cache.

Because the 1.13 and 1.14 caches are deliberately separate, the transformer
had to be downloaded separately for the 1.14 cache.

It was cached with:

```bash
docker compose -f docker-compose.stanza.yml run --rm stanza114 \
  python -c "from transformers import AutoModel, AutoTokenizer; \
  AutoTokenizer.from_pretrained('EMBEDDIA/crosloengual-bert'); \
  AutoModel.from_pretrained('EMBEDDIA/crosloengual-bert'); \
  print('Downloaded crosloengual-bert')"
```

Files downloaded included the approximately 499 MB model checkpoint.

After the cache was populated, the evaluation could run without fetching the
transformer during prediction.

---

### 7.4 Stanza 1.14 lemmatizer incompatibility with PyTorch 2.0.1

Stanza 1.14 introduced a new Slovenian lemmatizer/model representation.

The Stanza 1.14 release notes explicitly state that lemmatizer models from
Stanza 1.13 are not compatible with Stanza 1.14 and must be re-downloaded or
converted.

The 1.14 lemmatizer is loaded using PyTorch safe checkpoint loading:

```text
torch.load(..., weights_only=True)
```

When the Stanza 1.14 `default_accurate` model was tested under:

```text
torch 2.0.1+cu118
```

loading failed with:

```text
_pickle.UnpicklingError:
Weights only load failed.
Unsupported class _codecs.encode
```

PyTorch 2.0.1 also did not provide:

```text
torch.serialization.add_safe_globals
```

This showed that the old PyTorch version did not have the newer safe-loading
machinery needed by the Stanza 1.14 checkpoint.

The 1.14 image was therefore changed to:

```text
torch==2.6.0+cu118
```

After rebuilding, the following checks succeeded:

```text
stanza 1.14.0
torch 2.6.0+cu118
cuda True
safe_globals True
```

The Stanza 1.13 image was **not** changed and remains on:

```text
torch==2.0.1+cu118
```

This preserves the already completed and validated 1.13 environment.

---

### 7.5 Non-blocking PyTorch/Transformers warnings

Under the Stanza 1.14 environment, Transformers emits warnings such as:

```text
FutureWarning:
torch.utils._pytree._register_pytree_node is deprecated
```

These warnings do not prevent model loading or inference and did not affect
the completed evaluation.

They result from the older pinned Transformers version calling an API that is
deprecated in the newer PyTorch version.

No package was changed merely to suppress these warnings, because the working
environment was already reproducible and the warnings were non-fatal.

---

## 8. Downloading Stanza models

### Stanza 1.13

Default Slovenian package:

```bash
docker compose -f docker-compose.stanza.yml run --rm stanza113 \
  python -c "import stanza; stanza.download('sl')"
```

Accurate package:

```bash
docker compose -f docker-compose.stanza.yml run --rm stanza113 \
  python -c "import stanza; stanza.download('sl', package='default_accurate')"
```

Resources are stored under:

```text
/mnt/local-hddpool/niveshull/stanza-eval/1.13/stanza
```

---

### Stanza 1.14

Default Slovenian package:

```bash
docker compose -f docker-compose.stanza.yml run --rm stanza114 \
  python -c "import stanza; stanza.download('sl')"
```

Accurate package:

```bash
docker compose -f docker-compose.stanza.yml run --rm stanza114 \
  python -c "import stanza; stanza.download('sl', package='default_accurate')"
```

Resources are stored under:

```text
/mnt/local-hddpool/niveshull/stanza-eval/1.14/stanza
```

For Stanza 1.14, the available Slovenian package names were verified from
`resources.json`:

```text
default
default_fast
default_accurate
combined
ssj
sst
```

---

## 9. Prediction script

Predictions are produced with:

```text
scripts/predict_stanza.py
```

The Stanza pipeline is created with:

```python
stanza.Pipeline(
    "sl",
    package=args.package,
    processors="tokenize,pos,lemma,depparse",
    tokenize_pretokenized=True,
    use_gpu=True,
    download_method=None,
)
```

Important details:

### `tokenize_pretokenized=True`

The input is already tokenised according to the SSJ gold file.

Stanza therefore predicts annotation over the existing token sequence instead
of performing free tokenisation.

### `use_gpu=True`

Both version environments were tested with GPU availability before the full
runs.

### `download_method=None`

The actual prediction runs do not refresh/download Stanza resources
automatically.

This makes the run depend on the explicitly prepared cache rather than
silently changing resources during evaluation.

The external Hugging Face transformer needed by `default_accurate` must
likewise already exist in the corresponding version-specific cache.

---

## 10. Smoke tests

Before running the complete SSJ test set, a local two-sentence file was used:

```text
data/gold/ssj-smoke-2.conllu
```

It contains the first two SSJ sentences and was used only to verify that:

* the pipeline loads;
* GPU inference works;
* the expected Stanza package is used;
* output is valid CoNLL-U;
* token/word alignment remains 100%;
* the evaluator accepts the output.

Smoke predictions were written to:

```text
predictions/stanza/ssj-smoke-2-stanza113-default.conllu
predictions/stanza/ssj-smoke-2-stanza113-accurate.conllu
predictions/stanza/ssj-smoke-2-stanza114-default.conllu
predictions/stanza/ssj-smoke-2-stanza114-accurate.conllu
```

These files are **functional/preflight artifacts only**.

Their scores must not be interpreted as evaluation results because they cover
only two sentences.

---

## 11. Full prediction commands

### Stanza 1.13.0 — default

```bash
docker compose -f docker-compose.stanza.yml run --rm stanza113 \
  python scripts/predict_stanza.py \
  --gold data/gold/sl_ssj-ud-test.conllu \
  --output predictions/stanza/stanza-1.13.0-default-ssj.conllu \
  --package default
```

### Stanza 1.13.0 — default_accurate

```bash
docker compose -f docker-compose.stanza.yml run --rm stanza113 \
  python scripts/predict_stanza.py \
  --gold data/gold/sl_ssj-ud-test.conllu \
  --output predictions/stanza/stanza-1.13.0-accurate-ssj.conllu \
  --package default_accurate
```

### Stanza 1.14.0 — default

```bash
docker compose -f docker-compose.stanza.yml run --rm stanza114 \
  python scripts/predict_stanza.py \
  --gold data/gold/sl_ssj-ud-test.conllu \
  --output predictions/stanza/stanza-1.14.0-default-ssj.conllu \
  --package default
```

### Stanza 1.14.0 — default_accurate

```bash
docker compose -f docker-compose.stanza.yml run --rm stanza114 \
  python scripts/predict_stanza.py \
  --gold data/gold/sl_ssj-ud-test.conllu \
  --output predictions/stanza/stanza-1.14.0-accurate-ssj.conllu \
  --package default_accurate
```

Each full run processed:

```text
1282/1282 sentences
```

---

## 12. Evaluation commands

Evaluation uses:

```text
scripts/conll18_ud_eval_tag-based.py
```

### Stanza 1.13.0 — default

```bash
python3 scripts/conll18_ud_eval_tag-based.py -v \
  data/gold/sl_ssj-ud-test.conllu \
  predictions/stanza/stanza-1.13.0-default-ssj.conllu \
  | tee results/stanza/stanza-1.13.0-default-ssj-eval.txt
```

### Stanza 1.13.0 — default_accurate

```bash
python3 scripts/conll18_ud_eval_tag-based.py -v \
  data/gold/sl_ssj-ud-test.conllu \
  predictions/stanza/stanza-1.13.0-accurate-ssj.conllu \
  | tee results/stanza/stanza-1.13.0-accurate-ssj-eval.txt
```

### Stanza 1.14.0 — default

```bash
python3 scripts/conll18_ud_eval_tag-based.py -v \
  data/gold/sl_ssj-ud-test.conllu \
  predictions/stanza/stanza-1.14.0-default-ssj.conllu \
  | tee results/stanza/stanza-1.14.0-default-ssj-eval.txt
```

### Stanza 1.14.0 — default_accurate

```bash
python3 scripts/conll18_ud_eval_tag-based.py -v \
  data/gold/sl_ssj-ud-test.conllu \
  predictions/stanza/stanza-1.14.0-accurate-ssj.conllu \
  | tee results/stanza/stanza-1.14.0-accurate-ssj-eval.txt
```

---

## 13. Results

All four prediction files achieved:

```text
Sentences  100.00
Tokens     100.00
Words      100.00
```

confirming complete alignment with the gold test set.

### Main metrics

| Version | Package          |   LAS |   UAS |  UPOS |  XPOS | UFeats | Lemmas | AllTags |
| ------- | ---------------- | ----: | ----: | ----: | ----: | -----: | -----: | ------: |
| 1.13.0  | default          | 90.73 | 92.40 | 98.59 | 96.32 |  96.60 |  98.76 |   95.83 |
| 1.13.0  | default_accurate | 94.85 | 95.98 | 99.14 | 97.98 |  98.16 |  98.92 |   97.69 |
| 1.14.0  | default          | 90.73 | 92.40 | 98.59 | 96.32 |  96.60 |  98.76 |   95.83 |
| 1.14.0  | default_accurate | 94.86 | 95.98 | 99.14 | 97.98 |  98.16 |  98.89 |   97.69 |

### Composite dependency metrics

| Version | Package          | BLEX F1 | CLAS F1 | MLAS F1 |
| ------- | ---------------- | ------: | ------: | ------: |
| 1.13.0  | default          |   87.11 |   88.38 |   84.26 |
| 1.13.0  | default_accurate |   91.91 |   93.33 |   90.48 |
| 1.14.0  | default          |   87.11 |   88.38 |   84.22 |
| 1.14.0  | default_accurate |   91.88 |   93.34 |   90.49 |

Full evaluator output is stored in:

```text
results/stanza/
```

Files:

```text
stanza-1.13.0-default-ssj-eval.txt
stanza-1.13.0-accurate-ssj-eval.txt
stanza-1.14.0-default-ssj-eval.txt
stanza-1.14.0-accurate-ssj-eval.txt
```

Full predictions are stored in:

```text
predictions/
```

---

## 14. Interpretation

On this fixed SSJ test set, there is almost no aggregate difference between
Stanza 1.13.0 and 1.14.0 when the same package class is compared.

For `default`, the main reported metrics are identical to two decimal places:

```text
LAS     90.73
UAS     92.40
UPOS    98.59
XPOS    96.32
UFeats  96.60
Lemmas  98.76
```

For `default_accurate`, the differences between releases are also extremely
small:

```text
LAS:     94.85 -> 94.86
UAS:     95.98 -> 95.98
UPOS:    99.14 -> 99.14
XPOS:    97.98 -> 97.98
UFeats:  98.16 -> 98.16
Lemmas:  98.92 -> 98.89
```

The much larger difference is between the **package configurations**.

`default_accurate` substantially outperforms `default` on dependency metrics
in both releases.

For example:

```text
Stanza 1.13:
LAS 90.73 -> 94.85

Stanza 1.14:
LAS 90.73 -> 94.86
```

The aggregate results therefore suggest that, on this SSJ test set, moving from
Stanza 1.13.0 to 1.14.0 changes overall accuracy very little, whereas selecting
`default_accurate` instead of `default` has a clear effect.

Aggregate equality does **not** imply that the two releases produce identical
annotations token by token. A separate prediction-level diff would be needed
to identify cases where improvements and regressions cancel out in the overall
metrics.

---

## 15. Reproducing the comparison

### 15.1 Obtain the gold data

Place the SSJ r2.17 test file at:

```text
data/gold/sl_ssj-ud-test.conllu
```

Verify:

```bash
sha256sum data/gold/sl_ssj-ud-test.conllu
```

Expected SHA-256:

```text
c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0
```

---

### 15.2 Prepare cache directories

On the CJVT server:

```bash
mkdir -p /mnt/local-hddpool/niveshull/stanza-eval/1.13
mkdir -p /mnt/local-hddpool/niveshull/stanza-eval/1.14
```

The paths are CJVT/user-specific. On another machine, adjust the Compose volume
mounts accordingly.

---

### 15.3 Build the images

```bash
docker compose -f docker-compose.stanza.yml build stanza113
docker compose -f docker-compose.stanza.yml build stanza114
```

---

### 15.4 Check runtime versions and GPU

For 1.13:

```bash
docker compose -f docker-compose.stanza.yml run --rm stanza113 \
  python -c "import stanza, torch; \
  print('stanza', stanza.__version__); \
  print('torch', torch.__version__); \
  print('cuda', torch.cuda.is_available()); \
  print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no GPU')"
```

Expected core versions:

```text
stanza 1.13.0
torch 2.0.1+cu118
cuda True
```

For 1.14:

```bash
docker compose -f docker-compose.stanza.yml run --rm stanza114 \
  python -c "import stanza, torch; \
  print('stanza', stanza.__version__); \
  print('torch', torch.__version__); \
  print('cuda', torch.cuda.is_available()); \
  print('safe_globals', hasattr(torch.serialization, 'add_safe_globals'))"
```

Expected core versions:

```text
stanza 1.14.0
torch 2.6.0+cu118
cuda True
safe_globals True
```

---

### 15.5 Download models

Download `default` and `default_accurate` for both versions using the commands
in section 8.

For each fresh `default_accurate` cache, also make sure
`EMBEDDIA/crosloengual-bert` is available under `HF_HOME`.

---

### 15.6 Run predictions

Run all four commands from section 11.

---

### 15.7 Evaluate

Run all four evaluator commands from section 12.

Verify that:

```text
Sentences = 100.00
Tokens    = 100.00
Words     = 100.00
```

for every condition.

---

## 16. Files created for this comparison

Code/configuration:

```text
docker/Dockerfile.stanza
docker-compose.stanza.yml
scripts/predict_stanza.py
docker/README_stanza_versions.md
```

Full prediction artifacts:

```text
predictions/stanza/stanza-1.13.0-default-ssj.conllu
predictions/stanza/stanza-1.13.0-accurate-ssj.conllu
predictions/stanza/stanza-1.14.0-default-ssj.conllu
predictions/stanza/stanza-1.14.0-accurate-ssj.conllu
```

Smoke-test prediction artifacts:

```text
predictions/stanza/ssj-smoke-2-stanza113-default.conllu
predictions/stanza/ssj-smoke-2-stanza113-accurate.conllu
predictions/stanza/ssj-smoke-2-stanza114-default.conllu
predictions/stanza/ssj-smoke-2-stanza114-accurate.conllu
```

Evaluation output:

```text
results/stanza/stanza-1.13.0-default-ssj-eval.txt
results/stanza/stanza-1.13.0-accurate-ssj-eval.txt
results/stanza/stanza-1.14.0-default-ssj-eval.txt
results/stanza/stanza-1.14.0-accurate-ssj-eval.txt
```

Local-only data:

```text
data/gold/sl_ssj-ud-test.conllu
data/gold/ssj-smoke-2.conllu
```

Large model and transformer caches remain outside Git under:

```text
/mnt/local-hddpool/niveshull/stanza-eval/
```

---

## 17. Reproducibility notes

The following points are important when reproducing or interpreting the run:

1. **Use the exact SSJ gold file.**
   The SHA-256 should match the value recorded above.

2. **Do not share model caches between Stanza 1.13 and 1.14.**
   Stanza 1.14 changed the lemmatizer model format.

3. **Do not assume PyTorch 2.0.1 works for the Stanza 1.14 Slovenian models.**
   The new lemmatizer failed under that version during this run.

4. **Prepare the Hugging Face transformer cache before offline prediction.**
   `default_accurate` requires `EMBEDDIA/crosloengual-bert`.

5. **Keep sentence/token boundaries fixed.**
   This comparison evaluates linguistic annotation, not tokenisation quality.

6. **Check 100% alignment after every run.**
   `Sentences`, `Tokens` and `Words` should all be 100%.

7. **Do not interpret the two-sentence smoke scores.**
   They are only functional checks.

8. **The two Stanza releases do not use the same PyTorch version in this
   reproducible setup.**
   This was necessary because of Stanza 1.14 model loading compatibility, not
   because different hardware or evaluation settings were intentionally being
   compared.

9. **All four systems were run on the same gold data, server class, GPU access,
   prediction script and evaluator.**

10. **Aggregate metrics can hide changed individual predictions.**
    Token-/sentence-level comparison should be performed separately if the goal
    is to analyse what specifically changed between Stanza 1.13 and 1.14.

---

## 18. Exact Python environment snapshots

For full reproducibility, the complete installed Python package environment
from each Docker image was captured with `pip freeze | sort`.

Files:

```text
references/stanza-1.13.0-pip-freeze.txt
references/stanza-1.14.0-pip-freeze.txt
```

They were generated with:

```bash
docker compose -f docker-compose.stanza.yml run --rm stanza113 \
  pip freeze | sort > references/stanza-1.13.0-pip-freeze.txt

docker compose -f docker-compose.stanza.yml run --rm stanza114 \
  pip freeze | sort > references/stanza-1.14.0-pip-freeze.txt
```

The important verified differences are:

```text
Stanza 1.13:
stanza==1.13.0
torch==2.0.1+cu118

Stanza 1.14:
stanza==1.14.0
torch==2.6.0+cu118
```

All other explicitly pinned core dependencies are the same between the two
environments:

```text
accelerate==0.24.1
huggingface-hub==0.19.4
numpy==1.26.4
peft==0.6.2
transformers==4.35.2
typing_extensions==4.10.0
```

The `pip-freeze` files are the authoritative record of the complete Python
package environments used for the evaluation.

---

## 19. Docker image IDs from the completed run

The Docker images used for the completed 2026-08-10 evaluation had these local
image IDs:

- `conllu-stanza:1.13.0` — `sha256:dbbc66d648e4f951022c4511086b9d6cc3f663eb453bb1dfc421772154d6217c`
- `conllu-stanza:1.14.0` — `sha256:52edf2dff5c8da66ef448be0390728ad3df7a8f9d49f19b94eb3f83d8b83fc14`

These IDs identify the exact locally built images used for this run. They may
change after rebuilding the images, so the Dockerfile, Compose configuration
and `pip-freeze` snapshots remain the portable reproducibility record.

---

## 20. Machine-readable reproducibility manifest

A machine-readable summary of this comparison is stored in:

`references/stanza_version_comparison_manifest.json`

It records the dataset identity and SHA-256, evaluation design, server and
Docker environment, Stanza/PyTorch versions, model-package conditions,
important setup and compatibility notes, exact file hashes, and expected
evaluation metrics.

The manifest complements this README: this file explains the workflow and
decisions in human-readable form, while the JSON provides exact values for
later verification.
