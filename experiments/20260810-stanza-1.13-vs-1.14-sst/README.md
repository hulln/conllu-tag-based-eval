# Stanza 1.13.0 vs 1.14.0 on UD Slovenian SST

Run stamp `20260810-stanza-1.13-vs-1.14` · CJVT GPU server · 2026-08-10

Companion to the SSJ run of the same stamp,
[`experiments/20260810-stanza-1.13-vs-1.14-ssj/`](../20260810-stanza-1.13-vs-1.14-ssj/).
Same code, same containers, same model caches, same four conditions — the only
difference is the test set. Environment snapshots and the shared model-provenance
audit are **not duplicated here**; this README links to them.

## Purpose

Does upgrading Stanza from **1.13.0** to **1.14.0** change Slovenian annotation
quality on the standardized SST-UD test set, and how does that compare to the
effect of choosing the `default_accurate` model package over `default`?

SST is spoken-language data and is considerably harder than the written SSJ test
set, so it is the more informative place to look for a release-to-release
improvement. The SSJ run had already shown almost no difference between the two
releases; this run asks whether the spoken-language set behaves differently.

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

**UD Slovenian SST** ([upstream](https://github.com/UniversalDependencies/UD_Slovenian-SST)),
local file `data/gold/sl_sst-ud-test.conllu` (gitignored, as elsewhere in this
repository).

```text
SHA-256              6824234edf98cbbedb2e981644c324a3058c2920ed6cdcd7f467e835cfe25eeb
Git blob             384138ac9791e96e8e030bfc9dfafd7de741dce8
Sentences            432
Syntactic word rows  11,443
Multiword tokens     0
Empty nodes          0
```

### Why this file, and not a newer UD release

These exact bytes are the official SST test file in **both** UD `r2.16` and
`r2.17` — the releases are byte-identical for this file, which is why the
repository's other documentation refers to it either way (see
[data/README.md](../../data/README.md)).

UD `r2.18` was released later and changes this treebank, in particular by
enriching metadata/`MISC`. This experiment deliberately stays on the older
official file so that its scores remain comparable with the earlier SST
evaluations in this repository. **It is not an oversight, and it should not be
silently upgraded**; doing so would break continuity with
[`20260420-1105`](../20260420-1105/) and [`20260622-0810-tk13`](../20260622-0810-tk13/).

### Method

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

Identical to the SSJ run: the same two container images and the same two model
caches were used for both test sets on the same day.

| | Stanza 1.13 (`stanza113`) | Stanza 1.14 (`stanza114`) |
|---|---|---|
| stanza | 1.13.0 | 1.14.0 |
| torch | 2.0.1+cu118 | 2.6.0+cu118 |
| image | `conllu-stanza:1.13.0` | `conllu-stanza:1.14.0` |
| cache | `/mnt/local-hddpool/niveshull/stanza-eval/1.13` | `…/1.14` |

Build files: [docker/Dockerfile.stanza](../../docker/Dockerfile.stanza) and
[docker-compose.stanza.yml](../../docker-compose.stanza.yml). Complete pip-freeze
snapshots live once, with the SSJ run:
[`../20260810-stanza-1.13-vs-1.14-ssj/environment/`](../20260810-stanza-1.13-vs-1.14-ssj/environment/).

The full build rationale — why CUDA 11.8 wheels are pinned, why
`accelerate==0.24.1` is required, the `EMBEDDIA/crosloengual-bert` download for
`default_accurate`, and **why the two releases run on different PyTorch
versions** — is documented once in the
[SSJ experiment README](../20260810-stanza-1.13-vs-1.14-ssj/README.md#environment)
and is not repeated here.

## Reproducing

```bash
# 1. gold data — must match the SHA-256 above
sha256sum data/gold/sl_sst-ud-test.conllu

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
  --gold data/gold/sl_sst-ud-test.conllu \
  --package default \
  --output predictions/output/20260810-stanza-1.13-vs-1.14_sl-sst-ud-test_full_stanza-1.13.0-default_aligned_predicted.conllu

# 5. evaluate — 4×, one per prediction file
python3 scripts/conll18_ud_eval_tag-based.py -v \
  data/gold/sl_sst-ud-test.conllu \
  predictions/output/20260810-stanza-1.13-vs-1.14_sl-sst-ud-test_full_stanza-1.13.0-default_aligned_predicted.conllu \
  | tee results/output/20260810-stanza-1.13-vs-1.14_sl-sst-ud-test_full/main/stanza-1.13.0-default_aligned_eval.txt

# 6. token-level version diff (regenerates the change review)
python3 scripts/compare_stanza_versions_sst.py
```

Step 6 is deterministic and offline: it reads only the gold file and the four
committed prediction files, and rewrites the change review in place.

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
  treebank with no multiword tokens and no empty nodes** — verified true for the
  SST test file used here (0 and 0). Do not reuse the script unchanged on an MWT
  treebank.
- Gold `MISC` is copied through unchanged. On SST it carries the treebank's
  speech-corpus metadata (`Gos2.1_seg_id`, `Gos2.1_token_id`, `pronunciation`,
  `sentence_ending`). This is **gold annotation, not Stanza output**; the
  evaluator ignores `MISC` entirely.
- Stanza sorts `FEATS` case-sensitively, so 125 rows (`default`) and 124 rows
  (`default_accurate`) per file are not in UD's canonical feature order (e.g.
  `NumForm` before `Number`). The evaluator re-sorts `FEATS` at load, so official
  metrics are unaffected — but normalise before comparing `FEATS` as raw strings
  outside the evaluator.

## Headline result

On standardized SST the release upgrade again changes very little, while the
package choice has a much larger effect:

- `default`: **LAS 81.88 → 81.95** (+0.07). `default_accurate`:
  **86.11 → 86.13** (+0.02).
- The `UPOS`, `XPOS` and `UFeats` scores are identical between the releases in
  both packages — and not merely equal in aggregate: **zero** token rows differ
  in the underlying `UPOS`, `XPOS` and `FEATS` columns.
- `Lemmas` are identical under `default` (99.14) and change marginally under
  `default_accurate` (99.27 → 99.29).
- Only **56** (`default`) and **37** (`default_accurate`) token rows out of
  11,443 differ between the releases at all.
- `default_accurate` gains about **+4.2 LAS points** over `default` in both
  releases.

These are descriptive counts from single runs. **No significance test was
performed**, so the release differences must not be presented as statistically
significant, nor as statistical equivalence. The defensible summary is that the
release-to-release differences are extremely small in these runs, while
`default_accurate` is substantially better than `default`.

Full metrics:
[`results/output/20260810-stanza-1.13-vs-1.14_sl-sst-ud-test_full/main/`](../../results/output/20260810-stanza-1.13-vs-1.14_sl-sst-ud-test_full/main/).

## Token-level comparison

[`stanza-1.13-vs-1.14-change-review.md`](../../results/output/20260810-stanza-1.13-vs-1.14_sl-sst-ud-test_full/main/stanza-1.13-vs-1.14-change-review.md)
lists every token whose prediction changed between the releases, classified
against gold. Summary:

- **`default`** — 56 changed rows, all in the dependency fields. `HEAD` changed
  in 32 (15 fixes / 8 regressions / 9 both wrong); `DEPREL` in 46 (15 / 10 / 21).
- **`default_accurate`** — 37 changed rows. `LEMMA` changed in 10 (5 / 3 / 2),
  `HEAD` in 16 (10 / 5 / 1), `DEPREL` in 23 (6 / 8 / 9).
- Joint `HEAD`+`DEPREL` correctness — `default`: 15 fixes, 8 regressions, 33 both
  wrong, 0 both correct. `default_accurate`: 7 fixes, 4 regressions, 20 both
  wrong, 6 both correct.

**Terminology.** An *exact dependency fix* means the joint `HEAD`+`DEPREL`
result went from wrong to correct. It does **not** imply that both fields
changed — one field changing is enough to flip the joint outcome. The
per-field and joint tallies therefore do not sum to each other, by design.

## Model and resource provenance

The resolved model artifacts were audited after the run. The finding materially
constrains how this comparison may be described:

> The tokenizer, POS and dependency-parser checkpoints that the two conditions
> actually load are **byte-identical** between the 1.13 and 1.14 caches. The two
> combined lemmatizer checkpoints differ.

So this run does **not** reproduce the original Slovenian 1.13 default model
configuration against the 1.14 configuration: current 1.13 resource resolution
already points to the later combined POS and dependency-parser models. The Stanza
library versions and the lemmatizer checkpoints do still differ between the two
arms. The near-identical POS and dependency scores are consistent with the two
arms sharing the same POS and parser binaries, rather than providing evidence
about how two separately trained model sets compare.

The reason lies upstream: commit `654c7f7f` (2026-06-23) repointed the Slovenian
`default` and `default_accurate` packages in `resources_1.13.0.json` from `ssj_*`
to `combined_*` — five days *after* the 1.13.0 release. Installing 1.13 today
therefore resolves to a different Slovenian model set than 1.13 resolved to at
release time.

**The canonical record is
[references/stanza-1.13-vs-1.14-model-provenance.md](../../references/stanza-1.13-vs-1.14-model-provenance.md)**
— full chronology, before/after mapping tables, upstream MD5 cross-check, and an
explicit statement of what the audit does *not* establish. It covers this run and
the [SSJ companion run](../20260810-stanza-1.13-vs-1.14-ssj/) together, since both used
the same caches. Per-artifact SHA-256 values are in [manifest.json](manifest.json)
under `model_artifacts`.

## PyTorch control

The two arms do not share a PyTorch version (2.0.1+cu118 vs 2.6.0+cu118),
because Stanza 1.14's Slovenian lemmatizer will not load under the older torch.
That is a confound, so it was controlled: **Stanza 1.13.0 was rerun on SST under
`torch 2.6.0+cu118`** in image `conllu-stanza:1.13.0-torch2.6.0`.

Both control outputs were **byte-for-byte identical** to the original Stanza
1.13.0 + torch 2.0.1 SST predictions:

| Package | SHA-256 | Matches |
|---|---|---|
| `default` | `55f6103a91fe802c7e5df53efb8c6f3f8b4d85ac4513d80eb3c21adcc6844853` | `…_stanza-1.13.0-default_aligned_predicted.conllu` |
| `default_accurate` | `3a3888ebfcee7cfc5e5b980c23a6f7f1ab73eb47d22dae2d9c6867803d222a1e` | `…_stanza-1.13.0-accurate_aligned_predicted.conllu` |

Changing PyTorch 2.0.1 → 2.6.0 therefore did not change Stanza 1.13's SST output
in this control. The control is **one-directional** — 1.14 cannot be run under
torch 2.0.1 at all — so it does not exclude a PyTorch effect on the 1.14 arm.

The duplicate control prediction files were intentionally deleted once their
SHA-256 values had been recorded, so they are **not** in this repository; the
hashes above are the retained evidence. The equivalent SSJ control, including the
image build recipe needed to repeat either control, is documented in
[`../20260810-stanza-1.13-vs-1.14-ssj/control-torch2.6.md`](../20260810-stanza-1.13-vs-1.14-ssj/control-torch2.6.md).

## Files

Generated predictions — [`predictions/output/`](../../predictions/output/), prefix
`20260810-stanza-1.13-vs-1.14_sl-sst-ud-test_full_`:

- `…_stanza-1.13.0-default_aligned_predicted.conllu`
- `…_stanza-1.13.0-accurate_aligned_predicted.conllu`
- `…_stanza-1.14.0-default_aligned_predicted.conllu`
- `…_stanza-1.14.0-accurate_aligned_predicted.conllu`

Generated results — [`results/output/20260810-stanza-1.13-vs-1.14_sl-sst-ud-test_full/main/`](../../results/output/20260810-stanza-1.13-vs-1.14_sl-sst-ud-test_full/main/):

- `stanza-1.13.0-default_aligned_eval.txt`, `stanza-1.13.0-accurate_aligned_eval.txt`
- `stanza-1.14.0-default_aligned_eval.txt`, `stanza-1.14.0-accurate_aligned_eval.txt`
- `stanza-1.13-vs-1.14-change-review.md`

Code — [scripts/predict_stanza.py](../../scripts/predict_stanza.py),
[scripts/compare_stanza_versions_sst.py](../../scripts/compare_stanza_versions_sst.py),
[scripts/conll18_ud_eval_tag-based.py](../../scripts/conll18_ud_eval_tag-based.py).

## Provenance

[manifest.json](manifest.json) is the machine-readable record: dataset identity,
evaluation design, server and Docker environment, package conditions, resolved
model artifacts, the PyTorch control, SHA-256 for every input, script and output,
and the expected metrics.

Local Docker image IDs for the completed run are recorded there. They change on
rebuild, so the Dockerfile, Compose file and the shared
[`environment/`](../20260810-stanza-1.13-vs-1.14-ssj/environment/) pip-freeze
snapshots are the portable record.

## Verification / QA

This run does not go through `scripts/run_pipeline.py`, so it has no generated
`main/qa_validation.md`; that validator expects the Trankit/CLASSLA filename
contract. The following checks were performed directly on the SST artifacts.

Reproducible from this repository:

- All **17** `file_hashes` recorded in `manifest.json` recomputed and matched.
- Gold parsed independently as **432 sentences / 11,443 syntactic words / 0 MWT /
  0 empty nodes**, every row 10 columns; SHA-256 and Git blob ID as above.
- All four prediction files contain 11,443 aligned word rows across 432
  sentences. Gold `ID`, `FORM`, `MISC` and sentence comments are preserved
  exactly, and `DEPS` is `_` throughout.
- Every prediction file passed dependency-tree validation: exactly one root per
  sentence, no cycles, no self-loops, heads in range, and `root` labels
  consistent with `HEAD=0`.
- `expected_metrics` in the manifest matched the committed evaluator outputs on
  all 13 metrics × 4 conditions.
- `stanza-1.13-vs-1.14-change-review.md` regenerates **byte-identically** from
  `scripts/compare_stanza_versions_sst.py`.

Recorded from the run environment (server-side, not reproducible from this
repository):

- The version-specific `resources.json` files were identified as Stanza resource
  versions 1.13.0 and 1.14.0 and pinned by SHA-256 in the manifest.
- Every inspected model file matched the MD5 declared in its corresponding
  `resources.json`.
- The tokenizer, POS and dependency-parser checkpoints used by `default` and
  `default_accurate` are byte-identical across the two caches; the two combined
  lemmatizer checkpoints differ.
- The PyTorch control described above.

## Known limitations

1. **The evaluation uses the older official standardized SST test file**
   (byte-identical in UD `r2.16` and `r2.17`), intentionally, for continuity with
   the earlier SST evaluations. It is not the later `r2.18` file.
2. **This run does not reproduce the original 1.13 default configuration against
   the 1.14 configuration.** The POS and dependency checkpoints resolve to
   byte-identical files in both arms, because current 1.13 resource resolution
   already points to the later combined models — see
   [the provenance audit](../../references/stanza-1.13-vs-1.14-model-provenance.md).
   Of the model artifacts, only the lemmatizer checkpoints differ; the Stanza
   library versions differ as well.
3. **The Slovenian 1.13 defaults were repointed upstream after the 1.13
   release**, so "Stanza 1.13 vs 1.14" here means "as the two versions resolved
   on 2026-08-10", not "as they stood on their respective release dates". The
   historical resource *mappings* have been reconstructed; a **historical 1.13
   model run has not been performed**, so this repository holds no scores for the
   `ssj_*` model set 1.13 resolved to at release time — see
   [the provenance document](../../references/stanza-1.13-vs-1.14-model-provenance.md).
4. **Identical parser checkpoints still produce a small number of different
   dependency predictions.** The PyTorch control rules out the 2.0.1-vs-2.6.0
   difference for the 1.13 arm, but this experiment does not isolate which
   Stanza library change causes the remaining differences.
5. **Model binaries and `resources.json` snapshots are not committed.** Their
   hashes are recorded in `manifest.json`, but reproducing the exact model
   environment still requires obtaining artifacts that match those hashes.
6. **Single main run per condition.** The PyTorch control is evidence of stable
   output for Stanza 1.13 in this setup; no broader determinism study was
   performed.
7. **No statistical testing.** Release differences are reported descriptively and
   must not be described as statistically significant or statistically
   indistinguishable.
8. Gold `MISC` is preserved in prediction files. It is not fed to Stanza and is
   ignored by the evaluator, but the prediction files therefore contain gold-side
   metadata in fields outside the evaluated annotation columns.
