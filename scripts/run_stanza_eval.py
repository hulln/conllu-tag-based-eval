#!/usr/bin/env python3
"""Aligned evaluation of Stanza on the website test sets, with pinned model artifacts.

Produces, for each test set, the same files as a run_pipeline.py run for one system:

  predictions/output/<run_id>_stanza_aligned_predicted.conllu
  results/output/<run_id>/main/stanza_aligned_eval.txt
  results/output/<run_id>/diagnostics/stanza_aligned_eval-tagged.txt
  results/output/<run_id>/diagnostics/stanza_aligned_errors.md
  results/output/<run_id>/main/qa_validation.md

where run_id = <run_stamp>_<dataset_tag>_full. Evaluation reuses run_pipeline.eval_and_analyze
(the same evaluator calls as for Trankit and CLASSLA); run_pipeline.py and qa_validate_run.py are
hash-pinned by references/canonical_run_manifest.json and are imported, not modified.

Run inside the Stanza 1.14 container (docker-compose.stanza114-eval.yml). Configuration, model
pins and gold hashes come from references/stanza-1.14.0-default_accurate.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from qa_validate_run import parse_eval_metrics  # noqa: E402
from qa_validate_system_run import check_trees  # noqa: E402
from run_pipeline import eval_and_analyze, prediction_output_path, run, sanitize_label  # noqa: E402

RUN_LABEL = "full"
MODE = "aligned"
STAMP_TAG = "stanza114acc"
KEY_SCRIPTS = (
    "scripts/run_stanza_eval.py", "scripts/predict_stanza.py", "scripts/verify_stanza_artifacts.py",
    "scripts/qa_validate_system_run.py", "scripts/qa_validate_run.py", "scripts/run_pipeline.py",
    "scripts/conll18_ud_eval_tag-based.py", "scripts/analyze_errors.py",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def git_state(paths) -> dict:
    """HEAD plus any uncommitted (modified or untracked) state of the files this run depends on."""
    try:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True, text=True, check=True)
        status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", *paths],
                                cwd=REPO_ROOT, capture_output=True, text=True, check=True)
        return {"commit": head.stdout.strip(), "uncommitted": status.stdout.splitlines()}
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None, "note": "git not available in this environment; record the commit from the host"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aligned Stanza evaluation on the website test sets.")
    parser.add_argument("--config", default="references/stanza-1.14.0-default_accurate.json")
    parser.add_argument("--run-stamp", default=None,
                        help=f"Run stamp (default: <YYYYMMDD-HHMM>-{STAMP_TAG}). Must be new.")
    parser.add_argument("--datasets", default="ssj,sst,pog", help="Comma-separated test-set keys from the config.")
    parser.add_argument("--pred-root", default="predictions/output")
    parser.add_argument("--results-root", default="results/output")
    parser.add_argument("--top-n", type=int, default=20, help="Top N rows for confusion tables (as run_pipeline.py).")
    parser.add_argument("--preflight-only", action="store_true",
                        help="Check gold hashes, output paths, environment and model artifacts, then stop.")
    parser.add_argument("--skip-prediction", action="store_true",
                        help="Evaluate existing prediction files of this run stamp (no model is loaded).")
    parser.add_argument("--allow-cpu", action="store_true", help="Do not require CUDA (August ran on GPU).")
    parser.add_argument("--no-august-check", action="store_true",
                        help="Do not compare SSJ/SST outputs with the August reference hashes.")
    return parser.parse_args()


def main() -> int:
    sys.stdout.reconfigure(line_buffering=True)  # keep our lines in order with subprocess output
    args = parse_args()
    config_path = (REPO_ROOT / args.config).resolve()
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    system = cfg["system"]["key"]
    package = cfg["system"]["package"]
    stamp = sanitize_label(args.run_stamp or f"{datetime.now().strftime('%Y%m%d-%H%M')}-{STAMP_TAG}")
    pred_root = (REPO_ROOT / args.pred_root).resolve()
    results_root = (REPO_ROOT / args.results_root).resolve()
    python_bin = sys.executable

    by_key = {t["key"]: t for t in cfg["test_sets"]}
    keys = [k.strip() for k in args.datasets.split(",") if k.strip()]
    unknown = [k for k in keys if k not in by_key]
    if unknown:
        raise SystemExit(f"Unknown test-set keys {unknown}; config has {sorted(by_key)}")

    plan = []
    problems = []
    for key in keys:
        t = by_key[key]
        gold = REPO_ROOT / t["gold"]
        dataset_tag = sanitize_label(gold.stem)
        run_id = f"{stamp}_{dataset_tag}_{sanitize_label(RUN_LABEL)}"
        pred = prediction_output_path(pred_root, stamp, dataset_tag, sanitize_label(RUN_LABEL), system, MODE)
        res = results_root / run_id
        item = {"key": key, "gold": gold, "run_id": run_id, "pred": pred, "main": res / "main",
                "diag": res / "diagnostics", "expected_gold_sha256": t["sha256"]}
        plan.append(item)
        if not gold.is_file():
            problems.append(f"{key}: gold file missing: {rel(gold)}")
        elif sha256_file(gold) != t["sha256"]:
            problems.append(f"{key}: gold SHA-256 differs from pinned value: {rel(gold)}")
        if args.skip_prediction:
            if not pred.is_file():
                problems.append(f"{key}: --skip-prediction but prediction missing: {rel(pred)}")
        elif pred.exists():
            problems.append(f"{key}: prediction already exists (refusing to overwrite): {rel(pred)}")
        if res.exists() and any(res.rglob("*")):
            problems.append(f"{key}: results directory already exists and is not empty: {rel(res)}")

    print(f"Run stamp: {stamp}")
    for item in plan:
        print(f"  {item['key']}: {rel(item['gold'])} -> {rel(item['pred'])}")

    needs_model = not args.skip_prediction
    if needs_model:
        for var, want in (("HF_HUB_OFFLINE", "1"), ("TRANSFORMERS_OFFLINE", "1")):
            if os.environ.get(var) != want:
                problems.append(f"environment: {var} must be {want} so nothing is downloaded during prediction")
        for var in ("STANZA_RESOURCES_DIR", "HF_HOME"):
            if not os.environ.get(var):
                problems.append(f"environment: {var} is not set")
        try:
            import torch  # noqa: F401
            if not args.allow_cpu and not torch.cuda.is_available():
                problems.append("environment: CUDA is not available (use --allow-cpu only deliberately)")
        except ImportError:
            problems.append("environment: torch is not importable (run inside the Stanza container)")

    if problems:
        print("\nPreflight problems:")
        for p in problems:
            print(f"  - {p}")
        return 1

    verification_report = None
    if needs_model:
        tmp_report = results_root / f".{stamp}_artifact_verification.json"
        rc = subprocess.run([python_bin, str(SCRIPTS / "verify_stanza_artifacts.py"), "--pins", str(config_path),
                             "--report", str(tmp_report)], cwd=REPO_ROOT).returncode
        if tmp_report.is_file():
            verification_report = json.loads(tmp_report.read_text(encoding="utf-8"))
            tmp_report.unlink()
        if rc != 0 or verification_report is None:
            print("Model artifact verification failed; nothing was predicted.")
            return 1
    print("Preflight: OK")
    if args.preflight_only:
        return 0

    failures = []
    summary = []
    for item in plan:
        key, gold, pred = item["key"], item["gold"], item["pred"]
        item["main"].mkdir(parents=True, exist_ok=True)
        item["diag"].mkdir(parents=True, exist_ok=True)
        provenance = item["main"] / f"{system}_prediction_provenance.json"
        commands = {}
        if needs_model:
            cmd = [python_bin, "scripts/predict_stanza.py", "--gold", rel(gold), "--package", package,
                   "--output", rel(pred), "--provenance-out", rel(provenance)]
            if not args.allow_cpu:
                cmd.append("--require-gpu")
            commands["prediction"] = " ".join(cmd)
            run(cmd, cwd=REPO_ROOT)
            (item["main"] / f"{system}_artifact_verification.json").write_text(
                json.dumps(verification_report, indent=1) + "\n", encoding="utf-8")

        trees = check_trees(pred, gold)
        if trees["counts"]["blocking_problems"]:
            failures.append(f"{key}: structural problems in prediction, evaluation not run")
            (item["main"] / "qa_tree_checks.json").write_text(json.dumps(trees, indent=1) + "\n", encoding="utf-8")
            print(f"\n{key}: prediction is not a set of well-formed, gold-aligned trees: {trees['counts']}")
            print("No automatic correction is applied. The raw file is kept for review; compare the documented "
                  "rule used for Trankit in results/output/20260622-0810-tk13_sl-sst-ud-test-pog_full/NORMALIZATION_NOTE.md.")
            continue

        summary_out = item["main"] / f"{system}_{MODE}_eval.txt"
        tagged_out = item["diag"] / f"{system}_{MODE}_eval-tagged.txt"
        errors_out = item["diag"] / f"{system}_{MODE}_errors.md"
        eval_and_analyze(REPO_ROOT, python_bin, Path(rel(gold)), Path(rel(pred)), summary_out, tagged_out,
                         errors_out, f"Stanza {MODE}", args.top_n)

        qa_cmd = [python_bin, "scripts/qa_validate_system_run.py", "--system", system, "--run-stamp", stamp,
                  "--gold", rel(gold), "--run-label", RUN_LABEL, "--pred-root", rel(pred_root),
                  "--results-root", rel(results_root)]
        qa_status = "PASS"
        try:
            run(qa_cmd, cwd=REPO_ROOT)
        except subprocess.CalledProcessError:
            qa_status = "FAIL"
            failures.append(f"{key}: QA validation failed")

        august = None
        ref = (cfg.get("august_reference") or {}).get(key)
        if ref and not args.no_august_check:
            august = {
                "reference_prediction": ref["prediction"],
                "prediction_identical": sha256_file(pred) == ref["prediction_sha256"],
                "reference_eval": ref["eval"],
                "eval_identical": sha256_file(summary_out) == ref["eval_sha256"],
            }
            if not (august["prediction_identical"] and august["eval_identical"]):
                failures.append(f"{key}: output differs from the August reference run")

        files = [pred, summary_out, tagged_out, errors_out, item["main"] / "qa_validation.md"]
        manifest = {
            "schema_version": 1,
            "run_id": item["run_id"],
            "run_stamp": stamp,
            "dataset_tag": sanitize_label(gold.stem),
            "run_label": RUN_LABEL,
            "mode": MODE,
            "system": cfg["system"],
            "source": git_state([*KEY_SCRIPTS, rel(config_path), "docker/Dockerfile.stanza",
                                 "docker-compose.stanza114-eval.yml"]),
            "config": {"path": rel(config_path), "sha256": sha256_file(config_path)},
            "dataset": {"gold_file": rel(gold), "sha256": sha256_file(gold)},
            "commands": {"runner": " ".join([rel(Path(sys.argv[0]))] + sys.argv[1:]), **commands,
                         "qa": " ".join(qa_cmd)},
            "prediction_provenance": rel(provenance) if provenance.exists() else None,
            "artifact_verification": (verification_report or {}).get("status"),
            "august_reference_check": august,
            "qa_status": qa_status,
            "metrics": {k: v for k, v in parse_eval_metrics(summary_out).items()
                        if k in ("LAS", "UAS", "UPOS", "XPOS", "UFeats", "Lemmas", "MLAS", "BLEX")},
            "file_hashes": {rel(p): sha256_file(p) for p in files if p.exists()},
            "script_hashes": {s: sha256_file(REPO_ROOT / s) for s in KEY_SCRIPTS},
        }
        (item["main"] / "run_manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n",
                                                        encoding="utf-8")
        summary.append((key, manifest["metrics"], qa_status, august))

    print("\nSummary")
    for key, m, qa_status, august in summary:
        metrics = " ".join(f"{k}={m[k]:.2f}" for k in ("LAS", "UAS", "UPOS", "XPOS", "Lemmas") if k in m)
        same = "n/a" if august is None else ("identical" if august["prediction_identical"] and august["eval_identical"] else "DIFFERS")
        print(f"  {key:4s} QA={qa_status} August={same} {metrics}")
    if failures:
        print("\nFailures:")
        for f in failures:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
