#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Dict


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def parse_eval_metrics(path: Path) -> Dict[str, float]:
    metrics: Dict[str, float] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "|" not in line or line.startswith("Metric") or line.startswith("-"):
            continue

        parts = [part.strip() for part in line.split("|")]
        if len(parts) < 4:
            continue

        metric = parts[0]
        try:
            f1 = float(parts[3])
        except ValueError:
            continue

        metrics[metric] = f1

    return metrics


def render_template(path_template: str, run_stamp: str) -> str:
    try:
        return path_template.format(run_stamp=run_stamp)
    except KeyError as exc:
        raise ValueError(f"Unsupported placeholder in manifest path template: {path_template}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a rerun against the canonical aligned manifest (hashes + core metrics)."
    )
    parser.add_argument(
        "--manifest",
        default="references/canonical_run_manifest.json",
        help="Path to canonical manifest JSON.",
    )
    parser.add_argument(
        "--run-stamp",
        default=None,
        help="Run stamp to verify. Defaults to manifest run_stamp.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = repo_root / manifest_path

    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest file not found: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    run_stamp = args.run_stamp or manifest.get("run_stamp")
    if not run_stamp:
        raise ValueError("Run stamp is missing. Pass --run-stamp or define run_stamp in manifest.")

    tolerance = float(manifest.get("metric_tolerance", 0.0))
    failures: list[str] = []

    print(f"Manifest: {manifest_path}")
    print(f"Canonical run id: {manifest.get('canonical_run_id', '<unknown>')}")
    print(f"Run stamp under verification: {run_stamp}")
    print("")

    file_hashes: Dict[str, str] = manifest.get("file_hashes", {})
    print("[1/2] Verifying file hashes")
    for template, expected_hash in file_hashes.items():
        rel_path = render_template(template, run_stamp)
        path = repo_root / rel_path

        if not path.exists():
            failures.append(f"Missing file: {rel_path}")
            print(f"  [FAIL] {rel_path} (missing)")
            continue

        actual_hash = sha256_file(path)
        if actual_hash != expected_hash:
            failures.append(
                f"Hash mismatch: {rel_path} (expected {expected_hash}, got {actual_hash})"
            )
            print(f"  [FAIL] {rel_path}")
            continue

        print(f"  [OK]   {rel_path}")

    print("")
    print("[2/2] Verifying eval metrics")
    expected_metrics: Dict[str, Dict[str, float]] = manifest.get("expected_metrics", {})
    for template, metric_expectations in expected_metrics.items():
        rel_path = render_template(template, run_stamp)
        path = repo_root / rel_path

        if not path.exists():
            failures.append(f"Missing eval file: {rel_path}")
            print(f"  [FAIL] {rel_path} (missing)")
            continue

        observed = parse_eval_metrics(path)
        print(f"  [FILE] {rel_path}")
        for metric_name, expected_value in metric_expectations.items():
            actual_value = observed.get(metric_name)
            if actual_value is None:
                failures.append(f"Missing metric {metric_name} in {rel_path}")
                print(f"    [FAIL] {metric_name} missing")
                continue

            delta = abs(actual_value - float(expected_value))
            if delta > tolerance:
                failures.append(
                    f"Metric mismatch in {rel_path}: {metric_name} expected {expected_value:.2f}, got {actual_value:.2f}"
                )
                print(f"    [FAIL] {metric_name}: expected {expected_value:.2f}, got {actual_value:.2f}")
                continue

            print(f"    [OK]   {metric_name}: {actual_value:.2f}")

    print("")
    if failures:
        print("Verification FAILED")
        for item in failures:
            print(f"- {item}")
        raise SystemExit(1)

    print("Verification PASSED")


if __name__ == "__main__":
    main()
