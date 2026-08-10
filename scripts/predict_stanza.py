#!/usr/bin/env python3

import argparse
from pathlib import Path

import stanza

def read_gold(path: Path):
    sentences = []
    comments = []
    rows = []

    def flush():
        nonlocal comments, rows
        if rows:
            sentences.append((comments, rows))
        comments = []
        rows = []

    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            flush()
        elif line.startswith("#"):
            comments.append(line)
        else:
            cols = line.split("\t")
            if len(cols) == 10 and cols[0].isdigit():
                rows.append(cols)

    flush()
    return sentences

def predict_sentence(nlp, rows):
    tokens = [row[1] for row in rows]
    doc = nlp([tokens])

    if len(doc.sentences) != 1:
        raise RuntimeError(f"Expected 1 sentence, got {len(doc.sentences)}")

    words = doc.sentences[0].words
    if len(words) != len(rows):
        raise RuntimeError(
            f"Token count mismatch: gold={len(rows)} stanza={len(words)}"
        )

    return words

def predicted_rows(gold_rows, words):
    output = []

    for gold, word in zip(gold_rows, words):
        row = [
            gold[0],                 # ID
            gold[1],                 # FORM: keep gold token
            word.lemma or "_",
            word.upos or "_",
            word.xpos or "_",
            word.feats or "_",
            str(word.head),
            word.deprel or "_",
            "_",                     # DEPS: not predicted here
            gold[9],                 # preserve MISC (NER, SpaceAfter, etc.)
        ]
        output.append(row)

    return output

def write_sentence(out, comments, rows):
    for comment in comments:
        out.write(comment + "\n")
    for row in rows:
        out.write("\t".join(row) + "\n")
    out.write("\n")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Run Stanza on gold-tokenized CoNLL-U and export predictions."
    )
    parser.add_argument("--gold", required=True, help="Gold CoNLL-U file.")
    parser.add_argument("--output", required=True, help="Output prediction CoNLL-U file.")
    parser.add_argument(
        "--package",
        choices=["default", "default_accurate"],
        required=True,
        help="Stanza package to evaluate.",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=100,
        help="Print progress every N sentences.",
    )
    return parser.parse_args()

def main():
    args = parse_args()

    gold_path = Path(args.gold)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    sentences = read_gold(gold_path)

    print(f"Stanza version: {stanza.__version__}")
    print(f"Package: {args.package}")
    print(f"Sentences: {len(sentences)}")

    nlp = stanza.Pipeline(
        "sl",
        package=args.package,
        processors="tokenize,pos,lemma,depparse",
        tokenize_pretokenized=True,
        use_gpu=True,
        download_method=None,
    )

    with output_path.open("w", encoding="utf-8") as out:
        for i, (comments, gold_rows) in enumerate(sentences, start=1):
            words = predict_sentence(nlp, gold_rows)
            rows = predicted_rows(gold_rows, words)
            write_sentence(out, comments, rows)

            if args.progress_every > 0 and (
                i % args.progress_every == 0 or i == len(sentences)
            ):
                print(f"Processed {i}/{len(sentences)} sentences", flush=True)

    print(f"Wrote predictions to {output_path}")


if __name__ == "__main__":
    main()
