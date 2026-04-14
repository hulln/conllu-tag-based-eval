#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
import re
import subprocess
import sys
from pathlib import Path
from typing import List


def canonical_mode(mode: str) -> str:
    if mode in {"base", "raw", "unaligned"}:
        return "base"
    return "aligned"


def sanitize_label(value: str) -> str:
    cleaned = value.strip().lower().replace("_", "-")
    cleaned = re.sub(r"[^a-z0-9-]+", "-", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return cleaned or "unknown"


def prediction_filename(run_stamp: str, dataset_tag: str, run_tag: str, model: str, mode: str) -> str:
    # Sort-friendly and self-describing: time, dataset, run type, model, mode.
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


def resolve_prediction_path(
    pred_root: Path,
    run_stamp: str,
    dataset_tag: str,
    run_tag: str,
    model: str,
    mode: str,
) -> Path:
    preferred = prediction_output_path(pred_root, run_stamp, dataset_tag, run_tag, model, mode)
    if preferred.exists():
        return preferred

    if mode == "base":
        legacy = prediction_legacy_path(pred_root, run_stamp, dataset_tag, run_tag, model, mode)
        if legacy.exists():
            return legacy

    return preferred


def result_filename(
    run_stamp: str,
    dataset_tag: str,
    run_tag: str,
    subject: str,
    mode: str,
    artifact: str,
    extension: str,
) -> str:
    subject_tag = sanitize_label(subject)
    artifact_tag = sanitize_label(artifact)
    return f"{run_stamp}_{dataset_tag}_{run_tag}_{subject_tag}_{mode}_{artifact_tag}.{extension}"


def discover_latest_complete_run_stamp(
    pred_root: Path,
    dataset_tag: str,
    run_tag: str,
    active_modes: List[str],
) -> str | None:
    required = {(model, mode) for model in ("classla", "trankit") for mode in active_modes}
    by_stamp: dict[str, set[tuple[str, str]]] = {}

    for path in pred_root.rglob(f"*_{dataset_tag}_{run_tag}_*_predicted.conllu"):
        name = path.name
        if not name.endswith("_predicted.conllu"):
            continue

        core = name[: -len("_predicted.conllu")]
        try:
            prefix, model, mode = core.rsplit("_", 2)
            stamp, _rest = prefix.split("_", 1)
        except ValueError:
            continue

        if model not in {"classla", "trankit"}:
            continue
        if mode not in active_modes:
            continue

        by_stamp.setdefault(stamp, set()).add((model, mode))

    complete = [stamp for stamp, present in by_stamp.items() if required.issubset(present)]
    if not complete:
        return None

    return sorted(complete)[-1]


def run(cmd: List[str], cwd: Path, output_file: Path | None = None) -> None:
    pretty = " ".join(cmd)
    print(f"$ {pretty}")

    if output_file is None:
        subprocess.run(cmd, cwd=str(cwd), check=True)
        return

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as f:
        subprocess.run(cmd, cwd=str(cwd), check=True, stdout=f, stderr=subprocess.STDOUT)


def build_sample_input(source: Path, target: Path, sample_lines: int) -> None:
    lines = []
    for line in source.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        lines.append(line)
        if len(lines) == sample_lines:
            break

    if len(lines) < sample_lines:
        raise ValueError(f"Requested {sample_lines} lines but source only has {len(lines)} non-empty lines: {source}")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote sample input: {target} ({len(lines)} lines)")


def build_sample_gold(source: Path, target: Path, sample_sentences: int) -> None:
    blocks = [block for block in source.read_text(encoding="utf-8").strip().split("\n\n") if block.strip()]
    if len(blocks) < sample_sentences:
        raise ValueError(
            f"Requested {sample_sentences} sentences but gold has {len(blocks)} sentence blocks: {source}"
        )

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n\n".join(blocks[:sample_sentences]) + "\n\n", encoding="utf-8")
    print(f"Wrote sample gold: {target} ({sample_sentences} sentences)")


def eval_and_analyze(
    repo_root: Path,
    python_bin: str,
    gold_path: Path,
    pred_path: Path,
    summary_out: Path,
    tagged_out: Path,
    errors_out: Path,
    model_name: str,
    top_n: int,
) -> None:
    run(
        [
            python_bin,
            "evaluation/conll18_ud_eval_tag-based.py",
            str(gold_path),
            str(pred_path),
            "-v",
        ],
        cwd=repo_root,
        output_file=summary_out,
    )

    run(
        [
            python_bin,
            "evaluation/conll18_ud_eval_tag-based.py",
            str(gold_path),
            str(pred_path),
            "-v",
            "--upos",
            ".*",
            "--xpos",
            ".*",
            "--uas",
            ".*",
            "--las",
            ".*",
        ],
        cwd=repo_root,
        output_file=tagged_out,
    )

    run(
        [
            python_bin,
            "scripts/analyze_errors.py",
            str(gold_path),
            str(pred_path),
            str(errors_out),
            "--model-name",
            model_name,
            "--top-n",
            str(top_n),
        ],
        cwd=repo_root,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the full evaluation pipeline for CLASSLA and Trankit.")
    parser.add_argument(
        "--gold",
        default="data/gold/sl_ssj-ud-test.conllu",
        help="Path to gold CoNLL-U file.",
    )
    parser.add_argument(
        "--input",
        default="data/raw/sl_ssj-ud-test.sentences.txt",
        help="Path to raw sentence-per-line text file.",
    )
    parser.add_argument(
        "--sample-lines",
        type=int,
        default=0,
        help="If >0, run on the first N non-empty lines only.",
    )
    parser.add_argument(
        "--download-classla-models",
        action="store_true",
        help="Download CLASSLA models before first CLASSLA run.",
    )
    parser.add_argument(
        "--skip-prediction",
        action="store_true",
        help="Skip prediction and only run evaluation/analysis on existing prediction files.",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=20,
        help="Top N rows for confusion tables.",
    )
    parser.add_argument(
        "--modes",
        choices=["both", "aligned", "base", "raw", "unaligned"],
        default="aligned",
        help=(
            "Run only aligned (default, primary task), both modes, or one specific mode. "
            "Canonical modes are aligned and base; raw/unaligned are aliases of base."
        ),
    )
    parser.add_argument(
        "--run-stamp",
        default=None,
        help=(
            "Timestamp token used in flat prediction/result filenames. "
            "Default: current time in YYYYMMDD-HHMM format."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    python_bin = sys.executable

    gold_path = Path(args.gold)
    input_path = Path(args.input)

    if args.sample_lines > 0:
        run_label = f"sample-{args.sample_lines}"
        sample_input = Path("data/samples") / f"{run_label}.txt"
        sample_gold = Path("data/gold/samples") / f"{run_label}.conllu"
        build_sample_input(repo_root / input_path, repo_root / sample_input, args.sample_lines)
        build_sample_gold(repo_root / gold_path, repo_root / sample_gold, args.sample_lines)
        active_input = sample_input
        active_gold = sample_gold
        pred_root = Path("predictions/runs")
    else:
        run_label = "full"
        active_input = input_path
        active_gold = gold_path
        pred_root = Path("predictions/runs")

    active_modes = ["aligned", "base"] if args.modes == "both" else [canonical_mode(args.modes)]

    dataset_tag = sanitize_label(active_gold.stem)
    run_tag = sanitize_label(run_label)

    if args.run_stamp:
        run_stamp = sanitize_label(args.run_stamp)
    elif args.skip_prediction:
        detected = discover_latest_complete_run_stamp(pred_root, dataset_tag, run_tag, active_modes)
        if detected is None:
            raise ValueError(
                "--skip-prediction could not find a complete prediction set for the selected run/modes. "
                "Provide --run-stamp explicitly or run prediction first."
            )
        run_stamp = detected
        print(f"Auto-detected run stamp for --skip-prediction: {run_stamp}")
    else:
        run_stamp = datetime.now().strftime("%Y%m%d-%H%M")

    result_root = Path("results/runs") / f"{run_stamp}_{dataset_tag}_{run_tag}"
    main_results_root = result_root / "main"
    diagnostics_root = result_root / "diagnostics"
    supplementary_base_root = result_root / "supplementary" / "base"
    supplementary_base_main_root = supplementary_base_root / "main"
    supplementary_base_diagnostics_root = supplementary_base_root / "diagnostics"

    classla_preds = {
        mode: prediction_output_path(pred_root, run_stamp, dataset_tag, run_tag, "classla", mode)
        for mode in active_modes
    }
    trankit_preds = {
        mode: prediction_output_path(pred_root, run_stamp, dataset_tag, run_tag, "trankit", mode)
        for mode in active_modes
    }

    if args.skip_prediction:
        classla_preds = {
            mode: resolve_prediction_path(pred_root, run_stamp, dataset_tag, run_tag, "classla", mode)
            for mode in active_modes
        }
        trankit_preds = {
            mode: resolve_prediction_path(pred_root, run_stamp, dataset_tag, run_tag, "trankit", mode)
            for mode in active_modes
        }

    def mode_result_roots(mode: str) -> tuple[Path, Path]:
        if mode == "aligned":
            return main_results_root, diagnostics_root
        return supplementary_base_main_root, supplementary_base_diagnostics_root

    classla_results = {
        mode: {
            "eval": mode_result_roots(mode)[0] / f"classla_{mode}_eval.txt",
            "eval_tagged": mode_result_roots(mode)[1] / f"classla_{mode}_eval-tagged.txt",
            "errors": mode_result_roots(mode)[1] / f"classla_{mode}_errors.md",
        }
        for mode in active_modes
    }
    trankit_results = {
        mode: {
            "eval": mode_result_roots(mode)[0] / f"trankit_{mode}_eval.txt",
            "eval_tagged": mode_result_roots(mode)[1] / f"trankit_{mode}_eval-tagged.txt",
            "errors": mode_result_roots(mode)[1] / f"trankit_{mode}_errors.md",
        }
        for mode in active_modes
    }
    comparison_reports = {
        mode: mode_result_roots(mode)[0] / f"classla-vs-trankit_{mode}_comparison.md"
        for mode in active_modes
    }

    if not args.skip_prediction:
        if args.modes == "both":
            classla_cmd = [
                python_bin,
                "scripts/predict_classla.py",
                "--input",
                str(active_input),
                "--mode",
                "both",
                "--aligned-gold",
                str(active_gold),
                "--output-base",
                str(classla_preds["base"]),
                "--output-aligned",
                str(classla_preds["aligned"]),
            ]
            if args.download_classla_models:
                classla_cmd.append("--download-models")
            run(classla_cmd, cwd=repo_root)

            run(
                [
                    python_bin,
                    "scripts/predict_trankit.py",
                    "--input",
                    str(active_input),
                    "--mode",
                    "both",
                    "--aligned-gold",
                    str(active_gold),
                    "--output-base",
                    str(trankit_preds["base"]),
                    "--output-aligned",
                    str(trankit_preds["aligned"]),
                ],
                cwd=repo_root,
            )
        else:
            mode = active_modes[0]
            classla_cmd = [
                python_bin,
                "scripts/predict_classla.py",
                "--input",
                str(active_input),
                "--mode",
                mode,
                "--output",
                str(classla_preds[mode]),
            ]
            if mode == "aligned":
                classla_cmd.extend(["--aligned-gold", str(active_gold)])
            if args.download_classla_models:
                classla_cmd.append("--download-models")

            run(classla_cmd, cwd=repo_root)

            trankit_cmd = [
                python_bin,
                "scripts/predict_trankit.py",
                "--input",
                str(active_input),
                "--mode",
                mode,
                "--output",
                str(trankit_preds[mode]),
            ]
            if mode == "aligned":
                trankit_cmd.extend(["--aligned-gold", str(active_gold)])

            run(trankit_cmd, cwd=repo_root)

    for mode in active_modes:
        eval_and_analyze(
            repo_root,
            python_bin,
            active_gold,
            classla_preds[mode],
            classla_results[mode]["eval"],
            classla_results[mode]["eval_tagged"],
            classla_results[mode]["errors"],
            f"CLASSLA {mode}",
            args.top_n,
        )

        eval_and_analyze(
            repo_root,
            python_bin,
            active_gold,
            trankit_preds[mode],
            trankit_results[mode]["eval"],
            trankit_results[mode]["eval_tagged"],
            trankit_results[mode]["errors"],
            f"Trankit {mode}",
            args.top_n,
        )

        run(
            [
                python_bin,
                "scripts/compare_models.py",
                str(active_gold),
                str(classla_preds[mode]),
                str(trankit_preds[mode]),
                str(comparison_reports[mode]),
                "--model-a",
                f"CLASSLA {mode}",
                "--model-b",
                f"Trankit {mode}",
                "--top-n",
                str(args.top_n),
            ],
            cwd=repo_root,
        )

    print("")
    print("Pipeline completed.")
    print(f"Run label: {run_label}")
    print(f"Gold used: {active_gold}")
    print(f"Input used: {active_input}")
    print(f"Modes: {', '.join(active_modes)}")
    print(f"Run stamp: {run_stamp}")
    print(f"Predictions root: {pred_root}")
    print(f"Results root: {result_root}")
    print(f"Main results root (aligned): {main_results_root}")
    print(f"Diagnostics root (aligned): {diagnostics_root}")
    if "base" in active_modes:
        print(f"Supplementary base results root: {supplementary_base_root}")
    for mode in active_modes:
        print(f"Prediction file (CLASSLA {mode}): {classla_preds[mode]}")
        print(f"Prediction file (Trankit {mode}): {trankit_preds[mode]}")
        print(f"Result file (CLASSLA {mode} eval): {classla_results[mode]['eval']}")
        print(f"Result file (CLASSLA {mode} eval-tagged): {classla_results[mode]['eval_tagged']}")
        print(f"Result file (CLASSLA {mode} errors): {classla_results[mode]['errors']}")
        print(f"Result file (Trankit {mode} eval): {trankit_results[mode]['eval']}")
        print(f"Result file (Trankit {mode} eval-tagged): {trankit_results[mode]['eval_tagged']}")
        print(f"Result file (Trankit {mode} errors): {trankit_results[mode]['errors']}")
        print(f"Result file (comparison {mode}): {comparison_reports[mode]}")


if __name__ == "__main__":
    main()
