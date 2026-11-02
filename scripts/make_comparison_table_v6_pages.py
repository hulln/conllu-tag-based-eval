#!/usr/bin/env python3
"""Make tables/comparison_table_v6{,_sl}.html from the v5 pages (v5 files are only read).

    python3 scripts/make_comparison_table_v6_pages.py            # writes into tables/
    python3 scripts/build_interactive_comparison_table_v6.py     # the data file

v6 is v5 with Stanza 1.14 as a third tool: a draft notice, a "compare with"
switch per tool (one or both at once), each tool's own run in the Details box,
and the Slovenian Stanza texts. Every edit must match exactly once, so a changed
v5 page fails loudly instead of producing a half-edited v6 page.
"""
import sys
from pathlib import Path

TABLES = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "tables"

STANZA_PROV_SL = (
    "Stanza &mdash; izdaja <strong>1.14.0</strong>, paket <code>default_accurate</code> "
    "(slovenski modeli <code>combined</code>; označevalnik in razčlenjevalnik uporabljata transformer "
    '<a href="https://huggingface.co/EMBEDDIA/crosloengual-bert">CroSloEngual BERT</a>), '
    'pognana s <a href="https://pypi.org/project/stanza/1.14.0/">stanza==1.14.0</a> in datotekami modelov iz te izdaje. '
    "Naučena na UD Slovenian SSJ in SST (standardizirani zapis), označevalnik in lematizator tudi na delih "
    "učnega korpusa SUK 1.1."
)
POG_NOTE_SL = (
    "Od treh orodij ima le SPOT-Trankit 1.3 med učnimi podatki tudi pogovorni zapis. "
    "Učni podatki orodij CLASSLA-Stanza in Stanza vsebujejo govorjeno slovenščino le v standardiziranem zapisu."
)

DRAFT_CSS = """<meta name="robots" content="noindex,nofollow">
<style>
  .draft-note { max-width: 980px; margin: 0 0 14px; padding: 8px 12px; border-left: 3px solid #e12a26; background: #fff; font-size: 14px; color: #161616; }
  /* Compared with two tools: seven columns, so a narrower label and count column,
     headers that may wrap onto two lines, and shorter bars. */
  .table-wrap-wide table.compare-multi { min-width: 760px; }
  .table-wrap-wide table.compare-multi th:first-child,
  .table-wrap-wide table.compare-multi td:first-child { width: 14%; }
  .table-wrap-wide table.compare-multi th:nth-child(2),
  .table-wrap-wide table.compare-multi td:nth-child(2) { width: 10%; }
  table.compare-multi th { white-space: normal; vertical-align: bottom; line-height: 1.3; }
  table.compare-multi .bar-wrap { width: 48px; }
</style>
"""

COMMON = [
    ('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n',
     '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n' + DRAFT_CSS),
    ('<script src="comparison_table_v5_data.js"></script>', '<script src="comparison_table_v6_data.js"></script>'),
    ("const DATA = window.TABLE_DATA_V5;", "const DATA = window.TABLE_DATA_V6;"),
    ("  function otherKey() { return state.model === 'trankit' ? 'classla' : 'trankit'; }\n",
     "  function otherKeys() { return DATA.model_order.filter(k => k !== state.model); }\n"
     "  // Each tool has its own run; SPOT-Trankit and CLASSLA-Stanza share one.\n"
     "  function runId(c) { return (c.run_ids && c.run_ids[modelKey()]) || c.run_id; }\n"),
    ("  function otherLabel() { return labelOf(otherKey()); }\n", ""),
    ("  function otherShort() { return shortOf(otherKey()); }\n", ""),
    ("    const compareBtn = document.getElementById(cfg.compareBtnId);\n",
     "    // One \"compare with\" button per other tool (the static button is the template).\n"
     "    const compareTemplate = document.getElementById(cfg.compareBtnId);\n"
     "    const compareBtns = DATA.model_order.map(function(k) {\n"
     "      const b = compareTemplate.cloneNode(false);\n"
     "      b.removeAttribute('id');\n"
     "      b.dataset.key = k;\n"
     "      b.addEventListener('click', () => { compareWith = compareWith === k ? null : k; expanded = false; render(); });\n"
     "      compareTemplate.before(b);\n"
     "      return b;\n"
     "    });\n"
     "    compareTemplate.remove();\n"),
    ("    let compare = false;\n", "    let compareWith = null;  // key of the tool shown for comparison, or null\n"),
    ("      const mk = modelKey(), ok = otherKey();\n",
     "      if (compareWith === modelKey()) compareWith = null;\n"
     "      const mk = modelKey(), compare = compareWith !== null;\n"
     "      const ok = compare ? compareWith : otherKeys()[0];\n"),
    ("          `<th class=\"right\">${otherShort()}${cfg.headerSuffix}</th>` +\n",
     "          `<th class=\"right\">${shortOf(ok)}${cfg.headerSuffix}</th>` +\n"),
    ("      compareBtn.classList.toggle('active', compare);\n", ""),
    ("    compareBtn.addEventListener('click', () => { compare = !compare; expanded = false; render(); });\n", ""),
    ("        compare = false;\n", "        compareWith = null;\n"),
    ("        c.run_id,\n", "        runId(c),\n"),
]

