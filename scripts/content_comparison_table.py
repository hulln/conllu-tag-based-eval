#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


def read_conllu(path: Path) -> List[Dict]:
    sentences: List[Dict] = []
    tokens: List[Dict] = []
    meta: Dict[str, str] = {}

    def flush() -> None:
        nonlocal tokens, meta
        if tokens or meta:
            sentences.append(
                {
                    "sent_id": meta.get("sent_id"),
                    "text": meta.get("text"),
                    "tokens": tokens,
                }
            )
        tokens = []
        meta = {}

    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            flush()
            continue

        if line.startswith("#"):
            if line.startswith("# sent_id = "):
                meta["sent_id"] = line[len("# sent_id = ") :].strip()
            elif line.startswith("# text = "):
                meta["text"] = line[len("# text = ") :].strip()
            continue

        cols = line.split("\t")
        if len(cols) != 10:
            continue

        tok_id = cols[0]
        if "-" in tok_id or "." in tok_id:
            continue

        try:
            position = int(tok_id)
        except ValueError:
            position = len(tokens) + 1

        tokens.append(
            {
                "id": position,
                "form": cols[1],
                "head": cols[6],
                "deprel": cols[7].split(":")[0],
            }
        )

    flush()
    return sentences


def align_sentences(gold_sents: Sequence[Dict], pred_sents: Sequence[Dict]):
    if len(gold_sents) == len(pred_sents):
        text_total = 0
        text_matches = 0
        for g, p in zip(gold_sents, pred_sents):
            if g.get("text") and p.get("text"):
                text_total += 1
                if g["text"] == p["text"]:
                    text_matches += 1
        if text_total == 0 or text_matches / max(text_total, 1) >= 0.95:
            return [(idx, g, idx, p) for idx, (g, p) in enumerate(zip(gold_sents, pred_sents))], [], []

    pred_by_text = defaultdict(list)
    for p_idx, p in enumerate(pred_sents):
        text = p.get("text")
        if text:
            pred_by_text[text].append((p_idx, p))

    pairs = []
    unmatched_gold = []
    used_pred = set()

    for g_idx, g in enumerate(gold_sents):
        text = g.get("text")
        if text and pred_by_text.get(text):
            p_idx, p = pred_by_text[text].pop(0)
            pairs.append((g_idx, g, p_idx, p))
            used_pred.add(p_idx)
        else:
            unmatched_gold.append(g_idx)

    unmatched_pred = [idx for idx in range(len(pred_sents)) if idx not in used_pred]
    return pairs, unmatched_gold, unmatched_pred


def _pct(numerator: int, denominator: int) -> float:
    return 100.0 * numerator / denominator if denominator else 0.0


def _trim(text: str | None, max_len: int = 96) -> str:
    safe = (text or "").replace("|", "/")
    if len(safe) <= max_len:
        return safe
    return safe[: max_len - 3] + "..."


def _example_line(example: Dict, with_both_models: bool = False) -> str:
    base = (
        f"sid={example['sent_id']}; tok={example['token_form']}#{example['token_id']}; "
        f"gold=({example['gold_head']},{example['gold_rel']})"
    )

    if with_both_models:
        tail = (
            f"; classla=({example['classla_head']},{example['classla_rel']}); "
            f"trankit=({example['trankit_head']},{example['trankit_rel']})"
        )
    else:
        tail = f"; pred=({example['pred_head']},{example['pred_rel']})"

    return (base + tail + f"; text=\"{_trim(example['text'])}\"").replace("|", "/")


def _push_example(example_store: Dict, key, example: Dict, max_examples: int) -> None:
    rows = example_store.setdefault(key, [])
    if len(rows) < max_examples:
        rows.append(example)


