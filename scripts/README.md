# scripts/

Pipeline and analysis entry points.

- [run_pipeline.py](run_pipeline.py): end-to-end orchestration. Aligned mode is primary by default; base mode is optional. Runs QA validation at the end unless `--skip-qa` is used.
  - Trankit invocations are wired to `--model-source clarin-11356-1997`, i.e. the specific Slovenian CLARIN handle `11356/1997` from supervisor instructions.
  - Use `--publish-interactive-table` to refresh [tables/comparison_table.html](../tables/comparison_table.html) and [tables/comparison_table_data.js](../tables/comparison_table_data.js) from the aligned outputs of that run.
- Default write targets are [predictions/output](../predictions/output/) and [results/output](../results/output/).
- [conll18_ud_eval_tag-based.py](conll18_ud_eval_tag-based.py): reference evaluator used for scoring; kept unchanged from the originally provided version.
- [predict_trankit.py](predict_trankit.py): Trankit prediction export with the same aligned-mode contract as CLASSLA.
  - For Slovenian (`--lang slovenian` or `--lang sl`), default `--model-source auto` uses the specific CLARIN model handle `11356/1997` and verifies MD5 (`0ddfac8d7445f8fa300f59dde1a00352`) before extraction.
  - Default CLARIN URL is `https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1997/trankit-sl-ssj%2bsst.zip` (the same command-line form shown on CLARIN).
  - Use `--model-source upstream` to force Trankit default model downloads instead.
- [predict_classla.py](predict_classla.py): CLASSLA prediction export. In aligned mode it consumes gold CoNLL-U segmentation/tokenization and preserves gold sentence metadata.
- [qa_validate_run.py](qa_validate_run.py): strict mode-aware run validation for aligned-only or aligned+base runs.
- [verify_canonical_run.py](verify_canonical_run.py): strict rerun verifier using canonical hash/metric manifest.
- [content_comparison_table.py](content_comparison_table.py): table-style HEAD/DEPREL content comparison (with examples) for Task 2 reporting.
- [build_interactive_comparison_table.py](build_interactive_comparison_table.py): builds the public interactive comparison table bundle in [tables](../tables/) from aligned predictions and tagged eval outputs.
- [analyze_errors.py](analyze_errors.py): model-vs-gold HEAD/DEPREL error summaries.
- [compare_models.py](compare_models.py): token-level Trankit-vs-CLASSLA comparison.
- [export_raw_sentences.py](export_raw_sentences.py): helper for deriving raw sentence input from gold CoNLL-U when base mode is needed.
- [compare_conllu_files.py](compare_conllu_files.py): utility for CoNLL-U comparison/debugging.
