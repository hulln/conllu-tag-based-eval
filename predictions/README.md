# predictions/

**Generated** model outputs in CoNLL-U format. Nothing here is written by hand —
these files are produced by the prediction scripts and should only be
regenerated, never edited.

- [output/](output/) — public aligned prediction outputs, one flat directory
- [../archive/local/](../archive/local/) — local-only historical outputs (gitignored)

## Naming

```
<run_id>_<system>_<mode>_predicted.conllu
```

where `run_id = <stamp>_<dataset-tag>_<label>`, e.g.

```
20260622-0810-tk13_sl-ssj-ud-test_full_trankit_aligned_predicted.conllu
20260810-stanza-1.13-vs-1.14_sl-ssj-ud-test_full_stanza-1.14.0-accurate_aligned_predicted.conllu
```

To find out what a run was and why, look up its stamp in
[experiments/](../experiments/).

## Aligned-mode contract

Aligned predictions keep the gold `ID`, `FORM` and `MISC` columns and the gold
sentence metadata, and replace `LEMMA`, `UPOS`, `XPOS`, `FEATS`, `HEAD` and
`DEPREL` with the system's predictions. Sentence and token boundaries therefore
match gold exactly.

## Producing and checking

Produced by [run_pipeline.py](../scripts/run_pipeline.py),
[predict_trankit.py](../scripts/predict_trankit.py),
[predict_classla.py](../scripts/predict_classla.py) and
[predict_stanza.py](../scripts/predict_stanza.py).

Verify the canonical run's files against pinned hashes with
[verify_canonical_run.py](../scripts/verify_canonical_run.py) and
[references/canonical_run_manifest.json](../references/canonical_run_manifest.json).

Supplementary base-mode outputs, superseded trial runs and sample files are
local-only; see [`.gitignore`](../.gitignore).
