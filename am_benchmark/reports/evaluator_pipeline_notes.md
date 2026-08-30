# Evaluator pipeline engineering notes

> Historical design notes. The current authoritative implementation status is
> documented in `../README.md` and `ui_prototype_notes.md`.

## Practical flow

~~~text
gold CoNLL-U + prediction CoNLL-U
    -> scripts/conll18_ud_eval_tag-based.py
    -> metric objects / verbose plain-text table
    -> run-level result rows and optional error aggregation
    -> generated JavaScript data bundle
    -> static interactive table
~~~

## Evaluator and invocation

The repository evaluator is `scripts/conll18_ud_eval_tag-based.py`. It is the
CoNLL-2018 UD Shared Task evaluator with local regex-filtered UPOS, XPOS, UAS,
and LAS breakdowns. It has no third-party dependencies and can be used either
through its `load_conllu_file()` and `evaluate()` Python functions or through
the command line:

~~~text
python3 scripts/conll18_ud_eval_tag-based.py GOLD.conllu PREDICTION.conllu -v
~~~

Verbose mode emits Precision, Recall, F1, and, where defined, aligned accuracy
for these base metrics: Tokens, Sentences, Words, UPOS, XPOS, UFeats, AllTags,
Lemmas, UAS, LAS, CLAS, MLAS, and BLEX. The optional `--upos`, `--xpos`, `--uas`,
and `--las` regexes add per-tag or per-relation rows. Without `-v`, the command
prints only LAS, MLAS, and BLEX F1.

The evaluator rejects malformed CoNLL-U, files without a final sentence-ending
blank line, and gold/prediction pairs whose concatenated token text differs.
Dependency relation subtypes are ignored, following its inherited scoring
rules.

## Existing wrappers and result storage

`scripts/run_pipeline.py` is the main old workflow. Its `eval_and_analyze()`
function invokes the evaluator twice per prediction: once for the 13 base
metrics and once with all four regex breakdowns. It then runs error analysis,
cross-system comparison, optional table generation, and QA.

That wrapper is not directly reusable for this benchmark because it assumes a
paired Trankit/CLASSLA run, defaults to Slovenian SSJ inputs, can generate model
predictions, and writes to the production `predictions/output/`,
`results/output/`, and `tables/` trees. Existing results use:

~~~text
results/output/<run_id>/
    main/          base metric tables, comparisons, QA
    diagnostics/   expanded tag/relation metrics and error analyses
~~~

The evaluator itself is reusable unchanged. The new
`am_benchmark/scripts/run_benchmark_evaluation.py` imports that implementation
and adds manifest selection, gold-status gates, isolated output, hashes, and an
optional repeat check. It does not generate predictions, reimplement metrics,
run error analysis, or write to the production result tree.

## Interactive table data flow

The current v5 table is built by
`scripts/build_interactive_comparison_table_v5.py`. It reads hard-coded gold,
prediction, and expanded evaluator-output paths, reuses parsing/profile helpers
from the v2 builder, and writes `tables/comparison_table_v5_data.js`. The static
HTML page loads that file as `window.TABLE_DATA_V5` and renders selectors,
metric cards, accuracy tables, error tables, examples, exports, and deep links.

The current payload is corpus-centric: it has two fixed models (`trankit` and
`classla`) and three fixed Slovenian corpora (`ssj`, `sst`, `pog`). Each corpus
contains metrics indexed by model plus precomputed error and accuracy rows. The
page assumes exactly one comparison model through a two-model toggle.

Reusable unchanged or with a thin adapter:

- the evaluator and its exact metric definitions;
- the existing CoNLL-U parsing/error-profile helpers;
- the static generated-data-bundle pattern;
- frontend filtering, sorting, export, example-panel, and deep-link behaviour.

Hard-coded to the old comparison:

- Trankit/CLASSLA model names and two-model comparison logic;
- Slovenian SSJ/SST/POG corpus definitions and provenance prose;
- result and prediction paths embedded in the v5 builder;
- the model/corpus-only selector state and URL hash;
- Slovenian-specific XPOS terminology and some page copy;
- the five displayed overview metrics, despite the evaluator producing 13.

## Current authoritative stable outcome

Aaron's six supplied gold files resolved the former provenance and availability
gates. The canonical manifest now contains 36 stable spaCy/Stanza runs: six per
language/test cohort across EN, NL, and SL. All 36 completed through the existing
evaluator and produced identical numeric output on a second execution.

Every pair has matching underlying character text and exact sentence spans.
Eight tokenizer-varying runs have token-boundary F1 below 100%, which is an
evaluated model/tokenizer difference rather than a mapping error. All aligned
word scores are 100%, and all 13 base metric families are present.

The authoritative result is
`authoritative_spacy_stanza_results.tsv`. Historical provisional SL fixtures
remain under `smoke_test/` for regression context only. The known NL Trankit
English-content file is excluded under Aaron's explicit invalid-file decision;
its valid dialect-named counterpart supplies the canonical NL spoken run.
