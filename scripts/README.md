# scripts/

Pipeline and analysis entry points.

- [run_pipeline.py](run_pipeline.py): end-to-end orchestration. Aligned mode is primary by default; base mode is optional. Runs QA validation at the end unless `--skip-qa` is used.
  - Trankit invocations are wired to `--model-source clarin-11356-1997`, i.e. the specific Slovenian CLARIN handle `11356/1997` selected for this project.
  - Use `--publish-interactive-table` to refresh [tables/comparison_table_v2_ssj.html](../tables/comparison_table_v2_ssj.html) and [tables/comparison_table_v2_ssj_data.js](../tables/comparison_table_v2_ssj_data.js) from the aligned outputs of that run.
- Default write targets are [predictions/output](../predictions/output/) and [results/output](../results/output/).
- [conll18_ud_eval_tag-based.py](conll18_ud_eval_tag-based.py): reference evaluator used for scoring; kept unchanged from the originally provided version.
- [predict_trankit.py](predict_trankit.py): Trankit prediction export with the same aligned-mode contract as CLASSLA.
  - For Slovenian (`--lang slovenian` or `--lang sl`), default `--model-source auto` uses the specific CLARIN model handle `11356/1997` and verifies MD5 (`0ddfac8d7445f8fa300f59dde1a00352`) before extraction.
  - Default CLARIN URL is `https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1997/trankit-sl-ssj%2bsst.zip` (the same command-line form shown on CLARIN).
  - Use `--model-source upstream` to force Trankit default model downloads instead.
- [predict_classla.py](predict_classla.py): CLASSLA prediction export. In aligned mode it consumes gold CoNLL-U segmentation/tokenization and preserves gold sentence metadata.
- [predict_stanza.py](predict_stanza.py): plain-Stanza prediction export for the Stanza version comparison ([SSJ](../experiments/20260810-stanza-1.13-vs-1.14-ssj/), [SST](../experiments/20260810-stanza-1.13-vs-1.14-sst/)). Aligned mode only; `--package default|default_accurate`. Assumes a treebank with no multiword tokens or empty nodes. Takes `--gold`/`--output`, so one script serves both test sets.
- [compare_stanza_versions.py](compare_stanza_versions.py): token-level diff of two Stanza releases over the same gold file, classifying every changed field as fix/regression/both-wrong. Regenerates the SSJ `stanza-1.13-vs-1.14-change-review.md`.
- [compare_stanza_versions_sst.py](compare_stanza_versions_sst.py): the same analysis for the SST arm.
  - **Why these two are deliberately not merged.** Each is a frozen, argument-free record of exactly which four prediction files produced one committed change review, and each is pinned by SHA-256 in its experiment's `manifest.json`. Parameterising them would replace that pinned record with a script whose output depends on invocation, and would rewrite the hash already committed for the completed SSJ run. They differ only in the `GOLD`/`OUTPUT`/`RUNS` path constants and one label string, so `diff` between them is a one-screen review. Both regenerate their change review byte-identically. If a third dataset is ever added, revisit this and parameterise once — do not add a third copy.
- [compare_stanza_release_time.py](compare_stanza_release_time.py): regenerates `comparison.txt` for the [release-time reconstruction](../experiments/20260811-stanza-release-time-1.13-vs-1.14/) from the committed evaluator files, reading the F1 column for every metric. Prints three explicitly separated comparisons — release-time 1.13 → release-time 1.14, release-time 1.13 → present-day-resource 1.13, and present-day-resource 1.13 → the original 2026-08-10 1.14 — and independently verifies that the reconstructed 1.14 predictions and evaluator outputs are byte-identical to the original 1.14 run. Each block reads the artifacts named in its own title, so `--skip-identity-check` cannot change which files are compared.
- [qa_validate_run.py](qa_validate_run.py): strict mode-aware run validation for aligned-only or aligned+base runs.
- [verify_canonical_run.py](verify_canonical_run.py): strict rerun verifier using canonical hash/metric manifest.
- [content_comparison_table.py](content_comparison_table.py): table-style HEAD/DEPREL content comparison (with examples) for Task 2 reporting.
- [build_interactive_comparison_table_v2.py](build_interactive_comparison_table_v2.py): builds the public interactive comparison table bundle in [tables](../tables/) from aligned predictions and tagged eval outputs. Accepts `--dataset-label` (e.g. `SSJ-UD`, `SST-UD`) and `--ack-text`.
- [build_interactive_comparison_table.py](build_interactive_comparison_table.py): legacy v1 table builder (kept for reference).
- [analyze_errors.py](analyze_errors.py): model-vs-gold HEAD/DEPREL error summaries.
- [compare_models.py](compare_models.py): token-level Trankit-vs-CLASSLA comparison.
- [export_raw_sentences.py](export_raw_sentences.py): helper for deriving raw sentence input from gold CoNLL-U when base mode is needed.
- [compare_conllu_files.py](compare_conllu_files.py): utility for CoNLL-U comparison/debugging.
