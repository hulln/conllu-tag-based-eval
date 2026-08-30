(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.AMBenchmarkUI = api;
})(typeof window !== "undefined" ? window : null, function () {
  "use strict";

  /* The reader fixes the comparison context; model and training condition then
     become the table's rows. Nothing here enumerates combinations — available
     values always come from the rows actually present in the bundle. */
  const CONTEXT_DIMENSIONS = ["language", "test_condition"];

  /* Column groups follow the evaluator's own metric semantics. Only metrics
     present in the bundle are rendered, so a future TSV may add or drop any. */
  const COMPARISON_GROUPS = [
    { name: "Tagging", metrics: ["UPOS", "XPOS", "Lemmas"] },
    { name: "Dependencies", metrics: ["UAS", "LAS"] },
    { name: "Content words", metrics: ["MLAS", "BLEX"] }
  ];

  const METRIC_DESCRIPTIONS = {
    UPOS: "Universal part-of-speech",
    XPOS: "Language-specific part-of-speech",
    Lemmas: "Lemmatization",
    UAS: "Unlabelled Attachment Score",
    LAS: "Labelled Attachment Score",
    MLAS: "Morphology-Aware Labelled Attachment Score",
    BLEX: "Bi-lexical Dependency Score"
  };

  /* Layers used to separate the full evaluator output in the detail table. */
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
     so new languages, systems and conditions appear without a code change. */
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
    for (const dimension of CONTEXT_DIMENSIONS) {
      const options = contextValues(data, state, dimension);
      const wanted = requested[dimension];
      if (wanted && options.includes(wanted)) state[dimension] = wanted;
      else {
        if (wanted) invalid = true;
        state[dimension] = options[0] || "";
      }
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

  function sortRows(rows, sort, data) {
    if (!sort || !sort.key) return rows;
    const direction = sort.direction === "asc" ? 1 : -1;
    const copy = rows.slice();
    copy.sort((a, b) => {
      if (sort.key === "model" || sort.key === "training_condition") {
        const left = label(sort.key, a[sort.key]);
        const right = label(sort.key, b[sort.key]);
        return left.localeCompare(right) * direction ||
          orderIndex(data, "model", a.model) - orderIndex(data, "model", b.model);
      }
      const left = metricValue(a, sort.key, "f1");
      const right = metricValue(b, sort.key, "f1");
      /* Rows without a value always sink, in either direction. */
      if (left == null && right == null) return 0;
      if (left == null) return 1;
      if (right == null) return -1;
      return (left - right) * direction;
    });
    return copy;
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

  function start(data, doc, browserWindow) {
    if (!data || !Array.isArray(data.rows) || !data.rows.length) {
      throw new Error("The result bundle contains no rows.");
    }

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
    let sort = { key: null, direction: "desc" };
    let openRun = "";
    let urlSyncBlocked = false;

    const metrics = comparisonMetrics(data);
    const groups = comparisonGroups(data);

    /* Restore an opened run from the URL only if it exists in this context. */
    const initialRows = rowsFor(data, state);
    if (requested.model && requested.training_condition) {
      const wanted = findRun(initialRows, requested.model, requested.training_condition);
      if (wanted) openRun = runId(wanted);
      else invalidRequest = true;
    }

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
      const rows = rowsFor(data, state);
      const open = rows.find(row => runId(row) === openRun);
      if (open) {
        params.set(QUERY_NAMES.model, open.model);
        params.set(QUERY_NAMES.training_condition, open.training_condition);
      }
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

    function renderContextControl(dimension, container, labelId) {
      const options = contextValues(data, state, dimension);
      container.replaceChildren();

      /* A handful of values reads better as a segmented control; a long list
         (a future benchmark may have many) falls back to a native select. */
      if (options.length <= 4) {
        const group = doc.createElement("div");
        group.className = "seg";
        group.setAttribute("role", "group");
        group.setAttribute("aria-labelledby", labelId);
        for (const value of options) {
          const button = doc.createElement("button");
          button.type = "button";
          button.className = "seg-btn" + (options.length === 1 ? " solo" : "");
          button.textContent = label(dimension, value);
          button.setAttribute("aria-pressed", String(value === state[dimension]));
          if (options.length === 1) button.setAttribute("aria-disabled", "true");
          else button.addEventListener("click", () => choose(dimension, value));
          group.appendChild(button);
        }
        container.appendChild(group);
        return;
      }

      const select = doc.createElement("select");
      select.setAttribute("aria-labelledby", labelId);
      for (const value of options) {
        const option = doc.createElement("option");
        option.value = value;
        option.textContent = label(dimension, value);
        option.selected = value === state[dimension];
        select.appendChild(option);
      }
      select.addEventListener("change", event => choose(dimension, event.target.value));
      container.appendChild(select);
    }

    function choose(dimension, value) {
      if (state[dimension] === value) return;
      const next = Object.assign({}, state, { [dimension]: value });
      /* Later context dimensions may not survive an earlier change. */
      for (const downstream of CONTEXT_DIMENSIONS.slice(CONTEXT_DIMENSIONS.indexOf(dimension) + 1)) {
        delete next[downstream];
      }
      const previous = data.rows.find(row => runId(row) === openRun);
      state = resolveContext(data, next).state;
      invalidRequest = false;
      /* Keep the same system/training open across a context change when it exists. */
      const carried = previous && findRun(rowsFor(data, state), previous.model, previous.training_condition);
      openRun = carried ? runId(carried) : "";
      render();
    }

    function renderHead() {
      const colgroup = doc.getElementById("comparison-cols");
      colgroup.replaceChildren();
      for (const className of ["c-model", "c-train"]) {
        const col = doc.createElement("col");
        col.className = className;
        colgroup.appendChild(col);
      }
      for (let index = 0; index < metrics.length; index += 1) {
        const col = doc.createElement("col");
        col.className = "c-metric";
        colgroup.appendChild(col);
      }

      const head = doc.getElementById("comparison-head");
      head.replaceChildren();

      const groupRow = doc.createElement("tr");
      groupRow.className = "groups";
      const spacer = cell("th", "");
      spacer.colSpan = 2;
      groupRow.appendChild(spacer);
      for (const group of groups) {
        const th = cell("th", group.name, "grp");
        th.colSpan = group.metrics.length;
        groupRow.appendChild(th);
      }
      head.appendChild(groupRow);

      const columnRow = doc.createElement("tr");
      columnRow.className = "cols";
      columnRow.appendChild(sortableHeader("model", "System", ""));
      columnRow.appendChild(sortableHeader("training_condition", "Training data", ""));
      for (const group of groups) {
        group.metrics.forEach((metric, index) => {
          columnRow.appendChild(sortableHeader(
            metric,
            metric,
            "num" + (index === 0 ? " grp-start" : ""),
            METRIC_DESCRIPTIONS[metric]
          ));
        });
      }
      head.appendChild(columnRow);
    }

    function sortableHeader(key, text, className, description) {
      const th = cell("th", null, (className + " sortable").trim());
      th.scope = "col";
      th.tabIndex = 0;
      th.setAttribute("role", "columnheader");
      const active = sort.key === key;
      th.setAttribute("aria-sort", active ? (sort.direction === "asc" ? "ascending" : "descending") : "none");
      if (description) {
        th.classList.add("metric-explained");
        th.dataset.tooltip = description;
        th.setAttribute("aria-label", text + " — " + description + ". Activate to sort.");
        const abbreviation = cell("abbr", text, "metric-help");
        abbreviation.setAttribute("aria-hidden", "true");
        th.append(abbreviation);
      } else {
        th.append(doc.createTextNode(text));
      }
      th.append(cell("span", active ? (sort.direction === "asc" ? "▲" : "▼") : "", "sort-mark"));
      const activate = () => {
        if (sort.key === key) sort.direction = sort.direction === "desc" ? "asc" : "desc";
        else sort = { key: key, direction: key === "model" || key === "training_condition" ? "asc" : "desc" };
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

    function renderTable(rows, mixedStatus) {
      const body = doc.getElementById("comparison-body");
      body.replaceChildren();
      const best = bestValues(rows, metrics);
      const ordered = sortRows(rows, sort, data);
      const grouped = !sort.key;
      let previousModel = null;

      for (const row of ordered) {
        const tr = doc.createElement("tr");
        tr.className = "row-select";
        if (grouped && row.model !== previousModel) tr.classList.add("group-start");
        previousModel = row.model;
        if (runId(row) === openRun) tr.classList.add("is-open");
        tr.tabIndex = 0;
        tr.setAttribute("aria-expanded", String(runId(row) === openRun));

        const modelCell = cell("td", null, "model");
        modelCell.append(cell("span", "↳", "marker"));
        modelCell.append(doc.createTextNode(label("model", row.model)));
        tr.appendChild(modelCell);

        const trainingText = label("training_condition", row.training_condition) +
          (mixedStatus && row.result_status === "success" && !isAuthoritative(row) ? " †" : "");
        tr.appendChild(cell("td", trainingText, "train"));

        const reason = unavailableReason(row);
        if (reason) {
          const td = cell("td", reason, "no-data-cell");
          td.colSpan = metrics.length;
          tr.appendChild(td);
          tr.classList.add("no-data");
        } else {
          for (const group of groups) {
            group.metrics.forEach((metric, index) => {
              const value = metricValue(row, metric, "f1");
              let className = "num" + (index === 0 ? " grp-start" : "");
              if (best[metric] != null && value === best[metric]) className += " best";
              tr.appendChild(cell("td", formatScore(value), className));
            });
          }
        }

        const toggle = () => {
          openRun = openRun === runId(row) ? "" : runId(row);
          render();
        };
        tr.addEventListener("click", toggle);
        tr.addEventListener("keydown", event => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            toggle();
          }
        });
        body.appendChild(tr);
      }

      /* Sticky headers only once the table is long enough to scroll behind them.
         The second header row must sit exactly below the first, so its offset is
         measured rather than guessed. */
      const wrap = doc.getElementById("table-wrap");
      const tall = ordered.length > 14;
      wrap.classList.toggle("tall", tall);
      if (tall) {
        const groupRow = doc.querySelector("#comparison-head tr.groups");
        const height = groupRow && groupRow.getBoundingClientRect ? groupRow.getBoundingClientRect().height : 0;
        if (height) wrap.style.setProperty("--group-h", Math.round(height) + "px");
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
          " The scores are reproducible evaluator output over the prediction and gold files named below, " +
          "but the gold release has not been confirmed for this benchmark. Not citable as benchmark results."
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

    function renderDetail(rows) {
      const section = doc.getElementById("detail");
      const row = rows.find(candidate => runId(candidate) === openRun) || null;
      if (!row) {
        section.hidden = true;
        return;
      }
      section.hidden = false;

      const heading = doc.getElementById("detail-heading");
      heading.replaceChildren();
      heading.append(doc.createTextNode(label("model", row.model) + " · " +
        label("training_condition", row.training_condition) + " training"));
      heading.append(cell("span", " — " + contextDescription(state) + " test", "qualifier"));

      const fieldsPresent = new Set((data.metrics || []).flatMap(metric => metric.fields));
      const fields = SCORE_FIELDS.concat(COUNT_FIELDS).filter(field => fieldsPresent.has(field));

      const head = doc.getElementById("metrics-head");
      head.replaceChildren();
      const headRow = doc.createElement("tr");
      headRow.appendChild(cell("th", "Metric"));
      for (const field of fields) headRow.appendChild(cell("th", label("metric_field", field), "num"));
      head.appendChild(headRow);

      const body = doc.getElementById("metrics-body");
      body.replaceChildren();
      const reason = unavailableReason(row);
      if (reason) {
        const tr = doc.createElement("tr");
        tr.className = "no-data";
        const td = cell("td", reason);
        td.colSpan = fields.length + 1;
        tr.appendChild(td);
        body.appendChild(tr);
      } else {
        const layerOf = name => METRIC_LAYERS.findIndex(layer => layer.includes(name));
        let previousLayer = null;
        for (const definition of data.metrics) {
          const tr = doc.createElement("tr");
          const layer = layerOf(definition.name);
          if (previousLayer !== null && layer !== previousLayer) tr.className = "layer-start";
          previousLayer = layer;
          tr.appendChild(cell("td", definition.name, "metric-name"));
          for (const field of fields) {
            const value = metricValue(row, definition.name, field);
            const text = COUNT_FIELDS.includes(field) ? formatCount(value) : formatScore(value);
            tr.appendChild(cell("td", text, "num"));
          }
          body.appendChild(tr);
        }
      }

      const summaryList = doc.getElementById("provenance-summary");
      const technicalList = doc.getElementById("provenance-list");
      summaryList.replaceChildren();
      technicalList.replaceChildren();
      const summaryEntries = [
        ["Gold cohort", row.gold_cohort, false],
        ["Gold status", row.gold_status, false],
        ["Repeat check", row.repeat_deterministic, false]
      ];
      const technicalEntries = [
        ["Gold file", row.gold_file, true],
        ["Gold SHA-256", row.gold_sha256, true],
        ["Prediction", row.prediction_file, true],
        ["Prediction SHA-256", row.prediction_sha256, true],
        ["Evaluator", row.evaluator_file, true],
        ["Evaluator SHA-256", row.evaluator_sha256, true]
      ];
      for (const [list, entries] of [
        [summaryList, summaryEntries],
        [technicalList, technicalEntries]
      ]) {
        for (const [term, value, mono] of entries) {
          if (!value) continue;
          list.append(cell("dt", term), cell("dd", value, mono ? "mono" : ""));
        }
      }

      const note = doc.getElementById("detail-note");
      const hasCounts = COUNT_FIELDS.some(field => fields.includes(field));
      note.textContent = hasCounts
        ? "Score fields are percentage points; count fields are raw evaluator counts."
        : "Percentage points. This result TSV carries no raw-count columns, so counts are not shown.";
    }

    function render() {
      renderContextControl("language", doc.getElementById("language-control"), "language-label");
      renderContextControl("test_condition", doc.getElementById("test-control"), "test-label");

      const rows = rowsFor(data, state);
      if (openRun && !rows.some(row => runId(row) === openRun)) openRun = "";

      doc.getElementById("table-heading").textContent =
        "Systems compared — " + contextDescription(state);
      doc.getElementById("row-count").textContent =
        rows.length + (rows.length === 1 ? " run" : " runs");

      const empty = doc.getElementById("empty");
      const wrap = doc.getElementById("table-wrap");
      const note = doc.getElementById("table-note");
      const hasRows = rows.length > 0;
      empty.hidden = hasRows;
      wrap.hidden = !hasRows;
      note.hidden = !hasRows;
      if (!hasRows) {
        empty.textContent = "No evaluated runs for this combination.";
        doc.getElementById("detail").hidden = true;
        doc.getElementById("caveat").hidden = true;
      } else {
        renderHead();
        const mixed = renderCaveat(rows);
        renderTable(rows, mixed);
        renderDetail(rows);

        const parts = ["F1 in percentage points."];
        if (Object.keys(bestValues(rows, metrics)).length) parts.push("Bold marks the highest value in a column.");
        if (mixed) parts.push("† marks a run whose gold version is unconfirmed.");
        parts.push("Select a row for the complete evaluator output.");
        note.textContent = parts.join(" ");
      }

      const request = doc.getElementById("request-note");
      request.hidden = !invalidRequest;
      request.textContent = invalidRequest
        ? "Part of the requested link was unavailable; the nearest existing result is shown."
        : "";

      doc.getElementById("source-meta").textContent =
        data.source.path + " · " + data.source.row_count + " rows · SHA-256 " + data.source.sha256;

      writeUrl();
      doc.body.dataset.uiReady = "true";
    }

    doc.getElementById("detail-close").addEventListener("click", () => {
      openRun = "";
      render();
    });

    render();
    return {
      getState: () => Object.assign({}, state),
      getOpenRun: () => openRun,
      getSort: () => Object.assign({}, sort)
    };
  }

  return {
    CONTEXT_DIMENSIONS,
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
    sortRows,
    isAuthoritative,
    unavailableReason,
    parseRequest,
    formatScore,
    start
  };
});

if (typeof window !== "undefined") {
  window.addEventListener("DOMContentLoaded", function () {
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
