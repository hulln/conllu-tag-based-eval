#!/usr/bin/env python3

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

# stanza (and torch) are imported inside main() so the CoNLL-U helpers can be
# imported and tested without the Stanza environment.

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
    parser.add_argument(
        "--require-gpu",
        action="store_true",
        help="Abort instead of silently falling back to CPU when CUDA is unavailable.",
    )
    parser.add_argument(
        "--provenance-out",
        default=None,
        help="Optional JSON file recording library versions, device, offline flags and the "
        "SHA-256 of every model file the pipeline reports loading.",
    )
    return parser.parse_args()

def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()

def collect_model_paths(nlp):
    """Best-effort: gather '*_path' settings from the pipeline and its processors.

    Attribute names differ between Stanza releases, so nothing here may fail
    the run; whatever is found is recorded with its SHA-256.
    """
    found = {}
    configs = []
    for attr in ("config", "_config"):
        cfg = getattr(nlp, attr, None)
        if isinstance(cfg, dict):
            configs.append(("pipeline", cfg))
    processors = getattr(nlp, "processors", None)
    if isinstance(processors, dict):
        for name, proc in processors.items():
            for attr in ("config", "_config"):
                cfg = getattr(proc, attr, None)
                if isinstance(cfg, dict):
                    configs.append((name, cfg))
    for owner, cfg in configs:
        for key, value in cfg.items():
            if key.endswith("_path") and isinstance(value, str) and os.path.isfile(value):
                found[f"{owner}:{key}"] = {"path": value, "sha256": sha256_file(value)}
    return found

def write_provenance(path, args, stanza, torch, nlp, gold_path, output_path, n_sentences):
    record = {
        "argv": sys.argv,
        "package": args.package,
        "stanza_version": stanza.__version__,
        "torch_version": torch.__version__,
        "torch_cuda_version": getattr(torch.version, "cuda", None),
        "cuda_available": torch.cuda.is_available(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "env": {key: os.environ.get(key) for key in (
            "STANZA_RESOURCES_DIR", "HF_HOME", "HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE", "TORCH_HOME")},
        "gold": {"path": str(gold_path), "sha256": sha256_file(gold_path)},
        "output": {"path": str(output_path), "sha256": sha256_file(output_path)},
        "sentences": n_sentences,
        "loaded_model_files": collect_model_paths(nlp),
    }
    try:
        import transformers
        record["transformers_version"] = transformers.__version__
    except ImportError:
        record["transformers_version"] = None
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote provenance to {path}")

def main():
    args = parse_args()

    import stanza
    import torch

    if args.require_gpu and not torch.cuda.is_available():
        raise SystemExit("--require-gpu was given but torch.cuda.is_available() is False")

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

    if args.provenance_out:
        write_provenance(args.provenance_out, args, stanza, torch, nlp, gold_path, output_path, len(sentences))


if __name__ == "__main__":
    main()
