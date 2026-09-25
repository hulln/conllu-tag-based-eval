#!/usr/bin/env python3
"""Audit the label vocabularies of canonical predictions against their gold cohorts.

The source audit checks structure (columns, token IDs, HEADs, sentence spans); it
does not look at what the annotation columns contain. The evaluator compares
labels as exact strings, so a prediction in another label scheme or spelling
evaluates without error and scores as wrong. This audit catches that before a
score is trusted:

- DEPREL base labels (subtypes stripped, as the evaluator does) that are neither
  in the gold cohort nor in the UD relation inventory, and labels that differ from
  a gold label only in letter case;
- UPOS values outside the 17 UD tags;
- FEATS, LEMMA and XPOS left empty ("_") far more often than in gold, which means
  the layer was not predicted at all.

Read-only: nothing under source/ is modified.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


BENCHMARK_DIR = Path(__file__).resolve().parents[1]
CANONICAL_PATH = BENCHMARK_DIR / "reports" / "canonical_predictions.tsv"
STABLE_MODELS = ("spacy", "stanza")

UD_UPOS = set(
    "ADJ ADP ADV AUX CCONJ DET INTJ NOUN NUM PART PRON PROPN PUNCT SCONJ SYM VERB X".split()
)
UD_DEPREL = set(
    """acl advcl advmod amod appos aux case cc ccomp clf compound conj cop csubj dep det
    discourse dislocated expl fixed flat goeswith iobj list mark nmod nsubj nummod obj obl
    orphan parataxis punct reparandum root vocative xcomp""".split()
)

# Thresholds, in percentage points of word tokens.
FOREIGN_LABEL_THRESHOLD = 0.5
EMPTY_LAYER_EXCESS = 20.0
EMPTY_LEMMA_THRESHOLD = 5.0


def word_rows(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            columns = line.split("\t")
            if len(columns) == 10 and columns[0].isdigit():
                yield columns


def profile(path: Path) -> dict[str, object]:
    result = {
        "words": 0, "deprel": Counter(), "upos": Counter(),
        "feats_empty": 0, "lemma_empty": 0, "xpos_empty": 0,
    }
    for columns in word_rows(path):
        result["words"] += 1
        result["deprel"][columns[7].split(":")[0]] += 1
        result["upos"][columns[3]] += 1
        result["feats_empty"] += columns[5] == "_"
        result["lemma_empty"] += columns[2] == "_"
        result["xpos_empty"] += columns[4] == "_"
    return result


def gold_path(language: str, test_condition: str) -> Path:
    kind = "written" if test_condition == "writtentest" else "spoken"
    return BENCHMARK_DIR / "source" / "gold" / f"{language.lower()}_gold_test_{kind}_final_clean.conllu"


def percent(part: float, whole: int) -> float:
    return 100 * part / whole if whole else 0.0


def top(counts: dict[str, int], limit: int = 6) -> str:
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]
    return ", ".join(f"{label}={count}" for label, count in ranked)


def issues_for(pred: dict[str, object], gold: dict[str, object]) -> list[str]:
    words = pred["words"]
    gold_labels = set(gold["deprel"])
    foreign = {label: count for label, count in pred["deprel"].items()
               if label not in gold_labels and label not in UD_DEPREL}
    case_only = {label: count for label, count in pred["deprel"].items()
                 if label not in gold_labels and label.lower() in gold_labels}
    bad_upos = {label: count for label, count in pred["upos"].items() if label not in UD_UPOS}

    issues = []
    if percent(sum(foreign.values()), words) > FOREIGN_LABEL_THRESHOLD:
        issues.append(f"DEPREL outside gold and UD on {percent(sum(foreign.values()), words):.1f}% "
                      f"of words ({top(foreign)})")
    if case_only:
        issues.append(f"DEPREL differing from gold only in case ({top(case_only)})")
    if percent(sum(bad_upos.values()), words) > FOREIGN_LABEL_THRESHOLD:
        issues.append(f"UPOS outside UD on {percent(sum(bad_upos.values()), words):.1f}% of words "
                      f"({top(bad_upos, 4)})")
    for layer, key in (("FEATS", "feats_empty"), ("XPOS", "xpos_empty")):
        predicted = percent(pred[key], words)
        expected = percent(gold[key], gold["words"])
        if predicted - expected > EMPTY_LAYER_EXCESS:
            issues.append(f"{layer} empty on {predicted:.0f}% of words (gold: {expected:.0f}%)")
    if percent(pred["lemma_empty"], words) > EMPTY_LEMMA_THRESHOLD:
        issues.append(f"LEMMA empty on {percent(pred['lemma_empty'], words):.0f}% of words")
    return issues


def main() -> int:
    gold_profiles: dict[Path, dict[str, object]] = {}
    flagged = total = 0
    with CANONICAL_PATH.open(encoding="utf-8") as handle:
        for run in csv.DictReader(handle, delimiter="\t"):
            if run["usable_now"] != "true":
                continue
            total += 1
            gold_file = gold_path(run["language"], run["test_condition"])
            gold = gold_profiles.setdefault(gold_file, profile(gold_file))
            issues = issues_for(profile(BENCHMARK_DIR / run["selected_file"]), gold)
            if not issues:
                continue
            flagged += 1
            status = "shown" if run["model"] in STABLE_MODELS else "provisional"
            print(f"[{status}] {run['language']} {run['test_condition']} "
                  f"{run['model']} {run['training_condition']}")
            for issue in issues:
                print(f"    - {issue}")
    print(f"\n{flagged} of {total} usable runs flagged")
    return 1 if flagged else 0


if __name__ == "__main__":
    raise SystemExit(main())
