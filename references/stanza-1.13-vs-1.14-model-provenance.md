# Model provenance for the Stanza 1.13.0 vs 1.14.0 comparison

Follow-up provenance audit, **2026-08-11**, covering both runs of the
`20260810-stanza-1.13-vs-1.14` stamp:

- [`experiments/20260810-stanza-1.13-vs-1.14-ssj/`](../experiments/20260810-stanza-1.13-vs-1.14-ssj/) — SSJ
- [`experiments/20260810-stanza-1.13-vs-1.14-sst/`](../experiments/20260810-stanza-1.13-vs-1.14-sst/) — SST

Both runs were executed on 2026-08-10. This audit was performed **afterwards**,
on the caches those runs used and on the upstream resource history. It does not
change any score, prediction file or evaluator output; it changes how the
comparison should be interpreted.

The original SSJ manifest listed the unpinned model artifacts as an open item
(`model_artifacts_todo`). This document is the resolution of that item. It also
carries the upstream chronology and the two pinned release-time resource commits
used by the follow-up
[release-time reconstruction](../experiments/20260811-stanza-release-time-1.13-vs-1.14/).

## Why this matters

The headline framing "Stanza 1.13 vs Stanza 1.14" invites the reading that two
different generations of trained Slovenian models are being compared. On the
evidence below, that reading is **not** supported for the POS and dependency
components: in these caches both conditions resolve to the *same* model files.

## Resolved resource versions

Each container used its own `STANZA_RESOURCES_DIR`, so neither release could
reuse the other's downloads.

| | Stanza 1.13 arm | Stanza 1.14 arm |
|---|---|---|
| `DEFAULT_RESOURCES_VERSION` reported by the library | `1.13.0` | `1.14.0` |
| `resources.json` SHA-256 | `ad1104000ff4175881e2ef5eb4ded2d9082eefe52f053e98918b54926ede0594` | `4e41c1df152146fa26ed0c006a08feea7a60bb3414bb6d57dbda24ad2e3cb99c` |

The Slovenian package mappings are **identical** in the two resource versions:

| Package | tokenize | lemma | pos | depparse | transformer |
|---|---|---|---|---|---|
| `default` | `combined_nocharlm` | `combined_nocharlm` | `combined_charlm` | `combined_nocharlm` | — |
| `default_accurate` | `combined_charlm` | `combined_charlm` | `combined_crosloengual-bert` | `combined_crosloengual-bert` | `EMBEDDIA/crosloengual-bert` |

## Artifact comparison

Every inspected cache file matched the MD5 declared for it by its own
version-specific `resources.json`, so each cache is internally consistent.

Comparing the two caches against each other:

**Byte-identical between the 1.13 and 1.14 caches**

- tokenizer checkpoints (`combined_nocharlm`, `combined_charlm`)
- POS checkpoints (`combined_charlm`, `combined_crosloengual-bert`)
- dependency-parser checkpoints (`combined_nocharlm`, `combined_crosloengual-bert`)
- the inspected charLM and pretrain files
- the inspected NER files (not used by this experiment, which runs only
  `tokenize,pos,lemma,depparse`)

**Different between the two caches**

- `lemma` `combined_nocharlm`
- `lemma` `combined_charlm`
- `default.zip` (the package bundle — consistent with the lemmatizer change)

Per-file SHA-256 values are recorded under `model_artifacts` in
[the SST manifest](../experiments/20260810-stanza-1.13-vs-1.14-sst/manifest.json)
and [the SSJ manifest](../experiments/20260810-stanza-1.13-vs-1.14-ssj/manifest.json).

### Independent upstream corroboration

The cache comparison above was made server-side on the CJVT machine. It is
independently corroborated by the **MD5 values that upstream itself declares**
in the two versioned resource files, read directly from
`stanfordnlp/stanza-resources` on 2026-08-11:

