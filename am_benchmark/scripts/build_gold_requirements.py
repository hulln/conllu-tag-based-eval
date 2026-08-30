#!/usr/bin/env python3
"""Map Aaron's authoritative gold handoff to canonical prediction cohorts."""

from __future__ import annotations

import csv
import hashlib
import io
import unicodedata
from collections import defaultdict
from pathlib import Path

from resolve_source import display_path, field_difference_counts, profile_conllu


LANGUAGE_ORDER = {"EN": 0, "NL": 1, "SL": 2}
TEST_ORDER = {"writtentest": 0, "spokentest": 1}

BENCHMARK_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = BENCHMARK_DIR.parent
REPORT_DIR = BENCHMARK_DIR / "reports"
CANONICAL_PATH = REPORT_DIR / "canonical_predictions.tsv"
GOLD_DIR = BENCHMARK_DIR / "source" / "gold"

GOLD_SPECS = {
    "EN:writtentest": {
        "filename": "en_gold_test_written_final_clean.conllu",
        "dataset": "UD English GUM test, 9 written genres (inferred from GUM IDs and metadata)",
        "normalisation": "None; authoritative supplied written-test file.",
    },
    "EN:spokentest": {
        "filename": "en_gold_test_spoken_final_clean.conllu",
        "dataset": "UD English GUM test, 6 spoken genres (inferred from GUM IDs and metadata)",
        "normalisation": "None; authoritative supplied spoken-test file.",
    },
    "NL:writtentest": {
        "filename": "nl_gold_test_written_final_clean.conllu",
        "dataset": "UD Dutch LassySmall test followed by UD Dutch Alpino test (explicit IDs/archives)",
        "normalisation": "None; authoritative supplied written-test file.",
    },
    "NL:spokentest": {
        "filename": "nl_gold_test_spoken_final_clean.conllu",
        "dataset": "Dutch dialect speech, plausibly GCND; exact corpus identity remains unverified",
        "normalisation": "NL source labels dialecttest and spokentest are canonicalised to spokentest.",
    },
    "SL:writtentest": {
        "filename": "sl_gold_test_written_final_clean.conllu",
        "dataset": "UD Slovenian SSJ test (IDs and byte comparison)",
        "normalisation": "None; authoritative supplied written-test file.",
    },
    "SL:spokentest": {
        "filename": "sl_gold_test_spoken_final_clean.conllu",
        "dataset": "UD Slovenian SST test (IDs and structural comparison)",
        "normalisation": "None; authoritative supplied spoken-test file.",
    },
}

LOCAL_SL_GOLD = {
    "SL:writtentest": REPO_DIR / "data" / "gold" / "sl_ssj-ud-test.conllu",
    "SL:spokentest": REPO_DIR / "data" / "gold" / "sl_sst-ud-test.conllu",
}


def read_canonical_rows() -> list[dict[str, str]]:
    with CANONICAL_PATH.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source, delimiter="\t"))


def evaluator_character_signature(path: Path) -> tuple[str, tuple[int, ...]]:
    """Return the legacy evaluator's underlying-text hash and sentence ends."""
    characters: list[str] = []
    sentence_ends: list[int] = []
    in_sentence = False
    skip_components = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            if in_sentence:
                sentence_ends.append(len(characters))
                in_sentence = False
            skip_components = 0
            continue
        if line.startswith("#"):
            continue
        columns = line.split("\t")
        if len(columns) != 10:
            continue
        token_id, form = columns[0], columns[1]
        if skip_components:
            skip_components -= 1
            continue
        if "." in token_id:
            continue
        if "-" in token_id:
            start, end = map(int, token_id.split("-"))
            skip_components = end - start + 1
        characters.extend(
            character for character in form if unicodedata.category(character) != "Zs"
        )
        in_sentence = True
    if in_sentence:
        sentence_ends.append(len(characters))
    digest = hashlib.sha256("".join(characters).encode("utf-8")).hexdigest()
    return digest, tuple(sentence_ends)


