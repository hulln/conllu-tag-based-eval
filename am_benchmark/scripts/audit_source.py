#!/usr/bin/env python3
"""Audit supplied CoNLL-U prediction files without modifying them."""

from __future__ import annotations

import hashlib
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


LANGUAGES = ("EN", "NL", "SL")
BENCHMARK_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = BENCHMARK_DIR / "source"
REPORT_PATH = BENCHMARK_DIR / "reports" / "source_audit.txt"

NUMBERED_COPY_RE = re.compile(r"^(?P<base>.+)\((?P<number>[0-9]+)\)\.conllu$")
ORDINARY_ID_RE = re.compile(r"^[1-9][0-9]*$")
MULTIWORD_ID_RE = re.compile(r"^(?P<start>[1-9][0-9]*)-(?P<end>[1-9][0-9]*)$")
EMPTY_NODE_ID_RE = re.compile(r"^(?:0|[1-9][0-9]*)\.[1-9][0-9]*$")
HEAD_RE = re.compile(r"^(?:0|[1-9][0-9]*)$")


def display_path(path: Path) -> str:
    """Return a stable path relative to am_benchmark."""
    return path.relative_to(BENCHMARK_DIR).as_posix()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def numbered_copy_match(path: Path) -> re.Match[str] | None:
    return NUMBERED_COPY_RE.match(path.name)


def is_clean_file(path: Path) -> bool:
    """Classify clean files after ignoring a final download-copy number."""
    match = numbered_copy_match(path)
    logical_name = match.group("base") if match else path.stem
    return logical_name.endswith("_clean")


def classify_token_id(token_id: str) -> str | None:
    if ORDINARY_ID_RE.fullmatch(token_id):
        return "ordinary"

    multiword_match = MULTIWORD_ID_RE.fullmatch(token_id)
    if multiword_match:
        start = int(multiword_match.group("start"))
        end = int(multiword_match.group("end"))
        if start < end:
            return "multiword"
        return None

    if EMPTY_NODE_ID_RE.fullmatch(token_id):
        return "empty"

    return None


def sentence_findings(
    rows: list[dict[str, object]], sentence_number: int, relative_path: str
) -> list[str]:
    """Check ordinary-token numbering and HEAD references in one sentence."""
    ordinary_rows = [row for row in rows if row["kind"] == "ordinary"]
    ordinary_ids = [int(row["id"]) for row in ordinary_rows]
    existing_ids = set(ordinary_ids)
    findings: list[str] = []

    duplicates = sorted(
        token_id for token_id, count in Counter(ordinary_ids).items() if count > 1
    )
    if duplicates:
        joined = ", ".join(str(token_id) for token_id in duplicates)
        findings.append(
            f"{relative_path}: sentence {sentence_number}: "
            f"duplicate ordinary ID(s): {joined}"
        )

    if ordinary_ids:
        missing_ids = sorted(set(range(1, max(ordinary_ids) + 1)) - existing_ids)
        if missing_ids:
            joined = ", ".join(str(token_id) for token_id in missing_ids)
            findings.append(
                f"{relative_path}: sentence {sentence_number}: "
                f"gap(s) in ordinary IDs; missing: {joined}"
            )

    for row in ordinary_rows:
        head = str(row["head"])
        if HEAD_RE.fullmatch(head) and head != "0" and int(head) not in existing_ids:
            findings.append(
                f"{relative_path}:{row['line']}: sentence {sentence_number}: "
                f"token {row['id']} has HEAD {head}, but ordinary ID {head} "
                "does not exist in the sentence"
            )

    return findings