| Slovenian model | MD5 in `resources_1.13.0.json` | MD5 in `resources_1.14.0.json` | |
|---|---|---|---|
| `pos` `combined_charlm` | `74240ce9ffbbe05e79b5ca6922223fa9` | `74240ce9ffbbe05e79b5ca6922223fa9` | same |
| `pos` `combined_crosloengual-bert` | `81efb4bf6671c538dae71da2b2113c0c` | `81efb4bf6671c538dae71da2b2113c0c` | same |
| `depparse` `combined_nocharlm` | `7b2d2d0f22ec8516a909dcf39dee30d1` | `7b2d2d0f22ec8516a909dcf39dee30d1` | same |
| `depparse` `combined_crosloengual-bert` | `c640d6c89966bf456a0f5ef526187550` | `c640d6c89966bf456a0f5ef526187550` | same |
| `lemma` `combined_charlm` | `bec8e49a13927cc132011e5c16e76c44` | `ed65f0e34223ec836654f7e1c49b9708` | **differ** |
| `lemma` `combined_nocharlm` | `b59036d16659a05bf7cc3c5d54313100` | `cb53c36fd0678f8244d6d254431b1087` | **differ** |

Upstream therefore *declares* the same POS and dependency-parser artifacts for
both resource versions, and different lemmatizers. The cache observation and the
upstream declaration agree.

### Consequence for the results

This explains what the run-level results already showed:

- `UPOS`, `XPOS` and `FEATS` predictions do **not** differ between the releases
  on either test set — 0 changed token rows in all four package/dataset
  combinations. The POS checkpoints are the same file.
- Lemma output differs only under `default_accurate` (43 tokens on SSJ, 10 on
  SST) and not at all under `default`, even though **both** combined
  lemmatizer checkpoints differ between the caches. The `nocharlm` lemmatizer
  change simply produced no different lemma on either test set.
- The remaining differences are in `HEAD`/`DEPREL`, produced by
  byte-identical parser checkpoints. See "What this does not establish" below.

## Upstream resource history

