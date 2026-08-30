# AM multilingual CoNLL-U benchmark

## Purpose

This directory adapts the repository's existing interactive CoNLL-U evaluation
platform to Aaron Maladry's multilingual benchmark. Prediction preparation is
separated from evaluation so source provenance, gold correspondence, exclusions,
and result status remain auditable.

## Current state

- The 80 source-named prediction runs resolve to 78 canonical logical runs after
  normalising NL `dialecttest` to `spokentest`.
- The unnumbered `_clean.conllu` file remains canonical for each retained run.
- All 78 canonical predictions are structurally usable: 36 spaCy/Stanza runs
  form the stable evaluated subset and 42 other runs remain provisional.
- NL Stanza default dialect/spoken files are byte-identical and deduplicated.
- The NL Trankit spoken-named file containing EN content remains excluded. Its
  distinct valid dialect-named counterpart supplies the canonical spoken run.
- Raw files, all 97 numbered copies, and four `.conllu_` alternates are
  noncanonical.
- Aaron's six supplied gold files are authoritative and map to EN/NL/SL written
  and spoken cohorts. All 78 canonical predictions have evaluator-compatible
  underlying text and sentence spans.
- The unchanged existing evaluator completed 36/36 stable spaCy/Stanza runs,
  with identical numeric output on repetition.
- The local UI bundle contains those 36 authoritative rows across EN, NL, and
  SL. It remains isolated from the production interactive table.

## Workflow

~~~mermaid
flowchart TD
    A[Source prediction files] --> B[Resolution and structural validation]
    B --> C[80 source-named runs]
    C --> D[NL spoken/dialect normalisation]
    D --> E[78 canonical logical runs]
    E --> S[36 stable spaCy/Stanza runs]
    E --> P[42 usable provisional runs]
    A --> X[Wrong-language and noncanonical files audited]
    G[6 authoritative supplied gold cohorts] --> V[Prediction/gold compatibility]
    S --> V
    V --> R[36 deterministic authoritative results]
    R --> U[Local multilingual UI bundle]
~~~

## Benchmark dimensions

The values are derived from `reports/canonical_predictions.tsv`; not every
cross-product combination occurs.

- Languages: EN, NL, SL.
- Systems: UDpipe2, UDpipessj, UDPipesst, diaparser, singletaskXPOS,
  singletaskXPOSclassification, spacy, stanza, trankit, trankit_1epochs,
  trankit_2epochs, trankit_50epochs.
- Training conditions: default, writtentrain, writtenandspokentrain,
  writtenanddialecttrain.
- Canonical test conditions: writtentest, spokentest. Original NL dialect labels
  remain in provenance fields.
- Authoritative metrics currently cover only the stable spaCy/Stanza subset.
  Historical SL smoke-test files remain under `reports/smoke_test/` as fixtures.

## Gold readiness

The 78 canonical runs use six shared authoritative gold cohorts:

| Gold cohort | Logical runs | Stable runs | Supplied file |
|---|---:|---:|---|
| EN written | 12 | 6 | `source/gold/en_gold_test_written_final_clean.conllu` |
| EN spoken | 12 | 6 | `source/gold/en_gold_test_spoken_final_clean.conllu` |
| NL written | 15 | 6 | `source/gold/nl_gold_test_written_final_clean.conllu` |
| NL spoken | 13 | 6 | `source/gold/nl_gold_test_spoken_final_clean.conllu` |
| SL written | 13 | 6 | `source/gold/sl_gold_test_written_final_clean.conllu` |
| SL spoken | 13 | 6 | `source/gold/sl_gold_test_spoken_final_clean.conllu` |

The supplied SL written file is byte-identical to the repository's SSJ gold.
The supplied SL spoken file is structurally identical to the repository's SST
gold but not byte-identical: it adds metadata and changes 10 `MISC` values.
`reports/gold_requirements.tsv` records checksums, counts, inferred identities,
exact structure/surface matches, evaluator compatibility, and normalisation.

## File map

- `source/` — immutable local prediction inputs and `source/gold/` authoritative
  local gold; these transferred/private inputs remain gitignored.
- `scripts/` — audit, resolution, gold mapping, evaluation, and UI build tools.
- `ui/` — isolated local static benchmark UI and generated data bundle.
- `reports/source_resolution.md` — source evidence and canonical decisions.
- `reports/canonical_predictions.tsv` — one row per canonical logical run.
- `reports/excluded_or_ambiguous_files.tsv` — every noncanonical physical file.
- `reports/gold_requirements.tsv` — one row per authoritative language/test gold
  cohort.
- `reports/prediction_gold_mapping.tsv` — run-to-gold mapping and readiness.
- `reports/gold_questions.md` — resolved decisions and optional metadata follow-up.
- `reports/authoritative_spacy_stanza_results.tsv` — 36 authoritative stable rows.
- `reports/smoke_test/` — historical provisional engineering fixtures.

## Reproduce and view

From `am_benchmark/`:

~~~text
python3 scripts/audit_source.py
python3 scripts/resolve_source.py
python3 scripts/build_gold_requirements.py
python3 scripts/run_benchmark_evaluation.py --execute --initial-debugging-only --model spacy --model stanza --repeat-check
python3 scripts/build_ui_data.py
python3 -m http.server 8000 --bind 127.0.0.1
~~~

The authoritative result filename is available only with
`--initial-debugging-only`, which is additionally restricted to spaCy/Stanza.
An unrestricted run writes `reports/general_evaluation_results.tsv` instead and
marks the 42 non-stable system rows as provisional.

Open `http://127.0.0.1:8000/ui/`. The browser derives all available dimensions
from the 36-row result bundle. NL exposes only the canonical spoken condition,
and authoritative rows do not display a provisional warning.

## Next stage

The stable subset and local UI data are complete. Production integration still
requires review, and the 42 non-spaCy/Stanza runs remain provisional until their
result stability is confirmed.
