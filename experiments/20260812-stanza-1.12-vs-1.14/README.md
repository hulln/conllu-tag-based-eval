# Stanza 1.12.0 vs 1.14.0: release-time Slovenian models

Run stamp `20260812-stanza-1.12-vs-1.14` · CJVT GPU server · 2026-08-12

## Purpose

This experiment compares Stanza **1.12.0** and **1.14.0** using the Slovenian
resource/model configurations that belonged to those releases, evaluated on the
same aligned UD Slovenian **SSJ** (written) and **SST** (spoken) test sets.

The comparison uses both:

- `default`
- `default_accurate`

and reports:

- LAS
- UAS
- lemma accuracy
- UPOS accuracy
- UFeats accuracy

Sentence and token boundaries are taken from gold, so tokenisation quality is
outside the scope of the evaluation.

## Why 1.12 is used as the reference

Earlier experiments compared Stanza 1.13.0 and 1.14.0. Investigation showed
that `resources_1.13.0.json` had been modified after the release of Stanza
1.13.0, so a present-day installation of 1.13.0 no longer reproduced the
Slovenian model configuration available at its release time.

Stanza 1.12.0 therefore provides an unambiguous older reference configuration.

The release-time 1.12 `default` configuration is identical to the release-time
1.13 `default` configuration at the model-artifact level and produces
byte-identical predictions on both SSJ and SST.

For `default_accurate`, Stanza 1.13 had already introduced the
`ssj_crosloengual-bert` POS model, while Stanza 1.12 still used
`ssj_nocharlm` POS. Consequently the two `default_accurate` conditions are not
identical.

## Release-time configurations

### Stanza 1.12.0

Historical resource commit:

`d3596e4069988fe0829d38f3c3aa3174f8950324`

Historical `resources_1.12.0.json` SHA-256:

`2445b58053a96c1fcfd95e9ee977ad7f6313e68994bcd437cc30b4346fab2f0e`

`default`:

- `tokenize=ssj`
- `lemma=ssj_nocharlm`
- `pos=ssj_nocharlm`
- `depparse=ssj_nocharlm`

`default_accurate`:

- `tokenize=ssj`
- `lemma=ssj_nocharlm`
- `pos=ssj_nocharlm`
- `depparse=ssj_crosloengual-bert`

All required 1.12 model artifacts were verified against the MD5 values declared
in the pinned historical resource file.

### Stanza 1.14.0

The 1.14 side reuses the already verified release-time reconstruction from:

`experiments/20260811-stanza-release-time-1.13-vs-1.14/`

That reconstruction verified that all four release-time 1.14 prediction and
evaluator files are byte-identical to the original 2026-08-10 Stanza 1.14 run.

## Main results

See:

- `table.md` for the compact table requested for reporting;
- `comparison.txt` for the per-condition 1.12 -> 1.14 deltas.

The largest changes occur on SST. For example:

- `default` LAS: 68.90 -> 81.95 (+13.05)
- `default_accurate` LAS: 77.48 -> 86.13 (+8.65)

Lemmatization improves in every condition:

- SSJ `default`: 97.61 -> 98.76 (+1.15)
- SSJ `default_accurate`: 97.61 -> 98.89 (+1.28)
- SST `default`: 97.89 -> 99.14 (+1.25)
- SST `default_accurate`: 97.89 -> 99.29 (+1.40)

## Files

- `comparison.txt` — generated 1.12 -> 1.14 comparison.
- `table.md` — compact reporting table.
- `scripts/compare_stanza_112_114.py` — script that regenerates both files.

The 1.12 prediction and evaluator files are stored under
`predictions/output/` and `results/output/` with the
`20260812-stanza-1.12-release-defaults` run stamp.

The 1.14 artifacts are the verified release-time files from the
`20260811-stanza-1.14-release-defaults` run stamp.