def _model_error_profile(
    model_name: str,
    gold_sents: Sequence[Dict],
    pred_sents: Sequence[Dict],
    top_n: int,
    max_examples: int,
) -> Dict:
    pairs, unmatched_gold, unmatched_pred = align_sentences(gold_sents, pred_sents)

    totals = Counter()
    head_only = Counter()
    rel_only = Counter()
    both_wrong = Counter()

    head_only_examples: Dict = {}
    rel_only_examples: Dict = {}
    both_wrong_examples: Dict = {}

    for g_idx, g, _p_idx, p in pairs:
        gtoks = g["tokens"]
        ptoks = p["tokens"]

        if len(gtoks) != len(ptoks):
            totals["skipped_len_mismatch"] += 1
            continue

        for gt, pt in zip(gtoks, ptoks):
            if gt["form"] != pt["form"]:
                totals["skipped_form_mismatch"] += 1
                continue

            totals["compared"] += 1
            head_ok = gt["head"] == pt["head"]
            rel_ok = gt["deprel"] == pt["deprel"]

            if head_ok and rel_ok:
                totals["las_correct"] += 1
                continue

            example = {
                "sent_id": g.get("sent_id") or str(g_idx + 1),
                "text": g.get("text") or "",
                "token_id": gt["id"],
                "token_form": gt["form"],
                "gold_head": gt["head"],
                "gold_rel": gt["deprel"],
                "pred_head": pt["head"],
                "pred_rel": pt["deprel"],
            }

            if not head_ok and rel_ok:
                key = gt["deprel"]
                head_only[key] += 1
                totals["head_only"] += 1
                _push_example(head_only_examples, key, example, max_examples)
            elif head_ok and not rel_ok:
                key = (gt["deprel"], pt["deprel"])
                rel_only[key] += 1
                totals["rel_only"] += 1
                _push_example(rel_only_examples, key, example, max_examples)
            else:
                key = (gt["deprel"], pt["deprel"])
                both_wrong[key] += 1
                totals["both_wrong"] += 1
                _push_example(both_wrong_examples, key, example, max_examples)

    return {
        "model_name": model_name,
        "pairs": len(pairs),
        "unmatched_gold": len(unmatched_gold),
        "unmatched_pred": len(unmatched_pred),
        "totals": totals,
        "head_only": head_only,
        "rel_only": rel_only,
        "both_wrong": both_wrong,
        "head_only_examples": head_only_examples,
        "rel_only_examples": rel_only_examples,
        "both_wrong_examples": both_wrong_examples,
        "top_n": top_n,
    }


def _render_bucket_rows(
    counter: Counter,
    examples: Dict,
    compared: int,
    bucket: str,
    top_n: int,
) -> List[str]:
    rows = []
    if not counter:
        rows.append("| - | - | - | - |")
        return rows

    for rank, (key, count) in enumerate(counter.most_common(top_n), start=1):
        if bucket == "head_only":
            gold_label = str(key)
            pred_label = "(same DEPREL, wrong HEAD)"
        else:
            gold_label, pred_label = key

        ex = _example_line(examples.get(key, [{}])[0]) if examples.get(key) else ""
        rows.append(
            f"| {rank} | {gold_label} | {pred_label} | {count} ({_pct(count, compared):.2f}%) | {ex} |"
        )
    return rows


def _loser_error_desc(g_rel: str, loser_rel: str, loser_head_ok: bool) -> str:
    if loser_head_ok and loser_rel != g_rel:
        return f"DEPREL {g_rel}->{loser_rel}, HEAD ok"
    if not loser_head_ok and loser_rel == g_rel:
        return f"HEAD wrong, DEPREL {g_rel}"
    if not loser_head_ok and loser_rel != g_rel:
        return f"HEAD wrong + DEPREL {g_rel}->{loser_rel}"
    return "unexpected"


