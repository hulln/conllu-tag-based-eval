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
(`model_artifacts_todo`). This document is the resolution of that item.

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
| **2026-07-15** | **Stanza 1.14.0 released on PyPI** |
| 2026-07-16 | `f2976f2d` — more aliases (`resources_1.14.0.json`) |
| 2026-08-06 | `8048f8a1` — "Update lemmatizers for 1.14.0 to have forward & backward charlm args" — **last commit to touch `resources_1.14.0.json`** before the runs |
| 2026-08-10 | Both experiment runs executed |
| 2026-08-11 | This audit |

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

- **`resources_1.13.0.json` was edited after the 1.13.0 release.** The 1.13.0
  library shipped on 2026-06-18; the Slovenian defaults were switched to
  `combined_*` on 2026-06-23 and further updated on 2026-06-25.
- **`resources_1.14.0.json` was largely prepared *before* the 1.14.0 release.**
  The 2026-06-29 sort-and-lemmatizer commit `79abac10` **predates** the 2026-07-15
  release of Stanza 1.14.0. It is *not* an example of a post-release edit.
  Post-release edits to that file do exist (`f2976f2d` on 2026-07-16, aliases;
  `8048f8a1` on 2026-08-06, lemmatizer charlm arguments), but they are not the
  commits usually cited.

A blanket statement that "the versioned resource files were edited after the
corresponding library releases" is therefore **inaccurate**. The accurate,
narrower statement is the one this audit can support:

> `resources_1.13.0.json` was switched from Slovenian `ssj_*` defaults to
> `combined_*` defaults, including the dependency parser, **after** the Stanza
> 1.13.0 library release — and the current 1.13 and 1.14 caches resolve to
> byte-identical Slovenian POS and dependency-parser files.

### Interpretation

Installing "Stanza 1.13 with resources 1.13" today does not reproduce the
Slovenian model set that a user of Stanza 1.13 obtained at release time: at
release the defaults pointed at `ssj_*` models, and today they point at
`combined_*` models that were added afterwards.

That is a documented sequence of upstream events, not a demonstrated causal
mechanism for this experiment's outputs. What is established is the *mapping*
history and the *artifact identity*; what is not established is a step-by-step
account of how each differing prediction arises.

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
| historical Slovenian package mappings and `depparse` entry lists before/after each commit | `resources_1.13.0.json` and `resources_1.14.0.json` fetched at the specific commits `9b46b7fe`, `a2bf3aae`, `654c7f7f`, `8cbebe5e`, `aab5014f`, `8048f8a1` and parsed directly, 2026-08-11 |
| upstream-declared MD5s for the Slovenian combined models | the same fetched resource files |
| Stanza 1.13.0 / 1.14.0 release dates | PyPI release metadata, 2026-08-11 |
| changed-token counts per field | [`scripts/compare_stanza_versions.py`](../scripts/compare_stanza_versions.py) and [`scripts/compare_stanza_versions_sst.py`](../scripts/compare_stanza_versions_sst.py), regenerated from the committed prediction files |
