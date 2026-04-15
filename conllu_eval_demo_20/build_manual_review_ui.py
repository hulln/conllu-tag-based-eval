#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


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

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip("\n")
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
            token_position = int(tok_id)
        except ValueError:
            token_position = len(tokens) + 1

        tokens.append(
            {
                "id": token_position,
                "form": cols[1],
                "lemma": cols[2],
                "upos": cols[3],
                "xpos": cols[4],
                "feats": cols[5],
                "head": cols[6],
                "deprel": cols[7].split(":")[0],
            }
        )

    flush()
    return sentences


def align_by_sent_id(
    gold_sentences: List[Dict[str, Any]],
    pred_sentences: List[Dict[str, Any]],
    model_name: str,
) -> List[Dict[str, Any]]:
    pred_by_sent_id: Dict[str, Dict[str, Any]] = {}
    for idx, sent in enumerate(pred_sentences, start=1):
        sent_id = sent.get("sent_id") or f"index-{idx}"
        pred_by_sent_id[sent_id] = sent

    aligned: List[Dict[str, Any]] = []
    missing: List[str] = []

    for idx, gold_sent in enumerate(gold_sentences, start=1):
        sent_id = gold_sent.get("sent_id") or f"index-{idx}"
        pred = pred_by_sent_id.get(sent_id)
        if pred is None:
            missing.append(sent_id)
            continue
        aligned.append(pred)

    if missing:
        first = ", ".join(missing[:5])
        raise ValueError(
            f"Missing {len(missing)} {model_name} sentences by sent_id. First missing: {first}"
        )

    return aligned


