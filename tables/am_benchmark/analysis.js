(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.AMBenchmarkAnalysis = api;
})(typeof window !== "undefined" ? window : null, function () {
  "use strict";

  /* This page is deliberately a sibling of tables/comparison_table_v5.html: the
     controls block, the count toolbar with its Show more toggle, the merge
     (A<->B) switch, the dark table chrome with a grey accuracy bar, the clickable
     row with its return-arrow marker, and the examples side panel are all that
     page's components, adapted to one selected multilingual run rather than to a
     tool/corpus switch. What deliberately differs is listed in the UI README. */

  const DIAGNOSTICS_DIR = "data/diagnostics/";
  const EXAMPLES_DIR = "data/examples/";
  const INDEX_FILE = "index.json";
  const OVERVIEW_PAGE = "index.html";

  const RUN_FIELDS = ["language", "test_condition", "model", "training_condition"];
  const QUERY_NAMES = {
    language: "lang",
    test_condition: "test",
    model: "model",
    training_condition: "training"
  };
  const EXAMPLE_PARAM = "ex";

  /* v5's own row limit, so a long table folds at the same length here. */
  const ROW_LIMIT = 20;
  const MERGED_PREFIX = "merged~";

  /* Which gold cohorts may have their sentences republished. A licensing fact
     about the corpora, not something the diagnostic data can state, so it is
     declared once: a run outside it makes no example request at all. */
  const EXAMPLE_COHORTS = ["SL:writtentest", "SL:spokentest"];
  const EXAMPLES_UNAVAILABLE_NOTE =
    "Sentence examples are currently available for Slovenian test sets.";

  const SUMMARY_METRICS = [
    { name: "UPOS", description: "Universal part-of-speech" },
    { name: "XPOS", description: "Language-specific part-of-speech" },
    { name: "Lemmas", description: "Lemmatization" },
    { name: "UAS", description: "Unlabelled Attachment Score" },
    /* The dependency sections below elaborate this one number, so it carries the
       accent border v5 gives its highlighted metric box. */
    { name: "LAS", description: "Labelled Attachment Score", primary: true }
  ];

  /* v5 letters its three buckets A/B/C; the wording is this benchmark's. */
  const DEPENDENCY_CATEGORIES = {
    both_wrong: {
      heading: "A. Wrong head and wrong relation",
      short: "wrong head + wrong relation",
      description:
        "The system selected both the wrong syntactic head and the wrong dependency relation.",
      tally: "both wrong"
    },
    rel_only: {
      heading: "B. Correct head, wrong relation",
      short: "correct head, wrong relation",
      description: "The syntactic head is correct, but the dependency relation is wrong.",
      tally: "relation only"
    },
    head_only: {
      heading: "C. Correct relation, wrong head",
      short: "correct relation, wrong head",
      description: "The relation label is correct, but the word is attached to the wrong head.",
      tally: "head only"
    }
  };
  const DEPENDENCY_ORDER = ["both_wrong", "rel_only", "head_only"];

  const TAG_LAYERS = [
    {
      key: "upos",
      heading: "Universal part-of-speech errors",
      description:
        "The most frequent UPOS tagging errors the system made against the manually " +
        "annotated test set.",
      placeholder: "e.g. NOUN"
    },
    {
      key: "xpos",
      heading: "Language-specific part-of-speech errors",
      description:
        "The most frequent language-specific tagging errors the system made. Tagsets " +
        "differ by language, so this table is long where the tagset is fine-grained.",
      placeholder: ""
    }
  ];

  const POLICY_NOTE =
    "Scores come from the same CoNLL 2018 evaluation script that produced the benchmark, " +
    "over the authoritative gold file and the canonical prediction named above; error " +
    "categories use the published comparison-table definitions. The diagnostic file holds " +
    "derived counts and annotation labels only — no corpus sentence, fragment, token or " +
    "lemma. This page reads that one precomputed file and does not parse CoNLL-U.";

  const EXAMPLE_POLICY_NOTE =
    "Sentence examples for this run are published separately, under the licence named in " +
    "the examples panel, and are loaded only when a row is opened.";

  function overview() {
    const api = typeof window !== "undefined" ? window.AMBenchmarkUI : null;
    if (!api) throw new Error("app.js must load before analysis.js.");
    return api;
  }

  function label(field, value) {
    return overview().label(field, value);
  }

  function own(table, key) {
    return overview().lookup(table, key);
  }

  function formatScore(value) {
    return overview().formatScore(value);
  }

  /* Grouped thousands, done here rather than with toLocaleString so the output
     does not depend on the reader's locale. */
  function formatCount(value) {
    if (value == null) return "—";
    return String(value).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  function percentage(correct, total) {
    return total ? (100 * correct) / total : null;
  }

  function runKey(run) {
    return RUN_FIELDS.map(field => run[field]).join("-");
  }

  function requestIsComplete(request) {
    return RUN_FIELDS.every(field => Boolean(request[field]));
  }

  function findRun(index, request) {
    if (!index || !Array.isArray(index.runs)) return null;
    if (!requestIsComplete(request)) return null;
    return index.runs.find(run => RUN_FIELDS.every(field => run[field] === request[field])) || null;
  }

  function contextDescription(run) {
    return [label("language", run.language), label("test_condition", run.test_condition)]
      .filter(Boolean).join(" · ");
  }

  function systemDescription(run) {
    return [label("model", run.model), label("training_condition", run.training_condition)]
      .filter(Boolean).join(" · ");
  }

  function overviewUrl(run) {
    if (!run) return OVERVIEW_PAGE;
    const params = new URLSearchParams();
    for (const field of RUN_FIELDS) params.set(QUERY_NAMES[field], run[field]);
    return OVERVIEW_PAGE + "?" + params.toString();
  }

  function analysisUrl(run) {
    const params = new URLSearchParams();
    for (const field of RUN_FIELDS) params.set(QUERY_NAMES[field], run[field]);
    return "analysis.html?" + params.toString();
  }

  function cell(doc, tag, text, className) {
    const node = doc.createElement(tag);
    if (text != null) node.textContent = text;
    if (className) node.className = className;
    return node;
  }

  function splitPattern(key) {
    const parts = String(key).split("__to__");
    return parts.length === 2
      ? { gold: parts[0], predicted: parts[1] }
      : { gold: key, predicted: key };
  }

  /* --------------------------------------------------------------- selections
     ?ex=dep.both_wrong.obl__to__nmod, ?ex=upos.NOUN__to__PROPN, ?ex=rel.obl,
     ?ex=upos-acc.NOUN, and a merged row as ?ex=upos.merged~A__to__B~B__to__A.
     The pattern is named, never a sentence. */

  const EXAMPLE_SECTIONS = ["dep", "upos", "xpos", "rel", "upos-acc"];

  function encodeKeys(keys) {
    return keys.length === 1
      ? encodeURIComponent(keys[0])
      : MERGED_PREFIX + keys.map(encodeURIComponent).join("~");
  }

  function decodeKeys(token) {
    if (token.indexOf(MERGED_PREFIX) === 0) {
      return token.slice(MERGED_PREFIX.length).split("~").map(decodeURIComponent).filter(Boolean);
    }
    const key = decodeURIComponent(token);
    return key ? [key] : [];
  }

  function formatExampleSelection(selection) {
    if (!selection || !selection.keys || !selection.keys.length) return "";
    const parts = [encodeURIComponent(selection.section)];
    if (selection.category) parts.push(encodeURIComponent(selection.category));
    parts.push(encodeKeys(selection.keys));
    return parts.join(".");
  }

  function parseExampleSelection(value) {
    if (!value) return null;
    const raw = String(value);
    const first = raw.indexOf(".");
    if (first < 0) return null;
    const section = decodeURIComponent(raw.slice(0, first));
    if (EXAMPLE_SECTIONS.indexOf(section) === -1) return null;
    const rest = raw.slice(first + 1);
    if (section !== "dep") {
      const keys = decodeKeys(rest);
      return keys.length ? { section: section, category: "", keys: keys } : null;
    }
    const second = rest.indexOf(".");
    if (second < 0) return null;
    const category = decodeURIComponent(rest.slice(0, second));
    if (DEPENDENCY_ORDER.indexOf(category) === -1) return null;
    const keys = decodeKeys(rest.slice(second + 1));
    return keys.length ? { section: section, category: category, keys: keys } : null;
  }

  function tableIdFor(selection) {
    return selection.section === "dep" ? "dep:" + selection.category : selection.section;
  }

  /* ------------------------------------------------------------------- tables
     One engine behind every aggregate table, following v5: rows are built and
     sorted in full, then trimmed to the row limit, so a column sort applies to
     the whole filtered set rather than to the visible page. */

  function createTable(doc, spec) {
    const table = spec.table;
    const head = table.querySelector("thead tr");
    const body = table.querySelector("tbody");
    const wrap = table.closest(".table-wrap");
    let expanded = false;
    let sort = null;
    let selectedKey = null;

    function compareRows(a, b) {
      const column = spec.columns[sort.index];
      const direction = sort.direction === "asc" ? 1 : -1;
      const left = column.sortValue ? column.sortValue(a.row) : column.text(a.row);
      const right = column.sortValue ? column.sortValue(b.row) : column.text(b.row);
      if (left == null && right == null) return a.index - b.index;
      if (left == null) return 1;
      if (right == null) return -1;
      const result = typeof left === "number" && typeof right === "number"
        ? left - right
        : String(left).localeCompare(String(right));
      return result * direction || a.index - b.index;
    }

    function header(column, index) {
      const classes = ["sortable"];
      if (column.right) classes.unshift("right");
      const th = cell(doc, "th", null, classes.join(" "));
      th.scope = "col";
      th.tabIndex = 0;
      th.setAttribute("role", "columnheader");
      const active = sort && sort.index === index;
      th.setAttribute("aria-sort",
        active ? (sort.direction === "asc" ? "ascending" : "descending") : "none");
      th.title = active
        ? "Click to reverse; click again to restore the default order"
        : "Click to sort";
      th.append(doc.createTextNode(column.label));
      if (active) {
        th.append(cell(doc, "span", sort.direction === "asc" ? "▲" : "▼", "sort-ind"));
      }
      const activate = () => {
        const first = column.right ? "desc" : "asc";
        if (!sort || sort.index !== index) sort = { index: index, direction: first };
        else if (sort.direction === first) {
          sort = { index: index, direction: first === "asc" ? "desc" : "asc" };
        } else sort = null;
        render();
      };
      th.addEventListener("click", activate);
      th.addEventListener("keydown", event => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          activate();
        }
      });
      return th;
    }

    /* A percentage beside a rule of its own length, as v5 draws it: one neutral
       ink, no scale, hidden from assistive technology because the number next to
       it carries the value. */
    function accuracyCell(column, row) {
      const td = cell(doc, "td", null, "right");
      td.append(doc.createTextNode(column.text(row)));
      const value = column.sortValue(row);
      const wrapper = doc.createElement("span");
      wrapper.className = "bar-wrap";
      wrapper.setAttribute("aria-hidden", "true");
      const fill = doc.createElement("span");
      fill.className = "bar";
      fill.style.width = (value == null ? 0 : Math.max(0, Math.min(100, value))) + "%";
      wrapper.appendChild(fill);
      td.appendChild(wrapper);
      return td;
    }

    function markSelected(key) {
      selectedKey = key;
      for (const row of body.querySelectorAll("tr[data-row-key]")) {
        row.classList.toggle("selected-row", key != null && row.dataset.rowKey === key);
      }
    }

    function rowKeys() {
      return Array.from(body.querySelectorAll("tr[data-row-key]")).map(row => row.dataset.rowKey);
    }

    function rowFor(key) {
      const rows = Array.from(body.querySelectorAll("tr[data-row-key]"));
      const direct = rows.find(row => row.dataset.rowKey === key);
      if (direct) return direct;
      /* A merged row's keys may be stored in either order, so fall back to
         comparing the sets rather than the joined string. */
      const wanted = key.split(" ").slice().sort().join(" ");
      return rows.find(row => row.dataset.rowKey.split(" ").slice().sort().join(" ") === wanted) || null;
    }

    function render() {
      const rows = spec.rows();
      const records = rows.map((row, index) => ({ row: row, index: index }));
      if (sort) records.sort(compareRows);

      /* The header row is rebuilt on every render so sort listeners cannot
         accumulate; that would drop keyboard focus mid-sort, so the focused
         column is restored onto its replacement. */
      const headers = Array.from(head.children);
      const focused = headers.indexOf(doc.activeElement);
      head.replaceChildren();
      spec.columns.forEach((column, index) => head.appendChild(header(column, index)));
      if (focused !== -1 && head.children[focused]) head.children[focused].focus();

      body.replaceChildren();
      if (!records.length) {
        const tr = doc.createElement("tr");
        tr.className = "no-data-row";
        const td = cell(doc, "td", "No matching rows.");
        td.colSpan = spec.columns.length;
        tr.appendChild(td);
        body.appendChild(tr);
      } else {
        const shown = expanded ? records : records.slice(0, ROW_LIMIT);
        for (const record of shown) {
          const tr = doc.createElement("tr");
          for (const column of spec.columns) {
            tr.appendChild(column.bar
              ? accuracyCell(column, record.row)
              : cell(doc, "td", column.text(record.row), column.right ? "right" : "label"));
          }
          const keys = spec.rowKeys(record.row);
          tr.dataset.rowKey = keys.join(" ");
          /* Interactive only where examples exist behind the row, so the marker
             never promises something the data layer cannot deliver. */
          if (spec.onActivate) {
            tr.classList.add("clickable-row");
            tr.tabIndex = 0;
            tr.setAttribute("aria-label", "Show examples for " + spec.rowLabel(record.row));
            const activate = () => spec.onActivate(keys, tr);
            tr.addEventListener("click", activate);
            tr.addEventListener("keydown", event => {
              if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                activate();
              }
            });
          }
          body.appendChild(tr);
        }
      }

      const total = records.length;
      const visible = Math.min(total, expanded ? total : ROW_LIMIT);
      spec.count.textContent = "Showing " + visible + " / " + total;
      if (total <= ROW_LIMIT) {
        spec.toggle.hidden = true;
      } else {
        spec.toggle.hidden = false;
        spec.toggle.textContent = expanded ? "Show less" : "Show more";
      }
      if (wrap) {
        wrap.classList.toggle("expanded-scroll", expanded && total > ROW_LIMIT);
        wrap.scrollTop = 0;
      }
      markSelected(selectedKey);
    }

    spec.toggle.addEventListener("click", () => {
      expanded = !expanded;
      render();
    });

    return {
      render: render,
      table: table,
      collapse() { expanded = false; },
      /* Filled in by a section that has a merge toggle, so a merged deep link can
         put the table into the state the link describes. */
      setMerged: null,
      rowKeys: rowKeys,
      rowFor: rowFor,
      select: markSelected,
      /* A deep link may name a row folded below the cut; expand once so the link
         lands on something the reader can see. */
      reveal(key) {
        if (!rowFor(key)) {
          expanded = true;
          render();
        }
        return rowFor(key);
      }
    };
  }

  /* v5 exports what is on screen, read back out of the rendered table, so a file
     always matches the filter, merge state, sort and visible rows. */
  function renderedHeaders(table) {
    return Array.from(table.querySelectorAll("thead th")).map(th => {
      const copy = th.cloneNode(true);
      for (const mark of copy.querySelectorAll(".sort-ind")) mark.remove();
      return copy.textContent.replace(/\s+/g, " ").trim();
    });
  }

  function renderedRows(table) {
    return Array.from(table.querySelectorAll("tbody tr"))
      .filter(row => !row.classList.contains("no-data-row"))
      .map(row => Array.from(row.cells).map(td => td.textContent.replace(/\s+/g, " ").trim()));
  }

  function csvText(columns, rows) {
    const quote = value => '"' + String(value == null ? "" : value).replace(/"/g, '""') + '"';
    return [columns.map(quote).join(",")]
      .concat(rows.map(row => row.map(quote).join(",")))
      .join("\n");
  }

  function markdownTable(columns, rows) {
    const clean = value =>
      String(value == null ? "" : value).replace(/\|/g, "\\|").replace(/\s+/g, " ").trim();
    return ["| " + columns.map(clean).join(" | ") + " |",
      "| " + columns.map(() => "---").join(" | ") + " |"]
      .concat(rows.map(row => "| " + row.map(clean).join(" | ") + " |"))
      .join("\n");
  }

  function slug(text) {
    return String(text || "table").toLowerCase()
      .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 80) || "table";
  }

  /* --------------------------------------------------------- example payloads */

  function exampleSentence(file, index) {
    const row = file.sentences.rows[index];
    return row ? { id: row[0], tokens: row[1] } : { id: "", tokens: [] };
  }

  function headForm(sentence, index) {
    if (index == null || index < 0) return "root";
    return sentence.tokens[index] == null ? "?" : sentence.tokens[index];
  }

  function mergedLabel(keys) {
    const first = splitPattern(keys[0]);
    if (keys.length === 1) return first.gold + " → " + first.predicted;
    const pair = [first.gold, first.predicted].sort();
    return pair[0] === pair[1] ? pair[0] : pair.join(" ↔ ");
  }

  /* Every section resolves to the same shape: a list of items plus an exact
     population total, so the panel and the exports never have to know which
     table opened them. */
  function collectExamples(file, selection) {
    if (!file) return null;
    const keys = selection.keys;
    const items = [];
    let total = 0;

    if (selection.section === "rel" || selection.section === "upos-acc") {
      const table = selection.section === "rel" ? file.relation_errors : file.upos_errors;
      const entry = table && own(table.patterns, keys[0]);
      if (!entry) return null;
      total = entry.total;
      for (const example of entry.examples) {
        const sentence = exampleSentence(file, example[0]);
        if (selection.section === "rel") {
          const category = table.categories[example[4]];
          const reading = DEPENDENCY_CATEGORIES[category];
          const goldHead = headForm(sentence, example[2]);
          const predictedHead = headForm(sentence, example[3]);
          const facts = [[["gold relation", keys[0]], ["predicted relation", example[5]]]];
          facts.push(category === "rel_only"
            ? [["head", goldHead]]
            : [["gold head", goldHead], ["predicted head", predictedHead]]);
          items.push({
            sentence: sentence,
            token: example[1],
            kind: reading ? reading.short : category,
            facts: facts,
            row: {
              gold: keys[0], predicted: example[5], category: category,
              goldHead: goldHead, predictedHead: predictedHead
            }
          });
        } else {
          items.push({
            sentence: sentence,
            token: example[1],
            kind: "",
            facts: [[["gold UPOS", keys[0]], ["predicted UPOS", example[2]]]],
            row: { gold: keys[0], predicted: example[2] }
          });
        }
      }
      return { items: items, total: total };
    }

    for (const key of keys) {
      const pattern = splitPattern(key);
      if (selection.section === "dep") {
        const table = own(file.dependency, selection.category);
        const entry = table && own(table.patterns, key);
        if (!entry) continue;
        total += entry.total;
        for (const example of entry.examples) {
          const sentence = exampleSentence(file, example[0]);
          const goldHead = headForm(sentence, example[2]);
          const predictedHead = headForm(sentence, example[3]);
          const goldRelation = selection.category === "head_only" ? key : pattern.gold;
          const predictedRelation = selection.category === "head_only" ? key : pattern.predicted;
          const facts = selection.category === "head_only"
            ? [[["relation", key]], [["gold head", goldHead], ["predicted head", predictedHead]]]
            : [[["gold relation", pattern.gold], ["predicted relation", pattern.predicted]],
              selection.category === "rel_only"
                ? [["head", goldHead]]
                : [["gold head", goldHead], ["predicted head", predictedHead]]];
          items.push({
            sentence: sentence,
            token: example[1],
            kind: "",
            facts: facts,
            row: {
              gold: goldRelation, predicted: predictedRelation,
              goldHead: goldHead, predictedHead: predictedHead
            }
          });
        }
      } else {
        const table = own(file.tags, selection.section);
        const entry = table && own(table.patterns, key);
        if (!entry) continue;
        total += entry.total;
        const layer = selection.section.toUpperCase();
        for (const example of entry.examples) {
          const sentence = exampleSentence(file, example[0]);
          items.push({
            sentence: sentence,
            token: example[1],
            kind: "",
            facts: [[["gold " + layer, pattern.gold], ["predicted " + layer, pattern.predicted]]],
            row: { gold: pattern.gold, predicted: pattern.predicted }
          });
        }
      }
    }
    return { items: items, total: total };
  }

  function exampleTitle(selection, model) {
    const system = label("model", model);
    const key = selection.keys[0];
    if (selection.section === "rel") return system + " · " + key + " · LAS errors";
    if (selection.section === "upos-acc") return system + " · " + key + " · UPOS errors";
    if (selection.section === "dep") {
      return selection.category === "head_only"
        ? system + " · " + key
        : system + " · " + mergedLabel(selection.keys);
    }
    return system + " · " + selection.section.toUpperCase() +
      " · " + mergedLabel(selection.keys);
  }

  function exampleSubtitle(selection) {
    if (selection.section === "rel") return "Labelled attachment errors on this gold relation";
    if (selection.section === "upos-acc") return "Tagging errors on this gold tag";
    const merged = selection.keys.length > 1 ? " · merged A↔B" : "";
    if (selection.section === "dep") {
      const reading = DEPENDENCY_CATEGORIES[selection.category];
      return (reading ? reading.heading : selection.category) + merged;
    }
    const layer = TAG_LAYERS.find(entry => entry.key === selection.section);
    return (layer ? layer.heading : selection.section.toUpperCase()) + merged;
  }

  function exampleNoun(selection) {
    if (selection.section === "rel") return "LAS errors";
    if (selection.section === "upos-acc") return "errors";
    return "examples";
  }

  function exampleCountText(selection, shown, total) {
    const noun = exampleNoun(selection);
    if (shown >= total) {
      return "Showing all " + formatCount(total) + " " +
        (total === 1 ? noun.replace(/s$/, "") : noun);
    }
    return "Showing " + formatCount(shown) + " of " + formatCount(total) + " " + noun;
  }

  function exportColumns(selection) {
    if (selection.section === "rel") {
      return ["sentence_id", "sentence", "token", "error_category", "gold_relation",
        "predicted_relation", "gold_head", "predicted_head"];
    }
    if (selection.section === "dep") {
      return ["sentence_id", "sentence", "token", "gold_relation", "predicted_relation",
        "gold_head", "predicted_head"];
    }
    return ["sentence_id", "sentence", "token", "gold_tag", "predicted_tag"];
  }

  function exportRows(selection, items) {
    return items.map(item => {
      const text = item.sentence.tokens.join(" ");
      const token = item.sentence.tokens[item.token];
      if (selection.section === "rel") {
        return [item.sentence.id, text, token, item.kind, item.row.gold, item.row.predicted,
          item.row.goldHead, item.row.predictedHead];
      }
      if (selection.section === "dep") {
        return [item.sentence.id, text, token, item.row.gold, item.row.predicted,
          item.row.goldHead, item.row.predictedHead];
      }
      return [item.sentence.id, text, token, item.row.gold, item.row.predicted];
    });
  }

  function markdownExamples(file, selection, collected, model) {
    const lines = [
      "**" + exampleTitle(selection, model) + "** — " + exampleSubtitle(selection),
      exampleCountText(selection, collected.items.length, collected.total) +
        (collected.items.length < collected.total
          ? " (stored sample, capped at " + file.max_examples_per_pattern + " per pattern)"
          : ""),
      ""
    ];
    collected.items.forEach((item, position) => {
      const marked = item.sentence.tokens
        .map((token, index) => (index === item.token ? "**" + token + "**" : token))
        .join(" ");
      lines.push((position + 1) + ". " + marked);
      if (item.kind) lines.push("   - " + item.kind);
      for (const group of item.facts) {
        for (const pair of group) lines.push("   - " + pair[0] + ": " + pair[1]);
      }
      lines.push("");
    });
    lines.push("Examples from " + file.source.corpus + " (" + file.source.release + "), " +
      file.source.licence + ".");
    return lines.join("\n");
  }

  /* ------------------------------------------------------------------ exports */

  function createClipboard(doc, browserWindow) {
    function flash(button, ok) {
      const original = button.textContent;
      button.textContent = ok ? "✓" : "!";
      browserWindow.setTimeout(() => { button.textContent = original; }, 1400);
    }
    return {
      download(text, filename, type) {
        const blob = new browserWindow.Blob(["﻿" + text], { type: type });
        const url = browserWindow.URL.createObjectURL(blob);
        const anchor = doc.createElement("a");
        anchor.href = url;
        anchor.download = filename;
        doc.body.appendChild(anchor);
        anchor.click();
        doc.body.removeChild(anchor);
        browserWindow.URL.revokeObjectURL(url);
      },
      copyText(text, button) {
        const api = browserWindow.navigator && browserWindow.navigator.clipboard;
        if (api && typeof api.writeText === "function") {
          api.writeText(text).then(() => flash(button, true), () => flash(button, false));
          return;
        }
        /* Older or restricted contexts: a hidden textarea is still the only
           fallback that works without a permission prompt. */
        const area = doc.createElement("textarea");
        area.value = text;
        area.setAttribute("readonly", "");
        area.style.position = "fixed";
        area.style.left = "-9999px";
        doc.body.appendChild(area);
        area.select();
        let copied = false;
        try {
          copied = doc.execCommand("copy");
        } catch (error) {
          copied = false;
        }
        doc.body.removeChild(area);
        flash(button, copied);
      }
    };
  }

  /* ---------------------------------------------------------- examples panel */

  function createExamples(doc, browserWindow, run, diagnostics, clipboard) {
    const provenance = diagnostics.provenance || {};
    const available = EXAMPLE_COHORTS.indexOf(provenance.gold_cohort) !== -1;
    const node = id => doc.getElementById(id);
    const panel = node("examples-panel");
    const backdrop = node("examples-backdrop");
    const body = node("examples-body");
    const buttons = {
      prev: node("examples-prev"), next: node("examples-next"), link: node("examples-link"),
      csv: node("examples-csv"), md: node("examples-md"), close: node("examples-close")
    };

    const tables = {};
    let file = null;
    let pending = null;
    let selection = null;
    let collected = null;
    let returnFocus = null;

    const isOpen = () => !panel.hidden;

    /* One request per run, on first use, kept for the rest of the visit. */
    function ensureFile() {
      if (file) return Promise.resolve(file);
      if (!pending) {
        pending = loadJson(browserWindow, EXAMPLES_DIR + run.key + ".json")
          .then(loaded => { file = loaded; pending = null; return loaded; })
          .catch(error => { pending = null; throw error; });
      }
      return pending;
    }

    function currentUrl() {
      const params = new URLSearchParams(browserWindow.location.search);
      const value = formatExampleSelection(selection);
      if (value) params.set(EXAMPLE_PARAM, value);
      else params.delete(EXAMPLE_PARAM);
      const query = params.toString();
      return browserWindow.location.pathname + (query ? "?" + query : "");
    }

    function writeUrl() {
      /* A convenience, as on the overview: a context that refuses History writes
         must cost the reader a shareable link, not the panel. */
      try {
        browserWindow.history.replaceState(null, "", currentUrl());
      } catch (error) {
        /* ignore */
      }
    }

    function currentRowKey() {
      return selection ? selection.keys.join(" ") : null;
    }

    function siblingKeys() {
      const table = selection ? tables[tableIdFor(selection)] : null;
      return table ? table.rowKeys() : [];
    }

    function setActions(enabled) {
      for (const name of ["link", "csv", "md"]) buttons[name].disabled = !enabled;
      const keys = selection ? siblingKeys() : [];
      const position = selection ? keys.indexOf(currentRowKey()) : -1;
      buttons.prev.disabled = position <= 0;
      buttons.next.disabled = position < 0 || position >= keys.length - 1;
    }

    function exportName(extension) {
      const parts = [run.key, selection.section];
      if (selection.category) parts.push(selection.category);
      parts.push(selection.keys.join("-and-"));
      return slug(parts.join("-")) + "_examples-" +
        collected.items.length + "-of-" + collected.total + "." + extension;
    }

    /* Corpus text reaches the DOM as text nodes only; nothing builds markup from
       a sentence. */
    function renderExample(item, position) {
      const wrapper = doc.createElement("div");
      wrapper.className = "example-item";

      const meta = doc.createElement("div");
      meta.className = "example-meta";
      meta.append(cell(doc, "span", "#" + (position + 1)));
      if (item.sentence.id) {
        meta.append(doc.createTextNode(" · "));
        meta.append(cell(doc, "span", item.sentence.id));
      }
      if (item.kind) {
        meta.append(doc.createTextNode(" · "));
        meta.append(cell(doc, "span", item.kind, "example-kind"));
      }
      wrapper.appendChild(meta);

      const line = doc.createElement("div");
      line.className = "example-sentence";
      item.sentence.tokens.forEach((token, index) => {
        if (index) line.appendChild(doc.createTextNode(" "));
        if (index === item.token) {
          const marked = doc.createElement("mark");
          marked.textContent = token;
          line.appendChild(marked);
        } else {
          line.appendChild(doc.createTextNode(token));
        }
      });
      wrapper.appendChild(line);

      for (const group of item.facts) {
        const facts = doc.createElement("div");
        facts.className = "example-facts";
        group.forEach((pair, index) => {
          if (index) facts.append(cell(doc, "span", " · ", "example-sep"));
          facts.append(cell(doc, "span", pair[0] + ": ", "example-name"));
          facts.append(cell(doc, "span", pair[1], "example-value"));
        });
        wrapper.appendChild(facts);
      }
      return wrapper;
    }

    function render() {
      node("examples-title").textContent = exampleTitle(selection, run.model);
      node("examples-subtitle").textContent = exampleSubtitle(selection);
      const count = node("examples-count");
      body.replaceChildren();

      if (!collected || !collected.items.length) {
        count.textContent = "";
        body.appendChild(cell(doc, "p", "No examples are stored for this row.", "examples-empty"));
        setActions(false);
      } else {
        count.replaceChildren();
        count.append(cell(doc, "span",
          exampleCountText(selection, collected.items.length, collected.total)));
        if (collected.items.length < collected.total) {
          count.append(cell(doc, "span",
            "Stored sample, capped at " + file.max_examples_per_pattern + " per pattern.",
            "examples-cap"));
        }
        collected.items.forEach((item, position) => body.appendChild(renderExample(item, position)));
        setActions(true);
      }

      node("examples-source").textContent = "Examples from " + file.source.corpus +
        " (" + file.source.release + "), " + file.source.licence + ".";
      body.scrollTop = 0;
    }

    function show() {
      const opening = !isOpen();
      if (opening) {
        returnFocus = doc.activeElement && doc.activeElement !== doc.body ? doc.activeElement : null;
      }
      backdrop.hidden = false;
      panel.hidden = false;
      doc.body.dataset.examples = "open";
      if (opening) panel.focus();
    }

    function close() {
      if (!isOpen()) return;
      const target = returnFocus;
      panel.hidden = true;
      backdrop.hidden = true;
      delete doc.body.dataset.examples;
      const table = selection ? tables[tableIdFor(selection)] : null;
      if (table) table.select(null);
      selection = null;
      collected = null;
      returnFocus = null;
      writeUrl();
      if (target && typeof target.focus === "function") target.focus();
    }

    function failed(message) {
      node("examples-title").textContent = "Examples";
      node("examples-subtitle").textContent = "";
      node("examples-count").textContent = "";
      node("examples-source").textContent = "";
      body.replaceChildren(cell(doc, "p", message, "examples-empty"));
      setActions(false);
      show();
    }

    function open(next, row) {
      if (!available) return Promise.resolve(null);
      const previous = selection ? tables[tableIdFor(selection)] : null;
      selection = next;
      const table = tables[tableIdFor(next)];
      if (previous && previous !== table) previous.select(null);
      if (table) table.select(currentRowKey());
      if (row && !isOpen()) returnFocus = row;
      return ensureFile().then(() => {
        collected = collectExamples(file, next);
        render();
        show();
        writeUrl();
        return collected;
      }).catch(error => {
        collected = null;
        failed("The examples for this run could not be loaded (" + error.message + ").");
        return null;
      });
    }

    function step(delta) {
      if (!selection) return;
      const table = tables[tableIdFor(selection)];
      if (!table) return;
      const keys = table.rowKeys();
      const position = keys.indexOf(currentRowKey());
      const target = position + delta;
      if (position < 0 || target < 0 || target >= keys.length) return;
      const rowKey = keys[target];
      const row = table.rowFor(rowKey);
      returnFocus = row || returnFocus;
      if (row && typeof row.scrollIntoView === "function") row.scrollIntoView({ block: "nearest" });
      open({ section: selection.section, category: selection.category, keys: rowKey.split(" ") });
    }

    buttons.close.addEventListener("click", close);
    backdrop.addEventListener("click", close);
    buttons.prev.addEventListener("click", () => step(-1));
    buttons.next.addEventListener("click", () => step(1));
    buttons.link.addEventListener("click", () => {
      writeUrl();
      clipboard.copyText(browserWindow.location.href, buttons.link);
    });
    buttons.csv.addEventListener("click", () => {
      if (!collected) return;
      clipboard.download(csvText(exportColumns(selection), exportRows(selection, collected.items)),
        exportName("csv"), "text/csv;charset=utf-8;");
    });
    buttons.md.addEventListener("click", () => {
      if (!collected) return;
      clipboard.copyText(markdownExamples(file, selection, collected, run.model), buttons.md);
    });

    doc.addEventListener("keydown", event => {
      if (event.key === "Escape" && isOpen()) {
        event.preventDefault();
        close();
      }
    });

    /* Tab must not walk out of an open dialog into the page behind it. */
    panel.addEventListener("keydown", event => {
      if (event.key !== "Tab") return;
      const focusable = Array.from(
        panel.querySelectorAll("button, [href], input, select, textarea, [tabindex]:not([tabindex='-1'])")
      ).filter(element => !element.disabled && element.offsetParent !== null);
      if (!focusable.length) {
        event.preventDefault();
        panel.focus();
        return;
      }
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && (doc.activeElement === first || doc.activeElement === panel)) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && doc.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });

    return {
      available: available,
      register(id, controller) { tables[id] = controller; },
      open: open,
      close: close,
      restore(next) {
        if (!available || !next) return;
        const table = tables[tableIdFor(next)];
        if (!table) return;
        /* A link to a merged row describes a merged view, so put the table in it
           before looking for the row. */
        if (next.keys.length > 1 && table.setMerged) table.setMerged(true);
        const row = table.reveal(next.keys.join(" "));
        if (row && typeof row.scrollIntoView === "function") row.scrollIntoView({ block: "center" });
        /* The panel's content comes from the selection, not the row, so a link
           still opens even when no row matches. */
        open(next, row);
      }
    };
  }

  /* ------------------------------------------------------------------ filters
     v5's filter field: a search input with a clear affordance that appears once
     there is something to clear, and that resets the expanded state. */
  function wireFilter(doc, input, onChange) {
    if (!input) return () => "";
    const field = input.closest(".filter-field");
    const clear = doc.createElement("button");
    clear.type = "button";
    clear.className = "filter-clear";
    clear.textContent = "×";
    clear.title = "Clear filter";
    clear.setAttribute("aria-label", "Clear filter");
    clear.hidden = true;
    if (field) field.appendChild(clear);
    const sync = () => { clear.hidden = input.value.trim() === ""; };
    input.addEventListener("input", () => { sync(); onChange(); });
    clear.addEventListener("click", () => {
      input.value = "";
      sync();
      onChange();
      input.focus();
    });
    sync();
    return () => input.value.trim().toLowerCase();
  }

  function matches(text, query) {
    return !query || String(text).toLowerCase().indexOf(query) !== -1;
  }

  /* Merge (A<->B): the two directions of one confusion pair become a single row
     with the summed count, exactly as v5 folds them. */
  function mergeRows(rows) {
    const groups = new Map();
    for (const row of rows) {
      const parts = row.key.split("__to__");
      const id = parts.length === 2 ? parts.slice().sort().join("__sym__") : row.key;
      const existing = groups.get(id);
      if (existing) {
        existing.count += row.count;
        existing.keys.push(row.key);
      } else {
        groups.set(id, { count: row.count, keys: [row.key] });
      }
    }
    const merged = Array.from(groups.values()).map(group => ({
      label: mergedLabel(group.keys),
      count: group.count,
      keys: group.keys
    }));
    merged.sort((a, b) => b.count - a.count || a.label.localeCompare(b.label));
    return merged;
  }

  /* --------------------------------------------------------------- rendering */

  function renderSummary(doc, data, examples) {
    const summary = data.summary;
    const overviewNode = doc.getElementById("overview");
    overviewNode.replaceChildren();

    for (const metric of SUMMARY_METRICS) {
      const value = Object.prototype.hasOwnProperty.call(summary.f1, metric.name)
        ? summary.f1[metric.name] : null;
      const box = doc.createElement("div");
      box.className = "metric-box" + (metric.primary ? " highlight" : "");
      box.append(cell(doc, "div", metric.name, "label"));
      box.append(cell(doc, "div", formatScore(value), "val"));
      box.append(cell(doc, "div", metric.description, "sub"));
      overviewNode.appendChild(box);
    }

    const provenance = data.provenance || {};
    doc.getElementById("run-meta").textContent = [
      provenance.gold_cohort,
      provenance.gold_status ? provenance.gold_status.toLowerCase() + " gold" : "",
      formatCount(summary.gold_words) + " gold words",
      formatCount(summary.aligned_words) + " aligned"
    ].filter(Boolean).join(" · ");

    const list = doc.getElementById("provenance-list");
    list.replaceChildren();
    const entries = [
      ["Gold cohort", provenance.gold_cohort, false],
      ["Gold status", provenance.gold_status, false],
      ["Gold file", provenance.gold_file, true],
      ["Gold SHA-256", provenance.gold_sha256, true],
      ["Prediction", provenance.prediction_file, true],
      ["Prediction SHA-256", provenance.prediction_sha256, true],
      ["Evaluator", provenance.evaluator_file, true],
      ["Evaluator SHA-256", provenance.evaluator_sha256, true],
      ["Diagnostic set", data.generator, true],
      ["Content policy", data.content_policy, false]
    ];
    for (const entry of entries) {
      if (!entry[1]) continue;
      list.append(cell(doc, "dt", entry[0]), cell(doc, "dd", entry[1], entry[2] ? "mono" : ""));
    }
    const note = doc.getElementById("policy-note");
    note.textContent = POLICY_NOTE;
    if (examples && examples.available) note.append(doc.createTextNode(" " + EXAMPLE_POLICY_NOTE));
  }

  function wireExports(controller, csvButton, mdButton, filename, clipboard) {
    csvButton.addEventListener("click", () => {
      const table = controller.table;
      clipboard.download(csvText(renderedHeaders(table), renderedRows(table)),
        filename() + ".csv", "text/csv;charset=utf-8;");
    });
    mdButton.addEventListener("click", () => {
      const table = controller.table;
      clipboard.copyText(markdownTable(renderedHeaders(table), renderedRows(table)), mdButton);
    });
  }

  function renderAccuracySections(doc, data, examples, clipboard) {
    const interactive = Boolean(examples && examples.available);
    const configs = [
      {
        section: "rel", source: "las_by_relation", table: "rel-table", filter: "rel-filter",
        count: "rel-count", toggle: "rel-toggle", csv: "rel-csv", md: "rel-md",
        head: "Relation", metric: "LAS", suffix: "las-by-relation"
      },
      {
        section: "upos-acc", source: "upos_accuracy", table: "upos-acc-table",
        filter: "upos-acc-filter", count: "upos-acc-count", toggle: "upos-acc-toggle",
        csv: "upos-acc-csv", md: "upos-acc-md",
        head: "UPOS", metric: "Accuracy", suffix: "upos-accuracy"
      }
    ];

    for (const config of configs) {
      let query = () => "";
      const controller = createTable(doc, {
        table: doc.getElementById(config.table),
        count: doc.getElementById(config.count),
        toggle: doc.getElementById(config.toggle),
        columns: [
          { label: config.head, text: row => row[0], sortValue: row => row[0] },
          {
            label: "Gold count", right: true,
            text: row => formatCount(row[1]), sortValue: row => row[1]
          },
          {
            label: config.metric, right: true, bar: true,
            text: row => formatScore(percentage(row[2], row[1])),
            sortValue: row => percentage(row[2], row[1])
          }
        ],
        rows: () => data.tables[config.source].rows.filter(row => matches(row[0], query())),
        rowKeys: row => [row[0]],
        rowLabel: row => row[0],
        onActivate: interactive
          ? keys => examples.open({ section: config.section, category: "", keys: keys })
          : null
      });
      query = wireFilter(doc, doc.getElementById(config.filter), () => {
        controller.collapse();
        controller.render();
      });
      wireExports(controller, doc.getElementById(config.csv), doc.getElementById(config.md),
        () => slug(data.run.key + "-" + config.suffix), clipboard);
      controller.render();
      if (interactive) examples.register(config.section, controller);
    }
  }

  /* A bucket or tag block: v5's heading row with its action buttons, the count
     toolbar, and the table directly beneath. */
  function buildErrorSection(doc, container, options, clipboard) {
    const block = doc.createElement("div");
    block.className = "error-section";

    const header = doc.createElement("div");
    header.className = "bucket-header";
    header.appendChild(cell(doc, "h3", options.heading));
    const actions = doc.createElement("div");
    actions.className = "action-btns";
    let mergeButton = null;
    if (options.mergeable) {
      mergeButton = cell(doc, "button", "Merge (A⇔B)", "toggle-btn");
      mergeButton.type = "button";
      mergeButton.title = "Fold each pair and its reverse into one row";
      actions.appendChild(mergeButton);
    }
    const csvButton = cell(doc, "button", "↓ CSV", "action-btn");
    csvButton.type = "button";
    csvButton.title = "Export visible rows as CSV";
    const mdButton = cell(doc, "button", "⎘ MD", "action-btn");
    mdButton.type = "button";
    mdButton.title = "Copy visible rows as Markdown";
    actions.appendChild(csvButton);
    actions.appendChild(mdButton);
    header.appendChild(actions);
    block.appendChild(header);

    if (options.description) {
      block.appendChild(cell(doc, "p", options.description, "note section-note"));
    }

    let ownFilterInput = null;
    if (options.filterPlaceholder) {
      const controls = doc.createElement("div");
      controls.className = "controls";
      const main = doc.createElement("div");
      main.className = "control-main";
      const field = doc.createElement("label");
      field.className = "filter-field";
      const icon = cell(doc, "span", "", "filter-icon");
      icon.setAttribute("aria-hidden", "true");
      field.appendChild(icon);
      field.appendChild(cell(doc, "span", "Filter rows", "sr-only"));
      ownFilterInput = doc.createElement("input");
      ownFilterInput.type = "search";
      ownFilterInput.placeholder = options.filterPlaceholder;
      field.appendChild(ownFilterInput);
      main.appendChild(field);
      controls.appendChild(main);
      block.appendChild(controls);
    }

    const toolbar = doc.createElement("div");
    toolbar.className = "toolbar";
    const meta = doc.createElement("div");
    meta.className = "count-meta";
    const count = cell(doc, "div", "", "note");
    const toggle = cell(doc, "button", "Show more", "inline-toggle");
    toggle.type = "button";
    toggle.hidden = true;
    meta.appendChild(count);
    meta.appendChild(toggle);
    toolbar.appendChild(meta);
    block.appendChild(toolbar);

    const wrap = doc.createElement("div");
    wrap.className = "table-wrap";
    const table = doc.createElement("table");
    const thead = doc.createElement("thead");
    thead.appendChild(doc.createElement("tr"));
    table.appendChild(thead);
    table.appendChild(doc.createElement("tbody"));
    wrap.appendChild(table);
    block.appendChild(wrap);
    container.appendChild(block);

    let merged = false;
    let query = options.query || (() => "");

    const controller = createTable(doc, {
      table: table,
      count: count,
      toggle: toggle,
      columns: [
        { label: "Error pair", text: row => row.label, sortValue: row => row.label },
        {
          label: "Error count", right: true,
          text: row => formatCount(row.count), sortValue: row => row.count
        }
      ],
      rows: () => {
        const base = options.rows().map(row => ({
          label: row.label, count: row.count, keys: [row.key]
        }));
        const rows = merged && options.mergeable
          ? mergeRows(base.map(row => ({ label: row.label, count: row.count, key: row.keys[0] })))
          : base;
        const value = query();
        return rows.filter(row => matches(row.label, value));
      },
      rowKeys: row => row.keys,
      rowLabel: row => row.label,
      onActivate: options.onActivate || null
    });

    if (ownFilterInput) {
      query = wireFilter(doc, ownFilterInput, () => {
        controller.collapse();
        controller.render();
      });
    }
    if (mergeButton) {
      const applyMerge = () => {
        mergeButton.classList.toggle("active", merged);
        mergeButton.textContent = merged ? "Show (A→B)" : "Merge (A⇔B)";
        controller.collapse();
        controller.render();
      };
      mergeButton.addEventListener("click", () => {
        merged = !merged;
        applyMerge();
      });
      controller.setMerged = on => {
        if (merged === on) return;
        merged = on;
        applyMerge();
      };
    }
    wireExports(controller, csvButton, mdButton, options.filename, clipboard);
    controller.render();
    return controller;
  }

  function renderDependencyErrors(doc, data, examples, clipboard, sharedQuery) {
    const categories = data.tables.dependency_errors.categories;
    const total = categories.reduce((sum, category) => sum + category.total, 0);

    const tally = doc.getElementById("dep-tally");
    tally.replaceChildren();
    tally.append(cell(doc, "strong", formatCount(total) + " LAS errors"));
    for (const category of categories) {
      const reading = DEPENDENCY_CATEGORIES[category.key];
      tally.append(cell(doc, "span",
        formatCount(category.total) + " " + (reading ? reading.tally : category.key), "tally-part"));
    }

    const container = doc.getElementById("dep-buckets");
    container.replaceChildren();
    const interactive = Boolean(examples && examples.available);
    const controllers = [];

    for (const category of categories) {
      const reading = DEPENDENCY_CATEGORIES[category.key];
      const paired = category.columns.length === 3;
      const controller = buildErrorSection(doc, container, {
        heading: reading ? reading.heading : category.label,
        description: (reading ? reading.description + " " : "") +
          formatCount(category.total) + " errors over " + formatCount(category.rows.length) +
          (paired ? " relation pairs." : " relations."),
        mergeable: paired,
        query: sharedQuery,
        rows: () => category.rows.map(row => paired
          ? {
            label: row[0] + " → " + row[1], count: row[2],
            key: row[0] + "__to__" + row[1]
          }
          : { label: row[0], count: row[1], key: row[0] }),
        filename: () => slug(data.run.key + "-deprel-errors-" + category.key),
        onActivate: interactive
          ? keys => examples.open({ section: "dep", category: category.key, keys: keys })
          : null
      }, clipboard);
      if (interactive) examples.register("dep:" + category.key, controller);
      controllers.push(controller);
    }
    setAvailabilityNote(doc, "dep-examples-note", interactive);
    return controllers;
  }

  /* The language-specific placeholder comes from the run's own most frequent gold
     tags, so it never suggests Slovenian tags on an English or Dutch page. */
  function tagPlaceholder(layer, rows) {
    if (layer.placeholder) return layer.placeholder;
    const tags = [];
    for (const row of rows) {
      if (tags.indexOf(row[0]) === -1) tags.push(row[0]);
      if (tags.length === 2) break;
    }
    if (tags.length === 2) return "e.g. " + tags[0] + " or " + tags[1];
    return tags.length === 1 ? "e.g. " + tags[0] : "Filter rows";
  }

  function renderTagErrors(doc, data, examples, clipboard) {
    const tags = data.tables.tag_errors;
    const container = doc.getElementById("tag-sections");
    container.replaceChildren();
    const interactive = Boolean(examples && examples.available);

    for (const layer of TAG_LAYERS) {
      const table = tags[layer.key];
      if (!table) continue;
      const controller = buildErrorSection(doc, container, {
        heading: layer.heading,
        description: layer.description + " " + formatCount(table.total) + " errors over " +
          formatCount(table.rows.length) + " pairs.",
        mergeable: true,
        filterPlaceholder: tagPlaceholder(layer, table.rows),
        rows: () => table.rows.map(row => ({
          label: row[0] + " → " + row[1], count: row[2], key: row[0] + "__to__" + row[1]
        })),
        filename: () => slug(data.run.key + "-" + layer.key + "-errors"),
        onActivate: interactive
          ? keys => examples.open({ section: layer.key, category: "", keys: keys })
          : null
      }, clipboard);
      if (interactive) examples.register(layer.key, controller);
    }

    /* The diagnostic set carries a lemma error count and nothing else, so the
       page shows a count and says why, rather than a table implying detail that
       was deliberately not published. */
    if (tags.lemma) {
      const block = doc.createElement("div");
      block.className = "error-section";
      const header = doc.createElement("div");
      header.className = "bucket-header";
      header.appendChild(cell(doc, "h3", "Lemmatization"));
      block.appendChild(header);
      const stat = doc.createElement("p");
      stat.className = "stat";
      stat.append(cell(doc, "span", formatCount(tags.lemma.total), "stat-value"));
      stat.append(cell(doc, "span", "lemma errors", "stat-unit"));
      block.appendChild(stat);
      block.appendChild(cell(doc, "p", tags.lemma.note, "note section-note"));
      container.appendChild(block);
    }

    setAvailabilityNote(doc, "tag-examples-note", interactive);
  }

  /* Stated once per error section, in the note voice, because it is a property
     of the corpus rather than a fault the reader should act on. */
  function setAvailabilityNote(doc, id, interactive) {
    const note = doc.getElementById(id);
    if (!note) return;
    note.textContent = interactive ? "" : EXAMPLES_UNAVAILABLE_NOTE;
    note.hidden = interactive;
  }

  function renderRunChoices(doc, index) {
    const container = doc.getElementById("run-choices");
    container.replaceChildren();
    if (!index || !Array.isArray(index.runs) || !index.runs.length) {
      container.hidden = true;
      return;
    }
    container.appendChild(cell(doc, "h2", "Runs with diagnostics"));
    const groups = new Map();
    for (const run of index.runs) {
      const key = run.language + "|" + run.test_condition;
      if (!groups.has(key)) groups.set(key, { run: run, items: [] });
      groups.get(key).items.push(run);
    }
    for (const group of groups.values()) {
      const block = doc.createElement("div");
      block.className = "choice-group";
      block.appendChild(cell(doc, "h3", contextDescription(group.run)));
      const list = doc.createElement("ul");
      for (const run of group.items) {
        const item = doc.createElement("li");
        const link = doc.createElement("a");
        link.href = analysisUrl(run);
        link.textContent = systemDescription(run);
        item.appendChild(link);
        list.appendChild(item);
      }
      block.appendChild(list);
      container.appendChild(block);
    }
    container.hidden = false;
  }

  function showNotice(doc, text) {
    const notice = doc.getElementById("notice");
    notice.textContent = text;
    notice.hidden = false;
  }

  function showNoRun(doc, index, message) {
    showNotice(doc, message);
    renderRunChoices(doc, index);
    doc.getElementById("back-link").href = OVERVIEW_PAGE;
    doc.getElementById("run-context").textContent = "No run selected";
    doc.getElementById("run-subtitle").hidden = true;
    doc.getElementById("run-meta").hidden = true;
    doc.getElementById("run-hero").hidden = false;
  }

  function requestedExample(browserWindow) {
    try {
      return new URLSearchParams(browserWindow.location.search).get(EXAMPLE_PARAM) || "";
    } catch (error) {
      return "";
    }
  }

  async function loadJson(browserWindow, url) {
    const response = await browserWindow.fetch(url, { cache: "no-cache" });
    if (!response.ok) throw new Error(url + " returned HTTP " + response.status);
    return response.json();
  }

  async function start(doc, browserWindow) {
    let request;
    try {
      request = overview().parseRequest(browserWindow.location.search);
    } catch (error) {
      request = { language: "", test_condition: "", model: "", training_condition: "" };
    }

    let index;
    try {
      index = await loadJson(browserWindow, DIAGNOSTICS_DIR + INDEX_FILE);
    } catch (error) {
      const isFile = String(browserWindow.location.protocol) === "file:";
      showNotice(doc, isFile
        ? "This page was opened from the file system, so the browser refused to load the " +
          "diagnostic set. Serve the directory over HTTP (python3 -m http.server) and reopen it."
        : "The diagnostic set could not be loaded (" + error.message + "). Regenerate it with " +
          "am_benchmark/scripts/build_diagnostics_data.py.");
      doc.body.dataset.uiReady = "error";
      return null;
    }

    const run = findRun(index, request);
    if (!run) {
      showNoRun(doc, index, requestIsComplete(request)
        ? "No diagnostics exist for that combination of language, test data, system and " +
          "training condition. The runs below are available."
        : "This page analyses one benchmark run, named by the link that opened it. " +
          "Choose one below.");
      doc.body.dataset.uiReady = "no-run";
      return null;
    }

    let data;
    try {
      data = await loadJson(browserWindow, DIAGNOSTICS_DIR + run.file);
    } catch (error) {
      showNotice(doc,
        "The diagnostics file for this run could not be loaded (" + error.message + ").");
      doc.body.dataset.uiReady = "error";
      return null;
    }

    doc.title = contextDescription(run) + " — " + systemDescription(run) +
      " — detailed analysis";
    doc.getElementById("run-context").textContent = contextDescription(run);
    doc.getElementById("run-subtitle").textContent =
      systemDescription(run) + " training. Accuracy and error breakdowns for this benchmark run.";
    doc.getElementById("back-link").href = overviewUrl(run);
    doc.getElementById("run-hero").hidden = false;

    const clipboard = createClipboard(doc, browserWindow);
    const examples = createExamples(doc, browserWindow, run, data, clipboard);

    renderSummary(doc, data, examples);
    renderAccuracySections(doc, data, examples, clipboard);

    /* One filter above the three dependency buckets, as v5 does. */
    let dependencyControllers = [];
    const dependencyQuery = wireFilter(doc, doc.getElementById("dep-filter"), () => {
      for (const controller of dependencyControllers) {
        controller.collapse();
        controller.render();
      }
    });
    dependencyControllers = renderDependencyErrors(
      doc, data, examples, clipboard, () => dependencyQuery());
    renderTagErrors(doc, data, examples, clipboard);

    doc.getElementById("source-meta").textContent =
      "Aggregate diagnostics: " + DIAGNOSTICS_DIR + run.file + ".";
    doc.getElementById("analysis").hidden = false;
    doc.body.dataset.uiReady = "true";

    if (examples.available) examples.restore(parseExampleSelection(requestedExample(browserWindow)));
    return { run: run, data: data, examples: examples };
  }

  return {
    RUN_FIELDS,
    QUERY_NAMES,
    ROW_LIMIT,
    EXAMPLE_COHORTS,
    DEPENDENCY_CATEGORIES,
    SUMMARY_METRICS,
    runKey,
    requestIsComplete,
    findRun,
    percentage,
    formatCount,
    overviewUrl,
    analysisUrl,
    parseExampleSelection,
    formatExampleSelection,
    mergeRows,
    mergedLabel,
    collectExamples,
    exampleTitle,
    exampleSubtitle,
    exampleCountText,
    exportColumns,
    exportRows,
    csvText,
    markdownTable,
    markdownExamples,
    createTable,
    start
  };
});

if (typeof window !== "undefined") {
  window.addEventListener("DOMContentLoaded", function () {
    if (document.body.dataset.ui !== "analysis") return;
    window.AMBenchmarkAnalysis.start(document, window).catch(function (error) {
      const target = document.getElementById("app-error");
      if (target) {
        target.hidden = false;
        target.textContent = "The analysis could not start: " + error.message;
      }
      document.body.dataset.uiReady = "error";
      console.error(error);
    });
  });
}
