(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.AMBenchmarkAnalysis = api;
})(typeof window !== "undefined" ? window : null, function () {
  "use strict";

  /* One run, read as a short scientific report. The interaction concepts come from
     tables/comparison_table_v5.html — the Show more toggle, the merge (A<->B)
     switch, the accuracy bar, the clickable error row and the examples side panel —
     but the layout is this interface's own: every table carries one toolbar (count
     left, filter and exports right) directly above it, and the tables are typeset
     with rules rather than boxed. What deliberately differs is listed in the
     interface README. */

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

  /* Whether a run has sentence examples is a licensing fact about its corpus, and
     one the generator already decided: data/examples/index.json lists the runs it
     wrote a file for and the reason each withheld cohort has none. That manifest is
     asked rather than a second allowlist being kept here, so the two cannot drift.
     This sentence is only the fallback for a cohort the manifest does not explain. */
  const EXAMPLES_UNAVAILABLE_NOTE =
    "Sentence examples are not published for this test set, because public " +
    "redistribution rights for its underlying corpus are not established.";

  /* The same five headline metrics the overview leads with, described in the same
     words, so the two surfaces read as one document. */
  const SUMMARY_METRICS = [
    { name: "UPOS", description: "Universal part-of-speech" },
    { name: "XPOS", description: "Language-specific part-of-speech" },
    { name: "Lemmas", description: "Lemmatization" },
    { name: "UAS", description: "Unlabelled attachment score" },
    /* The dependency sections below elaborate this one number, so it is the only
       metric that carries the accent. */
    { name: "LAS", description: "Labelled attachment score", primary: true }
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
    "Error categories use the published comparison-table definitions. The error and " +
    "accuracy data holds counts and annotation labels only — no corpus sentence, " +
    "fragment, token or lemma.";

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

  /* What the examples manifest says about one run: the entry naming its file, if it
     has one, and the sentence to show where it has none. A manifest that is missing
     or unreadable means no examples, which is how a copy served without an
     examples directory behaves. */
  function exampleCatalogue(index, run, diagnostics) {
    const cohort = ((diagnostics && diagnostics.provenance) || {}).gold_cohort;
    const runs = index && Array.isArray(index.runs) ? index.runs : [];
    const entry = runs.filter(item => item.key === run.key)[0] || null;
    const withheld = index && index.withheld_cohorts && cohort &&
      Object.prototype.hasOwnProperty.call(index.withheld_cohorts, cohort)
      ? index.withheld_cohorts[cohort] : "";
    return { entry: entry, note: withheld || EXAMPLES_UNAVAILABLE_NOTE };
  }

  /* The run named the way a reader would name it: no manifest identifiers. */
  function contextDescription(run) {
    const parts = [label("language", run.language)];
    if (run.test_condition) parts.push(label("test_condition", run.test_condition) + " test data");
    return parts.join(" · ");
  }

  /* The run a link asked for, named the way the page names a run it can show. */
  function requestDescription(request) {
    return RUN_FIELDS.map(field => label(field, request[field])).filter(Boolean).join(" · ");
  }

  /* The complete evaluator output lives in the shared result bundle, the same one
     the overview reads, so the two surfaces can never disagree about a number. */
  function resultRow(browserWindow, run) {
    const bundle = browserWindow && browserWindow.AM_BENCHMARK_RESULTS;
    if (!bundle || !Array.isArray(bundle.rows)) return null;
    return bundle.rows.find(row => RUN_FIELDS.every(field => row[field] === run[field])) || null;
  }

  function systemDescription(run) {
    const training = label("training_condition", run.training_condition);
    return [label("model", run.model), training ? training + " training" : ""]
      .filter(Boolean).join(" · ");
  }

  function overviewUrl(run) {
    if (!run) return OVERVIEW_PAGE;
    const params = new URLSearchParams();
    for (const field of RUN_FIELDS) params.set(QUERY_NAMES[field], run[field]);
    return OVERVIEW_PAGE + "?" + params.toString();
  }

  function cell(doc, tag, text, className) {
    const node = doc.createElement(tag);
    if (text != null) node.textContent = text;
    if (className) node.className = className;
    return node;
  }

  /* "A. Wrong head and wrong relation" is two things: an index into the three
     categories, and the category's name. The letter is structure and takes the
     accent; the name is content and stays charcoal. Headings without a letter are
     returned unchanged, so this is safe for the tag layers too. */
  function sectionHeading(doc, tag, text, className) {
    const node = cell(doc, tag, null, className);
    const match = /^([A-Z]\.)\s+(\S[\s\S]*)$/.exec(String(text));
    if (!match) {
      node.textContent = text;
      return node;
    }
    node.append(cell(doc, "span", match[1], "section-marker"));
    node.append(doc.createTextNode(" " + match[2]));
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
  const EXAMPLE_PANELS = {
    rel: "accuracy",
    "upos-acc": "accuracy",
    dep: "dependency-errors",
    upos: "tagging-errors",
    xpos: "tagging-errors"
  };

  function examplePanel(selection) {
    return selection ? EXAMPLE_PANELS[selection.section] || "" : "";
  }

  /* --------------------------------------------------------------- view tabs
     The fragment is explicit reader state, not a scroll position. Panel ids are
     deliberately prefixed, so writing #accuracy cannot make the browser jump. */

  function createAnalysisTabs(doc, browserWindow) {
    const tablist = doc.getElementById("section-nav");
    const tabs = Array.from(tablist.querySelectorAll('[role="tab"][data-panel]'));
    const panels = new Map();
    const available = new Map();
    let selected = "";

    for (const tab of tabs) {
      const key = tab.dataset.panel;
      panels.set(key, doc.getElementById(tab.getAttribute("aria-controls")));
      available.set(key, true);
    }

    const availableTabs = () => tabs.filter(tab => available.get(tab.dataset.panel));
    const firstAvailable = () => {
      const first = availableTabs()[0];
      return first ? first.dataset.panel : "";
    };
    const hashKey = () => String(browserWindow.location.hash || "").replace(/^#/, "");

    function writeHash(key, mode) {
      if (!key || hashKey() === key) return;
      const location = browserWindow.location;
      const url = location.pathname + location.search + "#" + key;
      try {
        browserWindow.history[mode + "State"](null, "", url);
      } catch (error) {
        /* A non-opaque HTTP page has History API support. This fallback keeps the
           tabs usable in a restricted preview; no element owns the fragment, so
           assigning it still cannot scroll to an old heading. */
        location.hash = key;
      }
    }

    function activate(requested, options) {
      const settings = options || {};
      const key = available.get(requested) ? requested : firstAvailable();
      if (!key) return "";
      selected = key;
      for (const tab of tabs) {
        const isAvailable = Boolean(available.get(tab.dataset.panel));
        const isSelected = isAvailable && tab.dataset.panel === key;
        tab.hidden = !isAvailable;
        tab.disabled = !isAvailable;
        tab.setAttribute("aria-selected", String(isSelected));
        tab.tabIndex = isSelected ? 0 : -1;
        const panel = panels.get(tab.dataset.panel);
        if (panel) panel.hidden = !isSelected;
      }
      const activeTab = tabs.find(tab => tab.dataset.panel === key);
      if (settings.focus && activeTab) activeTab.focus();
      if (settings.history === "push" || settings.history === "replace") {
        writeHash(key, settings.history);
      }
      return key;
    }

    function syncFromHistory() {
      const requested = hashKey();
      activate(requested || firstAvailable(), {
        history: requested && !available.get(requested) ? "replace" : "none"
      });
    }

    for (const tab of tabs) {
      tab.addEventListener("click", () => {
        if (available.get(tab.dataset.panel)) {
          activate(tab.dataset.panel, { history: "push" });
        }
      });
      tab.addEventListener("keydown", event => {
        const activeTabs = availableTabs();
        const position = activeTabs.indexOf(tab);
        if (position < 0) return;
        let target = -1;
        if (event.key === "ArrowLeft") target = (position - 1 + activeTabs.length) % activeTabs.length;
        if (event.key === "ArrowRight") target = (position + 1) % activeTabs.length;
        if (event.key === "Home") target = 0;
        if (event.key === "End") target = activeTabs.length - 1;
        if (target >= 0) {
          event.preventDefault();
          activate(activeTabs[target].dataset.panel, { focus: true, history: "push" });
        } else if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          activate(tab.dataset.panel, { history: "push" });
        }
      });
    }

    browserWindow.addEventListener("popstate", syncFromHistory);
    browserWindow.addEventListener("hashchange", syncFromHistory);

    return {
      activate,
      initialize(preferred) {
        if (preferred && available.get(preferred)) {
          return activate(preferred, { history: "replace" });
        }
        const requested = hashKey();
        return activate(requested || firstAvailable(), {
          history: requested && !available.get(requested) ? "replace" : "none"
        });
      },
      setAvailable(key, value) {
        if (!available.has(key)) return;
        const isAvailable = Boolean(value);
        available.set(key, isAvailable);
        const tab = tabs.find(item => item.dataset.panel === key);
        if (tab) {
          tab.hidden = !isAvailable;
          tab.disabled = !isAvailable;
          if (isAvailable) tab.removeAttribute("aria-disabled");
          else tab.setAttribute("aria-disabled", "true");
        }
        const panel = panels.get(key);
        if (!isAvailable && panel) panel.hidden = true;
        if (!isAvailable && selected === key) activate(firstAvailable(), { history: "replace" });
      }
    };
  }

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

    /* The same sorting model the overview uses, and the one the CJVT table
       established: a click on a new column sorts by it, a click on the column
       already sorted reverses it, and sorting is only turned off through the
       explicit ✕ on the active header, which restores the natural order. */
    function header(column, index) {
      const classes = ["sortable"];
      if (column.right) classes.unshift("right");
      const th = cell(doc, "th", null, classes.join(" "));
      th.scope = "col";
      th.tabIndex = 0;
      th.dataset.sortIndex = String(index);
      const active = sort && sort.index === index;
      th.setAttribute("aria-sort",
        active ? (sort.direction === "asc" ? "ascending" : "descending") : "none");
      th.setAttribute("aria-label", column.label + ". Activate to sort.");
      th.title = active ? "Click to reverse the sort" : "Click to sort by " + column.label;
      if (column.bar) th.classList.add("has-bar");

      const indicator = cell(doc, "span", null, "sort-ind");
      indicator.append(cell(doc, "span",
        active ? (sort.direction === "asc" ? "↑" : "↓") : "", "sort-arrow"));
      const label = cell(doc, "span", column.label, "col-label");
      if (column.right) th.append(indicator, label);
      else th.append(label, indicator);

      const activate = () => {
        const first = column.right ? "desc" : "asc";
        if (!sort || sort.index !== index) sort = { index: index, direction: first };
        else sort = { index: index, direction: sort.direction === "asc" ? "desc" : "asc" };
        render();
        focusHeader(index);
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

    /* Clearing a sort is explicit, as in the CJVT table, but the control sits beside
       the row count rather than inside a narrow header cell. */
    let sortStatus = null;
    let sortReset = null;
    function renderSortReset() {
      const meta = spec.count && spec.count.parentElement;
      if (!meta) return;
      if (!sortReset) {
        sortStatus = cell(doc, "span", "", "sort-status");
        sortReset = cell(doc, "button", "Clear sort", "inline-toggle");
        sortReset.type = "button";
        sortReset.addEventListener("click", () => {
          sort = null;
          render();
        });
        meta.appendChild(sortStatus);
        meta.appendChild(sortReset);
      }
      sortStatus.textContent = sort
        ? "Sorted by " + spec.columns[sort.index].label +
          (sort.direction === "asc" ? " ↑" : " ↓")
        : "";
      sortStatus.hidden = !sort;
      sortReset.hidden = !sort;
    }

    /* The header row is rebuilt on every render, so focus goes back to the column
       the reader just acted on. */
    function focusHeader(index) {
      const th = table.querySelector('thead th[data-sort-index="' + index + '"]');
      if (th && typeof th.focus === "function") th.focus();
    }

    /* A percentage beside a rule of its own length, as v5 draws it: one neutral
       ink, no scale, hidden from assistive technology because the number next to
       it carries the value. */
    function accuracyCell(column, row) {
      /* The cell shares the header's content box; the bar is positioned into the
         padding beside it, so the number and its column label always right-align
         on the same edge whatever the bar's width. */
      const td = cell(doc, "td", null, "right has-bar");
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
      renderSortReset();
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

  /* One cohort can come from more than one treebank — NL written is the LassySmall
     test split followed by the Alpino test split — so the attribution is read from
     source.parts, falling back to the flat fields a schema-1 file carries. */
  function sourceParts(file) {
    const source = (file && file.source) || {};
    return Array.isArray(source.parts) && source.parts.length ? source.parts : [source];
  }

  function joinNames(names) {
    if (names.length < 2) return names.join("");
    return names.slice(0, -1).join(", ") + " and " + names[names.length - 1];
  }

  function distinct(values) {
    const seen = [];
    for (const value of values) {
      if (value && seen.indexOf(value) === -1) seen.push(value);
    }
    return seen;
  }

  function sourceText(file) {
    const parts = sourceParts(file);
    /* Two treebanks of one cohort are normally taken from the same UD release, so
       it is stated once at the end rather than after each corpus. */
    const releases = distinct(parts.map(part => part.release));
    const shared = releases.length === 1 ? releases[0] : "";
    const names = parts.map(part => {
      const detail = [part.section, shared ? "" : part.release].filter(Boolean).join(", ");
      return part.corpus + (detail ? " (" + detail + ")" : "");
    });
    const tail = [shared].concat(distinct(parts.map(part => part.licence))).filter(Boolean);
    return "Examples from " + joinNames(names) +
      (tail.length ? ", " + tail.join(", ") : "") + ".";
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

  /* The panel heading is the error pattern itself. The page already says which
     run this is, so repeating the system name here only crowds the pattern out. */
  function examplePattern(selection) {
    const key = selection.keys[0];
    if (selection.section === "rel" || selection.section === "upos-acc") return key;
    if (selection.section === "dep") {
      return selection.category === "head_only" ? key : mergedLabel(selection.keys);
    }
    return mergedLabel(selection.keys);
  }

  /* Exports name the system, because a copied note leaves this page. */
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

  /* The panel states the population first and the sample second, so a reader
     never mistakes twenty-five stored sentences for the whole story. */
  function occurrenceText(selection, total) {
    const noun = exampleNoun(selection);
    return formatCount(total) + " " + (total === 1 ? noun.replace(/s$/, "") : noun);
  }

  function sampleText(shown, total) {
    if (shown >= total) return "Showing all " + formatCount(shown) +
      (shown === 1 ? " example" : " examples");
    return "Showing " + formatCount(shown) + " examples";
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
    lines.push(sourceText(file));
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

  function createExamples(doc, browserWindow, run, catalogue, clipboard, tabs) {
    const entry = catalogue.entry;
    const available = Boolean(entry);
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
        pending = loadJson(browserWindow, EXAMPLES_DIR + entry.file)
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
      return browserWindow.location.pathname + (query ? "?" + query : "") +
        (browserWindow.location.hash || "");
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
      node("examples-title").textContent = examplePattern(selection);
      node("examples-subtitle").textContent = exampleSubtitle(selection);
      const count = node("examples-count");
      body.replaceChildren();

      if (!collected || !collected.items.length) {
        count.textContent = "";
        body.appendChild(cell(doc, "p", "No examples are stored for this row.", "examples-empty"));
        setActions(false);
      } else {
        count.replaceChildren();
        count.append(cell(doc, "span", occurrenceText(selection, collected.total), "examples-total"));
        count.append(cell(doc, "span",
          sampleText(collected.items.length, collected.total), "examples-shown"));
        collected.items.forEach((item, position) => body.appendChild(renderExample(item, position)));
        setActions(true);
      }

      node("examples-source").textContent = sourceText(file);
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
      note: catalogue.note,
      register(id, controller) { tables[id] = controller; },
      open: open,
      close: close,
      restore(next) {
        if (!available || !next) return;
        const table = tables[tableIdFor(next)];
        if (!table) return;
        /* A requested row can live in a panel hidden by the initial fragment. Make
           its parent visible before reveal() and scrollIntoView(), and normalise a
           disagreeing fragment into the same shareable URL. */
        const parent = examplePanel(next);
        if (parent && tabs) tabs.activate(parent, { history: "replace" });
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

  function renderSummary(doc, data) {
    const summary = data.summary;
    const overviewNode = doc.getElementById("overview");
    overviewNode.replaceChildren();

    for (const metric of SUMMARY_METRICS) {
      const value = Object.prototype.hasOwnProperty.call(summary.f1, metric.name)
        ? summary.f1[metric.name] : null;
      const box = doc.createElement("div");
      box.className = "metric-box" + (metric.primary ? " primary" : "");
      box.append(cell(doc, "div", metric.name, "label"));
      box.append(cell(doc, "div", formatScore(value), "val"));
      box.append(cell(doc, "div", metric.description, "sub"));
      overviewNode.appendChild(box);
    }

    /* One quiet line of scale, in words. The cohort identifier, the file names and
       the checksums belong to the reproducibility section, not above the results. */
    doc.getElementById("run-meta").textContent = [
      formatCount(summary.gold_words) + " gold words",
      formatCount(summary.aligned_words) + " aligned",
      summary.relations_attested + " dependency relations",
      summary.tags_attested + " part-of-speech tags"
    ].join(" · ");
  }

  /* Everything a reader needs to reproduce or cite the run, kept behind one
     disclosure so a page of scientific results does not open with checksums. */
  function renderProvenance(doc, data, examples) {
    const provenance = data.provenance || {};
    const note = doc.getElementById("reproducibility-note");
    if (note) {
      note.textContent = "Scores were computed with the CoNLL 2018 evaluation script over the " +
        "gold and prediction files below, and repeat identically on a re-run.";
    }
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
      ["Diagnostic file", DIAGNOSTICS_DIR + (data.run && data.run.key ? data.run.key + ".json" : ""), true],
      ["Content policy", data.content_policy, false]
    ];
    for (const entry of entries) {
      if (!entry[1]) continue;
      list.append(cell(doc, "dt", entry[0]), cell(doc, "dd", entry[1], entry[2] ? "mono" : ""));
    }
    const policy = doc.getElementById("policy-note");
    policy.textContent = POLICY_NOTE;
    if (examples && examples.available) policy.append(doc.createTextNode(" " + EXAMPLE_POLICY_NOTE));
  }

  /* The full evaluator table, read from the shared result bundle rather than
     recomputed or duplicated into the diagnostic files. */
  function renderAllMetrics(doc, row, bundle) {
    const api = overview();
    if (!row || !bundle) return false;

    const present = new Set((bundle.metrics || []).flatMap(metric => metric.fields));
    const fields = api.SCORE_FIELDS.concat(api.COUNT_FIELDS).filter(field => present.has(field));

    const head = doc.getElementById("metrics-head");
    head.replaceChildren();
    const headRow = doc.createElement("tr");
    const first = cell(doc, "th", "Metric");
    first.scope = "col";
    headRow.appendChild(first);
    for (const field of fields) {
      const th = cell(doc, "th", api.label("metric_field", field), "num");
      th.scope = "col";
      headRow.appendChild(th);
    }
    head.appendChild(headRow);

    const body = doc.getElementById("metrics-body");
    body.replaceChildren();
    const layerOf = name => api.METRIC_LAYERS.findIndex(layer => layer.includes(name));
    let previousLayer = null;
    for (const definition of bundle.metrics) {
      const tr = doc.createElement("tr");
      const layer = layerOf(definition.name);
      if (previousLayer !== null && layer !== previousLayer) tr.className = "layer-start";
      previousLayer = layer;
      const name = cell(doc, "th", definition.name, "metric-name");
      name.scope = "row";
      tr.appendChild(name);
      for (const field of fields) {
        const value = api.metricValue(row, definition.name, field);
        const text = api.COUNT_FIELDS.includes(field)
          ? api.formatCount(value) : api.formatScore(value);
        tr.appendChild(cell(doc, "td", text, "num"));
      }
      body.appendChild(tr);
    }

    const hasCounts = api.COUNT_FIELDS.some(field => fields.includes(field));
    doc.getElementById("metrics-note").textContent = hasCounts
      ? "Score fields are percentage points; count fields are raw evaluator counts."
      : "All values are percentage points.";
    return true;
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
    header.appendChild(sectionHeading(doc, "h3", options.heading));
    /* The exports and the merge toggle act on this one table, so they sit in its
       toolbar rather than beside the heading two paragraphs above it. */
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
    block.appendChild(header);

    if (options.description) {
      block.appendChild(cell(doc, "p", options.description, "note section-note"));
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

    const main = doc.createElement("div");
    main.className = "control-main";
    let ownFilterInput = null;
    if (options.filterPlaceholder) {
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
    }
    main.appendChild(actions);
    toolbar.appendChild(main);
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
    setAvailabilityNote(doc, "dep-examples-note", examples);
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

    setAvailabilityNote(doc, "tag-examples-note", examples);
  }

  /* Stated once per error section: either how to open the evidence, or why there is
     none. The unavailable wording comes from the examples manifest, so the reason is
     the one the generator recorded — and the "click a row" instruction is never
     shown for a run whose rows do not respond to a click. */
  const EXAMPLES_HINT =
    "Select a row to see sentences for that error pattern; Enter or Space opens the " +
    "same view and Esc closes it.";

  function setAvailabilityNote(doc, id, examples) {
    const note = doc.getElementById(id);
    if (!note) return;
    const interactive = Boolean(examples && examples.available);
    note.textContent = interactive
      ? EXAMPLES_HINT
      : (examples && examples.note) || EXAMPLES_UNAVAILABLE_NOTE;
    note.hidden = false;
  }

  /* The one thing this page shows when it cannot show a run: a short statement and
     a single way back. It is deliberately not a run picker — choosing a run is the
     overview's job, and this page is subordinate to it. */
  function showEmptyState(doc, title, message) {
    doc.getElementById("empty-state-title").textContent = title;
    doc.getElementById("empty-state-message").textContent = message;
    doc.getElementById("empty-state").hidden = false;
    /* The empty state carries its own link back, so the breadcrumb above it would
       only repeat the same destination. */
    const crumb = doc.querySelector(".crumb");
    if (crumb) crumb.hidden = true;
  }

  /* A bare analysis.html names no run and therefore has nothing to analyse. It
     returns to the overview, replacing its own history entry so that Back goes to
     wherever the reader came from instead of bouncing off this page again. */
  function redirectToOverview(browserWindow) {
    const location = browserWindow.location;
    /* A partial query still names a context the overview understands, so it travels
       with the redirect rather than being discarded; the overview already falls back
       on any value it cannot honour. */
    const target = OVERVIEW_PAGE + ((location && location.search) || "");
    try {
      if (location && typeof location.replace === "function") {
        location.replace(target);
        return;
      }
    } catch (error) {
      /* fall through: an assignment is the only remaining way to leave */
    }
    if (location) location.href = target;
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

  /* The same contract check the overview makes, for the same reason: analysis.html
     and analysis.js are cached independently and must not be paired across
     versions. */
  const REQUIRED_ELEMENTS = [
    "back-link", "run-hero", "run-context", "run-subtitle", "run-meta",
    "empty-state", "empty-state-title", "empty-state-message",
    "analysis", "overview", "section-nav",
    "tab-accuracy", "tab-dependency-errors", "tab-tagging-errors",
    "tab-all-metrics", "tab-reproducibility",
    "panel-accuracy", "panel-dependency-errors", "panel-tagging-errors",
    "panel-all-metrics", "panel-reproducibility",
    "rel-table", "upos-acc-table", "dep-buckets", "tag-sections",
    "metrics-disclosure", "metrics-head", "metrics-body", "metrics-note",
    "all-metrics-note", "reproducibility-note",
    "provenance-list", "policy-note",
    "examples-panel", "examples-backdrop", "examples-body"
  ];

  async function start(doc, browserWindow) {
    const absent = overview().missingElements(doc, REQUIRED_ELEMENTS);
    if (absent.length) throw new Error(overview().mismatchMessage(absent));

    let request;
    try {
      request = overview().parseRequest(browserWindow.location.search);
    } catch (error) {
      request = { language: "", test_condition: "", model: "", training_condition: "" };
    }

    if (!requestIsComplete(request)) {
      redirectToOverview(browserWindow);
      doc.body.dataset.uiReady = "redirect";
      return null;
    }

    let index;
    try {
      index = await loadJson(browserWindow, DIAGNOSTICS_DIR + INDEX_FILE);
    } catch (error) {
      const isFile = String(browserWindow.location.protocol) === "file:";
      showEmptyState(doc, "Diagnostics unavailable", isFile
        ? "This page was opened from the file system, so the browser refused to load the " +
          "diagnostic set. Serve the directory over HTTP (python3 -m http.server) and reopen it."
        : "The diagnostic set could not be loaded (" + error.message + "). Regenerate it with " +
          "am_benchmark/scripts/build_diagnostics_data.py.");
      doc.body.dataset.uiReady = "error";
      return null;
    }

    const run = findRun(index, request);
    if (!run) {
      showEmptyState(doc, "Run not available",
        "The benchmark has no diagnostics for " + requestDescription(request) + ". " +
        "The link may be out of date, or that run may not be part of the evaluated subset.");
      doc.body.dataset.uiReady = "no-run";
      return null;
    }

    /* The examples manifest decides whether this run's rows are interactive, so it
       is needed before any table is built; it is optional, and fetched alongside the
       run's diagnostics rather than after them. */
    const manifest = loadJson(browserWindow, EXAMPLES_DIR + INDEX_FILE).catch(() => null);

    let data;
    try {
      data = await loadJson(browserWindow, DIAGNOSTICS_DIR + run.file);
    } catch (error) {
      showEmptyState(doc, "Diagnostics unavailable",
        "The diagnostics file for this run could not be loaded (" + error.message + ").");
      doc.body.dataset.uiReady = "error";
      return null;
    }
    const catalogue = exampleCatalogue(await manifest, run, data);

    doc.title = contextDescription(run) + " — " + systemDescription(run) +
      " — detailed analysis";
    doc.getElementById("run-context").textContent = contextDescription(run);
    doc.getElementById("run-subtitle").textContent = systemDescription(run);
    doc.getElementById("back-link").href = overviewUrl(run);
    doc.getElementById("run-hero").hidden = false;

    const tabs = createAnalysisTabs(doc, browserWindow);
    const clipboard = createClipboard(doc, browserWindow);
    const examples = createExamples(doc, browserWindow, run, catalogue, clipboard, tabs);

    renderSummary(doc, data);
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

    const hasAllMetrics = renderAllMetrics(
      doc, resultRow(browserWindow, run), browserWindow.AM_BENCHMARK_RESULTS);
    tabs.setAvailable("all-metrics", hasAllMetrics);
    renderProvenance(doc, data, examples);

    const requestedSelection = parseExampleSelection(requestedExample(browserWindow));
    tabs.initialize(examples.available ? examplePanel(requestedSelection) : "");
    doc.getElementById("analysis").hidden = false;
    doc.body.dataset.uiReady = "true";

    if (examples.available) examples.restore(requestedSelection);
    return { run: run, data: data, examples: examples };
  }

  return {
    RUN_FIELDS,
    QUERY_NAMES,
    ROW_LIMIT,
    REQUIRED_ELEMENTS,
    EXAMPLES_UNAVAILABLE_NOTE,
    DEPENDENCY_CATEGORIES,
    SUMMARY_METRICS,
    runKey,
    requestIsComplete,
    findRun,
    exampleCatalogue,
    percentage,
    formatCount,
    overviewUrl,
    sourceText,
    parseExampleSelection,
    formatExampleSelection,
    examplePanel,
    mergeRows,
    mergedLabel,
    collectExamples,
    examplePattern,
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