def build_review_data(
    gold_sentences: List[Dict[str, Any]],
    classla_sentences: List[Dict[str, Any]],
    trankit_sentences: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    review_rows: List[Dict[str, Any]] = []

    for sidx, (gold_sent, classla_sent, trankit_sent) in enumerate(
        zip(gold_sentences, classla_sentences, trankit_sentences), start=1
    ):
        sent_id = gold_sent.get("sent_id") or f"index-{sidx}"
        text = gold_sent.get("text") or ""

        gold_tokens = gold_sent.get("tokens", [])
        classla_tokens = classla_sent.get("tokens", [])
        trankit_tokens = trankit_sent.get("tokens", [])

        if not (len(gold_tokens) == len(classla_tokens) == len(trankit_tokens)):
            raise ValueError(
                f"Token-length mismatch in sent_id={sent_id}: "
                f"gold={len(gold_tokens)} classla={len(classla_tokens)} trankit={len(trankit_tokens)}"
            )

        tokens: List[Dict[str, Any]] = []
        classla_upos_ok = classla_uas_ok = classla_las_ok = 0
        trankit_upos_ok = trankit_uas_ok = trankit_las_ok = 0

        for tidx, (g, c, t) in enumerate(zip(gold_tokens, classla_tokens, trankit_tokens), start=1):
            if not (g["form"] == c["form"] == t["form"]):
                raise ValueError(
                    f"Token FORM mismatch in sent_id={sent_id}, token #{tidx}: "
                    f"gold={g['form']} classla={c['form']} trankit={t['form']}"
                )

            c_upos_ok = g["upos"] == c["upos"]
            c_head_ok = g["head"] == c["head"]
            c_deprel_ok = g["deprel"] == c["deprel"]

            t_upos_ok = g["upos"] == t["upos"]
            t_head_ok = g["head"] == t["head"]
            t_deprel_ok = g["deprel"] == t["deprel"]

            classla_upos_ok += int(c_upos_ok)
            classla_uas_ok += int(c_head_ok)
            classla_las_ok += int(c_head_ok and c_deprel_ok)

            trankit_upos_ok += int(t_upos_ok)
            trankit_uas_ok += int(t_head_ok)
            trankit_las_ok += int(t_head_ok and t_deprel_ok)

            tokens.append(
                {
                    "id": g["id"],
                    "form": g["form"],
                    "gold": {
                        "upos": g["upos"],
                        "head": g["head"],
                        "deprel": g["deprel"],
                    },
                    "classla": {
                        "upos": c["upos"],
                        "head": c["head"],
                        "deprel": c["deprel"],
                        "upos_ok": c_upos_ok,
                        "head_ok": c_head_ok,
                        "las_ok": c_head_ok and c_deprel_ok,
                    },
                    "trankit": {
                        "upos": t["upos"],
                        "head": t["head"],
                        "deprel": t["deprel"],
                        "upos_ok": t_upos_ok,
                        "head_ok": t_head_ok,
                        "las_ok": t_head_ok and t_deprel_ok,
                    },
                }
            )

        total = len(tokens)
        review_rows.append(
            {
                "sent_id": sent_id,
                "text": text,
                "tokens": tokens,
                "summary": {
                    "token_count": total,
                    "classla": {
                        "upos_ok": classla_upos_ok,
                        "uas_ok": classla_uas_ok,
                        "las_ok": classla_las_ok,
                    },
                    "trankit": {
                        "upos_ok": trankit_upos_ok,
                        "uas_ok": trankit_uas_ok,
                        "las_ok": trankit_las_ok,
                    },
                },
            }
        )

    return review_rows


def render_html(data: Dict[str, Any], title: str) -> str:
    payload = json.dumps(data, ensure_ascii=True, separators=(",", ":"))
    safe_title = (
        title.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )

    template = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__</title>
  <style>
    :root {{
      --bg: #f4f1ea;
      --ink: #1f2933;
      --muted: #6b7280;
      --panel: #fffdf8;
      --line: #d8d2c4;
      --accent: #1f6f8b;
      --good: #1a7f37;
      --bad: #b42318;
      --warn: #b54708;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
      background: radial-gradient(1000px 500px at 0% 0%, #efe8da 0%, var(--bg) 60%);
      color: var(--ink);
      line-height: 1.35;
    }}
    .wrap {{ max-width: 1280px; margin: 0 auto; padding: 18px; }}
    .top {{ display: grid; grid-template-columns: 1fr auto; gap: 12px; align-items: center; }}
    h1 {{ margin: 0; font-size: 1.2rem; }}
    .muted {{ color: var(--muted); font-size: 0.9rem; }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 12px;
      margin-top: 12px;
    }}
    .controls {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
    button, select, input[type="number"], textarea {{
      font: inherit;
      border: 1px solid var(--line);
      background: #fff;
      border-radius: 8px;
      padding: 7px 10px;
    }}
    button {{ cursor: pointer; }}
    button.primary {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
    .badge {{
      display: inline-block;
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 3px 9px;
      font-size: 0.8rem;
      background: #fff;
    }}
    .grid {{ display: grid; grid-template-columns: 360px 1fr; gap: 12px; margin-top: 12px; }}
    @media (max-width: 1050px) {{ .grid {{ grid-template-columns: 1fr; }} }}
    .stats dt {{ font-size: 0.82rem; color: var(--muted); }}
    .stats dd {{ margin: 0 0 8px 0; font-weight: 600; }}
    .sentence-title {{ font-weight: 700; margin-bottom: 6px; }}
    .sentence-text {{ font-size: 0.95rem; margin-bottom: 8px; }}
    .decision-group {{ display: grid; gap: 6px; margin-bottom: 10px; }}
    .decision-item {{ display: flex; gap: 8px; align-items: center; }}
    .decision-item label {{ cursor: pointer; }}
    textarea {{ width: 100%; min-height: 90px; resize: vertical; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.84rem; }}
    th, td {{ border: 1px solid var(--line); padding: 5px 6px; text-align: left; vertical-align: top; }}
    th {{ position: sticky; top: 0; background: #f8f5ee; z-index: 1; }}
    .ok {{ color: var(--good); font-weight: 700; }}
    .bad {{ color: var(--bad); font-weight: 700; }}
    .hint {{ color: var(--warn); }}
    .token-row-warn {{ background: #fff8ee; }}
    .token-row-bad {{ background: #fff0f0; }}
    .table-wrap {{ max-height: 62vh; overflow: auto; border: 1px solid var(--line); border-radius: 10px; }}
    .small {{ font-size: 0.8rem; }}
    .summary-cards {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; margin-top: 8px; }}
    .card {{ border: 1px solid var(--line); border-radius: 8px; padding: 8px; background: #fff; }}
    .tree-layout {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; margin-top: 12px; }}
    @media (max-width: 1250px) {{ .tree-layout {{ grid-template-columns: 1fr; }} }}
    .tree-pane {{ border: 1px solid var(--line); border-radius: 8px; background: #fff; padding: 8px; min-height: 190px; }}
    .tree-pane-title {{ font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); margin-bottom: 6px; }}
    .tree-scroll {{ max-height: 290px; overflow: auto; padding-right: 4px; }}
    .dep-tree, .dep-tree ul {{ list-style: none; margin: 0; padding-left: 14px; }}
    .dep-tree > li {{ margin: 4px 0; }}
    .dep-tree ul {{ border-left: 1px dashed var(--line); margin-left: 8px; }}
    .tree-node {{ display: inline-block; border: 1px solid var(--line); border-radius: 7px; background: #faf8f2; padding: 2px 6px; margin: 2px 0; }}
    .tree-node.gold {{ background: #eef4ff; border-color: #b8d4ff; }}
    .tree-node.ok {{ background: #edf8f0; border-color: #b7e1c0; }}
    .tree-node.head {{ background: #fff8ea; border-color: #f2d39c; }}
    .tree-node.bad {{ background: #ffeceb; border-color: #f5b7b1; }}
    .tree-node.cycle {{ background: #fce8f1; border-color: #f3b3d1; }}
    .tree-meta {{ color: var(--muted); font-size: 0.76rem; margin-left: 4px; }}
    .tree-legend {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }}
    .legend-chip {{ border: 1px solid var(--line); border-radius: 999px; padding: 2px 8px; font-size: 0.75rem; background: #fff; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="top">
      <div>
        <h1>Manual Review: Gold vs CLASSLA vs Trankit</h1>
        <div class="muted">Subfolder-only reviewer. Approve sentence-by-sentence and export your review JSON.</div>
      </div>
      <div class="controls">
        <span id="progressBadge" class="badge">0 / 0 reviewed</span>
        <button id="exportBtn" class="primary">Export review</button>
      </div>
    </div>

    <div class="panel controls">
      <button id="prevBtn">Prev</button>
      <button id="nextBtn">Next</button>
      <button id="nextUnreviewedBtn">Next unreviewed</button>
      <label class="small">Go to sentence
        <input id="jumpInput" type="number" min="1" value="1" style="width:80px; margin-left:6px;">
      </label>
      <button id="jumpBtn">Go</button>
      <span id="indexLabel" class="badge"></span>
    </div>

    <div class="grid">
      <div>
        <div class="panel">
          <div id="sentHeader" class="sentence-title"></div>
          <div id="sentText" class="sentence-text"></div>
          <div class="summary-cards">
            <div class="card small" id="classlaSentenceCard"></div>
            <div class="card small" id="trankitSentenceCard"></div>
          </div>
        </div>

        <div class="panel">
          <div class="sentence-title">Your decision for this sentence</div>
          <div class="decision-group" id="decisionGroup">
            <div class="decision-item"><input type="radio" name="decision" id="d_trankit" value="trankit"><label for="d_trankit">Prefer Trankit</label></div>
            <div class="decision-item"><input type="radio" name="decision" id="d_classla" value="classla"><label for="d_classla">Prefer CLASSLA</label></div>
            <div class="decision-item"><input type="radio" name="decision" id="d_tie" value="tie"><label for="d_tie">Both equally good</label></div>
            <div class="decision-item"><input type="radio" name="decision" id="d_followup" value="followup"><label for="d_followup">Needs follow-up</label></div>
          </div>
          <div class="small muted">Tip: keyboard shortcuts 1/2/3/4 set decision, left/right arrows navigate.</div>
          <div style="margin-top:8px;" class="small">Note</div>
          <textarea id="noteBox" placeholder="Optional note about this sentence..."></textarea>
        </div>

        <div class="panel">
          <div class="sentence-title">Live review stats</div>
          <dl class="stats" id="statsBox"></dl>
        </div>
      </div>

      <div class="panel">
        <div class="sentence-title">Token-level comparison</div>
        <div class="small muted" style="margin-bottom:8px;">Rows are highlighted when both models miss LAS (red) or when exactly one model misses LAS (amber).</div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th><th>FORM</th>
                <th>Gold UPOS</th><th>Gold HEAD</th><th>Gold DEPREL</th>
                <th>C UPOS</th><th>C HEAD</th><th>C DEPREL</th><th>C LAS</th>
                <th>T UPOS</th><th>T HEAD</th><th>T DEPREL</th><th>T LAS</th>
              </tr>
            </thead>
            <tbody id="tokenBody"></tbody>
          </table>
        </div>

        <div class="sentence-title" style="margin-top:12px;">Dependency tree view</div>
        <div class="small muted">Each pane shows a tree for the same sentence. Gold is the reference; model nodes are colored by LAS correctness.</div>
        <div class="tree-legend">
          <span class="legend-chip">Gold tree node</span>
          <span class="legend-chip">Model LAS OK</span>
          <span class="legend-chip">Model head OK, relation wrong</span>
          <span class="legend-chip">Model head wrong</span>
        </div>
        <div class="tree-layout">
          <div class="tree-pane">
            <div class="tree-pane-title">Gold</div>
            <div id="treeGold" class="tree-scroll"></div>
          </div>
          <div class="tree-pane">
            <div class="tree-pane-title">CLASSLA</div>
            <div id="treeClassla" class="tree-scroll"></div>
          </div>
          <div class="tree-pane">
            <div class="tree-pane-title">Trankit</div>
            <div id="treeTrankit" class="tree-scroll"></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
  const DATA = __PAYLOAD__;
  const STORAGE_KEY = "manual_review_random20_v1";
  const rows = DATA.sentences || [];
  const state = {{ index: 0, decisions: {{}}, notes: {{}} }};

  function clamp(v, lo, hi) {{ return Math.max(lo, Math.min(hi, v)); }}
  function pct(n, d) {{ return d === 0 ? "0.00" : ((100 * n) / d).toFixed(2); }}

  function escapeHtml(value) {{
    return String(value ?? "_")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }}

  function loadState() {{
    try {{
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      const saved = JSON.parse(raw);
      if (saved && typeof saved === "object") {{
        state.index = clamp(Number(saved.index || 0), 0, Math.max(rows.length - 1, 0));
        state.decisions = saved.decisions || {{}};
        state.notes = saved.notes || {{}};
      }}
    }} catch (_err) {{}}
  }}

  function saveState() {{
    localStorage.setItem(STORAGE_KEY, JSON.stringify({{ index: state.index, decisions: state.decisions, notes: state.notes }}));
  }}

  function decisionOrderKey(value) {{
    if (value === "trankit") return 0;
    if (value === "classla") return 1;
    if (value === "tie") return 2;
    if (value === "followup") return 3;
    return 9;
  }}

  function nextUnreviewedFrom(startIdx) {{
    for (let i = startIdx; i < rows.length; i++) {{
      const sid = rows[i].sent_id;
      if (!state.decisions[sid]) return i;
    }}
    for (let i = 0; i < startIdx; i++) {{
      const sid = rows[i].sent_id;
      if (!state.decisions[sid]) return i;
    }}
    return startIdx;
  }}

  function textCell(v) {{
    return escapeHtml(v);
  }}

  function badge(ok) {{
    return ok ? '<span class="ok">OK</span>' : '<span class="bad">X</span>';
  }}

  function sentenceTotals(sent, model) {{
    const total = sent.summary.token_count;
    const s = sent.summary[model];
    return `UPOS ${s.upos_ok}/${total} (${pct(s.upos_ok, total)}%), UAS ${s.uas_ok}/${total} (${pct(s.uas_ok, total)}%), LAS ${s.las_ok}/${total} (${pct(s.las_ok, total)}%)`;
  }}

  function modelHead(tok, model) {{
    const raw = model === "gold" ? tok.gold.head : tok[model].head;
    const num = Number(raw);
    return Number.isFinite(num) ? num : 0;
  }}

  function modelDeprel(tok, model) {{
    return model === "gold" ? tok.gold.deprel : tok[model].deprel;
  }}

  function modelNodeClass(tok, model) {{
    if (model === "gold") return "tree-node gold";
    if (tok[model].las_ok) return "tree-node ok";
    if (tok[model].head_ok) return "tree-node head";
    return "tree-node bad";
  }}

  function buildDependencyTree(tokens, model) {{
    const ids = tokens.map((tok) => Number(tok.id)).sort((a, b) => a - b);
    const idToTok = new Map(tokens.map((tok) => [Number(tok.id), tok]));
    const children = new Map(ids.map((id) => [id, []]));
    const roots = [];

    tokens.forEach((tok) => {{
      const id = Number(tok.id);
      const head = modelHead(tok, model);
      if (head > 0 && children.has(head) && head !== id) {{
        children.get(head).push(id);
      }} else {{
        roots.push(id);
      }}
    }});

    children.forEach((arr) => arr.sort((a, b) => a - b));
    roots.sort((a, b) => a - b);
    const visited = new Set();

    function renderNode(id) {{
      const tok = idToTok.get(id);
      if (!tok) return "";

      if (visited.has(id)) {{
        return `<li><span class="tree-node cycle">#${id} cycle</span></li>`;
      }}

      visited.add(id);
      const head = modelHead(tok, model);
      const rel = modelDeprel(tok, model);
      const cls = modelNodeClass(tok, model);
      const label = `<strong>${textCell(tok.form)}</strong><span class="tree-meta">#${id} h=${textCell(head)} ${textCell(rel)}</span>`;
      const kids = children.get(id) || [];
      const kidsHtml = kids.map((kid) => renderNode(kid)).join("");
      return `<li><span class="${cls}">${label}</span>${kidsHtml ? `<ul>${kidsHtml}</ul>` : ""}</li>`;
    }}

    let html = roots.map((rid) => renderNode(rid)).join("");
    if (!html) {{
      html = `<li><span class="tree-node cycle">No root found</span></li>`;
    }}

    const leftovers = ids.filter((id) => !visited.has(id));
    if (leftovers.length) {{
      html += leftovers.map((id) => renderNode(id)).join("");
    }}

    return `<ul class="dep-tree">${html}</ul>`;
  }}

  function renderStats() {{
    const decisions = Object.values(state.decisions);
    const reviewed = decisions.length;
    const counts = {{ trankit: 0, classla: 0, tie: 0, followup: 0 }};
    decisions.forEach((d) => {{ if (counts[d] !== undefined) counts[d] += 1; }});

    let totalTokens = 0;
    let cLas = 0;
    let tLas = 0;
    rows.forEach((sent) => {{
      totalTokens += sent.summary.token_count;
      cLas += sent.summary.classla.las_ok;
      tLas += sent.summary.trankit.las_ok;
    }});

    const lines = [
      ["Reviewed sentences", `${reviewed}/${rows.length}`],
      ["Prefer Trankit", String(counts.trankit)],
      ["Prefer CLASSLA", String(counts.classla)],
      ["Tie", String(counts.tie)],
      ["Needs follow-up", String(counts.followup)],
      ["Auto LAS CLASSLA", `${pct(cLas, totalTokens)}% (${cLas}/${totalTokens})`],
      ["Auto LAS Trankit", `${pct(tLas, totalTokens)}% (${tLas}/${totalTokens})`],
    ];

    document.getElementById("statsBox").innerHTML = lines.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join("");
    document.getElementById("progressBadge").textContent = `${reviewed} / ${rows.length} reviewed`;
  }}

  function renderCurrent() {{
    const sent = rows[state.index];
    if (!sent) return;

    document.getElementById("indexLabel").textContent = `Sentence ${state.index + 1} / ${rows.length}`;
    document.getElementById("jumpInput").value = String(state.index + 1);
    document.getElementById("sentHeader").textContent = `sent_id: ${sent.sent_id}`;
    document.getElementById("sentText").textContent = sent.text || "";
    document.getElementById("classlaSentenceCard").innerHTML = `<strong>CLASSLA</strong><br>${sentenceTotals(sent, "classla")}`;
    document.getElementById("trankitSentenceCard").innerHTML = `<strong>Trankit</strong><br>${sentenceTotals(sent, "trankit")}`;

    const decision = state.decisions[sent.sent_id] || "";
    document.querySelectorAll('input[name="decision"]').forEach((input) => {{
      input.checked = input.value === decision;
    }});

    document.getElementById("noteBox").value = state.notes[sent.sent_id] || "";

    const tbody = document.getElementById("tokenBody");
    tbody.innerHTML = sent.tokens.map((tok) => {{
      const c = tok.classla;
      const t = tok.trankit;
      const bothWrong = !c.las_ok && !t.las_ok;
      const oneWrong = c.las_ok !== t.las_ok;
      const rowClass = bothWrong ? "token-row-bad" : (oneWrong ? "token-row-warn" : "");
      return `
        <tr class="${rowClass}">
          <td>${textCell(tok.id)}</td>
          <td>${textCell(tok.form)}</td>
          <td>${textCell(tok.gold.upos)}</td>
          <td>${textCell(tok.gold.head)}</td>
          <td>${textCell(tok.gold.deprel)}</td>
          <td>${textCell(c.upos)}</td>
          <td>${textCell(c.head)}</td>
          <td>${textCell(c.deprel)}</td>
          <td>${badge(c.las_ok)}</td>
          <td>${textCell(t.upos)}</td>
          <td>${textCell(t.head)}</td>
          <td>${textCell(t.deprel)}</td>
          <td>${badge(t.las_ok)}</td>
        </tr>`;
    }}).join("");

      document.getElementById("treeGold").innerHTML = buildDependencyTree(sent.tokens, "gold");
      document.getElementById("treeClassla").innerHTML = buildDependencyTree(sent.tokens, "classla");
      document.getElementById("treeTrankit").innerHTML = buildDependencyTree(sent.tokens, "trankit");

    renderStats();
    saveState();
  }}

  function setDecision(value) {{
    const sent = rows[state.index];
    state.decisions[sent.sent_id] = value;
    renderCurrent();
  }}

  function bindEvents() {{
    document.getElementById("prevBtn").addEventListener("click", () => {{
      state.index = clamp(state.index - 1, 0, rows.length - 1);
      renderCurrent();
    }});
    document.getElementById("nextBtn").addEventListener("click", () => {{
      state.index = clamp(state.index + 1, 0, rows.length - 1);
      renderCurrent();
    }});
    document.getElementById("nextUnreviewedBtn").addEventListener("click", () => {{
      state.index = nextUnreviewedFrom(state.index + 1);
      renderCurrent();
    }});
    document.getElementById("jumpBtn").addEventListener("click", () => {{
      const wanted = Number(document.getElementById("jumpInput").value || "1") - 1;
      state.index = clamp(wanted, 0, rows.length - 1);
      renderCurrent();
    }});

    document.querySelectorAll('input[name="decision"]').forEach((input) => {{
      input.addEventListener("change", (ev) => setDecision(ev.target.value));
    }});

    document.getElementById("noteBox").addEventListener("input", (ev) => {{
      const sent = rows[state.index];
      state.notes[sent.sent_id] = ev.target.value;
      saveState();
    }});

    document.getElementById("exportBtn").addEventListener("click", () => {{
      const payload = {
        created_from: DATA.meta,
        exported_at: new Date().toISOString(),
        decisions: state.decisions,
        notes: state.notes,
      };
      const blob = new Blob([JSON.stringify(payload, null, 2)], {{ type: "application/json" }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "manual_review_decisions.json";
      a.click();
      URL.revokeObjectURL(url);
    }});

    document.addEventListener("keydown", (ev) => {{
      if (ev.key === "ArrowLeft") {{
        state.index = clamp(state.index - 1, 0, rows.length - 1);
        renderCurrent();
      }} else if (ev.key === "ArrowRight") {{
        state.index = clamp(state.index + 1, 0, rows.length - 1);
        renderCurrent();
      }} else if (ev.key === "1") {{
        setDecision("trankit");
      }} else if (ev.key === "2") {{
        setDecision("classla");
      }} else if (ev.key === "3") {{
        setDecision("tie");
      }} else if (ev.key === "4") {{
        setDecision("followup");
      }}
    }});
  }}

  loadState();
  bindEvents();
  renderCurrent();
  </script>
</body>
</html>
"""

    normalized = template.replace("{{", "{").replace("}}", "}")
    return normalized.replace("__TITLE__", safe_title).replace("__PAYLOAD__", payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a step-by-step manual review UI for gold vs CLASSLA vs Trankit (subfolder-only)."
    )
    parser.add_argument(
        "--gold",
        default="data/random20.gold.conllu",
        help="Gold CoNLL-U file (relative to this script folder unless absolute).",
    )
    parser.add_argument(
        "--classla",
        default="predictions/classla_random20_aligned.conllu",
        help="CLASSLA aligned prediction file.",
    )
    parser.add_argument(
        "--trankit",
        default="predictions/trankit_random20_aligned.conllu",
        help="Trankit aligned prediction file.",
    )
    parser.add_argument(
        "--output",
        default="tables/manual_review.html",
        help="Output HTML path.",
    )
    parser.add_argument(
        "--title",
        default="Manual Review UI",
        help="HTML page title.",
    )
    return parser.parse_args()


def resolve_path(base_dir: Path, raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


def main() -> None:
    args = parse_args()
    base_dir = Path(__file__).resolve().parent

    gold_path = resolve_path(base_dir, args.gold)
    classla_path = resolve_path(base_dir, args.classla)
    trankit_path = resolve_path(base_dir, args.trankit)
    out_path = resolve_path(base_dir, args.output)

    gold_sentences = read_conllu(gold_path)
    classla_sentences_raw = read_conllu(classla_path)
    trankit_sentences_raw = read_conllu(trankit_path)

    classla_sentences = align_by_sent_id(gold_sentences, classla_sentences_raw, "CLASSLA")
    trankit_sentences = align_by_sent_id(gold_sentences, trankit_sentences_raw, "Trankit")

    review_rows = build_review_data(gold_sentences, classla_sentences, trankit_sentences)

    payload = {
        "meta": {
            "gold": str(gold_path),
            "classla": str(classla_path),
            "trankit": str(trankit_path),
            "sentence_count": len(review_rows),
        },
        "sentences": review_rows,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_html(payload, args.title), encoding="utf-8")

    print(f"Wrote manual review UI: {out_path}")
    print("Open this file in a browser and review sentence-by-sentence.")


if __name__ == "__main__":
    main()
