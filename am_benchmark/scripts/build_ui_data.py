#!/usr/bin/env python3
"""Build the local benchmark UI data bundle from evaluation-result TSV rows."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


BENCHMARK_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = BENCHMARK_DIR.parent
INTERFACE_DIR = REPO_DIR / "tables/am_benchmark"
DEFAULT_INPUT = BENCHMARK_DIR / "reports/authoritative_spacy_stanza_results.tsv"
DEFAULT_OUTPUT = INTERFACE_DIR / "data/results.js"

# The bundle is written into the benchmark's own interface directory and nowhere
# else. The containment rule is what keeps a mistyped --output away from the
# production tables, results and predictions trees; widening it to exactly these
# two roots is the whole of the permission this script has.
ALLOWED_OUTPUT_ROOTS = (INTERFACE_DIR, BENCHMARK_DIR)

REQUIRED_FIELDS = [
    "language",
    "model",
    "training_condition",
    "test_condition",
    "gold_cohort",
    "gold_status",
    "result_status",
    "prediction_file",
]
METRIC_FIELDS = [
    "precision",
    "recall",
    "f1",
    "aligned_accuracy",
    "correct",
    "gold",
    "predicted",
    "aligned",
]
DIMENSION_FIELDS = ["language", "model", "training_condition", "test_condition"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert benchmark evaluation TSV rows to a compact UI JavaScript bundle."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def contained_output_path(path: Path) -> Path:
    if not path.is_absolute():
        path = REPO_DIR / path
    resolved = path.resolve()
    roots = [root.resolve() for root in ALLOWED_OUTPUT_ROOTS]
    if not any(root in resolved.parents for root in roots):
        allowed = " or ".join(str(root) for root in roots)
        raise ValueError(f"Output must stay under {allowed}")
    return resolved


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def discover_metrics(fieldnames: list[str]) -> tuple[list[str], dict[str, list[str]]]:
    metrics: list[str] = []
    fields_by_metric: dict[str, list[str]] = {}
    for column in fieldnames:
        for field in sorted(METRIC_FIELDS, key=len, reverse=True):
            suffix = f"_{field}"
            if not column.endswith(suffix):
                continue
            metric = column[: -len(suffix)]
            if metric not in fields_by_metric:
                metrics.append(metric)
                fields_by_metric[metric] = []
            fields_by_metric[metric].append(field)
            break
    return metrics, fields_by_metric


def numeric_or_none(value: str) -> int | float | None:
    if value == "":
        return None
    number = float(value)
    return int(number) if number.is_integer() else number


def ordered_values(rows: list[dict[str, str]], field: str) -> list[str]:
    values = {row[field] for row in rows}
    preferred = {
        "language": ["EN", "NL", "SL"],
        "training_condition": [
            "default",
            "writtentrain",
            "writtenandspokentrain",
            "writtenanddialecttrain",
        ],
        "test_condition": ["writtentest", "spokentest", "dialecttest"],
    }.get(field, [])
    return [value for value in preferred if value in values] + sorted(
        values.difference(preferred)
    )


def build_payload(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source, delimiter="\t")
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    missing = [field for field in REQUIRED_FIELDS if field not in fieldnames]
    if missing:
        raise ValueError("Missing required TSV columns: " + ", ".join(missing))
    if not rows:
        raise ValueError(f"No result rows found in {path}")

    metrics, fields_by_metric = discover_metrics(fieldnames)
    if not metrics:
        raise ValueError("No evaluator metric columns found")

    seen_keys: set[tuple[str, ...]] = set()
    output_rows = []
    metric_columns = {
        f"{metric}_{field}"
        for metric in metrics
        for field in fields_by_metric[metric]
    }
    for row in rows:
        key = tuple(row[field] for field in DIMENSION_FIELDS)
        if key in seen_keys:
            raise ValueError(f"Duplicate logical result key: {key}")
        seen_keys.add(key)

        output = {
            field: value
            for field, value in row.items()
            if field not in metric_columns
        }
        output["metrics"] = {
            metric: {
                field: numeric_or_none(row[f"{metric}_{field}"])
                for field in fields_by_metric[metric]
            }
            for metric in metrics
        }
        output_rows.append(output)

    return {
        "schema_version": 1,
        "source": {
            "path": str(path.resolve().relative_to(BENCHMARK_DIR)),
            "sha256": sha256(path),
            "row_count": len(rows),
        },
        "dimensions": {
            field: ordered_values(rows, field) for field in DIMENSION_FIELDS
        },
        "metrics": [
            {"name": metric, "fields": fields_by_metric[metric]}
            for metric in metrics
        ],
        "rows": output_rows,
    }


def main() -> int:
    args = parse_args()
    input_path = args.input.resolve()
    output_path = contained_output_path(args.output)
    payload = build_payload(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "window.AM_BENCHMARK_RESULTS = "
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    try:
        shown = output_path.relative_to(REPO_DIR)
    except ValueError:
        shown = output_path
    print(
        f"Wrote {shown} "
        f"({payload['source']['row_count']} rows, {len(payload['metrics'])} metrics)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
