(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.AMBenchmarkUI = api;
})(typeof window !== "undefined" ? window : null, function () {
  "use strict";

  /* The reader builds a comparison context — language, kind of test data, training
     setup — and the table then shows the systems that exist inside it. Nothing here
     enumerates combinations: every option comes from rows actually present in the
     bundle, so a new language, system or condition appears without a code change. */
  const CASCADE = ["language", "test_condition"];
  const TRAINING = "training_condition";
  const CONTEXT_DIMENSIONS = CASCADE.concat([TRAINING]);

  /* Training data is a filter rather than a cascade step: "All" keeps every
     training setup visible, which is what makes the experiment's structure legible.
     Empty state means All; the URL spells it out so a link reads unambiguously. */
  const TRAINING_ALL = "all";

  /* Column groups follow the evaluator's own metric semantics. Only metrics
     present in the bundle are rendered, so a future TSV may add or drop any. */
  const COMPARISON_GROUPS = [
    { name: "Tagging", metrics: ["UPOS", "XPOS", "Lemmas"] },
    { name: "Dependencies", metrics: ["UAS", "LAS"] },
    { name: "Content words", metrics: ["MLAS", "BLEX"] }
  ];

  /* The headline parsing metric: the one a reader compares systems on first. It
     carries a little more weight in the table and nothing else does. */
  const PRIMARY_METRIC = "LAS";

  const METRIC_DESCRIPTIONS = {
    UPOS: "Universal part-of-speech",
    XPOS: "Language-specific part-of-speech",
    Lemmas: "Lemmatization",
    UAS: "Unlabelled attachment score",
    LAS: "Labelled attachment score",
    MLAS: "Morphology-aware labelled attachment score",
    BLEX: "Bi-lexical dependency score"
  };

  /* Layers used to separate the full evaluator output on the analysis page. */
  const METRIC_LAYERS = [
    ["Tokens", "Sentences", "Words"],
    ["UPOS", "XPOS", "UFeats", "AllTags", "Lemmas"],
    ["UAS", "LAS"],
    ["CLAS", "MLAS", "BLEX"]
  ];

  const SCORE_FIELDS = ["precision", "recall", "f1", "aligned_accuracy"];
  const COUNT_FIELDS = ["correct", "gold", "predicted", "aligned"];

  const AUTHORITATIVE_GOLD = ["CONFIRMED", "AUTHORITATIVE"];

  /* Display names. Anything absent falls through to the raw manifest identifier,
     so new languages, systems and conditions appear without a code change. The
     interface never shows an identifier like "writtenandspokentrain" as copy. */
  const LABELS = {
    language: { EN: "English", NL: "Dutch", SL: "Slovenian" },
    model: { spacy: "spaCy", stanza: "Stanza", trankit: "Trankit" },
    training_condition: {
      default: "Default",
      writtentrain: "Written",
      writtenandspokentrain: "Written + spoken",
      writtenanddialecttrain: "Written + dialect"
    },
    test_condition: { writtentest: "Written", spokentest: "Spoken", dialecttest: "Dialect" },
    metric_field: {
      precision: "Precision",
      recall: "Recall",
      f1: "F1",
      aligned_accuracy: "Aligned acc.",
      correct: "Correct",
      gold: "Gold",
      predicted: "Predicted",
      aligned: "Aligned"
    }
  };

  const QUERY_NAMES = {
    language: "lang",
    test_condition: "test",
    model: "model",
    training_condition: "training"
  };

  const SORT_LABELS = {
    model: "System",
    training_condition: "Training"
  };

  /* Own-property lookup only: an inherited key such as "constructor" or
     "toString" must never be treated as a display name. */
  function lookup(table, key) {
    return table && Object.prototype.hasOwnProperty.call(table, key) ? table[key] : undefined;
  }

  function label(field, value) {
    const found = lookup(lookup(LABELS, field), value);
    return found === undefined ? value : found;
  }

  function matches(row, filters) {
    return Object.entries(filters).every(([field, value]) => !value || row[field] === value);
  }

  /* Values available for one context dimension, given the dimensions before it. */
  function contextValues(data, state, dimension) {
    const index = CONTEXT_DIMENSIONS.indexOf(dimension);
    const prefix = {};
    for (const field of CONTEXT_DIMENSIONS.slice(0, index)) prefix[field] = state[field];
    const present = new Set(data.rows.filter(row => matches(row, prefix)).map(row => row[dimension]));
    return (data.dimensions[dimension] || []).filter(value => present.has(value));
  }

  function resolveContext(data, requested) {
    const state = {};
    let invalid = false;
    for (const dimension of CASCADE) {
      const options = contextValues(data, state, dimension);
      const wanted = requested[dimension];
      if (wanted && options.includes(wanted)) state[dimension] = wanted;
      else {
        if (wanted) invalid = true;
        state[dimension] = options[0] || "";
      }
    }
    const wanted = requested[TRAINING];
    if (!wanted || wanted === TRAINING_ALL) state[TRAINING] = "";
    else if (contextValues(data, state, TRAINING).includes(wanted)) state[TRAINING] = wanted;
    else {
      invalid = true;
      state[TRAINING] = "";
    }
    return { state, invalid };
  }

  function orderIndex(data, field, value) {
    const order = data.dimensions[field] || [];
    const index = order.indexOf(value);
    return index === -1 ? order.length : index;
  }

  /* Every row for the context, in manifest order: system, then training. */
  function rowsFor(data, state) {
    return data.rows
      .filter(row => matches(row, state))
      .slice()
      .sort((a, b) =>
        orderIndex(data, "model", a.model) - orderIndex(data, "model", b.model) ||
        orderIndex(data, "training_condition", a.training_condition) -
          orderIndex(data, "training_condition", b.training_condition));
  }

  function runId(row) {
    return row ? row.model + " " + row.training_condition : "";
  }

  function findRun(rows, model, training) {
    return rows.find(row => row.model === model && row.training_condition === training) || null;
  }

  function metricValue(row, metric, field) {
    const entry = row && row.metrics && lookup(row.metrics, metric);
    const value = entry ? lookup(entry, field) : undefined;
    return value === undefined ? null : value;
  }

  function isAuthoritative(row) {
    if (!row || row.result_status !== "success") return false;
    const status = String(row.gold_status || "").toUpperCase();
    return AUTHORITATIVE_GOLD.includes(status) && !row.benchmark_use_notice;
  }

  function unavailableReason(row) {
    if (!row) return "No result available for this combination.";
    const result = String(row.result_status || "").toLowerCase();
    const gold = String(row.gold_status || "").toUpperCase();
    if (result === "success") return "";
    if (result === "excluded") return "Excluded from the benchmark.";
    if (gold.includes("MISSING")) return "Gold data not yet available.";
    return row.error_message || "No result available.";
  }

  /* Metrics the bundle actually carries, grouped for the comparison header. */
  function comparisonGroups(data) {
    const present = new Set((data.metrics || []).map(metric => metric.name));
    return COMPARISON_GROUPS
      .map(group => ({ name: group.name, metrics: group.metrics.filter(name => present.has(name)) }))
      .filter(group => group.metrics.length);
  }

  function comparisonMetrics(data) {
    return comparisonGroups(data).flatMap(group => group.metrics);
  }

  /* Highest F1 per column, over successful rows only. Ties all count as best.
     A single row has no "best", so nothing is emphasised. */
  function bestValues(rows, metrics) {
    const successes = rows.filter(row => row.result_status === "success");
    const best = {};
    if (successes.length < 2) return best;
    for (const metric of metrics) {
      const values = successes
        .map(row => metricValue(row, metric, "f1"))
        .filter(value => typeof value === "number" && !Number.isNaN(value));
      if (values.length > 1) best[metric] = Math.max.apply(null, values);
    }
    return best;
  }

  /* ------------------------------------------------------------------ ordering
     Two shapes, because the table has two jobs. With one training setup selected
     it is a leaderboard and rows sort freely. With All selected it shows each
     system's three training runs together, and sorting must never break that
     grouping: a metric orders the *groups* by their best value, and the training
     column orders rows *inside* each group. Nothing scatters a system's runs. */

  function groupRows(rows) {
    const groups = [];
    const index = new Map();
    for (const row of rows) {
      if (!index.has(row.model)) {
        index.set(row.model, { model: row.model, rows: [] });
        groups.push(index.get(row.model));
      }
      index.get(row.model).rows.push(row);
    }
    return groups;
  }

  function bestInGroup(group, metric) {
    const values = group.rows
      .map(row => metricValue(row, metric, "f1"))
      .filter(value => typeof value === "number" && !Number.isNaN(value));
    return values.length ? Math.max.apply(null, values) : null;
  }

  function sortGroups(rows, sort, data) {
    const modelOrder = (a, b) => orderIndex(data, "model", a.model) - orderIndex(data, "model", b.model);
    const trainingOrder = (a, b) =>
      orderIndex(data, TRAINING, a[TRAINING]) - orderIndex(data, TRAINING, b[TRAINING]);
    const groups = groupRows(rows.slice().sort((a, b) => modelOrder(a, b) || trainingOrder(a, b)));
    if (!sort || !sort.key) return groups;
    const direction = sort.direction === "asc" ? 1 : -1;

    if (sort.key === TRAINING) {
      for (const group of groups) group.rows.sort((a, b) => trainingOrder(a, b) * direction);
      return groups;
    }
    if (sort.key === "model") {
      groups.sort((a, b) => modelOrder(a, b) * direction);
      return groups;
    }
    groups.sort((a, b) => {
      const left = bestInGroup(a, sort.key);
      const right = bestInGroup(b, sort.key);
      if (left == null && right == null) return modelOrder(a, b);
      if (left == null) return 1;
      if (right == null) return -1;
      return (left - right) * direction || modelOrder(a, b);
    });
    return groups;
  }

  function sortRows(rows, sort, data) {
    const dimensionOrder = (field, a, b) =>
      orderIndex(data, field, a[field]) - orderIndex(data, field, b[field]);
    const naturalOrder = (a, b) =>
      dimensionOrder("model", a, b) || dimensionOrder(TRAINING, a, b);
    const copy = rows.slice();
    if (!sort || !sort.key) return copy.sort(naturalOrder);

    const direction = sort.direction === "asc" ? 1 : -1;
    copy.sort((a, b) => {
      if (sort.key === "model") {
        return dimensionOrder("model", a, b) * direction || dimensionOrder(TRAINING, a, b);
      }
      if (sort.key === TRAINING) {
        return dimensionOrder(TRAINING, a, b) * direction || dimensionOrder("model", a, b);
      }
      const left = metricValue(a, sort.key, "f1");
      const right = metricValue(b, sort.key, "f1");
      /* Rows without a value always sink, in either direction. */
      if (left == null && right == null) return naturalOrder(a, b);
      if (left == null) return 1;
      if (right == null) return -1;
      return (left - right) * direction || naturalOrder(a, b);
    });
    return copy;
  }

  function firstSortDirection(key) {
    return key === "model" || key === TRAINING ? "asc" : "desc";
  }

  function sortLabel(key) {
    return SORT_LABELS[key] || key;
  }

  function parseRequest(search) {
    const params = new URLSearchParams(search || "");
    /* "language" is the first prototype's parameter name; accepting it means an
       older shared link restores the same context instead of failing. */
    return {
      language: params.get(QUERY_NAMES.language) || params.get("language") || "",
      test_condition: params.get(QUERY_NAMES.test_condition) || "",
      model: params.get(QUERY_NAMES.model) || "",
      training_condition: params.get(QUERY_NAMES.training_condition) || ""
    };
  }

  /* Two decimals, not one. Rounding to a single decimal collapses genuinely
     different scores into a tie in thirteen of this bundle's context/metric
     combinations — Slovenian written LAS reaches 93.38 and 93.40 — which would
     make the best-value emphasis arbitrary. */
  function formatScore(value) {
    if (value == null || Number.isNaN(Number(value))) return "—";
    return Number(value).toFixed(2);
  }

  function formatCount(value) {
    return value == null ? "—" : String(value);
  }

  function cell(tag, text, className) {
    const node = document.createElement(tag);
    if (text != null) node.textContent = text;
    if (className) node.className = className;
    return node;
  }

  function contextDescription(state) {
    return [label("language", state.language), label("test_condition", state.test_condition)]
      .filter(Boolean)
      .join(" · ");
  }

  /* The heading over the table, in the reader's words rather than the manifest's. */
  function contextTitle(state) {
    const parts = [label("language", state.language)];
    if (state.test_condition) parts.push(label("test_condition", state.test_condition) + " test data");
    return parts.join(" · ");
  }

  function countSummary(rows, state) {
    const systems = new Set(rows.map(row => row.model)).size;
    const parts = [
      systems + (systems === 1 ? " system" : " systems"),
      rows.length + (rows.length === 1 ? " run" : " runs")
    ];
    if (state[TRAINING]) {
      parts.push(label(TRAINING, state[TRAINING]) + " training");
    }
    return parts.join(" · ");
  }

  /* One exact run, addressed the way the analysis page expects it. */
  function analysisUrl(state, row) {
    const params = new URLSearchParams();
    params.set(QUERY_NAMES.language, row.language);
    params.set(QUERY_NAMES.test_condition, row.test_condition);
    params.set(QUERY_NAMES.model, row.model);
    params.set(QUERY_NAMES.training_condition, row.training_condition);
    return "analysis.html?" + params.toString();
  }

  /* index.html and app.js are separate files that a browser caches independently,
     so a reader can end up running one version's script against another version's
     markup. That fails deep inside rendering as an opaque null reference, so the
     contract between the two is checked once, up front, and reported in terms the
     reader can act on. The ?v= query on the script tags is what prevents the pairing
     in the first place; this is the net under it. */
  const REQUIRED_ELEMENTS = [
    "language-control", "test-control", "training-control",
    "context-title", "context-meta", "context-note",
    "caveat", "request-note", "empty",
    "table-wrap", "comparison", "comparison-cols", "comparison-head",
    "source-details", "url-note"
  ];

  function missingElements(doc, required) {
    return (required || REQUIRED_ELEMENTS).filter(id => !doc.getElementById(id));
  }

  function mismatchMessage(missing) {
    return "This page's markup does not match its script (missing: " +
      missing.join(", ") + "). The browser is most likely serving a cached copy of " +
      "one of them — reload with Ctrl+Shift+R, or Cmd+Shift+R on macOS.";
  }

  function start(data, doc, browserWindow) {
    if (!data || !Array.isArray(data.rows) || !data.rows.length) {
      throw new Error("The result bundle contains no rows.");
    }
    const missing = missingElements(doc);
    if (missing.length) throw new Error(mismatchMessage(missing));

    /* Reading location is guarded for the same reason writeUrl is: a restricted
       origin must cost the reader their deep link, not the whole interface. */
    let requested;
    try {
      requested = parseRequest(browserWindow.location.search);
    } catch (error) {
      requested = parseRequest("");
    }
    let context = resolveContext(data, requested);
    let state = context.state;
    let invalidRequest = context.invalid;
    let urlSyncBlocked = false;
    let userSorted = false;

    const metrics = comparisonMetrics(data);
    const groups = comparisonGroups(data);
    const hasPrimary = metrics.includes(PRIMARY_METRIC);

    const singleTraining = () => Boolean(state[TRAINING]);
    const defaultSort = () =>
      singleTraining() && hasPrimary ? { key: PRIMARY_METRIC, direction: "desc" } : { key: null, direction: null };
    let sort = defaultSort();

    /* Syncing the address bar is a convenience, not part of rendering a result.
       Some environments refuse History API writes outright — a document with an
       opaque origin (most commonly a page opened over file://, or one embedded in
       a sandboxed frame) makes replaceState throw SecurityError. That must degrade
       to "links are not shareable here", never to a failed interface, so the call
       is isolated and disabled after the first refusal rather than retried on
       every render. */
    function writeUrl() {
      const params = new URLSearchParams();
      params.set(QUERY_NAMES.language, state.language);
      params.set(QUERY_NAMES.test_condition, state.test_condition);
      params.set(QUERY_NAMES[TRAINING], state[TRAINING] || TRAINING_ALL);
      const query = params.toString();
      doc.body.dataset.stateUrl = query;

      if (urlSyncBlocked) return;
      try {
        browserWindow.history.replaceState(null, "", browserWindow.location.pathname + "?" + query);
      } catch (error) {
        urlSyncBlocked = true;
        doc.body.dataset.urlSync = "blocked";
        reportUrlSyncBlocked(error);
      }
    }

    function reportUrlSyncBlocked(error) {
      const note = doc.getElementById("url-note");
      if (!note) return;
      const isFile = String(browserWindow.location.protocol) === "file:";
      note.textContent = isFile
        ? "Opened directly from the file system, so this browser will not update the address bar: " +
          "selections work, but the URL cannot be shared or bookmarked. Serve the directory over HTTP " +
          "(python3 -m http.server) to get shareable links."
        : "This browser blocked address-bar updates in the current context (" +
          (error && error.name ? error.name : "SecurityError") + "), so selections work but the URL " +
          "cannot be shared or bookmarked.";
      note.hidden = false;
    }

    /* --------------------------------------------------------------- controls */

    function renderContextControl(dimension, container, labelId, extra) {
      const values = contextValues(data, state, dimension);
      const options = (extra || []).concat(values.map(value => ({
        value: value,
        text: label(dimension, value)
      })));
      container.replaceChildren();

      /* A handful of values reads better as a segmented control; a long list
         (a future benchmark may have many) falls back to a native select. */
      if (options.length <= 5) {
        const group = doc.createElement("div");
        group.className = "seg";
        group.setAttribute("role", "group");
        group.setAttribute("aria-labelledby", labelId);
        for (const option of options) {
          const button = doc.createElement("button");
          button.type = "button";
          button.className = "seg-btn";
          button.textContent = option.text;
          const selected = option.value === (state[dimension] || "");
          button.setAttribute("aria-pressed", String(selected));
          if (options.length === 1) button.setAttribute("aria-disabled", "true");
          else button.addEventListener("click", () => choose(dimension, option.value));
          group.appendChild(button);
        }
        container.appendChild(group);
        return;
      }

      const select = doc.createElement("select");
      select.setAttribute("aria-labelledby", labelId);
      for (const option of options) {
        const node = doc.createElement("option");
        node.value = option.value;
        node.textContent = option.text;
        node.selected = option.value === (state[dimension] || "");
        select.appendChild(node);
      }
      select.addEventListener("change", event => choose(dimension, event.target.value));
      container.appendChild(select);
    }

    function choose(dimension, value) {
      const current = state[dimension] || "";
      if (current === value) return;
      const wasSingle = singleTraining();
      const next = Object.assign({}, state, { [dimension]: value });
      /* Later context dimensions may not survive an earlier change. */
      for (const downstream of CONTEXT_DIMENSIONS.slice(CONTEXT_DIMENSIONS.indexOf(dimension) + 1)) {
        if (downstream !== TRAINING) delete next[downstream];
      }
      state = resolveContext(data, next).state;
      /* A choice the reader just made is never a broken link. */
      invalidRequest = false;
      if (wasSingle !== singleTraining()) reconcileSort();
      render();
    }

    /* The two table shapes do not share every sort key, and an untouched table
       should open in the ordering that suits the shape it is in. */
    function reconcileSort() {
      const valid = sort.key === "model" ||
        metrics.includes(sort.key) ||
        (sort.key === TRAINING && !singleTraining());
      if (!userSorted || !valid) sort = defaultSort();
    }

    /* ------------------------------------------------------------------ table */

    function renderHead() {
      const grouped = !singleTraining();
      const colgroup = doc.getElementById("comparison-cols");
      colgroup.replaceChildren();
      colgroup.appendChild(cell("col", null, "c-model"));
      if (grouped) colgroup.appendChild(cell("col", null, "c-train"));
      for (let index = 0; index < metrics.length; index += 1) {
        colgroup.appendChild(cell("col", null, "c-metric"));
      }
      colgroup.appendChild(cell("col", null, "c-action"));

      const head = doc.getElementById("comparison-head");
      head.replaceChildren();

      const groupRow = doc.createElement("tr");
      groupRow.className = "groups";
      const spacer = cell("th", "");
      spacer.colSpan = grouped ? 2 : 1;
      groupRow.appendChild(spacer);
      for (const group of groups) {
        const th = cell("th", group.name, "grp");
        th.colSpan = group.metrics.length;
        th.scope = "colgroup";
        groupRow.appendChild(th);
      }
      groupRow.appendChild(cell("th", ""));
      head.appendChild(groupRow);

      const columnRow = doc.createElement("tr");
      columnRow.className = "cols";
      columnRow.appendChild(sortableHeader("model", "System", ""));
      if (grouped) columnRow.appendChild(sortableHeader(TRAINING, "Training", ""));
      for (const group of groups) {
        group.metrics.forEach((metric, index) => {
          let className = "num" + (index === 0 ? " grp-start" : "");
          if (metric === PRIMARY_METRIC) className += " primary";
          columnRow.appendChild(sortableHeader(metric, metric, className));
        });
      }
      const action = cell("th", null, "c-action");
      action.scope = "col";
      action.appendChild(cell("span", "Run", "sr-only"));
      columnRow.appendChild(action);
      head.appendChild(columnRow);
    }

    /* Sorting follows the CJVT table's model: a click on a new column sorts by it,
       a click on the column already sorted reverses it, and sorting is never turned
       off by accident — clearing is an explicit ✕ on the active header that restores
       the table's natural order. Enter and Space do the same as a click. */
    function sortableHeader(key, text, className) {
      const th = cell("th", null, (className + " sortable").trim());
      th.scope = "col";
      th.tabIndex = 0;
      th.dataset.sortKey = key;
      const active = sort.key === key;
      const numeric = className.indexOf("num") !== -1;
      th.setAttribute("aria-sort", active ? (sort.direction === "asc" ? "ascending" : "descending") : "none");
      th.setAttribute("aria-label", text + ". Activate to sort.");
      th.title = active ? "Click to reverse the sort" : "Click to sort by " + text;

      /* Reserved at a constant width so activating a sort never re-flows the row,
         and leading on a right-aligned column so the label keeps the numbers' edge. */
      const indicator = cell("span", null, "sort-ind");
      indicator.append(cell("span", active ? (sort.direction === "asc" ? "↑" : "↓") : "", "sort-arrow"));

      const label = cell("span", text, "col-label");
      const description = METRIC_DESCRIPTIONS[key];
      if (description) {
        /* The expansion of the abbreviation, on hover and on keyboard focus, and
           announced through aria-describedby rather than duplicated into the name. */
        label.classList.add("has-tip");
        const tipId = "tip-" + key.replace(/[^A-Za-z0-9_-]/g, "");
        const tip = cell("span", description, "col-tip");
        tip.id = tipId;
        tip.setAttribute("role", "tooltip");
        th.setAttribute("aria-describedby", tipId);
        th.dataset.key = key;
        if (numeric) th.append(indicator, label, tip);
        else th.append(label, indicator, tip);
      } else if (numeric) {
        th.append(indicator, label);
      } else {
        th.append(label, indicator);
      }

      const activate = () => {
        userSorted = true;
        if (sort.key !== key) sort = { key: key, direction: firstSortDirection(key) };
        else sort = { key: key, direction: sort.direction === "asc" ? "desc" : "asc" };
        render();
        focusHeader(key);
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

    /* Clearing a sort is explicit, as in the CJVT table — a click on a header only
       ever reverses it. The control lives on the summary line rather than inside a
       header, where at a 106px column width it sat on the cell's centre and was easy
       to hit when aiming to reverse the sort. */
    function renderContextMeta(rows) {
      const meta = doc.getElementById("context-meta");
      meta.replaceChildren();
      if (!rows.length) return;
      meta.append(doc.createTextNode(countSummary(rows, state)));
      if (!sort.key) return;
      meta.append(cell("span", "Sorted by " + sortLabel(sort.key) +
        (sort.direction === "asc" ? " ↑" : " ↓"), "sort-status"));
      const clear = cell("button", "Clear sort", "inline-toggle");
      clear.type = "button";
      clear.addEventListener("click", () => {
        sort = { key: null, direction: null };
        userSorted = false;
        render();
      });
      meta.appendChild(clear);
    }

    /* The header row is rebuilt on every render, so focus has to be put back on the
       column the reader just acted on. */
    function focusHeader(key) {
      const th = doc.querySelector('#comparison thead th[data-sort-key="' + key + '"]');
      if (th && typeof th.focus === "function") th.focus();
    }

    function scoreCells(tr, row, best) {
      const reason = unavailableReason(row);
      if (reason) {
        const td = cell("td", reason, "no-data-cell");
        td.colSpan = metrics.length;
        tr.appendChild(td);
        tr.classList.add("no-data");
        return;
      }
      for (const group of groups) {
        group.metrics.forEach((metric, index) => {
          const value = metricValue(row, metric, "f1");
          let className = "num" + (index === 0 ? " grp-start" : "");
          if (metric === PRIMARY_METRIC) className += " primary";
          if (best[metric] != null && value === best[metric]) className += " best";
          const td = cell("td", formatScore(value), className);
          if (className.indexOf("best") !== -1) {
            td.appendChild(cell("span", " (best)", "sr-only"));
          }
          tr.appendChild(td);
        });
      }
    }

    /* The visible action teaches what a row does; the whole row stays clickable
       as a convenience. The link is the only tab stop, so keyboard users get one
       predictable target per run rather than two. */
    function actionCell(tr, row, mixedStatus) {
      const td = cell("td", null, "c-action");
      const link = doc.createElement("a");
      link.className = "analyse";
      link.href = analysisUrl(state, row);
      link.append(doc.createTextNode("Analyse"));
      link.append(cell("span", "→", "arrow"));
      link.setAttribute("aria-label",
        "Analyse " + label("model", row.model) + ", " +
        label(TRAINING, row[TRAINING]) + " training, " + contextDescription(state) + " test data");
      td.appendChild(link);
      tr.appendChild(td);

      tr.classList.add("actionable");
      tr.addEventListener("click", event => {
        if (event.defaultPrevented || event.button || event.metaKey || event.ctrlKey ||
            event.shiftKey || event.altKey) return;
        if (event.target.closest("a")) return;
        link.click();
      });
      if (mixedStatus && row.result_status === "success" && !isAuthoritative(row)) {
        tr.classList.add("provisional");
      }
    }

    function renderTable(rows, mixedStatus) {
      const table = doc.getElementById("comparison");
      for (const body of Array.from(table.tBodies)) table.removeChild(body);
      const best = bestValues(rows, metrics);
      const grouped = !singleTraining();

      const makeRow = row => {
        return doc.createElement("tr");
      };

      if (!grouped) {
        const body = doc.createElement("tbody");
        for (const row of sortRows(rows, sort, data)) {
          const tr = makeRow(row);
          const th = cell("th", label("model", row.model), "model");
          th.scope = "row";
          tr.appendChild(th);
          scoreCells(tr, row, best);
          actionCell(tr, row, mixedStatus);
          body.appendChild(tr);
        }
        table.appendChild(body);
        return;
      }

      /* One tbody per system, with the system named once for the whole group.
         scope="rowgroup" keeps that association for assistive technology, so the
         name is not lost on the second and third training rows. */
      for (const group of sortGroups(rows, sort, data)) {
        const body = doc.createElement("tbody");
        body.className = "system-group";
        group.rows.forEach((row, index) => {
          const tr = makeRow(row);
          if (index === 0) {
            const th = cell("th", label("model", row.model), "model");
            th.scope = "rowgroup";
            th.rowSpan = group.rows.length;
            tr.appendChild(th);
          }
          const trainingCell = cell("td", label(TRAINING, row[TRAINING]), "train");
          if (mixedStatus && row.result_status === "success" && !isAuthoritative(row)) {
            trainingCell.append(cell("span", " †", "flag"));
          }
          tr.appendChild(trainingCell);
          scoreCells(tr, row, best);
          actionCell(tr, row, mixedStatus);
          body.appendChild(tr);
        });
        table.appendChild(body);
      }
    }

    /* Status is read from the rows, never assumed. Returns true when the context
       mixes confirmed and unconfirmed gold, so the table marks the exceptions. */
    function renderCaveat(rows) {
      const node = doc.getElementById("caveat");
      const evaluated = rows.filter(row => row.result_status === "success");
      const provisional = evaluated.filter(row => !isAuthoritative(row));
      if (!provisional.length) {
        node.hidden = true;
        return false;
      }
      node.replaceChildren();
      if (provisional.length === evaluated.length) {
        node.append(cell("strong", "Provisional results — gold version not yet confirmed."));
        node.append(doc.createTextNode(
          " The scores are reproducible evaluator output over the prediction and gold files named " +
          "on each run's analysis page, but the gold release has not been confirmed for this " +
          "benchmark. Not citable as benchmark results."
        ));
        node.hidden = false;
        return false;
      }
      node.append(cell("strong", "Mixed gold status."));
      node.append(doc.createTextNode(
        " " + provisional.length + " of " + evaluated.length +
        " runs (†) use gold whose version is not yet confirmed; the rest are confirmed."
      ));
      node.hidden = false;
      return true;
    }

    function render() {
      renderContextControl("language", doc.getElementById("language-control"), "language-label");
      renderContextControl("test_condition", doc.getElementById("test-control"), "test-label");
      renderContextControl(TRAINING, doc.getElementById("training-control"), "training-label",
        [{ value: "", text: "All" }]);

      const rows = rowsFor(data, state);

      doc.getElementById("context-title").textContent = contextTitle(state);
      renderContextMeta(rows);

      const empty = doc.getElementById("empty");
      const wrap = doc.getElementById("table-wrap");
      const note = doc.getElementById("context-note");
      const hasRows = rows.length > 0;
      empty.hidden = hasRows;
      wrap.hidden = !hasRows;
      note.hidden = !hasRows;

      if (!hasRows) {
        empty.replaceChildren();
        empty.append(cell("p", "No results for this combination", "empty-title"));
        empty.append(cell("p", "Try another test or training condition.", "empty-hint"));
        doc.getElementById("caveat").hidden = true;
      } else {
        renderHead();
        const mixed = renderCaveat(rows);
        renderTable(rows, mixed);

        const parts = ["Scores are F1 unless noted. Higher is better."];
        if (Object.keys(bestValues(rows, metrics)).length) {
          parts.push("Bold marks the best value in each column.");
        }
        if (mixed) parts.push("† marks a run whose gold version is unconfirmed.");
        note.textContent = parts.join(" ");
      }

      const request = doc.getElementById("request-note");
      request.hidden = !invalidRequest;
      request.textContent = invalidRequest
        ? "Part of the requested link was unavailable, so the nearest existing results are shown."
        : "";

      /* The file this page was built from, kept for citation and reproduction but
         behind a disclosure: a path and a checksum are implementation facts, not
         something a reader needs in front of the results. */
      const details = doc.getElementById("source-details");
      details.replaceChildren();
      for (const entry of [
        ["Result set", data.source.path, true],
        ["Rows", String(data.source.row_count), false],
        ["SHA-256", data.source.sha256, true]
      ]) {
        if (!entry[1]) continue;
        details.append(cell("dt", entry[0]), cell("dd", entry[1], entry[2] ? "mono" : ""));
      }

      writeUrl();
      doc.body.dataset.uiReady = "true";
    }

    render();
    return {
      getState: () => Object.assign({}, state),
      getSort: () => Object.assign({}, sort)
    };
  }

  return {
    CONTEXT_DIMENSIONS,
    TRAINING_ALL,
    PRIMARY_METRIC,
    METRIC_DESCRIPTIONS,
    METRIC_LAYERS,
    SCORE_FIELDS,
    COUNT_FIELDS,
    QUERY_NAMES,
    REQUIRED_ELEMENTS,
    missingElements,
    mismatchMessage,
    label,
    lookup,
    contextValues,
    resolveContext,
    rowsFor,
    runId,
    findRun,
    metricValue,
    comparisonMetrics,
    comparisonGroups,
    bestValues,
    groupRows,
    sortGroups,
    sortRows,
    sortLabel,
    contextTitle,
    countSummary,
    analysisUrl,
    isAuthoritative,
    unavailableReason,
    parseRequest,
    formatScore,
    formatCount,
    start
  };
});

if (typeof window !== "undefined") {
  window.addEventListener("DOMContentLoaded", function () {
    /* This module is also loaded by the analysis page for its display names, metric
       vocabulary and URL helpers, so the comparison interface only starts on its
       own page. */
    if (document.body.dataset.ui !== "overview") return;
    try {
      window.AMBenchmarkUI.start(window.AM_BENCHMARK_RESULTS, document, window);
    } catch (error) {
      const target = document.getElementById("app-error");
      if (target) {
        target.hidden = false;
        target.textContent = "The interface could not start: " + error.message;
      }
      document.body.dataset.uiReady = "error";
      console.error(error);
    }
  });
}