def tsv_text(rows: list[dict[str, object]], fieldnames: list[str]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output, fieldnames=fieldnames, delimiter="\t", lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def local_sl_comparison(
    cohort: str, supplied: Path, supplied_profile: dict[str, object]
) -> str:
    local = LOCAL_SL_GOLD.get(cohort)
    if local is None or not local.is_file():
        return "Not applicable."
    local_profile = profile_conllu(local)
    if supplied_profile["sha256"] == local_profile["sha256"]:
        return f"Byte-identical to {display_path(local)}."
    structural = (
        supplied_profile["structure_hash"] == local_profile["structure_hash"]
        and supplied_profile["surface_hash"] == local_profile["surface_hash"]
        and supplied_profile["sent_id_hash"] == local_profile["sent_id_hash"]
        and supplied_profile["sent_id_count"] == local_profile["sent_id_count"]
    )
    if structural:
        differences = field_difference_counts(supplied, local)
        detail = ", ".join(f"{field}={count}" for field, count in differences.items())
        return (
            f"Structurally identical but not byte-identical to {display_path(local)}; "
            f"data-row differences: {detail or 'none (comments/formatting only)'}."
        )
    return f"Actually different from {display_path(local)}."


def build_requirements(
    canonical_rows: list[dict[str, str]],
) -> tuple[list[dict[str, object]], dict[str, dict[str, object]]]:
    cohorts: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in canonical_rows:
        cohorts[f"{row['language']}:{row['test_condition']}"].append(row)

    unexpected = sorted(set(cohorts) - set(GOLD_SPECS))
    missing = sorted(set(GOLD_SPECS) - set(cohorts))
    if unexpected or missing:
        raise ValueError(f"Gold cohort mismatch; unexpected={unexpected}, missing={missing}")

    prediction_paths = {
        BENCHMARK_DIR / row["selected_file"]
        for row in canonical_rows
        if row["selected_file"]
    }
    prediction_profiles = {path: profile_conllu(path) for path in prediction_paths}
    prediction_signatures = {
        path: evaluator_character_signature(path) for path in prediction_paths
    }

    requirements: list[dict[str, object]] = []
    details: dict[str, dict[str, object]] = {}
    for cohort in sorted(
        GOLD_SPECS,
        key=lambda value: (
            LANGUAGE_ORDER[value.split(":")[0]],
            TEST_ORDER[value.split(":")[1]],
        ),
    ):
        language, test_condition = cohort.split(":")
        spec = GOLD_SPECS[cohort]
        gold_path = GOLD_DIR / str(spec["filename"])
        if not gold_path.is_file():
            raise FileNotFoundError(f"Missing authoritative gold: {gold_path}")
        gold_profile = profile_conllu(gold_path)
        gold_signature = evaluator_character_signature(gold_path)
        rows = cohorts[cohort]
        selected = [row for row in rows if row["selected_file"]]
        profiles = [prediction_profiles[BENCHMARK_DIR / row["selected_file"]] for row in selected]
        signatures = [prediction_signatures[BENCHMARK_DIR / row["selected_file"]] for row in selected]
        exact_structure = sum(
            profile["structure_hash"] == gold_profile["structure_hash"] for profile in profiles
        )
        exact_surface = sum(
            profile["surface_hash"] == gold_profile["surface_hash"] for profile in profiles
        )
        exact_sent_ids = sum(
            profile["sent_id_count"] == gold_profile["sent_id_count"]
            and profile["sent_id_hash"] == gold_profile["sent_id_hash"]
            for profile in profiles
        )
        character_matches = sum(signature[0] == gold_signature[0] for signature in signatures)
        sentence_matches = sum(signature[1] == gold_signature[1] for signature in signatures)
        ready = character_matches == len(selected)
        requirement = {
            "gold_cohort": cohort,
            "language": language,
            "test_condition": test_condition,
            "prediction_run_count": len(rows),
            "usable_prediction_run_count": len(selected),
            "initial_debugging_run_count": sum(
                row["recommended_for_initial_debugging"] == "true" for row in rows
            ),
            "required_gold_role": f"Authoritative {language} {test_condition} benchmark gold.",
            "candidate_gold_file": display_path(gold_path),
            "supplied_filename": gold_path.name,
            "dataset_treebank_identity": spec["dataset"],
            "candidate_sha256": gold_profile["sha256"],
            "candidate_sentences": gold_profile["sentence_count"],
            "candidate_ordinary_tokens": gold_profile["ordinary_count"],
            "candidate_status": "AUTHORITATIVE",
            "surface_structure_match": (
                f"{exact_structure}/{len(selected)} exact sentence/ID structure; "
                f"{exact_surface}/{len(selected)} exact ID/FORM surface sequence; "
                f"{character_matches}/{len(selected)} evaluator-compatible underlying text."
            ),
            "sent_id_match": (
                f"{exact_sent_ids}/{len(selected)} exact sent_id sequence; "
                f"{sentence_matches}/{len(selected)} exact evaluator sentence spans."
            ),
            "confidence": "AUTHORITATIVE handoff; dataset identity is separately labelled as inferred where necessary.",
            "blocking": str(not ready).lower(),
            "reason": "Aaron identified the supplied gold/test files as authoritative for all three languages.",
            "naming_normalisation": spec["normalisation"],
            "local_gold_comparison": local_sl_comparison(cohort, gold_path, gold_profile),
            "notes": (
                "Exact token structure may differ for tokenizer-varying predictions; compatibility is based on "
                "the unchanged repository evaluator's required underlying character sequence."
            ),
        }
        requirements.append(requirement)
        details[cohort] = requirement
    return requirements, details


def build_prediction_mapping(
    canonical_rows: list[dict[str, str]],
    requirements: dict[str, dict[str, object]],
) -> list[dict[str, object]]:
    mapping = []
    signature_cache: dict[Path, tuple[str, tuple[int, ...]]] = {}

    def signature(path: Path) -> tuple[str, tuple[int, ...]]:
        if path not in signature_cache:
            signature_cache[path] = evaluator_character_signature(path)
        return signature_cache[path]

    for row in canonical_rows:
        cohort = f"{row['language']}:{row['test_condition']}"
        requirement = requirements[cohort]
        prediction = BENCHMARK_DIR / row["selected_file"] if row["selected_file"] else None
        gold = BENCHMARK_DIR / str(requirement["candidate_gold_file"])
        compatible = bool(prediction and signature(prediction)[0] == signature(gold)[0])
        mapping.append(
            {
                "language": row["language"],
                "model": row["model"],
                "training_condition": row["training_condition"],
                "test_condition": row["test_condition"],
                "source_test_condition": row["source_test_condition"],
                "source_test_conditions": row["source_test_conditions"],
                "selected_prediction": row["selected_file"],
                "gold_cohort": cohort,
                "gold_file": requirement["candidate_gold_file"],
                "gold_status": "AUTHORITATIVE",
                "initial_debugging": row["recommended_for_initial_debugging"],
                "evaluation_ready": str(compatible).lower(),
                "blocking_reason": "" if compatible else "Prediction/gold underlying character sequence differs.",
            }
        )
    return mapping


def build_questions() -> str:
    return """# Gold handoff resolution

There are no remaining gold-availability or cohort-mapping questions blocking the
stable evaluation.

Aaron's clarification resolves the previous blockers: all six supplied files are
authoritative; Dutch `dialecttest` and `spokentest` are one canonical `spokentest`
cohort; and the NL Trankit file containing English text remains excluded.

The exact release label for the EN and NL files, and the precise corpus identity of
the NL spoken material, remain useful descriptive metadata if Aaron wishes to add
them later. They do not override the supplied-file checksums or block evaluation.
Non-spaCy/Stanza result families remain provisional independently of gold readiness.
"""


REQUIREMENT_FIELDS = [
    "gold_cohort", "language", "test_condition", "prediction_run_count",
    "usable_prediction_run_count", "initial_debugging_run_count", "required_gold_role",
    "candidate_gold_file", "supplied_filename", "dataset_treebank_identity",
    "candidate_sha256", "candidate_sentences", "candidate_ordinary_tokens",
    "candidate_status", "surface_structure_match", "sent_id_match", "confidence",
    "blocking", "reason", "naming_normalisation", "local_gold_comparison", "notes",
]


def main() -> int:
    canonical_rows = read_canonical_rows()
    requirements, by_cohort = build_requirements(canonical_rows)
    mapping = build_prediction_mapping(canonical_rows, by_cohort)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    requirements_text = tsv_text(requirements, REQUIREMENT_FIELDS)
    (REPORT_DIR / "gold_requirements.tsv").write_text(requirements_text, encoding="utf-8")
    (REPORT_DIR / "prediction_gold_mapping.tsv").write_text(
        tsv_text(
            mapping,
            [
                "language", "model", "training_condition", "test_condition",
                "source_test_condition", "source_test_conditions", "selected_prediction",
                "gold_cohort", "gold_file", "gold_status", "initial_debugging",
                "blocking_reason", "evaluation_ready",
            ],
        ),
        encoding="utf-8",
    )
    (REPORT_DIR / "gold_questions.md").write_text(build_questions(), encoding="utf-8")

    ready = sum(row["evaluation_ready"] == "true" for row in mapping)
    print("AM benchmark gold handoff mapped")
    print(f"Authoritative gold cohorts: {len(requirements)}")
    print(f"Canonical prediction mappings: {len(mapping)}")
    print(f"Evaluator-compatible mappings: {ready}/{len(mapping)}")
    print(
        "Initial stable spaCy/Stanza mappings: "
        f"{sum(row['initial_debugging'] == 'true' for row in mapping)}"
    )
    print("Reports created:")
    print("  reports/gold_requirements.tsv")
    print("  reports/prediction_gold_mapping.tsv")
    print("  reports/gold_questions.md")
    return 0 if ready == len(mapping) else 1


if __name__ == "__main__":
    raise SystemExit(main())
