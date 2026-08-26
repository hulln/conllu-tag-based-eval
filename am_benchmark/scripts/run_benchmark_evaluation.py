#!/usr/bin/env python3
"""Run manifest-selected benchmark evaluations through the existing evaluator.

Normal execution accepts only confirmed gold. ``--smoke-test`` explicitly
permits the two provisional Slovenian fixtures named in this project. Results
remain under ``am_benchmark/reports/`` and are never written to the
repository's production ``results/`` tree.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import sys
from pathlib import Path


BENCHMARK_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = BENCHMARK_DIR.parent
REPORT_DIR = BENCHMARK_DIR / "reports"
MAPPING_PATH = REPORT_DIR / "prediction_gold_mapping.tsv"
EVALUATOR_PATH = REPO_DIR / "scripts" / "conll18_ud_eval_tag-based.py"

AUTHORITATIVE_GOLD_STATUSES = {"CONFIRMED", "AUTHORITATIVE"}
PROVISIONAL_FIXTURES = {
    "SL:writtentest": (REPO_DIR / "data/gold/sl_ssj-ud-test.conllu").resolve(),
    "SL:spokentest": (REPO_DIR / "data/gold/sl_sst-ud-test.conllu").resolve(),
}
METRICS = [
    "Tokens",
    "Sentences",
    "Words",
    "UPOS",
    "XPOS",
    "UFeats",
    "AllTags",
    "Lemmas",
    "UAS",
    "LAS",
    "CLAS",
    "MLAS",
    "BLEX",
]
SCORE_FIELDS = ["precision", "recall", "f1", "aligned_accuracy"]

PROVISIONAL_SCOPE = "PROVISIONAL ENGINEERING SMOKE TEST"
PROVISIONAL_GOLD_NOTICE = "GOLD PROVENANCE NOT YET CONFIRMED"
PROVISIONAL_USE_NOTICE = "DO NOT TREAT AS BENCHMARK RESULT"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate manifest-selected predictions with strict gold-status gates."
    )
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        "--dry-run", action="store_true", help="Print the plan without evaluating."
    )
    action.add_argument(
        "--execute", action="store_true", help="Run permitted evaluations."
    )
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Permit only the two configured provisional SL engineering fixtures.",
    )
    parser.add_argument(
        "--initial-debugging-only",
        action="store_true",
        help="Select only rows marked for initial debugging in the mapping.",
    )
    parser.add_argument("--language", action="append", help="Filter by language.")
    parser.add_argument("--model", action="append", help="Filter by model/system.")
    parser.add_argument(
        "--training-condition", action="append", help="Filter by training condition."
    )
    parser.add_argument(
        "--test-condition", action="append", help="Filter by test condition."
    )
    parser.add_argument(
        "--repeat-check",
        action="store_true",
        help="Evaluate each run twice and require identical numeric output.",
    )
    parser.add_argument(
        "--output",
        help=(
            "TSV output path under am_benchmark/reports/. Smoke-test output "
            "must be under reports/smoke_test/."
        ),
    )
    return parser.parse_args()


def load_mapping() -> list[dict[str, str]]:
    with MAPPING_PATH.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source, delimiter="\t"))


def selected_by_filters(row: dict[str, str], args: argparse.Namespace) -> bool:
    if not row["selected_prediction"]:
        return False
    if args.initial_debugging_only and row["initial_debugging"] != "true":
        return False
    filters = {
        "language": args.language,
        "model": args.model,
        "training_condition": args.training_condition,
        "test_condition": args.test_condition,
    }
    return all(not allowed or row[field] in allowed for field, allowed in filters.items())


def resolve_manifest_path(value: str) -> Path:
    return (BENCHMARK_DIR / value).resolve()


def permission_reason(row: dict[str, str], smoke_test: bool) -> tuple[bool, str]:
    gold_status = row["gold_status"].strip().upper()
    gold_path = resolve_manifest_path(row["gold_file"]) if row["gold_file"] else None

    if gold_status in AUTHORITATIVE_GOLD_STATUSES:
        return True, "authoritative gold status"

    if smoke_test:
        expected = PROVISIONAL_FIXTURES.get(row["gold_cohort"])
        if expected is not None and gold_path == expected:
            return True, "explicitly permitted provisional SL engineering fixture"
        return False, "not one of the two configured provisional SL fixtures"

    return False, f"gold status is {row['gold_status'] or 'missing'}"


def load_evaluator():
    spec = importlib.util.spec_from_file_location("aaron_existing_ud_eval", EVALUATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load evaluator: {EVALUATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate_once(evaluator, gold_path: Path, prediction_path: Path) -> dict[str, float | None]:
    evaluation = evaluator.evaluate(
        evaluator.load_conllu_file(str(gold_path)),
        evaluator.load_conllu_file(str(prediction_path)),
    )
    scores: dict[str, float | None] = {}
    for metric in METRICS:
        score = evaluation[metric]
        for field in SCORE_FIELDS:
            value = getattr(score, field)
            scores[f"{metric}_{field}"] = None if value is None else 100.0 * value
    return scores


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_DIR))
    except ValueError:
        return str(path)


def output_path(args: argparse.Namespace) -> Path:
    if args.output:
        path = Path(args.output)
        if not path.is_absolute():
            path = BENCHMARK_DIR / path
    elif args.smoke_test:
        path = REPORT_DIR / "smoke_test/sl_spacy_stanza_results.tsv"
    else:
        path = REPORT_DIR / "evaluation_results.tsv"

    path = path.resolve()
    allowed_root = (REPORT_DIR / "smoke_test").resolve() if args.smoke_test else REPORT_DIR.resolve()
    if path != allowed_root and allowed_root not in path.parents:
        raise ValueError(f"Output must stay under {allowed_root}")
    return path


def result_fieldnames() -> list[str]:
    identifiers = [
        "result_scope",
        "gold_provenance_notice",
        "benchmark_use_notice",
        "language",
        "model",
        "training_condition",
        "test_condition",
        "gold_cohort",
        "gold_file",
        "prediction_file",
        "gold_status",
        "result_status",
        "repeat_deterministic",
        "evaluator_file",
        "evaluator_sha256",
        "gold_sha256",
        "prediction_sha256",
        "error_message",
    ]
    metrics = [f"{metric}_{field}" for metric in METRICS for field in SCORE_FIELDS]
    return identifiers + metrics


def tsv_text(rows: list[dict[str, object]]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output,
        fieldnames=result_fieldnames(),
        delimiter="\t",
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def main() -> int:
    args = parse_args()
    candidates = [row for row in load_mapping() if selected_by_filters(row, args)]
    permitted: list[dict[str, str]] = []
    blocked: list[tuple[dict[str, str], str]] = []
    for row in candidates:
        allowed, reason = permission_reason(row, args.smoke_test)
        (permitted if allowed else blocked).append(row if allowed else (row, reason))

    mode = "PROVISIONAL SMOKE TEST" if args.smoke_test else "AUTHORITATIVE"
    print(f"Mode: {mode}")
    print(f"Selected manifest rows: {len(candidates)}")
    print(f"Permitted: {len(permitted)}")
    print(f"Blocked/skipped: {len(blocked)}")
    for row in permitted:
        print(
            "EVALUATE "
            f"{row['language']} {row['model']} {row['training_condition']} "
            f"{row['test_condition']} -> {row['gold_cohort']}"
        )
    for row, reason in blocked:
        print(
            "SKIP "
            f"{row['language']} {row['model']} {row['training_condition']} "
            f"{row['test_condition']}: {reason}"
        )

    if args.dry_run:
        print("Dry run only; evaluator was not invoked.")
        return 0
    if not permitted:
        print("No permitted evaluations; no output written.", file=sys.stderr)
        return 2

    evaluator = load_evaluator()
    evaluator_hash = sha256(EVALUATOR_PATH)
    results: list[dict[str, object]] = []
    deterministic = True
    for row in permitted:
        gold_path = resolve_manifest_path(row["gold_file"])
        prediction_path = resolve_manifest_path(row["selected_prediction"])
        result: dict[str, object] = {
            "result_scope": PROVISIONAL_SCOPE if args.smoke_test else "BENCHMARK EVALUATION",
            "gold_provenance_notice": PROVISIONAL_GOLD_NOTICE if args.smoke_test else "AUTHORITATIVE GOLD CONFIRMED",
            "benchmark_use_notice": PROVISIONAL_USE_NOTICE if args.smoke_test else "",
            "language": row["language"],
            "model": row["model"],
            "training_condition": row["training_condition"],
            "test_condition": row["test_condition"],
            "gold_cohort": row["gold_cohort"],
            "gold_file": display_path(gold_path),
            "prediction_file": display_path(prediction_path),
            "gold_status": row["gold_status"],
            "result_status": "success",
            "repeat_deterministic": "not_checked",
            "evaluator_file": display_path(EVALUATOR_PATH),
            "evaluator_sha256": evaluator_hash,
            "gold_sha256": sha256(gold_path),
            "prediction_sha256": sha256(prediction_path),
            "error_message": "",
        }
        try:
            scores = evaluate_once(evaluator, gold_path, prediction_path)
            if args.repeat_check:
                repeated_scores = evaluate_once(evaluator, gold_path, prediction_path)
                same = scores == repeated_scores
                result["repeat_deterministic"] = str(same).lower()
                deterministic = deterministic and same
            result.update(scores)
        except Exception as exc:  # evaluator errors should remain visible in the TSV
            result["result_status"] = "error"
            result["error_message"] = f"{type(exc).__name__}: {exc}"
            deterministic = False
        results.append(result)

    destination = output_path(args)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(tsv_text(results), encoding="utf-8")
    successes = sum(row["result_status"] == "success" for row in results)
    print(f"Successful evaluations: {successes}/{len(results)}")
    if args.repeat_check:
        print(f"Repeated output deterministic: {'YES' if deterministic else 'NO'}")
    print(f"Wrote {display_path(destination)}")
    return 0 if successes == len(results) and deterministic else 1


if __name__ == "__main__":
    raise SystemExit(main())
