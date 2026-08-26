# Provisional Slovenian evaluator smoke test

**PROVISIONAL ENGINEERING SMOKE TEST**  
**GOLD PROVENANCE NOT YET CONFIRMED**  
**DO NOT TREAT AS BENCHMARK RESULT**

This directory contains isolated technical output from the existing repository
evaluator. It uses the local SSJ and unsuffixed SST files only as engineering
fixtures. No artifact here belongs in the repository's production `results/`
tree or in an authoritative benchmark report.

`sl_spacy_stanza_results.tsv` contains the 12 stable SL spaCy/Stanza manifest
runs: 6 written and 6 spoken. All completed successfully, returned all 13 base
evaluator metrics, and produced exactly identical numeric fields on a second
execution.

From `am_benchmark/`, reproduce the isolated check with:

~~~text
python3 scripts/run_benchmark_evaluation.py --execute --smoke-test --initial-debugging-only --language SL --model spacy --model stanza --repeat-check
~~~
