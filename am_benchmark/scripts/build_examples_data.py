#!/usr/bin/env python3
"""Extract sentence examples for the Slovenian stable runs only.

The aggregate diagnostics under ``tables/am_benchmark/data/diagnostics/`` stay
exactly as they are: counts and annotation labels, no corpus text. This script
writes a *separate* layer that the analysis page loads only when a reader asks to
see examples for one error pattern, and only for cohorts whose corpus may be
redistributed.

Nothing here re-resolves sources or re-classifies errors. Run selection comes from
``run_benchmark_evaluation`` through ``build_diagnostics_data``; which token is an
example of which error comes from the published CJVT profiler
(``build_interactive_comparison_table_v2.collect_model_profile``), so an example
row can only ever belong to an error pattern the aggregate file already reports.
The emitted counters are checked against that file before anything is written.

ONLY THE ALLOWLISTED COHORTS ARE EXTRACTED. English and Dutch gold were supplied
for benchmarking and redistribution permission has not been established for them,
so a run outside ``COHORT_SOURCES`` raises rather than producing a file.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from argparse import Namespace
from pathlib import Path
from typing import Any

BENCHMARK_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = BENCHMARK_DIR.parent

sys.path.insert(0, str(BENCHMARK_DIR / "scripts"))
sys.path.insert(0, str(REPO_DIR / "scripts"))

import build_diagnostics_data as diagnostics  # noqa: E402  run selection + run keys
import build_interactive_comparison_table_v2 as v2  # noqa: E402  CJVT error/example semantics
import run_benchmark_evaluation as benchmark  # noqa: E402  manifest paths + hashing

SCHEMA_VERSION = 1
GENERATOR = "am_benchmark/scripts/build_examples_data.py"

# The panel shows at most this many examples for one error pattern and always
# reports the pattern's full occurrence count beside them.
MAX_EXAMPLES = 25

DEFAULT_OUTPUT_DIR = REPO_DIR / "tables/am_benchmark/data/examples"
DIAGNOSTICS_DIR = REPO_DIR / "tables/am_benchmark/data/diagnostics"

# The allowlist is a licensing fact, not something derivable from the data, so it
# is stated once here. A cohort absent from this table produces no examples.
# Both Slovenian treebanks are released under CC BY-SA 4.0; the release labels are
# the ones the benchmark's own test-set identification already established.
COHORT_SOURCES = {
    "SL:writtentest": {
        "corpus": "UD Slovenian SSJ",
        "release": "r2.17",
        "url": "https://github.com/UniversalDependencies/UD_Slovenian-SSJ",
        "licence": "CC BY-SA 4.0",
    },
    "SL:spokentest": {
        "corpus": "UD Slovenian SST",
        "release": "r2.16 / r2.17",
        "url": "https://github.com/UniversalDependencies/UD_Slovenian-SST",
        "licence": "CC BY-SA 4.0",
    },
}

# Positional example columns, declared in the payload so the file reads on its own.
DEPENDENCY_COLUMNS = ["sentence", "token", "gold_head", "predicted_head"]
TAG_COLUMNS = ["sentence", "token"]

# The accuracy tables are clickable too, so each gold relation and each gold UPOS
# tag gets its own sample of the tokens it got wrong. A relation example also
# carries which of the three categories it fell into, as an index into
# DEPENDENCY_BUCKETS, so the panel can say why each one is an error.
RELATION_ERROR_COLUMNS = [
    "sentence", "token", "gold_head", "predicted_head", "category", "predicted_relation"
]
UPOS_ERROR_COLUMNS = ["sentence", "token", "predicted"]

DEPENDENCY_BUCKETS = ["both_wrong", "rel_only", "head_only"]
TAG_LAYERS = ["upos", "xpos"]

ROOT = -1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Write sentence examples for the allowlisted Slovenian stable runs. "
            "Aggregate diagnostics and benchmark results are read-only inputs."
        )
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--test-condition", action="append", help="Restrict to a test condition.")
    parser.add_argument("--model", action="append", help="Restrict to a system.")
    parser.add_argument(
        "--training-condition", action="append", help="Restrict to a training condition."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Report the selected runs and write nothing."
    )
    return parser.parse_args()


def allowlisted_runs(args: argparse.Namespace) -> list[dict[str, str]]:
    """Stable runs whose gold cohort may be republished as sentences.

    Selection is the benchmark's own: ``build_diagnostics_data.stable_runs`` applies
    the same manifest filters and permission gate the authoritative evaluation uses.
    """
    languages = sorted({cohort.split(":", 1)[0] for cohort in COHORT_SOURCES})
    selection = Namespace(
        language=languages,
        model=args.model,
        training_condition=args.training_condition,
        test_condition=args.test_condition,
    )
    runs = []
    for row in diagnostics.stable_runs(selection):
        cohort = row["gold_cohort"]
        if cohort not in COHORT_SOURCES:
            raise RuntimeError(
                f"Refusing to extract examples for {cohort}: not in the redistribution "
                f"allowlist. Add it to COHORT_SOURCES only when its licence permits."
            )
        runs.append(row)
    return runs


def sentence_index(gold_sentences, prediction_sentences) -> dict[str, tuple[int, Any, Any]]:
    """Map the profiler's sentence identifier to its gold and predicted sentence.

    ``collect_model_profile`` labels an example with ``sent_id`` when the file has
    one and the aligned position otherwise; the same alignment helper and the same
    fallback are used here so a label always resolves to the sentence it came from.
    """
    pairs, _, _ = v2.align_sentences(gold_sentences, prediction_sentences)
    index: dict[str, tuple[int, Any, Any]] = {}
    for gold_idx, gold_sentence, _pred_idx, prediction_sentence in pairs:
        label = gold_sentence.get("sent_id") or str(gold_idx + 1)
        if label in index:
            raise RuntimeError(f"Duplicate sentence identifier in gold data: {label}")
        index[label] = (gold_idx, gold_sentence, prediction_sentence)
    return index


def token_position(sentence, token_id: int) -> int:
    """Index of a 1-based CoNLL-U token id in the parsed token list."""
    position = token_id - 1
    tokens = sentence["tokens"]
    if not 0 <= position < len(tokens) or tokens[position]["id"] != token_id:
        raise RuntimeError(f"Token id {token_id} does not address its own row")
    return position


def head_position(token, length: int) -> int:
    """Head as a 0-based token index, or ROOT for HEAD=0."""
    try:
        head = int(token["head"])
    except (TypeError, ValueError):
        raise RuntimeError(f"Unparsable HEAD {token['head']!r}") from None
    if head == 0:
        return ROOT
    if not 1 <= head <= length:
        raise RuntimeError(f"HEAD {head} points outside a sentence of {length} words")
    return head - 1


class SentencePool:
    """Sentences referenced by at least one example, stored once each.

    Only the identifier and the token forms are kept. Speaker, document, audio and
    MISC fields are never read: the CJVT reader parses ``sent_id`` and ``text`` and
    nothing else out of the comment block, and ``text`` is not emitted.
    """

    def __init__(self) -> None:
        self._positions: dict[int, int] = {}
        self.rows: list[list[Any]] = []

    def index_of(self, gold_idx: int, gold_sentence, label: str) -> int:
        if gold_idx not in self._positions:
            self._positions[gold_idx] = len(self.rows)
            self.rows.append([label, [token["form"] for token in gold_sentence["tokens"]]])
        return self._positions[gold_idx]


def dependency_example(pool: SentencePool, sentences, item) -> list[Any]:
    label = item["sid"]
    gold_idx, gold_sentence, prediction_sentence = sentences[label]
    token_id = int(item["token_id"])
    position = token_position(gold_sentence, token_id)
    gold_token = gold_sentence["tokens"][position]
    prediction_token = prediction_sentence["tokens"][position]
    if gold_token["form"] != prediction_token["form"]:
        raise RuntimeError(f"Gold and predicted token disagree at {label}#{token_id}")
    length = len(gold_sentence["tokens"])
    return [
        pool.index_of(gold_idx, gold_sentence, label),
        position,
        head_position(gold_token, length),
        head_position(prediction_token, length),
    ]


def tag_example(pool: SentencePool, sentences, item) -> list[Any]:
    label = item["sid"]
    gold_idx, gold_sentence, _prediction_sentence = sentences[label]
    position = token_position(gold_sentence, int(item["token_id"]))
    return [pool.index_of(gold_idx, gold_sentence, label), position]


def classify(gold_token, prediction_token) -> str | None:
    """The CJVT profiler's own three-way split, restated for a second traversal.

    ``collect_model_profile`` makes exactly this decision from exactly these two
    comparisons; the relation index needs the outcome per token rather than per
    confusion pair, and ``check_relation_totals`` proves the two agree.
    """
    head_ok = gold_token["head"] == prediction_token["head"]
    relation_ok = gold_token["deprel"] == prediction_token["deprel"]
    if head_ok and relation_ok:
        return None
    if head_ok:
        return "rel_only"
    if relation_ok:
        return "head_only"
    return "both_wrong"


def accuracy_error_index(
    pool: SentencePool, gold_sentences, prediction_sentences
) -> tuple[dict[str, dict], dict[str, dict], dict[str, int], dict[str, int]]:
    """Per-relation LAS errors and per-tag UPOS errors, in corpus order.

    One traversal of the aligned sentences, taking the first MAX_EXAMPLES tokens
    for each gold relation and each gold tag, so the sample is deterministic and
    reproducible in the same way the profiler's is.
    """
    relations: dict[str, list] = {}
    tags: dict[str, list] = {}
    relation_totals: Counter = Counter()
    tag_totals: Counter = Counter()

    pairs, _, _ = v2.align_sentences(gold_sentences, prediction_sentences)
    for gold_idx, gold_sentence, _pred_idx, prediction_sentence in pairs:
        gold_tokens = gold_sentence["tokens"]
        prediction_tokens = prediction_sentence["tokens"]
        if len(gold_tokens) != len(prediction_tokens):
            continue
        label = gold_sentence.get("sent_id") or str(gold_idx + 1)
        length = len(gold_tokens)
        for position, (gold_token, prediction_token) in enumerate(zip(gold_tokens, prediction_tokens)):
            if gold_token["form"] != prediction_token["form"]:
                continue
            category = classify(gold_token, prediction_token)
            if category is not None:
                relation = gold_token["deprel"]
                relation_totals[relation] += 1
                examples = relations.setdefault(relation, [])
                if len(examples) < MAX_EXAMPLES:
                    examples.append([
                        pool.index_of(gold_idx, gold_sentence, label),
                        position,
                        head_position(gold_token, length),
                        head_position(prediction_token, length),
                        DEPENDENCY_BUCKETS.index(category),
                        prediction_token["deprel"],
                    ])
            if gold_token["upos"] != prediction_token["upos"]:
                tag = gold_token["upos"]
                tag_totals[tag] += 1
                examples = tags.setdefault(tag, [])
                if len(examples) < MAX_EXAMPLES:
                    examples.append([
                        pool.index_of(gold_idx, gold_sentence, label),
                        position,
                        prediction_token["upos"],
                    ])
    return relations, tags, relation_totals, tag_totals


def accuracy_error_totals(key: str) -> tuple[dict[str, int], dict[str, int]]:
    """Errors per gold relation and per gold tag, as the aggregate file states them."""
    data = json.loads((DIAGNOSTICS_DIR / f"{key}.json").read_text(encoding="utf-8"))
    tables = data["tables"]
    relations = {row[0]: row[1] - row[2] for row in tables["las_by_relation"]["rows"]}
    tags = {row[0]: row[1] - row[2] for row in tables["upos_accuracy"]["rows"]}
    return relations, tags


def check_relation_totals(key: str, counted, published, what: str) -> None:
    """Refuse to publish a sample whose population disagrees with the aggregate."""
    counted = {name: value for name, value in counted.items() if value}
    expected = {name: value for name, value in published.items() if value}
    if counted != expected:
        missing = sorted(set(expected) ^ set(counted))
        differing = sorted(
            name for name in set(expected) & set(counted) if expected[name] != counted[name]
        )
        raise RuntimeError(
            f"{key}: {what} error totals disagree with the aggregate table "
            f"(unmatched: {missing[:6]}, differing: {differing[:6]})"
        )


def aggregate_totals(key: str) -> dict[str, dict[str, int]]:
    """Error-pattern totals as the published aggregate file states them."""
    path = DIAGNOSTICS_DIR / f"{key}.json"
    if not path.is_file():
        raise RuntimeError(f"No aggregate diagnostics for {key}; run build_diagnostics_data.py")
    data = json.loads(path.read_text(encoding="utf-8"))
    totals: dict[str, dict[str, int]] = {}
    for category in data["tables"]["dependency_errors"]["categories"]:
        paired = len(category["columns"]) == 3
        totals[category["key"]] = {
            (f"{row[0]}__to__{row[1]}" if paired else row[0]): row[-1]
            for row in category["rows"]
        }
    for layer in TAG_LAYERS:
        table = data["tables"]["tag_errors"][layer]
        totals[layer] = {f"{row[0]}__to__{row[1]}": row[2] for row in table["rows"]}
    return totals


def check_against_aggregate(key: str, profile: dict[str, Any]) -> dict[str, dict[str, int]]:
    """Every extracted pattern must be a pattern the aggregate file already reports."""
    published = aggregate_totals(key)
    problems = []
    for bucket in DEPENDENCY_BUCKETS:
        counted = dict(profile["deprel_counters"][bucket])
        if counted != published.get(bucket):
            problems.append(f"{bucket} counters differ from the published aggregate")
    for layer in TAG_LAYERS:
        counted = dict(profile["tag_counters"][layer])
        if counted != published.get(layer):
            problems.append(f"{layer} counters differ from the published aggregate")
    totals = profile["totals"]
    for skipped in ("skipped_len_mismatch", "skipped_form_mismatch"):
        if totals.get(skipped):
            problems.append(f"{skipped}={totals[skipped]}")
    if problems:
        raise RuntimeError(f"{key}: refusing to write examples — " + "; ".join(problems))
    return published


def build_run(row: dict[str, str]) -> dict[str, Any]:
    key = diagnostics.run_key(row)
    cohort = row["gold_cohort"]
    gold_path = benchmark.resolve_manifest_path(row["gold_file"])
    prediction_path = benchmark.resolve_manifest_path(row["selected_prediction"])

    gold_sentences = v2.read_conllu(gold_path)
    prediction_sentences = v2.read_conllu(prediction_path)
    # The CJVT profiler decides which token is an example of which pattern; passing
    # the cap here is the only place the sample size is set.
    profile = v2.collect_model_profile(gold_sentences, prediction_sentences, MAX_EXAMPLES)
    published = check_against_aggregate(key, profile)

    sentences = sentence_index(gold_sentences, prediction_sentences)
    pool = SentencePool()

    dependency: dict[str, Any] = {}
    for bucket in DEPENDENCY_BUCKETS:
        patterns = {}
        for pattern, items in sorted(profile["deprel_examples"][bucket].items()):
            if not items:
                continue
            patterns[pattern] = {
                "total": published[bucket][pattern],
                "examples": [dependency_example(pool, sentences, item) for item in items],
            }
        dependency[bucket] = {"columns": DEPENDENCY_COLUMNS, "patterns": patterns}

    tags: dict[str, Any] = {}
    for layer in TAG_LAYERS:
        patterns = {}
        for pattern, items in sorted(profile["tag_examples"][layer].items()):
            if not items:
                continue
            patterns[pattern] = {
                "total": published[layer][pattern],
                "examples": [tag_example(pool, sentences, item) for item in items],
            }
        tags[layer] = {"columns": TAG_COLUMNS, "patterns": patterns}

    # The accuracy tables are clickable as well, so each gold relation and gold tag
    # gets its own error sample drawn from the same sentence pool.
    relation_examples, upos_examples, relation_counts, upos_counts = accuracy_error_index(
        pool, gold_sentences, prediction_sentences
    )
    published_relations, published_tags = accuracy_error_totals(key)
    check_relation_totals(key, relation_counts, published_relations, "per-relation LAS")
    check_relation_totals(key, upos_counts, published_tags, "per-tag UPOS")

    relation_errors = {
        "columns": RELATION_ERROR_COLUMNS,
        "categories": DEPENDENCY_BUCKETS,
        "patterns": {
            relation: {"total": relation_counts[relation], "examples": examples}
            for relation, examples in sorted(relation_examples.items())
        },
    }
    upos_errors = {
        "columns": UPOS_ERROR_COLUMNS,
        "patterns": {
            tag: {"total": upos_counts[tag], "examples": examples}
            for tag, examples in sorted(upos_examples.items())
        },
    }

    stored = sum(
        len(entry["examples"])
        for group in (dependency, tags)
        for table in group.values()
        for entry in table["patterns"].values()
    ) + sum(
        len(entry["examples"])
        for table in (relation_errors, upos_errors)
        for entry in table["patterns"].values()
    )
    over_cap = [
        entry for group in (dependency, tags) for table in group.values()
        for entry in table["patterns"].values() if len(entry["examples"]) > MAX_EXAMPLES
    ] + [
        entry for table in (relation_errors, upos_errors)
        for entry in table["patterns"].values() if len(entry["examples"]) > MAX_EXAMPLES
    ]
    if over_cap:
        raise RuntimeError(f"{key}: a pattern stored more than {MAX_EXAMPLES} examples")

    source = dict(COHORT_SOURCES[cohort])
    source.update({
        "gold_cohort": cohort,
        "gold_file": benchmark.display_path(gold_path),
        "gold_sha256": benchmark.sha256(gold_path),
        "prediction_file": benchmark.display_path(prediction_path),
        "prediction_sha256": benchmark.sha256(prediction_path),
    })

    return {
        "schema_version": SCHEMA_VERSION,
        "kind": "am-benchmark-run-examples",
        "generator": GENERATOR,
        "run": {
            "key": key,
            "language": row["language"],
            "test_condition": row["test_condition"],
            "model": row["model"],
            "training_condition": row["training_condition"],
        },
        "source": source,
        "max_examples_per_pattern": MAX_EXAMPLES,
        "sentences": {"columns": ["sent_id", "tokens"], "rows": pool.rows},
        "dependency": dependency,
        "tags": tags,
        "relation_errors": relation_errors,
        "upos_errors": upos_errors,
        "counts": {"sentences": len(pool.rows), "examples": stored},
    }


def write_json(path: Path, payload: Any) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"
    path.write_text(text, encoding="utf-8")
    return len(text.encode("utf-8"))


def main() -> int:
    args = parse_args()
    runs = allowlisted_runs(args)
    if not runs:
        print("No allowlisted runs selected.", file=sys.stderr)
        return 2

    print(f"Allowlisted cohorts: {', '.join(sorted(COHORT_SOURCES))}")
    print(f"Runs selected: {len(runs)}")
    for row in runs:
        print(f"  {diagnostics.run_key(row)}")
    if args.dry_run:
        print("Dry run only; nothing was read from the corpora and nothing was written.")
        return 0

    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = REPO_DIR / output_dir

    payloads = {}
    for row in runs:
        key = diagnostics.run_key(row)
        payloads[key] = build_run(row)
        counts = payloads[key]["counts"]
        print(f"  {key}: {counts['examples']} examples over {counts['sentences']} sentences")

    index = {
        "schema_version": SCHEMA_VERSION,
        "kind": "am-benchmark-examples-index",
        "generator": GENERATOR,
        "max_examples_per_pattern": MAX_EXAMPLES,
        "cohorts": COHORT_SOURCES,
        "runs": [
            {
                "key": key,
                "language": payload["run"]["language"],
                "test_condition": payload["run"]["test_condition"],
                "model": payload["run"]["model"],
                "training_condition": payload["run"]["training_condition"],
                "gold_cohort": payload["source"]["gold_cohort"],
                "file": f"{key}.json",
            }
            for key, payload in payloads.items()
        ],
    }

    total = write_json(output_dir / "index.json", index)
    for key, payload in payloads.items():
        total += write_json(output_dir / f"{key}.json", payload)
    try:
        shown = output_dir.resolve().relative_to(REPO_DIR)
    except ValueError:
        shown = output_dir
    print(f"Wrote {len(payloads) + 1} files to {shown} ({total / 1024:.0f} KiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