EN = COMMON + [
    ('    <a href="comparison_table_v5_sl.html" hreflang="sl">SL</a>', '    <a href="comparison_table_v6_sl.html" hreflang="sl">SL</a>'),
    ('    <a href="comparison_table_v5.html" aria-current="page">EN</a>', '    <a href="comparison_table_v6.html" aria-current="page">EN</a>'),
    ('<header class="page-head">\n',
     '<div class="draft-note"><strong>Draft</strong> (2 November 2026): Stanza 1.14 added as a third tool. Not published yet; '
     'the published version is at <a href="https://orodja.cjvt.si/oznacevalnik/eval/">orodja.cjvt.si/oznacevalnik/eval</a>.</div>\n'
     '<header class="page-head">\n'),
    ("        ? `${cfg.subtitle} <em>Comparison shown: difference = ${modelLabel()} &minus; ${otherLabel()}.</em>`\n",
     "        ? `${cfg.subtitle} <em>Comparison shown: difference = ${modelLabel()} &minus; ${labelOf(ok)}.</em>`\n"),
    ("      compareBtn.textContent = compare ? 'Hide comparison' : `Compare with ${otherShort()}`;\n",
     "      compareBtns.forEach(function(b) {\n"
     "        const on = b.dataset.key === compareWith;\n"
     "        b.hidden = b.dataset.key === mk;\n"
     "        b.textContent = on ? 'Hide comparison' : `Compare with ${shortOf(b.dataset.key)}`;\n"
     "        b.classList.toggle('active', on);\n"
     "      });\n"),
    ("    if (data) lines.push(`<div class=\"provenance-line\"><strong>Test set:</strong> ${data}</div>`);\n",
     "    if (data) lines.push(`<div class=\"provenance-line\"><strong>Test set:</strong> ${data}</div>`);\n"
     "    if (p.note) lines.push(`<div class=\"provenance-line\"><strong>Training data:</strong> ${p.note}</div>`);\n"),
    ("(run <code>${c.run_id}</code>)", "(run <code>${runId(c)}</code>)"),
]

