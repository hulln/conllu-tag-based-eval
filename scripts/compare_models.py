#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


def read_conllu(path: Path) -> List[Dict]:
    sentences = []
    tokens = []
    meta = {}

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

        tokens.append(
            {
                "form": cols[1],
                "head": cols[6],
                "deprel": cols[7].split(":")[0],
            }
        )

    flush()
    return sentences


def align_sentences(gold_sents: List[Dict], pred_sents: List[Dict]):
    if len(gold_sents) == len(pred_sents):
        text_total = 0
        text_matches = 0
        for g, p in zip(gold_sents, pred_sents):
            if g.get("text") and p.get("text"):
                text_total += 1
                if g["text"] == p["text"]:
                    text_matches += 1
        if text_total == 0 or text_matches / max(text_total, 1) >= 0.95:
            pairs = []
            for idx, (g, p) in enumerate(zip(gold_sents, pred_sents)):
                pairs.append((idx, g, idx, p))
            return pairs, [], []

    pred_by_text = defaultdict(list)
    for p_idx, p in enumerate(pred_sents):
        if p.get("text"):
            pred_by_text[p["text"]].append((p_idx, p))

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


def _pct(num: int, den: int) -> float:
    return 100.0 * num / den if den else 0.0


def _build_gold_to_pred_map(gold_sents: List[Dict], pred_sents: List[Dict]):
    pairs, unmatched_gold, unmatched_pred = align_sentences(gold_sents, pred_sents)
    mapping = {}
    for g_idx, _g, p_idx, p in pairs:
        mapping[g_idx] = (p_idx, p)
    return mapping, unmatched_gold, unmatched_pred


def _render_counter(counter: Counter, top_n: int) -> List[str]:
    lines = ["gold_deprel\tpred_deprel\tcount"]
    for (g_rel, p_rel), count in counter.most_common(top_n):
        lines.append(f"{g_rel}\t{p_rel}\t{count}")
    if len(lines) == 1:
        lines.append("(no items)")
    return lines


