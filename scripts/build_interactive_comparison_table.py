#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Sequence


BUCKETS = ("head_only", "both_wrong", "rel_only")


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
                meta["sent_id"] = line[len("# sent_id = ") :].strip()
            elif line.startswith("# text = "):
                meta["text"] = line[len("# text = ") :].strip()
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
                "head": cols[6],
                "deprel": cols[7].split(":")[0],
            }
        )

    flush()
    return sentences


def align_sentences(gold_sents: Sequence[Dict[str, Any]], pred_sents: Sequence[Dict[str, Any]]):
    if len(gold_sents) == len(pred_sents):
        text_total = 0
        text_matches = 0
        for gold_sent, pred_sent in zip(gold_sents, pred_sents):
            if gold_sent.get("text") and pred_sent.get("text"):
                text_total += 1
                if gold_sent["text"] == pred_sent["text"]:
                    text_matches += 1
        if text_total == 0 or text_matches / max(text_total, 1) >= 0.95:
            return [
                (idx, gold_sent, idx, pred_sent)
                for idx, (gold_sent, pred_sent) in enumerate(zip(gold_sents, pred_sents))
            ], [], []

    pred_by_text: Dict[str, list] = defaultdict(list)
    for pred_idx, pred_sent in enumerate(pred_sents):
        text = pred_sent.get("text")
        if text:
            pred_by_text[text].append((pred_idx, pred_sent))

    pairs = []
    unmatched_gold = []
    used_pred = set()

    for gold_idx, gold_sent in enumerate(gold_sents):
        text = gold_sent.get("text")
        if text and pred_by_text.get(text):
            pred_idx, pred_sent = pred_by_text[text].pop(0)
            pairs.append((gold_idx, gold_sent, pred_idx, pred_sent))
            used_pred.add(pred_idx)
        else:
            unmatched_gold.append(gold_idx)

    unmatched_pred = [idx for idx in range(len(pred_sents)) if idx not in used_pred]
    return pairs, unmatched_gold, unmatched_pred


def parse_eval_metrics(path: Path) -> Dict[str, float]:
    metrics: Dict[str, float] = {}

    for line in path.read_text(encoding="utf-8").splitlines():
        if "|" not in line or line.startswith("Metric") or line.startswith("-"):
            continue

        parts = [part.strip() for part in line.split("|")]
        if len(parts) < 4:
            continue

        try:
            metrics[parts[0]] = float(parts[3])
        except ValueError:
            continue

    return metrics


def sentence_html(tokens: Sequence[Dict[str, Any]], highlight_id: int) -> str:
    rendered = []
    for token in tokens:
        form = html.escape(str(token["form"]))
        if token["id"] == highlight_id:
            form = f"<mark>{form}</mark>"
        rendered.append(form)
    return " ".join(rendered)


def bucket_key(bucket: str, gold_rel: str, pred_rel: str) -> str:
    if bucket == "head_only":
        return f"{gold_rel}_{gold_rel}"
    return f"{gold_rel}_to_{pred_rel}"


def bucket_label(bucket: str, key: str) -> str:
    if bucket == "head_only":
        return key.replace("_", "-", 1)
    return key.replace("_to_", "->")


def collect_model_profile(
    gold_sents: Sequence[Dict[str, Any]],
    pred_sents: Sequence[Dict[str, Any]],
    max_examples: int | None,
) -> Dict[str, Any]:
    counters = {bucket: Counter() for bucket in BUCKETS}
    examples = {bucket: defaultdict(list) for bucket in BUCKETS}
    totals = Counter()

    pairs, _unmatched_gold, _unmatched_pred = align_sentences(gold_sents, pred_sents)

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
            head_ok = gold_tok["head"] == pred_tok["head"]
            rel_ok = gold_tok["deprel"] == pred_tok["deprel"]

            if head_ok and rel_ok:
                totals["las_correct"] += 1
                continue

            if not head_ok and rel_ok:
                bucket = "head_only"
            elif head_ok and not rel_ok:
                bucket = "rel_only"
            else:
                bucket = "both_wrong"

            key = bucket_key(bucket, gold_tok["deprel"], pred_tok["deprel"])
            counters[bucket][key] += 1

            if max_examples is None or len(examples[bucket][key]) < max_examples:
                examples[bucket][key].append(
                    {
                        "sid": gold_sent.get("sent_id") or str(gold_idx + 1),
                        "token": str(gold_tok["form"]),
                        "token_id": str(gold_tok["id"]),
                        "gold": f"({gold_tok['head']},{gold_tok['deprel']})",
                        "pred": f"({pred_tok['head']},{pred_tok['deprel']})",
                        "sentence_html": sentence_html(gold_tokens, gold_tok["id"]),
                    }
                )

    return {
        "counters": counters,
        "examples": {bucket: dict(rows) for bucket, rows in examples.items()},
        "totals": totals,
    }