def _model_vs_model_section(
    gold_sents: Sequence[Dict],
    classla_sents: Sequence[Dict],
    trankit_sents: Sequence[Dict],
    top_n: int,
    max_examples: int,
) -> Dict:
    classla_pairs, _, _ = align_sentences(gold_sents, classla_sents)
    trankit_pairs, _, _ = align_sentences(gold_sents, trankit_sents)

    classla_map = {g_idx: p for g_idx, _g, _p_idx, p in classla_pairs}
    trankit_map = {g_idx: p for g_idx, _g, _p_idx, p in trankit_pairs}

    shared = sorted(set(classla_map.keys()) & set(trankit_map.keys()))

    totals = Counter()
    classla_wins = Counter()
    trankit_wins = Counter()
    classla_win_examples: Dict = {}
    trankit_win_examples: Dict = {}

    for g_idx in shared:
        g = gold_sents[g_idx]
        c = classla_map[g_idx]
        t = trankit_map[g_idx]

        gtoks = g["tokens"]
        ctoks = c["tokens"]
        ttoks = t["tokens"]

        if len(gtoks) != len(ctoks) or len(gtoks) != len(ttoks):
            totals["skipped_len_mismatch"] += 1
            continue

        for gt, ct, tt in zip(gtoks, ctoks, ttoks):
            if gt["form"] != ct["form"] or gt["form"] != tt["form"]:
                totals["skipped_form_mismatch"] += 1
                continue

            totals["compared"] += 1

            c_ok = (ct["head"] == gt["head"]) and (ct["deprel"] == gt["deprel"])
            t_ok = (tt["head"] == gt["head"]) and (tt["deprel"] == gt["deprel"])

            if c_ok and not t_ok:
                key = (gt["deprel"], tt["deprel"], tt["head"] == gt["head"])
                classla_wins[key] += 1
                totals["classla_wins"] += 1
                example = {
                    "sent_id": g.get("sent_id") or str(g_idx + 1),
                    "text": g.get("text") or "",
                    "token_id": gt["id"],
                    "token_form": gt["form"],
                    "gold_head": gt["head"],
                    "gold_rel": gt["deprel"],
                    "classla_head": ct["head"],
                    "classla_rel": ct["deprel"],
                    "trankit_head": tt["head"],
                    "trankit_rel": tt["deprel"],
                }
                _push_example(classla_win_examples, key, example, max_examples)
            elif t_ok and not c_ok:
                key = (gt["deprel"], ct["deprel"], ct["head"] == gt["head"])
                trankit_wins[key] += 1
                totals["trankit_wins"] += 1
                example = {
                    "sent_id": g.get("sent_id") or str(g_idx + 1),
                    "text": g.get("text") or "",
                    "token_id": gt["id"],
                    "token_form": gt["form"],
                    "gold_head": gt["head"],
                    "gold_rel": gt["deprel"],
                    "classla_head": ct["head"],
                    "classla_rel": ct["deprel"],
                    "trankit_head": tt["head"],
                    "trankit_rel": tt["deprel"],
                }
                _push_example(trankit_win_examples, key, example, max_examples)

    return {
        "totals": totals,
        "classla_wins": classla_wins,
        "trankit_wins": trankit_wins,
        "classla_win_examples": classla_win_examples,
        "trankit_win_examples": trankit_win_examples,
        "top_n": top_n,
    }


def _render_win_rows(counter: Counter, examples: Dict, compared: int, top_n: int) -> List[str]:
    if not counter:
        return ["| - | - | - | - |"]

    rows = []
    for rank, ((g_rel, loser_rel, loser_head_ok), count) in enumerate(counter.most_common(top_n), start=1):
        desc = _loser_error_desc(g_rel, loser_rel, loser_head_ok)
        ex = _example_line(examples.get((g_rel, loser_rel, loser_head_ok), [{}])[0], with_both_models=True)
        rows.append(f"| {rank} | {g_rel} | {desc} | {count} ({_pct(count, compared):.2f}%) | {ex} |")
    return rows


