#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def read_sent_ids(path: Path) -> list[str]:
    ids = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not ids:
        raise ValueError(f"No sentence IDs found in {path}")
    return ids


def read_blocks_by_sent_id(path: Path) -> dict[str, str]:
    blocks: dict[str, str] = {}
    current: list[str] = []
    current_id = ""

    def flush() -> None:
        nonlocal current, current_id
        if current and current_id:
            blocks[current_id] = "\n".join(current).rstrip() + "\n"
        current = []
        current_id = ""

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip("\n")
        if not line.strip():
            flush()
            continue
        current.append(line)
        if line.startswith("# sent_id = "):
            current_id = line[len("# sent_id = ") :].strip()

    flush()
    return blocks


def write_selected(source: Path, sent_ids: list[str], output: Path, label: str) -> None:
    blocks = read_blocks_by_sent_id(source)
    missing = [sent_id for sent_id in sent_ids if sent_id not in blocks]
    if missing:
        raise ValueError(f"{label}: missing selected sentence IDs in {source}: {missing}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(blocks[sent_id] for sent_id in sent_ids) + "\n", encoding="utf-8")
    print(f"{label}: wrote {len(sent_ids)} selected sentences to {output}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract the random-20 demo files from existing full-run files.")
    parser.add_argument("--sent-ids", required=True, type=Path)
    parser.add_argument("--gold-source", required=True, type=Path)
    parser.add_argument("--classla-source", required=True, type=Path)
    parser.add_argument("--trankit-source", required=True, type=Path)
    parser.add_argument("--gold-out", required=True, type=Path)
    parser.add_argument("--classla-out", required=True, type=Path)
    parser.add_argument("--trankit-out", required=True, type=Path)
    args = parser.parse_args()

    sent_ids = read_sent_ids(args.sent_ids)
    print("Extracting these sentence IDs:")
    for index, sent_id in enumerate(sent_ids, start=1):
        print(f"{index:02d}. {sent_id}")

    write_selected(args.gold_source, sent_ids, args.gold_out, "gold")
    write_selected(args.classla_source, sent_ids, args.classla_out, "CLASSLA")
    write_selected(args.trankit_source, sent_ids, args.trankit_out, "Trankit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
