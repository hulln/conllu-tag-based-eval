#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Iterable, Sequence

try:
    import classla
except ModuleNotFoundError:
    classla = None


def iter_nonempty_lines(path: Path) -> Iterable[str]:
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            yield line


def parse_gold_alignment(path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    tokens: list[str] = []
    sent_text: str | None = None

    def flush() -> None:
        nonlocal tokens, sent_text
        if tokens:
            entries.append({"text": sent_text or " ".join(tokens), "tokens": tokens})
        tokens = []
        sent_text = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip("\n")
        if not line.strip():
            flush()
            continue

        if line.startswith("#"):
            if line.startswith("# text = "):
                sent_text = line[len("# text = ") :].strip()
            continue

        cols = line.split("\t")
        if len(cols) != 10:
            continue

        tok_id = cols[0]
        if "-" in tok_id or "." in tok_id:
            continue

        tokens.append(cols[1])

    flush()

    if not entries:
        raise ValueError(f"No tokenized sentence entries found in aligned gold file: {path}")

    return entries


def canonical_mode(mode: str) -> str:
    if mode in {"base", "raw", "unaligned"}:
        return "base"
    return "aligned"


def _safe_val(value: str | None, default: str = "") -> str:
    if value is None:
        return default
    text = value.strip()
    return text if text else default


def _infer_text_from_block(block_lines: Sequence[str]) -> str:
    forms: list[str] = []
    for line in block_lines:
        if not line.strip() or line.startswith("#"):
            continue
        cols = line.split("\t")
        if len(cols) != 10:
            continue
        tok_id = cols[0]
        if "-" in tok_id or "." in tok_id:
            continue
        forms.append(cols[1])
    return " ".join(forms)


def _normalize_sentence_block(block_text: str, sent_id: int, text_hint: str | None = None) -> str:
    raw_lines = [line for line in block_text.splitlines() if line.strip()]
    body_lines: list[str] = []
    existing_text: str | None = None

    for line in raw_lines:
        if line.startswith("# text = "):
            existing_text = line[len("# text = ") :].strip()
            continue
        if line.startswith("# sent_id = ") or line.startswith("# newpar"):
            continue
        body_lines.append(line)

    sent_text = _safe_val(text_hint, default=_safe_val(existing_text, default=_infer_text_from_block(body_lines)))

    lines = [f"# sent_id = {sent_id}"]
    if sent_text:
        lines.append(f"# text = {sent_text}")
    lines.extend(body_lines)
    return "\n".join(lines)


def run_aligned(
    nlp: Any,
    gold_entries: Sequence[dict[str, Any]],
    output_path: Path,
    progress_every: int,
) -> None:
    total = len(gold_entries)
    with output_path.open("w", encoding="utf-8") as out:
        for idx, entry in enumerate(gold_entries, start=1):
            tokenized_sent = entry["tokens"]
            text_fallback = _safe_val(entry.get("text"), default=" ".join(tokenized_sent))
            doc = nlp([tokenized_sent])

            sent_count = len(getattr(doc, "sentences", []) or [])
            if sent_count != 1:
                raise RuntimeError(
                    f"Aligned mode expected exactly 1 sentence for gold sentence {idx}, got {sent_count}"
                )

            block = _normalize_sentence_block(doc.to_conll().rstrip(), sent_id=idx, text_hint=text_fallback)
            out.write(block + "\n\n")

            if idx == 1:
                out.flush()
                print(f"[CLASSLA aligned] started sentence loop: {idx}/{total}")

            if progress_every > 0 and (idx % progress_every == 0 or idx == total):
                out.flush()
                print(f"[CLASSLA aligned] processed {idx}/{total} sentences")


def run_base(nlp: Any, lines: Iterable[str]) -> str:
    # Keep line breaks so model sentence splitting can differ from gold.
    text = "\n".join(lines)
    doc = nlp(text)
    blocks = [block for block in doc.to_conll().strip().split("\n\n") if block.strip()]
    normalized = [
        _normalize_sentence_block(block, sent_id=idx)
        for idx, block in enumerate(blocks, start=1)
    ]
    return "\n\n".join(normalized).strip() + "\n\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run CLASSLA and export CoNLL-U predictions.")
    parser.add_argument("--input", required=True, help="Path to raw sentence text file.")
    parser.add_argument("--output", default=None, help="Path to output CoNLL-U file for single-mode runs.")
    parser.add_argument(
        "--output-base",
        default=None,
        help="Output CoNLL-U path for base mode when --mode both is used.",
    )
    parser.add_argument(
        "--output-aligned",
        default=None,
        help="Output CoNLL-U path for aligned mode when --mode both is used.",
    )
    parser.add_argument(
        "--mode",
        choices=["aligned", "base", "raw", "unaligned", "both"],
        default="aligned",
        help=(
            "aligned = strict alignment to gold token boundaries via --aligned-gold; "
            "base/raw/unaligned = process full text and keep model sentence splitting; "
            "both = write base and aligned outputs in one run"
        ),
    )
    parser.add_argument(
        "--aligned-gold",
        default=None,
        help="Gold CoNLL-U file used to enforce strict token and sentence alignment in aligned mode.",
    )
    parser.add_argument("--lang", default="sl", help="CLASSLA language code (default: sl).")
    parser.add_argument(
        "--download-models",
        action="store_true",
        help="Download CLASSLA resources before running.",
    )
    parser.add_argument(
        "--no-lexicon",
        action="store_true",
        help="Disable lexicon-guided POS tagging (default is enabled).",
    )
    parser.add_argument(
        "--processors",
        default="tokenize,pos,lemma,depparse",
        help="CLASSLA processor list.",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=100,
        help="Print aligned-mode progress every N sentences (0 disables).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mode = canonical_mode(args.mode) if args.mode != "both" else "both"

    if classla is None:
        raise SystemExit(
            "Missing dependency: classla. Install requirements first, e.g. `pip install -r requirements.txt`."
        )

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else None
    output_base_path = Path(args.output_base) if args.output_base else None
    output_aligned_path = Path(args.output_aligned) if args.output_aligned else None

    if args.download_models:
        classla.download(args.lang)

    lines = list(iter_nonempty_lines(input_path))
    if not lines:
        raise ValueError(f"No non-empty input lines found in {input_path}")

    gold_entries: list[dict[str, Any]] = []
    if mode in {"aligned", "both"}:
        if not args.aligned_gold:
            raise ValueError("Aligned mode requires --aligned-gold for strict alignment.")

        gold_entries = parse_gold_alignment(Path(args.aligned_gold))
        if len(gold_entries) != len(lines):
            raise ValueError(
                "Strict aligned mode requires equal sentence counts between input and gold: "
                f"input={len(lines)} gold={len(gold_entries)}"
            )

    base_pipeline_kwargs = {
        "processors": args.processors,
        "pos_use_lexicon": not args.no_lexicon,
    }

    if mode == "both":
        if output_base_path is None or output_aligned_path is None:
            raise ValueError("Mode both requires --output-base and --output-aligned.")

        output_base_path.parent.mkdir(parents=True, exist_ok=True)
        output_aligned_path.parent.mkdir(parents=True, exist_ok=True)

        nlp_base = classla.Pipeline(args.lang, **base_pipeline_kwargs)
        conllu = run_base(nlp_base, lines)
        output_base_path.write_text(conllu, encoding="utf-8")
        print(f"[CLASSLA base] input lines: {len(lines)}")
        print(f"Wrote CLASSLA base prediction to {output_base_path}")

        aligned_pipeline_kwargs = dict(base_pipeline_kwargs)
        aligned_pipeline_kwargs["tokenize_pretokenized"] = True
        aligned_pipeline_kwargs["tokenize_no_ssplit"] = True

        nlp_aligned = classla.Pipeline(args.lang, **aligned_pipeline_kwargs)
        run_aligned(nlp_aligned, gold_entries, output_aligned_path, args.progress_every)
        print(f"Wrote CLASSLA aligned prediction to {output_aligned_path}")
        return

    pipeline_kwargs = dict(base_pipeline_kwargs)
    if mode == "aligned":
        # Strict alignment: consume gold tokenized sentences exactly as provided.
        pipeline_kwargs["tokenize_pretokenized"] = True
        pipeline_kwargs["tokenize_no_ssplit"] = True

    nlp = classla.Pipeline(args.lang, **pipeline_kwargs)

    if args.mode != mode:
        print(f"[CLASSLA] mode alias '{args.mode}' mapped to canonical mode '{mode}'")

    if output_path is None:
        raise ValueError("Single-mode runs require --output.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if mode == "aligned":
        run_aligned(nlp, gold_entries, output_path, args.progress_every)
        print(f"Wrote CLASSLA {mode} prediction to {output_path}")
        return

    conllu = run_base(nlp, lines)
    output_path.write_text(conllu, encoding="utf-8")
    print(f"[CLASSLA base] input lines: {len(lines)}")
    print(f"Wrote CLASSLA {mode} prediction to {output_path}")


if __name__ == "__main__":
    main()
