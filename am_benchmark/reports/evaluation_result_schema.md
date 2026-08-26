# Evaluation result schema

## Purpose and grain

One TSV row represents one logical prediction run evaluated against one gold
cohort with one pinned evaluator file. The schema is language-independent and
can hold future EN, NL, and SL runs without adding identifying columns.

The provisional implementation is demonstrated by
`reports/smoke_test/sl_spacy_stanza_results.tsv`. A failed evaluator invocation
still has one row: `result_status` is `error`, `error_message` is populated, and
metric fields are empty.

## Identification, status, and provenance fields

| Field | Type | Meaning |
|---|---|---|
| `result_scope` | string | Official or explicitly provisional execution scope. |
| `gold_provenance_notice` | string | Whether gold provenance is authoritative or unconfirmed. |
| `benchmark_use_notice` | string | Mandatory non-publication warning for provisional rows. |
| `language` | string | Manifest language code. |
| `model` | string | Manifest model/system name. |
| `training_condition` | string | Manifest training condition. |
| `test_condition` | string | Manifest test condition. |
| `gold_cohort` | string | Shared language/test gold requirement. |
| `gold_file` | path string | Repository-relative gold path. |
| `prediction_file` | path string | Repository-relative canonical prediction path. |
| `gold_status` | string | Status copied from the gold mapping. |
| `result_status` | enum | `success` or `error`. |
| `repeat_deterministic` | enum | `true`, `false`, or `not_checked`. |
| `evaluator_file` | path string | Existing evaluator implementation used. |
| `evaluator_sha256` | SHA-256 string | Pins evaluator content. |
| `gold_sha256` | SHA-256 string | Pins gold content. |
| `prediction_sha256` | SHA-256 string | Pins prediction content. |
| `error_message` | string | Empty on success; evaluator exception on failure. |

Provisional rows contain these exact labels:

~~~text
PROVISIONAL ENGINEERING SMOKE TEST
GOLD PROVENANCE NOT YET CONFIRMED
DO NOT TREAT AS BENCHMARK RESULT
~~~

## Evaluator metric fields

The metric families use the evaluator's exact names; no benchmark-specific
metrics are introduced:

~~~text
Tokens Sentences Words UPOS XPOS UFeats AllTags Lemmas UAS LAS CLAS MLAS BLEX
~~~

Each family has four numeric percentage-point columns:

- `<Metric>_precision`
- `<Metric>_recall`
- `<Metric>_f1`
- `<Metric>_aligned_accuracy`

Values come directly from the existing evaluator's score object and are
multiplied by 100. The TSV preserves numeric precision; a consumer may display
two decimals, matching the evaluator CLI. Aligned accuracy is empty for Tokens,
Sentences, and Words because the evaluator does not set `aligned_total` on those
three alignment scores.

The current frontend displays F1 for Lemmas, UPOS, XPOS, UAS, and LAS. It can
read those columns directly while retaining the other evaluator metrics for
future views. Tokens, Sentences, and Words are alignment diagnostics in this
pretokenised setup and must not be presented as model-quality findings.

## Consumer rules

- The unique run key is normally `language + model + training_condition +
  test_condition`; `gold_cohort` and file hashes make the evaluated inputs
  explicit.
- Only rows with `result_status=success` may feed metric displays.
- Official views must additionally require authoritative `gold_status` and must
  reject a non-empty `benchmark_use_notice`.
- Selector values must be derived from available rows, not from a presumed full
  cross-product.
- Raw numeric values should remain unchanged during aggregation; rounding is a
  display concern.
