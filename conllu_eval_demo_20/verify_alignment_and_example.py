#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def read_conllu(path: Path) -> list[dict[str, object]]:
    sentences: list[dict[str, object]] = []
    sent_id = ""
    text = ""
    tokens: list[dict[str, str]] = []

    def flush() -> None:
        nonlocal sent_id, text, tokens
        if tokens:
            sentences.append({"sent_id": sent_id, "text": text, "tokens": tokens})
        sent_id = ""
        text = ""
        tokens = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip("\n")
        if not line.strip():
            flush()
            continue
        if line.startswith("# sent_id = "):
            sent_id = line[len("# sent_id = ") :].strip()
            continue
        if line.startswith("# text = "):
            text = line[len("# text = ") :].strip()
            continue
        if line.startswith("#"):
            continue

        cols = line.split("\t")
        if len(cols) != 10:
            continue
        token_id = cols[0]
        if "-" in token_id or "." in token_id:
            continue

        tokens.append(
            {
                "id": token_id,
                "form": cols[1],
                "lemma": cols[2],
                "upos": cols[3],
                "xpos": cols[4],
                "head": cols[6],
                "deprel": cols[7].split(":", 1)[0],
                "raw_deprel": cols[7],
            }
        )

    flush()
    return sentences


def pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "n/a"
    return f"{100 * numerator / denominator:.2f}%"


def compare_model(
    gold: list[dict[str, object]],
    pred: list[dict[str, object]],
    label: str,
) -> tuple[bool, dict[str, int], list[str]]:
    ok = True
    issues: list[str] = []
    stats = {
        "sentences": len(gold),
        "tokens": 0,
        "sent_id_mismatches": 0,
        "token_count_mismatches": 0,
        "form_mismatches": 0,
        "upos_correct": 0,
        "uas_correct": 0,
        "las_correct": 0,
    }

    if len(gold) != len(pred):
        ok = False
        issues.append(f"{label}: sentence count mismatch: gold={len(gold)} pred={len(pred)}")

    for sent_index, (gold_sent, pred_sent) in enumerate(zip(gold, pred), start=1):
        gold_id = str(gold_sent["sent_id"])
        pred_id = str(pred_sent["sent_id"])
        gold_tokens = list(gold_sent["tokens"])  # type: ignore[arg-type]
        pred_tokens = list(pred_sent["tokens"])  # type: ignore[arg-type]

        if gold_id != pred_id:
            ok = False
            stats["sent_id_mismatches"] += 1
            issues.append(f"{label}: sentence {sent_index} ID mismatch: gold={gold_id} pred={pred_id}")

        if len(gold_tokens) != len(pred_tokens):
            ok = False
            stats["token_count_mismatches"] += 1
            issues.append(
                f"{label}: sentence {gold_id or sent_index} token count mismatch: "
                f"gold={len(gold_tokens)} pred={len(pred_tokens)}"
            )

        for token_index, (gold_tok, pred_tok) in enumerate(zip(gold_tokens, pred_tokens), start=1):
            stats["tokens"] += 1
            if gold_tok["form"] != pred_tok["form"]:
                ok = False
                stats["form_mismatches"] += 1
                issues.append(
                    f"{label}: {gold_id} token {token_index} form mismatch: "
                    f"gold={gold_tok['form']} pred={pred_tok['form']}"
                )
                continue

            if gold_tok["upos"] == pred_tok["upos"]:
                stats["upos_correct"] += 1
            if gold_tok["head"] == pred_tok["head"]:
                stats["uas_correct"] += 1
            if gold_tok["head"] == pred_tok["head"] and gold_tok["deprel"] == pred_tok["deprel"]:
                stats["las_correct"] += 1

    return ok, stats, issues


def choose_example(
    gold: list[dict[str, object]],
    classla: list[dict[str, object]],
    trankit: list[dict[str, object]],
) -> int:
    for index, (gold_sent, classla_sent, trankit_sent) in enumerate(zip(gold, classla, trankit)):
        gold_tokens = list(gold_sent["tokens"])  # type: ignore[arg-type]
        classla_tokens = list(classla_sent["tokens"])  # type: ignore[arg-type]
        trankit_tokens = list(trankit_sent["tokens"])  # type: ignore[arg-type]
        for gold_tok, classla_tok, trankit_tok in zip(gold_tokens, classla_tokens, trankit_tokens):
            classla_las_ok = gold_tok["head"] == classla_tok["head"] and gold_tok["deprel"] == classla_tok["deprel"]
            trankit_las_ok = gold_tok["head"] == trankit_tok["head"] and gold_tok["deprel"] == trankit_tok["deprel"]
            if not classla_las_ok or not trankit_las_ok:
                return index
    return 0