The relevant history is in the *versioned* resource files of
[`stanfordnlp/stanza-resources`](https://github.com/stanfordnlp/stanza-resources).
All commits below were read from the GitHub API on 2026-08-11; library release
dates come from PyPI.

### Chronology

| Date | Event |
|---|---|
| 2026-06-03 | `e29e2b5d` — `resources_1.13.0.json` created ("for the upcoming 1.13.0 model") |
| 2026-06-17 | `4b3990ca`, `9b46b7fe` — Slovenian BERT POS + NER added to `resources_1.13.0.json` |
| **2026-06-18** | **Stanza 1.13.0 released on PyPI** |
| **2026-06-23** | **`654c7f7f` — "Add a combined set of models and a charlm for SL…" — modifies `resources_1.13.0.json` (+115/−17). See below.** |
| 2026-06-25 | `8cbebe5e` — "Update with newer combined tokenizer, lemma, pos for Slovenian" (`resources_1.13.0.json`) |
| 2026-06-25 | `4847a9d4` — "Update SL lemmatizers with a dictionary" |
| 2026-06-25 | `aab5014f` — "Oops, needed the pretrain in the SL lemmatizer" — **last commit to touch `resources_1.13.0.json`** |
| 2026-06-26 | `2f5f337e`, `45a6e7dd` — `resources_1.14.0.json`: lemmatizers updated to "new, smaller versions" |
| 2026-06-29 | `79abac10` — "Sort all of the languages alphabetically. Should be the same (except we also updated the Slovenian lemmatizer, oops)" (`resources_1.14.0.json`) |
| 2026-06-30 | `8c4cedae` — aliases added to `resources_1.14.0.json` |
| **2026-07-15, 01:09 UTC** | `f016b8e9` — "Upgrade the EN tokenizers with more features…" — **modifies `resources_1.14.0.json`**, and is the **last commit to touch that file before the release**. Its changes to the file are confined to the English section |
| **2026-07-15, 01:58 UTC** | **Stanza 1.14.0 released on PyPI.** Release-time `stanza-resources` state pinned by the reconstruction: `f016b8e92f0ae9dd76729db44c4a582a72db2252` (see below) |
| 2026-07-16 | `f2976f2d` — more aliases (`resources_1.14.0.json`) — **post-release** |
| 2026-08-06 | `8048f8a1` — "Update lemmatizers for 1.14.0 to have forward & backward charlm args" — **post-release**, and the **last commit to touch `resources_1.14.0.json`** before the runs |
| 2026-08-10 | Both experiment runs executed |
| 2026-08-11 | This audit; release-time reconstruction experiment executed |

### The two pinned release-time resource commits

The follow-up reconstruction
([`experiments/20260811-stanza-release-time-1.13-vs-1.14/`](../experiments/20260811-stanza-release-time-1.13-vs-1.14/))
pins one `stanza-resources` commit per release:

| Release | Pinned commit | Pinned file | SHA-256 of that file |
|---|---|---|---|
| 1.13.0 (2026-06-18) | `9b46b7fe61df0ef466240f0ee19825cdc352af65` | `resources_1.13.0.json` | `77a07c185dd875edae3b15cf62be01491ae37477f8902275276f7bfa91f7a22b` |
| 1.14.0 (2026-07-15) | `f016b8e92f0ae9dd76729db44c4a582a72db2252` | `resources_1.14.0.json` | `dbaf5f0c740072df4f0c571c750073c21e5af4d23b277ca590f2b64400a58a84` |

Why each commit represents the **release-time** state of its file:

- **1.13.0 — `9b46b7fe`.** It is the last commit in the chronology above to touch
  `resources_1.13.0.json` before the 2026-06-18 release. Everything that
  repointed the Slovenian defaults from `ssj_*` to `combined_*` (`654c7f7f`,
  `8cbebe5e`, `4847a9d4`, `aab5014f`) comes **after** that release.
- **1.14.0 — `f016b8e9`.** It does modify `resources_1.14.0.json`, but it was
  committed on 2026-07-15 at 01:09 UTC, shortly before the 01:58 UTC PyPI
  release, and is the last commit to touch that file before it. Its changes are
  confined to the **English** section, so the Slovenian mappings and declared
  MD5s pinned here are the ones in place at release. The pin **precedes** the
  two post-release edits `f2976f2d` (2026-07-16) and `8048f8a1` (2026-08-06).

Pinning matters in opposite directions for the two files. For 1.13.0 the
post-release edits changed which Slovenian models `default` resolves to, so
pinning `9b46b7fe` changes the outcome. For 1.14.0 they did not: the Slovenian
package mappings at `f016b8e9`, and the model binaries they resolve to, are the
same as in the present-day `resources_1.14.0.json` that the 2026-08-10 run used.
The pinned and unpinned 1.14 configurations were expected to agree before the
runs, so the byte-identical 1.14 predictions and evaluator outputs confirm
reproducibility for those four runs rather than showing anything new. The
resource-resolution problem is confined to the 1.13 side.

### Upstream MD5 cross-check of the release-time artifacts

Both pinned files were re-fetched from `stanfordnlp/stanza-resources` at their
commits and hashed; each matched the SHA-256 recorded in the reconstruction's
manifest. The MD5 each file **declares** for every Slovenian artifact the
reconstruction used was then compared against
[`model-artifacts.json`](../experiments/20260811-stanza-release-time-1.13-vs-1.14/model-artifacts.json).

Release-time **1.13.0**, `resources_1.13.0.json` @ `9b46b7fe` — all 7 match:

| Artifact | MD5 declared upstream | In `model-artifacts.json` | |
|---|---|---|---|
| `tokenize/ssj.pt` | `a6b8b84173f313ee80e0f3cc18ae477d` | same | match |
| `lemma/ssj_nocharlm.pt` | `4dec22506f988669cab44666ee931e40` | same | match |
| `pos/ssj_nocharlm.pt` | `f5d37e80374a5ad1617e3ed9513979fa` | same | match |
| `pos/ssj_crosloengual-bert.pt` | `5a88beac7ad13e8463b0549d0413e8ab` | same | match |
| `depparse/ssj_nocharlm.pt` | `4234e03672e96e82a782c4619c44f269` | same | match |
| `depparse/ssj_crosloengual-bert.pt` | `b6ee4c4d5e6d48bf8ba54572e58b0663` | same | match |
| `pretrain/conll17.pt` | `e9710fbfa537a30610e7c3cb370d52f0` | same | match |

Release-time **1.14.0**, `resources_1.14.0.json` @ `f016b8e9` — all 11 match:
the `combined_*` `tokenize`/`lemma`/`pos`/`depparse` set (two each),
`pretrain/conll17.pt`, and `forward_charlm/oscar2023.pt` /
`backward_charlm/oscar2023.pt`.

In both cases the recorded artifact set is exactly the dependency closure of
`default` and `default_accurate` over `tokenize,pos,lemma,depparse`, computed
from the pinned file itself — 7 for 1.13.0, 11 for 1.14.0, with nothing missing
and nothing extra.

The release-time `ssj_*` artifact identities are therefore **independently
corroborated upstream**, on the same footing as the `combined_*` ones. The
historical resource files are not committed to this repository, but their
contents are re-fetchable at the pinned commits and verify against the recorded
SHA-256; that is a packaging limitation, not a provenance gap.

One further check falls out of the same files: at `9b46b7fe` the Slovenian
`depparse` entries are exactly `ssj_crosloengual-bert`, `ssj_nocharlm`,
`sst_nocharlm`, with **no `combined` package and no `combined_*` entry**. That
confirms the before/after table below from the file contents themselves.

### Release-time declared dependencies

Which dependencies each checkpoint declares is a separate axis from what it was
trained on. Read directly from the two pinned files, for the components the
[release-time reconstruction](../experiments/20260811-stanza-release-time-1.13-vs-1.14/)
runs:

| Component | Release-time 1.13.0 (`9b46b7fe`) | Release-time 1.14.0 (`f016b8e9`) |
|---|---|---|
| `default` POS | `ssj_nocharlm`, deps: `pretrain conll17` | `combined_charlm`, deps: `pretrain conll17` + `oscar2023` fwd/bwd charLM |
| `default` lemma | `ssj_nocharlm`, no declared deps | `combined_nocharlm`, no declared deps |
| `default_accurate` POS | `ssj_crosloengual-bert`, deps: `pretrain conll17` | `combined_crosloengual-bert`, deps: `pretrain conll17` + `oscar2023` fwd/bwd charLM |
| `default_accurate` lemma | `ssj_nocharlm`, no declared deps | `combined_charlm`, deps: `pretrain conll17` + `oscar2023` fwd/bwd charLM |

The `lemma` `combined_charlm` entry **already** declares the charLM at
`f016b8e9`, so the post-release commit `8048f8a1` (2026-08-06) is not the origin
of the charLM arguments in the release-time 1.14 configuration and must not be
cited as a factor in a release-time comparison.

These declared dependencies are not the whole POS/lemma difference either: the
`combined_*` checkpoints were also trained on different data — see
[What `combined` means for Slovenian](#what-combined-means-for-slovenian--training-data-not-just-resolution)
below.

### The decisive commit: `654c7f7f` (2026-06-23)

[`654c7f7f489b6f8c4bfec0b4a6e5088bf2634e76`](https://github.com/stanfordnlp/stanza-resources/commit/654c7f7f489b6f8c4bfec0b4a6e5088bf2634e76)
— *"Add a combined set of models and a charlm for SL. Actually, the transformer
models were not trained with charlm, but now list that as a dependency.
Hopefully they are ignored...?"* — landed **5 days after the Stanza 1.13.0
release** and modified only `resources_1.13.0.json`.

Its diff to the Slovenian section is what makes the present comparison hard to
read as a historical one. Reconstructed from the file contents at the commit and
at its parent `a2bf3aae`:

| | Before `654c7f7f` (state at the 1.13.0 release) | After `654c7f7f` |
|---|---|---|
| `packages.default` | `tokenize: ssj`, `lemma: ssj_nocharlm`, `pos: ssj_nocharlm`, `depparse: ssj_nocharlm` | `tokenize: combined_nocharlm`, `lemma: combined_nocharlm`, `pos: combined_nocharlm`, `depparse: combined_nocharlm` |
| `packages.default_accurate` | `tokenize: ssj`, `lemma: ssj_nocharlm`, `pos: ssj_crosloengual-bert`, `depparse: ssj_crosloengual-bert` | `tokenize: combined_nocharlm`, `lemma: combined_nocharlm`, `pos: combined_crosloengual-bert`, `depparse: combined_crosloengual-bert` |
| available `depparse` entries | `ssj_crosloengual-bert`, `ssj_nocharlm`, `sst_nocharlm` | the same **plus `combined_nocharlm` and `combined_crosloengual-bert`** |
| `combined` package | absent | present |

Two things follow, and both are directly verifiable from the file contents:

1. **The `combined_*` dependency-parser entries did not exist in
   `resources_1.13.0.json` at the time Stanza 1.13.0 was released.** They were
   introduced by this commit.
2. **Slovenian `default` and `default_accurate` were repointed from `ssj_*` to
   `combined_*` by this commit**, again after the 1.13.0 release.

### What `combined` means for Slovenian — training data, not just resolution

The resource files answer a resolution question: which checkpoint a package maps
to, and which dependencies that checkpoint declares. What those checkpoints were
trained on comes from Stanza's dataset-preparation code instead.

In Stanza 1.14.0, `stanza/utils/datasets/prepare_tokenizer_treebank.py`
registers `sl_combined` in `COMBINED_FNS` and builds it with
`build_combined_slovenian_dataset`, whose **train** split is the concatenation of
`["UD_Slovenian-SSJ", "UD_Slovenian-SST"]`; `dev` and `test` come from SSJ only.
`prepare_pos_treebank.py`, `prepare_lemma_treebank.py` and
`prepare_depparse_treebank.py` all route through the same
`copy_conllu_treebank` → `process_treebank` → `build_combined_dataset` dispatch.

Two consequences, both directly readable from that code:

- The SSJ+SST training merge applies to **POS, lemma and dependency parsing
  alike** — not to the dependency parser alone.
- `build_extra_combined_slovenian_dataset` supplies additional Slovene data
  (SUK: `ssj500k-tag.ud.conllu` and `ambiga.ud.conllu`) for the **POS and lemma**
  model types only, and returns nothing for the other model types.

The `ssj_*` → `combined_*` move is therefore not just a dependency-parser merge,
and the POS and lemma difference is not just their newly declared charLM
dependencies: those components received the same spoken-SST training coverage,
plus the extra Slovene resources above.

### What the later commits did — and did not — do

`8cbebe5e` (2026-06-25) is often the commit one reaches for, because its message
names Slovenian explicitly. It is **not** the origin of the combined dependency
parser. Diffing its Slovenian section against its parent (`654c7f7f`):

- it **adds** `combined_charlm` entries for `tokenize`, `lemma` and `pos`;
- it repoints `default.pos` → `combined_charlm` and
  `default_accurate.tokenize`/`lemma` → `combined_charlm`;
- it **adds no `depparse` entry and changes no `depparse` mapping** — the
  `depparse` model list is identical before and after.

So `8cbebe5e` explains the final *tokenizer/lemma/POS* mappings, while
`654c7f7f` explains the *dependency-parser* mappings. Attributing the identical
parser artifacts to `8cbebe5e` would be wrong.

After the three 2026-06-25 commits, the Slovenian `default` and
`default_accurate` mappings in `resources_1.13.0.json` reached exactly the state
both experiment arms used.

### Timing relative to the library releases

The two versioned files behave differently, and the distinction matters:

- **`resources_1.13.0.json` was edited after its release.** The library shipped
  on 2026-06-18; the Slovenian defaults were switched to `combined_*` on
  2026-06-23 and updated again on 2026-06-25.
- **`resources_1.14.0.json` was largely prepared *before* its release.** The
  2026-06-29 sort-and-lemmatizer commit `79abac10` predates the 2026-07-15
  release, so it is not a post-release edit. Post-release edits to that file do
  exist — `f2976f2d` (2026-07-16, aliases) and `8048f8a1` (2026-08-06,
  lemmatizer charlm arguments) — but they come after the pin used by the
  reconstruction.

A general claim that the versioned resource files get edited after their library
releases therefore does not hold for both files. What this audit supports is
narrower:

> `resources_1.13.0.json` was switched from Slovenian `ssj_*` defaults to
> `combined_*` defaults, including the dependency parser, **after** the Stanza
> 1.13.0 library release — and the current 1.13 and 1.14 caches resolve to
> byte-identical Slovenian POS and dependency-parser files.

### Interpretation

Installing "Stanza 1.13 with resources 1.13" today does not reproduce the
Slovenian model set that a user of Stanza 1.13 obtained at release time: at
release the defaults pointed at `ssj_*` models, and today they point at
`combined_*` models that were added afterwards.

That is a documented sequence of upstream events, not an explanation of this
experiment's outputs: it establishes the mapping history and the artifact
identity, not how each differing prediction arises.

Upstream commit messages are quoted as published. The parenthetical asides
("Hopefully they are ignored...?", "oops") are the upstream authors' wording
about their own changes; they are not evidence of a defect, and nothing here
should be read as a Stanza bug report.

## What this does not establish

- **Not** that Stanza 1.14 contains no new Slovenian training. It shows only
  which artifacts these two caches resolved to on 2026-08-10, and what the
  versioned resource files declare.
- The 2026-08-10 run documented here is **not itself a historical rerun**: it
  records how the two Stanza versions resolved their Slovenian resources on that
  date. A separate follow-up experiment,
  [`experiments/20260811-stanza-release-time-1.13-vs-1.14/`](../experiments/20260811-stanza-release-time-1.13-vs-1.14/),
  subsequently reconstructed the release-time Slovenian resource/model
  configurations for both 1.13.0 and 1.14.0 and evaluated them on SSJ and SST.
  The original 2026-08-10 predictions, scores and provenance remain unchanged.
- **Not** an explanation for every changed dependency prediction. The parser
  checkpoints are byte-identical, yet `HEAD`/`DEPREL` output is not. Library
  code between the two releases — inference, batching, preprocessing, or
  dependency-stack behaviour — can also affect output, and this experiment did
  not isolate which change is responsible. The PyTorch control
  ([SSJ](../experiments/20260810-stanza-1.13-vs-1.14-ssj/control-torch2.6.md),
  and the SST repeat recorded in the SST manifest) rules out the
  torch 2.0.1-vs-2.6.0 difference as the cause for the Stanza 1.13 arm only.
- **Not** a statistical claim of any kind. No significance test was performed in
  either run.
- **Not** fully reproducible from this repository. The caches live on the CJVT
  server; the hashes are recorded, the binaries are not committed. The upstream
  resource history, by contrast, is public and re-checkable at any time.

## Provenance of the statements above

| Claim | How it was established |
|---|---|
| resource versions, `resources.json` and model-file SHA-256, MD5 cross-checks | inspected on the CJVT server caches used by the runs; recorded in the experiment manifests |
| upstream commit IDs, dates, messages, changed files | GitHub API, 2026-08-11 |
| historical Slovenian package mappings and `depparse` entry lists before/after each commit | `resources_1.13.0.json` and `resources_1.14.0.json` fetched at the specific commits `9b46b7fe`, `a2bf3aae`, `654c7f7f`, `8cbebe5e`, `aab5014f`, `8c4cedae`, `f016b8e9`, `8048f8a1` and parsed directly, 2026-08-11 |
| that `f016b8e9` modifies `resources_1.14.0.json`, is the last commit to touch it before the 1.14.0 release, and changes only its English section | GitHub API commit list for that file path, plus a direct comparison of the file at `8c4cedae` and at `f016b8e9`, 2026-08-11 |
| Slovenian `combined` training-data composition (SSJ+SST train for POS, lemma and depparse; SUK extra data for POS and lemma) | `stanza/utils/datasets/prepare_tokenizer_treebank.py`, `prepare_pos_treebank.py`, `prepare_lemma_treebank.py` and `prepare_depparse_treebank.py` read at tag `v1.14.0` of `stanfordnlp/stanza`, 2026-08-11 |
| upstream-declared MD5s for the Slovenian combined models | the same fetched resource files |
| the two pinned release-time resource commits `9b46b7fe` / `f016b8e9` and their `resources.json` SHA-256 | recorded by the 2026-08-11 reconstruction in [its manifest](../experiments/20260811-stanza-release-time-1.13-vs-1.14/manifest.json) under `release_time_resources`; both files were re-fetched at those commits and hashed, and both matched |
| upstream-declared MD5s for the release-time Slovenian `ssj_*` and `combined_*` artifacts, and the release-time package mappings, `depparse` entry lists and declared dependencies | the two re-fetched pinned files, parsed directly; compared artifact-by-artifact against [`model-artifacts.json`](../experiments/20260811-stanza-release-time-1.13-vs-1.14/model-artifacts.json) — 7/7 for 1.13.0 and 11/11 for 1.14.0 |
| Stanza 1.13.0 / 1.14.0 release dates | PyPI release metadata, 2026-08-11 |
| changed-token counts per field | [`scripts/compare_stanza_versions.py`](../scripts/compare_stanza_versions.py) and [`scripts/compare_stanza_versions_sst.py`](../scripts/compare_stanza_versions_sst.py), regenerated from the committed prediction files |
