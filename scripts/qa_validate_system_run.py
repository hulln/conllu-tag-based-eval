#!/usr/bin/env python3
"""QA validation for an aligned run of a single system (e.g. Stanza).

qa_validate_run.py validates the Trankit + CLASSLA pair of a run_pipeline.py run and is
hash-pinned by references/canonical_run_manifest.json, so it is left unchanged. This script
imports its checking functions and applies the same aligned-mode failure rules to one
system's files:

  predictions/output/<run_id>_<system>_aligned_predicted.conllu
  results/output/<run_id>/main/<system>_aligned_eval.txt
  results/output/<run_id>/diagnostics/<system>_aligned_eval-tagged.txt
  results/output/<run_id>/diagnostics/<system>_aligned_errors.md

The pairwise "classla-vs-trankit" comparison report does not exist for a single system and is
not checked. In addition, check_trees() verifies dependency-tree well-formedness and that
ID/FORM match gold token by token; the evaluator rejects multiple roots and cycles on its own,
and this check reports such problems per sentence instead of as a single parse error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_validate_run import (  # noqa: E402
    display_path,
    first_existing_path,
    first_list_mismatch,
    inspect_prediction,
    load_ud_loader,
    parse_eval_metrics,
    prediction_legacy_path,
    prediction_output_path,
    resolve_path,
    sanitize_label,
)


def read_rows(path: Path) -> List[List[List[str]]]:
    sentences: List[List[List[str]]] = []
    rows: List[List[str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            if rows:
                sentences.append(rows)
                rows = []
            continue
        if line.startswith("#"):
            continue
        cols = line.split("\t")
        if len(cols) == 10 and cols[0].isdigit():
            rows.append(cols)
    if rows:
        sentences.append(rows)
    return sentences


def check_trees(pred_path: Path, gold_path: Path, max_examples: int = 20) -> Dict[str, object]:
    """Per-sentence structural checks of an aligned prediction against its gold file."""
    pred = read_rows(pred_path)
    gold = read_rows(gold_path)
    counts = {
        "sentences": len(pred),
        "gold_sentences": len(gold),
        "multiple_roots": 0,
        "no_root": 0,
        "cycles": 0,
        "head_out_of_range": 0,
        "head_not_integer": 0,
        "root_label_mismatch": 0,
        "id_mismatch": 0,
        "form_mismatch": 0,
        "length_mismatch": 0,
    }
    examples: List[str] = []

    def note(kind: str, idx: int, detail: str = "") -> None:
        counts[kind] += 1
        if len(examples) < max_examples:
            examples.append(f"sentence {idx + 1}: {kind} {detail}".rstrip())

    for idx, rows in enumerate(pred):
        grows = gold[idx] if idx < len(gold) else []
        if len(rows) != len(grows):
            note("length_mismatch", idx, f"(pred {len(rows)}, gold {len(grows)})")
        for pos, (prow, grow) in enumerate(zip(rows, grows), start=1):
            if prow[0] != grow[0] or prow[0] != str(pos):
                note("id_mismatch", idx, f"(token {pos}: pred {prow[0]!r}, gold {grow[0]!r})")
            if prow[1] != grow[1]:
                note("form_mismatch", idx, f"(token {pos}: pred {prow[1]!r}, gold {grow[1]!r})")

        n = len(rows)
        heads: List[int] = []
        ok_heads = True
        for row in rows:
            try:
                heads.append(int(row[6]))
            except ValueError:
                note("head_not_integer", idx, f"(token {row[0]}: {row[6]!r})")
                ok_heads = False
        if not ok_heads:
            continue
        roots = [i + 1 for i, h in enumerate(heads) if h == 0]
        if len(roots) > 1:
            note("multiple_roots", idx, f"(ids {roots})")
        elif not roots:
            note("no_root", idx)
        if any(h < 0 or h > n for h in heads):
            note("head_out_of_range", idx)
            continue
        for i, (h, row) in enumerate(zip(heads, rows), start=1):
            if (h == 0) != (row[7].split(":")[0] == "root"):
                note("root_label_mismatch", idx, f"(token {i}: head {h}, deprel {row[7]!r})")
        for start in range(1, n + 1):
            seen, node = set(), start
            while node != 0 and node not in seen:
                seen.add(node)
                node = heads[node - 1]
            if node != 0:
                note("cycles", idx, f"(through token {start})")
                break

    blocking = ("multiple_roots", "no_root", "cycles", "head_out_of_range", "head_not_integer",
                "id_mismatch", "form_mismatch", "length_mismatch")
    counts["blocking_problems"] = sum(counts[k] for k in blocking)
    return {"counts": counts, "examples": examples}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate one system's aligned run and write a QA markdown report.")
    parser.add_argument("--system", required=True, help="System key used in file names, e.g. stanza")
    parser.add_argument("--run-stamp", required=True, help="Run stamp, e.g. 20261030-1400-stanza114acc")
    parser.add_argument("--gold", required=True, help="Gold CoNLL-U path")
    parser.add_argument("--run-label", default="full", help="Run label (default: full)")
    parser.add_argument("--pred-root", default="predictions/output", help="Predictions root")
    parser.add_argument("--results-root", default="results/output", help="Results root")
    parser.add_argument("--output", default=None, help="Markdown output (default: <run>/main/qa_validation.md)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    system = sanitize_label(args.system)
    mode = "aligned"

    gold_path = resolve_path(repo_root, args.gold)
    dataset_tag = sanitize_label(gold_path.stem)
    run_tag = sanitize_label(args.run_label)
    run_stamp = sanitize_label(args.run_stamp)
    run_id = f"{run_stamp}_{dataset_tag}_{run_tag}"
    pred_root = resolve_path(repo_root, args.pred_root)
    results_root = resolve_path(repo_root, args.results_root)
    main_root = results_root / run_id / "main"
    diag_root = results_root / run_id / "diagnostics"
    output_path = resolve_path(repo_root, args.output) if args.output else main_root / "qa_validation.md"

    load_ud = load_ud_loader(repo_root)
    gold_check = inspect_prediction(gold_path, load_ud)
    if not gold_check.exists:
        raise FileNotFoundError(f"Gold file not found: {gold_path}")
    if not gold_check.parse_ok:
        raise RuntimeError(f"Gold file failed evaluator parse: {gold_path}: {gold_check.parse_error}")

    pred_path = first_existing_path(
        [
            prediction_output_path(pred_root, run_stamp, dataset_tag, run_tag, system, mode),
            prediction_legacy_path(pred_root, run_stamp, dataset_tag, run_tag, system, mode),
        ]
    )
    chk = inspect_prediction(pred_path, load_ud)
    eval_path = main_root / f"{system}_{mode}_eval.txt"
    expected = [eval_path, diag_root / f"{system}_{mode}_eval-tagged.txt", diag_root / f"{system}_{mode}_errors.md"]
    missing = [p for p in expected if not p.exists()]
    tracebacks = []
    for p in expected:
        if p.exists():
            first_line = p.read_text(encoding="utf-8").splitlines()[:1]
            if first_line and first_line[0].startswith("Traceback"):
                tracebacks.append(p)
    metrics = parse_eval_metrics(eval_path)
    trees = check_trees(pred_path, gold_path) if chk.exists else None

    failures: List[str] = []
    warnings: List[str] = []

    # Same aligned-mode rules as qa_validate_run.py.
    if not chk.exists:
        failures.append(f"Missing prediction file: {display_path(repo_root, chk.path)}")
    else:
        if chk.malformed_rows > 0:
            failures.append(f"Malformed rows found in {display_path(repo_root, chk.path)}: {chk.malformed_rows}")
        if not chk.parse_ok:
            failures.append(f"Evaluator parser failed for {display_path(repo_root, chk.path)}: {chk.parse_error}")
        if not chk.ends_with_blank_line:
            failures.append(f"CoNLL-U file does not end with blank line: {display_path(repo_root, chk.path)}")
        for label, observed, reference in (
            ("sentence count", chk.sentences, gold_check.sentences),
            ("token count", chk.tokens, gold_check.tokens),
            ("word count", chk.words, gold_check.words),
            ("sentence-block", chk.blocks, gold_check.blocks),
        ):
            if observed != reference:
                failures.append(f"Aligned {label} mismatch in {chk.path.name}: predicted={observed} gold={reference}")
        if chk.sent_id_present != chk.blocks:
            failures.append(f"Aligned prediction missing # sent_id lines: {chk.path.name} ({chk.sent_id_present}/{chk.blocks})")
        if chk.text_present != chk.blocks:
            failures.append(f"Aligned prediction missing # text lines: {chk.path.name} ({chk.text_present}/{chk.blocks})")
        if chk.unique_sent_id_count != chk.blocks:
            failures.append(
                f"Aligned prediction has non-unique sent_id values: {chk.path.name} ({chk.unique_sent_id_count}/{chk.blocks} unique)"
            )
        mismatch = first_list_mismatch(gold_check.sent_ids, chk.sent_ids)
        if mismatch is not None:
            failures.append(f"Aligned sent_id sequence mismatch in {chk.path.name}: {mismatch}")

    failures.extend(f"Missing result file: {display_path(repo_root, p)}" for p in missing)
    failures.extend(f"Result file starts with traceback: {display_path(repo_root, p)}" for p in tracebacks)
    if eval_path.exists():
        for name in ("Sentences", "Tokens", "Words"):
            value = metrics.get(name)
            if value is None:
                failures.append(f"Missing {name} metric in aligned eval summary: {display_path(repo_root, eval_path)}")
            elif value < 99.995:
                failures.append(f"Aligned eval summary is below 100 for {name}: {display_path(repo_root, eval_path)} = {value:.2f}")

    # Additional structural checks (see module docstring).
    if trees is not None:
        tc = trees["counts"]
        if tc["blocking_problems"]:
            failures.append(f"Structural problems in {chk.path.name}: " + ", ".join(
                f"{k}={tc[k]}" for k in ("multiple_roots", "no_root", "cycles", "head_out_of_range",
                                         "head_not_integer", "id_mismatch", "form_mismatch", "length_mismatch") if tc[k]))
        if tc["root_label_mismatch"]:
            warnings.append(f"HEAD=0 and DEPREL=root disagree on {tc['root_label_mismatch']} tokens in {chk.path.name}")

    status = "PASS" if not failures else "FAIL"
    key = f"{system}_{mode}"
    lines: List[str] = [
        f"# QA Validation Report: {run_id}",
        "",
        f"- Status: **{status}**",
        f"- System: {system}",
        f"- Modes validated: {mode}",
        f"- Gold file: {display_path(repo_root, gold_path)}",
        f"- Predictions root: {display_path(repo_root, pred_root)}",
        f"- Results root: {display_path(repo_root, results_root / run_id)}",
        f"- Validator: scripts/qa_validate_system_run.py (check functions from scripts/qa_validate_run.py)",
        "",
        "## Gold Reference Counts",
        f"- Sentences (evaluator): {gold_check.sentences}",
        f"- Tokens (evaluator): {gold_check.tokens}",
        f"- Words (evaluator): {gold_check.words}",
        f"- Sentence blocks (raw split): {gold_check.blocks}",
        f"- # sent_id present: {gold_check.sent_id_present}/{gold_check.blocks}",
        f"- # text present: {gold_check.text_present}/{gold_check.blocks}",
        f"- First sent_id values: {gold_check.sent_ids[:5]}",
        "",
        "## Prediction File Checks",
        f"### {key}",
        f"- Path: {display_path(repo_root, chk.path)}",
        f"- Exists: {chk.exists}",
        f"- Evaluator parse OK: {chk.parse_ok}",
    ]
    if chk.parse_error:
        lines.append(f"- Parse error: {chk.parse_error}")
    lines += [
        f"- Sentences (evaluator): {chk.sentences}",
        f"- Tokens (evaluator): {chk.tokens}",
        f"- Words (evaluator): {chk.words}",
        f"- Sentence blocks (raw split): {chk.blocks}",
        f"- Malformed token rows: {chk.malformed_rows}",
        f"- # sent_id present: {chk.sent_id_present}/{chk.blocks}",
        f"- # text present: {chk.text_present}/{chk.blocks}",
        f"- Unique sent_id count: {chk.unique_sent_id_count}",
        f"- First sent_id values: {chk.sent_ids[:5]}",
        f"- Ends with blank line: {chk.ends_with_blank_line}",
        "",
        "## Tree Structure Checks",
    ]
    if trees is None:
        lines.append("- Not run (prediction file missing)")
    else:
        lines += [f"- {k}: {v}" for k, v in trees["counts"].items()]
        lines += [f"- example: {e}" for e in trees["examples"]]
    lines += [
        "",
        "## Result File Checks",
        f"- Expected files: {len(expected)}",
        f"- Missing result files: {len(missing)}",
        f"- Traceback-leading result files: {len(tracebacks)}",
        "",
        "## Core Metrics (F1 from eval summary)",
        f"### {key}",
    ]
    for metric in ("Sentences", "Tokens", "Words", "LAS", "UAS", "UPOS", "XPOS", "Lemmas", "MLAS"):
        if metric in metrics:
            lines.append(f"- {metric}: {metrics[metric]:.2f}")
    lines += ["", "## Failures"] + ([f"- {x}" for x in failures] or ["- None"])
    lines += ["", "## Warnings"] + ([f"- {x}" for x in warnings] or ["- None"]) + [""]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    (output_path.parent / "qa_tree_checks.json").write_text(
        json.dumps(trees, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote QA validation report to {output_path}")
    print(f"Status: {status}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