SL = COMMON + [
    ('    <a href="comparison_table_v5_sl.html" aria-current="page">SL</a>', '    <a href="comparison_table_v6_sl.html" aria-current="page">SL</a>'),
    ('    <a href="comparison_table_v5.html" hreflang="en">EN</a>', '    <a href="comparison_table_v6.html" hreflang="en">EN</a>'),
    ('<header class="page-head">\n',
     '<div class="draft-note"><strong>Osnutek</strong> (2. 11. 2026): kot tretje orodje je dodana Stanza 1.14. Še ni objavljeno; '
     'objavljena različica je na <a href="https://orodja.cjvt.si/oznacevalnik/eval/">orodja.cjvt.si/oznacevalnik/eval</a>.</div>\n'
     '<header class="page-head">\n'),
    ("        ? `${cfg.subtitle} <em>Prikazana primerjava: razlika = ${modelLabel()} &minus; ${otherLabel()}.</em>`\n",
     "        ? `${cfg.subtitle} <em>Prikazana primerjava: razlika = ${modelLabel()} &minus; ${labelOf(ok)}.</em>`\n"),
    ("      compareBtn.textContent = compare ? 'Skrij primerjavo' : `Primerjaj s ${otherShort()}`;\n",
     "      compareBtns.forEach(function(b) {\n"
     "        const on = b.dataset.key === compareWith;\n"
     "        b.hidden = b.dataset.key === mk;\n"
     "        b.textContent = on ? 'Skrij primerjavo' : `Primerjaj s ${shortOf(b.dataset.key)}`;\n"
     "        b.classList.toggle('active', on);\n"
     "      });\n"),
    ("  const DOMAIN_SL = { ssj: 'pisni', sst: 'govorjeni · standardizirani', pog: 'govorjeni · pogovorni' };\n",
     "  const DOMAIN_SL = { ssj: 'pisni', sst: 'govorjeni · standardizirani', pog: 'govorjeni · pogovorni' };\n"
     f"  const STANZA_PROV_SL = `{STANZA_PROV_SL}`;\n"
     "  for (const k of ['ssj', 'sst', 'pog']) PROV_SL[k].stanza = STANZA_PROV_SL;\n"
     f"  PROV_SL.pog.note = `{POG_NOTE_SL}`;\n"),
    ("    if (data) lines.push(`<div class=\"provenance-line\"><strong>Testna množica:</strong> ${data}</div>`);\n",
     "    if (data) lines.push(`<div class=\"provenance-line\"><strong>Testna množica:</strong> ${data}</div>`);\n"
     "    if (p.note) lines.push(`<div class=\"provenance-line\"><strong>Učni podatki:</strong> ${p.note}</div>`);\n"),
    ("(zagon <code>${c.run_id}</code>)", "(zagon <code>${runId(c)}</code>)"),
]