def compare(
    gold_path: Path,
    pred_a_path: Path,
    pred_b_path: Path,
    out_path: Path,
    model_a: str,
    model_b: str,
    top_n: int,
) -> None:
    gold = read_conllu(gold_path)
    pred_a = read_conllu(pred_a_path)
    pred_b = read_conllu(pred_b_path)

    map_a, unmatched_gold_a, unmatched_pred_a = _build_gold_to_pred_map(gold, pred_a)
    map_b, unmatched_gold_b, unmatched_pred_b = _build_gold_to_pred_map(gold, pred_b)

    common_gold_idxs = sorted(set(map_a.keys()) & set(map_b.keys()))

    totals = Counter()
    skipped_len_mismatch_sentences = 0
    skipped_form_mismatch_tokens = 0

    b_errors_when_a_las_better = Counter()
    a_errors_when_b_las_better = Counter()
    b_errors_when_a_rel_better = Counter()
    a_errors_when_b_rel_better = Counter()

    for g_idx in common_gold_idxs:
        g_tokens = gold[g_idx]["tokens"]
        a_tokens = map_a[g_idx][1]["tokens"]
        b_tokens = map_b[g_idx][1]["tokens"]

        if len(g_tokens) != len(a_tokens) or len(g_tokens) != len(b_tokens):
            skipped_len_mismatch_sentences += 1
            continue

        for gt, at, bt in zip(g_tokens, a_tokens, b_tokens):
            if gt["form"] != at["form"] or gt["form"] != bt["form"]:
                skipped_form_mismatch_tokens += 1
                continue

            totals["compared_tokens"] += 1

            g_head, g_rel = gt["head"], gt["deprel"]
            a_head, a_rel = at["head"], at["deprel"]
            b_head, b_rel = bt["head"], bt["deprel"]

            a_uas_ok = a_head == g_head
            b_uas_ok = b_head == g_head
            a_rel_ok = a_rel == g_rel
            b_rel_ok = b_rel == g_rel
            a_las_ok = a_uas_ok and a_rel_ok
            b_las_ok = b_uas_ok and b_rel_ok

            if a_las_ok and not b_las_ok:
                totals["las_a_only"] += 1
                b_errors_when_a_las_better[(g_rel, b_rel)] += 1
            elif b_las_ok and not a_las_ok:
                totals["las_b_only"] += 1
                a_errors_when_b_las_better[(g_rel, a_rel)] += 1
            elif a_las_ok and b_las_ok:
                totals["las_both"] += 1
            else:
                totals["las_neither"] += 1

            if a_uas_ok and not b_uas_ok:
                totals["uas_a_only"] += 1
            elif b_uas_ok and not a_uas_ok:
                totals["uas_b_only"] += 1
            elif a_uas_ok and b_uas_ok:
                totals["uas_both"] += 1
            else:
                totals["uas_neither"] += 1

            if a_rel_ok and not b_rel_ok:
                totals["rel_a_only"] += 1
                b_errors_when_a_rel_better[(g_rel, b_rel)] += 1
            elif b_rel_ok and not a_rel_ok:
                totals["rel_b_only"] += 1
                a_errors_when_b_rel_better[(g_rel, a_rel)] += 1
            elif a_rel_ok and b_rel_ok:
                totals["rel_both"] += 1
            else:
                totals["rel_neither"] += 1

    compared = totals["compared_tokens"]

    out = []
    out.append(f"# {model_a} vs {model_b} (exact difference report)")
    out.append("")
    out.append("## Coverage")
    out.append(f"- Gold sentences: {len(gold)}")
    out.append(f"- {model_a} predicted sentences: {len(pred_a)}")
    out.append(f"- {model_b} predicted sentences: {len(pred_b)}")
    out.append(f"- Gold sentences paired with both models: {len(common_gold_idxs)}")
    out.append(f"- Unmatched gold for {model_a}: {len(unmatched_gold_a)}")
    out.append(f"- Unmatched gold for {model_b}: {len(unmatched_gold_b)}")
    out.append(f"- Unmatched predicted for {model_a}: {len(unmatched_pred_a)}")
    out.append(f"- Unmatched predicted for {model_b}: {len(unmatched_pred_b)}")
    out.append(f"- Skipped sentence pairs (token count mismatch): {skipped_len_mismatch_sentences}")
    out.append(f"- Compared tokens (FORM-aligned): {compared}")
    out.append(f"- Skipped tokens (FORM mismatch): {skipped_form_mismatch_tokens}")
    out.append("")

    out.append("## LAS exact differences")
    out.append(f"- {model_a} correct, {model_b} wrong: {totals['las_a_only']} ({_pct(totals['las_a_only'], compared):.2f}%)")
    out.append(f"- {model_a} wrong, {model_b} correct: {totals['las_b_only']} ({_pct(totals['las_b_only'], compared):.2f}%)")
    out.append(f"- Both correct: {totals['las_both']} ({_pct(totals['las_both'], compared):.2f}%)")
    out.append(f"- Both wrong: {totals['las_neither']} ({_pct(totals['las_neither'], compared):.2f}%)")
    out.append("")

    out.append("## UAS exact differences")
    out.append(f"- {model_a} correct, {model_b} wrong: {totals['uas_a_only']} ({_pct(totals['uas_a_only'], compared):.2f}%)")
    out.append(f"- {model_a} wrong, {model_b} correct: {totals['uas_b_only']} ({_pct(totals['uas_b_only'], compared):.2f}%)")
    out.append(f"- Both correct: {totals['uas_both']} ({_pct(totals['uas_both'], compared):.2f}%)")
    out.append(f"- Both wrong: {totals['uas_neither']} ({_pct(totals['uas_neither'], compared):.2f}%)")
    out.append("")

    out.append("## DEPREL exact differences")
    out.append(f"- {model_a} correct, {model_b} wrong: {totals['rel_a_only']} ({_pct(totals['rel_a_only'], compared):.2f}%)")
    out.append(f"- {model_a} wrong, {model_b} correct: {totals['rel_b_only']} ({_pct(totals['rel_b_only'], compared):.2f}%)")
    out.append(f"- Both correct: {totals['rel_both']} ({_pct(totals['rel_both'], compared):.2f}%)")
    out.append(f"- Both wrong: {totals['rel_neither']} ({_pct(totals['rel_neither'], compared):.2f}%)")
    out.append("")

    out.append(f"## Top LAS mistakes where {model_a} wins")
    out.extend(_render_counter(b_errors_when_a_las_better, top_n))
    out.append("")

    out.append(f"## Top LAS mistakes where {model_a} loses to {model_b}")
    out.extend(_render_counter(a_errors_when_b_las_better, top_n))
    out.append("")

    out.append(f"## Top DEPREL mistakes where {model_a} wins")
    out.extend(_render_counter(b_errors_when_a_rel_better, top_n))
    out.append("")

    out.append(f"## Top DEPREL mistakes where {model_a} loses to {model_b}")
    out.extend(_render_counter(a_errors_when_b_rel_better, top_n))
    out.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote comparison report to {out_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two predicted CoNLL-U files against the same gold file.")
    parser.add_argument("gold", help="Path to gold CoNLL-U file.")
    parser.add_argument("pred_a", help="Path to model A prediction file.")
    parser.add_argument("pred_b", help="Path to model B prediction file.")
    parser.add_argument("out", help="Path to output Markdown file.")
    parser.add_argument("--model-a", default="ModelA", help="Name of model A.")
    parser.add_argument("--model-b", default="ModelB", help="Name of model B.")
    parser.add_argument("--top-n", type=int, default=20, help="Top N confusion rows per section.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    compare(
        gold_path=Path(args.gold),
        pred_a_path=Path(args.pred_a),
        pred_b_path=Path(args.pred_b),
        out_path=Path(args.out),
        model_a=args.model_a,
        model_b=args.model_b,
        top_n=args.top_n,
    )


if __name__ == "__main__":
    main()
