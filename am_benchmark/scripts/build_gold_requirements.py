#!/usr/bin/env python3
"""Build gold-cohort requirements from the resolved prediction manifest.

This is a targeted follow-up to source resolution. It reads the canonical TSV,
selected prediction files, and local gold candidates. It does not score models or
modify prediction/gold data.
"""

from __future__ import annotations

import csv
import io
from collections import defaultdict
from pathlib import Path

from resolve_source import display_path, profile_conllu


LANGUAGE_ORDER = {"EN": 0, "NL": 1, "SL": 2}
TEST_ORDER = {"writtentest": 0, "spokentest": 1, "dialecttest": 2}

BENCHMARK_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = BENCHMARK_DIR.parent
REPORT_DIR = BENCHMARK_DIR / "reports"
CANONICAL_PATH = REPORT_DIR / "canonical_predictions.tsv"


def read_canonical_rows() -> list[dict[str, str]]:
    with CANONICAL_PATH.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source, delimiter="\t"))


def local_gold_scope(path: Path) -> tuple[str, str] | None:
    """Infer only mappings explicitly documented by this repository."""
    name = path.name.lower()
    if name.startswith("sl_") and "_ssj-" in name:
        return "SL", "writtentest"
    if name.startswith("sl_") and "_sst-" in name:
        return "SL", "spokentest"
    return None


def local_gold_role(path: Path) -> str:
    name = path.name
    if "_ssj-" in name:
        return "Existing primary SSJ written gold; documented as UD Slovenian SSJ r2.17."
    if name.endswith("-pog.conllu"):
        return "Colloquial 420-sentence SST transcription; used in the existing v5 paired-transcription analysis."
    if name.endswith("-stan.conllu"):
        return "Standardised 420-sentence partner to -pog; present locally but not evaluated in existing v5."
    if "_sst-" in name:
        return "Existing primary official standardised SST gold; 432 sentences, pinned to the r2.16/r2.17-identical file."
    return "Local gold candidate with no documented cohort mapping."


def test_label(test_condition: str) -> str:
    return {
        "writtentest": "written test",
        "spokentest": "spoken test",
        "dialecttest": "dialect test",
    }[test_condition]


