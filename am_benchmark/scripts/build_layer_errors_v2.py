#!/usr/bin/env python3
"""Feature and lemma error tables for the v2 interface prototype.

The published diagnostic set (``build_diagnostics_data.py``) has no feature errors,
because the CJVT profiler it builds on never reads the FEATS column, and it reduces
lemma errors to one count, because lemmas are corpus text. This generator adds both
layers for ``tables/am_benchmark_v2`` only, into a folder of its own, and leaves the
published diagnostic set and its aggregate-only policy untouched.

Words are compared exactly as the existing error tables compare them: sentences
aligned by the CJVT profiler's ``align_sentences``, and a word skipped when the
sentence lengths or the word forms disagree.

- Features: a word is a feature error when its universal features, filtered as the
  evaluator filters them, differ from gold. Rows break those errors down by single
  feature ("Case=Nom" -> "Case=Acc", or "_" where one side lacks the feature). The
  word total is reconciled against the evaluator's own UFeats count.
- Lemmas: gold/predicted lemma pairs, for every test set. Lemmas are corpus text:
  do not publish these files before the licence question for the Dutch spoken test
  set is settled (see ``build_examples_v2.py``).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

BENCHMARK_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = BENCHMARK_DIR.parent

sys.path.insert(0, str(BENCHMARK_DIR / "scripts"))
sys.path.insert(0, str(REPO_DIR / "scripts"))

import build_diagnostics_data as diagnostics  # noqa: E402  stable-run selection, row format
import build_interactive_comparison_table_v2 as v2  # noqa: E402  CJVT alignment
import run_benchmark_evaluation as benchmark  # noqa: E402  evaluator access

SCHEMA_VERSION = 1
GENERATOR = "am_benchmark/scripts/build_layer_errors_v2.py"
OUTPUT_DIR = REPO_DIR / "tables" / "am_benchmark_v2" / "data" / "layers"
MISSING = "_"


def read_feats(path: Path) -> list[list[str]]:
    """FEATS per word, in exactly the sentences and words ``v2.read_conllu`` yields."""
    sentences: list[list[str]] = []
    feats: list[str] = []
    has_meta = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            if feats or has_meta:
                sentences.append(feats)
            feats, has_meta = [], False
            continue
        if line.startswith("#"):
            if line.startswith("# sent_id = ") or line.startswith("# text = "):
                has_meta = True
            continue
        cols = line.split("\t")
        if len(cols) != 10 or "-" in cols[0] or "." in cols[0]:
            continue
        feats.append(cols[5])
    if feats or has_meta:
        sentences.append(feats)
    return sentences


def read_with_feats(path: Path) -> list[dict[str, Any]]:
    sentences = v2.read_conllu(path)
    feats = read_feats(path)
    if len(feats) != len(sentences) or any(
            len(f) != len(s["tokens"]) for f, s in zip(feats, sentences)):
        raise ValueError(f"FEATS reader disagrees with v2.read_conllu on {path}")
    for sentence, sentence_feats in zip(sentences, feats):
        for token, value in zip(sentence["tokens"], sentence_feats):
            token["feats"] = value
    return sentences


def universal(value: str, names: set[str]) -> dict[str, str]:
    """The universal features of a FEATS value, as the evaluator keeps them."""
    kept = {}
    for feature in value.split("|"):
        name, _, val = feature.partition("=")
        if name in names:
            kept[name] = val
    return kept


def compare_layers(gold_path: Path, prediction_path: Path, names: set[str]) -> dict[str, Any]:
    gold = read_with_feats(gold_path)
    prediction = read_with_feats(prediction_path)
    pairs, _, _ = v2.align_sentences(gold, prediction)

    feature_pairs: Counter = Counter()
    lemma_pairs: Counter = Counter()
    feature_words = compared = predicted_empty = predicted_blank = 0
    for _gi, gold_sent, _pi, pred_sent in pairs:
        gold_tokens, pred_tokens = gold_sent["tokens"], pred_sent["tokens"]
        if len(gold_tokens) != len(pred_tokens):
            continue
        for gold_tok, pred_tok in zip(gold_tokens, pred_tokens):
            if gold_tok["form"] != pred_tok["form"]:
                continue
            compared += 1
            gold_feats = universal(gold_tok["feats"], names)
            pred_feats = universal(pred_tok["feats"], names)
            predicted_empty += not pred_feats
            # The column itself left blank: no features of any kind, universal or not.
            predicted_blank += pred_tok["feats"] == MISSING
            if gold_feats != pred_feats:
                feature_words += 1
                for name in sorted(set(gold_feats) | set(pred_feats)):
                    g, p = gold_feats.get(name), pred_feats.get(name)
                    if g != p:
                        feature_pairs[(f"{name}={g}" if g else MISSING,
                                       f"{name}={p}" if p else MISSING)] += 1
            if gold_tok["lemma"] != pred_tok["lemma"]:
                lemma_pairs[(gold_tok["lemma"], pred_tok["lemma"])] += 1
    return {
        "compared": compared,
        "feature_words": feature_words,
        "feature_pairs": feature_pairs,
        "predicted_empty": predicted_empty,
        "predicted_blank": predicted_blank,
        "lemma_pairs": lemma_pairs,
    }


def rows(counter: Counter) -> list[list[Any]]:
    ordered = [[gold, predicted, count] for (gold, predicted), count in counter.items()]
    ordered.sort(key=lambda row: (-row[2], row[0], row[1]))
    return ordered


def build_run(evaluator, row: dict[str, str]) -> dict[str, Any]:
    key = diagnostics.run_key(row)
    gold_path = benchmark.resolve_manifest_path(row["gold_file"])
    prediction_path = benchmark.resolve_manifest_path(row["selected_prediction"])

    evaluation = evaluator.evaluate(
        evaluator.load_conllu_file(str(gold_path)),
        evaluator.load_conllu_file(str(prediction_path)),
    )
    layers = compare_layers(gold_path, prediction_path, set(evaluator.UNIVERSAL_FEATURES))

    ufeats = evaluation["UFeats"]
    expected = ufeats.aligned_total - ufeats.correct
    if layers["compared"] != ufeats.aligned_total or layers["feature_words"] != expected:
        raise ValueError(
            f"{key}: feature errors do not reconcile with the evaluator "
            f"(compared {layers['compared']} vs aligned {ufeats.aligned_total}; "
            f"errors {layers['feature_words']} vs {expected})")

    lemmas = {
        "total": sum(layers["lemma_pairs"].values()),
        "columns": ["gold", "predicted", "count"],
        "rows": rows(layers["lemma_pairs"]),
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "kind": "am-benchmark-v2-layer-errors",
        "generator": GENERATOR,
        "run": {"key": key},
        "features": {
            "total": layers["feature_words"],
            "compared": layers["compared"],
            "predicted_empty": layers["predicted_empty"],
            "predicted_blank": layers["predicted_blank"],
            "columns": ["gold", "predicted", "count"],
            "rows": rows(layers["feature_pairs"]),
        },
        "lemmas": lemmas,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.parse_args()
    runs = diagnostics.stable_runs(argparse.Namespace(
        language=None, model=None, training_condition=None, test_condition=None))

    evaluator = benchmark.load_evaluator()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for row in runs:
        payload = build_run(evaluator, row)
        key = payload["run"]["key"]
        text = json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"
        (OUTPUT_DIR / f"{key}.json").write_text(text, encoding="utf-8")
        print(f"  {key}: {payload['features']['total']} feature errors "
              f"({len(payload['features']['rows'])} rows), "
              f"{payload['lemmas']['total']} lemma errors "
              f"({len(payload['lemmas']['rows'])} rows)")
    print(f"Wrote {len(runs)} files to {OUTPUT_DIR.relative_to(REPO_DIR)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
