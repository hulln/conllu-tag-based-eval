# references/

Material that is **not tied to a single experiment**: repository-level
reproducibility metadata, cross-run and dataset-level notes, and external
sources.

Documentation of an individual run belongs in [`experiments/`](../experiments/),
not here.

## Repository-level

- [canonical_run_manifest.json](canonical_run_manifest.json) — hashes and expected
  metrics for the canonical SSJ run [`20260414-1819`](../experiments/20260414-1819/),
  used by [scripts/verify_canonical_run.py](../scripts/verify_canonical_run.py)
  for strict rerun verification. This is the repository's reproducibility anchor
  and is deliberately kept here rather than in the experiment directory, because
  it is the verifier's default input and pins files across the whole public
  surface (scripts, predictions, results and the published table bundle).

## Cross-run and dataset notes

- [sst_vs_pog_comparison_2026-06-22.md](sst_vs_pog_comparison_2026-06-22.md) —
  audit of the supplied colloquial (`pog`) and standardised (`stan`) SST test
  files against the official UD SST test file.
- [v5_publication_qa_2026-06-22.md](v5_publication_qa_2026-06-22.md) — QA of the
  v5 publication surface, spanning the three [`20260622-0810-tk13`](../experiments/20260622-0810-tk13/)
  runs and the published tables.

## External sources

- Dobrovoljc, Terčon, Ljubešić — https://doi.org/10.4312/slo2.0.2023.1.218-246

Local-only material in this directory is excluded from Git by
[`.gitignore`](../.gitignore): `*.txt` notes, `*.pdf` copies, and
`run-comparison-*.md`.
