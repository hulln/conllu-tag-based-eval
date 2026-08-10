# results/

**Generated** evaluation outputs and analysis reports. Nothing here is written by
hand — these files are produced by the pipeline and analysis scripts and should
only be regenerated, never edited.

## Layout

```
output/<run_id>/
├── main/           eval summaries, cross-system comparison reports, qa_validation.md
└── diagnostics/    tagged metrics and per-system error analyses
```

`run_id = <stamp>_<dataset-tag>_<label>`. One run directory per dataset; a single
experiment stamp can therefore produce several. To find out what a run was and
why, look up its stamp in [experiments/](../experiments/).

Supplementary base-mode outputs and legacy layouts are local-only; historical
runs live in [../archive/local/](../archive/local/).

## Where to start

For a pipeline run, open `main/qa_validation.md` first — it reports gold counts,
per-file integrity checks and an overall PASS/FAIL. Runs made outside
[run_pipeline.py](../scripts/run_pipeline.py) have no generated
`qa_validation.md`; their verification is recorded in the experiment README
instead.

Metrics come from [conll18_ud_eval_tag-based.py](../scripts/conll18_ud_eval_tag-based.py).
In aligned mode the `Sentences`, `Tokens` and `Words` rows are 100.00 **by
construction** — boundaries are taken from gold, so those rows confirm the
alignment held rather than measuring quality.

## Verification

```bash
python3 scripts/qa_validate_run.py --run-stamp <stamp> --modes aligned   # any run: integrity
python3 scripts/verify_canonical_run.py --run-stamp <stamp>              # canonical: exact match
```

The canonical anchor is [references/canonical_run_manifest.json](../references/canonical_run_manifest.json),
which pins run `20260414-1819`.

## Published tables

The interactive comparison tables built from these outputs are in
[../tables/](../tables/); the current one is the v5 table (EN + SL).
