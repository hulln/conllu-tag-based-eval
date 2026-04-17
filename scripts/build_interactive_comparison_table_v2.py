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


def render_html(out_js_name: str) -> str:
    out_js_name = html.escape(out_js_name, quote=True)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Error Analysis: SPOT-Trankit on SSJ-UD test set</title>
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
  tr.selected-row td {{ background: #fff7d4 !important; }}
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
  .example-box {{
    background: #fff;
    border: 1px solid #ddd;
    padding: 12px 14px;
    border-radius: 2px;
    min-height: 100px;
    margin-top: 10px;
  }}
  .example-box h3 {{ margin-top: 0; margin-bottom: 8px; }}
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
  mark {{ background: #f7e7a1; padding: 0 2px; }}
  .note {{ font-size: 11px; color: #888; margin-top: 8px; line-height: 1.6; }}
  .controls, .toolbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin: 8px 0 10px;
    flex-wrap: wrap;
  }}
  input[type="search"] {{ border: 1px solid #d7d2cb; background: #fff; padding: 7px 9px; font: inherit; min-width: 220px; }}
  .toggle-btn {{ border: 1px solid #d7d2cb; background: #fff; color: #333; padding: 6px 10px; font: inherit; cursor: pointer; }}
  .toggle-btn:hover {{ background: #f3f0eb; }}
  .toggle-btn[hidden] {{ display: none; }}
  .toggle-btn.active {{ background: #1a1a1a; color: #f0ede8; border-color: #1a1a1a; }}
  .control-label {{ font-size: 11px; color: #666; margin-right: 6px; }}
  .ack {{ font-size: 12px; color: #444; line-height: 1.7; margin-top: 8px; }}
  @media (max-width: 820px) {{
    body {{ padding: 24px 18px 36px; }}
    .overview {{ grid-template-columns: 1fr 1fr; }}
  }}
</style>
</head>
<body>
<h1>Error Analysis: SPOT-Trankit on SSJ-UD test set</h1>
<div class="subtitle" id="subtitle"></div>
<div class="provenance">
  <strong>Model:</strong>
  SPOT-Trankit &mdash; <a href="https://www.clarin.si/repository/xmlui/handle/11356/1997">CLARIN 11356/1997</a>
  (<code>trankit-sl-ssj+sst.zip</code>, MD5 <code>0ddfac8d7445f8fa300f59dde1a00352</code>)
  with <a href="https://pypi.org/project/trankit/1.1.2/">trankit==1.1.2</a>.
  CLASSLA-Stanza included for reference: <a href="https://pypi.org/project/classla/2.2.1/">classla==2.2.1</a>
  (<code>classla.Pipeline('sl', pos_use_lexicon=True)</code>).
  &nbsp;&middot;&nbsp;
  <strong>Data:</strong>
  <a href="https://github.com/UniversalDependencies/UD_Slovenian-SSJ">UD Slovenian SSJ</a> test set
  (<code>sl_ssj-ud-test.conllu</code>);
  predictions were run on <em>pre-tokenised</em> text (gold sentence and token boundaries supplied).
</div>

<h2>Overall Accuracy &mdash; SPOT-Trankit</h2>
<div class="overview" id="overview"></div>
<div class="classla-note" id="classla-note"></div>

<h2>LAS by Dependency Relation</h2>
<div class="controls">
  <div class="note" style="margin-top:0">Sorted by SPOT-Trankit LAS. Difference = SPOT-Trankit LAS &minus; CLASSLA LAS.</div>
  <div>
    <label class="control-label" for="rel-filter">Search</label>
    <input id="rel-filter" type="search" placeholder="e.g. nsubj or obl">
  </div>
</div>
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
<div class="toolbar">
  <div class="note" id="rel-count-note"></div>
  <button id="rel-toggle" class="toggle-btn" type="button" hidden>Show more</button>
</div>

<h2>UPOS Accuracy by Tag</h2>
<div class="controls">
  <div class="note" style="margin-top:0">Sorted by SPOT-Trankit accuracy. Difference = SPOT-Trankit &minus; CLASSLA.</div>
  <div>
    <label class="control-label" for="upos-acc-filter">Search</label>
    <input id="upos-acc-filter" type="search" placeholder="e.g. NOUN or VERB">
  </div>
</div>
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
<div class="toolbar">
  <div class="note" id="upos-acc-count-note"></div>
  <button id="upos-acc-toggle" class="toggle-btn" type="button" hidden>Show more</button>
</div>

<h2>Most Common Errors &mdash; Dependency Relations</h2>
<div class="note">Lower error count is better. Click a row to show examples below.
  Green rows = SPOT-Trankit makes fewer errors; blue rows = CLASSLA makes fewer errors.</div>
<div id="deprel-error-sections"></div>

<h2>Most Common Errors &mdash; UPOS</h2>
<div class="note">SPOT-Trankit only. Click a row for examples.</div>
<div class="toolbar" style="margin-top:10px">
  <span></span>
  <button id="upos-merge-btn" class="toggle-btn" type="button">Merge symmetric pairs (A&harr;B)</button>
</div>
<table>
  <thead>
    <tr>
      <th>Error pair</th>
      <th class="right">Count</th>
    </tr>
  </thead>
  <tbody id="upos-err-table"></tbody>
</table>
<div class="toolbar">
  <div class="note" id="upos-err-count-note"></div>
  <button id="upos-err-toggle" class="toggle-btn" type="button" hidden>Show more</button>
</div>

<h2>Most Common Errors &mdash; XPOS (MSD)</h2>
<div class="note">SPOT-Trankit only. Click a row for examples.</div>
<div class="toolbar" style="margin-top:10px">
  <span></span>
  <button id="xpos-merge-btn" class="toggle-btn" type="button">Merge symmetric pairs (A&harr;B)</button>
</div>
<table>
  <thead>
    <tr>
      <th>Error pair</th>
      <th class="right">Count</th>
    </tr>
  </thead>
  <tbody id="xpos-err-table"></tbody>
</table>
<div class="toolbar">
  <div class="note" id="xpos-err-count-note"></div>
  <button id="xpos-err-toggle" class="toggle-btn" type="button" hidden>Show more</button>
</div>

<h2>Most Common Errors &mdash; Lemma</h2>
<div class="note">SPOT-Trankit only. Click a row for examples.</div>
<div class="toolbar" style="margin-top:10px">
  <span></span>
  <button id="lemma-merge-btn" class="toggle-btn" type="button">Merge symmetric pairs (A&harr;B)</button>
</div>
<table>
  <thead>
    <tr>
      <th>Error pair</th>
      <th class="right">Count</th>
    </tr>
  </thead>
  <tbody id="lemma-err-table"></tbody>
</table>
<div class="toolbar">
  <div class="note" id="lemma-err-count-note"></div>
  <button id="lemma-err-toggle" class="toggle-btn" type="button" hidden>Show more</button>
</div>

<h2>Examples for Selected Row</h2>
<div class="note" id="examples-meta">Click any table row to view stored examples.</div>
<div class="example-box">
  <h3 id="examples-title">SPOT-Trankit</h3>
  <div id="trankit-examples" class="note">No examples.</div>
</div>

<h2>Acknowledgement</h2>
<div class="ack" id="ack-text">
  <em>(Acknowledgement text to be added.)</em>
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

  function deltaClass(v, largerBetter) {{
    if (v === 0) return 'neut';
    return (largerBetter ? v > 0 : v < 0) ? 'pos' : 'neg';
  }}
  function deltaText(v, digits) {{
    const s = digits != null ? v.toFixed(digits) : String(v);
    return v > 0 ? '+' + s : s;
  }}

  // Generic accuracy table renderer
  function makeAccTable(tbodyId, countNoteId, toggleId, filterInputId, rows, labelKey) {{
    const tbody = document.getElementById(tbodyId);
    const countNote = document.getElementById(countNoteId);
    const toggle = document.getElementById(toggleId);
    const filterInput = filterInputId ? document.getElementById(filterInputId) : null;
    let expanded = false;

    function render() {{
      const q = filterInput ? filterInput.value.trim().toLowerCase() : '';
      const filtered = q ? rows.filter(r => r[labelKey].toLowerCase().includes(q)) : rows;
      tbody.innerHTML = '';
      const visible = expanded ? filtered : filtered.slice(0, ROW_LIMIT);
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
      countNote.textContent = `Showing ${{visible.length}} / ${{filtered.length}}`;
      if (filtered.length <= ROW_LIMIT) {{ toggle.hidden = true; }}
      else {{ toggle.hidden = false; toggle.textContent = expanded ? 'Show less' : `Show more (${{filtered.length - ROW_LIMIT}})`; }}
    }}

    if (filterInput) filterInput.addEventListener('input', () => {{ expanded = false; render(); }});
    toggle.addEventListener('click', () => {{ expanded = !expanded; render(); }});
    render();
  }}

  makeAccTable('rel-table', 'rel-count-note', 'rel-toggle', 'rel-filter', data.deprel_accuracy_rows, 'tag');
  makeAccTable('upos-acc-table', 'upos-acc-count-note', 'upos-acc-toggle', 'upos-acc-filter', data.upos_accuracy_rows, 'tag');

  // Examples rendering
  const examplesMeta = document.getElementById('examples-meta');
  const trankitExamplesDiv = document.getElementById('trankit-examples');
  const examplesTitle = document.getElementById('examples-title');
  let selectedRow = null;

  function renderExamples(items, metaText, titleText) {{
    examplesMeta.textContent = metaText;
    examplesTitle.textContent = titleText || 'SPOT-Trankit';
    trankitExamplesDiv.innerHTML = '';
    if (!items || items.length === 0) {{
      trankitExamplesDiv.className = 'note';
      trankitExamplesDiv.textContent = 'No examples stored.';
      return;
    }}
    trankitExamplesDiv.className = '';
    for (const item of items) {{
      const div = document.createElement('div');
      div.className = 'example-item';
      div.innerHTML = `
        <div class="example-meta">sid=${{item.sid}} &middot; token=${{item.token}}#${{item.token_id}} &middot; gold=${{item.gold}} &middot; pred=${{item.pred}}</div>
        <div class="example-sentence">${{item.sentence_html}}</div>
      `;
      trankitExamplesDiv.appendChild(div);
    }}
  }}

  function selectRow(tr) {{
    if (selectedRow) selectedRow.classList.remove('selected-row');
    selectedRow = tr;
    if (tr) tr.classList.add('selected-row');
  }}

  // Deprel error sections (Trankit + CLASSLA comparison)
  const bucketTitles = {{
    head_only: 'A) Wrong HEAD, correct DEPREL',
    both_wrong: 'B) Wrong HEAD and wrong DEPREL',
    rel_only: 'C) Correct HEAD, wrong DEPREL',
  }};

  const deprelSections = document.getElementById('deprel-error-sections');
  for (const bucket of ['head_only', 'both_wrong', 'rel_only']) {{
    const rows = data.deprel_error_rows[bucket] || [];
    const wrapper = document.createElement('div');
    const toolbar = document.createElement('div');
    toolbar.className = 'toolbar';
    const heading = document.createElement('h3');
    heading.textContent = bucketTitles[bucket];
    heading.style.margin = '0';
    toolbar.appendChild(heading);
    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'toggle-btn';
    toolbar.appendChild(toggle);
    wrapper.appendChild(toolbar);

    const table = document.createElement('table');
    table.innerHTML = `
      <thead><tr>
        <th>Pattern</th>
        <th class="right">SPOT-Trankit</th>
        <th class="right">CLASSLA</th>
        <th class="right">Diff</th>
      </tr></thead>
      <tbody></tbody>
    `;
    const tbody = table.querySelector('tbody');
    let expanded = false;

    function paintDeprel(rows, tbody, toggle, expanded) {{
      tbody.innerHTML = '';
      const visible = expanded ? rows : rows.slice(0, ROW_LIMIT);
      for (const row of visible) {{
        const tr = document.createElement('tr');
        tr.className = 'clickable-row';
        if (row.diff < 0) tr.classList.add('trankit-better');
        if (row.diff > 0) tr.classList.add('classla-better');
        tr.innerHTML = `
          <td class="label">${{row.label}}</td>
          <td class="right">${{row.trankit_count}}</td>
          <td class="right">${{row.classla_count}}</td>
          <td class="right ${{deltaClass(row.diff, false)}}">${{deltaText(row.diff)}}</td>
        `;
        tr.addEventListener('click', function() {{
          selectRow(tr);
          const exs = (data.deprel_examples[bucket] || {{}})[row.key] || {{}};
          renderExamples(exs.trankit || [], `${{bucketTitles[bucket]}} · ${{row.label}} · ${{(exs.trankit||[]).length}}/${{row.trankit_count}} examples`, 'SPOT-Trankit');
          document.getElementById('examples-meta').scrollIntoView({{behavior:'smooth', block:'nearest'}});
        }});
        tbody.appendChild(tr);
      }}
      if (rows.length <= ROW_LIMIT) {{ toggle.hidden = true; }}
      else {{ toggle.hidden = false; toggle.textContent = expanded ? 'Show less' : `Show more (${{rows.length - ROW_LIMIT}})`; }}
    }}

    let deprelExpanded = false;
    paintDeprel(rows, tbody, toggle, deprelExpanded);
    toggle.addEventListener('click', function() {{
      deprelExpanded = !deprelExpanded;
      paintDeprel(rows, tbody, toggle, deprelExpanded);
    }});

    wrapper.appendChild(table);
    deprelSections.appendChild(wrapper);
  }}

  // Generic tag error table with merge toggle
  function makeTagErrTable(tbodyId, countNoteId, toggleId, mergeBtnId, layer) {{
    const rows = data.tag_error_rows[layer] || [];
    const tbody = document.getElementById(tbodyId);
    const countNote = document.getElementById(countNoteId);
    const toggle = document.getElementById(toggleId);
    const mergeBtn = document.getElementById(mergeBtnId);
    let expanded = false;
    let merged = false;

    function computeRows() {{
      if (!merged) return rows;
      const map = new Map();
      for (const row of rows) {{
        const k = [row.gold, row.pred].sort().join('__sym__');
        const existing = map.get(k);
        if (existing) {{
          existing.count += row.count;
          existing.keys.push(row.key);
        }} else {{
          const [a, b] = [row.gold, row.pred].sort();
          map.set(k, {{
            key: k,
            label: a === b ? a : `${{a}} ↔ ${{b}}`,
            gold: a,
            pred: b,
            count: row.count,
            keys: [row.key],
          }});
        }}
      }}
      return Array.from(map.values()).sort((a, b) => b.count - a.count);
    }}

    function render() {{
      const displayRows = computeRows();
      tbody.innerHTML = '';
      const visible = expanded ? displayRows : displayRows.slice(0, ROW_LIMIT);
      for (const row of visible) {{
        const tr = document.createElement('tr');
        tr.className = 'clickable-row';
        tr.innerHTML = `<td class="label">${{row.label}}</td><td class="right">${{row.count}}</td>`;
        tr.addEventListener('click', function() {{
          selectRow(tr);
          let exs = [];
          const keys = row.keys || [row.key];
          for (const k of keys) {{
            const e = (data.tag_examples[layer] || {{}})[k] || [];
            exs = exs.concat(e);
          }}
          renderExamples(exs, `${{layer.toUpperCase()}} errors · ${{row.label}} · ${{exs.length}} examples`, 'SPOT-Trankit');
          document.getElementById('examples-meta').scrollIntoView({{behavior:'smooth', block:'nearest'}});
        }});
        tbody.appendChild(tr);
      }}
      countNote.textContent = `Showing ${{visible.length}} / ${{displayRows.length}}`;
      if (displayRows.length <= ROW_LIMIT) {{ toggle.hidden = true; }}
      else {{ toggle.hidden = false; toggle.textContent = expanded ? 'Show less' : `Show more (${{displayRows.length - ROW_LIMIT}})`; }}
    }}

    mergeBtn.addEventListener('click', function() {{
      merged = !merged;
      expanded = false;
      mergeBtn.classList.toggle('active', merged);
      mergeBtn.textContent = merged ? 'Show asymmetric pairs (A→B)' : 'Merge symmetric pairs (A↔B)';
      render();
    }});
    toggle.addEventListener('click', () => {{ expanded = !expanded; render(); }});
    render();
  }}

  makeTagErrTable('upos-err-table', 'upos-err-count-note', 'upos-err-toggle', 'upos-merge-btn', 'upos');
  makeTagErrTable('xpos-err-table', 'xpos-err-count-note', 'xpos-err-toggle', 'xpos-merge-btn', 'xpos');
  makeTagErrTable('lemma-err-table', 'lemma-err-count-note', 'lemma-err-toggle', 'lemma-merge-btn', 'lemma');

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

    deprel_error_rows_trankit = build_deprel_error_rows(trankit_profile)
    deprel_error_rows_classla = build_deprel_error_rows(classla_profile)

    # Merge classla counts into deprel rows for comparison display
    deprel_error_rows_combined: Dict[str, Any] = {}
    for bucket in DEPREL_BUCKETS:
        classla_map = {r["key"]: r["count"] for r in deprel_error_rows_classla.get(bucket, [])}
        combined = []
        keys_seen = set()
        for row in deprel_error_rows_trankit.get(bucket, []):
            c = classla_map.get(row["key"], 0)
            combined.append({**row, "trankit_count": row["count"], "classla_count": c, "diff": row["count"] - c})
            keys_seen.add(row["key"])
        for key, count in classla_map.items():
            if key not in keys_seen:
                if "__to__" in key:
                    parts = key.split("__to__")
                    label = f"{parts[0]} → {parts[1]}"
                else:
                    label = key
                combined.append({"key": key, "label": label, "trankit_count": 0, "classla_count": count, "diff": -count})
        combined.sort(key=lambda r: (r["trankit_count"], r["classla_count"]), reverse=True)
        deprel_error_rows_combined[bucket] = combined

    # Build deprel examples: trankit only
    deprel_examples: Dict[str, Any] = {}
    for bucket in DEPREL_BUCKETS:
        deprel_examples[bucket] = {}
        for key, exs in trankit_profile["deprel_examples"].get(bucket, {}).items():
            deprel_examples[bucket][key] = {"trankit": exs}

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
    out_html_path.write_text(render_html(out_js_path.name), encoding="utf-8")
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
    )


if __name__ == "__main__":
    main()
