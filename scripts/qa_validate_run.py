#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Sequence


def canonical_mode(mode: str) -> str:
    if mode in {"base", "raw", "unaligned"}:
        return "base"
    return "aligned"


def resolve_active_modes(mode_arg: str) -> List[str]:
    return ["aligned", "base"] if mode_arg == "both" else [canonical_mode(mode_arg)]


def sanitize_label(value: str) -> str:
    cleaned = value.strip().lower().replace("_", "-")
    cleaned = re.sub(r"[^a-z0-9-]+", "-", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return cleaned or "unknown"


def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (repo_root / path)


def display_path(repo_root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def prediction_filename(run_stamp: str, dataset_tag: str, run_tag: str, model: str, mode: str) -> str:
    return f"{run_stamp}_{dataset_tag}_{run_tag}_{model}_{mode}_predicted.conllu"


def prediction_output_path(
    pred_root: Path,
    run_stamp: str,
    dataset_tag: str,
    run_tag: str,
    model: str,
    mode: str,
) -> Path:
    filename = prediction_filename(run_stamp, dataset_tag, run_tag, model, mode)
    if mode == "base":
        return pred_root / "supplementary" / "base" / filename
    return pred_root / filename


def prediction_legacy_path(
    pred_root: Path,
    run_stamp: str,
    dataset_tag: str,
    run_tag: str,
    model: str,
    mode: str,
) -> Path:
    return pred_root / prediction_filename(run_stamp, dataset_tag, run_tag, model, mode)


def first_existing_path(paths: Sequence[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    return paths[0]


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
    sent_ids: List[str]
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
            sent_ids=[],
            unique_sent_id_count=0,
            ends_with_blank_line=False,
        )

    text = path.read_text(encoding="utf-8")
    blocks = [block for block in text.strip().split("\n\n") if block.strip()]

    malformed_rows = 0
    sent_id_present = 0
    text_present = 0
    sent_ids: List[str] = []

    for block in blocks:
        block_lines = block.splitlines()
        has_sent_id = False
        has_text = False
        for line in block_lines:
            if line.startswith("# sent_id = "):
                has_sent_id = True
                sent_ids.append(line.split("=", 1)[1].strip())
            elif line.startswith("# text = "):
                has_text = True

            if not line.strip() or line.startswith("#"):
                continue
            if len(line.split("\t")) != 10:
                malformed_rows += 1

        sent_id_present += int(has_sent_id)
        text_present += int(has_text)

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
        sent_ids=sent_ids,
        unique_sent_id_count=len(set(sent_ids)),
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

    labels = ["a_only", "b_only", "both_correct", "both_wrong"]
    in_las_section = False
    bullet_idx = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() == "## LAS exact differences":
            in_las_section = True
            continue
        if in_las_section and line.startswith("## "):
            break
        if not in_las_section or not line.startswith("- "):
            continue

        if bullet_idx < len(labels):
            out[labels[bullet_idx]] = line[2:]
        bullet_idx += 1

    return out


def first_list_mismatch(expected: Sequence[str], observed: Sequence[str]) -> str | None:
    max_len = max(len(expected), len(observed))
    for idx in range(max_len):
        exp = expected[idx] if idx < len(expected) else "<missing>"
        obs = observed[idx] if idx < len(observed) else "<missing>"
        if exp != obs:
            return f"position {idx + 1}: expected {exp!r}, observed {obs!r}"
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate one pipeline run and write a QA markdown report.")
    parser.add_argument("--run-stamp", required=True, help="Run stamp, e.g. 20260409-2248")
    parser.add_argument("--gold", default="data/gold/sl_ssj-ud-test.conllu", help="Gold CoNLL-U path")
    parser.add_argument("--run-label", default="full", help="Run label used by pipeline (default: full)")
    parser.add_argument("--pred-root", default="predictions/runs", help="Predictions root")
    parser.add_argument("--results-root", default="results/runs", help="Results root")
    parser.add_argument(
        "--modes",
        choices=["both", "aligned", "base", "raw", "unaligned"],
        default="aligned",
        help="Validate aligned only (default), both modes, or one specific mode.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional markdown output path. Default depends on the selected mode(s).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]

    active_modes = resolve_active_modes(args.modes)
    gold_path = resolve_path(repo_root, args.gold)
    dataset_tag = sanitize_label(gold_path.stem)
    run_tag = sanitize_label(args.run_label)
    run_stamp = sanitize_label(args.run_stamp)

    run_id = f"{run_stamp}_{dataset_tag}_{run_tag}"
    pred_root = resolve_path(repo_root, args.pred_root)
    results_root = resolve_path(repo_root, args.results_root)
    run_results_root = results_root / run_id
    main_results_root = run_results_root / "main"
    diagnostics_root = run_results_root / "diagnostics"
    supplementary_base_root = run_results_root / "supplementary" / "base"
    supplementary_base_main_root = supplementary_base_root / "main"
    supplementary_base_diagnostics_root = supplementary_base_root / "diagnostics"

    if args.output:
        output_path = resolve_path(repo_root, args.output)
    elif "aligned" in active_modes:
        output_path = main_results_root / "qa_validation.md"
    else:
        output_path = supplementary_base_main_root / "qa_validation.md"

    load_ud = load_ud_loader(repo_root)
    gold_check = inspect_prediction(gold_path, load_ud)
    if not gold_check.exists:
        raise FileNotFoundError(f"Gold file not found: {gold_path}")
    if not gold_check.parse_ok:
        raise RuntimeError(f"Gold file failed evaluator parse: {gold_path}: {gold_check.parse_error}")

    checks: Dict[str, PredictionCheck] = {}
    for mode in active_modes:
        for model in ("classla", "trankit"):
            key = f"{model}_{mode}"
            pred_path = first_existing_path(
                [
                    prediction_output_path(pred_root, run_stamp, dataset_tag, run_tag, model, mode),
                    prediction_legacy_path(pred_root, run_stamp, dataset_tag, run_tag, model, mode),
                ]
            )
            checks[key] = inspect_prediction(pred_path, load_ud)

    expected_main_groups: List[List[Path]] = []
    expected_diagnostics_groups: List[List[Path]] = []

    eval_paths: Dict[str, Path] = {}
    comparison_paths: Dict[str, Path] = {}

    if "aligned" in active_modes:
        eval_paths["classla_aligned"] = main_results_root / "classla_aligned_eval.txt"
        eval_paths["trankit_aligned"] = main_results_root / "trankit_aligned_eval.txt"
        comparison_paths["aligned"] = main_results_root / "classla-vs-trankit_aligned_comparison.md"

        expected_main_groups.extend(
            [
                [eval_paths["classla_aligned"]],
                [eval_paths["trankit_aligned"]],
                [comparison_paths["aligned"]],
            ]
        )
        expected_diagnostics_groups.extend(
            [
                [diagnostics_root / "classla_aligned_eval-tagged.txt"],
                [diagnostics_root / "classla_aligned_errors.md"],
                [diagnostics_root / "trankit_aligned_eval-tagged.txt"],
                [diagnostics_root / "trankit_aligned_errors.md"],
            ]
        )

    if "base" in active_modes:
        eval_paths["classla_base"] = first_existing_path(
            [supplementary_base_main_root / "classla_base_eval.txt", main_results_root / "classla_base_eval.txt"]
        )
        eval_paths["trankit_base"] = first_existing_path(
            [supplementary_base_main_root / "trankit_base_eval.txt", main_results_root / "trankit_base_eval.txt"]
        )
        comparison_paths["base"] = first_existing_path(
            [
                supplementary_base_main_root / "classla-vs-trankit_base_comparison.md",
                main_results_root / "classla-vs-trankit_base_comparison.md",
            ]
        )

        expected_main_groups.extend(
            [
                [supplementary_base_main_root / "classla_base_eval.txt", main_results_root / "classla_base_eval.txt"],
                [supplementary_base_main_root / "trankit_base_eval.txt", main_results_root / "trankit_base_eval.txt"],
                [
                    supplementary_base_main_root / "classla-vs-trankit_base_comparison.md",
                    main_results_root / "classla-vs-trankit_base_comparison.md",
                ],
            ]
        )
        expected_diagnostics_groups.extend(
            [
                [
                    supplementary_base_diagnostics_root / "classla_base_eval-tagged.txt",
                    diagnostics_root / "classla_base_eval-tagged.txt",
                ],
                [
                    supplementary_base_diagnostics_root / "classla_base_errors.md",
                    diagnostics_root / "classla_base_errors.md",
                ],
                [
                    supplementary_base_diagnostics_root / "trankit_base_eval-tagged.txt",
                    diagnostics_root / "trankit_base_eval-tagged.txt",
                ],
                [
                    supplementary_base_diagnostics_root / "trankit_base_errors.md",
                    diagnostics_root / "trankit_base_errors.md",
                ],
            ]
        )

    expected_main = [group[0] for group in expected_main_groups]
    expected_diagnostics = [group[0] for group in expected_diagnostics_groups]

    selected_result_paths: List[Path] = []
    missing_results: List[Path] = []
    for group in expected_main_groups + expected_diagnostics_groups:
        resolved = first_existing_path(group)
        if resolved.exists():
            selected_result_paths.append(resolved)
        else:
            missing_results.append(group[0])

    traceback_files = []
    for path in selected_result_paths:
        first_line = path.read_text(encoding="utf-8").splitlines()[:1]
        if first_line and first_line[0].startswith("Traceback"):
            traceback_files.append(path)

    eval_metrics = {key: parse_eval_metrics(path) for key, path in eval_paths.items()}
    comparison_counts = {mode: parse_comparison_counts(path) for mode, path in comparison_paths.items()}

    failures: List[str] = []
    warnings: List[str] = []

    for key, chk in checks.items():
        mode = key.rsplit("_", 1)[1]
        if not chk.exists:
            failures.append(f"Missing prediction file: {display_path(repo_root, chk.path)}")
            continue
        if chk.malformed_rows > 0:
            failures.append(f"Malformed rows found in {display_path(repo_root, chk.path)}: {chk.malformed_rows}")
        if not chk.parse_ok:
            failures.append(f"Evaluator parser failed for {display_path(repo_root, chk.path)}: {chk.parse_error}")
        if not chk.ends_with_blank_line:
            failures.append(f"CoNLL-U file does not end with blank line: {display_path(repo_root, chk.path)}")

        if mode == "aligned":
            if chk.sentences != gold_check.sentences:
                failures.append(
                    f"Aligned sentence count mismatch in {chk.path.name}: predicted={chk.sentences} gold={gold_check.sentences}"
                )
            if chk.tokens != gold_check.tokens:
                failures.append(
                    f"Aligned token count mismatch in {chk.path.name}: predicted={chk.tokens} gold={gold_check.tokens}"
                )
            if chk.words != gold_check.words:
                failures.append(
                    f"Aligned word count mismatch in {chk.path.name}: predicted={chk.words} gold={gold_check.words}"
                )
            if chk.blocks != gold_check.blocks:
                failures.append(
                    f"Aligned sentence-block mismatch in {chk.path.name}: predicted={chk.blocks} gold={gold_check.blocks}"
                )
            if chk.sent_id_present != chk.blocks:
                failures.append(f"Aligned prediction missing # sent_id lines: {chk.path.name} ({chk.sent_id_present}/{chk.blocks})")
            if chk.text_present != chk.blocks:
                failures.append(f"Aligned prediction missing # text lines: {chk.path.name} ({chk.text_present}/{chk.blocks})")
            if chk.unique_sent_id_count != chk.blocks:
                failures.append(
                    f"Aligned prediction has non-unique sent_id values: {chk.path.name} "
                    f"({chk.unique_sent_id_count}/{chk.blocks} unique)"
                )

            sent_id_mismatch = first_list_mismatch(gold_check.sent_ids, chk.sent_ids)
            if sent_id_mismatch is not None:
                failures.append(f"Aligned sent_id sequence mismatch in {chk.path.name}: {sent_id_mismatch}")
        else:
            if chk.sent_id_present < chk.blocks:
                warnings.append(f"Missing # sent_id in {chk.path.name}: {chk.blocks - chk.sent_id_present} sentence blocks")
            if chk.text_present < chk.blocks:
                warnings.append(f"Missing # text in {chk.path.name}: {chk.blocks - chk.text_present} sentence blocks")
            if chk.sent_id_present > 0 and chk.unique_sent_id_count <= max(1, chk.blocks // 10):
                warnings.append(
                    f"Low sent_id uniqueness in {chk.path.name}: {chk.unique_sent_id_count} unique IDs for {chk.blocks} blocks"
                )

    if missing_results:
        failures.extend([f"Missing result file: {display_path(repo_root, path)}" for path in missing_results])
    if traceback_files:
        failures.extend([f"Result file starts with traceback: {display_path(repo_root, path)}" for path in traceback_files])

    for key, path in eval_paths.items():
        metric_map = eval_metrics.get(key, {})
        if key.endswith("_aligned"):
            for metric_name in ("Sentences", "Tokens", "Words"):
                value = metric_map.get(metric_name)
                if value is None:
                    failures.append(
                        f"Missing {metric_name} metric in aligned eval summary: {display_path(repo_root, path)}"
                    )
                elif value < 99.995:
                    failures.append(
                        f"Aligned eval summary is below 100 for {metric_name}: {display_path(repo_root, path)} = {value:.2f}"
                    )

    for mode, path in comparison_paths.items():
        if not path.exists():
            continue
        if not comparison_counts.get(mode):
            failures.append(f"Could not parse LAS difference snapshot from comparison report: {display_path(repo_root, path)}")

    status = "PASS" if not failures else "FAIL"

    lines: List[str] = []
    lines.append(f"# QA Validation Report: {run_id}")
    lines.append("")
    lines.append(f"- Status: **{status}**")
    lines.append(f"- Modes validated: {', '.join(active_modes)}")
    lines.append(f"- Gold file: {display_path(repo_root, gold_path)}")
    lines.append(f"- Predictions root: {display_path(repo_root, pred_root)}")
    lines.append(f"- Results root: {display_path(repo_root, run_results_root)}")
    lines.append(f"- Aligned results root: {display_path(repo_root, main_results_root)}")
    lines.append(f"- Supplementary base results root: {display_path(repo_root, supplementary_base_root)}")
    lines.append("")

    lines.append("## Gold Reference Counts")
    lines.append(f"- Sentences (evaluator): {gold_check.sentences}")
    lines.append(f"- Tokens (evaluator): {gold_check.tokens}")
    lines.append(f"- Words (evaluator): {gold_check.words}")
    lines.append(f"- Sentence blocks (raw split): {gold_check.blocks}")
    lines.append(f"- # sent_id present: {gold_check.sent_id_present}/{gold_check.blocks}")
    lines.append(f"- # text present: {gold_check.text_present}/{gold_check.blocks}")
    lines.append(f"- First sent_id values: {gold_check.sent_ids[:5]}")
    lines.append("")

    lines.append("## Prediction File Checks")
    for mode in active_modes:
        for model in ("classla", "trankit"):
            key = f"{model}_{mode}"
            chk = checks[key]
            lines.append(f"### {key}")
            lines.append(f"- Path: {display_path(repo_root, chk.path)}")
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
            lines.append(f"- First sent_id values: {chk.sent_ids[:5]}")
            lines.append(f"- Ends with blank line: {chk.ends_with_blank_line}")
            lines.append("")

    lines.append("## Result File Checks")
    lines.append(f"- Expected main files: {len(expected_main)}")
    lines.append(f"- Expected diagnostics files: {len(expected_diagnostics)}")
    lines.append(f"- Missing result files: {len(missing_results)}")
    lines.append(f"- Traceback-leading result files: {len(traceback_files)}")
    lines.append("")

    lines.append("## Core Metrics (F1 from eval summaries)")
    for mode in active_modes:
        for model in ("classla", "trankit"):
            key = f"{model}_{mode}"
            metric_map = eval_metrics.get(key, {})
            lines.append(f"### {key}")
            for metric in ("Sentences", "Tokens", "Words", "LAS", "UAS", "UPOS", "XPOS", "Lemmas", "MLAS"):
                value = metric_map.get(metric)
                if value is not None:
                    lines.append(f"- {metric}: {value:.2f}")
            lines.append("")

    lines.append("## Model-vs-Model LAS Difference Snapshot")
    for mode in active_modes:
        lines.append(f"### {mode}")
        snapshot = comparison_counts.get(mode, {})
        if not snapshot:
            lines.append("- Could not parse LAS section from comparison report")
        else:
            for label in ("a_only", "b_only", "both_correct", "both_wrong"):
                if label in snapshot:
                    lines.append(f"- {snapshot[label]}")
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

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
