#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


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
                    "text": meta.get("text", ""),
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
        if not tok_id.isdigit():
            continue

        tokens.append(
            {
                "id": tok_id,
                "form": cols[1],
                "lemma": cols[2],
                "upos": cols[3],
                "xpos": cols[4],
                "feats": cols[5],
                "head": cols[6],
                "deprel": cols[7],
                "deps": cols[8],
                "misc": cols[9],
            }
        )

    flush()
    return sentences


def align_sentences(a_sents: List[Dict], b_sents: List[Dict]):
    if len(a_sents) == len(b_sents):
        text_total = 0
        text_matches = 0
        for a, b in zip(a_sents, b_sents):
            if a.get("text") and b.get("text"):
                text_total += 1
                if a["text"] == b["text"]:
                    text_matches += 1

        if text_total == 0 or text_matches / max(text_total, 1) >= 0.95:
            pairs = []
            for idx, (a, b) in enumerate(zip(a_sents, b_sents)):
                pairs.append((idx, a, idx, b))
            return pairs, [], []

    b_by_text: Dict[str, List[Tuple[int, Dict]]] = defaultdict(list)
    for b_idx, b in enumerate(b_sents):
        if b.get("text"):
            b_by_text[b["text"]].append((b_idx, b))

    pairs = []
    unmatched_a = []
    used_b = set()

    for a_idx, a in enumerate(a_sents):
        text = a.get("text", "")
        if text and b_by_text.get(text):
            b_idx, b = b_by_text[text].pop(0)
            pairs.append((a_idx, a, b_idx, b))
            used_b.add(b_idx)
        else:
            unmatched_a.append(a_idx)

    unmatched_b = [idx for idx in range(len(b_sents)) if idx not in used_b]
    return pairs, unmatched_a, unmatched_b


def pct(num: int, den: int) -> float:
    return 100.0 * num / den if den else 0.0


def render_counter(counter: Counter, top_n: int, header: str) -> List[str]:
    lines = [header]
    for (left, right), count in counter.most_common(top_n):
        lines.append(f"{left}\t{right}\t{count}")
    if len(lines) == 1:
        lines.append("(no items)")
    return lines