def audit_file(path: Path) -> dict[str, object]:
    """Read and audit one file. The source file is never opened for writing."""
    relative_path = display_path(path)
    data = path.read_bytes()
    result: dict[str, object] = {
        "path": path,
        "relative_path": relative_path,
        "size": len(data),
        "sha256": sha256_bytes(data),
        "basic_errors": [],
        "structural_errors": [],
        "sentence_anomalies": [],
        "signature": None,
        "sentence_count": 0,
        "row_count": 0,
    }

    basic_errors = result["basic_errors"]
    structural_errors = result["structural_errors"]
    sentence_anomalies = result["sentence_anomalies"]
    assert isinstance(basic_errors, list)
    assert isinstance(structural_errors, list)
    assert isinstance(sentence_anomalies, list)

    if not data:
        basic_errors.append(f"{relative_path}: file is empty")

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        basic_errors.append(
            f"{relative_path}: not valid UTF-8 "
            f"(byte {error.start}: {error.reason})"
        )
        return result

    sentences: list[tuple[str, ...]] = []
    current_rows: list[dict[str, object]] = []
    current_signature: list[str] = []

    def finish_sentence() -> None:
        if not current_signature:
            return
        sentence_number = len(sentences) + 1
        sentences.append(tuple(current_signature))
        sentence_anomalies.extend(
            sentence_findings(current_rows, sentence_number, relative_path)
        )
        current_rows.clear()
        current_signature.clear()

    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            finish_sentence()
            continue
        if line.startswith("#"):
            continue

        columns = line.split("\t")
        if len(columns) != 10:
            basic_errors.append(
                f"{relative_path}:{line_number}: expected 10 tab-separated "
                f"columns, found {len(columns)}"
            )
            current_signature.append(f"<invalid-columns:{len(columns)}>")
            continue

        token_id = columns[0]
        head = columns[6]
        kind = classify_token_id(token_id)
        current_signature.append(token_id)
        result["row_count"] = int(result["row_count"]) + 1

        if kind is None:
            structural_errors.append(
                f"{relative_path}:{line_number}: invalid token ID {token_id!r}"
            )
            continue

        current_rows.append(
            {"id": token_id, "head": head, "kind": kind, "line": line_number}
        )

        if kind == "ordinary" and not HEAD_RE.fullmatch(head):
            structural_errors.append(
                f"{relative_path}:{line_number}: ordinary token {token_id} "
                f"has invalid HEAD {head!r}; expected a non-negative integer"
            )
        elif kind in {"multiword", "empty"} and head != "_":
            structural_errors.append(
                f"{relative_path}:{line_number}: {kind} row {token_id} "
                f"has HEAD {head!r}; expected '_'"
            )

    finish_sentence()
    result["signature"] = tuple(sentences)
    result["sentence_count"] = len(sentences)
    return result


def duplicate_groups(results: list[dict[str, object]]) -> list[tuple[str, list[Path]]]:
    by_hash: dict[str, list[Path]] = defaultdict(list)
    for result in results:
        by_hash[str(result["sha256"])].append(result["path"])
    return sorted(
        (
            (digest, sorted(paths, key=display_path))
            for digest, paths in by_hash.items()
            if len(paths) > 1
        ),
        key=lambda group: [display_path(path) for path in group[1]],
    )


def inventory(files: list[Path]) -> dict[str, int]:
    return {
        "total": len(files),
        "numbered": sum(numbered_copy_match(path) is not None for path in files),
        "raw": sum(not is_clean_file(path) for path in files),
        "clean": sum(is_clean_file(path) for path in files),
    }


def compare_numbered_copies(
    files: list[Path], results_by_path: dict[Path, dict[str, object]]
) -> list[dict[str, object]]:
    file_set = set(files)
    comparisons = []
    for path in files:
        match = numbered_copy_match(path)
        if not match:
            continue
        counterpart = path.with_name(f"{match.group('base')}.conllu")
        if counterpart not in file_set:
            status = "counterpart missing"
        elif results_by_path[path]["sha256"] == results_by_path[counterpart]["sha256"]:
            status = "identical"
        else:
            status = "different"
        comparisons.append(
            {"copy": path, "counterpart": counterpart, "status": status}
        )
    return comparisons


def find_cross_language_duplicates(
    language_results: dict[str, list[dict[str, object]]]
) -> list[tuple[str, list[tuple[str, Path]]]]:
    by_hash: dict[str, list[tuple[str, Path]]] = defaultdict(list)
    for language, results in language_results.items():
        for result in results:
            by_hash[str(result["sha256"])].append((language, result["path"]))

    groups = []
    for digest, entries in by_hash.items():
        if len({language for language, _ in entries}) > 1:
            groups.append(
                (digest, sorted(entries, key=lambda entry: (entry[0], display_path(entry[1]))))
            )
    return sorted(groups, key=lambda group: group[0])


def compare_raw_and_clean(
    files: list[Path], results_by_path: dict[Path, dict[str, object]]
) -> list[dict[str, object]]:
    file_set = set(files)
    comparisons = []

    for raw_path in files:
        if numbered_copy_match(raw_path) or is_clean_file(raw_path):
            continue
        clean_path = raw_path.with_name(f"{raw_path.stem}_clean.conllu")
        if clean_path not in file_set:
            continue

        raw_result = results_by_path[raw_path]
        clean_result = results_by_path[clean_path]
        identical = raw_result["sha256"] == clean_result["sha256"]
        if identical:
            structure = "identical"
        elif raw_result["signature"] is None or clean_result["signature"] is None:
            structure = "unavailable because at least one file is not UTF-8 readable"
        elif raw_result["signature"] == clean_result["signature"]:
            structure = "same"
        else:
            structure = "different"

        comparisons.append(
            {
                "raw": raw_path,
                "clean": clean_path,
                "identical": identical,
                "structure": structure,
                "raw_sentences": raw_result["sentence_count"],
                "clean_sentences": clean_result["sentence_count"],
                "raw_rows": raw_result["row_count"],
                "clean_rows": clean_result["row_count"],
            }
        )

    return sorted(comparisons, key=lambda item: display_path(item["raw"]))


