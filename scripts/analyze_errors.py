#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path


def read_conllu(path: Path):
    sentences = []
    tokens = []
    meta = {}

    def flush():
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
            # Skip malformed lines silently; evaluator already passed, so this is rare.
            continue
        tok_id = cols[0]
        if "-" in tok_id or "." in tok_id:
            # Skip multiword tokens and empty nodes.
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


def align_sentences(gold_sents, pred_sents):
    # Prefer direct index alignment if counts match and texts mostly match.
    if len(gold_sents) == len(pred_sents):
        text_matches = 0
        text_total = 0
        for g, p in zip(gold_sents, pred_sents):
            if g["text"] and p["text"]:
                text_total += 1
                if g["text"] == p["text"]:
                    text_matches += 1
        if text_total == 0 or text_matches / max(text_total, 1) >= 0.95:
            pairs = []
            for idx, (g, p) in enumerate(zip(gold_sents, pred_sents)):
                pairs.append((idx, g, idx, p))
            return pairs, [], []

    # Fallback: align by sentence text with FIFO matching.
    pred_by_text = defaultdict(list)
    for p_idx, p in enumerate(pred_sents):
        if p["text"]:
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


def analyze(gold_path: Path, pred_path: Path, out_path: Path, model_name: str, top_n: int):
    gold_sents = read_conllu(gold_path)
    pred_sents = read_conllu(pred_path)

    pairs, unmatched_gold, unmatched_pred = align_sentences(gold_sents, pred_sents)

    wrong_head_only = Counter()
    wrong_rel_only = Counter()
    wrong_both = Counter()
    totals = Counter()
    skipped_form_mismatch = 0
    skipped_len_mismatch_sentences = 0
    compared = 0

    for g_idx, g, _, p in pairs:
        g_tokens = g["tokens"]
        p_tokens = p["tokens"]
        if len(g_tokens) != len(p_tokens):
            skipped_len_mismatch_sentences += 1
            continue

        for gt, pt in zip(g_tokens, p_tokens):
            if gt["form"] != pt["form"]:
                skipped_form_mismatch += 1
                continue

            compared += 1
            g_head = gt["head"]
            p_head = pt["head"]
            g_rel = gt["deprel"]
            p_rel = pt["deprel"]

            head_ok = g_head == p_head
            rel_ok = g_rel == p_rel

            if head_ok:
                totals["head_correct"] += 1
            if rel_ok:
                totals["rel_correct"] += 1
            if head_ok and rel_ok:
                totals["las_correct"] += 1
                continue

            if not head_ok and rel_ok:
                wrong_head_only[g_rel] += 1
                totals["wrong_head_only"] += 1
            elif head_ok and not rel_ok:
                wrong_rel_only[(g_rel, p_rel)] += 1
                totals["wrong_rel_only"] += 1
            else:
                wrong_both[(g_rel, p_rel)] += 1
                totals["wrong_both"] += 1

    out = []
    out.append(f"# {model_name} error analysis (gold vs predicted)")
    out.append("")
    out.append(f"- Gold sentences: {len(gold_sents)}")
    out.append(f"- Pred sentences: {len(pred_sents)}")
    out.append(f"- Paired sentences: {len(pairs)}")
    out.append(f"- Unmatched gold sentences: {len(unmatched_gold)}")
    out.append(f"- Unmatched predicted sentences: {len(unmatched_pred)}")
    out.append(f"- Skipped sentence pairs (length mismatch): {skipped_len_mismatch_sentences}")
    out.append(f"- Tokens compared (form-aligned): {compared}")
    out.append(f"- Tokens skipped due to FORM mismatch: {skipped_form_mismatch}")
    out.append("")
    out.append("## Core accuracy on compared tokens")
    out.append(f"- UAS proxy (HEAD only): {totals['head_correct']}/{compared} = {_pct(totals['head_correct'], compared):.2f}%")
    out.append(f"- DEPREL accuracy: {totals['rel_correct']}/{compared} = {_pct(totals['rel_correct'], compared):.2f}%")
    out.append(f"- LAS proxy (HEAD+DEPREL): {totals['las_correct']}/{compared} = {_pct(totals['las_correct'], compared):.2f}%")
    out.append("")
    out.append("## Error buckets")
    out.append(f"- Wrong head only: {totals['wrong_head_only']}")
    out.append(f"- Wrong relation only: {totals['wrong_rel_only']}")
    out.append(f"- Wrong head and relation: {totals['wrong_both']}")
    out.append("")

    def render_top(title, counter):
        out.append(f"## {title}")
        out.append("")
        if not counter:
            out.append("(no items)")
            out.append("")
            return

        first = next(iter(counter.keys()))
        if isinstance(first, tuple):
            out.append("gold_deprel\tpred_deprel\tcount")
            for (g_rel, p_rel), c in counter.most_common(top_n):
                out.append(f"{g_rel}\t{p_rel}\t{c}")
        else:
            out.append("gold_deprel\tcount")
            for g_rel, c in counter.most_common(top_n):
                out.append(f"{g_rel}\t{c}")
        out.append("")

    render_top("Wrong head only (top)", wrong_head_only)
    render_top("Wrong relation only (top)", wrong_rel_only)
    render_top("Wrong head and relation (top)", wrong_both)

    out_path.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote analysis to {out_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze token-level HEAD/DEPREL errors from CoNLL-U files.")
    parser.add_argument("gold", help="Path to gold CoNLL-U file.")
    parser.add_argument("pred", help="Path to predicted CoNLL-U file.")
    parser.add_argument("out", help="Path to output Markdown report.")
    parser.add_argument("--model-name", default="Model", help="Label shown in the report title.")
    parser.add_argument("--top-n", type=int, default=20, help="Top N entries shown in each error table.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    analyze(
        gold_path=Path(args.gold),
        pred_path=Path(args.pred),
        out_path=Path(args.out),
        model_name=args.model_name,
        top_n=args.top_n,
    )


if __name__ == "__main__":
    main()
