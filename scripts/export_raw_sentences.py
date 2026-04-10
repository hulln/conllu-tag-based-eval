#!/usr/bin/env python3
from pathlib import Path
import sys


def export_raw_sentences(gold_path: Path, out_path: Path) -> int:
    sentences = []
    for line in gold_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# text = "):
            sentences.append(line[len("# text = "):])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(sentences) + "\n", encoding="utf-8")
    return len(sentences)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: export_raw_sentences.py GOLD.conllu OUT.txt")
        raise SystemExit(2)

    gold_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    count = export_raw_sentences(gold_path, out_path)
    print(f"Exported {count} sentences to {out_path}")


if __name__ == "__main__":
    main()