def add_heading(lines: list[str], number: int, title: str) -> None:
    lines.extend([f"{number}. {title}", "=" * (len(title) + 3), ""])


def add_items(lines: list[str], items: list[str], empty_message: str) -> None:
    if items:
        lines.extend(f"- {item}" for item in items)
    else:
        lines.append(f"- {empty_message}")
    lines.append("")


def build_report(
    files_by_language: dict[str, list[Path]],
    language_results: dict[str, list[dict[str, object]]],
    within_duplicates: dict[str, list[tuple[str, list[Path]]]],
    numbered_comparisons: dict[str, list[dict[str, object]]],
    cross_duplicates: list[tuple[str, list[tuple[str, Path]]]],
    raw_clean_comparisons: list[dict[str, object]],
) -> str:
    all_results = [
        result for language in LANGUAGES for result in language_results[language]
    ]
    basic_errors = [
        error for result in all_results for error in result["basic_errors"]
    ]
    structural_errors = [
        error for result in all_results for error in result["structural_errors"]
    ]
    sentence_anomalies = [
        anomaly for result in all_results for anomaly in result["sentence_anomalies"]
    ]
    lines = [
        "CoNLL-U Source Audit",
        "====================",
        "",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Source root: {display_path(SOURCE_DIR)}",
        "Source files were read only; the audit performs no rewriting or cleanup.",
        "",
    ]

    add_heading(lines, 1, "Overall summary")
    lines.append(f"Total .conllu files: {len(all_results)}")
    for language in LANGUAGES:
        counts = inventory(files_by_language[language])
        lines.append(
            f"{language}: {counts['total']} total; {counts['numbered']} numbered copies; "
            f"{counts['raw']} raw; {counts['clean']} clean"
        )
    lines.extend(
        [
            f"Basic validity errors: {len(basic_errors)}",
            f"Token-ID/HEAD structural errors: {len(structural_errors)}",
            f"Sentence-level structural anomalies: {len(sentence_anomalies)}",
            "Within-language duplicate hash groups: "
            f"{sum(len(groups) for groups in within_duplicates.values())}",
            f"Cross-language duplicate hash groups: {len(cross_duplicates)}",
            f"Raw/clean pairs: {len(raw_clean_comparisons)}",
            "",
            "Inventory note: numbered-copy status overlaps with raw/clean status. "
            "For example, foo_clean(1).conllu is both numbered and clean.",
            "",
        ]
    )

    for section_number, language in enumerate(LANGUAGES, start=2):
        add_heading(lines, section_number, language)
        counts = inventory(files_by_language[language])
        lines.extend(
            [
                "File inventory:",
                f"- Total .conllu files: {counts['total']}",
                f"- Numbered download-copy files: {counts['numbered']}",
                f"- Raw files: {counts['raw']}",
                f"- Clean files: {counts['clean']}",
                "",
                "Exact duplicate groups within the language:",
            ]
        )
        groups = within_duplicates[language]
        if groups:
            for digest, paths in groups:
                lines.append(f"- SHA-256 {digest}")
                lines.extend(f"  - {display_path(path)}" for path in paths)
        else:
            lines.append("- None")
        lines.extend(["", "Numbered download-copy comparisons:"])
        comparisons = numbered_comparisons[language]
        if comparisons:
            for comparison in comparisons:
                lines.append(
                    f"- {display_path(comparison['copy'])} -> "
                    f"{display_path(comparison['counterpart'])}: {comparison['status']}"
                )
        else:
            lines.append("- None")

        lines.extend(["", "Basic file validity errors:"])
        language_basic_errors = [
            error
            for result in language_results[language]
            for error in result["basic_errors"]
        ]
        add_items(lines, language_basic_errors, "None")

    add_heading(lines, 5, "Cross-language duplicate hashes")
    if cross_duplicates:
        for digest, entries in cross_duplicates:
            lines.append(f"- SHA-256 {digest}")
            for language, path in entries:
                lines.append(f"  - {language}: {display_path(path)}")
    else:
        lines.append("- None")
    lines.append("")

    add_heading(lines, 6, "Raw-vs-clean differences")
    if raw_clean_comparisons:
        for comparison in raw_clean_comparisons:
            byte_status = "identical" if comparison["identical"] else "different"
            lines.extend(
                [
                    f"- {display_path(comparison['raw'])}",
                    f"  clean: {display_path(comparison['clean'])}",
                    f"  bytes: {byte_status}",
                    f"  basic sentence/token structure: {comparison['structure']}",
                ]
            )
            if not comparison["identical"]:
                lines.append(
                    "  counts: "
                    f"raw={comparison['raw_sentences']} sentences/"
                    f"{comparison['raw_rows']} token rows; "
                    f"clean={comparison['clean_sentences']} sentences/"
                    f"{comparison['clean_rows']} token rows"
                )
    else:
        lines.append("- No unnumbered raw/clean pairs found")
    lines.append("")

    add_heading(lines, 7, "Structural anomalies")
    lines.extend(
        [
            "Token-ID and HEAD errors:",
            "These violate the row-level structural rules used by this audit.",
        ]
    )
    add_items(lines, structural_errors, "None")
    lines.extend(
        [
            "Sentence-level warnings:",
            "These are observations, not automatic claims that a source file is corrupt.",
        ]
    )
    add_items(lines, sentence_anomalies, "None")
    return "\n".join(lines).rstrip() + "\n"