def tsv_text(rows: list[dict[str, object]], fieldnames: list[str]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output, fieldnames=fieldnames, delimiter="\t", lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def compare_candidate(
    candidate: Path,
    selected_rows: list[dict[str, str]],
    prediction_profiles: dict[Path, dict[str, object]],
    gold_profiles: dict[Path, dict[str, object]],
) -> dict[str, object]:
    gold_profile = gold_profiles[candidate]
    structures = 0
    surfaces = 0
    sent_ids = 0
    incomplete_sent_ids = 0
    for row in selected_rows:
        prediction = BENCHMARK_DIR / row["selected_file"]
        profile = prediction_profiles[prediction]
        structures += profile["structure_hash"] == gold_profile["structure_hash"]
        surfaces += profile["surface_hash"] == gold_profile["surface_hash"]
        sent_ids += (
            profile["sent_id_count"] == gold_profile["sent_id_count"]
            and profile["sent_id_hash"] == gold_profile["sent_id_hash"]
        )
        incomplete_sent_ids += profile["sent_id_count"] != profile["sentence_count"]
    return {
        "path": candidate,
        "sha256": gold_profile["sha256"],
        "sentence_count": gold_profile["sentence_count"],
        "ordinary_count": gold_profile["ordinary_count"],
        "structures": structures,
        "surfaces": surfaces,
        "sent_ids": sent_ids,
        "incomplete_sent_ids": incomplete_sent_ids,
        "selected_count": len(selected_rows),
    }


def build_requirements(
    canonical_rows: list[dict[str, str]],
) -> tuple[list[dict[str, object]], dict[str, dict[str, object]]]:
    cohorts: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in canonical_rows:
        cohorts[(row["language"], row["test_condition"])].append(row)

    selected_paths = sorted(
        {
            BENCHMARK_DIR / row["selected_file"]
            for row in canonical_rows
            if row["selected_file"]
        }
    )
    prediction_profiles = {path: profile_conllu(path) for path in selected_paths}

    gold_dir = REPO_DIR / "data" / "gold"
    local_candidates = sorted(gold_dir.glob("*.conllu")) if gold_dir.is_dir() else []
    gold_profiles = {path: profile_conllu(path) for path in local_candidates}
    candidates_by_cohort: dict[tuple[str, str], list[Path]] = defaultdict(list)
    for path in local_candidates:
        scope = local_gold_scope(path)
        if scope is not None:
            candidates_by_cohort[scope].append(path)

    requirements = []
    details_by_cohort: dict[str, dict[str, object]] = {}
    for language, test_condition in sorted(
        cohorts,
        key=lambda key: (LANGUAGE_ORDER[key[0]], TEST_ORDER[key[1]]),
    ):
        rows = cohorts[(language, test_condition)]
        selected_rows = [row for row in rows if row["selected_file"]]
        comparisons = [
            compare_candidate(
                candidate, selected_rows, prediction_profiles, gold_profiles
            )
            for candidate in candidates_by_cohort[(language, test_condition)]
        ]
        comparisons.sort(
            key=lambda item: (
                int(item["surfaces"]),
                int(item["structures"]),
                -len(str(item["path"])),
            ),
            reverse=True,
        )
        best = comparisons[0] if comparisons and comparisons[0]["surfaces"] else None
        cohort_id = f"{language}:{test_condition}"

        if best is None:
            candidate_file = ""
            candidate_sha256 = ""
            candidate_sentences = ""
            candidate_ordinary_tokens = ""
            candidate_status = "MISSING"
            surface_structure_match = "No local candidate available."
            sent_id_match = "Not testable."
            confidence = "HIGH confidence repository has no candidate; authoritative identity remains unknown."
            reason = (
                "Targeted search of filenames, scripts, READMEs, configs, tracked references, "
                "comments, manifests, and repository history found no non-prediction gold candidate."
            )
            notes = "Stop here; do not reconstruct gold annotations from predictions."
        else:
            candidate_file = display_path(best["path"])
            candidate_sha256 = best["sha256"]
            candidate_sentences = best["sentence_count"]
            candidate_ordinary_tokens = best["ordinary_count"]
            candidate_status = "CANDIDATE — NEEDS PROVENANCE CONFIRMATION"
            surface_structure_match = (
                f"{best['structures']}/{best['selected_count']} exact sentence/ID structure; "
                f"{best['surfaces']}/{best['selected_count']} exact ID/FORM surface sequence."
            )
            sent_id_match = (
                f"{best['sent_ids']}/{best['selected_count']} exact; "
                f"{best['incomplete_sent_ids']} prediction files have incomplete sent_id coverage."
            )
            confidence = "HIGH structural alignment; UNCONFIRMED authority/version for AM benchmark."
            reason = (
                f"{local_gold_role(best['path'])} It aligns with every selected prediction in this cohort, "
                "but the AM handoff does not identify this file, release, or checksum as authoritative."
            )
            alternatives = [comparison for comparison in comparisons if comparison is not best]
            if alternatives:
                notes = "Other local files are not structural matches: " + "; ".join(
                    f"{display_path(item['path'])} ({item['structures']}/{item['selected_count']} structure, "
                    f"{item['surfaces']}/{item['selected_count']} surface; {local_gold_role(item['path'])})"
                    for item in alternatives
                )
            else:
                notes = "No other local candidate exists for this cohort."

        requirement = {
            "gold_cohort": cohort_id,
            "language": language,
            "test_condition": test_condition,
            "prediction_run_count": len(rows),
            "usable_prediction_run_count": len(selected_rows),
            "initial_debugging_run_count": sum(
                row["recommended_for_initial_debugging"] == "true" for row in rows
            ),
            "required_gold_role": (
                f"Authoritative {language} {test_label(test_condition)} gold CoNLL-U matching "
                "the prediction cohort's sentence/token content and intended annotation release."
            ),
            "candidate_gold_file": candidate_file,
            "candidate_sha256": candidate_sha256,
            "candidate_sentences": candidate_sentences,
            "candidate_ordinary_tokens": candidate_ordinary_tokens,
            "candidate_status": candidate_status,
            "surface_structure_match": surface_structure_match,
            "sent_id_match": sent_id_match,
            "confidence": confidence,
            "blocking": "true",
            "reason": reason,
            "notes": notes,
        }
        requirements.append(requirement)
        details_by_cohort[cohort_id] = requirement

    return requirements, details_by_cohort


def build_prediction_mapping(
    canonical_rows: list[dict[str, str]],
    requirements_by_cohort: dict[str, dict[str, object]],
) -> list[dict[str, object]]:
    mapping = []
    for row in canonical_rows:
        cohort_id = f"{row['language']}:{row['test_condition']}"
        requirement = requirements_by_cohort[cohort_id]
        if not row["selected_file"]:
            blocking_reason = (
                f"Prediction is excluded ({row['status']}); gold cohort is also unresolved."
            )
        elif requirement["candidate_status"] == "MISSING":
            blocking_reason = "Authoritative cohort gold is absent from the repository."
        else:
            blocking_reason = (
                "Local gold aligns structurally, but its authority/release for the AM benchmark is unconfirmed."
            )
        mapping.append(
            {
                "language": row["language"],
                "model": row["model"],
                "training_condition": row["training_condition"],
                "test_condition": row["test_condition"],
                "selected_prediction": row["selected_file"],
                "gold_cohort": cohort_id,
                "gold_file": requirement["candidate_gold_file"],
                "gold_status": requirement["candidate_status"],
                "initial_debugging": row["recommended_for_initial_debugging"],
                "evaluation_ready": "false",
                "blocking_reason": blocking_reason,
            }
        )
    return mapping


def build_questions(requirements: list[dict[str, object]]) -> str:
    requirement_by_cohort = {
        str(row["gold_cohort"]): row for row in requirements
    }
    sl_written = requirement_by_cohort["SL:writtentest"]
    sl_spoken = requirement_by_cohort["SL:spokentest"]
    return f"""# Gold clarification requirements

These are the remaining human inputs required before evaluation. For every
provided or confirmed gold file, record the dataset/treebank name, exact release
or version, filename, SHA-256 checksum, and cohort mapping.

## EN gold files

- Identify or provide the authoritative EN written-test gold CoNLL-U for cohort
  EN:writtentest.
- Identify or provide the authoritative EN spoken-test gold CoNLL-U for cohort
  EN:spokentest.

## NL gold files

- Identify or provide the authoritative NL written-test gold CoNLL-U for cohort
  NL:writtentest.
- Identify or provide the authoritative NL spoken-test gold CoNLL-U for cohort
  NL:spokentest.
- Identify or provide the authoritative NL dialect-test gold CoNLL-U for cohort
  NL:dialecttest, and clarify whether spoken and dialect are distinct datasets.

## SL provenance confirmation

- Confirm whether {sl_written['candidate_gold_file']} (SHA-256
  {sl_written['candidate_sha256']})—the local UD Slovenian SSJ r2.17 file that
  exactly matches the written predictions' ID/FORM structure—is the intended
  SL:writtentest gold.
- Confirm whether {sl_spoken['candidate_gold_file']} (SHA-256
  {sl_spoken['candidate_sha256']})—the local official standardised UD Slovenian
  SST r2.16/r2.17 file that exactly matches the spoken predictions' ID/FORM
  structure—is the intended SL:spokentest gold.
- If either answer is no, provide the authoritative replacement and exact release
  information. Structural alignment alone is not sufficient confirmation.

## Separate prediction blocker

- Provide a corrected NL Trankit written+spoken-training/spoken-test prediction,
  or confirm that this logical run should remain excluded. The current file is
  byte-identical to EN content.
"""


def main() -> int:
    canonical_rows = read_canonical_rows()
    requirements, requirements_by_cohort = build_requirements(canonical_rows)
    mapping = build_prediction_mapping(canonical_rows, requirements_by_cohort)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "gold_requirements.tsv").write_text(
        tsv_text(
            requirements,
            [
                "gold_cohort",
                "language",
                "test_condition",
                "prediction_run_count",
                "usable_prediction_run_count",
                "initial_debugging_run_count",
                "required_gold_role",
                "candidate_gold_file",
                "candidate_sha256",
                "candidate_sentences",
                "candidate_ordinary_tokens",
                "candidate_status",
                "surface_structure_match",
                "sent_id_match",
                "confidence",
                "blocking",
                "reason",
                "notes",
            ],
        ),
        encoding="utf-8",
    )
    (REPORT_DIR / "prediction_gold_mapping.tsv").write_text(
        tsv_text(
            mapping,
            [
                "language",
                "model",
                "training_condition",
                "test_condition",
                "selected_prediction",
                "gold_cohort",
                "gold_file",
                "gold_status",
                "initial_debugging",
                "evaluation_ready",
                "blocking_reason",
            ],
        ),
        encoding="utf-8",
    )
    (REPORT_DIR / "gold_questions.md").write_text(
        build_questions(requirements), encoding="utf-8"
    )

    initial_cohorts = sum(
        int(row["initial_debugging_run_count"]) > 0 for row in requirements
    )
    candidates = [
        row for row in requirements if row["candidate_status"] != "MISSING"
    ]
    missing = [row for row in requirements if row["candidate_status"] == "MISSING"]
    print("AM benchmark gold requirements complete")
    print(f"Distinct gold cohorts required: {len(requirements)}")
    print(
        "Gold cohorts required for initial spaCy/Stanza debugging: "
        f"{initial_cohorts}"
    )
    print(
        "Plausible local candidates: "
        + ", ".join(str(row["gold_cohort"]) for row in candidates)
    )
    print(
        "Missing candidates: "
        + ", ".join(str(row["gold_cohort"]) for row in missing)
    )
    print(
        "Awaiting provenance/version confirmation: "
        + ", ".join(str(row["gold_cohort"]) for row in candidates)
    )
    print("Evaluation ready: NO — all seven cohorts remain blocking")
    print(
        "Human clarification: provide EN/NL gold; confirm exact SL files/releases; "
        "resolve broken NL Trankit prediction"
    )
    print("Reports created:")
    print("  reports/gold_requirements.tsv")
    print("  reports/prediction_gold_mapping.tsv")
    print("  reports/gold_questions.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