# Accuracy tables: each "compare with" button is an on/off switch, so the selected
# tool can be compared with one other tool or with both. This replaces the
# single-comparison block produced by the edits above.
MULTI_COMPARE = r"""    // One "compare with" switch per tool (the static button is the template);
    // any number can be on, and the selected tool's own switch is hidden.
    const compareTemplate = document.getElementById(cfg.compareBtnId);
    const compareWith = new Set();
    const compareBtns = DATA.model_order.map(function(k) {
      const b = compareTemplate.cloneNode(false);
      b.removeAttribute('id');
      b.dataset.key = k;
      b.addEventListener('click', () => {
        if (compareWith.has(k)) compareWith.delete(k); else compareWith.add(k);
        expanded = false;
        render();
      });
      compareTemplate.before(b);
      return b;
    });
    compareTemplate.remove();
    const tableWrap = tbody.closest('.table-wrap');
    const tableEl = tbody.closest('table');
    const theadRow = tableEl.querySelector('thead tr');
    let expanded = false;

    function render() {
      const mk = modelKey();
      compareWith.delete(mk);
      const others = DATA.model_order.filter(k => compareWith.has(k));
      const tie = others.concat(otherKeys().filter(k => !compareWith.has(k)));
      const rows = cfg.rows();
      const q = filterInput ? filterInput.value.trim().toLowerCase() : '';
      const filtered = q ? rows.filter(r => r.tag.toLowerCase().includes(q)) : rows;
      const sorted = filtered.slice().sort((a, b) =>
        (b[mk] - a[mk]) || tie.reduce((d, k) => d || (b[k] - a[k]), 0) || (b.count - a.count) || a.tag.localeCompare(b.tag));

      // Header row (rebuilt fresh, so sort listeners do not accumulate).
      if (others.length) {
        theadRow.innerHTML =
          `<th>${cfg.tagHeader}</th><th class="right">@COUNT@</th>` +
          `<th class="right">${modelShort()}${cfg.headerSuffix}</th>` +
          others.map(k => `<th class="right">${shortOf(k)}${cfg.headerSuffix}</th>`).join('') +
          others.map(k => `<th class="right">${others.length > 1 ? `@DIFF@ (${shortOf(k)})` : '@DIFF@'}</th>`).join('');
      } else {
        theadRow.innerHTML =
          `<th>${cfg.tagHeader}</th><th class="right">@COUNT@</th><th class="right">${cfg.shortMetric}</th>`;
      }
      tableEl.classList.toggle('compare-multi', others.length > 1);
      noteEl.innerHTML = others.length
        ? `${cfg.subtitle} <em>@SHOWN@ ${others.map(k => `${modelLabel()} &minus; ${labelOf(k)}`).join('; ')}.</em>`
        : cfg.subtitle;
      compareBtns.forEach(function(b) {
        const on = compareWith.has(b.dataset.key);
        b.hidden = b.dataset.key === mk;
        b.textContent = `@WITH@ ${shortOf(b.dataset.key)}`;
        b.classList.toggle('active', on);
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });

      tbody.innerHTML = '';
      const colspan = 3 + 2 * others.length;
      if (!sorted.length) {
        renderEmptyRow(tbody, colspan, '@EMPTY@');
      } else {
        for (const row of sorted) {
          const mv = row[mk];
          const tr = document.createElement('tr');
          if (others.length) {
            // Shade the row only when the selected tool is better (or worse) than every compared tool.
            const diffs = others.map(k => mv - row[k]);
            if (diffs.every(d => d > 0)) tr.classList.add('model-better');
            else if (diffs.every(d => d < 0)) tr.classList.add('other-better');
            tr.innerHTML =
              `<td class="label">${row.tag}</td>` +
              `<td class="right">${@INT@(row.count)}</td>` +
              `<td class="right">${@NUM@(mv)} ${bar('bar-model', mv)}</td>` +
              others.map(k => `<td class="right">${@NUM@(row[k])} ${bar('bar-other', row[k])}</td>`).join('') +
              diffs.map(d => `<td class="right ${deltaClass(d, true)}">${deltaText(d, 2)}</td>`).join('');
          } else {
            tr.innerHTML =
              `<td class="label">${row.tag}</td>` +
              `<td class="right">${@INT@(row.count)}</td>` +
              `<td class="right">${@NUM@(mv)} ${bar('bar-model', mv)}</td>`;
          }
          tbody.appendChild(tr);
        }
      }
"""
WORDS = {
    "en": {"@COUNT@": "Gold count", "@DIFF@": "Diff", "@SHOWN@": "Comparison shown: difference =",
           "@WITH@": "Compare with", "@EMPTY@": "No matching rows.", "@INT@": "String", "@NUM@": "(v => v.toFixed(2))"},
    "sl": {"@COUNT@": "Pojavitve", "@DIFF@": "Razlika", "@SHOWN@": "Prikazana primerjava: razlika =",
           "@WITH@": "Primerjaj s", "@EMPTY@": "Ni ustreznih vrstic.", "@INT@": "formatInt", "@NUM@": "formatDecimal"},
}


def multi_compare(s: str, lang: str) -> str:
    block = MULTI_COMPARE
    for k, v in WORDS[lang].items():
        block = block.replace(k, v)
    start = s.index('    // One "compare with" button per other tool (the static button is the template).\n')
    end = s.index("      makeSortable(tableEl, render);\n", start)
    s = s[:start] + block + s[end:]
    if s.count("        compareWith = null;\n") != 1:
        raise SystemExit("reset line not found")
    return s.replace("        compareWith = null;\n", "        compareWith.clear();\n")


for src, dst, edits, lang in (("comparison_table_v5.html", "comparison_table_v6.html", EN, "en"),
                              ("comparison_table_v5_sl.html", "comparison_table_v6_sl.html", SL, "sl")):
    s = (TABLES / src).read_text(encoding="utf-8")
    for old, new in edits:
        n = s.count(old)
        if n != 1:
            raise SystemExit(f"{src}: expected 1 match, found {n}: {old[:80]!r}")
        s = s.replace(old, new)
    s = multi_compare(s, lang)
    for leftover in ("otherKey()", "otherLabel()", "otherShort()", "compareBtn.", "TABLE_DATA_V5", "_v5"):
        if leftover in s:
            raise SystemExit(f"{dst}: leftover {leftover!r}")
    (TABLES / dst).write_text(s, encoding="utf-8")
    print(f"wrote {dst} ({len(edits)} edits)")
