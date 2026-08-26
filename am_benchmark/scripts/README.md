# AM benchmark workflow tools

`audit_source.py` turns the initial manual sanity checks on the supplied prediction
files into a small, repeatable audit. It inventories the inputs, detects exact
duplicates, checks basic CoNLL-U row structure, and records sentence-level
numbering anomalies before any evaluation work is considered.

The files under `source/` are immutable research inputs. The audit opens them only
for reading. It does not rename, move, delete, clean, rewrite, or otherwise repair
them, and it does not run model evaluation. Its only filesystem output is
`reports/source_audit.txt`; the `reports/` directory is created when needed.

## Running the audit

From `am_benchmark/`, run:

```text
python3 scripts/audit_source.py
```

The script uses only the Python standard library. It recursively scans files whose
names end exactly in `.conllu` under `source/EN`, `source/NL`, and `source/SL`.
Files with another final suffix, such as `.conllu_`, are outside the inventory.

The terminal output is a concise count summary. Full paths and findings are written
to `reports/source_audit.txt`. A run returns exit status 0 when there are no errors,
1 when row- or file-level errors are found, and 2 when an expected language input
directory is missing. Warnings alone do not make the run fail.

## Checks and interpretation

### File inventory

For each language the report counts all `.conllu` files, numbered browser/download
copies such as `foo(1).conllu`, raw files, and clean files. A final parenthesized
number is ignored only when deciding whether a file is raw or clean, so
`foo_clean(1).conllu` is both a numbered copy and a clean file. Raw and clean counts
therefore partition the total, while the numbered count overlaps them.

### Exact duplicates

SHA-256 is calculated from each file's bytes. The report lists duplicate hash
groups within a language and hashes shared by different language folders. Every
numbered copy is also compared with the same-directory unnumbered name; the result
is `identical`, `different`, or `counterpart missing`. Duplicate findings are
warnings or provenance information, not instructions to delete files.

### Basic file validity

An error is recorded when a file is empty, cannot be decoded as UTF-8, or contains
a non-comment, non-empty line with other than 10 tab-separated columns. Comments
are lines beginning with `#`; blank lines delimit sentences.

### Token IDs and HEAD values

The accepted ID forms are positive ordinary integers (`1`, `2`, ...), increasing
multiword ranges (`3-4`), and empty-node IDs (`3.1`, including sentence-initial
forms such as `0.1`). Thus `0.1` is deliberately valid. Ordinary rows must have a
non-negative integer HEAD. Multiword-token rows and empty-node rows must have `_`
as HEAD. Violations are errors because they do not match the row-level rules used
by this audit.

### Sentence-level structure

Within each sentence the script considers valid ordinary token IDs and reports:

- duplicate ordinary IDs;
- missing integers between 1 and the largest ordinary ID;
- non-root HEAD values that refer to an ordinary ID absent from that sentence.

These findings are warnings labelled as structural anomalies. They are not
automatically classified as corruption: irregular numbering or references may
reflect properties of the supplied data or earlier preprocessing and should be
reviewed in context.

### Raw versus clean

For each same-directory, unnumbered pair `foo.conllu` and `foo_clean.conllu`, the
script first compares the bytes. If they differ, it compares a basic structural
signature: the sequence of token-row IDs in each sentence, with malformed-column
rows represented explicitly. This detects changes in sentence boundaries, token
row counts, row order, or ID values. It intentionally does not compare annotations
such as FORM, UPOS, HEAD, or DEPREL as part of this particular structure check and
never attempts to fix either file.

## Warnings versus errors

Errors identify failures of the audit's basic file or row-level rules: empty or
non-UTF-8 files, wrong column counts, invalid ID syntax, or invalid HEAD form.
Warnings and informational findings cover duplicates, numbered-copy differences,
raw/clean differences, and sentence-level numbering or reference anomalies. An
error is a strong reason to inspect a file before using it; a warning is a prompt
for research interpretation, not a verdict that the input is unusable.

## Canonical source resolution

After the basic audit, run the complete source-resolution workflow from
`am_benchmark/`:

```text
python3 scripts/resolve_source.py
```

This workflow treats each language/model/training/test filename stem as one
logical prediction run. It associates raw, clean, numbered-copy, and nonstandard
alternate files; applies stronger evaluator-oriented checks to clean candidates;
summarises raw-to-clean field changes; checks cross-language byte and ID/FORM
identity; and compares local gold candidates by exact sentence, ID, FORM, and
`sent_id` signatures. It does not compute model scores and does not claim full UD
validation.

It writes:

- `reports/source_resolution.md` — the investigation and recommendation;
- `reports/canonical_predictions.tsv` — one row per logical prediction run;
- `reports/excluded_or_ambiguous_files.tsv` — every physical source file not
  selected as canonical, with a reason.

The stronger structural gate checks the basic rules above plus ID order, one root
per sentence, nonexistent HEAD targets, self-loops, longer dependency cycles,
multiword-token component placement, empty-node consistency, non-empty FORM
values, and the final blank line required by the repository evaluator. Passing
this gate means structurally safe for that evaluator; it does not establish
annotation correctness without a matching gold file.

## Gold requirements

After source resolution, build the distinct language/test gold cohorts and the
run-to-cohort mapping with:

~~~text
python3 scripts/build_gold_requirements.py
~~~

This is a targeted follow-up: it reads canonical_predictions.tsv, selected
prediction structure, repository documentation-backed local gold candidates, and
their structural signatures. It does not repeat duplicate/source resolution and
does not run scoring. It writes gold_requirements.tsv,
prediction_gold_mapping.tsv, and gold_questions.md under reports/.

## Manifest-driven evaluation wrapper

`run_benchmark_evaluation.py` calls the existing repository evaluator without
reimplementing its metrics. An explicit action is required. Normal mode accepts
only authoritative gold, so the current stable SL subset is blocked:

~~~text
python3 scripts/run_benchmark_evaluation.py --dry-run --initial-debugging-only --language SL --model spacy --model stanza
~~~

The two named local SL candidates may be used only through the explicit,
isolated engineering-smoke-test gate:

~~~text
python3 scripts/run_benchmark_evaluation.py --dry-run --smoke-test --initial-debugging-only --language SL --model spacy --model stanza
python3 scripts/run_benchmark_evaluation.py --execute --smoke-test --initial-debugging-only --language SL --model spacy --model stanza --repeat-check
~~~

Smoke-test output is restricted to reports/smoke_test/. Result rows include
input/evaluator hashes, all 13 base evaluator metric families, repeat status,
and explicit warnings that the gold provenance is unconfirmed and the values
are not benchmark results. The wrapper never writes to the production
predictions/, results/, or tables/ directories.

## Local UI data bundle

Build the static prototype's browser bundle from the current result TSV with:

~~~text
python3 scripts/build_ui_data.py
~~~

`build_ui_data.py` validates the result identifiers, rejects duplicate logical
keys, discovers evaluator metric families and available score/count fields from
the TSV header, and writes `ui/data/results.js`. It preserves row-level gold and
result statuses so the UI can show or hide provisional warnings without
language-specific assumptions. The browser never parses CoNLL-U inputs.