def print_stats(label: str, stats: dict[str, int]) -> None:
    tokens = stats["tokens"]
    print(f"\n{label}")
    print(f"sentences compared: {stats['sentences']}")
    print(f"tokens compared:    {tokens}")
    print(f"sent_id mismatches: {stats['sent_id_mismatches']}")
    print(f"token mismatches:   {stats['token_count_mismatches']}")
    print(f"form mismatches:    {stats['form_mismatches']}")
    print(f"UPOS correct:       {stats['upos_correct']}/{tokens} = {pct(stats['upos_correct'], tokens)}")
    print(f"UAS correct:        {stats['uas_correct']}/{tokens} = {pct(stats['uas_correct'], tokens)}")
    print(f"LAS correct:        {stats['las_correct']}/{tokens} = {pct(stats['las_correct'], tokens)}")


def print_example(
    gold: list[dict[str, object]],
    classla: list[dict[str, object]],
    trankit: list[dict[str, object]],
) -> None:
    index = choose_example(gold, classla, trankit)
    gold_sent = gold[index]
    classla_sent = classla[index]
    trankit_sent = trankit[index]
    gold_tokens = list(gold_sent["tokens"])  # type: ignore[arg-type]
    classla_tokens = list(classla_sent["tokens"])  # type: ignore[arg-type]
    trankit_tokens = list(trankit_sent["tokens"])  # type: ignore[arg-type]

    print("\nConcrete token-by-token example")
    print(f"sent_id: {gold_sent['sent_id']}")
    print(f"text: {gold_sent['text']}")
    print(
        "ID\tFORM\tGOLD_HEAD\tGOLD_DEPREL\t"
        "CLASSLA_HEAD\tCLASSLA_DEPREL\tCLASSLA_LAS_OK\t"
        "TRANKIT_HEAD\tTRANKIT_DEPREL\tTRANKIT_LAS_OK"
    )
    for gold_tok, classla_tok, trankit_tok in zip(gold_tokens, classla_tokens, trankit_tokens):
        classla_ok = gold_tok["head"] == classla_tok["head"] and gold_tok["deprel"] == classla_tok["deprel"]
        trankit_ok = gold_tok["head"] == trankit_tok["head"] and gold_tok["deprel"] == trankit_tok["deprel"]
        print(
            f"{gold_tok['id']}\t{gold_tok['form']}\t"
            f"{gold_tok['head']}\t{gold_tok['deprel']}\t"
            f"{classla_tok['head']}\t{classla_tok['deprel']}\t{classla_ok}\t"
            f"{trankit_tok['head']}\t{trankit_tok['deprel']}\t{trankit_ok}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Check demo gold/pred alignment and print one concrete example.")
    parser.add_argument("--gold", required=True, type=Path)
    parser.add_argument("--classla", required=True, type=Path)
    parser.add_argument("--trankit", required=True, type=Path)
    args = parser.parse_args()

    gold = read_conllu(args.gold)
    classla = read_conllu(args.classla)
    trankit = read_conllu(args.trankit)

    print("Alignment rule used in this demo:")
    print("1. The gold and prediction files must contain the same sentence IDs in the same order.")
    print("2. Each matched sentence must contain the same number of real tokens.")
    print("3. Each matched token must have the same FORM text.")
    print("4. Only then do we compare UPOS, HEAD, and DEPREL values.")

    all_ok = True
    for label, pred in [("CLASSLA", classla), ("Trankit", trankit)]:
        ok, stats, issues = compare_model(gold, pred, label)
        all_ok = all_ok and ok
        print_stats(label, stats)
        if issues:
            print(f"\nFirst {label} alignment issues:")
            for issue in issues[:10]:
                print(f"- {issue}")

    if all_ok:
        print("\nAlignment verdict: OK. The files compare the same examples and same token forms.")
    else:
        print("\nAlignment verdict: FAILED. Do not trust metrics until this is fixed.")

    print_example(gold, classla, trankit)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
