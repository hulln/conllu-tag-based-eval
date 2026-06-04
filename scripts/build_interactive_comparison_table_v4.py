#!/usr/bin/env python3
"""Build the combined data bundle for the v4 interactive comparison table.

v4 differs from v2/v3 in two ways:

1. Two-layer switching in a single page: the reader picks a **tagger**
   (SPOT-Trankit / CLASSLA-Stanza) and then a **corpus** (SSJ / SST).
2. Because either tagger can be the focus, the error rows + example
   sentences are emitted for **both** taggers (v2/v3 stored Trankit only).

This script only emits the data file (``window.TABLE_DATA_V4``); the page
itself lives in the committed, static ``tables/comparison_table_v4.html``.

Reuses the parsing/profiling helpers from
``build_interactive_comparison_table_v2`` so error definitions stay identical
to the published v2/v3 bundles.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import build_interactive_comparison_table_v2 as v2

REPO_ROOT = Path(__file__).resolve().parent.parent

MODELS = {
    "trankit": {"label": "SPOT-Trankit", "short": "SPOT-Trankit"},
    "classla": {"label": "CLASSLA-Stanza", "short": "CLASSLA"},
}
MODEL_ORDER = ["trankit", "classla"]
CORPUS_ORDER = ["ssj", "sst"]

# Provenance is split so the page can show only the relevant pieces:
#   - a MODEL part that switches with the selected model (CLASSLA's pipeline
#     even differs by corpus: lexicon on for written, spoken model otherwise);
#   - a DATA part that switches with the corpus.
# The page composes "Model: <model part> · Data: <data part>".
# Trankit provenance differs by corpus: SSJ (written) uses the 1.2 model, which
# is marginally better on standard text; SST (spoken) uses the newer 1.3 model
# (11356/2201, adds non-standard spoken training data), which is better on SST.
TRANKIT_PROV_12 = (
    'SPOT-Trankit &mdash; <a href="https://www.clarin.si/repository/xmlui/handle/11356/1997">CLARIN 11356/1997</a> (model 1.2), '
    'run with <a href="https://pypi.org/project/trankit/1.1.2/">trankit==1.1.2</a> using the Slovenian model archive '
    '<code>trankit-sl-ssj+sst.zip</code> (MD5 <code>0ddfac8d7445f8fa300f59dde1a00352</code>).'
)
TRANKIT_PROV_13 = (
    'SPOT-Trankit &mdash; <a href="https://www.clarin.si/repository/xmlui/handle/11356/2201">CLARIN 11356/2201</a> (model 1.3, '
    'adds non-standard spoken Slovenian), run with <a href="https://pypi.org/project/trankit/1.1.2/">trankit==1.1.2</a> using the '
    'Slovenian model archive <code>trankit-sl-ssj+sststand+sstpog.zip</code> (MD5 <code>ff1f3b86a4996fd5944db14725c602d8</code>). '
    'Model 1.3 replaces 1.2 here because it scores higher on SST for every metric except UPOS (unchanged) and lemmatisation '
    '(&minus;0.05).'
)
CLASSLA_PROV_WRITTEN = (
    'CLASSLA-Stanza &mdash; run with <a href="https://pypi.org/project/classla/2.2.1/">classla==2.2.1</a> '
    "(<code>classla.Pipeline('sl', pos_use_lexicon=True)</code>)."
)
CLASSLA_PROV_SPOKEN = (
    'CLASSLA-Stanza &mdash; run with <a href="https://pypi.org/project/classla/2.2.1/">classla==2.2.1</a> '
    "(<code>classla.Pipeline('sl', type='spoken')</code>; lexicon disabled for spoken model)."
)
DATA_PROV_SSJ = (
    '<a href="https://github.com/UniversalDependencies/UD_Slovenian-SSJ/blob/master/sl_ssj-ud-test.conllu">UD Slovenian SSJ</a> '
    'test set, <a href="https://github.com/UniversalDependencies/UD_Slovenian-SSJ/tree/master">v2.17</a> (2025-10-22); '
    'predictions were run on <em>pre-tokenised</em> text (gold sentence and token boundaries supplied).'
)
DATA_PROV_SST = (
    '<a href="https://github.com/UniversalDependencies/UD_Slovenian-SST/blob/master/sl_sst-ud-test.conllu">UD Slovenian SST</a> '
    'test set, <a href="https://github.com/UniversalDependencies/UD_Slovenian-SST/tree/master">v2.16</a> (2024-12-20); '
    'predictions were run on <em>pre-tokenised</em> text (gold sentence and token boundaries supplied).'
)

CORPORA = [
    {
        "key": "ssj",
        "label": "SSJ-UD",
        "domain": "written",
        "run_id": "20260414-1819_sl-ssj-ud-test_full",
        "gold": "data/gold/sl_ssj-ud-test.conllu",
        "provenance": {
            "models": {"trankit": TRANKIT_PROV_12, "classla": CLASSLA_PROV_WRITTEN},
            "data": DATA_PROV_SSJ,
        },
    },
    {
        "key": "sst",
        "label": "SST-UD",
        "domain": "spoken",
        "run_id": "20260604-0859-tk13_sl-sst-ud-test_full",
        "gold": "data/gold/sl_sst-ud-test.conllu",
        "provenance": {
            "models": {"trankit": TRANKIT_PROV_13, "classla": CLASSLA_PROV_SPOKEN},
            "data": DATA_PROV_SST,
        },
    },
]


def metrics_block(m: Dict[str, float], errors: int) -> Dict[str, Any]:
    return {
        "las": m.get("LAS", 0.0),
        "uas": m.get("UAS", 0.0),
        "upos": m.get("UPOS", 0.0),
        "xpos": m.get("XPOS", 0.0),
        "lemma": m.get("Lemmas", 0.0),
        "errors": errors,
    }


def tagger_error_block(profile: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "deprel_error_rows": v2.build_deprel_error_rows(profile),
        "deprel_examples": profile["deprel_examples"],
        "tag_error_rows": v2.build_tag_error_rows(profile),
        "tag_examples": profile["tag_examples"],
    }


def accuracy_rows_both(gold_sents, trankit_metrics, classla_metrics) -> Dict[str, List[Dict]]:
    """Accuracy rows carrying both models' value per tag (no precomputed diff;
    the page computes focus - reference at render time)."""
    deprel = v2.build_deprel_accuracy_rows(gold_sents, trankit_metrics, classla_metrics)
    upos = v2.build_upos_accuracy_rows(gold_sents, trankit_metrics, classla_metrics)
    for row in deprel + upos:
        row.pop("diff", None)
    return {"deprel": deprel, "upos": upos}


def build_corpus(cfg: Dict[str, Any], max_examples: int | None) -> Dict[str, Any]:
    run_id = cfg["run_id"]
    gold_path = REPO_ROOT / cfg["gold"]
    trankit_pred = REPO_ROOT / "predictions" / "output" / f"{run_id}_trankit_aligned_predicted.conllu"
    classla_pred = REPO_ROOT / "predictions" / "output" / f"{run_id}_classla_aligned_predicted.conllu"
    diag = REPO_ROOT / "results" / "output" / run_id / "diagnostics"
    trankit_eval = diag / "trankit_aligned_eval-tagged.txt"
    classla_eval = diag / "classla_aligned_eval-tagged.txt"

    for p in (gold_path, trankit_pred, classla_pred, trankit_eval, classla_eval):
        if not p.exists():
            raise FileNotFoundError(f"Missing input for corpus {cfg['key']}: {p}")

    gold_sents = v2.read_conllu(gold_path)
    trankit_profile = v2.collect_model_profile(gold_sents, v2.read_conllu(trankit_pred), max_examples)
    classla_profile = v2.collect_model_profile(gold_sents, v2.read_conllu(classla_pred), max_examples)

    trankit_metrics = v2.parse_eval_metrics(trankit_eval)
    classla_metrics = v2.parse_eval_metrics(classla_eval)

    compared = trankit_profile["totals"]["compared"]
    accuracy = accuracy_rows_both(gold_sents, trankit_metrics, classla_metrics)

    return {
        "key": cfg["key"],
        "label": cfg["label"],
        "domain": cfg["domain"],
        "run_id": run_id,
        "gold_sentences": len(gold_sents),
        "compared_tokens": compared,
        "provenance": cfg["provenance"],
        "metrics": {
            "trankit": metrics_block(
                trankit_metrics, compared - trankit_profile["totals"]["las_correct"]
            ),
            "classla": metrics_block(
                classla_metrics, compared - classla_profile["totals"]["las_correct"]
            ),
        },
        "deprel_accuracy_rows": accuracy["deprel"],
        "upos_accuracy_rows": accuracy["upos"],
        "errors": {
            "trankit": tagger_error_block(trankit_profile),
            "classla": tagger_error_block(classla_profile),
        },
    }


def build_payload(max_examples: int | None) -> Dict[str, Any]:
    corpora = {cfg["key"]: build_corpus(cfg, max_examples) for cfg in CORPORA}
    return {
        "models": MODELS,
        "model_order": MODEL_ORDER,
        "corpus_order": CORPUS_ORDER,
        "corpora": corpora,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the v4 combined data bundle.")
    parser.add_argument(
        "out_js",
        nargs="?",
        default=str(REPO_ROOT / "tables" / "comparison_table_v4_data.js"),
        help="Output JS data file (default: tables/comparison_table_v4_data.js).",
    )
    parser.add_argument(
        "--examples-per-item",
        type=int,
        default=25,
        help="Max stored examples per error pattern; 0 stores all (default: 25).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    max_examples = None if args.examples_per_item <= 0 else args.examples_per_item
    payload = build_payload(max_examples)
    out_path = Path(args.out_js)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        "window.TABLE_DATA_V4 = "
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {out_path} ({out_path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
