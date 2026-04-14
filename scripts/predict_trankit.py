#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

try:
    from trankit import Pipeline
except ModuleNotFoundError:
    Pipeline = None


def _download_zip(url: str, target_path: Path, timeout_seconds: int = 30) -> None:
    import ssl
    from urllib.request import Request, urlopen

    request = Request(url, headers={"User-Agent": "conllu-tag-based-eval/1.0"})
    ssl_context = ssl.create_default_context()
    with urlopen(request, timeout=timeout_seconds, context=ssl_context) as response:
        with target_path.open("wb") as out_f:
            shutil.copyfileobj(response, out_f, length=1024 * 1024)


def _safe_extract_zip(zip_path: Path, target_dir: Path) -> None:
    target_root = target_dir.resolve()
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            member_path = Path(member.filename)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise RuntimeError(f"Unsafe zip entry in Trankit model archive: {member.filename}")

            resolved_member = (target_root / member_path).resolve()
            if resolved_member != target_root and target_root not in resolved_member.parents:
                raise RuntimeError(f"Zip entry escapes target directory: {member.filename}")

        archive.extractall(target_dir)


def _trankit_model_ready(lang_dir: Path, language: str) -> bool:
    required_files = [
        lang_dir / f"{language}.tokenizer.mdl",
        lang_dir / f"{language}.tagger.mdl",
    ]
    return all(path.exists() for path in required_files)


def ensure_trankit_model(language: str, cache_dir: str | None) -> str:
    from trankit.utils.tbinfo import saved_model_version

    embedding_name = "xlm-roberta-base"
    effective_cache_dir = cache_dir or "cache/trankit"
    lang_dir = Path(effective_cache_dir) / embedding_name / language
    marker = lang_dir / f"{language}.downloaded"

    if _trankit_model_ready(lang_dir, language):
        marker.write_text("", encoding="utf-8")
        return effective_cache_dir

    marker.unlink(missing_ok=True)

    lang_dir.mkdir(parents=True, exist_ok=True)

    urls = [
        f"https://nlp.uoregon.edu/download/trankit/{saved_model_version}/{embedding_name}/{language}.zip",
        f"https://huggingface.co/uonlp/trankit/resolve/main/models/{saved_model_version}/{embedding_name}/{language}.zip",
    ]

    failures: List[str] = []
    for url in urls:
        temp_zip_path: Path | None = None
        try:
            print(f"[Trankit] attempting model download: {url}")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".zip", dir=str(lang_dir)) as tmp_f:
                temp_zip_path = Path(tmp_f.name)

            _download_zip(url, temp_zip_path)
            _safe_extract_zip(temp_zip_path, lang_dir)
            if not _trankit_model_ready(lang_dir, language):
                raise RuntimeError(f"Downloaded archive did not produce the expected Trankit model files in {lang_dir}")
            marker.write_text("", encoding="utf-8")
            print(f"[Trankit] model cache ready: {lang_dir}")
            temp_zip_path.unlink(missing_ok=True)
            return effective_cache_dir
        except Exception as exc:
            failures.append(f"{url} -> {exc}")
            if temp_zip_path is not None:
                temp_zip_path.unlink(missing_ok=True)

    raise RuntimeError(
        "Unable to download Trankit language model from configured sources:\n"
        + "\n".join(failures)
    )


def iter_nonempty_lines(path: Path) -> Iterable[str]:
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            yield line


def parse_gold_alignment(path: Path) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    tokens: List[str] = []
    sent_text: str | None = None
    sent_id: str | None = None
    comment_lines: List[str] = []

    def flush() -> None:
        nonlocal tokens, sent_text, sent_id, comment_lines
        if tokens:
            entries.append(
                {
                    "sent_id": sent_id or str(len(entries) + 1),
                    "text": sent_text or " ".join(tokens),
                    "tokens": tokens,
                    "comments": comment_lines,
                }
            )
        tokens = []
        sent_text = None
        sent_id = None
        comment_lines = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip("\n")
        if not line.strip():
            flush()
            continue

        if line.startswith("#"):
            comment_lines.append(line)
            if line.startswith("# sent_id = "):
                sent_id = line[len("# sent_id = ") :].strip()
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


