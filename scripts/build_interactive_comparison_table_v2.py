#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Sequence


DEPREL_BUCKETS = ("head_only", "both_wrong", "rel_only")
TAG_LAYERS = ("upos", "xpos", "lemma")


def read_conllu(path: Path) -> List[Dict[str, Any]]:
    sentences: List[Dict[str, Any]] = []
    tokens: List[Dict[str, Any]] = []
    meta: Dict[str, str] = {}

    def flush() -> None:
        nonlocal tokens, meta
        if tokens or meta:
            sentences.append(
                {
                    "sent_id": meta.get("sent_id"),
                    "text": meta.get("text"),
                    "tokens": tokens,
                }
            )
        tokens = []
        meta = {}

    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            flush()
            continue
        if line.startswith("#"):
            if line.startswith("# sent_id = "):
                meta["sent_id"] = line[len("# sent_id = "):].strip()
            elif line.startswith("# text = "):
                meta["text"] = line[len("# text = "):].strip()
            continue
        cols = line.split("\t")
        if len(cols) != 10:
            continue
        tok_id = cols[0]
        if "-" in tok_id or "." in tok_id:
            continue
        try:
            position = int(tok_id)
        except ValueError:
            position = len(tokens) + 1

        tokens.append(
            {
                "id": position,
                "form": cols[1],
                "lemma": cols[2],
                "upos": cols[3],
                "xpos": cols[4],
                "head": cols[6],
                "deprel": cols[7].split(":")[0],
            }
        )

    flush()
    return sentences


def align_sentences(gold_sents, pred_sents):
    if len(gold_sents) == len(pred_sents):
        text_total = text_matches = 0
        for g, p in zip(gold_sents, pred_sents):
            if g.get("text") and p.get("text"):
                text_total += 1
                if g["text"] == p["text"]:
                    text_matches += 1
        if text_total == 0 or text_matches / max(text_total, 1) >= 0.95:
            return [(i, g, i, p) for i, (g, p) in enumerate(zip(gold_sents, pred_sents))], [], []

    pred_by_text: Dict[str, list] = defaultdict(list)
    for idx, sent in enumerate(pred_sents):
        if sent.get("text"):
            pred_by_text[sent["text"]].append((idx, sent))

    pairs, unmatched_gold, used_pred = [], [], set()
    for gold_idx, gold_sent in enumerate(gold_sents):
        text = gold_sent.get("text")
        if text and pred_by_text.get(text):
            pred_idx, pred_sent = pred_by_text[text].pop(0)
            pairs.append((gold_idx, gold_sent, pred_idx, pred_sent))
            used_pred.add(pred_idx)
        else:
            unmatched_gold.append(gold_idx)

    unmatched_pred = [i for i in range(len(pred_sents)) if i not in used_pred]
    return pairs, unmatched_gold, unmatched_pred