def merge_examples(classla_examples: Dict[str, Dict], trankit_examples: Dict[str, Dict]) -> Dict[str, Dict]:
    merged: Dict[str, Dict] = {}
    for bucket in BUCKETS:
        merged[bucket] = {}
        keys = set(classla_examples.get(bucket, {}).keys()) | set(trankit_examples.get(bucket, {}).keys())
        for key in keys:
            merged[bucket][key] = {
                "trankit": trankit_examples.get(bucket, {}).get(key, []),
                "classla": classla_examples.get(bucket, {}).get(key, []),
            }
    return merged


def build_error_rows(classla_profile: Dict[str, Any], trankit_profile: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    rows: Dict[str, List[Dict[str, Any]]] = {}

    for bucket in BUCKETS:
        keys = (
            set(classla_profile["counters"].get(bucket, {}).keys())
            | set(trankit_profile["counters"].get(bucket, {}).keys())
        )
        bucket_rows = []
        for key in keys:
            classla_count = classla_profile["counters"][bucket].get(key, 0)
            trankit_count = trankit_profile["counters"][bucket].get(key, 0)
            bucket_rows.append(
                {
                    "key": key,
                    "label": bucket_label(bucket, key),
                    "trankit_count": trankit_count,
                    "classla_count": classla_count,
                    "diff": trankit_count - classla_count,
                }
            )

        bucket_rows.sort(
            key=lambda row: (
                row["trankit_count"],
                row["classla_count"],
                abs(row["diff"]),
                row["label"],
            ),
            reverse=True,
        )
        rows[bucket] = bucket_rows

    return rows


def build_relation_rows(
    gold_sents: Sequence[Dict[str, Any]],
    classla_eval_tagged_path: Path,
    trankit_eval_tagged_path: Path,
) -> List[Dict[str, Any]]:
    gold_counts = Counter()
    for sent in gold_sents:
        for tok in sent["tokens"]:
            gold_counts[tok["deprel"]] += 1

    classla_metrics = parse_eval_metrics(classla_eval_tagged_path)
    trankit_metrics = parse_eval_metrics(trankit_eval_tagged_path)
    rows = []

    for rel, count in gold_counts.items():
        classla_las = classla_metrics.get(f"LAS_{rel}", 0.0)
        trankit_las = trankit_metrics.get(f"LAS_{rel}", 0.0)
        rows.append(
            {
                "rel": rel,
                "count": count,
                "trankit_las": trankit_las,
                "classla_las": classla_las,
                "diff": trankit_las - classla_las,
            }
        )

    rows.sort(key=lambda row: (row["trankit_las"], row["classla_las"], row["count"], row["rel"]), reverse=True)
    return rows


def render_html(out_js_name: str) -> str:
    out_js_name = html.escape(out_js_name, quote=True)
    return f"""<!DOCTYPE html>
<html lang="sl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Analiza napak: Trankit vs. CLASSLA-Stanza - SSJ-UD testna množica</title>
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
    border-bottom: 1px solid rgba(31, 95, 143, 0.25);
  }}
  .provenance a:hover {{ border-bottom-color: rgba(31, 95, 143, 0.75); }}
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
  .pos {{ color: #1a7a3a; font-weight: 600; }}
  .neg {{ color: #b83232; font-weight: 600; }}
  .neut {{ color: #888; }}
  .overview {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 28px; }}
  .metric-box {{ background: #fff; border: 1px solid #ddd; padding: 14px 16px; border-radius: 2px; }}
  .metric-box .label {{ font-size: 10.5px; text-transform: uppercase; letter-spacing: .07em; color: #888; margin-bottom: 3px; }}
  .metric-box .val {{ font-family: 'IBM Plex Mono', monospace; font-size: 22px; font-weight: 600; color: #1a1a1a; }}
  .metric-box .sub {{ font-size: 10.5px; color: #aaa; margin-top: 2px; }}
  .metric-box.highlight {{ border-color: #1a7a3a; background: #f4fbf6; }}
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
  .examples {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 10px; }}
  .example-box {{ background: #fff; border: 1px solid #ddd; padding: 12px 14px; border-radius: 2px; min-height: 120px; }}
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
  .control-label {{ font-size: 11px; color: #666; margin-right: 6px; }}
  @media (max-width: 820px) {{
    body {{ padding: 24px 18px 36px; }}
    .overview {{ grid-template-columns: 1fr 1fr; }}
    .examples {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<h1>Analiza napak: Trankit vs. CLASSLA-Stanza - SSJ-UD testna množica</h1>
<div class="subtitle" id="subtitle"></div>
<div class="provenance">
  <strong>Verzije/modelski viri:</strong>
  Trankit <a href="https://www.clarin.si/repository/xmlui/handle/11356/1997">CLARIN 11356/1997</a>
  (<code>trankit-sl-ssj+sst.zip</code>, MD5 <code>0ddfac8d7445f8fa300f59dde1a00352</code>) z
  <a href="https://pypi.org/project/trankit/1.1.2/">trankit==1.1.2</a> &nbsp;·&nbsp;
  CLASSLA <a href="https://pypi.org/project/classla/2.2.1/">classla==2.2.1</a>
  (<code>classla.Pipeline('sl', pos_use_lexicon=True)</code>).
</div>
<div class="overview" id="overview"></div>

<h2>Pregled napak po tipu</h2>
<div class="note">Nižje število napak je boljše. Klik na vrstico odpre konkretne primere spodaj.</div>
<div class="note">Privzeto je vsak blok napak razvrščen po stolpcu Trankit, od največ do najmanj napak.</div>
<div id="error-sections"></div>

<h2>LAS po relacijah</h2>
<div class="controls">
  <div class="note" style="margin-top:0">Privzeto razvrščeno po Trankit LAS. Razlika = Trankit LAS minus CLASSLA LAS.</div>
  <div>
    <label class="control-label" for="relation-filter">Iskanje relacij</label>
    <input id="relation-filter" type="search" placeholder="npr. nsubj ali obl">
  </div>
</div>
<table>
  <thead>
    <tr>
      <th>Relacija</th>
      <th class="right">Gold</th>
      <th class="right">Trankit LAS</th>
      <th class="right">CLASSLA LAS</th>
      <th class="right">Razlika</th>
    </tr>
  </thead>
  <tbody id="relation-table"></tbody>
</table>
<div class="toolbar">
  <div class="note" id="relation-count-note"></div>
  <button id="relation-toggle" class="toggle-btn" type="button" hidden>Prikaži več</button>
</div>

<h2>Primeri za izbrano vrstico</h2>
<div class="note" id="examples-meta">Prikažejo se vsi shranjeni primeri za izbrano vrstico.</div>
<div class="examples">
  <div class="example-box">
    <h3>Trankit</h3>
    <div id="trankit-examples" class="note">Ni primerov.</div>
  </div>
  <div class="example-box">
    <h3>CLASSLA</h3>
    <div id="classla-examples" class="note">Ni primerov.</div>
  </div>
</div>

<script src="{out_js_name}"></script>
<script>
  (function () {{
    const data = window.TABLE_DATA;
    if (!data) {{
      document.body.innerHTML = '<p>Primerjalni podatki niso na voljo.</p>';
      return;
    }}

    const subtitle = document.getElementById('subtitle');
    subtitle.textContent = `Run: ${{data.summary.run_id}} · Gold povedi: ${{data.summary.gold_sentences}} · Primerjani tokeni: ${{data.summary.compared_tokens}}`;

    const overview = document.getElementById('overview');
    const delta = data.summary.trankit_las - data.summary.classla_las;
    const overviewItems = [
      ['Trankit LAS', data.summary.trankit_las.toFixed(2), `${{data.summary.trankit_errors}} LAS napak`],
      ['CLASSLA LAS', data.summary.classla_las.toFixed(2), `${{data.summary.classla_errors}} LAS napak`],
      ['Razlika LAS', `${{delta >= 0 ? '+' : ''}}${{delta.toFixed(2)}}`, 'Trankit minus CLASSLA'],
      ['Primerjani tokeni', String(data.summary.compared_tokens), 'Iz gold poravnane primerjave'],
    ];
    for (const [label, value, sub] of overviewItems) {{
      const box = document.createElement('div');
      box.className = 'metric-box' + (label === 'Trankit LAS' ? ' highlight' : '');
      box.innerHTML = `
        <div class="label">${{label}}</div>
        <div class="val">${{value}}</div>
        <div class="sub">${{sub}}</div>
      `;
      overview.appendChild(box);
    }}

    const bucketTitles = {{
      head_only: 'A) Napačen HEAD, pravilen DEPREL',
      both_wrong: 'B) Napačen HEAD in napačen DEPREL',
      rel_only: 'C) Pravilen HEAD, napačen DEPREL',
    }};
    const ERROR_ROW_LIMIT = 20;
    const RELATION_ROW_LIMIT = 20;

    function deltaClass(value, largerIsBetter) {{
      if (value === 0) return 'neut';
      const better = largerIsBetter ? value > 0 : value < 0;
      return better ? 'pos' : 'neg';
    }}

    function deltaText(value, digits) {{
      if (digits === undefined) {{
        return value > 0 ? `+${{value}}` : String(value);
      }}
      const fixed = value.toFixed(digits);
      return value > 0 ? `+${{fixed}}` : fixed;
    }}

    function renderExampleColumn(target, items) {{
      target.innerHTML = '';
      if (!items || items.length === 0) {{
        target.className = 'note';
        target.textContent = 'Ni primerov.';
        return;
      }}
      target.className = '';

      const list = document.createElement('div');
      for (const item of items) {{
        const div = document.createElement('div');
        div.className = 'example-item';
        div.innerHTML = `
          <div class="example-meta">sid=${{item.sid}} · tok=${{item.token}}#${{item.token_id}} · gold=${{item.gold}} · pred=${{item.pred}}</div>
          <div class="example-sentence">${{item.sentence_html}}</div>
        `;
        list.appendChild(div);
      }}

      target.appendChild(list);
    }}

    const examplesMeta = document.getElementById('examples-meta');
    const classlaExamples = document.getElementById('classla-examples');
    const trankitExamples = document.getElementById('trankit-examples');

    function showExamples(bucket, key, label) {{
      const examples = (data.examples[bucket] || {{}})[key] || {{ trankit: [], classla: [] }};
      const rowTotals = (data.error_rows[bucket] || []).find(function (row) {{
        return row.key === key;
      }}) || {{ trankit_count: 0, classla_count: 0 }};
      examplesMeta.textContent = `${{bucketTitles[bucket]}} · ${{label}} · primeri: Trankit ${{examples.trankit.length}}/${{rowTotals.trankit_count}}, CLASSLA ${{examples.classla.length}}/${{rowTotals.classla_count}}`;
      renderExampleColumn(trankitExamples, examples.trankit);
      renderExampleColumn(classlaExamples, examples.classla);
    }}

    const errorSections = document.getElementById('error-sections');
    for (const bucket of ['head_only', 'both_wrong', 'rel_only']) {{
      const rows = data.error_rows[bucket] || [];
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
        <thead>
          <tr>
            <th>Vzorec</th>
            <th class="right">Trankit</th>
            <th class="right">CLASSLA</th>
            <th class="right">Razlika</th>
          </tr>
        </thead>
        <tbody></tbody>
      `;
      const tbody = table.querySelector('tbody');
      let expanded = false;

      function paintRows() {{
        tbody.innerHTML = '';
        const visible = expanded ? rows : rows.slice(0, ERROR_ROW_LIMIT);
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
          tr.addEventListener('click', function () {{
            showExamples(bucket, row.key, row.label);
          }});
          tbody.appendChild(tr);
        }}

        if (rows.length <= ERROR_ROW_LIMIT) {{
          toggle.hidden = true;
        }} else {{
          toggle.hidden = false;
          toggle.textContent = expanded ? 'Prikaži manj' : `Prikaži več (${{rows.length - ERROR_ROW_LIMIT}})`;
        }}
      }}

      toggle.addEventListener('click', function () {{
        expanded = !expanded;
        paintRows();
      }});

      wrapper.appendChild(table);
      errorSections.appendChild(wrapper);
      paintRows();
    }}

    const relationFilter = document.getElementById('relation-filter');
    const relationTable = document.getElementById('relation-table');
    const relationToggle = document.getElementById('relation-toggle');
    const relationCountNote = document.getElementById('relation-count-note');
    let relationsExpanded = false;

    function relationBar(value, cssClass) {{
      return `<span class="bar-wrap"><span class="bar ${{cssClass}}" style="width:${{Math.max(0, Math.min(100, value))}}%"></span></span>`;
    }}

    function renderRelations() {{
      const query = relationFilter.value.trim().toLowerCase();
      const filtered = data.relation_rows.filter(function (row) {{
        return !query || row.rel.toLowerCase().includes(query);
      }});
      relationTable.innerHTML = '';
      const visible = relationsExpanded ? filtered : filtered.slice(0, RELATION_ROW_LIMIT);
      for (const row of visible) {{
        const tr = document.createElement('tr');
        if (row.diff < 0) tr.classList.add('classla-better');
        if (row.diff > 0) tr.classList.add('trankit-better');
        tr.innerHTML = `
          <td class="label">${{row.rel}}</td>
          <td class="right">${{row.count}}</td>
          <td class="right">${{row.trankit_las.toFixed(2)}} ${{relationBar(row.trankit_las, 'bar-t')}}</td>
          <td class="right">${{row.classla_las.toFixed(2)}} ${{relationBar(row.classla_las, 'bar-c')}}</td>
          <td class="right ${{deltaClass(row.diff, true)}}">${{deltaText(row.diff, 2)}}</td>
        `;
        relationTable.appendChild(tr);
      }}

      relationCountNote.textContent = `Prikazanih relacij: ${{visible.length}} / ${{filtered.length}}`;
      if (filtered.length <= RELATION_ROW_LIMIT) {{
        relationToggle.hidden = true;
      }} else {{
        relationToggle.hidden = false;
        relationToggle.textContent = relationsExpanded ? 'Prikaži manj' : `Prikaži več (${{filtered.length - RELATION_ROW_LIMIT}})`;
      }}
    }}

    relationFilter.addEventListener('input', function () {{
      relationsExpanded = false;
      renderRelations();
    }});
    relationToggle.addEventListener('click', function () {{
      relationsExpanded = !relationsExpanded;
      renderRelations();
    }});
    renderRelations();
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

    classla_profile = collect_model_profile(gold_sents, classla_sents, max_examples)
    trankit_profile = collect_model_profile(gold_sents, trankit_sents, max_examples)

    classla_metrics = parse_eval_metrics(classla_eval_tagged_path)
    trankit_metrics = parse_eval_metrics(trankit_eval_tagged_path)
    compared = classla_profile["totals"]["compared"]

    summary = {
        "run_id": run_id,
        "gold_sentences": len(gold_sents),
        "compared_tokens": compared,
        "trankit_las": trankit_metrics.get("LAS", 0.0),
        "classla_las": classla_metrics.get("LAS", 0.0),
        "trankit_errors": compared - trankit_profile["totals"]["las_correct"],
        "classla_errors": compared - classla_profile["totals"]["las_correct"],
    }

    payload = {
        "summary": summary,
        "error_rows": build_error_rows(classla_profile, trankit_profile),
        "examples": merge_examples(classla_profile["examples"], trankit_profile["examples"]),
        "relation_rows": build_relation_rows(gold_sents, classla_eval_tagged_path, trankit_eval_tagged_path),
    }

    out_html_path.parent.mkdir(parents=True, exist_ok=True)
    out_js_path.parent.mkdir(parents=True, exist_ok=True)
    out_js_path.write_text(
        "window.TABLE_DATA = "
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    out_html_path.write_text(render_html(out_js_path.name), encoding="utf-8")

    print(f"Wrote interactive comparison table HTML to {out_html_path}")
    print(f"Wrote interactive comparison table data to {out_js_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the interactive comparison table HTML/data bundle.")
    parser.add_argument("gold", help="Path to gold CoNLL-U file.")
    parser.add_argument("trankit_pred", help="Path to Trankit aligned prediction file.")
    parser.add_argument("classla_pred", help="Path to CLASSLA aligned prediction file.")
    parser.add_argument("trankit_eval_tagged", help="Path to Trankit aligned eval-tagged file.")
    parser.add_argument("classla_eval_tagged", help="Path to CLASSLA aligned eval-tagged file.")
    parser.add_argument("out_html", help="Path to generated HTML file.")
    parser.add_argument("out_js", help="Path to generated JS data file.")
    parser.add_argument("--run-id", required=True, help="Run id shown in the table header.")
    parser.add_argument(
        "--examples-per-item",
        type=int,
        default=0,
        help="Maximum stored examples per model and error pattern; 0 stores all examples.",
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