def _safe_val(value, default: str = "_") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def _token_form(token: Dict) -> str:
    return _safe_val(token.get("text") or token.get("form"))


def _token_lemma(token: Dict) -> str:
    return _safe_val(token.get("lemma"))


def _token_upos(token: Dict) -> str:
    return _safe_val(token.get("upos"))


def _token_xpos(token: Dict) -> str:
    return _safe_val(token.get("xpos"))


def _token_feats(token: Dict) -> str:
    feats = token.get("feats")
    if isinstance(feats, dict):
        if not feats:
            return "_"
        return "|".join(f"{k}={v}" for k, v in sorted(feats.items()))
    return _safe_val(feats)


def _token_head(token: Dict) -> str:
    head = token.get("head")
    if head is None:
        return "_"
    return str(head)


def _token_deprel(token: Dict) -> str:
    return _safe_val(token.get("deprel"))


def _word_line(idx: int, token: Dict) -> str:
    return "\t".join(
        [
            str(idx),
            _token_form(token),
            _token_lemma(token),
            _token_upos(token),
            _token_xpos(token),
            _token_feats(token),
            _token_head(token),
            _token_deprel(token),
            "_",
            "_",
        ]
    )


def _sentence_to_conllu(
    sentence: Dict,
    sent_id: str | int,
    text_fallback: str,
    extra_comments: Sequence[str] | None = None,
) -> str:
    lines: List[str] = []
    sent_text = _safe_val(sentence.get("text"), default=text_fallback)

    comment_lines = list(extra_comments or [])
    wrote_sent_id = False
    wrote_text = False
    for line in comment_lines:
        if line.startswith("# sent_id = "):
            lines.append(f"# sent_id = {sent_id}")
            wrote_sent_id = True
        elif line.startswith("# text = "):
            lines.append(f"# text = {sent_text}")
            wrote_text = True
        else:
            lines.append(line)

    if not wrote_sent_id:
        lines.append(f"# sent_id = {sent_id}")
    if not wrote_text:
        lines.append(f"# text = {sent_text}")

    running_id = 1
    tokens = sentence.get("tokens", [])
    for token in tokens:
        expanded = token.get("expanded") or []
        if expanded:
            start_id = running_id
            end_id = start_id + len(expanded) - 1
            lines.append(
                "\t".join(
                    [
                        f"{start_id}-{end_id}",
                        _token_form(token),
                        "_",
                        "_",
                        "_",
                        "_",
                        "_",
                        "_",
                        "_",
                        "_",
                    ]
                )
            )
            for word in expanded:
                lines.append(_word_line(running_id, word))
                running_id += 1
        else:
            lines.append(_word_line(running_id, token))
            running_id += 1

    return "\n".join(lines)


def _normalize_doc_output(obj, text_fallback: str) -> List[Dict]:
    # Trankit returns either a sentence dict or a doc dict with a sentences list.
    if isinstance(obj, dict) and "sentences" in obj:
        return obj.get("sentences", [])
    if isinstance(obj, dict) and "tokens" in obj:
        return [obj]
    raise ValueError("Unexpected Trankit output format; expected dict with sentences or tokens.")


def _validate_conllu_text(conllu_text: str, label: str) -> None:
    for line_no, line in enumerate(conllu_text.splitlines(), start=1):
        if not line.strip() or line.startswith("#"):
            continue
        if len(line.split("\t")) != 10:
            snippet = line if len(line) <= 200 else (line[:200] + "...")
            raise ValueError(f"{label}: malformed CoNLL-U line {line_no}: {snippet}")


