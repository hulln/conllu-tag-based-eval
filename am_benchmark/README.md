# AM multilingual CoNLL-U benchmark

## Purpose

This directory contains the work needed to adapt the repository's existing
interactive CoNLL-U evaluation platform to a multilingual benchmark. The
benchmark varies by language, model/system, training condition, test condition,
and evaluation metric. Prediction preparation is separated from evaluation so
that source provenance and gold correspondence remain auditable.

## Current state

- Prediction inputs have been resolved into 80 logical runs.
- The unnumbered _clean.conllu file is canonical for each run.
- 79 canonical predictions are usable: 37 spaCy/Stanza runs form the stable
  initial-debugging subset and 42 other runs are structurally usable but
  provisional.
- One NL Trankit spoken-test run is excluded because it contains EN content.
- Raw files, all 97 numbered copies, and four .conllu_ alternates are
  noncanonical.
- Gold mapping is unresolved. Authoritative benchmark evaluation has **not**
  been run.
- The existing evaluator has completed a deterministic engineering smoke test
  on 12 stable SL spaCy/Stanza runs using explicitly provisional local gold
  fixtures. Those values are not benchmark results.
- A local data-driven UI prototype displays only those provisional fixture
  rows and is isolated from the production interactive table.

## Workflow

~~~mermaid
flowchart TD
    A[Source prediction files] --> B[Resolution, deduplication, validation]
    A --> N[Noncanonical variants]
    N --> N1[Raw files]
    N --> N2[Numbered copies]
    N --> N3[.conllu_ alternates]
    B --> C[80 logical runs]
    C --> S[37 stable spaCy/Stanza runs]
    C --> P[42 usable provisional runs]
    C --> X[1 excluded wrong-language run]
    S --> D[Canonical unnumbered _clean predictions]
    P --> D
    D --> G{Matching authoritative gold confirmed?}
    G -- No --> R[Resolve gold cohort mapping]
    R --> G
    G -- Provisional fixture only --> T[Engineering smoke test]
    T --> Q[Provisional machine-readable results]
    Q --> L[Local benchmark UI prototype]
    G -- Yes --> E[Evaluation]
    E --> M[Metrics]
    M --> U[Interactive evaluation interface]
~~~

## Benchmark dimensions

The values below are derived from reports/canonical_predictions.tsv; not every
cross-product combination occurs.

- Languages: EN, NL, SL.
- Models/systems: UDpipe2, UDpipessj, UDPipesst, diaparser,
  singletaskXPOS, singletaskXPOSclassification, spacy, stanza,
  trankit, trankit_1epochs, trankit_2epochs, trankit_50epochs.
- Training conditions: default, writtentrain, writtenandspokentrain,
  writtenanddialecttrain.
- Test conditions: writtentest, spokentest, dialecttest.
- Official evaluation metrics will be produced only after gold confirmation.
  The current SL smoke-test values exist solely as engineering fixtures.

## Gold readiness

The 80 runs require seven shared gold cohorts:

| Gold cohort | Logical runs | Initial spaCy/Stanza runs | Current status |
|---|---:|---:|---|
| EN written | 12 | 6 | Missing |
| EN spoken | 12 | 6 | Missing |
| NL written | 15 | 6 | Missing |
| NL spoken | 11 | 6 | Missing; 10 predictions usable |
| NL dialect | 4 | 1 | Missing |
| SL written | 13 | 6 | Candidate; provenance confirmation required |
| SL spoken | 13 | 6 | Candidate; provenance confirmation required |

For SL written, ../data/gold/sl_ssj-ud-test.conllu matches the sentence/ID and
ID/FORM sequence of all 13 selected predictions. Repository documentation
identifies it as the existing primary UD Slovenian SSJ r2.17 gold, but the
benchmark handoff does not confirm that exact release/checksum as authoritative.

For SL spoken, ../data/gold/sl_sst-ud-test.conllu likewise matches all 13
selected predictions. It is the repository's 432-sentence official standardised
SST file, pinned to the byte-identical r2.16/r2.17 version. The local 420-sentence
-pog file is the colloquial version used in the existing v5 paired-transcription
analysis; -stan is its standardised partner and was not evaluated in v5. Neither
has the sentence/ID structure of the AM spoken predictions. For both aligned
SL candidates, 8 of 13 prediction files reproduce the complete sent_id sequence;
the other five have incomplete sent_id metadata.

No EN or NL gold candidate was found in the targeted repository search.
Structural alignment does not establish gold provenance, so all seven cohorts
remain blocking and no initial-debugging evaluation can safely begin yet.

## File map

- source/ — immutable prediction inputs supplied for the benchmark.
- scripts/ — audit, source-resolution, gold-requirements, evaluation-wrapper,
  and UI-data build tools.
- ui/ — isolated local static benchmark UI prototype and generated result-data
  bundle.
- reports/source_resolution.md — evidence and canonical-selection decision.
- reports/canonical_predictions.tsv — one row per logical prediction run.
- reports/excluded_or_ambiguous_files.tsv — every noncanonical physical source
  file and its reason.
- reports/gold_requirements.tsv — one row per required language/test gold
  cohort.
- reports/prediction_gold_mapping.tsv — run-to-cohort mapping and readiness.
- reports/gold_questions.md — the remaining collaborator clarification list.
- reports/smoke_test/sl_spacy_stanza_results.tsv — provisional evaluator
  fixture rows; not authoritative benchmark output.
- reports/ui_prototype_notes.md — prototype implementation and QA handoff.

## Local result-data and UI prototype

The local engineering path is:

~~~text
canonical prediction + confirmed/provisional gold
    -> scripts/run_benchmark_evaluation.py
    -> machine-readable evaluation-result TSV
    -> scripts/build_ui_data.py
    -> ui/data/results.js
    -> ui/index.html
~~~

The browser derives available language, model, training-condition, and
test-condition options from result rows; it does not encode individual run
combinations. The current bundle contains only the 12 provisional SL
spaCy/Stanza smoke-test rows. Its visible warning is driven by each row's
`gold_status`, `result_status`, and benchmark-use notice, so an authoritative
future result does not inherit the provisional label.

From `am_benchmark/`:

~~~text
python3 scripts/build_ui_data.py
python3 -m http.server 8000
~~~

Then open `http://127.0.0.1:8000/ui/`. This is a local prototype, not a
replacement for the deployed interface.

## Next stage

Authoritative evaluation starts only after each required gold cohort is mapped
to a confirmed CoNLL-U file. Once those results exist, rebuild the UI bundle
from the authoritative result TSV and validate the multilingual interface
before any production integration. Other usable systems remain provisional
until their result stability is confirmed.
