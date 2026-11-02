#!/usr/bin/env python3
"""Build the data bundle for the v6 interactive comparison table (draft).

v6 is v5 with a third tool, Stanza 1.14 (``package="default_accurate"``):

1. ``models`` / ``model_order`` list three tools, and every per-model block
   (metrics, error rows, accuracy columns) has a ``stanza`` entry.
2. The tools come from different runs, so each corpus carries ``run_ids``
   per model (``run_id`` is kept, the SPOT-Trankit/CLASSLA-Stanza run).
3. The colloquial (``pog``) corpus has a training-data note, because only
   SPOT-Trankit 1.3 was trained on colloquial transcriptions.

Everything else (gold files, error definitions, metrics) is v5's: the error
rows reuse the ``build_interactive_comparison_table_v2`` helpers, and the
SPOT-Trankit/CLASSLA-Stanza inputs are the same 20260622-0810-tk13 runs.
The page itself is the committed, static ``tables/comparison_table_v6.html``.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

import build_interactive_comparison_table_v2 as v2
import build_interactive_comparison_table_v5 as v5

REPO_ROOT = Path(__file__).resolve().parent.parent

MODELS = {
    **v5.MODELS,
    "stanza": {"label": "Stanza 1.14", "short": "Stanza"},
}
MODEL_ORDER = ["trankit", "classla", "stanza"]
CORPUS_ORDER = v5.CORPUS_ORDER

STANZA_RUN = "20261102-1110-stanza114acc"

# Stanza uses the same package on every test set. Training data per component
# (Stanza 1.14 Slovenian "combined" models): tokenizer and parser on UD
# Slovenian SSJ + SST train; POS tagger and lemmatiser on the same plus the
# SUK 1.1 ssj500k-tag and ambiga parts.
STANZA_PROV = (
    'Stanza &mdash; release <strong>1.14.0</strong>, package <code>default_accurate</code> '
    '(Slovenian <code>combined</code> models; the tagger and parser use the '
    '<a href="https://huggingface.co/EMBEDDIA/crosloengual-bert">CroSloEngual BERT</a> transformer), '
    'run with <a href="https://pypi.org/project/stanza/1.14.0/">stanza==1.14.0</a> and the model files of that release. '
    'Trained on UD Slovenian SSJ and SST (standardised transcription); the tagger and lemmatiser '
    'also on parts of the SUK 1.1 training corpus.'
)
POG_TRAINING_NOTE = (
    'Of the three tools, only SPOT-Trankit 1.3 has colloquial transcriptions in its training data. '
    'The training data of CLASSLA-Stanza and Stanza contain spoken Slovenian only in standardised transcription.'
)

CORPORA = []
for _cfg in v5.CORPORA:
    cfg = dict(_cfg)
    cfg["provenance"] = {
        "models": {**_cfg["provenance"]["models"], "stanza": STANZA_PROV},
        "data": _cfg["provenance"]["data"],
    }
    if cfg["key"] == "pog":
        cfg["provenance"]["note"] = POG_TRAINING_NOTE
    test_tag = _cfg["run_id"].split("_", 1)[1]  # e.g. "sl-ssj-ud-test_full"
    cfg["run_ids"] = {"trankit": _cfg["run_id"], "classla": _cfg["run_id"], "stanza": f"{STANZA_RUN}_{test_tag}"}
    CORPORA.append(cfg)


def accuracy_rows(gold_sents, metrics: Dict[str, Dict[str, float]], field: str, prefix: str) -> List[Dict]:
    """One row per gold label with every model's score (v2's rows, for N models)."""
    counts: Counter = Counter(tok[field] for sent in gold_sents for tok in sent["tokens"])
    rows = [
        {"tag": tag, "count": count, **{m: metrics[m].get(f"{prefix}_{tag}", 0.0) for m in MODEL_ORDER}}
        for tag, count in counts.items()
    ]
    rows.sort(key=lambda r: (*(r[m] for m in MODEL_ORDER), r["count"], r["tag"]), reverse=True)
    return rows


def build_corpus(cfg: Dict[str, Any], max_examples: int | None) -> Dict[str, Any]:
    gold_path = REPO_ROOT / cfg["gold"]
    paths = {}
    for m in MODEL_ORDER:
        run = cfg["run_ids"][m]
        paths[m] = (
            REPO_ROOT / "predictions" / "output" / f"{run}_{m}_aligned_predicted.conllu",
            REPO_ROOT / "results" / "output" / run / "diagnostics" / f"{m}_aligned_eval-tagged.txt",
        )
    for p in (gold_path, *(p for pair in paths.values() for p in pair)):
        if not p.exists():
            raise FileNotFoundError(f"Missing input for corpus {cfg['key']}: {p}")

    gold_sents = v2.read_conllu(gold_path)
    profiles = {m: v2.collect_model_profile(gold_sents, v2.read_conllu(paths[m][0]), max_examples) for m in MODEL_ORDER}
    metrics = {m: v2.parse_eval_metrics(paths[m][1]) for m in MODEL_ORDER}

    compared = {m: profiles[m]["totals"]["compared"] for m in MODEL_ORDER}
    if len(set(compared.values())) != 1:
        raise ValueError(f"Compared token counts differ between tools for {cfg['key']}: {compared}")

    return {
        "key": cfg["key"],
        "label": cfg["label"],
        "domain": cfg["domain"],
        "run_id": cfg["run_id"],
        "run_ids": cfg["run_ids"],
        "gold_sentences": len(gold_sents),
        "compared_tokens": compared["trankit"],
        "provenance": cfg["provenance"],
        "metrics": {
            m: v5.metrics_block(metrics[m], compared[m] - profiles[m]["totals"]["las_correct"]) for m in MODEL_ORDER
        },
        "deprel_accuracy_rows": accuracy_rows(gold_sents, metrics, "deprel", "LAS"),
        "upos_accuracy_rows": accuracy_rows(gold_sents, metrics, "upos", "UPOS"),
        "errors": {m: v5.tagger_error_block(profiles[m]) for m in MODEL_ORDER},
    }


def build_payload(max_examples: int | None) -> Dict[str, Any]:
    return {
        "models": MODELS,
        "model_order": MODEL_ORDER,
        "corpus_order": CORPUS_ORDER,
        "corpora": {cfg["key"]: build_corpus(cfg, max_examples) for cfg in CORPORA},
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the v6 (three-tool) data bundle.")
    parser.add_argument(
        "out_js",
        nargs="?",
        default=str(REPO_ROOT / "tables" / "comparison_table_v6_data.js"),
        help="Output JS data file (default: tables/comparison_table_v6_data.js).",
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
        "window.TABLE_DATA_V6 = "
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {out_path} ({out_path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
