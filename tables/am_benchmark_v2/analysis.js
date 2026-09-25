(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.AMBenchmarkAnalysis = api;
})(typeof window !== "undefined" ? window : null, function () {
  "use strict";

  /* One run, read as a short scientific report, opened below the overview table
     rather than on a page of its own. The interaction concepts come from
     tables/comparison_table_v5.html — the Show more toggle, the merge (A<->B)
     switch, the accuracy bar, the Compare toggle, the clickable error row and the
     examples side panel — but the layout is this interface's own: every table
     carries one toolbar (count left, filter and exports right) directly above it,
     and the tables are typeset with rules rather than boxed. */

  /* This prototype reads the current interface's published data rather than a
     copy of it. */
  const DATA_DIR = "../am_benchmark/data/";
  /* The same folder, named from the repository root for the provenance table. */
  const PUBLISHED_DATA_DIR = "tables/am_benchmark/data/";
  const DIAGNOSTICS_DIR = DATA_DIR + "diagnostics/";
  /* Feature and lemma error tables exist for this prototype only, in its own folder
     (am_benchmark/scripts/build_layer_errors_v2.py). */
  const LAYERS_DIR = "data/layers/";
  const EXAMPLES_DIR = DATA_DIR + "examples/";
  const INDEX_FILE = "index.json";

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

  /* The prototype's own examples folder holds the Dutch spoken runs, which the
     current interface's folder does not have (am_benchmark/scripts/
     build_examples_v2.py). The two manifests are read together. */
  const OWN_EXAMPLES_DIR = "data/examples/";

  /* Only shown if a run's example file is missing, e.g. when the data folders were
     not copied along with the page. */
  const EXAMPLES_UNAVAILABLE_NOTE = "Sentence examples are not available for this run.";

  /* The same headline metrics as the overview table's columns, described in the
     same words, so the two read as one document. */
  const SUMMARY_METRICS = [
    { name: "UPOS", description: "Universal part-of-speech tags" },
    { name: "XPOS", description: "Language-specific part-of-speech tags" },
    { name: "UFeats", description: "Universal morphological features" },
    { name: "Lemmas", description: "Lemmatisation" },
    { name: "UAS", description: "Unlabelled attachment score: correct head" },
    /* The dependency sections below elaborate this one number, so it is the only
       metric that carries the accent. */
    { name: "LAS", description: "Labelled attachment score: correct head and relation", primary: true }
  ];
  const SUMMARY_GROUPS = [
    { name: "Morphology", metrics: ["UPOS", "XPOS", "UFeats", "Lemmas"] },
    { name: "Syntax", metrics: ["UAS", "LAS"] }
  ];

  /* v5 letters its three buckets A/B/C; the wording is this benchmark's. */
  const DEPENDENCY_CATEGORIES = {
    both_wrong: {
      heading: "A. Wrong head and wrong relation",
      short: "head and relation wrong",
      description:
        "The system selected both the wrong syntactic head and the wrong dependency relation.",
      tally: "head and relation wrong"
    },
    rel_only: {
      heading: "B. Correct head, wrong relation",
      short: "only the relation wrong",
      description: "The syntactic head is correct, but the dependency relation is wrong.",
      tally: "only the relation wrong"
    },
    head_only: {
      heading: "C. Correct relation, wrong head",
      short: "only the head wrong",
      description: "The relation label is correct, but the word is attached to the wrong head.",
      tally: "only the head wrong"
    }
  };
  const DEPENDENCY_ORDER = ["both_wrong", "rel_only", "head_only"];

  /* Universal tags only: the language-specific (XPOS) error table is no longer part
     of the analysis (am_benchmark/notes/feedback/2026-09-25-kd-table-feedback.md). */
  const TAG_LAYERS = [
    {
      key: "upos",
      heading: "Part of speech",
      /* The examples panel stands alone, so it names the layer in full. */
      panelTitle: "Part-of-speech errors",
      tally: "part-of-speech errors",
      description:
        "The most frequent confusions between the correct and the predicted UPOS tag.",
      placeholder: "e.g. NOUN"
    }
  ];

  const POLICY_NOTE =
    "Dependency error types A, B and C use the same definitions as the CJVT comparison table.";

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
  function exampleCatalogue(index, run) {
    const runs = index && Array.isArray(index.runs) ? index.runs : [];
    const entry = runs.filter(item => item.key === run.key)[0] || null;
    return { entry: entry, note: EXAMPLES_UNAVAILABLE_NOTE };
  }

  /* The current interface's manifest and the prototype's own, as one: each run
     entry remembers which folder its file is in. */
  function mergeManifests(shared, own) {
    const runs = [];
    for (const [manifest, dir] of [[shared, EXAMPLES_DIR], [own, OWN_EXAMPLES_DIR]]) {
      for (const entry of (manifest && manifest.runs) || []) {
        runs.push(Object.assign({}, entry, { dir: dir }));
      }
    }
    return { runs: runs };
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

  const EXAMPLE_SECTIONS = ["dep", "upos", "rel", "upos-acc"];
  const EXAMPLE_PANELS = {
    rel: "syntax",
    "upos-acc": "morphology",
    dep: "syntax",
    upos: "morphology"
  };

  function examplePanel(selection) {
    return selection ? EXAMPLE_PANELS[selection.section] || "" : "";
  }

  /* --------------------------------------------------------------- view tabs
     The fragment is explicit reader state, not a scroll position. Panel ids are
     deliberately prefixed, so writing #syntax cannot make the browser jump. The
     fragment is replaced rather than pushed: the overview replaces its own URL
     state, and a Back button that stepped through tabs of a run no longer on
     screen would show one run under another run's address. */

  function createAnalysisTabs(doc, browserWindow, signal) {
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

    function writeHash(key) {
      if (!key || hashKey() === key) return;
      const location = browserWindow.location;
      const url = location.pathname + location.search + "#" + key;
      try {
        browserWindow.history.replaceState(null, "", url);
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
      if (settings.history === "replace") writeHash(key);
      return key;
    }

    function syncFromHistory() {
      const requested = hashKey();
      activate(requested || firstAvailable(), {
        history: requested && !available.get(requested) ? "replace" : "none"
      });
    }

    /* The tab row stays pinned while a long panel scrolls under it. A tab chosen
       from down there opens its panel at the top, just under the row, rather than
       wherever the previous panel's length left the page. */
    function keepPanelStart() {
      const bar = doc.getElementById("analysis-nav");
      const above = bar ? bar.previousElementSibling : null;
      if (!above || typeof browserWindow.scrollTo !== "function") return;
      /* The row's top margin and the summary's bottom margin collapse into one gap,
         the larger of the two. */
      const margin = Math.max(
        parseFloat(browserWindow.getComputedStyle(bar).marginTop) || 0,
        parseFloat(browserWindow.getComputedStyle(above).marginBottom) || 0);
      const start = above.getBoundingClientRect().bottom + browserWindow.scrollY + margin;
      if (browserWindow.scrollY > start) browserWindow.scrollTo({ top: start });
    }

    for (const tab of tabs) {
      tab.addEventListener("click", () => {
        if (available.get(tab.dataset.panel)) {
          activate(tab.dataset.panel, { history: "replace" });
          keepPanelStart();
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
          activate(activeTabs[target].dataset.panel, { focus: true, history: "replace" });
          keepPanelStart();
        } else if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          activate(tab.dataset.panel, { history: "replace" });
          keepPanelStart();
        }
      });
    }

    /* A hand-edited fragment still selects its tab. The listener belongs to this
       run and is removed with it. */
    browserWindow.addEventListener("hashchange", syncFromHistory, { signal: signal });

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
     the whole filtered set rather than to the visible page. The columns may be a
     function, for a table whose Compare toggle changes them. */

  function createTable(doc, spec) {
    const table = spec.table;
    const head = table.querySelector("thead tr");
    const body = table.querySelector("tbody");
    const wrap = table.closest(".table-wrap");
    let expanded = false;
    let sort = null;
    let selectedKey = null;

    const columns = () => (typeof spec.columns === "function" ? spec.columns() : spec.columns);

    function compareRows(a, b) {
      const column = columns()[sort.index];
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
        ? "Sorted by " + columns()[sort.index].label +
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
      fill.className = "bar" + (column.barClass ? " " + column.barClass : "");
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

    /* The rows the examples panel can step through: only those that open evidence,
       so Previous and Next never land on a row compared in from the other run. */
    function rowKeys() {
      return Array.from(body.querySelectorAll("tr.clickable-row[data-row-key]"))
        .map(row => row.dataset.rowKey);
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
      const current = columns();
      const headers = Array.from(head.children);
      const focused = headers.indexOf(doc.activeElement);
      head.replaceChildren();
      current.forEach((column, index) => head.appendChild(header(column, index)));
      if (focused !== -1 && head.children[focused]) head.children[focused].focus();

      body.replaceChildren();
      if (!records.length) {
        const tr = doc.createElement("tr");
        tr.className = "no-data-row";
        const td = cell(doc, "td", "No matching rows.");
        td.colSpan = current.length;
        tr.appendChild(td);
        body.appendChild(tr);
      } else {
        const shown = expanded ? records : records.slice(0, ROW_LIMIT);
        for (const record of shown) {
          const tr = doc.createElement("tr");
          for (const column of current) {
            const className = (column.right ? "right" : "label") +
              (column.cellClass ? " " + column.cellClass(record.row) : "");
            tr.appendChild(column.bar
              ? accuracyCell(column, record.row)
              : cell(doc, "td", column.text(record.row), className));
          }
          const keys = spec.rowKeys(record.row);
          tr.dataset.rowKey = keys.join(" ");
          /* Interactive only where examples exist behind the row, so the marker
             never promises something the data layer cannot deliver. */
          if (spec.onActivate && (!spec.isActivatable || spec.isActivatable(record.row))) {
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
      /* "Showing 16 / 16" states one number twice; a table shown in full says so. */
      spec.count.textContent = visible < total
        ? "Showing " + visible + " / " + total
        : total === 1 ? "Showing 1 row" : "Showing all " + total;
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
      /* A column index means nothing once the columns change. */
      resetSort() { sort = null; },
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
    /* Named as the test set, not as "examples from": every system is scored on these
       same sentences, which is why this line reads the same for every run. */
    return "Test set: " + joinNames(names) +
      (tail.length ? ", " + tail.join(", ") : "") +
      ". Every system is tested on these same sentences.";
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
          const facts = [[["correct relation", keys[0]], ["predicted relation", example[5]]]];
          facts.push(category === "rel_only"
            ? [["head (correct)", goldHead]]
            : [["correct head", goldHead], ["predicted head", predictedHead]]);
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
            facts: [[["correct UPOS", keys[0]], ["predicted UPOS", example[2]]]],
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
            ? [[["relation (correct)", key]], [["correct head", goldHead], ["predicted head", predictedHead]]]
            : [[["correct relation", pattern.gold], ["predicted relation", pattern.predicted]],
              selection.category === "rel_only"
                ? [["head (correct)", goldHead]]
                : [["correct head", goldHead], ["predicted head", predictedHead]]];
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
            facts: [[["correct " + layer, pattern.gold], ["predicted " + layer, pattern.predicted]]],
            row: { gold: pattern.gold, predicted: pattern.predicted }
          });
        }
      }
    }
    return { items: items, total: total };
  }

  /* The panel heading is the error pattern itself; the subtitle names the run,
     because the panel covers the page that says which run this is. */
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
    if (selection.section === "rel") return "Words with this relation whose head or relation the system got wrong";
    if (selection.section === "upos-acc") return "Words with this UPOS tag that the system tagged differently";
    const merged = selection.keys.length > 1 ? " · both directions" : "";
    if (selection.section === "dep") {
      const reading = DEPENDENCY_CATEGORIES[selection.category];
      return (reading ? reading.heading : selection.category) + merged;
    }
    const layer = TAG_LAYERS.find(entry => entry.key === selection.section);
    return (layer ? layer.panelTitle : selection.section.toUpperCase()) + merged;
  }

  function exampleNoun(selection) {
    return "errors";
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
    return formatCount(total) + (total === 1 ? " error" : " errors") + " in total";
  }

  /* Examples keep the test set's own order, so the first few are often the same
     sentences for every system; saying so stops that reading as a fault. */
  function sampleText(shown, total) {
    if (shown >= total) return "all shown, in test-set order";
    return "the first " + formatCount(shown) + " shown, in test-set order";
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

  /* The panel is part of the page, not of the run, so every listener attached to it
     here is bound to the run's signal and removed when another run opens. */
  function createExamples(doc, browserWindow, run, catalogue, clipboard, tabs, signal) {
    const bound = { signal: signal };
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
        pending = loadJson(browserWindow, (entry.dir || EXAMPLES_DIR) + entry.file)
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
      node("examples-subtitle").textContent = systemDescription(run) + " · " + exampleSubtitle(selection);
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

    buttons.close.addEventListener("click", close, bound);
    backdrop.addEventListener("click", close, bound);
    buttons.prev.addEventListener("click", () => step(-1), bound);
    buttons.next.addEventListener("click", () => step(1), bound);
    buttons.link.addEventListener("click", () => {
      writeUrl();
      clipboard.copyText(browserWindow.location.href, buttons.link);
    }, bound);
    buttons.csv.addEventListener("click", () => {
      if (!collected) return;
      clipboard.download(csvText(exportColumns(selection), exportRows(selection, collected.items)),
        exportName("csv"), "text/csv;charset=utf-8;");
    }, bound);
    buttons.md.addEventListener("click", () => {
      if (!collected) return;
      clipboard.copyText(markdownExamples(file, selection, collected, run.model), buttons.md);
    }, bound);

    doc.addEventListener("keydown", event => {
      if (event.key === "Escape" && isOpen()) {
        event.preventDefault();
        close();
      }
    }, bound);

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
    }, bound);

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

  /* The headline values come from the shared result bundle, the row the table above
     shows, so the two cannot disagree; the diagnostic set's own summary does not
     carry UFeats. */
  function renderSummary(doc, data, row) {
    const summary = data.summary;
    const overviewNode = doc.getElementById("run-summary");
    overviewNode.replaceChildren();

    /* The tiles fall into the overview table's two groups, under the same labels,
       so the split into morphology and syntax reads the same in both places. */
    for (const group of SUMMARY_GROUPS) {
      const groupNode = cell(doc, "div", null, "metric-group");
      groupNode.style.setProperty("--tiles", String(group.metrics.length));
      groupNode.append(cell(doc, "p", group.name, "metric-group-label"));
      const tiles = cell(doc, "div", null, "metric-tiles");
      for (const name of group.metrics) {
        const metric = SUMMARY_METRICS.find(item => item.name === name);
        const value = row
          ? overview().metricValue(row, metric.name, "f1")
          : (Object.prototype.hasOwnProperty.call(summary.f1, metric.name) ? summary.f1[metric.name] : null);
        const box = doc.createElement("div");
        box.className = "metric-box" + (metric.primary ? " primary" : "");
        box.append(cell(doc, "div", metric.name, "label"));
        box.append(cell(doc, "div", formatScore(value), "val"));
        box.append(cell(doc, "div", metric.description, "sub"));
        tiles.appendChild(box);
      }
      groupNode.appendChild(tiles);
      overviewNode.appendChild(groupNode);
    }

    /* One quiet line of scale, in words. Relation and tag counts are left to the
       tables, whose row counts already state them. The cohort identifier, the file
       names and the checksums belong to the reproducibility section. */
    doc.getElementById("analysis-meta").textContent =
      "Test set of " + formatCount(summary.gold_words) + " words" +
      (summary.aligned_words === summary.gold_words
        ? ""
        : ", of which " + formatCount(summary.aligned_words) + " could be matched to the system's output");
  }

  /* An item/value table, typeset like every other table in the analysis. Items
     without a value are left out rather than shown empty. */
  function fillKeyValues(doc, body, entries) {
    body.replaceChildren();
    for (const entry of entries) {
      if (!entry[1]) continue;
      const tr = doc.createElement("tr");
      const name = cell(doc, "th", entry[0], "kv-name");
      name.scope = "row";
      tr.append(name, cell(doc, "td", entry[1], "kv-value"));
      body.appendChild(tr);
    }
  }

  /* Everything a reader needs to reproduce or cite the run, and the result file
     the whole benchmark table is built from. */
  function renderProvenance(doc, data, examples, bundle) {
    const provenance = data.provenance || {};
    const note = doc.getElementById("reproducibility-note");
    if (note) {
      note.textContent = "Scores were computed with the CoNLL 2018 evaluation script over the " +
        "gold and prediction files below, and repeat identically on a re-run.";
    }
    fillKeyValues(doc, doc.getElementById("provenance-body"), [
      ["Gold cohort", provenance.gold_cohort],
      ["Gold status", provenance.gold_status],
      ["Gold file", provenance.gold_file],
      ["Gold SHA-256", provenance.gold_sha256],
      ["Prediction", provenance.prediction_file],
      ["Prediction SHA-256", provenance.prediction_sha256],
      ["Evaluator", provenance.evaluator_file],
      ["Evaluator SHA-256", provenance.evaluator_sha256],
      ["Diagnostic set", data.generator],
      ["Diagnostic file", data.run && data.run.key
        ? PUBLISHED_DATA_DIR + "diagnostics/" + data.run.key + ".json" : ""]
    ]);
    const source = (bundle && bundle.source) || {};
    fillKeyValues(doc, doc.getElementById("result-set-body"), [
      /* The bundle records its source relative to am_benchmark/; shown from the
         repository root like every other path here. */
      ["Result set", source.path && source.path.indexOf("am_benchmark/") !== 0
        ? "am_benchmark/" + source.path : source.path],
      ["Rows", source.row_count == null ? "" : String(source.row_count)],
      ["SHA-256", source.sha256]
    ]);
    const policy = doc.getElementById("policy-note");
    policy.textContent = POLICY_NOTE;
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

  /* ------------------------------------------------------------ compare with
     v5's Compare toggle, with one fixed counterpart: the same system and training
     setup on the other test modality. Rows from both runs are joined by label; a
     label attested in only one test set keeps its row, with a dash on the side
     that lacks it. */

  function diffClass(value) {
    if (value == null || Math.abs(value) < 0.005) return "diff-neut";
    return value > 0 ? "diff-pos" : "diff-neg";
  }

  function diffText(value) {
    if (value == null) return "—";
    if (Math.abs(value) < 0.005) return "0.00";
    return (value > 0 ? "+" : "") + value.toFixed(2);
  }

  /* Whether each accuracy table was last left in Compare mode, kept across runs for
     the rest of the visit. */
  const rememberedCompare = {};

  function pairedRows(own, other) {
    const theirs = new Map(other.map(row => [row[0], row]));
    const seen = new Set();
    const rows = own.map(row => {
      seen.add(row[0]);
      const match = theirs.get(row[0]);
      const score = percentage(row[2], row[1]);
      const otherScore = match ? percentage(match[2], match[1]) : null;
      return {
        key: row[0], gold: row[1], score: score, inThis: true,
        otherGold: match ? match[1] : null, otherScore: otherScore,
        diff: score != null && otherScore != null ? score - otherScore : null
      };
    });
    for (const row of other) {
      if (seen.has(row[0])) continue;
      rows.push({
        key: row[0], gold: null, score: null, inThis: false,
        otherGold: row[1], otherScore: percentage(row[2], row[1]), diff: null
      });
    }
    return rows;
  }

  function renderAccuracySections(doc, run, data, examples, clipboard, counterpart) {
    const interactive = Boolean(examples && examples.available);
    const thisName = label("test_condition", run.test_condition);
    const configs = [
      {
        section: "rel", source: "las_by_relation", table: "rel-table", filter: "rel-filter",
        count: "rel-count", toggle: "rel-toggle", csv: "rel-csv", md: "rel-md",
        compare: "rel-compare", note: "rel-note",
        head: "Relation", metric: "LAS", suffix: "las-by-relation"
      },
      {
        section: "upos-acc", source: "upos_accuracy", table: "upos-acc-table",
        filter: "upos-acc-filter", count: "upos-acc-count", toggle: "upos-acc-toggle",
        csv: "upos-acc-csv", md: "upos-acc-md", compare: "upos-acc-compare", note: "upos-acc-note",
        head: "Part of speech", metric: "Accuracy", suffix: "upos-accuracy"
      }
    ];

    for (const config of configs) {
      let query = () => "";
      let comparing = false;
      let other = null;
      const otherName = counterpart ? counterpart.name : "";

      const single = [
        { label: config.head, text: row => row.key, sortValue: row => row.key },
        {
          label: "Occurrences", right: true,
          text: row => formatCount(row.gold), sortValue: row => row.gold
        },
        {
          label: config.metric, right: true, bar: true,
          text: row => formatScore(row.score), sortValue: row => row.score
        }
      ];
      /* The two test sets are different corpora, so each side keeps its own gold
         count: a score on 3 tokens and one on 300 are not the same evidence. */
      const paired = [
        { label: config.head, text: row => row.key, sortValue: row => row.key },
        {
          label: "Occurrences (" + thisName.toLowerCase() + ")", right: true,
          text: row => formatCount(row.gold), sortValue: row => row.gold
        },
        {
          label: config.metric + " (" + thisName.toLowerCase() + ")", right: true, bar: true, barClass: "bar-this",
          text: row => formatScore(row.score), sortValue: row => row.score
        },
        {
          label: "Occurrences (" + otherName.toLowerCase() + ")", right: true,
          text: row => formatCount(row.otherGold), sortValue: row => row.otherGold
        },
        {
          label: config.metric + " (" + otherName.toLowerCase() + ")", right: true, bar: true,
          text: row => formatScore(row.otherScore), sortValue: row => row.otherScore
        },
        {
          label: "Difference", right: true,
          text: row => diffText(row.diff), sortValue: row => row.diff,
          cellClass: row => diffClass(row.diff)
        }
      ];

      const ownRows = data.tables[config.source].rows;
      const controller = createTable(doc, {
        table: doc.getElementById(config.table),
        count: doc.getElementById(config.count),
        toggle: doc.getElementById(config.toggle),
        columns: () => (comparing && other ? paired : single),
        rows: () => {
          const rows = comparing && other
            ? pairedRows(ownRows, other.tables[config.source].rows)
            : ownRows.map(row => ({ key: row[0], gold: row[1], score: percentage(row[2], row[1]), inThis: true }));
          const value = query();
          return rows.filter(row => matches(row.key, value));
        },
        rowKeys: row => [row.key],
        rowLabel: row => row.key,
        isActivatable: row => row.inThis,
        onActivate: interactive
          ? keys => examples.open({ section: config.section, category: "", keys: keys })
          : null
      });
      query = wireFilter(doc, doc.getElementById(config.filter), () => {
        controller.collapse();
        controller.render();
      });
      wireExports(controller, doc.getElementById(config.csv), doc.getElementById(config.md),
        () => slug(data.run.key + "-" + config.suffix + (comparing ? "-vs-" + otherName : "")), clipboard);

      const button = doc.getElementById(config.compare);
      const note = doc.getElementById(config.note);
      const baseNote = note.textContent.replace(/\s+/g, " ").trim();
      const syncCompare = () => {
        button.textContent = comparing ? "Hide comparison" : "Compare with " + otherName.toLowerCase();
        button.classList.toggle("active", comparing);
        button.setAttribute("aria-pressed", String(comparing));
        note.textContent = baseNote;
        if (comparing) {
          note.append(" ");
          note.append(cell(doc, "em", "Compared with the same system and training on the " +
            otherName.toLowerCase() + " test data. Difference = " + thisName.toLowerCase() + " minus " +
            otherName.toLowerCase() + ", in percentage points: positive means better on " +
            thisName.toLowerCase() + ", red means worse. The two test sets are different texts, " +
            "so each has its own number of occurrences."));
        }
      };
      if (counterpart) {
        button.hidden = false;
        syncCompare();
        button.addEventListener("click", () => {
          const next = !comparing;
          const apply = () => {
            comparing = next;
            rememberedCompare[config.section] = next;
            controller.resetSort();
            controller.collapse();
            syncCompare();
            controller.render();
          };
          if (!next || other) {
            apply();
            return;
          }
          button.disabled = true;
          button.textContent = "Loading…";
          counterpart.load().then(loaded => {
            other = loaded;
            button.disabled = false;
            apply();
          }, error => {
            button.textContent = "Comparison unavailable";
            button.title = error.message;
          });
        });
      }
      controller.render();
      if (interactive) examples.register(config.section, controller);
      /* A reader comparing modalities while moving between runs keeps comparing. */
      if (counterpart && rememberedCompare[config.section]) button.click();
    }
  }

  /* A bucket or tag block: v5's heading row with its action buttons, the count
     toolbar, and the table directly beneath. */
  function buildErrorSection(doc, container, options, clipboard) {
    const block = doc.createElement("div");
    block.className = "error-section";

    const header = doc.createElement("div");
    header.className = "bucket-header";
    header.appendChild(sectionHeading(doc, options.headingTag || "h3", options.heading));
    /* The exports and the merge toggle act on this one table, so they sit in its
       toolbar rather than beside the heading two paragraphs above it. */
    const actions = doc.createElement("div");
    actions.className = "action-btns";
    let mergeButton = null;
    if (options.mergeable) {
      mergeButton = cell(doc, "button", "Combine both directions", "toggle-btn");
      mergeButton.type = "button";
      mergeButton.title = "Show A → B and B → A as one row, with their errors added up";
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
    if (options.notice) block.appendChild(options.notice);

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
        { label: options.pairHeader || "Correct → predicted", text: row => row.label, sortValue: row => row.label },
        {
          label: "Errors", right: true,
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
        mergeButton.textContent = merged ? "Separate directions" : "Combine both directions";
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
    tally.append(cell(doc, "strong", formatCount(total) + " words with a wrong head or relation:"));
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
        headingTag: "h4",
        /* Category C keeps the relation right, so its rows are single relations. */
        pairHeader: paired ? "" : "Relation",
        /* What the category means, and nothing counted: its total is on the tally
           line above and its number of rows on its own count line. */
        description: reading ? reading.description : "",
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
    setAvailabilityNote(doc, "syntax-examples-note", examples);
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

  /* A notice inside an error subsection: a bold lead, then the explanation. */
  function layerNotice(doc, lead, text, quiet) {
    const node = cell(doc, "p", null, "notice" + (quiet ? " quiet" : ""));
    node.append(cell(doc, "strong", lead), doc.createTextNode(" " + text));
    return node;
  }

  function pairRows(rows) {
    return rows.map(row => ({
      label: row[0] + " → " + row[1], count: row[2], key: row[0] + "__to__" + row[1]
    }));
  }

  /* Morphology's errors in the order KD named the layers — part of speech, lemmas,
     features — each with its total once on the tally line above. Part of speech
     comes from the published diagnostic set; lemmas and features from this
     prototype's own layer files, when present. */
  function renderTagErrors(doc, data, examples, clipboard, layers) {
    const tags = data.tables.tag_errors;
    const container = doc.getElementById("tag-sections");
    container.replaceChildren();
    const interactive = Boolean(examples && examples.available);
    const lemmas = layers && layers.lemmas;
    const features = layers && layers.features;

    /* Each layer's total, once, on one line — the counterpart of Syntax's tally.
       The layers overlap on words, so there is no grand total to lead with. */
    const tally = doc.getElementById("morph-tally");
    tally.replaceChildren();
    const layerTotals = TAG_LAYERS.filter(layer => tags[layer.key])
      .map(layer => [tags[layer.key].total, layer.tally]);
    if (lemmas || tags.lemma) layerTotals.push([(lemmas || tags.lemma).total, "lemma errors"]);
    if (features) layerTotals.push([features.total, "feature errors"]);
    for (const [total, noun] of layerTotals) {
      const part = cell(doc, "span", null, "tally-part");
      part.append(cell(doc, "strong", formatCount(total)), doc.createTextNode(" " + noun));
      tally.appendChild(part);
    }

    for (const layer of TAG_LAYERS) {
      const table = tags[layer.key];
      if (!table) continue;
      const controller = buildErrorSection(doc, container, {
        heading: layer.heading,
        headingTag: "h4",
        description: layer.description,
        mergeable: true,
        filterPlaceholder: tagPlaceholder(layer, table.rows),
        rows: () => pairRows(table.rows),
        filename: () => slug(data.run.key + "-" + layer.key + "-errors"),
        onActivate: interactive
          ? keys => examples.open({ section: layer.key, category: "", keys: keys })
          : null
      }, clipboard);
      if (interactive) examples.register(layer.key, controller);
    }

    if (lemmas) {
      buildErrorSection(doc, container, {
        heading: "Lemmas",
        headingTag: "h4",
        description: "The most frequent confusions between the correct and the predicted lemma.",
        mergeable: true,
        filterPlaceholder: tagPlaceholder({ placeholder: "" }, lemmas.rows),
        rows: () => pairRows(lemmas.rows),
        filename: () => slug(data.run.key + "-lemma-errors")
      }, clipboard);
    } else if (tags.lemma) {
      /* Only when the layer files are missing: the count alone, from the
         diagnostic set. */
      const block = cell(doc, "div", null, "error-section");
      const header = cell(doc, "div", null, "bucket-header");
      header.appendChild(cell(doc, "h4", "Lemmas"));
      block.appendChild(header);
      block.appendChild(cell(doc, "p", "Counted in the total above.", "note section-note"));
      container.appendChild(block);
    }

    /* Features are compared one at a time, so a word wrong in two features adds a
       row to each. A system whose output has no features at all is said to have
       none, with the count read from its file, rather than its rows being read as
       feature errors it made. */
    if (features) {
      const blank = features.compared > 0 && features.predicted_blank === features.compared;
      buildErrorSection(doc, container, {
        heading: "Features",
        headingTag: "h4",
        description: "The most frequent confusions in single universal features. _ means the " +
          "feature is absent: on the left, the test set does not mark it; on the right, the " +
          "system did not predict it. A word can be wrong in more than one feature, so the rows " +
          "add up to more than the total above.",
        notice: blank
          ? layerNotice(doc, "No features in this system's output.",
            "Its FEATS column is _ for all " + formatCount(features.compared) + " words of the " +
            "test set, so every feature the test set marks appears below as missing (→ _).", true)
          : null,
        mergeable: true,
        filterPlaceholder: "e.g. Case or Number",
        rows: () => pairRows(features.rows),
        filename: () => slug(data.run.key + "-feature-errors")
      }, clipboard);
    }

    setAvailabilityNote(doc, "morph-examples-note", examples);
  }

  /* Stated once per layer tab: either how to open the evidence, or why there is
     none. The unavailable wording comes from the examples manifest, so the reason is
     the one the generator recorded — and the "click a row" instruction is never
     shown for a run whose rows do not respond to a click. */
  const EXAMPLES_HINT =
    "Rows marked ↳ open example sentences from the test set (Enter or Space does the " +
    "same; Esc closes them).";

  function setAvailabilityNote(doc, id, examples) {
    const note = doc.getElementById(id);
    if (!note) return;
    const interactive = Boolean(examples && examples.available);
    note.textContent = interactive
      ? EXAMPLES_HINT
      : (examples && examples.note) || EXAMPLES_UNAVAILABLE_NOTE;
    note.hidden = false;
  }

  async function loadJson(browserWindow, url) {
    const response = await browserWindow.fetch(url, { cache: "no-cache" });
    if (!response.ok) throw new Error(url + " returned HTTP " + response.status);
    return response.json();
  }

  /* Diagnostic files are read-only and small, and a reader moves between a handful
     of runs, so each is fetched once per visit. A failed request is forgotten, so a
     later attempt can succeed. */
  const loaded = new Map();

  function loadCached(browserWindow, url) {
    if (!loaded.has(url)) {
      loaded.set(url, loadJson(browserWindow, url).catch(error => {
        loaded.delete(url);
        throw error;
      }));
    }
    return loaded.get(url);
  }

  /* The fixed counterpart of Compare: the same language, system and training setup
     on the other test modality, if the benchmark has it. */
  function counterpartFor(browserWindow, index, run) {
    const other = (index.runs || []).find(item =>
      item.language === run.language && item.model === run.model &&
      item.training_condition === run.training_condition &&
      item.test_condition !== run.test_condition);
    if (!other) return null;
    return {
      run: other,
      name: label("test_condition", other.test_condition),
      load: () => loadCached(browserWindow, DIAGNOSTICS_DIR + other.file)
    };
  }

  /* Marks the tab row while it is pinned to the top of the viewport, which is when
     it names the run. Read on scroll and resize, at most once a frame; the
     listeners belong to the run and are removed with it. */
  function watchPinnedNav(doc, browserWindow, signal) {
    const bar = doc.getElementById("analysis-nav");
    let pending = false;
    const update = () => {
      pending = false;
      const sticky = browserWindow.getComputedStyle(bar).position === "sticky";
      bar.classList.toggle("is-stuck", sticky && bar.getBoundingClientRect().top <= 0.5);
    };
    const schedule = () => {
      if (pending) return;
      pending = true;
      browserWindow.requestAnimationFrame(update);
    };
    browserWindow.addEventListener("scroll", schedule, { passive: true, signal: signal });
    browserWindow.addEventListener("resize", schedule, { signal: signal });
    update();
  }

  /* The same contract check the overview makes, for the same reason: the template
     and this script are cached independently and must not be paired across
     versions. Checked after the template is cloned into the page. */
  const REQUIRED_ELEMENTS = [
    "analysis-title", "analysis-subtitle", "analysis-meta", "analysis-mount",
    "run-summary", "analysis-nav", "section-nav", "nav-run",
    "tab-morphology", "tab-syntax", "tab-all-metrics", "tab-reproducibility",
    "panel-morphology", "panel-syntax", "panel-all-metrics", "panel-reproducibility",
    "upos-acc-table", "upos-acc-compare", "upos-acc-note", "morph-tally", "tag-sections",
    "rel-table", "rel-compare", "rel-note", "dep-tally", "dep-filter", "dep-buckets",
    "morph-examples-note", "syntax-examples-note",
    "metrics-head", "metrics-body", "metrics-note", "all-metrics-note",
    "reproducibility-note", "provenance-body", "result-set-body", "policy-note",
    "examples-panel", "examples-backdrop", "examples-body"
  ];

  /* --------------------------------------------------------------- lifecycle
     One run is mounted at a time. Its markup is a fresh clone of the template, so
     nothing a previous run rendered or wired survives; the listeners it attached
     outside that markup — the examples panel, the document, the window — are bound
     to its AbortController and removed with it. A load that finishes after another
     run was opened is discarded. */

  let session = null;
  let generation = 0;

  function unmount(doc) {
    generation += 1;
    if (session) {
      if (session.examples) session.examples.close();
      session.abort.abort();
      session = null;
    }
    const mountNode = doc.getElementById("analysis-mount");
    if (mountNode) mountNode.replaceChildren();
  }

  /* A loading, missing or failed run: one short statement in place of the tabs. */
  function showStatus(doc, title, message) {
    const mountNode = doc.getElementById("analysis-mount");
    if (!mountNode) return;
    const box = cell(doc, "div", null, "analysis-status");
    box.append(cell(doc, "p", title, "empty-title"));
    if (message) box.append(cell(doc, "p", message, "empty-hint"));
    mountNode.replaceChildren(box);
  }

  async function mount(doc, browserWindow, request, options) {
    unmount(doc);
    const settings = options || {};
    const mine = generation;
    const abort = new AbortController();
    session = { abort: abort, examples: null };
    const stale = () => mine !== generation;

    doc.getElementById("analysis-title").textContent = systemDescription(request);
    doc.getElementById("analysis-subtitle").textContent = contextDescription(request);
    doc.getElementById("analysis-meta").textContent = "";
    showStatus(doc, "Loading the analysis…", "");

    let index;
    try {
      index = await loadCached(browserWindow, DIAGNOSTICS_DIR + INDEX_FILE);
    } catch (error) {
      if (stale()) return null;
      const isFile = String(browserWindow.location.protocol) === "file:";
      showStatus(doc, "Diagnostics unavailable", isFile
        ? "This page was opened from the file system, so the browser refused to load the " +
          "diagnostic set. Serve the tables folder instead: cd tables && python3 -m http.server " +
          "8000, then open http://localhost:8000/am_benchmark_v2/."
        : "The diagnostic set could not be loaded (" + error.message + "). Regenerate it with " +
          "am_benchmark/scripts/build_diagnostics_data.py.");
      return null;
    }
    if (stale()) return null;

    const run = findRun(index, request);
    if (!run) {
      showStatus(doc, "Run not available",
        "The benchmark has no diagnostics for " + requestDescription(request) + ". " +
        "That run may not be part of the evaluated subset.");
      return null;
    }

    /* The examples manifest decides whether this run's rows are interactive, so it
       is needed before any table is built; it is optional, and fetched alongside the
       run's diagnostics rather than after them. */
    const manifest = Promise.all([
      loadCached(browserWindow, EXAMPLES_DIR + INDEX_FILE).catch(() => null),
      loadCached(browserWindow, OWN_EXAMPLES_DIR + INDEX_FILE).catch(() => null)
    ]).then(([shared, own]) => mergeManifests(shared, own));
    /* Optional too: without it the Morphology tab falls back to the lemma count. */
    const layerErrors = loadCached(browserWindow, LAYERS_DIR + run.file).catch(() => null);

    let data;
    try {
      data = await loadCached(browserWindow, DIAGNOSTICS_DIR + run.file);
    } catch (error) {
      if (stale()) return null;
      showStatus(doc, "Diagnostics unavailable",
        "The diagnostics file for this run could not be loaded (" + error.message + ").");
      return null;
    }
    const catalogue = exampleCatalogue(await manifest, run);
    const layers = await layerErrors;
    if (stale()) return null;

    const mountNode = doc.getElementById("analysis-mount");
    mountNode.replaceChildren(doc.getElementById("analysis-template").content.cloneNode(true));
    const absent = overview().missingElements(doc, REQUIRED_ELEMENTS);
    if (absent.length) throw new Error(overview().mismatchMessage(absent));

    doc.getElementById("nav-run").textContent =
      systemDescription(run) + " · " + contextDescription(run);
    watchPinnedNav(doc, browserWindow, abort.signal);

    const tabs = createAnalysisTabs(doc, browserWindow, abort.signal);
    const clipboard = createClipboard(doc, browserWindow);
    const examples = createExamples(doc, browserWindow, run, catalogue, clipboard, tabs, abort.signal);
    session.examples = examples;

    renderSummary(doc, data, resultRow(browserWindow, run));
    renderAccuracySections(doc, run, data, examples, clipboard, counterpartFor(browserWindow, index, run));

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
    renderTagErrors(doc, data, examples, clipboard, layers);

    const hasAllMetrics = renderAllMetrics(
      doc, resultRow(browserWindow, run), browserWindow.AM_BENCHMARK_RESULTS);
    tabs.setAvailable("all-metrics", hasAllMetrics);
    renderProvenance(doc, data, examples, browserWindow.AM_BENCHMARK_RESULTS);

    const requestedSelection = parseExampleSelection(settings.example || "");
    tabs.initialize(examples.available ? examplePanel(requestedSelection) : "");
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
    sourceText,
    parseExampleSelection,
    formatExampleSelection,
    examplePanel,
    mergeRows,
    mergedLabel,
    pairedRows,
    diffText,
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
    mount,
    unmount,
    showStatus
  };
});
