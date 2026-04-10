#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List


def sanitize_label(value: str) -> str:
    cleaned = value.strip().lower().replace("_", "-")
    cleaned = re.sub(r"[^a-z0-9-]+", "-", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return cleaned or "unknown"


def prediction_filename(run_stamp: str, dataset_tag: str, run_tag: str, model: str, mode: str) -> str:
    return f"{run_stamp}_{dataset_tag}_{run_tag}_{model}_{mode}_predicted.conllu"


@dataclass
class PredictionCheck:
    path: Path
    exists: bool
    parse_ok: bool
    parse_error: str | None
    sentences: int
    tokens: int
    words: int
    blocks: int
    malformed_rows: int
    sent_id_present: int
    text_present: int
    first_sent_ids: List[str]
    unique_sent_id_count: int
    ends_with_blank_line: bool


def load_ud_loader(repo_root: Path) -> Callable[[str], object]:
    eval_path = repo_root / "evaluation" / "conll18_ud_eval_tag-based.py"
    spec = importlib.util.spec_from_file_location("ud_eval_tag_based", eval_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load evaluator module from {eval_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.load_conllu_file


def inspect_prediction(path: Path, load_ud: Callable[[str], object]) -> PredictionCheck:
    if not path.exists():
        return PredictionCheck(
            path=path,
            exists=False,
            parse_ok=False,
            parse_error="missing file",
            sentences=0,
            tokens=0,
            words=0,
            blocks=0,
            malformed_rows=0,
            sent_id_present=0,
            text_present=0,
            first_sent_ids=[],
            unique_sent_id_count=0,
            ends_with_blank_line=False,
        )

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    blocks = [block for block in text.strip().split("\n\n") if block.strip()]

    malformed_rows = 0
    sent_id_present = 0
    text_present = 0
    all_sent_ids: List[str] = []

    for block in blocks:
        block_lines = block.splitlines()
        has_sent_id = False
        has_text = False
        for line in block_lines:
            if line.startswith("# sent_id = "):
                has_sent_id = True
                all_sent_ids.append(line.split("=", 1)[1].strip())
            elif line.startswith("# text = "):
                has_text = True

            if not line.strip() or line.startswith("#"):
                continue
            if len(line.split("\t")) != 10:
                malformed_rows += 1

        sent_id_present += int(has_sent_id)
        text_present += int(has_text)

    first_sent_ids = all_sent_ids[:5]
    unique_sent_id_count = len(set(all_sent_ids))
    ends_with_blank_line = text.endswith("\n\n")

    parse_ok = True
    parse_error = None
    sentences = 0
    tokens = 0
    words = 0
    try:
        ud = load_ud(str(path))
        sentences = len(getattr(ud, "sentences", []))
        tokens = len(getattr(ud, "tokens", []))
        words = len(getattr(ud, "words", []))
    except Exception as exc:  # noqa: BLE001
        parse_ok = False
        parse_error = str(exc)

    return PredictionCheck(
        path=path,
        exists=True,
        parse_ok=parse_ok,
        parse_error=parse_error,
        sentences=sentences,
        tokens=tokens,
        words=words,
        blocks=len(blocks),
        malformed_rows=malformed_rows,
        sent_id_present=sent_id_present,
        text_present=text_present,
        first_sent_ids=first_sent_ids,
        unique_sent_id_count=unique_sent_id_count,
        ends_with_blank_line=ends_with_blank_line,
    )


def parse_eval_metrics(path: Path) -> Dict[str, float]:
    metrics: Dict[str, float] = {}
    if not path.exists():
        return metrics

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


def parse_comparison_counts(path: Path) -> Dict[str, str]:
    out: Dict[str, str] = {}
    if not path.exists():
        return out

    patterns = {
        "las_a_only": re.compile(r"^- .*correct, .*wrong: .*"),
        "las_b_only": re.compile(r"^- .*correct, .*wrong: .*"),
        "both_correct": re.compile(r"^- Both correct: .*"),
        "both_wrong": re.compile(r"^- Both wrong: .*"),
    }

    in_las_section = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() == "## LAS exact differences":
            in_las_section = True
            continue
        if in_las_section and line.startswith("## "):
            break
        if not in_las_section:
            continue

        if patterns["las_a_only"].match(line) and "a_only" not in out:
            out["a_only"] = line[2:]
        elif patterns["las_b_only"].match(line) and "a_only" in out and "b_only" not in out:
            out["b_only"] = line[2:]
        elif patterns["both_correct"].match(line):
            out["both_correct"] = line[2:]
        elif patterns["both_wrong"].match(line):
            out["both_wrong"] = line[2:]

    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate one pipeline run and write a QA markdown report.")
    parser.add_argument("--run-stamp", required=True, help="Run stamp, e.g. 20260409-2248")
    parser.add_argument("--gold", default="data/gold/sl_ssj-ud-test.conllu", help="Gold CoNLL-U path")
    parser.add_argument("--run-label", default="full", help="Run label used by pipeline (default: full)")
    parser.add_argument("--pred-root", default="predictions/runs", help="Predictions root")
    parser.add_argument("--results-root", default="results/runs", help="Results root")
    parser.add_argument(
        "--output",
        default=None,
        help="Output markdown path (default: results/runs/<run>/main/qa_validation.md)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]

    gold_path = Path(args.gold)
    dataset_tag = sanitize_label(gold_path.stem)
    run_tag = sanitize_label(args.run_label)
    run_stamp = sanitize_label(args.run_stamp)

    run_id = f"{run_stamp}_{dataset_tag}_{run_tag}"
    pred_root = Path(args.pred_root)
    results_root = Path(args.results_root)
    run_results_root = results_root / run_id
    main_results_root = run_results_root / "main"
    diagnostics_root = run_results_root / "diagnostics"

    output_path = Path(args.output) if args.output else (main_results_root / "qa_validation.md")

    load_ud = load_ud_loader(repo_root)

    checks: Dict[str, PredictionCheck] = {}
    for model in ("classla", "trankit"):
        for mode in ("aligned", "base"):
            key = f"{model}_{mode}"
            pred_path = pred_root / prediction_filename(run_stamp, dataset_tag, run_tag, model, mode)
            checks[key] = inspect_prediction(pred_path, load_ud)

    expected_main = [
        main_results_root / "classla_aligned_eval.txt",
        main_results_root / "trankit_aligned_eval.txt",
        main_results_root / "classla_base_eval.txt",
        main_results_root / "trankit_base_eval.txt",
        main_results_root / "classla-vs-trankit_aligned_comparison.md",
        main_results_root / "classla-vs-trankit_base_comparison.md",
    ]

    expected_diagnostics = []
    for model in ("classla", "trankit"):
        for mode in ("aligned", "base"):
            expected_diagnostics.append(diagnostics_root / f"{model}_{mode}_eval-tagged.txt")
            expected_diagnostics.append(diagnostics_root / f"{model}_{mode}_errors.md")

    missing_results = [p for p in (expected_main + expected_diagnostics) if not p.exists()]

    traceback_files = []
    for p in expected_main + expected_diagnostics:
        if not p.exists():
            continue
        first_line = p.read_text(encoding="utf-8").splitlines()[:1]
        if first_line and first_line[0].startswith("Traceback"):
            traceback_files.append(p)

    eval_metrics = {
        "classla_aligned": parse_eval_metrics(main_results_root / "classla_aligned_eval.txt"),
        "trankit_aligned": parse_eval_metrics(main_results_root / "trankit_aligned_eval.txt"),
        "classla_base": parse_eval_metrics(main_results_root / "classla_base_eval.txt"),
        "trankit_base": parse_eval_metrics(main_results_root / "trankit_base_eval.txt"),
    }

    comparison_counts = {
        "aligned": parse_comparison_counts(main_results_root / "classla-vs-trankit_aligned_comparison.md"),
        "base": parse_comparison_counts(main_results_root / "classla-vs-trankit_base_comparison.md"),
    }

    failures: List[str] = []
    warnings: List[str] = []

    for key, chk in checks.items():
        if not chk.exists:
            failures.append(f"Missing prediction file: {chk.path}")
            continue
        if chk.malformed_rows > 0:
            failures.append(f"Malformed rows found in {chk.path}: {chk.malformed_rows}")
        if not chk.parse_ok:
            failures.append(f"Evaluator parser failed for {chk.path}: {chk.parse_error}")
        if not chk.ends_with_blank_line:
            failures.append(f"CoNLL-U file does not end with blank line: {chk.path}")

        if chk.sent_id_present < chk.blocks:
            warnings.append(f"Missing # sent_id in {chk.path.name}: {chk.blocks - chk.sent_id_present} sentence blocks")
        if chk.text_present < chk.blocks:
            warnings.append(f"Missing # text in {chk.path.name}: {chk.blocks - chk.text_present} sentence blocks")
        if chk.sent_id_present > 0 and chk.unique_sent_id_count <= max(1, chk.blocks // 10):
            warnings.append(
                f"Low sent_id uniqueness in {chk.path.name}: {chk.unique_sent_id_count} unique IDs for {chk.blocks} blocks"
            )

    if missing_results:
        failures.extend([f"Missing result file: {p}" for p in missing_results])
    if traceback_files:
        failures.extend([f"Result file starts with traceback: {p}" for p in traceback_files])

    status = "PASS" if not failures else "FAIL"

    lines: List[str] = []
    lines.append(f"# QA Validation Report: {run_id}")
    lines.append("")
    lines.append(f"- Status: **{status}**")
    lines.append(f"- Gold file: {gold_path}")
    lines.append(f"- Predictions root: {pred_root}")
    lines.append(f"- Results root: {run_results_root}")
    lines.append("")

    lines.append("## Prediction File Checks")
    for key in sorted(checks.keys()):
        chk = checks[key]
        lines.append(f"### {key}")
        lines.append(f"- Path: {chk.path}")
        lines.append(f"- Exists: {chk.exists}")
        lines.append(f"- Evaluator parse OK: {chk.parse_ok}")
        if chk.parse_error:
            lines.append(f"- Parse error: {chk.parse_error}")
        lines.append(f"- Sentences (evaluator): {chk.sentences}")
        lines.append(f"- Tokens (evaluator): {chk.tokens}")
        lines.append(f"- Words (evaluator): {chk.words}")
        lines.append(f"- Sentence blocks (raw split): {chk.blocks}")
        lines.append(f"- Malformed token rows: {chk.malformed_rows}")
        lines.append(f"- # sent_id present: {chk.sent_id_present}/{chk.blocks}")
        lines.append(f"- # text present: {chk.text_present}/{chk.blocks}")
        lines.append(f"- Unique sent_id count: {chk.unique_sent_id_count}")
        lines.append(f"- First sent_id values: {chk.first_sent_ids}")
        lines.append(f"- Ends with blank line: {chk.ends_with_blank_line}")
        lines.append("")

    lines.append("## Result File Checks")
    lines.append(f"- Expected main files: {len(expected_main)}")
    lines.append(f"- Expected diagnostics files: {len(expected_diagnostics)}")
    lines.append(f"- Missing result files: {len(missing_results)}")
    lines.append(f"- Traceback-leading result files: {len(traceback_files)}")
    lines.append("")

    lines.append("## Core Metrics (F1 from eval summaries)")
    for key in ("classla_aligned", "trankit_aligned", "classla_base", "trankit_base"):
        metric_map = eval_metrics[key]
        lines.append(f"### {key}")
        for metric in ("LAS", "UAS", "UPOS", "XPOS", "Lemmas", "MLAS"):
            value = metric_map.get(metric)
            if value is not None:
                lines.append(f"- {metric}: {value:.2f}")
        lines.append("")

    lines.append("## Model-vs-Model LAS Difference Snapshot")
    for mode in ("aligned", "base"):
        lines.append(f"### {mode}")
        snap = comparison_counts[mode]
        if not snap:
            lines.append("- Could not parse LAS section from comparison report")
        else:
            for label in ("a_only", "b_only", "both_correct", "both_wrong"):
                if label in snap:
                    lines.append(f"- {snap[label]}")
        lines.append("")

    lines.append("## Failures")
    if failures:
        for item in failures:
            lines.append(f"- {item}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Warnings")
    if warnings:
        for item in warnings:
            lines.append(f"- {item}")
    else:
        lines.append("- None")
    lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote QA validation report to {output_path}")
    print(f"Status: {status}")


if __name__ == "__main__":
    main()