def build_report(
    gold_path: Path,
    classla_pred_path: Path,
    trankit_pred_path: Path,
    out_path: Path,
    model_a: str,
    model_b: str,
    top_n: int,
    max_examples: int,
) -> None:
    gold_sents = read_conllu(gold_path)
    classla_sents = read_conllu(classla_pred_path)
    trankit_sents = read_conllu(trankit_pred_path)

    classla_profile = _model_error_profile(model_a, gold_sents, classla_sents, top_n, max_examples)
    trankit_profile = _model_error_profile(model_b, gold_sents, trankit_sents, top_n, max_examples)
    diff = _model_vs_model_section(gold_sents, classla_sents, trankit_sents, top_n, max_examples)

    lines: List[str] = []
    lines.append(f"# Table-style content comparison ({model_a} vs {model_b})")
    lines.append("")
    lines.append("Columns 7-8 are compared directly (HEAD and DEPREL), with concrete token examples.")
    lines.append("")
    lines.append("## Scope")
    lines.append(f"- Gold sentences: {len(gold_sents)}")
    lines.append(f"- {model_a} sentences: {len(classla_sents)}")
    lines.append(f"- {model_b} sentences: {len(trankit_sents)}")
    lines.append("")

    def render_model_section(profile: Dict) -> None:
        totals = profile["totals"]
        compared = totals["compared"]
        lines.append(f"## {profile['model_name']} - error content tables")
        lines.append(f"- Compared tokens: {compared}")
        lines.append(f"- LAS-correct tokens: {totals['las_correct']} ({_pct(totals['las_correct'], compared):.2f}%)")
        lines.append("")

        lines.append("### A) HEAD wrong, DEPREL correct")
        lines.append("| Rank | Gold DEPREL | Pred DEPREL | Count | Example |")
        lines.append("|---|---|---|---:|---|")
        lines.extend(_render_bucket_rows(profile["head_only"], profile["head_only_examples"], compared, "head_only", profile["top_n"]))
        lines.append("")

        lines.append("### B) HEAD correct, DEPREL wrong")
        lines.append("| Rank | Gold DEPREL | Pred DEPREL | Count | Example |")
        lines.append("|---|---|---|---:|---|")
        lines.extend(_render_bucket_rows(profile["rel_only"], profile["rel_only_examples"], compared, "rel_only", profile["top_n"]))
        lines.append("")

        lines.append("### C) HEAD wrong, DEPREL wrong")
        lines.append("| Rank | Gold DEPREL | Pred DEPREL | Count | Example |")
        lines.append("|---|---|---|---:|---|")
        lines.extend(_render_bucket_rows(profile["both_wrong"], profile["both_wrong_examples"], compared, "both_wrong", profile["top_n"]))
        lines.append("")

    render_model_section(classla_profile)
    render_model_section(trankit_profile)

    compared_diff = diff["totals"]["compared"]
    lines.append("## Direct model comparison (LAS exact)")
    lines.append(f"- Compared tokens: {compared_diff}")
    lines.append(f"- {model_a} correct, {model_b} wrong: {diff['totals']['classla_wins']} ({_pct(diff['totals']['classla_wins'], compared_diff):.2f}%)")
    lines.append(f"- {model_b} correct, {model_a} wrong: {diff['totals']['trankit_wins']} ({_pct(diff['totals']['trankit_wins'], compared_diff):.2f}%)")
    lines.append("")

    lines.append(f"### Where {model_a} is better")
    lines.append("| Rank | Gold DEPREL | Loser error pattern | Count | Example |")
    lines.append("|---|---|---|---:|---|")
    lines.extend(_render_win_rows(diff["classla_wins"], diff["classla_win_examples"], compared_diff, diff["top_n"]))
    lines.append("")

    lines.append(f"### Where {model_b} is better")
    lines.append("| Rank | Gold DEPREL | Loser error pattern | Count | Example |")
    lines.append("|---|---|---|---:|---|")
    lines.extend(_render_win_rows(diff["trankit_wins"], diff["trankit_win_examples"], compared_diff, diff["top_n"]))
    lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote content comparison report to {out_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Table-style HEAD/DEPREL content comparison from CoNLL-U files.")
    parser.add_argument("gold", help="Path to gold CoNLL-U file")
    parser.add_argument("classla_pred", help="Path to CLASSLA prediction CoNLL-U")
    parser.add_argument("trankit_pred", help="Path to Trankit prediction CoNLL-U")
    parser.add_argument("out", help="Path to output Markdown table report")
    parser.add_argument("--model-a", default="CLASSLA aligned", help="Label for model A")
    parser.add_argument("--model-b", default="Trankit aligned", help="Label for model B")
    parser.add_argument("--top-n", type=int, default=15, help="Top N rows per table")
    parser.add_argument("--examples-per-item", type=int, default=1, help="Max stored examples per pattern")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_report(
        gold_path=Path(args.gold),
        classla_pred_path=Path(args.classla_pred),
        trankit_pred_path=Path(args.trankit_pred),
        out_path=Path(args.out),
        model_a=args.model_a,
        model_b=args.model_b,
        top_n=args.top_n,
        max_examples=max(1, args.examples_per_item),
    )


if __name__ == "__main__":
    main()