def print_terminal_summary(
    files_by_language: dict[str, list[Path]],
    language_results: dict[str, list[dict[str, object]]],
    within_duplicates: dict[str, list[tuple[str, list[Path]]]],
    cross_duplicates: list[tuple[str, list[tuple[str, Path]]]],
    raw_clean_comparisons: list[dict[str, object]],
) -> None:
    all_results = [
        result for language in LANGUAGES for result in language_results[language]
    ]
    error_count = sum(
        len(result["basic_errors"]) + len(result["structural_errors"])
        for result in all_results
    )
    anomaly_count = sum(len(result["sentence_anomalies"]) for result in all_results)
    different_raw_clean = sum(
        not comparison["identical"] for comparison in raw_clean_comparisons
    )

    print("CoNLL-U source audit complete")
    print(f"Scanned {len(all_results)} .conllu files")
    for language in LANGUAGES:
        counts = inventory(files_by_language[language])
        print(
            f"  {language}: {counts['total']} total, {counts['numbered']} numbered, "
            f"{counts['raw']} raw, {counts['clean']} clean"
        )
    print(f"Errors: {error_count}")
    print(f"Sentence-level structural anomaly observations: {anomaly_count}")
    print(
        "Within-language duplicate hash groups: "
        f"{sum(len(groups) for groups in within_duplicates.values())}"
    )
    print(f"Cross-language duplicate hash groups: {len(cross_duplicates)}")
    print(
        f"Raw/clean pairs: {len(raw_clean_comparisons)} "
        f"({different_raw_clean} byte-different)"
    )
    print(f"Detailed report: {display_path(REPORT_PATH)}")


def main() -> int:
    missing_directories = [
        SOURCE_DIR / language
        for language in LANGUAGES
        if not (SOURCE_DIR / language).is_dir()
    ]
    if missing_directories:
        print("Cannot run source audit; missing input directories:", file=sys.stderr)
        for path in missing_directories:
            print(f"  {path}", file=sys.stderr)
        return 2

    files_by_language = {
        language: sorted(
            (SOURCE_DIR / language).rglob("*.conllu"), key=display_path
        )
        for language in LANGUAGES
    }
    language_results = {
        language: [audit_file(path) for path in files_by_language[language]]
        for language in LANGUAGES
    }
    all_results = [
        result for language in LANGUAGES for result in language_results[language]
    ]
    results_by_path = {result["path"]: result for result in all_results}
    within_duplicates = {
        language: duplicate_groups(language_results[language])
        for language in LANGUAGES
    }
    numbered_comparisons = {
        language: compare_numbered_copies(
            files_by_language[language], results_by_path
        )
        for language in LANGUAGES
    }
    cross_duplicates = find_cross_language_duplicates(language_results)
    raw_clean_comparisons = []
    for language in LANGUAGES:
        raw_clean_comparisons.extend(
            compare_raw_and_clean(files_by_language[language], results_by_path)
        )

    report = build_report(
        files_by_language,
        language_results,
        within_duplicates,
        numbered_comparisons,
        cross_duplicates,
        raw_clean_comparisons,
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print_terminal_summary(
        files_by_language,
        language_results,
        within_duplicates,
        cross_duplicates,
        raw_clean_comparisons,
    )

    has_errors = any(
        result["basic_errors"] or result["structural_errors"]
        for result in all_results
    )
    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
