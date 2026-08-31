#!/usr/bin/env python3
"""Derive per-run aggregate diagnostics for the stable spaCy/Stanza benchmark subset.

Nothing here re-resolves sources, re-maps gold, re-selects predictions or rescores
the benchmark. File selection comes from ``run_benchmark_evaluation`` (the same
manifest rows and the same authoritative gold/prediction paths); per-relation LAS
and per-tag UPOS come from the unmodified repository evaluator; dependency and
tagging error categories come from the published CJVT profiler in
``build_interactive_comparison_table_v2``, so the error definitions stay identical
to the v2/v3/v5 bundles.

CORPUS TEXT NEVER ENTERS THE OUTPUT. This is a property of the generator, not of
the page that reads it:

1. ``collect_model_profile`` is called with ``max_examples=0``, so the profiler's
   example lists stay empty and no sentence is ever built;
2. only the profiler's *counters* are emitted -- the ``*_examples`` structures are
   never read;
3. the lemma layer is reduced to a single error count, because gold and predicted
   lemmas are themselves corpus text;
4. ``assert_aggregate_only`` walks the finished payload and refuses to write any
   string that is not a short, whitespace-free annotation label.

Redistribution permission is not established for every supplied gold source, so the
aggregate set publishes derived counts for every run without exception. Sentences for
the cohorts that may be republished are a separate layer, written by
``build_examples_data.py`` under its own licensing allowlist; this generator produces
none of them and its output is unchanged by that layer's existence.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

BENCHMARK_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = BENCHMARK_DIR.parent

sys.path.insert(0, str(BENCHMARK_DIR / "scripts"))
sys.path.insert(0, str(REPO_DIR / "scripts"))

import build_interactive_comparison_table_v2 as v2  # noqa: E402  CJVT error semantics
import run_benchmark_evaluation as benchmark  # noqa: E402  manifest + evaluator access

SCHEMA_VERSION = 1
GENERATOR = "am_benchmark/scripts/build_diagnostics_data.py"

# Emitted alongside every payload so a reader of the raw file knows the policy
# without having to consult this module.
CONTENT_POLICY = "aggregate-only"
CONTENT_POLICY_NOTE = (
    "Derived counts and annotation labels only. No corpus sentence, sentence "
    "fragment, token form, lemma or source comment is present, by construction "
    "of the generator rather than by omission in the interface."
)

# One destination: the benchmark interface has a single copy, under tables/.
DEFAULT_OUTPUT_DIRS = [REPO_DIR / "tables/am_benchmark/data/diagnostics"]

# Matched against every DEPREL/UPOS value the evaluator reports, so per-relation
# and per-tag results cover the whole tagset actually present.
ALL_VALUES = ".*"

# Order follows the three-way distinction the CJVT profiler defines; the labels
# are the page's, the buckets are v2's.
ERROR_CATEGORIES = [
    ("both_wrong", "Wrong relation and wrong head", ["gold_relation", "predicted_relation", "count"]),
    ("rel_only", "Correct head, wrong relation", ["gold_relation", "predicted_relation", "count"]),
    ("head_only", "Correct relation, wrong head", ["gold_relation", "count"]),
]

SUMMARY_METRICS = ["UPOS", "XPOS", "Lemmas", "UAS", "LAS"]

# An annotation label is one short field: a relation name, a UPOS tag, or a
# language-specific XPOS tag. It never spans two whitespace-separated words, which
# is the minimum a sentence or a sentence fragment needs. One value in the supplied
# Dutch spoken gold carries a trailing space ("WW|inf|vrij|zonder| "); that is a
# stray character inside a single tag, so the rule is written about word runs
# rather than about the presence of any whitespace.
MAX_LABEL_LENGTH = 64

# Payload keys whose string values are generator-controlled provenance rather
# than data derived from annotation values.
PROVENANCE_KEYS = {
    "schema_version",
    "kind",
    "content_policy",
    "content_policy_note",
    "generator",
    "key",
    "language",
    "test_condition",
    "model",
    "training_condition",
    "gold_cohort",
    "gold_file",
    "gold_sha256",
    "gold_status",
    "prediction_file",
    "prediction_sha256",
    "evaluator_file",
    "evaluator_sha256",
    "label",
    "columns",
    "file",
    "note",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Write aggregate CoNLL-U diagnostics for the 36 stable spaCy/Stanza runs. "
            "Reuses the benchmark's own file selection and the unmodified evaluator."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        action="append",
        help=(
            "Destination directory for the diagnostics set. Repeatable. Defaults to "
            "tables/am_benchmark/data/diagnostics."
        ),
    )
    parser.add_argument("--language", action="append", help="Restrict to a language.")
    parser.add_argument("--model", action="append", help="Restrict to a system.")
    parser.add_argument(
        "--training-condition", action="append", help="Restrict to a training condition."
    )
    parser.add_argument(
        "--test-condition", action="append", help="Restrict to a test condition."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report the selected runs and write nothing.",
    )
    return parser.parse_args()


def stable_runs(args: argparse.Namespace) -> list[dict[str, str]]:
    """The stable subset, selected exactly as the authoritative evaluation selects it."""
    filters = {
        "language": args.language,
        "model": args.model,
        "training_condition": args.training_condition,
        "test_condition": args.test_condition,
    }
    selected = []
    for row in benchmark.load_mapping():
        if not row["selected_prediction"] or not benchmark.is_stable_result(row):
            continue
        if not all(not allowed or row[field] in allowed for field, allowed in filters.items()):
            continue
        permitted, reason = benchmark.permission_reason(row, smoke_test=False)
        if not permitted:
            raise RuntimeError(
                f"Stable run is not evaluation-permitted: "
                f"{row['language']} {row['model']} {row['training_condition']} "
                f"{row['test_condition']} ({reason})"
            )
        selected.append(row)
    return selected


def run_key(row: dict[str, str]) -> str:
    return "-".join(
        (row["language"], row["test_condition"], row["model"], row["training_condition"])
    )


def scored_rows(evaluation: dict[str, Any], prefix: str) -> list[list[Any]]:
    """Per-value scores from the evaluator, gold-attested values only.

    ``get_unquie_col_vals`` unions gold and system values, so a value the system
    invented but the gold never uses appears with a zero gold total. Those belong
    in the confusion tables, not in a gold-relative accuracy table.
    """
    aggregate_key = f"{prefix}_{ALL_VALUES}"
    rows = []
    for key, score in evaluation.items():
        if not key.startswith(f"{prefix}_") or key == aggregate_key:
            continue
        if score.gold_total <= 0:
            continue
        rows.append([key[len(prefix) + 1:], score.gold_total, score.correct, score.system_total])
    rows.sort(key=lambda row: (-row[1], row[0]))
    return rows


def counter_rows(counter: Counter, paired: bool) -> list[list[Any]]:
    """Confusion or single-label rows from a v2 counter, deterministically ordered.

    The v2 row builders define the key format and the count semantics; this only
    unpacks their output into positional columns so the emitted file stays small
    and self-describing.
    """
    rows = []
    for key, count in counter.items():
        if paired:
            parts = key.split("__to__")
            if len(parts) != 2:
                raise ValueError(f"Unexpected paired error key: {key!r}")
            rows.append([parts[0], parts[1], count])
        else:
            if "__to__" in key:
                raise ValueError(f"Unexpected paired error key in single-label bucket: {key!r}")
            rows.append([key, count])
    rows.sort(key=lambda row: (-row[-1], row[:-1]))
    return rows


def dependency_error_tables(profile: dict[str, Any]) -> list[dict[str, Any]]:
    """The v2 three-way distinction, unpacked into positional rows."""
    ordered = v2.build_deprel_error_rows(profile)
    tables = []
    for bucket, label, columns in ERROR_CATEGORIES:
        if bucket not in ordered:
            raise ValueError(f"CJVT profiler produced no {bucket!r} bucket")
        paired = len(columns) == 3
        rows = counter_rows(profile["deprel_counters"][bucket], paired)
        if len(rows) != len(ordered[bucket]):
            raise ValueError(f"Row count disagreement in bucket {bucket!r}")
        tables.append(
            {
                "key": bucket,
                "label": label,
                "columns": columns,
                "total": sum(row[-1] for row in rows),
                "rows": rows,
            }
        )
    return tables


def tag_error_tables(profile: dict[str, Any]) -> dict[str, Any]:
    """UPOS and XPOS confusion pairs; lemma errors as a count only.

    Lemma pairs are corpus text and are therefore never emitted, however the
    profiler counts them.
    """
    ordered = v2.build_tag_error_rows(profile)
    tables: dict[str, Any] = {}
    for layer in ("upos", "xpos"):
        rows = counter_rows(profile["tag_counters"][layer], paired=True)
        if len(rows) != len(ordered[layer]):
            raise ValueError(f"Row count disagreement in tag layer {layer!r}")
        tables[layer] = {
            "columns": ["gold", "predicted", "count"],
            "total": sum(row[-1] for row in rows),
            "rows": rows,
        }
    tables["lemma"] = {
        "columns": [],
        "total": sum(profile["tag_counters"]["lemma"].values()),
        "rows": [],
        "note": (
            "Count only. Gold and predicted lemmas are corpus text and are not "
            "published in this diagnostic set."
        ),
    }
    return tables


def reconcile(
    key: str,
    evaluation: dict[str, Any],
    profile: dict[str, Any],
    las_rows: list[list[Any]],
    upos_rows: list[list[Any]],
    dependency_tables: list[dict[str, Any]],
) -> None:
    """Refuse to emit anything whose parts do not add up.

    The evaluator aligns words itself; the CJVT profiler compares gold and
    prediction position by position. Both views must describe the same token
    population, or the diagnostics would mix two different denominators.
    """
    totals = profile["totals"]
    las = evaluation["LAS"]
    upos = evaluation["UPOS"]
    problems = []

    for skipped in ("skipped_len_mismatch", "skipped_form_mismatch"):
        if totals.get(skipped):
            problems.append(f"{skipped}={totals[skipped]}")

    if totals.get("compared") != las.gold_total:
        problems.append(
            f"compared={totals.get('compared')} != evaluator gold words={las.gold_total}"
        )
    if las.aligned_total != las.gold_total:
        problems.append(
            f"aligned words={las.aligned_total} != gold words={las.gold_total}"
        )
    if totals.get("las_correct") != las.correct:
        problems.append(
            f"profiler LAS correct={totals.get('las_correct')} != evaluator={las.correct}"
        )

    if sum(row[1] for row in las_rows) != las.gold_total:
        problems.append("per-relation gold totals do not sum to the evaluator gold total")
    if sum(row[2] for row in las_rows) != las.correct:
        problems.append("per-relation correct totals do not sum to the evaluator LAS correct")
    if sum(row[1] for row in upos_rows) != upos.gold_total:
        problems.append("per-tag gold totals do not sum to the evaluator gold total")
    if sum(row[2] for row in upos_rows) != upos.correct:
        problems.append("per-tag correct totals do not sum to the evaluator UPOS correct")

    errors = sum(table["total"] for table in dependency_tables)
    if errors != las.gold_total - las.correct:
        problems.append(
            f"dependency error categories sum to {errors}, "
            f"expected {las.gold_total - las.correct}"
        )

    if problems:
        raise RuntimeError(
            f"{key}: gold and prediction are not diagnostically compatible — "
            + "; ".join(problems)
        )


def is_annotation_label(value: str) -> bool:
    return len(value) <= MAX_LABEL_LENGTH and len(value.split()) <= 1


def assert_aggregate_only(key: str, payload: Any, path: tuple[str, ...] = ()) -> None:
    """Refuse to write anything but counts and annotation labels.

    Two rules, because either alone would be weak. Structurally, a string is only
    allowed under a generator-controlled provenance key or inside ``tables``; a
    field that started carrying examples would land somewhere else and be refused
    outright. By shape, a string inside ``tables`` must still be a single short
    annotation label, so a sentence or a fragment is refused even if it were given
    an expected key.
    """
    if isinstance(payload, dict):
        for name, value in payload.items():
            assert_aggregate_only(key, value, path + (str(name),))
        return
    if isinstance(payload, list):
        for value in payload:
            assert_aggregate_only(key, value, path)
        return
    if not isinstance(payload, str):
        return
    where = ".".join(path) or "<root>"
    if path and path[-1] in PROVENANCE_KEYS:
        return
    if path[:1] != ("tables",):
        raise RuntimeError(
            f"{key}: refused to write an unexpected free string at {where}: {payload[:80]!r}"
        )
    if not is_annotation_label(payload):
        raise RuntimeError(
            f"{key}: refused to write a value that is not an annotation label at "
            f"{where}: {payload[:80]!r}"
        )


def build_run(evaluator, row: dict[str, str]) -> dict[str, Any]:
    key = run_key(row)
    gold_path = benchmark.resolve_manifest_path(row["gold_file"])
    prediction_path = benchmark.resolve_manifest_path(row["selected_prediction"])

    # The evaluator raises UDError when the two files do not describe the same
    # underlying text; that is the intended hard failure, so it is not caught.
    evaluation = evaluator.evaluate(
        evaluator.load_conllu_file(str(gold_path)),
        evaluator.load_conllu_file(str(prediction_path)),
        upos=ALL_VALUES,
        las=ALL_VALUES,
    )

    gold_sentences = v2.read_conllu(gold_path)
    prediction_sentences = v2.read_conllu(prediction_path)
    # max_examples=0 keeps every example list empty; the counters are the only
    # thing this generator reads.
    profile = v2.collect_model_profile(gold_sentences, prediction_sentences, 0)

    las_rows = scored_rows(evaluation, "LAS")
    upos_rows = scored_rows(evaluation, "UPOS")
    dependency_tables = dependency_error_tables(profile)
    reconcile(key, evaluation, profile, las_rows, upos_rows, dependency_tables)

    las = evaluation["LAS"]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "kind": "am-benchmark-run-diagnostics",
        "content_policy": CONTENT_POLICY,
        "content_policy_note": CONTENT_POLICY_NOTE,
        "generator": GENERATOR,
        "run": {
            "key": key,
            "language": row["language"],
            "test_condition": row["test_condition"],
            "model": row["model"],
            "training_condition": row["training_condition"],
        },
        "provenance": {
            "gold_cohort": row["gold_cohort"],
            "gold_status": row["gold_status"],
            "gold_file": benchmark.display_path(gold_path),
            "gold_sha256": benchmark.sha256(gold_path),
            "prediction_file": benchmark.display_path(prediction_path),
            "prediction_sha256": benchmark.sha256(prediction_path),
            "evaluator_file": benchmark.display_path(benchmark.EVALUATOR_PATH),
            "evaluator_sha256": benchmark.sha256(benchmark.EVALUATOR_PATH),
        },
        "summary": {
            "gold_words": las.gold_total,
            "aligned_words": las.aligned_total,
            "las_correct": las.correct,
            "uas_correct": evaluation["UAS"].correct,
            "upos_correct": evaluation["UPOS"].correct,
            "relations_attested": len(las_rows),
            "tags_attested": len(upos_rows),
            "f1": {name: 100.0 * evaluation[name].f1 for name in SUMMARY_METRICS},
        },
        "tables": {
            "las_by_relation": {
                "columns": ["relation", "gold", "correct", "predicted"],
                "rows": las_rows,
            },
            "upos_accuracy": {
                "columns": ["tag", "gold", "correct", "predicted"],
                "rows": upos_rows,
            },
            "dependency_errors": {"categories": dependency_tables},
            "tag_errors": tag_error_tables(profile),
        },
    }
    assert_aggregate_only(key, payload)
    return payload


def write_json(path: Path, payload: Any) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=False) + "\n"
    path.write_text(text, encoding="utf-8")
    return len(text.encode("utf-8"))


def main() -> int:
    args = parse_args()
    runs = stable_runs(args)
    if not runs:
        print("No stable runs selected.", file=sys.stderr)
        return 2

    print(f"Stable runs selected: {len(runs)}")
    for row in runs:
        print(f"  {run_key(row)}")
    if args.dry_run:
        print("Dry run only; the evaluator was not invoked and nothing was written.")
        return 0

    evaluator = benchmark.load_evaluator()
    payloads = {}
    for row in runs:
        key = run_key(row)
        payloads[key] = build_run(evaluator, row)
        summary = payloads[key]["summary"]
        print(
            f"  {key}: {summary['gold_words']} gold words, "
            f"{summary['relations_attested']} relations, {summary['tags_attested']} tags"
        )

    index = {
        "schema_version": SCHEMA_VERSION,
        "kind": "am-benchmark-diagnostics-index",
        "content_policy": CONTENT_POLICY,
        "content_policy_note": CONTENT_POLICY_NOTE,
        "generator": GENERATOR,
        "runs": [
            {
                "key": key,
                "language": payload["run"]["language"],
                "test_condition": payload["run"]["test_condition"],
                "model": payload["run"]["model"],
                "training_condition": payload["run"]["training_condition"],
                "file": f"{key}.json",
            }
            for key, payload in payloads.items()
        ],
    }
    assert_aggregate_only("index", index)

    output_dirs = args.output_dir or DEFAULT_OUTPUT_DIRS
    for directory in output_dirs:
        directory = directory if directory.is_absolute() else REPO_DIR / directory
        total = write_json(directory / "index.json", index)
        for key, payload in payloads.items():
            total += write_json(directory / f"{key}.json", payload)
        try:
            shown = directory.resolve().relative_to(REPO_DIR)
        except ValueError:
            shown = directory
        print(f"Wrote {len(payloads) + 1} files to {shown} ({total / 1024:.0f} KiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
