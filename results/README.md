# results/

Evaluation outputs and analysis reports.

- `output/<run-id>/main/`: primary aligned outputs, including eval summaries, model comparison, and `qa_validation.md`
- `output/<run-id>/diagnostics/`: primary aligned verbose tagged metrics and error analyses
- [archive/local](../archive/local/): local-only legacy output layouts and historical comparisons (gitignored)

Supplementary base-mode outputs are local-only (gitignored).

Stanza 1.13.0 vs 1.14.0 evaluation outputs are stored in
[`output/20260810-stanza-1.13-vs-1.14_sl-ssj-ud-test_full/main/`](output/20260810-stanza-1.13-vs-1.14_sl-ssj-ud-test_full/main/).
The directory contains the four full SSJ evaluator outputs and the
token-level version-change review.

See [`../docker/README_stanza_versions.md`](../docker/README_stanza_versions.md)
for the full reproducibility record.

Current active canonical runs:

- SSJ: [output/20260414-1819_sl-ssj-ud-test_full](output/20260414-1819_sl-ssj-ud-test_full/)
- SST: [output/20260420-1105_sl-sst-ud-test_full](output/20260420-1105_sl-sst-ud-test_full/)

Trankit 1.3 run (CLARIN `11356/2201`, run `20260604-0859-tk13`) — its SST result is the one shown in the recommended v4 table; not part of the hash-pinned canonical anchor:

- SSJ: [output/20260604-0859-tk13_sl-ssj-ud-test_full](output/20260604-0859-tk13_sl-ssj-ud-test_full/)
- SST: [output/20260604-0859-tk13_sl-sst-ud-test_full](output/20260604-0859-tk13_sl-sst-ud-test_full/)

v5 run (CLARIN `11356/2201`, run `20260622-0810-tk13`):

- SSJ written: [output/20260622-0810-tk13_sl-ssj-ud-test_full](output/20260622-0810-tk13_sl-ssj-ud-test_full/)
- SST normalised: [output/20260622-0810-tk13_sl-sst-ud-test_full](output/20260622-0810-tk13_sl-sst-ud-test_full/)
- SST colloquial: [output/20260622-0810-tk13_sl-sst-ud-test-pog_full](output/20260622-0810-tk13_sl-sst-ud-test-pog_full/)

All three v5 runs have `qa_validation.md` status `PASS`. There is no v5 result
directory for the supplied paired `stan` test file.

Strict rerun verification:

- Run [scripts/verify_canonical_run.py](../scripts/verify_canonical_run.py) after a rerun.
- Source of truth is [references/canonical_run_manifest.json](../references/canonical_run_manifest.json).

First file to open for a run:

- SSJ: [output/20260414-1819_sl-ssj-ud-test_full/main/qa_validation.md](output/20260414-1819_sl-ssj-ud-test_full/main/qa_validation.md)
- SST: [output/20260420-1105_sl-sst-ud-test_full/main/qa_validation.md](output/20260420-1105_sl-sst-ud-test_full/main/qa_validation.md)

Public interactive tables:

- SSJ: [tables/comparison_table_v2_ssj.html](../tables/comparison_table_v2_ssj.html)
- SST: [tables/comparison_table_v3_sst.html](../tables/comparison_table_v3_sst.html)
- Combined v5 table: [tables/comparison_table_v5.html](../tables/comparison_table_v5.html)