def compare_files(
    file_a: Path,
    file_b: Path,
    out_path: Path,
    name_a: str,
    name_b: str,
    top_n: int,
) -> None:
    a_sents = read_conllu(file_a)
    b_sents = read_conllu(file_b)

    hash_a = sha256_of_file(file_a)
    hash_b = sha256_of_file(file_b)
    byte_identical = hash_a == hash_b

    pairs, unmatched_a, unmatched_b = align_sentences(a_sents, b_sents)

    totals = Counter()
    field_diffs = Counter()
    deprel_diffs = Counter()
    head_diffs = Counter()
    sample_sentence_diffs = []

    fields = ["lemma", "upos", "xpos", "feats", "head", "deprel", "deps", "misc"]

    for a_idx, a_sent, b_idx, b_sent in pairs:
        a_tokens = a_sent["tokens"]
        b_tokens = b_sent["tokens"]

        sent_has_diff = False
        if len(a_tokens) != len(b_tokens):
            totals["sentence_len_mismatch"] += 1
            totals["extra_tokens"] += abs(len(a_tokens) - len(b_tokens))
            sent_has_diff = True

        compare_n = min(len(a_tokens), len(b_tokens))
        for i in range(compare_n):
            at = a_tokens[i]
            bt = b_tokens[i]

            if at["form"] != bt["form"]:
                totals["form_mismatch"] += 1
                sent_has_diff = True
                continue

            totals["compared_tokens"] += 1
            token_has_diff = False
            for field in fields:
                if at[field] != bt[field]:
                    field_diffs[field] += 1
                    token_has_diff = True

            if token_has_diff:
                totals["token_diff"] += 1
                sent_has_diff = True
                if at["deprel"] != bt["deprel"]:
                    deprel_diffs[(at["deprel"], bt["deprel"])] += 1
                if at["head"] != bt["head"]:
                    head_diffs[(at["head"], bt["head"])] += 1
            else:
                totals["token_identical"] += 1

        if sent_has_diff:
            totals["sentence_diff"] += 1
            if len(sample_sentence_diffs) < top_n:
                sample_sentence_diffs.append(
                    (
                        a_idx + 1,
                        b_idx + 1,
                        a_sent.get("sent_id") or "_",
                        len(a_tokens),
                        len(b_tokens),
                        a_sent.get("text", "")[:200],
                    )
                )
        else:
            totals["sentence_identical"] += 1

    out = []
    out.append(f"# CoNLL-U file comparison: {name_a} vs {name_b}")
    out.append("")
    out.append("## File identity")
    out.append(f"- {name_a} path: {file_a}")
    out.append(f"- {name_b} path: {file_b}")
    out.append(f"- {name_a} sha256: {hash_a}")
    out.append(f"- {name_b} sha256: {hash_b}")
    out.append(f"- Byte-identical: {'yes' if byte_identical else 'no'}")
    out.append("")

    out.append("## Sentence coverage")
    out.append(f"- {name_a} sentences: {len(a_sents)}")
    out.append(f"- {name_b} sentences: {len(b_sents)}")
    out.append(f"- Paired sentences: {len(pairs)}")
    out.append(f"- Unmatched {name_a} sentences: {len(unmatched_a)}")
    out.append(f"- Unmatched {name_b} sentences: {len(unmatched_b)}")
    out.append(f"- Paired sentences with token length mismatch: {totals['sentence_len_mismatch']}")
    out.append(f"- Paired sentences fully identical: {totals['sentence_identical']}")
    out.append(f"- Paired sentences with at least one difference: {totals['sentence_diff']}")
    out.append("")

    compared = totals["compared_tokens"]
    out.append("## Token comparison (paired sentences)")
    out.append(f"- Compared tokens (FORM-aligned): {compared}")
    out.append(f"- Tokens fully identical (all fields): {totals['token_identical']} ({pct(totals['token_identical'], compared):.2f}%)")
    out.append(f"- Tokens with any field difference: {totals['token_diff']} ({pct(totals['token_diff'], compared):.2f}%)")
    out.append(f"- Tokens skipped due to FORM mismatch: {totals['form_mismatch']}")
    out.append(f"- Extra tokens from sentence length mismatch: {totals['extra_tokens']}")
    out.append("")

    out.append("## Field-level differences")
    for field in fields:
        out.append(f"- {field}: {field_diffs[field]} ({pct(field_diffs[field], compared):.2f}% of compared tokens)")
    out.append("")

    out.append("## Top DEPREL changes")
    out.extend(render_counter(deprel_diffs, top_n, f"{name_a}_deprel\t{name_b}_deprel\tcount"))
    out.append("")

    out.append("## Top HEAD changes")
    out.extend(render_counter(head_diffs, top_n, f"{name_a}_head\t{name_b}_head\tcount"))
    out.append("")

    out.append("## Example differing sentence pairs")
    out.append("a_idx\tb_idx\ta_sent_id\ta_tokens\tb_tokens\ttext")
    if sample_sentence_diffs:
        for a_idx, b_idx, sent_id, a_len, b_len, text in sample_sentence_diffs:
            out.append(f"{a_idx}\t{b_idx}\t{sent_id}\t{a_len}\t{b_len}\t{text}")
    else:
        out.append("(no differing sentence pairs)")
    out.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote CoNLL-U comparison report to {out_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two CoNLL-U files and write a Markdown report.")
    parser.add_argument("file_a", help="Path to first CoNLL-U file.")
    parser.add_argument("file_b", help="Path to second CoNLL-U file.")
    parser.add_argument("out", help="Path to output Markdown report.")
    parser.add_argument("--name-a", default="FileA", help="Display name for first file.")
    parser.add_argument("--name-b", default="FileB", help="Display name for second file.")
    parser.add_argument("--top-n", type=int, default=20, help="Top N rows for difference tables.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    compare_files(
        file_a=Path(args.file_a),
        file_b=Path(args.file_b),
        out_path=Path(args.out),
        name_a=args.name_a,
        name_b=args.name_b,
        top_n=args.top_n,
    )


if __name__ == "__main__":
    main()
