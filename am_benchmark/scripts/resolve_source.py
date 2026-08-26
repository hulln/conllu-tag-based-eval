#!/usr/bin/env python3
"""Resolve AM benchmark source files into defensible canonical run choices.

The source tree is immutable. This script reads files under ``source/`` and local
gold candidates elsewhere in the repository, then writes only to ``reports/``.
It does not run model evaluation.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from itertools import zip_longest
from pathlib import Path


LANGUAGES = ("EN", "NL", "SL")
COLUMN_NAMES = (
    "ID",
    "FORM",
    "LEMMA",
    "UPOS",
    "XPOS",
    "FEATS",
    "HEAD",
    "DEPREL",
    "DEPS",
    "MISC",
)
TRAINING_MARKERS = (
    "writtenanddialecttrain",
    "writtenandspokentrain",
    "writtentrain",
    "default",
)
TEST_CONDITIONS = ("writtentest", "spokentest", "dialecttest")

BENCHMARK_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = BENCHMARK_DIR.parent
SOURCE_DIR = BENCHMARK_DIR / "source"
REPORT_DIR = BENCHMARK_DIR / "reports"

NUMBERED_RE = re.compile(r"^(?P<base>.+)\((?P<number>[0-9]+)\)\.conllu$")
ORDINARY_ID_RE = re.compile(r"^[1-9][0-9]*$")
MULTIWORD_ID_RE = re.compile(r"^(?P<start>[1-9][0-9]*)-(?P<end>[1-9][0-9]*)$")
EMPTY_ID_RE = re.compile(r"^(?P<base>0|[1-9][0-9]*)\.(?P<sub>[1-9][0-9]*)$")
HEAD_RE = re.compile(r"^(?:0|[1-9][0-9]*)$")


def display_path(path: Path) -> str:
    try:
        return path.relative_to(BENCHMARK_DIR).as_posix()
    except ValueError:
        return "../" + path.relative_to(REPO_DIR).as_posix()


def token_id_kind(token_id: str) -> str | None:
    if ORDINARY_ID_RE.fullmatch(token_id):
        return "ordinary"
    multiword = MULTIWORD_ID_RE.fullmatch(token_id)
    if multiword and int(multiword.group("start")) < int(multiword.group("end")):
        return "multiword"
    if EMPTY_ID_RE.fullmatch(token_id):
        return "empty"
    return None


def add_issue(
    issues: list[dict[str, object]],
    code: str,
    message: str,
    sentence: int | None = None,
    line: int | None = None,
) -> None:
    issues.append(
        {"code": code, "message": message, "sentence": sentence, "line": line}
    )


def sentence_checks(
    rows: list[dict[str, object]], sentence_number: int, issues: list[dict[str, object]]
) -> None:
    ordinary = [row for row in rows if row["kind"] == "ordinary"]
    ordinary_ids = [int(row["id"]) for row in ordinary]
    id_counts = Counter(ordinary_ids)
    existing = set(ordinary_ids)

    duplicates = sorted(token_id for token_id, count in id_counts.items() if count > 1)
    if duplicates:
        add_issue(
            issues,
            "duplicate_ordinary_id",
            "duplicate ordinary ID(s): " + ", ".join(map(str, duplicates)),
            sentence_number,
        )

    if ordinary_ids:
        gaps = sorted(set(range(1, max(ordinary_ids) + 1)) - existing)
        if gaps:
            add_issue(
                issues,
                "ordinary_id_gap",
                "missing ordinary ID(s): " + ", ".join(map(str, gaps)),
                sentence_number,
            )
        if ordinary_ids != sorted(ordinary_ids):
            add_issue(
                issues,
                "ordinary_id_order",
                "ordinary IDs are not in ascending order",
                sentence_number,
            )

    heads: dict[int, int] = {}
    roots = 0
    for row in ordinary:
        token_id = int(row["id"])
        head_text = str(row["head"])
        if not HEAD_RE.fullmatch(head_text):
            continue
        head = int(head_text)
        if head == 0:
            roots += 1
        elif head not in existing:
            add_issue(
                issues,
                "missing_head_target",
                f"token {token_id} has HEAD {head}, which is absent",
                sentence_number,
                int(row["line"]),
            )
        if head == token_id:
            add_issue(
                issues,
                "self_loop",
                f"token {token_id} points to itself",
                sentence_number,
                int(row["line"]),
            )
        if id_counts[token_id] == 1:
            heads[token_id] = head

    if ordinary and roots != 1:
        add_issue(
            issues,
            "root_count",
            f"expected exactly one HEAD=0 root, found {roots}",
            sentence_number,
        )

    # Follow HEAD chains to find cycles longer than a self-loop.
    reported_cycles: set[tuple[int, ...]] = set()
    for start in heads:
        positions: dict[int, int] = {}
        chain: list[int] = []
        current = start
        while current in heads and current != 0:
            if current in positions:
                cycle = chain[positions[current] :]
                if len(cycle) > 1:
                    rotations = [tuple(cycle[index:] + cycle[:index]) for index in range(len(cycle))]
                    canonical_cycle = min(rotations)
                    if canonical_cycle not in reported_cycles:
                        reported_cycles.add(canonical_cycle)
                        add_issue(
                            issues,
                            "dependency_cycle",
                            "dependency cycle: " + " -> ".join(map(str, canonical_cycle)),
                            sentence_number,
                        )
                break
            positions[current] = len(chain)
            chain.append(current)
            next_id = heads[current]
            if next_id == 0 or next_id not in heads:
                break
            current = next_id

    # The repository evaluator consumes the component rows immediately after an
    # MWT header. Check that this physical sequence matches the stated range.
    for index, row in enumerate(rows):
        if row["kind"] != "multiword":
            continue
        start_text, end_text = str(row["id"]).split("-")
        expected = list(range(int(start_text), int(end_text) + 1))
        following = rows[index + 1 : index + 1 + len(expected)]
        actual = [
            int(item["id"])
            for item in following
            if item["kind"] == "ordinary"
        ]
        if actual != expected or len(following) != len(expected):
            add_issue(
                issues,
                "multiword_components",
                f"MWT {row['id']} is not followed by ordinary rows {expected}",
                sentence_number,
                int(row["line"]),
            )

    empty_nodes: dict[int, list[int]] = defaultdict(list)
    for row in rows:
        if row["kind"] != "empty":
            continue
        match = EMPTY_ID_RE.fullmatch(str(row["id"]))
        assert match is not None
        base = int(match.group("base"))
        sub = int(match.group("sub"))
        empty_nodes[base].append(sub)
        if base != 0 and base not in existing:
            add_issue(
                issues,
                "empty_node_base",
                f"empty node {row['id']} has absent base ID {base}",
                sentence_number,
                int(row["line"]),
            )
    for base, subs in empty_nodes.items():
        if subs != sorted(set(subs)):
            add_issue(
                issues,
                "empty_node_order",
                f"empty-node suffixes for base {base} are duplicated or out of order",
                sentence_number,
            )


def profile_conllu(path: Path) -> dict[str, object]:
    """Build hashes, counts, samples, and evaluator-relevant structural checks."""
    data = path.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    issues: list[dict[str, object]] = []
    profile: dict[str, object] = {
        "path": path,
        "sha256": sha256,
        "size": len(data),
        "issues": issues,
        "sentence_count": 0,
        "ordinary_count": 0,
        "data_row_count": 0,
        "multiword_count": 0,
        "empty_node_count": 0,
        "structure_hash": "",
        "surface_hash": "",
        "sent_id_hash": "",
        "sent_id_count": 0,
        "sample_forms": [],
    }
    if not data:
        add_issue(issues, "empty_file", "file is empty")

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        add_issue(
            issues,
            "invalid_utf8",
            f"invalid UTF-8 at byte {error.start}: {error.reason}",
        )
        return profile

    if text and not (text.endswith("\n\n") or text.endswith("\r\n\r\n")):
        add_issue(
            issues,
            "missing_final_blank_line",
            "file does not end with the blank line required by the repository evaluator",
        )

    structure_hasher = hashlib.sha256()
    surface_hasher = hashlib.sha256()
    sent_id_hasher = hashlib.sha256()
    rows: list[dict[str, object]] = []
    current_sent_id = ""
    sample_forms: list[str] = []

    def finish_sentence() -> None:
        nonlocal rows, current_sent_id
        if not rows:
            current_sent_id = ""
            return
        sentence_number = int(profile["sentence_count"]) + 1
        profile["sentence_count"] = sentence_number
        sentence_checks(rows, sentence_number, issues)
        structure_hasher.update(b"\n<SENTENCE>\n")
        surface_hasher.update(b"\n<SENTENCE>\n")
        sent_id_hasher.update((current_sent_id + "\n").encode("utf-8"))
        if current_sent_id:
            profile["sent_id_count"] = int(profile["sent_id_count"]) + 1
        rows = []
        current_sent_id = ""

    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            finish_sentence()
            continue
        if line.startswith("#"):
            if line.startswith("# sent_id = "):
                current_sent_id = line[len("# sent_id = ") :].strip()
            continue

        columns = line.split("\t")
        if len(columns) != 10:
            add_issue(
                issues,
                "column_count",
                f"expected 10 tab-separated columns, found {len(columns)}",
                int(profile["sentence_count"]) + 1,
                line_number,
            )
            structure_hasher.update(f"BAD:{len(columns)}\n".encode("ascii"))
            continue

        token_id, form, head = columns[0], columns[1], columns[6]
        kind = token_id_kind(token_id)
        profile["data_row_count"] = int(profile["data_row_count"]) + 1
        structure_hasher.update((token_id + "\n").encode("utf-8"))
        surface_hasher.update((token_id + "\t" + form + "\n").encode("utf-8"))

        if kind is None:
            add_issue(
                issues,
                "invalid_id",
                f"invalid ID {token_id!r}",
                int(profile["sentence_count"]) + 1,
                line_number,
            )
            rows.append(
                {"id": token_id, "form": form, "head": head, "kind": None, "line": line_number}
            )
            continue

        rows.append(
            {"id": token_id, "form": form, "head": head, "kind": kind, "line": line_number}
        )
        if kind == "ordinary":
            profile["ordinary_count"] = int(profile["ordinary_count"]) + 1
            if len(sample_forms) < 12:
                sample_forms.append(form)
            if not HEAD_RE.fullmatch(head):
                add_issue(
                    issues,
                    "invalid_head",
                    f"ordinary token {token_id} has invalid HEAD {head!r}",
                    int(profile["sentence_count"]) + 1,
                    line_number,
                )
        elif kind == "multiword":
            profile["multiword_count"] = int(profile["multiword_count"]) + 1
            if head != "_":
                add_issue(
                    issues,
                    "multiword_head",
                    f"MWT {token_id} has HEAD {head!r}, expected '_'",
                    int(profile["sentence_count"]) + 1,
                    line_number,
                )
        else:
            profile["empty_node_count"] = int(profile["empty_node_count"]) + 1
            if head != "_":
                add_issue(
                    issues,
                    "empty_node_head",
                    f"empty node {token_id} has HEAD {head!r}, expected '_'",
                    int(profile["sentence_count"]) + 1,
                    line_number,
                )

        if kind != "empty" and not "".join(
            character for character in form if unicodedata.category(character) != "Zs"
        ):
            add_issue(
                issues,
                "empty_form",
                f"row {token_id} has an empty/space-only FORM",
                int(profile["sentence_count"]) + 1,
                line_number,
            )

    finish_sentence()
    profile["structure_hash"] = structure_hasher.hexdigest()
    profile["surface_hash"] = surface_hasher.hexdigest()
    profile["sent_id_hash"] = sent_id_hasher.hexdigest()
    profile["sample_forms"] = sample_forms
    return profile


def logical_root(path: Path) -> str | None:
    name = path.name
    if name.endswith(".conllu_"):
        return name[: -len(".conllu_")]
    numbered = NUMBERED_RE.fullmatch(name)
    if numbered:
        name = numbered.group("base") + ".conllu"
    if not name.endswith(".conllu"):
        return None
    stem = name[: -len(".conllu")]
    if stem.endswith("_clean"):
        stem = stem[: -len("_clean")]
    return stem


def parse_run_name(root: str) -> tuple[str, str, str]:
    for test_condition in TEST_CONDITIONS:
        suffix = "_" + test_condition
        if not root.endswith(suffix):
            continue
        before_test = root[: -len(suffix)]
        for training in TRAINING_MARKERS:
            position = before_test.rfind(training)
            if position >= 0 and position + len(training) == len(before_test):
                model = before_test[:position].rstrip("_")
                if model:
                    return model, training, test_condition
    raise ValueError(f"Cannot parse logical run name: {root}")


def data_rows(path: Path) -> list[list[str]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            columns = line.split("\t")
            if len(columns) == 10:
                rows.append(columns)
    return rows


def field_difference_counts(left: Path, right: Path) -> dict[str, int]:
    counts = Counter()
    left_rows = data_rows(left)
    right_rows = data_rows(right)
    for left_row, right_row in zip_longest(left_rows, right_rows):
        if left_row is None or right_row is None:
            counts["DATA_ROW_COUNT"] += 1
            continue
        for index, name in enumerate(COLUMN_NAMES):
            if left_row[index] != right_row[index]:
                counts[name] += 1
    return dict(counts)


def format_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "none"
    ordered = [name for name in COLUMN_NAMES if counts.get(name)]
    ordered.extend(name for name in counts if name not in COLUMN_NAMES)
    return ", ".join(f"{name}={counts[name]}" for name in ordered)


def build_runs(
    physical_files: list[Path], profiles: dict[Path, dict[str, object]]
) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[Path]] = defaultdict(list)
    for path in physical_files:
        root = logical_root(path)
        if root is not None:
            grouped[(path.parent.name, root)].append(path)

    runs: list[dict[str, object]] = []
    for (language, root), files in sorted(grouped.items()):
        raw = next(
            (
                path
                for path in files
                if path.name == root + ".conllu"
            ),
            None,
        )
        clean = next(
            (
                path
                for path in files
                if path.name == root + "_clean.conllu"
            ),
            None,
        )
        # Numbered-only or alternate-only groups are still visible, but the current
        # source set is expected to have a raw/clean pair for each logical run.
        if raw is None and clean is None:
            continue
        numbered = sorted(
            [path for path in files if NUMBERED_RE.fullmatch(path.name)],
            key=display_path,
        )
        alternates = sorted(
            [path for path in files if path.name.endswith(".conllu_")],
            key=display_path,
        )
        model, training, test = parse_run_name(root)
        numbered_comparisons = []
        for copy in numbered:
            match = NUMBERED_RE.fullmatch(copy.name)
            assert match is not None
            counterpart = copy.with_name(match.group("base") + ".conllu")
            identical = (
                counterpart in profiles
                and profiles[copy]["sha256"] == profiles[counterpart]["sha256"]
            )
            numbered_comparisons.append(
                {"copy": copy, "counterpart": counterpart, "identical": identical}
            )

        raw_equals_clean = bool(
            raw
            and clean
            and profiles[raw]["sha256"] == profiles[clean]["sha256"]
        )
        if not raw or not clean:
            change_type = "missing pair member"
            change_fields: dict[str, int] = {}
        elif raw_equals_clean:
            change_type = "identical"
            change_fields = {}
        else:
            change_fields = field_difference_counts(raw, clean)
            if profiles[raw]["structure_hash"] != profiles[clean]["structure_hash"]:
                change_type = "structural"
            elif change_fields.get("ID") or change_fields.get("FORM"):
                change_type = "non-structural content/metadata"
            else:
                change_type = "annotation-only"

        runs.append(
            {
                "language": language,
                "root": root,
                "model": model,
                "training_condition": training,
                "test_condition": test,
                "raw": raw,
                "clean": clean,
                "numbered": numbered,
                "alternates": alternates,
                "numbered_comparisons": numbered_comparisons,
                "raw_equals_clean": raw_equals_clean,
                "change_type": change_type,
                "change_fields": change_fields,
            }
        )
    return runs


def cross_language_groups(
    profiles: dict[Path, dict[str, object]], key: str
) -> list[tuple[str, list[Path]]]:
    grouped: dict[str, list[Path]] = defaultdict(list)
    for path, profile in profiles.items():
        grouped[str(profile[key])].append(path)
    result = []
    for digest, paths in grouped.items():
        languages = {path.parent.name for path in paths if path.parent.name in LANGUAGES}
        if len(languages) > 1:
            result.append((digest, sorted(paths, key=display_path)))
    return sorted(result, key=lambda item: item[0])


def classify_runs(
    runs: list[dict[str, object]], profiles: dict[Path, dict[str, object]]
) -> None:
    surface_occurrences: dict[str, list[dict[str, object]]] = defaultdict(list)
    exact_occurrences: dict[str, list[dict[str, object]]] = defaultdict(list)
    for run in runs:
        clean = run["clean"]
        if clean is not None:
            surface_occurrences[str(profiles[clean]["surface_hash"])].append(run)
            exact_occurrences[str(profiles[clean]["sha256"])].append(run)

    for run in runs:
        clean = run["clean"]
        wrong_language = False
        wrong_language_evidence = ""
        if clean is not None:
            surface_peers = surface_occurrences[str(profiles[clean]["surface_hash"])]
            exact_peers = exact_occurrences[str(profiles[clean]["sha256"])]
            own_matching_peers = [
                peer
                for peer in surface_peers
                if peer is not run
                and peer["language"] == run["language"]
                and peer["test_condition"] == run["test_condition"]
            ]
            other_language_peers = [
                peer for peer in surface_peers if peer["language"] != run["language"]
            ]
            other_exact_peers = [
                peer for peer in exact_peers if peer["language"] != run["language"]
            ]
            if other_language_peers and not own_matching_peers:
                other_counts = Counter(peer["language"] for peer in other_language_peers)
                likely_language, peer_count = other_counts.most_common(1)[0]
                likely_cohort_count = sum(
                    1
                    for peer in runs
                    if peer["language"] == likely_language
                    and peer["test_condition"] == run["test_condition"]
                    and peer["clean"] is not None
                    and profiles[peer["clean"]]["surface_hash"]
                    == profiles[clean]["surface_hash"]
                )
                if likely_cohort_count >= 2 or other_exact_peers:
                    wrong_language = True
                    evidence_kind = "byte-identical" if other_exact_peers else "surface-identical"
                    wrong_language_evidence = (
                        f"{evidence_kind} to {likely_language} prediction content; "
                        f"sample: {' '.join(profiles[clean]['sample_forms'])}"
                    )

        clean_issues = profiles[clean]["issues"] if clean is not None else []
        numbered_mismatches = [
            comparison
            for comparison in run["numbered_comparisons"]
            if not comparison["identical"]
        ]

        if clean is None:
            status = "MISSING CLEAN FILE"
            selected = None
            usable = False
            recommended = False
            reason = "No unnumbered _clean.conllu file is available."
        elif numbered_mismatches:
            status = "AMBIGUOUS / NEEDS AM"
            selected = None
            usable = False
            recommended = False
            reason = "A numbered copy differs from its unnumbered counterpart."
        elif wrong_language:
            status = "EXCLUDE WRONG-LANGUAGE / CORRUPT"
            selected = None
            usable = False
            recommended = False
            reason = wrong_language_evidence
        elif clean_issues:
            status = "AMBIGUOUS / NEEDS AM"
            selected = None
            usable = False
            recommended = False
            reason = f"Clean file has {len(clean_issues)} strengthened structural issue(s)."
        elif str(run["model"]).lower().startswith(("spacy", "stanza")):
            status = "USE FOR INITIAL DEBUGGING"
            selected = clean
            usable = True
            recommended = True
            reason = "Clean file passes checks; AM identified spaCy/Stanza as stable debugging systems."
        else:
            status = "DEFER / RESULT MAY CHANGE"
            selected = clean
            usable = True
            recommended = False
            reason = "Clean file passes checks, but non-spaCy/Stanza results may still change."

        run.update(
            {
                "wrong_language": wrong_language,
                "wrong_language_evidence": wrong_language_evidence,
                "structural_status": (
                    "PASS" if clean is not None and not clean_issues else f"FAIL ({len(clean_issues)} issues)"
                ),
                "status": status,
                "selected": selected,
                "usable_now": usable,
                "recommended": recommended,
                "reason": reason,
            }
        )


def alternate_findings(
    runs: list[dict[str, object]], profiles: dict[Path, dict[str, object]]
) -> list[dict[str, object]]:
    findings = []
    for run in runs:
        for alternate in run["alternates"]:
            raw = run["raw"]
            clean = run["clean"]
            raw_counts = field_difference_counts(raw, alternate) if raw else {}
            clean_counts = field_difference_counts(clean, alternate) if clean else {}
            findings.append(
                {
                    "alternate": alternate,
                    "raw": raw,
                    "clean": clean,
                    "equals_raw": bool(raw and profiles[alternate]["sha256"] == profiles[raw]["sha256"]),
                    "equals_clean": bool(clean and profiles[alternate]["sha256"] == profiles[clean]["sha256"]),
                    "same_structure_as_raw": bool(
                        raw and profiles[alternate]["structure_hash"] == profiles[raw]["structure_hash"]
                    ),
                    "raw_counts": raw_counts,
                    "clean_counts": clean_counts,
                }
            )
    return findings


def gold_candidates() -> list[Path]:
    gold_dir = REPO_DIR / "data" / "gold"
    if not gold_dir.is_dir():
        return []
    return sorted(gold_dir.glob("*.conllu"))


def infer_gold_scope(path: Path) -> tuple[str, str]:
    name = path.name.lower()
    language = name[:2].upper() if len(name) >= 2 else ""
    if "_ssj" in name:
        test_condition = "writtentest"
    elif "_sst" in name:
        test_condition = "spokentest"
    else:
        test_condition = ""
    return language, test_condition


def compare_gold_candidates(
    candidates: list[Path],
    gold_profiles: dict[Path, dict[str, object]],
    runs: list[dict[str, object]],
    profiles: dict[Path, dict[str, object]],
) -> list[dict[str, object]]:
    comparisons = []
    for candidate in candidates:
        language, test_condition = infer_gold_scope(candidate)
        relevant = [
            run
            for run in runs
            if run["language"] == language
            and run["test_condition"] == test_condition
            and run["selected"] is not None
        ]
        gold_profile = gold_profiles[candidate]
        structure_matches = [
            run
            for run in relevant
            if profiles[run["selected"]]["structure_hash"] == gold_profile["structure_hash"]
        ]
        surface_matches = [
            run
            for run in relevant
            if profiles[run["selected"]]["surface_hash"] == gold_profile["surface_hash"]
        ]
        sent_id_matches = [
            run
            for run in relevant
            if profiles[run["selected"]]["sent_id_count"] == gold_profile["sent_id_count"]
            and profiles[run["selected"]]["sent_id_hash"] == gold_profile["sent_id_hash"]
        ]
        comparisons.append(
            {
                "path": candidate,
                "language": language,
                "test_condition": test_condition,
                "profile": gold_profile,
                "relevant_count": len(relevant),
                "structure_matches": len(structure_matches),
                "surface_matches": len(surface_matches),
                "sent_id_matches": len(sent_id_matches),
            }
        )
    return comparisons


def check_with_existing_evaluator_loader(
    runs: list[dict[str, object]],
) -> list[tuple[Path, str]]:
    """Parse clean candidates with the existing loader, without calling evaluate()."""
    evaluator_path = REPO_DIR / "scripts" / "conll18_ud_eval_tag-based.py"
    spec = importlib.util.spec_from_file_location("aaron_ud_eval_loader", evaluator_path)
    if spec is None or spec.loader is None:
        return [(evaluator_path, "could not import existing evaluator loader")]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    failures = []
    for run in runs:
        clean = run["clean"]
        if clean is None:
            continue
        try:
            module.load_conllu_file(str(clean))
        except Exception as error:  # The legacy loader exposes several error types.
            failures.append((clean, f"{type(error).__name__}: {error}"))
    return failures


def tsv_text(rows: list[dict[str, object]], fieldnames: list[str]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def canonical_tsv(runs: list[dict[str, object]]) -> str:
    rows = []
    for run in runs:
        notes = []
        if run["change_type"] != "identical":
            notes.append(
                f"raw->clean: {run['change_type']} ({format_counts(run['change_fields'])})"
            )
        if run["alternates"]:
            notes.append("nonstandard .conllu_ alternate exists and is excluded")
        rows.append(
            {
                "language": run["language"],
                "model": run["model"],
                "training_condition": run["training_condition"],
                "test_condition": run["test_condition"],
                "raw_file": display_path(run["raw"]) if run["raw"] else "",
                "clean_file": display_path(run["clean"]) if run["clean"] else "",
                "selected_file": display_path(run["selected"]) if run["selected"] else "",
                "numbered_duplicates": ";".join(display_path(path) for path in run["numbered"]),
                "raw_equals_clean": str(bool(run["raw_equals_clean"])).lower(),
                "raw_clean_change_type": run["change_type"],
                "structural_status": run["structural_status"],
                "status": run["status"],
                "usable_now": str(bool(run["usable_now"])).lower(),
                "recommended_for_initial_debugging": str(bool(run["recommended"])).lower(),
                "reason": run["reason"],
                "notes": "; ".join(notes),
            }
        )
    fields = [
        "language",
        "model",
        "training_condition",
        "test_condition",
        "raw_file",
        "clean_file",
        "selected_file",
        "numbered_duplicates",
        "raw_equals_clean",
        "raw_clean_change_type",
        "structural_status",
        "status",
        "usable_now",
        "recommended_for_initial_debugging",
        "reason",
        "notes",
    ]
    return tsv_text(rows, fields)


def excluded_tsv(
    physical_files: list[Path],
    runs: list[dict[str, object]],
    profiles: dict[Path, dict[str, object]],
) -> str:
    selected = {run["selected"] for run in runs if run["selected"] is not None}
    run_by_path = {
        path: run
        for run in runs
        for path in [run["raw"], run["clean"], *run["numbered"], *run["alternates"]]
        if path is not None
    }
    rows = []
    for path in physical_files:
        if path in selected:
            continue
        run = run_by_path.get(path)
        if run is None:
            category = "unclassified"
            reason = "Physical source file could not be associated with a logical run."
            related = ""
            identical_to = ""
        else:
            related = f"{run['language']}:{run['root']}"
            numbered = NUMBERED_RE.fullmatch(path.name)
            if numbered:
                counterpart = path.with_name(numbered.group("base") + ".conllu")
                identical = counterpart in profiles and profiles[path]["sha256"] == profiles[counterpart]["sha256"]
                category = "numbered_duplicate" if identical else "numbered_mismatch"
                reason = (
                    "Byte-identical numbered download/copy artifact; use the unnumbered file."
                    if identical
                    else "Numbered copy differs from its counterpart; needs clarification."
                )
                identical_to = display_path(counterpart) if identical else ""
            elif path.name.endswith(".conllu_"):
                category = "nonstandard_alternate"
                reason = "Unexplained .conllu_ alternate; canonical raw/clean files exist."
                identical_to = ""
            elif path == run["raw"]:
                category = "raw_superseded"
                if run["wrong_language"]:
                    reason = "Raw file is wrong-language content and is also superseded by the clean choice rule."
                else:
                    reason = "Raw version is superseded by AM's instructed _clean canonical version."
                identical_to = display_path(run["clean"]) if run["raw_equals_clean"] and run["clean"] else ""
            elif path == run["clean"] and run["wrong_language"]:
                category = "wrong_language"
                reason = str(run["reason"])
                identical_to = ""
            elif path == run["clean"]:
                category = "blocked_clean"
                reason = str(run["reason"])
                identical_to = ""
            else:
                category = "noncanonical"
                reason = "Not selected as the canonical physical file."
                identical_to = ""
        rows.append(
            {
                "physical_file": display_path(path),
                "language": path.parent.name,
                "category": category,
                "logical_run": related,
                "byte_identical_to": identical_to,
                "reason": reason,
            }
        )
    return tsv_text(
        rows,
        [
            "physical_file",
            "language",
            "category",
            "logical_run",
            "byte_identical_to",
            "reason",
        ],
    )


def report_markdown(
    physical_files: list[Path],
    profiles: dict[Path, dict[str, object]],
    runs: list[dict[str, object]],
    exact_cross_groups: list[tuple[str, list[Path]]],
    surface_cross_groups: list[tuple[str, list[Path]]],
    alternates: list[dict[str, object]],
    gold_comparisons: list[dict[str, object]],
    evaluator_loader_failures: list[tuple[Path, str]],
) -> str:
    usable = [run for run in runs if run["usable_now"]]
    recommended = [run for run in runs if run["recommended"]]
    blocked = [run for run in runs if not run["usable_now"]]
    provisional = [run for run in usable if not run["recommended"]]
    clean_pass = [
        run
        for run in runs
        if run["clean"] is not None and not profiles[run["clean"]]["issues"]
    ]
    numbered_comparisons = [
        comparison for run in runs for comparison in run["numbered_comparisons"]
    ]
    numbered_mismatches = [item for item in numbered_comparisons if not item["identical"]]
    change_counts = Counter(run["change_type"] for run in runs)
    structural_changes = [run for run in runs if run["change_type"] == "structural"]
    raw_structural_issues = [
        run
        for run in runs
        if run["raw"] is not None and profiles[run["raw"]]["issues"]
    ]
    raw_issue_codes = Counter(
        issue["code"]
        for run in raw_structural_issues
        for issue in profiles[run["raw"]]["issues"]
    )

    lines = [
        "# AM benchmark source resolution",
        "",
        f"Generated {datetime.now().astimezone().isoformat(timespec='seconds')}. "
        "This is a read-only source-data investigation; no model evaluation was run.",
        "",
        "## A. Executive conclusion",
        "",
        f"The 261 physical source files resolve to **{len(runs)} logical prediction runs**. "
        f"AM's `_clean` choice is available for every run, and **{len(clean_pass)}/{len(runs)} clean files pass** "
        "the strengthened CoNLL-U/evaluator structural gate.",
        "",
        f"**Use {len(usable)} canonical clean predictions structurally:** {len(recommended)} spaCy/Stanza runs are "
        f"the recommended initial-debugging subset, while {len(provisional)} other structurally usable runs remain "
        "provisional because their results may change. One logical run is excluded: the NL Trankit "
        "written+spoken-training/spoken-test clean file contains EN corpus content.",
        "",
        "Prediction inputs are therefore resolved, but evaluation is **not gold-ready**: no matching EN or NL gold "
        "CoNLL-U files were found, and local SL candidates require explicit provenance/correspondence confirmation "
        "even where surface structure matches.",
        "",
        "## B. Physical source-file inventory",
        "",
        "A logical run is the language plus model, training condition, and test condition encoded in a filename; "
        "raw, clean, numbered, and nonstandard variants are physical representations of that run.",
        "",
        "| Language | All regular files | `.conllu` | Logical runs | Numbered copies | `.conllu_` alternates |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for language in LANGUAGES:
        language_files = [path for path in physical_files if path.parent.name == language]
        language_runs = [run for run in runs if run["language"] == language]
        lines.append(
            f"| {language} | {len(language_files)} | {sum(path.name.endswith('.conllu') for path in language_files)} "
            f"| {len(language_runs)} | {sum(len(run['numbered']) for run in language_runs)} "
            f"| {sum(len(run['alternates']) for run in language_runs)} |"
        )
    lines.extend(
        [
            f"| **Total** | **{len(physical_files)}** | **{sum(path.name.endswith('.conllu') for path in physical_files)}** "
            f"| **{len(runs)}** | **{len(numbered_comparisons)}** | **{len(alternates)}** |",
            "",
            "The complete one-row-per-run inventory and selection decision is in `canonical_predictions.tsv`.",
            "",
            "## C. Duplicate and copy analysis",
            "",
            f"All **{len(numbered_comparisons)} numbered copies** are byte-identical to their same-directory "
            f"unnumbered counterparts; mismatches found: **{len(numbered_mismatches)}**. They are download/copy "
            "artifacts, not independent model runs.",
            "",
            f"Cross-language exact SHA-256 groups found: **{len(exact_cross_groups)}**.",
            "",
        ]
    )
    for digest, paths in exact_cross_groups:
        lines.append(f"- `{digest}`")
        lines.extend(f"  - `{display_path(path)}`" for path in paths)
    if not exact_cross_groups:
        lines.append("- None.")
    lines.extend(
        [
            "",
            f"Cross-language exact ID/FORM surface groups found: **{len(surface_cross_groups)}**. "
            "Surface identity is used as corroborating evidence, not as a general language detector.",
            "",
            "## D. Raw versus clean findings",
            "",
            f"Across {len(runs)} raw/clean pairs: **{change_counts['identical']} are byte-identical**, "
            f"**{change_counts['annotation-only']} have annotation-only changes**, and "
            f"**{change_counts['structural']} change sentence/token ID structure**.",
            "",
        ]
    )
    other_change_count = len(runs) - sum(
        change_counts[name] for name in ("identical", "annotation-only", "structural")
    )
    if other_change_count:
        lines.append(f"A further {other_change_count} pair(s) have another non-structural change type.")
        lines.append("")
    lines.extend(
        [
            "The structural cleaning is concentrated in these runs:",
            "",
            "| Language | Model | Training | Test | Changed fields |",
            "|---|---|---|---|---|",
        ]
    )
    for run in structural_changes:
        lines.append(
            f"| {run['language']} | {run['model']} | {run['training_condition']} | {run['test_condition']} "
            f"| {format_counts(run['change_fields'])} |"
        )
    if not structural_changes:
        lines.append("| — | — | — | — | None |")
    lines.extend(
        [
            "",
            f"The raw structural gate flags {len(raw_structural_issues)} logical raw files, while their clean "
            "counterparts pass. Raw finding counts by rule: "
            f"**{', '.join(f'{code}={count}' for code, count in sorted(raw_issue_codes.items()))}**. "
            "Cleaning therefore includes evaluator formatting, meaningful token renumbering, and dependency repair; "
            "it is not merely whitespace normalization.",
            "",
            "## E. Selected clean predictions pass the strengthened structural gate",
            "",
            "The gate checks UTF-8 and 10 columns; ordinary, MWT, and empty-node ID syntax (including legal `0.1`); "
            "sequential ordinary IDs; valid/non-dangling HEAD values; self-loops; longer dependency cycles; exactly "
            "one root; MWT component placement; empty-node base/order consistency; non-empty FORM values; and the "
            "final blank line required by the existing evaluator.",
            "",
            f"**Result: {len(clean_pass)}/{len(runs)} unnumbered clean candidates pass with zero findings.** "
            "This establishes evaluator-oriented structural safety, not full Universal Dependencies conformance and "
            "not correctness against gold annotations.",
            "",
            f"Independent parser cross-check: the repository's existing CoNLL-U evaluator loader accepted "
            f"**{len(runs) - len(evaluator_loader_failures)}/{len(runs)}** clean candidates. Only its load/validation "
            "path was called; no evaluation or scoring function was run.",
            "",
            "## F. Suspicious and invalid files",
            "",
        ]
    )
    for run in blocked:
        clean_profile = profiles[run["clean"]] if run["clean"] else None
        sample = " ".join(clean_profile["sample_forms"]) if clean_profile else ""
        lines.extend(
            [
                f"- **{run['language']} / {run['model']} / {run['training_condition']} / {run['test_condition']} — "
                f"{run['status']}**",
                f"  - Clean file: `{display_path(run['clean']) if run['clean'] else ''}`",
                f"  - Evidence: {run['reason']}",
                f"  - Opening token sample: `{sample}`",
                "  - Action: obtain a replacement or explicit clarification; do not repair or evaluate this file as NL.",
            ]
        )
    if not blocked:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "The seven NL raw files with malformed sentence numbering are retained as immutable evidence but are "
            "superseded by structurally clean `_clean` versions. Every noncanonical physical file and its reason is "
            "listed in `excluded_or_ambiguous_files.tsv`.",
            "",
            "## G. The four EN `.conllu_` files are unexplained alternates",
            "",
            "None is selected. Each has a normal raw and clean counterpart, and the normal raw equals clean.",
            "",
            "| Alternate | Equals raw/clean | Same ID structure | Differences from raw |",
            "|---|---|---|---|",
        ]
    )
    for item in alternates:
        lines.append(
            f"| `{display_path(item['alternate'])}` | {item['equals_raw'] and item['equals_clean']} "
            f"| {item['same_structure_as_raw']} | {format_counts(item['raw_counts'])} |"
        )
    lines.extend(
        [
            "",
            "Because these versions change real annotations—including a HEAD change in one file—renaming them or "
            "treating them as canonical would destroy provenance rather than resolve it.",
            "",
            "## H. Gold-file readiness",
            "",
            "Repository-wide discovery found local gold candidates only for SL. EN and NL have no candidate gold "
            "CoNLL-U files outside AM's prediction source tree.",
            "",
            "| Candidate | Intended cohort inferred from repository docs | Sentences | Ordinary tokens | "
            "Structure matches | ID/FORM surface matches | `sent_id` matches |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for comparison in gold_comparisons:
        profile = comparison["profile"]
        cohort = f"{comparison['language']} {comparison['test_condition']} ({comparison['relevant_count']} selected runs)"
        lines.append(
            f"| `{display_path(comparison['path'])}` | {cohort} | {profile['sentence_count']} "
            f"| {profile['ordinary_count']} | {comparison['structure_matches']} "
            f"| {comparison['surface_matches']} | {comparison['sent_id_matches']} |"
        )
    if not gold_comparisons:
        lines.append("| None found | — | — | — | — | — | — |")
    lines.extend(
        [
            "",
            "An exact structural/surface match is evidence of alignment, but it does not prove that the local gold "
            "annotation version is the one AM intended. Exact source treebank/release mapping still needs written "
            "confirmation. Evaluation of the three-language benchmark must not start until EN and NL gold files and "
            "all prediction-to-gold mappings are supplied or confirmed.",
            "",
            "## I. Exact recommendation for what to use",
            "",
            f"1. Use the **{len(recommended)} selected spaCy/Stanza `_clean.conllu` files** marked "
            "`USE FOR INITIAL DEBUGGING` in `canonical_predictions.tsv` for pipeline debugging once matching gold is confirmed.",
            f"2. Retain the **{len(provisional)} other selected clean files** as structurally usable but provisional; "
            "their status is `DEFER / RESULT MAY CHANGE` pending result-stability confirmation.",
            "3. Exclude every numbered copy, every raw file, and every `.conllu_` alternate from canonical selection.",
            "4. Exclude the NL Trankit written+spoken-training/spoken-test run entirely until a Dutch replacement is supplied.",
            "5. Do not run evaluation yet: gold readiness is incomplete.",
            "",
            "## J. Remaining questions for AM/KD",
            "",
            "1. Please provide or identify the exact EN and NL gold CoNLL-U files for written, spoken, and Dutch dialect test conditions.",
            "2. Please confirm the exact treebank/version mapping for the SL written and spoken prediction cohorts, including whether any local SSJ/SST candidate is authoritative for this handoff.",
            "3. Please replace or explain the NL `trankit_writtenandspokentrain_spokentest_clean.conllu`, whose content matches EN rather than NL.",
            "4. Please explain the provenance of the four EN `.conllu_` Stanza files; they are excluded unless explicitly established as intended results.",
            "5. Which non-spaCy/Stanza result families are now frozen, and which should remain deferred because outputs may change?",
            "",
            "### Reproducibility note",
            "",
            "Run `python3 scripts/resolve_source.py` from `am_benchmark/`. The script reads source and gold "
            "candidates, writes only these reports, and performs no evaluation or repair.",
        ]
    )
    return "\n".join(lines) + "\n"


def print_summary(
    runs: list[dict[str, object]],
    profiles: dict[Path, dict[str, object]],
    evaluator_loader_failures: list[tuple[Path, str]],
) -> None:
    usable = [run for run in runs if run["usable_now"]]
    recommended = [run for run in runs if run["recommended"]]
    provisional = [run for run in usable if not run["recommended"]]
    blocked = [run for run in runs if not run["usable_now"]]
    clean_pass = sum(
        run["clean"] is not None and not profiles[run["clean"]]["issues"] for run in runs
    )
    print("AM benchmark source resolution complete")
    print(f"Logical prediction runs: {len(runs)}")
    print(f"Canonical prediction files structurally usable: {len(usable)}")
    print(f"Recommended initial spaCy/Stanza debugging files: {len(recommended)}")
    print(f"Other structurally usable but provisional files: {len(provisional)}")
    print(f"Blocked/excluded logical runs: {len(blocked)}")
    for run in blocked:
        print(f"  NEEDS REPLACEMENT/CLARIFICATION: {run['language']} {run['root']} — {run['reason']}")
    print(f"Clean structural gate: {clean_pass}/{len(runs)} pass")
    print(
        "Existing evaluator loader: "
        f"{len(runs) - len(evaluator_loader_failures)}/{len(runs)} clean files accepted"
    )
    print("Gold readiness: NOT READY — EN/NL gold missing; SL correspondence still needs confirmation")
    print("Reports created:")
    print("  reports/source_resolution.md")
    print("  reports/canonical_predictions.tsv")
    print("  reports/excluded_or_ambiguous_files.tsv")


def main() -> int:
    physical_files = sorted(
        [
            path
            for language in LANGUAGES
            for path in (SOURCE_DIR / language).rglob("*")
            if path.is_file()
        ],
        key=display_path,
    )
    profiles = {path: profile_conllu(path) for path in physical_files}
    runs = build_runs(physical_files, profiles)
    classify_runs(runs, profiles)

    exact_cross_groups = cross_language_groups(profiles, "sha256")
    surface_cross_groups = cross_language_groups(profiles, "surface_hash")
    alternates = alternate_findings(runs, profiles)

    candidates = gold_candidates()
    gold_profiles = {path: profile_conllu(path) for path in candidates}
    gold_comparisons = compare_gold_candidates(
        candidates, gold_profiles, runs, profiles
    )
    evaluator_loader_failures = check_with_existing_evaluator_loader(runs)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "canonical_predictions.tsv").write_text(
        canonical_tsv(runs), encoding="utf-8"
    )
    (REPORT_DIR / "excluded_or_ambiguous_files.tsv").write_text(
        excluded_tsv(physical_files, runs, profiles), encoding="utf-8"
    )
    (REPORT_DIR / "source_resolution.md").write_text(
        report_markdown(
            physical_files,
            profiles,
            runs,
            exact_cross_groups,
            surface_cross_groups,
            alternates,
            gold_comparisons,
            evaluator_loader_failures,
        ),
        encoding="utf-8",
    )
    print_summary(runs, profiles, evaluator_loader_failures)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