def parse_eval_metrics(path: Path) -> Dict[str, float]:
    metrics: Dict[str, float] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "|" not in line or line.startswith("Metric") or line.startswith("-"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 4:
            continue
        try:
            metrics[parts[0]] = float(parts[3])
        except ValueError:
            continue
    return metrics


def sentence_html(tokens: Sequence[Dict[str, Any]], highlight_id: int) -> str:
    rendered = []
    for tok in tokens:
        form = html.escape(str(tok["form"]))
        if tok["id"] == highlight_id:
            form = f"<mark>{form}</mark>"
        rendered.append(form)
    return " ".join(rendered)


def collect_model_profile(
    gold_sents: Sequence[Dict[str, Any]],
    pred_sents: Sequence[Dict[str, Any]],
    max_examples: int | None,
) -> Dict[str, Any]:
    deprel_counters = {b: Counter() for b in DEPREL_BUCKETS}
    deprel_examples = {b: defaultdict(list) for b in DEPREL_BUCKETS}

    tag_counters = {layer: Counter() for layer in TAG_LAYERS}
    tag_examples = {layer: defaultdict(list) for layer in TAG_LAYERS}

    totals: Counter = Counter()
    pairs, _, _ = align_sentences(gold_sents, pred_sents)

    for gold_idx, gold_sent, _pred_idx, pred_sent in pairs:
        gold_tokens = gold_sent["tokens"]
        pred_tokens = pred_sent["tokens"]

        if len(gold_tokens) != len(pred_tokens):
            totals["skipped_len_mismatch"] += 1
            continue

        for gold_tok, pred_tok in zip(gold_tokens, pred_tokens):
            if gold_tok["form"] != pred_tok["form"]:
                totals["skipped_form_mismatch"] += 1
                continue

            totals["compared"] += 1
            sent_html = sentence_html(gold_tokens, gold_tok["id"])
            tok_id_str = str(gold_tok["id"])
            sid = gold_sent.get("sent_id") or str(gold_idx + 1)

            head_ok = gold_tok["head"] == pred_tok["head"]
            rel_ok = gold_tok["deprel"] == pred_tok["deprel"]

            if head_ok and rel_ok:
                totals["las_correct"] += 1
            else:
                if not head_ok and rel_ok:
                    bucket = "head_only"
                    key = gold_tok["deprel"]
                elif head_ok and not rel_ok:
                    bucket = "rel_only"
                    key = f"{gold_tok['deprel']}__to__{pred_tok['deprel']}"
                else:
                    bucket = "both_wrong"
                    key = f"{gold_tok['deprel']}__to__{pred_tok['deprel']}"

                deprel_counters[bucket][key] += 1
                exs = deprel_examples[bucket][key]
                if max_examples is None or len(exs) < max_examples:
                    exs.append({
                        "sid": sid,
                        "token": str(gold_tok["form"]),
                        "token_id": tok_id_str,
                        "gold": f"({gold_tok['head']},{gold_tok['deprel']})",
                        "pred": f"({pred_tok['head']},{pred_tok['deprel']})",
                        "sentence_html": sent_html,
                    })

            for layer, gold_field, pred_field in [
                ("upos", "upos", "upos"),
                ("xpos", "xpos", "xpos"),
                ("lemma", "lemma", "lemma"),
            ]:
                gold_val = gold_tok[gold_field]
                pred_val = pred_tok[pred_field]
                if gold_val != pred_val:
                    key = f"{gold_val}__to__{pred_val}"
                    tag_counters[layer][key] += 1
                    exs = tag_examples[layer][key]
                    if max_examples is None or len(exs) < max_examples:
                        exs.append({
                            "sid": sid,
                            "token": str(gold_tok["form"]),
                            "token_id": tok_id_str,
                            "gold": gold_val,
                            "pred": pred_val,
                            "sentence_html": sent_html,
                        })

    return {
        "deprel_counters": deprel_counters,
        "deprel_examples": {b: dict(rows) for b, rows in deprel_examples.items()},
        "tag_counters": tag_counters,
        "tag_examples": {layer: dict(rows) for layer, rows in tag_examples.items()},
        "totals": totals,
    }


def build_deprel_error_rows(trankit_profile: Dict[str, Any]) -> Dict[str, List[Dict]]:
    rows: Dict[str, List[Dict]] = {}
    for bucket in DEPREL_BUCKETS:
        bucket_rows = []
        for key, count in trankit_profile["deprel_counters"][bucket].items():
            if "__to__" in key:
                parts = key.split("__to__")
                label = f"{parts[0]} → {parts[1]}"
            else:
                label = key
            bucket_rows.append({"key": key, "label": label, "count": count})
        bucket_rows.sort(key=lambda r: r["count"], reverse=True)
        rows[bucket] = bucket_rows
    return rows


def build_tag_error_rows(trankit_profile: Dict[str, Any]) -> Dict[str, List[Dict]]:
    rows: Dict[str, List[Dict]] = {}
    for layer in TAG_LAYERS:
        layer_rows = []
        for key, count in trankit_profile["tag_counters"][layer].items():
            parts = key.split("__to__")
            label = f"{parts[0]} → {parts[1]}" if len(parts) == 2 else key
            gold = parts[0] if len(parts) == 2 else key
            pred = parts[1] if len(parts) == 2 else key
            layer_rows.append({"key": key, "label": label, "gold": gold, "pred": pred, "count": count})
        layer_rows.sort(key=lambda r: r["count"], reverse=True)
        rows[layer] = layer_rows
    return rows


def build_deprel_accuracy_rows(
    gold_sents: Sequence[Dict[str, Any]],
    trankit_metrics: Dict[str, float],
    classla_metrics: Dict[str, float],
) -> List[Dict]:
    gold_counts: Counter = Counter()
    for sent in gold_sents:
        for tok in sent["tokens"]:
            gold_counts[tok["deprel"]] += 1

    rows = []
    for rel, count in gold_counts.items():
        rows.append({
            "tag": rel,
            "count": count,
            "trankit": trankit_metrics.get(f"LAS_{rel}", 0.0),
            "classla": classla_metrics.get(f"LAS_{rel}", 0.0),
            "diff": trankit_metrics.get(f"LAS_{rel}", 0.0) - classla_metrics.get(f"LAS_{rel}", 0.0),
        })

    rows.sort(key=lambda r: (r["trankit"], r["classla"], r["count"], r["tag"]), reverse=True)
    return rows


def build_upos_accuracy_rows(
    gold_sents: Sequence[Dict[str, Any]],
    trankit_metrics: Dict[str, float],
    classla_metrics: Dict[str, float],
) -> List[Dict]:
    gold_counts: Counter = Counter()
    for sent in gold_sents:
        for tok in sent["tokens"]:
            gold_counts[tok["upos"]] += 1

    rows = []
    for upos, count in gold_counts.items():
        rows.append({
            "tag": upos,
            "count": count,
            "trankit": trankit_metrics.get(f"UPOS_{upos}", 0.0),
            "classla": classla_metrics.get(f"UPOS_{upos}", 0.0),
            "diff": trankit_metrics.get(f"UPOS_{upos}", 0.0) - classla_metrics.get(f"UPOS_{upos}", 0.0),
        })

    rows.sort(key=lambda r: (r["trankit"], r["classla"], r["count"], r["tag"]), reverse=True)
    return rows


ACK_DEFAULT = (
    "This work was supported by the research projects"
    " SPOT (model development, ARIS grant no. Z6-4617)"
    " and MAPCASE (model evaluation, ARIS grant no. J6-70213)."
    " The interactive website was developed by Nives H\u00fcll"
    " under the supervision of Kaja Dobrovoljc Zor."
)


def render_html(out_js_name: str, dataset_label: str = "SSJ-UD", ack_text: str = ACK_DEFAULT) -> str:
    out_js_name = html.escape(out_js_name, quote=True)
    dataset_label_esc = html.escape(dataset_label)
    ack_text_esc = html.escape(ack_text)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Error Analysis: SPOT-Trankit on {dataset_label_esc} test set</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 13px;
    background: #f8f7f4;
    color: #1a1a1a;
    padding: 36px 40px 60px;
    max-width: 980px;
    margin: 0 auto;
  }}
  h1 {{ font-size: 17px; font-weight: 600; letter-spacing: .01em; margin-bottom: 4px; }}
  .subtitle {{ font-size: 12px; color: #666; margin-bottom: 8px; font-weight: 300; line-height: 1.5; }}
  .provenance {{ font-size: 11px; color: #555; margin-bottom: 28px; line-height: 1.6; }}
  .provenance strong {{ color: #333; }}
  .provenance code {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10.5px;
    background: #efece6;
    padding: 1px 3px;
    border-radius: 2px;
  }}
  .provenance a {{
    color: #1f5f8f;
    text-decoration: none;
    border-bottom: 1px solid rgba(31,95,143,0.25);
  }}
  .provenance a:hover {{ border-bottom-color: rgba(31,95,143,0.75); }}
  h2 {{
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #444;
    margin: 32px 0 8px;
    padding-bottom: 4px;
    border-bottom: 1.5px solid #d0cdc7;
  }}
  h3 {{
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #555;
    margin: 18px 0 8px;
  }}
  table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; margin-bottom: 4px; }}
  .table-wrap {{
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    margin-bottom: 4px;
  }}
  .table-wrap-wide table {{ min-width: 640px; }}
  .table-wrap.expanded-scroll {{
    max-height: min(62vh, 520px);
    overflow: auto;
    scrollbar-gutter: stable;
  }}
  .table-wrap.expanded-scroll thead th {{
    position: sticky;
    top: 0;
    z-index: 4;
  }}
  th {{
    text-align: left;
    padding: 5px 10px;
    background: #1a1a1a;
    color: #f0ede8;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .04em;
    white-space: nowrap;
  }}
  th.right, td.right {{ text-align: right; }}
  td {{ padding: 4px 10px; border-bottom: 1px solid #e4e1db; vertical-align: middle; }}
  td.right {{ font-family: 'IBM Plex Mono', monospace; font-size: 12px; }}
  td.label {{ font-family: 'IBM Plex Mono', monospace; font-size: 11.5px; color: #333; }}
  tr:hover td {{ background: #f3f0eb; }}
  tr.classla-better td {{ background: #f0f4fb; }}
  tr.trankit-better td {{ background: #f0fbf5; }}
  tr.classla-better:hover td {{ background: #e6edf7; }}
  tr.trankit-better:hover td {{ background: #e6f7ed; }}
  tr.clickable-row td {{ cursor: pointer; }}
  tr.clickable-row:focus {{ outline: none; }}
  tr.clickable-row:focus-visible td {{ background: #ece9e2; }}
  tr.selected-row td {{ background: #fff7d4 !important; }}
  .no-data-row td {{
    color: #888;
    font-style: italic;
    background: #faf9f6 !important;
    text-align: left !important;
  }}
  .no-data-row td.right {{
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 12px;
  }}
  .pos {{ color: #1a7a3a; font-weight: 600; }}
  .neg {{ color: #b83232; font-weight: 600; }}
  .neut {{ color: #888; }}
  .overview {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 20px; }}
  .metric-box {{ background: #fff; border: 1px solid #ddd; padding: 14px 16px; border-radius: 2px; }}
  .metric-box .label {{ font-size: 10.5px; text-transform: uppercase; letter-spacing: .07em; color: #888; margin-bottom: 3px; }}
  .metric-box .val {{ font-family: 'IBM Plex Mono', monospace; font-size: 22px; font-weight: 600; color: #1a1a1a; }}
  .metric-box .sub {{ font-size: 10.5px; color: #aaa; margin-top: 2px; }}
  .metric-box.highlight {{ border-color: #1a7a3a; background: #f4fbf6; }}
  .classla-note {{ font-size: 11px; color: #555; margin-bottom: 16px; line-height: 1.6; background: #f3f0eb; padding: 8px 12px; border-radius: 2px; }}
  .bar-wrap {{
    display: inline-block;
    width: 70px;
    height: 8px;
    background: #e8e5e0;
    vertical-align: middle;
    margin-left: 6px;
    border-radius: 1px;
  }}
  .bar {{ display: block; height: 8px; border-radius: 1px; }}
  .bar-c {{ background: #4a6fa5; }}
  .bar-t {{ background: #2a9d5c; }}
  .example-item {{ border-top: 1px solid #ebe7df; padding-top: 8px; margin-top: 8px; }}
  .example-item:first-child {{ border-top: 0; padding-top: 0; margin-top: 0; }}
  .example-meta {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #666;
    margin-bottom: 6px;
    line-height: 1.45;
  }}
  .example-sentence {{ line-height: 1.6; color: #333; }}
  .examples-context {{
    margin-bottom: 10px;
    padding: 8px 10px;
    background: #f3f0eb;
    border-radius: 2px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10.5px;
    color: #555;
    line-height: 1.5;
    white-space: pre-wrap;
  }}
  mark {{ background: #f7e7a1; padding: 0 2px; }}
  .examples-backdrop {{
    position: fixed;
    inset: 0;
    background: rgba(26,26,26,0.14);
    z-index: 90;
    transition: opacity .15s;
  }}
  .examples-backdrop.hidden {{
    opacity: 0;
    pointer-events: none;
  }}
  .examples-panel {{
    position: fixed;
    top: 20px;
    right: 20px;
    width: 380px;
    max-height: calc(100vh - 40px);
    background: #fff;
    border: 1.5px solid #1a1a1a;
    border-radius: 3px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.13);
    display: flex;
    flex-direction: column;
    z-index: 100;
    transition: opacity .15s, transform .15s;
  }}
  .examples-panel.hidden {{
    opacity: 0;
    pointer-events: none;
    transform: translateY(-6px);
  }}
  .examples-panel-header {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 8px;
    padding: 10px 12px 8px;
    border-bottom: 1px solid #e4e1db;
    background: #1a1a1a;
    border-radius: 2px 2px 0 0;
    flex-shrink: 0;
  }}
  .examples-panel-title {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    color: #f0ede8;
    line-height: 1.4;
    word-break: break-word;
  }}
  .examples-panel-close {{
    background: none;
    border: none;
    color: #aaa;
    cursor: pointer;
    font-size: 16px;
    line-height: 1;
    padding: 0 2px;
    flex-shrink: 0;
    margin-top: -1px;
  }}
  .examples-panel-close:hover {{ color: #fff; }}
  .examples-panel-body {{
    overflow-y: auto;
    padding: 10px 12px 12px;
    flex: 1;
  }}
  @media (max-width: 820px) {{
    .examples-panel {{ width: calc(100vw - 24px); right: 12px; }}
  }}
  .note {{ font-size: 11px; color: #888; margin-top: 8px; line-height: 1.6; }}
  .controls, .toolbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin: 8px 0 10px;
    flex-wrap: wrap;
  }}
  .count-meta {{
    display: flex;
    align-items: baseline;
    gap: 8px;
    flex-wrap: wrap;
  }}
  .count-meta .note {{
    margin-top: 0;
  }}
  .control-note {{ flex: 1 1 280px; max-width: 560px; margin: 0; }}
  .control-main {{
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: flex-end;
  }}
  input[type="search"] {{
    border: 1px solid #d7d2cb;
    background: #fff;
    padding: 7px 9px;
    font: inherit;
    min-width: 220px;
    transition: border-color .14s ease, box-shadow .14s ease, background .14s ease;
  }}
  input[type="search"]:focus {{
    outline: none;
    border-color: #b8b0a4;
    box-shadow: 0 0 0 2px rgba(31,95,143,0.10);
  }}
  .toggle-btn {{
    border: 1px solid #d7d2cb;
    background: #fff;
    color: #333;
    padding: 6px 10px;
    font: inherit;
    cursor: pointer;
    transition: background .14s ease, border-color .14s ease, color .14s ease;
  }}
  .toggle-btn:hover {{
    background: #f3f0eb;
    border-color: #c8c1b5;
  }}
  .toggle-btn[hidden] {{ display: none; }}
  .toggle-btn.active {{ background: #1a1a1a; color: #f0ede8; border-color: #1a1a1a; }}
  .inline-toggle {{
    border: none;
    background: none;
    padding: 0;
    font: inherit;
    font-size: 11px;
    color: #888;
    line-height: 1.6;
    cursor: pointer;
    text-decoration: underline;
    text-underline-offset: 2px;
    transition: color .14s ease;
  }}
  .inline-toggle:hover {{
    color: #444;
  }}
  .inline-toggle[hidden] {{ display: none; }}
  .control-label {{
    font-size: 11px;
    color: #666;
    margin-right: 6px;
  }}
  .ack {{ font-size: 12px; color: #444; line-height: 1.7; margin-top: 8px; }}
  /* Column sort — same design as v1 */
  th.sortable {{ cursor: pointer; user-select: none; }}
  th.sortable::after {{
    content: '↕';
    display: inline-block;
    margin-left: 5px;
    color: #a9a39a;
    font-size: 10px;
  }}
  th.sortable[aria-sort="ascending"]::after {{ content: '↑'; color: #f0ede8; }}
  th.sortable[aria-sort="descending"]::after {{ content: '↓'; color: #f0ede8; }}
  th.sortable[aria-sort] {{ background: #333; }}
  /* Action buttons (export/copy) */
  .action-btn {{
    border: none;
    background: none;
    color: #aaa;
    font-size: 10.5px;
    font-family: 'IBM Plex Mono', monospace;
    cursor: pointer;
    padding: 3px 7px;
    border-radius: 2px;
    letter-spacing: .02em;
    transition: color .14s ease, background .14s ease;
  }}
  .action-btn:hover {{ color: #222; background: #ede9e3; }}
  .action-btns {{
    display: flex;
    gap: 2px;
    align-items: center;
    margin-left: 6px;
  }}
  button:focus-visible,
  input[type="search"]:focus-visible {{
    outline: 2px solid rgba(31,95,143,0.35);
    outline-offset: 2px;
  }}
  /* Deprel stacked buckets */
  .deprel-bucket .bucket-header {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 6px;
    margin-top: 18px;
  }}
  .deprel-bucket .bucket-header h3 {{ margin: 0; }}
  .deprel-bucket table {{ margin-bottom: 0; }}
  .deprel-bucket .bucket-toggle {{
    display: block;
    width: 100%;
    margin-top: 4px;
    text-align: center;
    border: 1px solid #d7d2cb;
    background: #fff;
    color: #555;
    font: inherit;
    font-size: 11px;
    padding: 4px 8px;
    cursor: pointer;
  }}
  .deprel-bucket .bucket-toggle:hover {{ background: #f3f0eb; }}
  /* MSD tooltip */
  .has-tip {{ position: relative; cursor: help; }}
  .has-tip::after {{
    content: attr(data-tip);
    position: absolute;
    left: 0; top: 100%;
    margin-top: 4px;
    background: #1a1a1a;
    color: #f0ede8;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10.5px;
    line-height: 1.5;
    white-space: pre;
    padding: 6px 9px;
    border-radius: 2px;
    pointer-events: none;
    opacity: 0;
    transform: translateY(-4px);
    transition: opacity .12s, transform .12s;
    z-index: 200;
    min-width: 180px;
    max-width: min(320px, calc(100vw - 48px));
    white-space: pre-wrap;
  }}
  .has-tip:hover::after,
  tr.clickable-row:focus .has-tip::after,
  tr.clickable-row:focus-visible .has-tip::after {{
    opacity: 1;
    transform: none;
  }}
  @media (max-width: 820px) {{
    body {{ padding: 24px 18px 36px; }}
    .overview {{ grid-template-columns: 1fr 1fr; }}
    .table-wrap-wide table {{ min-width: 560px; }}
    .control-main {{
      justify-content: flex-start;
    }}
  }}
</style>
</head>
<body>
<h1>Error Analysis: SPOT-Trankit on {dataset_label_esc} test set</h1>
<div class="subtitle" id="subtitle"></div>
<div class="provenance">
  <strong>Model:</strong>
  SPOT-Trankit &mdash; <a href="https://www.clarin.si/repository/xmlui/handle/11356/1997">CLARIN 11356/1997</a>,
  run with <a href="https://pypi.org/project/trankit/1.1.2/">trankit==1.1.2</a> using the Slovenian model archive
  <code>trankit-sl-ssj+sst.zip</code> (MD5 <code>0ddfac8d7445f8fa300f59dde1a00352</code>).
  CLASSLA-Stanza is included for reference and was run with <a href="https://pypi.org/project/classla/2.2.1/">classla==2.2.1</a>
  (<code>classla.Pipeline('sl', pos_use_lexicon=True)</code>).
  &nbsp;&middot;&nbsp;
  <strong>Data:</strong>
  <a href="https://github.com/UniversalDependencies/UD_Slovenian-SSJ/blob/master/sl_ssj-ud-test.conllu">UD Slovenian SSJ</a>
  test set, <a href="https://github.com/UniversalDependencies/UD_Slovenian-SSJ/tree/master">v2.17</a> (2025-10-22);
  predictions were run on <em>pre-tokenised</em> text (gold sentence and token boundaries supplied).
</div>

<h2 id="accuracy">Overall Accuracy &mdash; SPOT-Trankit</h2>
<div class="overview" id="overview"></div>
<div class="classla-note" id="classla-note"></div>

<h2 id="las-by-relation">LAS by Dependency Relation</h2>
<div class="controls">
  <div class="note control-note">Sorted by SPOT-Trankit LAS. Difference = SPOT-Trankit LAS &minus; CLASSLA LAS.</div>
  <div class="control-main">
    <label class="control-label" for="rel-filter">Search</label>
    <input id="rel-filter" type="search" placeholder="e.g. nsubj or obl">
    <div class="action-btns">
      <button class="action-btn" id="rel-csv-btn" title="Export all rows as CSV">&darr; CSV</button>
      <button class="action-btn" id="rel-md-btn" title="Copy visible rows as Markdown">&#x2398; MD</button>
    </div>
  </div>
</div>
<div class="toolbar">
  <div class="count-meta">
    <div class="note" id="rel-count-note"></div>
    <button id="rel-toggle" class="inline-toggle" type="button" hidden>Show more</button>
  </div>
</div>
<div class="table-wrap table-wrap-wide">
<table>
  <thead>
    <tr>
      <th>Relation</th>
      <th class="right">Gold</th>
      <th class="right">SPOT-Trankit LAS</th>
      <th class="right">CLASSLA LAS</th>
      <th class="right">Diff</th>
    </tr>
  </thead>
  <tbody id="rel-table"></tbody>
</table>
</div>

<h2 id="upos-accuracy">UPOS Accuracy by Tag</h2>
<div class="controls">
  <div class="note control-note">Sorted by SPOT-Trankit accuracy. Difference = SPOT-Trankit &minus; CLASSLA.</div>
  <div class="control-main">
    <label class="control-label" for="upos-acc-filter">Search</label>
    <input id="upos-acc-filter" type="search" placeholder="e.g. NOUN or VERB">
    <div class="action-btns">
      <button class="action-btn" id="upos-acc-csv-btn" title="Export all rows as CSV">&darr; CSV</button>
      <button class="action-btn" id="upos-acc-md-btn" title="Copy visible rows as Markdown">&#x2398; MD</button>
    </div>
  </div>
</div>
<div class="toolbar">
  <div class="count-meta">
    <div class="note" id="upos-acc-count-note"></div>
    <button id="upos-acc-toggle" class="inline-toggle" type="button" hidden>Show more</button>
  </div>
</div>
<div class="table-wrap table-wrap-wide">
<table>
  <thead>
    <tr>
      <th>UPOS</th>
      <th class="right">Gold</th>
      <th class="right">SPOT-Trankit</th>
      <th class="right">CLASSLA</th>
      <th class="right">Diff</th>
    </tr>
  </thead>
  <tbody id="upos-acc-table"></tbody>
</table>
</div>

<h2 id="errors-deprel">Most Common Errors &mdash; Dependency Relations</h2>
<div class="controls">
  <div class="note control-note">SPOT-Trankit only. Click a row for examples. <kbd>↑↓</kbd> to navigate, <kbd>Esc</kbd> to close.</div>
  <div class="control-main">
    <label class="control-label" for="deprel-err-filter">Search</label>
    <input id="deprel-err-filter" type="search" placeholder="e.g. nsubj or obl">
  </div>
</div>
<div id="deprel-error-sections"></div>

<h2 id="errors-upos">Most Common Errors &mdash; UPOS</h2>
<div class="controls">
  <div class="note control-note">SPOT-Trankit only. Click a row for examples.</div>
  <div class="control-main">
    <label class="control-label" for="upos-err-filter">Search</label>
    <input id="upos-err-filter" type="search" placeholder="e.g. NOUN">
    <button id="upos-merge-btn" class="toggle-btn" type="button">Merge (A&harr;B)</button>
    <div class="action-btns">
      <button class="action-btn" id="upos-err-csv-btn" title="Export all rows as CSV">&darr; CSV</button>
      <button class="action-btn" id="upos-err-md-btn" title="Copy visible rows as Markdown">&#x2398; MD</button>
    </div>
  </div>
</div>
<div class="toolbar">
  <div class="count-meta">
    <div class="note" id="upos-err-count-note"></div>
    <button id="upos-err-toggle" class="inline-toggle" type="button" hidden>Show more</button>
  </div>
</div>
<div class="table-wrap">
<table>
  <thead>
    <tr>
      <th>Error pair</th>
      <th class="right">Count</th>
    </tr>
  </thead>
  <tbody id="upos-err-table"></tbody>
</table>
</div>

<h2 id="errors-xpos">Most Common Errors &mdash; XPOS (MSD)</h2>
<div class="controls">
  <div class="note control-note">SPOT-Trankit only. Hover or focus a row for MSD decode. Click for examples.</div>
  <div class="control-main">
    <label class="control-label" for="xpos-err-filter">Search</label>
    <input id="xpos-err-filter" type="search" placeholder="e.g. Ncm or Vmpr">
    <button id="xpos-merge-btn" class="toggle-btn" type="button">Merge (A&harr;B)</button>
    <div class="action-btns">
      <button class="action-btn" id="xpos-err-csv-btn" title="Export all rows as CSV">&darr; CSV</button>
      <button class="action-btn" id="xpos-err-md-btn" title="Copy visible rows as Markdown">&#x2398; MD</button>
    </div>
  </div>
</div>
<div class="toolbar">
  <div class="count-meta">
    <div class="note" id="xpos-err-count-note"></div>
    <button id="xpos-err-toggle" class="inline-toggle" type="button" hidden>Show more</button>
  </div>
</div>
<div class="table-wrap">
<table>
  <thead>
    <tr>
      <th>Error pair</th>
      <th class="right">Count</th>
    </tr>
  </thead>
  <tbody id="xpos-err-table"></tbody>
</table>
</div>

<h2 id="errors-lemma">Most Common Errors &mdash; Lemma</h2>
<div class="controls">
  <div class="note control-note">SPOT-Trankit only. Click a row for examples.</div>
  <div class="control-main">
    <label class="control-label" for="lemma-err-filter">Search</label>
    <input id="lemma-err-filter" type="search" placeholder="e.g. biti or &lt;lemma&gt;">
    <button id="lemma-merge-btn" class="toggle-btn" type="button">Merge (A&harr;B)</button>
    <div class="action-btns">
      <button class="action-btn" id="lemma-err-csv-btn" title="Export all rows as CSV">&darr; CSV</button>
      <button class="action-btn" id="lemma-err-md-btn" title="Copy visible rows as Markdown">&#x2398; MD</button>
    </div>
  </div>
</div>
<div class="toolbar">
  <div class="count-meta">
    <div class="note" id="lemma-err-count-note"></div>
    <button id="lemma-err-toggle" class="inline-toggle" type="button" hidden>Show more</button>
  </div>
</div>
<div class="table-wrap">
<table>
  <thead>
    <tr>
      <th>Error pair</th>
      <th class="right">Count</th>
    </tr>
  </thead>
  <tbody id="lemma-err-table"></tbody>
</table>
</div>

<div class="examples-backdrop hidden" id="examples-backdrop"></div>
<div class="examples-panel hidden" id="examples-panel">
  <div class="examples-panel-header">
    <div class="examples-panel-title" id="examples-panel-title">Examples</div>
    <button class="examples-panel-close" id="examples-panel-close" title="Close">&times;</button>
  </div>
  <div class="examples-panel-body" id="examples-panel-body"></div>
</div>

<h2 id="acknowledgement">Acknowledgement</h2>
<div class="ack" id="ack-text">
  {ack_text_esc}
</div>

<script src="{out_js_name}"></script>
<script>
(function () {{
  const data = window.TABLE_DATA;
  if (!data) {{
    document.body.innerHTML = '<p>Table data not available.</p>';
    return;
  }}

  const subtitle = document.getElementById('subtitle');
  subtitle.textContent = `Run: ${{data.summary.run_id}} · Gold sentences: ${{data.summary.gold_sentences}} · Compared tokens: ${{data.summary.compared_tokens}}`;

  // Overview metrics
  const overview = document.getElementById('overview');
  const metricsOrder = [
    ['Lemma', 'trankit_lemma'],
    ['UPOS', 'trankit_upos'],
    ['XPOS', 'trankit_xpos'],
    ['UAS', 'trankit_uas'],
    ['LAS', 'trankit_las'],
  ];
  for (const [label, key] of metricsOrder) {{
    const val = data.summary[key];
    const box = document.createElement('div');
    box.className = 'metric-box' + (label === 'LAS' ? ' highlight' : '');
    box.innerHTML = `<div class="label">${{label}}</div><div class="val">${{val != null ? val.toFixed(2) : '—'}}</div><div class="sub">SPOT-Trankit</div>`;
    overview.appendChild(box);
  }}

  // CLASSLA note
  const clNote = document.getElementById('classla-note');
  const delta = data.summary.trankit_las - data.summary.classla_las;
  clNote.innerHTML = `For reference, <strong>CLASSLA-Stanza LAS</strong> on this run: <strong>${{data.summary.classla_las.toFixed(2)}}</strong> &nbsp;(&Delta; SPOT-Trankit &minus; CLASSLA = <span class="${{delta >= 0 ? 'pos' : 'neg'}}">${{delta >= 0 ? '+' : ''}}${{delta.toFixed(2)}}</span>). CLASSLA errors: ${{data.summary.classla_errors}}&nbsp;· SPOT-Trankit errors: ${{data.summary.trankit_errors}}.`;

  const ROW_LIMIT = 20;

  // --- Utility: export CSV from raw row data ---
  function downloadCSV(headers, rows, filename) {{
    const esc = function(v) {{ return '"' + String(v).replace(/"/g, '""') + '"'; }};
    const lines = [headers.map(esc).join(',')].concat(rows.map(function(r) {{ return r.map(esc).join(','); }}));
    const blob = new Blob(['\\ufeff' + lines.join('\\n')], {{type: 'text/csv;charset=utf-8;'}});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(a.href);
  }}

  // --- Utility: copy current DOM table view as Markdown ---
  function copyMarkdown(tableEl, btn) {{
    const ths = Array.from(tableEl.querySelectorAll('thead th')).map(function(th) {{ return th.textContent.trim().replace(/[▲▼]/g,'').trim(); }});
    const sep = ths.map(function() {{ return '---'; }});
    const bodyRows = Array.from(tableEl.querySelectorAll('tbody tr')).map(function(tr) {{
      return Array.from(tr.cells).map(function(td) {{ return td.textContent.trim(); }}).join(' | ');
    }});
    const md = ['| ' + ths.join(' | ') + ' |', '| ' + sep.join(' | ') + ' |']
      .concat(bodyRows.map(function(r) {{ return '| ' + r + ' |'; }})).join('\\n');
    navigator.clipboard.writeText(md).then(function() {{
      const orig = btn.textContent;
      btn.textContent = '✓';
      setTimeout(function() {{ btn.textContent = orig; }}, 1500);
    }});
  }}

  // --- Utility: make table headers clickable for sort (v1 design) ---
  function makeSortable(tableEl) {{
    tableEl.querySelectorAll('thead th').forEach(function(th, colIdx) {{
      th.classList.add('sortable');
      th.title = 'Click to sort';
      th.addEventListener('click', function() {{
        const cur = th.getAttribute('aria-sort');
        const asc = cur !== 'ascending';
        tableEl.querySelectorAll('thead th').forEach(function(h) {{ h.removeAttribute('aria-sort'); }});
        th.setAttribute('aria-sort', asc ? 'ascending' : 'descending');
        const tbody = tableEl.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        rows.sort(function(a, b) {{
          const ca = a.cells[colIdx], cb = b.cells[colIdx];
          const ta = ca ? ca.textContent.trim() : '';
          const tb = cb ? cb.textContent.trim() : '';
          const na = parseFloat(ta.replace(/[^0-9.\-+]/g, ''));
          const nb = parseFloat(tb.replace(/[^0-9.\-+]/g, ''));
          const isNum = !isNaN(na) && !isNaN(nb);
          const cmp = isNum ? (na - nb) : ta.localeCompare(tb);
          return asc ? cmp : -cmp;
        }});
        rows.forEach(function(r) {{ tbody.appendChild(r); }});
      }});
    }});
  }}

  function deltaClass(v, largerBetter) {{
    if (v === 0) return 'neut';
    return (largerBetter ? v > 0 : v < 0) ? 'pos' : 'neg';
  }}
  function deltaText(v, digits) {{
    const s = digits != null ? v.toFixed(digits) : String(v);
    return v > 0 ? '+' + s : s;
  }}

  function renderEmptyRow(tbody, colspan, message) {{
    const tr = document.createElement('tr');
    tr.className = 'no-data-row';
    tr.innerHTML = `<td colspan="${{colspan}}">${{message}}</td>`;
    tbody.appendChild(tr);
  }}

  function setCountNote(countEl, visibleCount, totalCount, expanded) {{
    countEl.textContent = `Showing ${{visibleCount}} / ${{totalCount}}`;
  }}

  function setExpandedScrollState(wrapper, expanded, totalCount) {{
    if (!wrapper) return;
    const active = expanded && totalCount > ROW_LIMIT;
    wrapper.classList.toggle('expanded-scroll', active);
    if (active) wrapper.scrollTop = 0;
  }}

  function wireClickableRow(tr, tbody, onActivate, ariaLabel) {{
    tr.classList.add('clickable-row');
    tr.tabIndex = 0;
    if (ariaLabel) tr.setAttribute('aria-label', ariaLabel);
    tr.addEventListener('focus', function() {{
      activeTbody = tbody;
    }});
    tr.addEventListener('click', function() {{
      activeTbody = tbody;
      onActivate();
    }});
    tr.addEventListener('keydown', function(e) {{
      if (e.key === 'Enter' || e.key === ' ') {{
        e.preventDefault();
        activeTbody = tbody;
        onActivate();
      }}
    }});
  }}

  // Generic accuracy table renderer
  function makeAccTable(tbodyId, countNoteId, toggleId, filterInputId, rows, labelKey) {{
    const tbody = document.getElementById(tbodyId);
    const countNote = document.getElementById(countNoteId);
    const toggle = document.getElementById(toggleId);
    const filterInput = filterInputId ? document.getElementById(filterInputId) : null;
    const tableWrap = tbody.closest('.table-wrap');
    let expanded = false;

    function render() {{
      const q = filterInput ? filterInput.value.trim().toLowerCase() : '';
      const filtered = q ? rows.filter(r => r[labelKey].toLowerCase().includes(q)) : rows;
      tbody.innerHTML = '';
      const visible = expanded ? filtered : filtered.slice(0, ROW_LIMIT);
      if (!filtered.length) {{
        renderEmptyRow(tbody, 5, 'No matching rows.');
      }} else {{
        for (const row of visible) {{
          const tr = document.createElement('tr');
          if (row.diff < 0) tr.classList.add('classla-better');
          if (row.diff > 0) tr.classList.add('trankit-better');
          const bar = v => `<span class="bar-wrap"><span class="bar bar-t" style="width:${{Math.max(0,Math.min(100,v))}}%"></span></span>`;
          tr.innerHTML = `
            <td class="label">${{row[labelKey]}}</td>
            <td class="right">${{row.count}}</td>
            <td class="right">${{row.trankit.toFixed(2)}} ${{bar(row.trankit)}}</td>
            <td class="right">${{row.classla.toFixed(2)}} <span class="bar-wrap"><span class="bar bar-c" style="width:${{Math.max(0,Math.min(100,row.classla))}}%"></span></span></td>
            <td class="right ${{deltaClass(row.diff, true)}}">${{deltaText(row.diff, 2)}}</td>
          `;
          tbody.appendChild(tr);
        }}
      }}
      setCountNote(countNote, visible.length, filtered.length, expanded);
      setExpandedScrollState(tableWrap, expanded, filtered.length);
      if (filtered.length <= ROW_LIMIT) {{ toggle.hidden = true; }}
      else {{ toggle.hidden = false; toggle.textContent = expanded ? 'Show less' : 'Show more'; }}
    }}

    if (filterInput) filterInput.addEventListener('input', () => {{ expanded = false; render(); }});
    toggle.addEventListener('click', () => {{ expanded = !expanded; render(); }});
    render();
  }}

  makeAccTable('rel-table', 'rel-count-note', 'rel-toggle', 'rel-filter', data.deprel_accuracy_rows, 'tag');
  makeAccTable('upos-acc-table', 'upos-acc-count-note', 'upos-acc-toggle', 'upos-acc-filter', data.upos_accuracy_rows, 'tag');

  // Sort + export wiring for accuracy tables
  (function() {{
    const relTbl = document.getElementById('rel-table').closest('table');
    makeSortable(relTbl);
    document.getElementById('rel-csv-btn').addEventListener('click', function() {{
      downloadCSV(
        ['Relation','Gold','SPOT-Trankit LAS','CLASSLA LAS','Diff'],
        data.deprel_accuracy_rows.map(function(r) {{ return [r.tag, r.count, r.trankit.toFixed(2), r.classla.toFixed(2), r.diff.toFixed(2)]; }}),
        'las-by-relation.csv'
      );
    }});
    document.getElementById('rel-md-btn').addEventListener('click', function() {{ copyMarkdown(relTbl, this); }});

    const uposAccTbl = document.getElementById('upos-acc-table').closest('table');
    makeSortable(uposAccTbl);
    document.getElementById('upos-acc-csv-btn').addEventListener('click', function() {{
      downloadCSV(
        ['UPOS','Gold','SPOT-Trankit','CLASSLA','Diff'],
        data.upos_accuracy_rows.map(function(r) {{ return [r.tag, r.count, r.trankit.toFixed(2), r.classla.toFixed(2), r.diff.toFixed(2)]; }}),
        'upos-accuracy.csv'
      );
    }});
    document.getElementById('upos-acc-md-btn').addEventListener('click', function() {{ copyMarkdown(uposAccTbl, this); }});
  }})();

  // MSD decoder (MULTEXT-E categories + JOS-style feature codes used in UD SSJ)
  function decodeMSD(tag) {{
    if (!tag || tag === '_') return tag;
    const CAT = {{
      N:'Noun', V:'Verb', A:'Adjective', P:'Pronoun',
      R:'Adverb', S:'Adposition', C:'Conjunction', M:'Numeral',
      Q:'Particle', I:'Interjection', X:'Residual', Z:'Punct',
      G:'Verb', K:'Numeral', L:'Particle', D:'Adposition', O:'Residual',
    }};
    const GEND = {{m:'masc', f:'fem', n:'neut'}};
    const NUM  = {{s:'sing', d:'dual', p:'plur'}};
    const CASE = {{n:'nom', g:'gen', d:'dat', a:'acc', l:'loc', i:'ins'}};
    const DEG  = {{p:'pos', c:'comp', s:'sup'}};
    const cat  = tag[0].toUpperCase();
    const f    = tag.slice(1).toLowerCase().split('');
    const out  = [CAT[cat] || cat];
    if (cat === 'N' || (cat === 'S' && tag.length > 3)) {{
      const TYPE = {{c:'common', p:'proper', o:'common'}};
      if (f[0]) out.push(TYPE[f[0]] || f[0]);
      if (f[1]) out.push(GEND[f[1]] || f[1]);
      if (f[2]) out.push(NUM[f[2]]  || f[2]);
      if (f[3]) out.push(CASE[f[3]] || f[3]);
      if (f[4] === 'y') out.push('animate');
    }} else if (cat === 'A') {{
      const TYPE = {{g:'general', s:'possessive', p:'participial'}};
      if (f[0]) out.push(TYPE[f[0]] || f[0]);
      if (f[2]) out.push(GEND[f[2]] || f[2]);
      if (f[3]) out.push(NUM[f[3]]  || f[3]);
      if (f[4]) out.push(CASE[f[4]] || f[4]);
    }} else if (cat === 'R') {{
      if (f[1]) out.push(DEG[f[1]] || f[1]);
    }} else if (cat === 'V' || cat === 'G') {{
      const TYPE = {{m:'main', a:'aux', c:'cop', o:'modal'}};
      const TENSE = {{p:'pres', f:'fut', i:'past', s:'cond'}};
      const ASP   = {{d:'perf', r:'imperf', b:'bi'}};
      if (f[0]) out.push(TYPE[f[0]]  || f[0]);
      if (f[1]) out.push(TENSE[f[1]] || f[1]);
      if (f[2]) out.push(ASP[f[2]]   || f[2]);
      if (f[3] && /[123]/.test(f[3])) out.push(f[3]+'p');
      if (f[4] && NUM[f[4]]) out.push(NUM[f[4]]);
    }} else if (cat === 'C') {{
      const TYPE = {{c:'coord', s:'subord'}};
      if (f[0]) out.push(TYPE[f[0]] || f[0]);
    }} else if (cat === 'P' || cat === 'Z') {{
      if (f.length) out.push(f.slice(0,4).join('-'));
    }} else if (cat === 'M' || cat === 'K') {{
      if (f.length) out.push(f.join('-'));
    }}
    return out.join(' · ');
  }}

  function msdTip(pair) {{
    const parts = pair.split(' → ');
    if (parts.length === 2) {{
      return `gold: ${{decodeMSD(parts[0].trim())}}\npred: ${{decodeMSD(parts[1].trim())}}`;
    }}
    const sym = pair.split(' ↔ ');
    if (sym.length === 2) {{
      return `${{decodeMSD(sym[0].trim())}} ↔ ${{decodeMSD(sym[1].trim())}}`;
    }}
    return decodeMSD(pair);
  }}

  // Examples panel
  const examplesBackdrop = document.getElementById('examples-backdrop');
  const examplesPanel = document.getElementById('examples-panel');
  const examplesPanelTitle = document.getElementById('examples-panel-title');
  const examplesPanelBody = document.getElementById('examples-panel-body');
  const examplesPanelClose = document.getElementById('examples-panel-close');
  let selectedRow = null;

  function closePanel() {{
    examplesPanel.classList.add('hidden');
    examplesBackdrop.classList.add('hidden');
    if (selectedRow) selectedRow.classList.remove('selected-row');
    selectedRow = null;
  }}
  examplesPanelClose.addEventListener('click', closePanel);
  examplesBackdrop.addEventListener('click', closePanel);

  let activeTbody = null;

  function selectRow(tr, tbody) {{
    if (selectedRow) selectedRow.classList.remove('selected-row');
    selectedRow = tr;
    tr.classList.add('selected-row');
    if (tbody) activeTbody = tbody;
    tr.addEventListener('dblclick', closePanel, {{ once: true }});
  }}

  // Keyboard nav: Escape closes, arrows move between rows
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape') {{
      if (!examplesPanel.classList.contains('hidden')) {{
        closePanel();
        e.preventDefault();
      }}
      return;
    }}
    if ((e.key === 'ArrowDown' || e.key === 'ArrowUp') && activeTbody) {{
      const target = e.target;
      if (target && target.closest && target.closest('input, textarea, select, button, a') && !target.closest('tr.clickable-row')) {{
        return;
      }}
      const rows = Array.from(activeTbody.querySelectorAll('tr.clickable-row'));
      if (!rows.length) return;
      const focusedRow = document.activeElement && document.activeElement.closest
        ? document.activeElement.closest('tr.clickable-row')
        : null;
      const currentRow = selectedRow && rows.includes(selectedRow)
        ? selectedRow
        : (focusedRow && rows.includes(focusedRow) ? focusedRow : null);
      if (!currentRow && focusedRow == null && document.activeElement && document.activeElement !== document.body && document.activeElement !== document.documentElement) {{
        return;
      }}
      const idx = currentRow ? rows.indexOf(currentRow) : -1;
      const next = e.key === 'ArrowDown'
        ? Math.min(idx + 1, rows.length - 1)
        : Math.max(idx - 1, 0);
      if (next !== idx) {{
        rows[next].focus({{ preventScroll: true }});
        rows[next].click();
        rows[next].scrollIntoView({{ block: 'nearest' }});
        e.preventDefault();
      }}
    }}
  }});

  function renderExamples(items, titleText, contextText) {{
    examplesPanelTitle.textContent = titleText || 'Examples';
    examplesPanelBody.innerHTML = '';
    if (contextText) {{
      const meta = document.createElement('div');
      meta.className = 'examples-context';
      meta.textContent = contextText;
      examplesPanelBody.appendChild(meta);
    }}
    if (!items || items.length === 0) {{
      const p = document.createElement('p');
      p.className = 'note';
      p.style.margin = '4px 0';
      p.textContent = 'No examples stored.';
      examplesPanelBody.appendChild(p);
    }} else {{
      for (const item of items) {{
        const div = document.createElement('div');
        div.className = 'example-item';
        div.innerHTML = `
          <div class="example-meta">sid=${{item.sid}} &middot; token=${{item.token}}#${{item.token_id}} &middot; gold=${{item.gold}} &middot; pred=${{item.pred}}</div>
          <div class="example-sentence">${{item.sentence_html}}</div>
        `;
        examplesPanelBody.appendChild(div);
      }}
    }}
    examplesBackdrop.classList.remove('hidden');
    examplesPanel.classList.remove('hidden');
    examplesPanelBody.scrollTop = 0;
  }}

  const bucketTitles = {{
    head_only: 'A) Wrong HEAD, correct DEPREL',
    both_wrong: 'B) Wrong HEAD and wrong DEPREL',
    rel_only: 'C) Correct HEAD, wrong DEPREL',
  }};

  const deprelFilter = document.getElementById('deprel-err-filter');
  const deprelSections = document.getElementById('deprel-error-sections');
  const allDeprelTbodies = {{}};
  const allDeprelToggles = {{}};
  const allDeprelExpanded = {{ head_only: false, both_wrong: false, rel_only: false }};

  function paintDeprel(bucket) {{
    const rows = data.deprel_error_rows[bucket] || [];
    const tbody = allDeprelTbodies[bucket];
    const toggle = allDeprelToggles[bucket];
    const q = deprelFilter ? deprelFilter.value.trim().toLowerCase() : '';
    const filtered = q ? rows.filter(r => r.label.toLowerCase().includes(q)) : rows;
    const expanded = allDeprelExpanded[bucket];
    tbody.innerHTML = '';
    const visible = expanded ? filtered : filtered.slice(0, ROW_LIMIT);
    if (!filtered.length) {{
      renderEmptyRow(tbody, 2, 'No matching rows.');
    }} else {{
      for (const row of visible) {{
        const tr = document.createElement('tr');
        tr.innerHTML = `<td class="label">${{row.label}}</td><td class="right">${{row.count}}</td>`;
        wireClickableRow(
          tr,
          tbody,
          function() {{
            selectRow(tr, tbody);
            const exs = (data.deprel_examples[bucket] || {{}})[row.key] || [];
            renderExamples(exs, `${{bucketTitles[bucket]}} · ${{row.label}} (${{exs.length}}/${{row.count}} examples)`);
          }},
          `Show examples for ${{row.label}}`
        );
        tbody.appendChild(tr);
      }}
    }}
    if (tbody._countNote) setCountNote(tbody._countNote, visible.length, filtered.length, expanded);
    setExpandedScrollState(tbody._tableWrap, expanded, filtered.length);
    if (filtered.length <= ROW_LIMIT) {{ toggle.hidden = true; }}
    else {{ toggle.hidden = false; toggle.textContent = expanded ? 'Show less' : 'Show more'; }}
  }}

  for (const bucket of ['head_only', 'both_wrong', 'rel_only']) {{
    const wrapper = document.createElement('div');
    wrapper.className = 'deprel-bucket';

    // Header row: title left, action buttons right
    const bucketHeader = document.createElement('div');
    bucketHeader.className = 'bucket-header';
    const heading = document.createElement('h3');
    heading.textContent = bucketTitles[bucket];
    bucketHeader.appendChild(heading);
    const actionBtns = document.createElement('div');
    actionBtns.className = 'action-btns';
    const csvBtn = document.createElement('button');
    csvBtn.className = 'action-btn'; csvBtn.title = 'Export all rows as CSV'; csvBtn.textContent = '\u2193 CSV';
    const mdBtn = document.createElement('button');
    mdBtn.className = 'action-btn'; mdBtn.title = 'Copy visible rows as Markdown'; mdBtn.textContent = '\u2398 MD';
    actionBtns.appendChild(csvBtn);
    actionBtns.appendChild(mdBtn);
    bucketHeader.appendChild(actionBtns);
    wrapper.appendChild(bucketHeader);

    // Count + show more above table
    const countBar = document.createElement('div');
    countBar.className = 'toolbar';
    const countMeta = document.createElement('div');
    countMeta.className = 'count-meta';
    const countNote = document.createElement('div');
    countNote.className = 'note';
    countMeta.appendChild(countNote);
    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'inline-toggle';
    toggle.hidden = true;
    allDeprelToggles[bucket] = toggle;
    toggle.addEventListener('click', function() {{
      allDeprelExpanded[bucket] = !allDeprelExpanded[bucket];
      paintDeprel(bucket);
    }});
    countMeta.appendChild(toggle);
    countBar.appendChild(countMeta);
    wrapper.appendChild(countBar);

    // Table
    const tableWrap = document.createElement('div');
    tableWrap.className = 'table-wrap';
    const table = document.createElement('table');
    table.innerHTML = `<thead><tr><th>Pattern</th><th class="right">Count</th></tr></thead><tbody></tbody>`;
    const tbody = table.querySelector('tbody');
    allDeprelTbodies[bucket] = tbody;
    // store countNote reference for paintDeprel
    tbody._countNote = countNote;
    tbody._tableWrap = tableWrap;
    tableWrap.appendChild(table);
    wrapper.appendChild(tableWrap);

    deprelSections.appendChild(wrapper);
    paintDeprel(bucket);
    makeSortable(table);
    (function(b, t, csv, md) {{
      csv.addEventListener('click', function() {{
        downloadCSV(['Pattern','Count'], (data.deprel_error_rows[b]||[]).map(function(r) {{ return [r.label, r.count]; }}), 'deprel-errors-' + b + '.csv');
      }});
      md.addEventListener('click', function() {{ copyMarkdown(t, md); }});
    }})(bucket, table, csvBtn, mdBtn);
  }}

  if (deprelFilter) {{
    deprelFilter.addEventListener('input', function() {{
      for (const b of ['head_only', 'both_wrong', 'rel_only']) {{
        allDeprelExpanded[b] = false;
        paintDeprel(b);
      }}
    }});
  }}

  // Generic tag error table: filter + merge + MSD tooltip for XPOS
  function makeTagErrTable(tbodyId, countNoteId, toggleId, mergeBtnId, filterInputId, layer) {{
    const rows = data.tag_error_rows[layer] || [];
    const tbody = document.getElementById(tbodyId);
    const countNote = document.getElementById(countNoteId);
    const toggle = document.getElementById(toggleId);
    const mergeBtn = document.getElementById(mergeBtnId);
    const filterInput = filterInputId ? document.getElementById(filterInputId) : null;
    const tableWrap = tbody.closest('.table-wrap');
    let expanded = false;
    let merged = false;

    function computeRows() {{
      const q = filterInput ? filterInput.value.trim().toLowerCase() : '';
      let base = rows;
      if (!merged) {{
        return q ? base.filter(r => r.label.toLowerCase().includes(q)) : base;
      }}
      const map = new Map();
      for (const row of base) {{
        const k = [row.gold, row.pred].sort().join('__sym__');
        const ex = map.get(k);
        if (ex) {{ ex.count += row.count; ex.keys.push(row.key); }}
        else {{
          const [a, b] = [row.gold, row.pred].sort();
          map.set(k, {{ key: k, label: a === b ? a : `${{a}} ↔ ${{b}}`, gold: a, pred: b, count: row.count, keys: [row.key] }});
        }}
      }}
      let merged_rows = Array.from(map.values()).sort((a, b) => b.count - a.count);
      return q ? merged_rows.filter(r => r.label.toLowerCase().includes(q)) : merged_rows;
    }}

    function render() {{
      const displayRows = computeRows();
      tbody.innerHTML = '';
      const visible = expanded ? displayRows : displayRows.slice(0, ROW_LIMIT);
      if (!displayRows.length) {{
        renderEmptyRow(tbody, 2, 'No matching rows.');
      }} else {{
        for (const row of visible) {{
          const tr = document.createElement('tr');
          const labelCell = document.createElement('td');
          labelCell.className = 'label';
          labelCell.textContent = row.label;
          let contextText = null;
          if (layer === 'xpos') {{
            contextText = msdTip(row.label);
            labelCell.classList.add('has-tip');
            labelCell.setAttribute('data-tip', contextText);
          }}
          const countCell = document.createElement('td');
          countCell.className = 'right';
          countCell.textContent = row.count;
          tr.appendChild(labelCell);
          tr.appendChild(countCell);
          wireClickableRow(
            tr,
            tbody,
            function() {{
              selectRow(tr, tbody);
              let exs = [];
              for (const k of (row.keys || [row.key])) {{
                exs = exs.concat((data.tag_examples[layer] || {{}})[k] || []);
              }}
              renderExamples(exs, `${{layer.toUpperCase()}} · ${{row.label}} (${{exs.length}} examples)`, contextText);
            }},
            `Show examples for ${{row.label}}`
          );
          tbody.appendChild(tr);
        }}
      }}
      setCountNote(countNote, visible.length, displayRows.length, expanded);
      setExpandedScrollState(tableWrap, expanded, displayRows.length);
      if (displayRows.length <= ROW_LIMIT) {{ toggle.hidden = true; }}
      else {{ toggle.hidden = false; toggle.textContent = expanded ? 'Show less' : 'Show more'; }}
    }}

    mergeBtn.addEventListener('click', function() {{
      merged = !merged;
      expanded = false;
      mergeBtn.classList.toggle('active', merged);
      mergeBtn.textContent = merged ? 'Show (A→B)' : 'Merge (A↔B)';
      render();
    }});
    toggle.addEventListener('click', () => {{ expanded = !expanded; render(); }});
    if (filterInput) filterInput.addEventListener('input', () => {{ expanded = false; render(); }});
    render();

    // Sort + export
    const tableEl = tbody.closest('table');
    makeSortable(tableEl);
    const csvBtn = document.getElementById(tbodyId.replace('-table', '-csv-btn'));
    const mdBtn  = document.getElementById(tbodyId.replace('-table', '-md-btn'));
    if (csvBtn) csvBtn.addEventListener('click', function() {{
      const exportRows = computeRows();
      downloadCSV(['Error pair','Count'], exportRows.map(function(r) {{ return [r.label, r.count]; }}), layer + '-errors.csv');
    }});
    if (mdBtn) mdBtn.addEventListener('click', function() {{ copyMarkdown(tableEl, mdBtn); }});
  }}

  makeTagErrTable('upos-err-table', 'upos-err-count-note', 'upos-err-toggle', 'upos-merge-btn', 'upos-err-filter', 'upos');
  makeTagErrTable('xpos-err-table', 'xpos-err-count-note', 'xpos-err-toggle', 'xpos-merge-btn', 'xpos-err-filter', 'xpos');
  makeTagErrTable('lemma-err-table', 'lemma-err-count-note', 'lemma-err-toggle', 'lemma-merge-btn', 'lemma-err-filter', 'lemma');


}})();
</script>
</body>
</html>
"""


def build_bundle(
    gold_path: Path,
    classla_pred_path: Path,
    trankit_pred_path: Path,
    classla_eval_tagged_path: Path,
    trankit_eval_tagged_path: Path,
    out_html_path: Path,
    out_js_path: Path,
    run_id: str,
    max_examples: int | None,
    dataset_label: str = "SSJ-UD",
    ack_text: str = ACK_DEFAULT,
) -> None:
    gold_sents = read_conllu(gold_path)
    classla_sents = read_conllu(classla_pred_path)
    trankit_sents = read_conllu(trankit_pred_path)

    trankit_profile = collect_model_profile(gold_sents, trankit_sents, max_examples)
    classla_profile = collect_model_profile(gold_sents, classla_sents, max_examples)

    classla_metrics = parse_eval_metrics(classla_eval_tagged_path)
    trankit_metrics = parse_eval_metrics(trankit_eval_tagged_path)

    compared = trankit_profile["totals"]["compared"]

    summary = {
        "run_id": run_id,
        "gold_sentences": len(gold_sents),
        "compared_tokens": compared,
        "trankit_las": trankit_metrics.get("LAS", 0.0),
        "trankit_uas": trankit_metrics.get("UAS", 0.0),
        "trankit_upos": trankit_metrics.get("UPOS", 0.0),
        "trankit_xpos": trankit_metrics.get("XPOS", 0.0),
        "trankit_lemma": trankit_metrics.get("Lemmas", 0.0),
        "classla_las": classla_metrics.get("LAS", 0.0),
        "trankit_errors": compared - trankit_profile["totals"]["las_correct"],
        "classla_errors": compared - classla_profile["totals"]["las_correct"],
    }

    deprel_error_rows_combined = build_deprel_error_rows(trankit_profile)

    deprel_examples = trankit_profile["deprel_examples"]

    payload = {
        "summary": summary,
        "deprel_error_rows": deprel_error_rows_combined,
        "deprel_examples": deprel_examples,
        "tag_error_rows": build_tag_error_rows(trankit_profile),
        "tag_examples": trankit_profile["tag_examples"],
        "deprel_accuracy_rows": build_deprel_accuracy_rows(gold_sents, trankit_metrics, classla_metrics),
        "upos_accuracy_rows": build_upos_accuracy_rows(gold_sents, trankit_metrics, classla_metrics),
    }

    out_html_path.parent.mkdir(parents=True, exist_ok=True)
    out_js_path.parent.mkdir(parents=True, exist_ok=True)
    out_js_path.write_text(
        "window.TABLE_DATA = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    out_html_path.write_text(render_html(out_js_path.name, dataset_label=dataset_label, ack_text=ack_text), encoding="utf-8")
    print(f"Wrote {out_html_path}")
    print(f"Wrote {out_js_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build v2 interactive comparison table HTML/data bundle.")
    parser.add_argument("gold", help="Path to gold CoNLL-U file.")
    parser.add_argument("trankit_pred", help="Path to SPOT-Trankit aligned prediction file.")
    parser.add_argument("classla_pred", help="Path to CLASSLA aligned prediction file.")
    parser.add_argument("trankit_eval_tagged", help="Path to SPOT-Trankit eval-tagged file.")
    parser.add_argument("classla_eval_tagged", help="Path to CLASSLA eval-tagged file.")
    parser.add_argument("out_html", help="Path to output HTML file.")
    parser.add_argument("out_js", help="Path to output JS data file.")
    parser.add_argument("--run-id", required=True, help="Run ID shown in the table header.")
    parser.add_argument("--dataset-label", default="SSJ-UD", help="Dataset label used in the page title and heading (e.g. SSJ-UD or SST-UD).")
    parser.add_argument("--ack-text", default=ACK_DEFAULT, help="Acknowledgement text for the bottom section.")
    parser.add_argument(
        "--examples-per-item",
        type=int,
        default=0,
        help="Max stored examples per error pattern; 0 stores all.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_bundle(
        gold_path=Path(args.gold),
        classla_pred_path=Path(args.classla_pred),
        trankit_pred_path=Path(args.trankit_pred),
        classla_eval_tagged_path=Path(args.classla_eval_tagged),
        trankit_eval_tagged_path=Path(args.trankit_eval_tagged),
        out_html_path=Path(args.out_html),
        out_js_path=Path(args.out_js),
        run_id=args.run_id,
        max_examples=None if args.examples_per_item <= 0 else args.examples_per_item,
        dataset_label=args.dataset_label,
        ack_text=args.ack_text,
    )


if __name__ == "__main__":
    main()