def _sanitize_conllu_text(conllu_text: str) -> tuple[str, int]:
    sanitized_lines: List[str] = []
    bad_count = 0

    for line in conllu_text.splitlines():
        if not line.strip() or line.startswith("#"):
            sanitized_lines.append(line)
            continue

        if len(line.split("\t")) != 10:
            bad_count += 1
            sanitized_lines.append(f"# malformed_raw = {line}")
            continue

        sanitized_lines.append(line)

    # CoNLL-U files must end with an empty line.
    return "\n".join(sanitized_lines).strip() + "\n\n", bad_count


def run_aligned(
    pipeline: Any,
    gold_entries: Sequence[Dict[str, Any]],
    output_path: Path,
    progress_every: int,
) -> None:
    total = len(gold_entries)
    sent_id = 1
    with output_path.open("w", encoding="utf-8") as out_f:
        for idx, entry in enumerate(gold_entries, start=1):
            tokenized_sent = entry["tokens"]
            text_fallback = _safe_val(entry.get("text"), default=" ".join(tokenized_sent))
            sent_id = _safe_val(str(entry.get("sent_id")), default=str(idx))

            out = pipeline(tokenized_sent, is_sent=True)
            sentences = _normalize_doc_output(out, text_fallback)

            if len(sentences) != 1:
                raise RuntimeError(
                    f"Aligned mode expected exactly 1 sentence for gold sentence {idx}, got {len(sentences)}"
                )

            for sent in sentences:
                out_f.write(
                    _sentence_to_conllu(
                        sent,
                        sent_id,
                        text_fallback,
                        extra_comments=entry.get("comments"),
                    )
                    + "\n\n"
                )

            if idx == 1:
                out_f.flush()
                print(f"[Trankit aligned] started line loop: {idx}/{total}")

            if progress_every > 0 and (idx % progress_every == 0 or idx == total):
                out_f.flush()
                print(f"[Trankit aligned] processed {idx}/{total} input lines")


def _run_base_bulk(pipeline: Any, lines: Sequence[str], progress_every: int) -> str:
    text = "\n".join(lines)
    out = pipeline(text)
    sentences = _normalize_doc_output(out, text)

    blocks: List[str] = []
    for sent_id, sent in enumerate(sentences, start=1):
        blocks.append(_sentence_to_conllu(sent, sent_id, "_"))

        if progress_every > 0 and sent_id % progress_every == 0:
            print(f"[Trankit base] built {sent_id} output sentences")

    print(f"[Trankit base] input lines: {len(lines)}")
    print(f"[Trankit base] output sentences: {len(sentences)}")
    # CoNLL-U files must end with an empty line.
    return "\n\n".join(blocks).strip() + "\n\n"


def _run_base_linewise(pipeline: Any, lines: Sequence[str], progress_every: int) -> str:
    total = len(lines)
    sent_id = 1
    blocks: List[str] = []

    for idx, line in enumerate(lines, start=1):
        out = pipeline(line)
        sentences = _normalize_doc_output(out, line)
        for sent in sentences:
            blocks.append(_sentence_to_conllu(sent, sent_id, line))
            sent_id += 1

        if progress_every > 0 and (idx % progress_every == 0 or idx == total):
            print(f"[Trankit base linewise] processed {idx}/{total} input lines")

    print(f"[Trankit base linewise] input lines: {len(lines)}")
    print(f"[Trankit base linewise] output sentences: {sent_id - 1}")
    # CoNLL-U files must end with an empty line.
    return "\n\n".join(blocks).strip() + "\n\n"


def run_base(pipeline: Any, lines: Sequence[str], progress_every: int) -> str:
    conllu = _run_base_bulk(pipeline, lines, progress_every)
    try:
        _validate_conllu_text(conllu, "Trankit base bulk")
        return conllu
    except ValueError as exc:
        print(f"[Trankit base] bulk output validation failed: {exc}")

    sanitized, bad_count = _sanitize_conllu_text(conllu)
    if bad_count > 0:
        try:
            _validate_conllu_text(sanitized, "Trankit base sanitized")
            print(f"[Trankit base] sanitized {bad_count} malformed non-CoNLL lines")
            return sanitized
        except ValueError as exc:
            print(f"[Trankit base] sanitized output still invalid: {exc}")

    print("[Trankit base] retrying with line-wise fallback")

    conllu = _run_base_linewise(pipeline, lines, progress_every)
    _validate_conllu_text(conllu, "Trankit base linewise")
    return conllu


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Trankit and export CoNLL-U predictions.")
    parser.add_argument(
        "--input",
        default=None,
        help="Path to raw sentence text file. Required for base mode and mode=both.",
    )
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
    parser.add_argument("--lang", default="slovenian", help="Trankit language code (default: slovenian).")
    parser.add_argument("--cache-dir", default=None, help="Optional model cache directory.")
    parser.add_argument(
        "--gpu",
        action="store_true",
        help="Enable GPU in Trankit pipeline (default: CPU only).",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=100,
        help="Print progress every N lines/sentences (0 disables).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mode = canonical_mode(args.mode) if args.mode != "both" else "both"

    if Pipeline is None:
        raise SystemExit(
            "Missing dependency: trankit. Install requirements first, e.g. `pip install -r requirements.txt`."
        )

    output_path = Path(args.output) if args.output else None
    output_base_path = Path(args.output_base) if args.output_base else None
    output_aligned_path = Path(args.output_aligned) if args.output_aligned else None

    gold_entries: List[Dict[str, Any]] = []
    if mode in {"aligned", "both"}:
        if not args.aligned_gold:
            raise ValueError("Aligned mode requires --aligned-gold for strict alignment.")

        gold_entries = parse_gold_alignment(Path(args.aligned_gold))

    lines: List[str] = []
    if mode in {"base", "both"}:
        if not args.input:
            raise ValueError("Base mode requires --input.")

        input_path = Path(args.input)
        lines = list(iter_nonempty_lines(input_path))
        if not lines:
            raise ValueError(f"No non-empty input lines found in {input_path}")

    if mode == "both" and len(gold_entries) != len(lines):
        raise ValueError(
            "Mode both requires equal sentence counts between input and aligned gold: "
            f"input={len(lines)} gold={len(gold_entries)}"
        )

    # Ensure language package exists locally before Pipeline init. This avoids
    # hard failures when the default Trankit host is temporarily unreachable.
    effective_cache_dir = ensure_trankit_model(args.lang, args.cache_dir)

    pipeline = Pipeline(lang=args.lang, gpu=args.gpu, cache_dir=effective_cache_dir)

    if mode == "both":
        if output_base_path is None or output_aligned_path is None:
            raise ValueError("Mode both requires --output-base and --output-aligned.")

        output_base_path.parent.mkdir(parents=True, exist_ok=True)
        output_aligned_path.parent.mkdir(parents=True, exist_ok=True)

        conllu = run_base(pipeline, lines, args.progress_every)
        output_base_path.write_text(conllu, encoding="utf-8")
        print(f"Wrote Trankit base prediction to {output_base_path}")

        run_aligned(pipeline, gold_entries, output_aligned_path, args.progress_every)
        print(f"Wrote Trankit aligned prediction to {output_aligned_path}")
        return

    if args.mode != mode:
        print(f"[Trankit] mode alias '{args.mode}' mapped to canonical mode '{mode}'")

    if output_path is None:
        raise ValueError("Single-mode runs require --output.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if mode == "aligned":
        run_aligned(pipeline, gold_entries, output_path, args.progress_every)
        print(f"Wrote Trankit {mode} prediction to {output_path}")
        return

    conllu = run_base(pipeline, lines, args.progress_every)
    output_path.write_text(conllu, encoding="utf-8")
    print(f"Wrote Trankit {mode} prediction to {output_path}")


if __name__ == "__main__":
    main()
