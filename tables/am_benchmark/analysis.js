(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.AMBenchmarkAnalysis = api;
})(typeof window !== "undefined" ? window : null, function () {
  "use strict";

  /* Diagnostics are generated one file per run and loaded on demand, so the page
     fetches the manifest plus exactly the run it was asked for. Display names,
     URL parameter names and score formatting come from the overview module, so
     the two pages can never disagree about what "writtenandspokentrain" is called. */
  const DIAGNOSTICS_DIR = "data/diagnostics/";
  const INDEX_FILE = "index.json";
  const OVERVIEW_PAGE = "index.html";

  const RUN_FIELDS = ["language", "test_condition", "model", "training_condition"];
  const QUERY_NAMES = {
    language: "lang",
    test_condition: "test",
    model: "model",
    training_condition: "training"
  };

  /* Long confusion tables open at a readable length; nothing is hidden without
     saying how much, and the full table is one activation away. */
  const DEFAULT_ROW_LIMIT = 25;

  const SUMMARY_METRICS = [
    { name: "UPOS", description: "Universal part-of-speech" },
    { name: "XPOS", description: "Language-specific part-of-speech" },
    { name: "Lemmas", description: "Lemmatization" },
    { name: "UAS", description: "Unlabelled Attachment Score" },
    { name: "LAS", description: "Labelled Attachment Score" }
  ];

  /* Which summary counts the diagnostic set carries for which metric. */
  const SUMMARY_CORRECT = { UPOS: "upos_correct", UAS: "uas_correct", LAS: "las_correct" };

  function overview() {
    const api = typeof window !== "undefined" ? window.AMBenchmarkUI : null;
    if (!api) throw new Error("app.js must load before analysis.js.");
    return api;
  }

  function label(field, value) {
    return overview().label(field, value);
  }

  function formatScore(value) {
    return overview().formatScore(value);
  }

  function formatCount(value) {
    return value == null ? "—" : String(value);
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

  /* The manifest is the authority on what exists: a link is only honoured when a
     diagnostic file was actually generated for that combination. */
  function findRun(index, request) {
    if (!index || !Array.isArray(index.runs)) return null;
    if (!requestIsComplete(request)) return null;
    return index.runs.find(run => RUN_FIELDS.every(field => run[field] === request[field])) || null;
  }

  function contextDescription(run) {
    return [label("language", run.language), label("test_condition", run.test_condition)]
      .filter(Boolean)
      .join(" · ");
  }

  function systemDescription(run) {
    return [label("model", run.model), label("training_condition", run.training_condition)]
      .filter(Boolean)
      .join(" · ");
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

  /* One sortable table renderer for every section. Columns declare how to read a
     value out of a positional row, so the compact generated arrays never have to
     be expanded into objects. */
  function renderTable(doc, container, spec) {
    const records = spec.rows.map((row, index) => ({ row: row, index: index }));
    let sort = spec.sort ? { index: spec.sort.index, direction: spec.sort.direction } : null;
    let expanded = false;

    function compare(left, right) {
      const column = spec.columns[sort.index];
      const direction = sort.direction === "asc" ? 1 : -1;
      const a = column.value(left.row);
      const b = column.value(right.row);
      if (a == null && b == null) return left.index - right.index;
      if (a == null) return 1;
      if (b == null) return -1;
      const result = typeof a === "number" && typeof b === "number"
        ? a - b
        : String(a).localeCompare(String(b));
      return result * direction || left.index - right.index;
    }

    function header(column, index) {
      const th = cell(doc, "th", null, (column.numeric ? "num " : "") + "sortable");
      th.scope = "col";
      th.tabIndex = 0;
      th.setAttribute("role", "columnheader");
      const active = sort && sort.index === index;
      th.setAttribute(
        "aria-sort",
        active ? (sort.direction === "asc" ? "ascending" : "descending") : "none"
      );
      th.append(doc.createTextNode(column.label));
      th.append(cell(
        doc,
        "span",
        active ? (sort.direction === "asc" ? "▲" : "▼") : "",
        "sort-mark"
      ));
      const activate = () => {
        const first = column.numeric ? "desc" : "asc";
        if (!sort || sort.index !== index) sort = { index: index, direction: first };
        else sort.direction = sort.direction === "asc" ? "desc" : "asc";
        draw();
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

    function draw() {
      container.replaceChildren();
      const ordered = records.slice();
      if (sort) ordered.sort(compare);
      const limit = spec.limit == null ? DEFAULT_ROW_LIMIT : spec.limit;
      const capped = !expanded && ordered.length > limit;
      const shown = capped ? ordered.slice(0, limit) : ordered;

      const wrap = doc.createElement("div");
      /* Two to four columns, capped per width class: numbers spread across a full
         line stop being scannable against their label. */
      wrap.className = "table-wrap cols-" + spec.columns.length;
      const table = doc.createElement("table");
      table.className = "analysis-table";
      if (spec.caption) {
        const caption = cell(doc, "caption", spec.caption, "sr-only");
        table.appendChild(caption);
      }

      const head = doc.createElement("thead");
      const headRow = doc.createElement("tr");
      headRow.className = "cols";
      spec.columns.forEach((column, index) => headRow.appendChild(header(column, index)));
      head.appendChild(headRow);
      table.appendChild(head);

      const body = doc.createElement("tbody");
      for (const record of shown) {
        const tr = doc.createElement("tr");
        for (const column of spec.columns) {
          tr.appendChild(cell(doc, "td", column.text(record.row), column.numeric ? "num" : ""));
        }
        body.appendChild(tr);
      }
      table.appendChild(body);
      wrap.appendChild(table);
      container.appendChild(wrap);

      if (ordered.length > limit) {
        const button = doc.createElement("button");
        button.type = "button";
        button.className = "row-toggle";
        button.textContent = capped
          ? "Show all " + ordered.length + " rows"
          : "Show the first " + limit + " rows";
        button.addEventListener("click", () => {
          expanded = !expanded;
          draw();
        });
        container.appendChild(button);
      }
    }

    draw();
  }

  /* Column definitions. Rows are the generated positional arrays; `value` is what
     sorting compares, `text` is what the cell shows. */
  function accuracyColumns(nameLabel, percentLabel) {
    return [
      { label: nameLabel, value: row => row[0], text: row => row[0] },
      { label: "Gold", numeric: true, value: row => row[1], text: row => formatCount(row[1]) },
      { label: "Correct", numeric: true, value: row => row[2], text: row => formatCount(row[2]) },
      {
        label: percentLabel,
        numeric: true,
        value: row => percentage(row[2], row[1]),
        text: row => formatScore(percentage(row[2], row[1]))
      }
    ];
  }

  function confusionColumns(goldLabel, predictedLabel) {
    return [
      { label: goldLabel, value: row => row[0], text: row => row[0] },
      { label: predictedLabel, value: row => row[1], text: row => row[1] },
      { label: "Count", numeric: true, value: row => row[2], text: row => formatCount(row[2]) }
    ];
  }

  function singleLabelColumns(goldLabel) {
    return [
      { label: goldLabel, value: row => row[0], text: row => row[0] },
      { label: "Count", numeric: true, value: row => row[1], text: row => formatCount(row[1]) }
    ];
  }

  function renderSummary(doc, data) {
    const summary = data.summary;
    doc.getElementById("summary-count").textContent =
      summary.gold_words + " gold words · " + summary.aligned_words + " aligned";

    const head = doc.getElementById("summary-head");
    head.replaceChildren();
    const headRow = doc.createElement("tr");
    headRow.className = "cols";
    headRow.appendChild(cell(doc, "th", "Metric"));
    headRow.appendChild(cell(doc, "th", "F1", "num"));
    headRow.appendChild(cell(doc, "th", "Correct", "num"));
    head.appendChild(headRow);

    const body = doc.getElementById("summary-body");
    body.replaceChildren();
    for (const metric of SUMMARY_METRICS) {
      const value = Object.prototype.hasOwnProperty.call(summary.f1, metric.name)
        ? summary.f1[metric.name]
        : null;
      const tr = doc.createElement("tr");
      const name = cell(doc, "td", null, "metric-name");
      name.append(doc.createTextNode(metric.name));
      name.append(cell(doc, "span", metric.description, "metric-gloss"));
      tr.appendChild(name);
      tr.appendChild(cell(doc, "td", formatScore(value), "num"));
      const countField = SUMMARY_CORRECT[metric.name];
      tr.appendChild(cell(doc, "td", formatCount(countField ? summary[countField] : null), "num"));
      body.appendChild(tr);
    }

    const provenance = data.provenance || {};
    const summaryList = doc.getElementById("provenance-summary");
    const technicalList = doc.getElementById("provenance-list");
    summaryList.replaceChildren();
    technicalList.replaceChildren();
    const entries = [
      [summaryList, [
        ["Gold cohort", provenance.gold_cohort, false],
        ["Gold status", provenance.gold_status, false],
        ["Relations", String(summary.relations_attested), false],
        ["UPOS tags", String(summary.tags_attested), false]
      ]],
      [technicalList, [
        ["Gold file", provenance.gold_file, true],
        ["Gold SHA-256", provenance.gold_sha256, true],
        ["Prediction", provenance.prediction_file, true],
        ["Prediction SHA-256", provenance.prediction_sha256, true],
        ["Evaluator", provenance.evaluator_file, true],
        ["Evaluator SHA-256", provenance.evaluator_sha256, true]
      ]]
    ];
    for (const [list, rows] of entries) {
      for (const [term, value, mono] of rows) {
        if (!value) continue;
        list.append(cell(doc, "dt", term), cell(doc, "dd", value, mono ? "mono" : ""));
      }
    }

    doc.getElementById("summary-note").textContent =
      "F1 in percentage points, from the same evaluator run that produced the benchmark. " +
      "Correct counts are aligned words scored right by that metric; the evaluator reports " +
      "no such count for XPOS or lemmas at this level.";
  }

  function renderAccuracySections(doc, data) {
    const las = data.tables.las_by_relation;
    doc.getElementById("las-count").textContent =
      las.rows.length + (las.rows.length === 1 ? " relation" : " relations");
    renderTable(doc, doc.getElementById("las-table"), {
      caption: "Labelled attachment score for each dependency relation attested in the gold data.",
      columns: accuracyColumns("Relation", "LAS %"),
      rows: las.rows,
      sort: { index: 1, direction: "desc" }
    });

    const upos = data.tables.upos_accuracy;
    doc.getElementById("upos-count").textContent =
      upos.rows.length + (upos.rows.length === 1 ? " tag" : " tags");
    renderTable(doc, doc.getElementById("upos-table"), {
      caption: "Accuracy for each universal part-of-speech tag attested in the gold data.",
      columns: accuracyColumns("Tag", "Accuracy %"),
      rows: upos.rows,
      sort: { index: 1, direction: "desc" }
    });
  }

  function renderSubsection(doc, container, heading, meta, spec) {
    const block = doc.createElement("div");
    /* The heading carries the category totals, so it is capped to the same measure
       as its table and the two read as one block. */
    block.className = "subsection cols-" + spec.columns.length;
    const head = doc.createElement("div");
    head.className = "subsection-head";
    head.appendChild(cell(doc, "h3", heading));
    head.appendChild(cell(doc, "span", meta, "count"));
    block.appendChild(head);
    const target = doc.createElement("div");
    block.appendChild(target);
    container.appendChild(block);
    renderTable(doc, target, spec);
  }

  function renderDependencyErrors(doc, data) {
    const categories = data.tables.dependency_errors.categories;
    const total = categories.reduce((sum, category) => sum + category.total, 0);
    doc.getElementById("dep-count").textContent =
      total + (total === 1 ? " error" : " errors");

    const container = doc.getElementById("dep-tables");
    container.replaceChildren();
    for (const category of categories) {
      const paired = category.columns.length === 3;
      const meta = category.total + " errors · " + category.rows.length +
        (paired ? " relation pairs" : " relations");
      renderSubsection(doc, container, category.label, meta, {
        caption: category.label + " — aggregate counts.",
        columns: paired
          ? confusionColumns("Gold relation", "Predicted relation")
          : singleLabelColumns("Gold relation"),
        rows: category.rows,
        sort: { index: paired ? 2 : 1, direction: "desc" }
      });
    }
  }

  function renderTagErrors(doc, data) {
    const tags = data.tables.tag_errors;
    const container = doc.getElementById("tag-tables");
    container.replaceChildren();

    const layers = [
      ["upos", "Universal part-of-speech confusions", "Gold UPOS", "Predicted UPOS"],
      ["xpos", "Language-specific part-of-speech confusions", "Gold XPOS", "Predicted XPOS"]
    ];
    let total = 0;
    for (const [key, heading, goldLabel, predictedLabel] of layers) {
      const layer = tags[key];
      if (!layer) continue;
      total += layer.total;
      renderSubsection(
        doc,
        container,
        heading,
        layer.total + " errors · " + layer.rows.length + " pairs",
        {
          caption: heading + " — aggregate counts.",
          columns: confusionColumns(goldLabel, predictedLabel),
          rows: layer.rows,
          sort: { index: 2, direction: "desc" }
        }
      );
    }

    if (tags.lemma) {
      total += tags.lemma.total;
      const block = doc.createElement("div");
      block.className = "subsection cols-3";
      const head = doc.createElement("div");
      head.className = "subsection-head";
      head.appendChild(cell(doc, "h3", "Lemmatization"));
      head.appendChild(cell(doc, "span", tags.lemma.total + " errors", "count"));
      block.appendChild(head);
      block.appendChild(cell(doc, "p", tags.lemma.note, "table-note"));
      container.appendChild(block);
    }

    doc.getElementById("tag-count").textContent = total + (total === 1 ? " error" : " errors");
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
      /* A page opened over file:// cannot fetch its own data directory. That is an
         environment limitation, not a missing result, and it is stated as such. */
      const isFile = String(browserWindow.location.protocol) === "file:";
      showNotice(
        doc,
        isFile
          ? "This page was opened from the file system, so the browser refused to load the " +
            "diagnostic set. Serve the directory over HTTP (python3 -m http.server) and reopen it."
          : "The diagnostic set could not be loaded (" + error.message + "). Regenerate it with " +
            "am_benchmark/scripts/build_diagnostics_data.py."
      );
      doc.body.dataset.uiReady = "error";
      return null;
    }

    const run = findRun(index, request);
    if (!run) {
      showNotice(
        doc,
        requestIsComplete(request)
          ? "No diagnostics exist for that combination of language, test data, system and " +
            "training condition. The runs below are available."
          : "This page analyses one benchmark run, named by the link that opened it. Choose one below."
      );
      renderRunChoices(doc, index);
      doc.getElementById("back-link").href = OVERVIEW_PAGE;
      doc.getElementById("run-identity").hidden = false;
      /* The masthead already names the page, so the identity bar carries only the
         missing-selection state and the route back. */
      doc.getElementById("run-context").textContent = "";
      doc.getElementById("run-system").textContent = "No run selected";
      doc.body.dataset.uiReady = "no-run";
      return null;
    }

    let data;
    try {
      data = await loadJson(browserWindow, DIAGNOSTICS_DIR + run.file);
    } catch (error) {
      showNotice(doc, "The diagnostics file for this run could not be loaded (" + error.message + ").");
      doc.body.dataset.uiReady = "error";
      return null;
    }

    doc.title = systemDescription(run) + " — " + contextDescription(run) + " — detailed analysis";
    doc.getElementById("run-context").textContent = contextDescription(run);
    doc.getElementById("run-system").textContent = systemDescription(run);
    doc.getElementById("back-link").href = overviewUrl(run);
    doc.getElementById("run-identity").hidden = false;

    renderSummary(doc, data);
    renderAccuracySections(doc, data);
    renderDependencyErrors(doc, data);
    renderTagErrors(doc, data);

    doc.getElementById("source-meta").textContent =
      DIAGNOSTICS_DIR + run.file + " · " + data.generator + " · " + data.content_policy;
    doc.getElementById("analysis").hidden = false;
    doc.body.dataset.uiReady = "true";
    return { run: run, data: data };
  }

  return {
    RUN_FIELDS,
    QUERY_NAMES,
    DEFAULT_ROW_LIMIT,
    runKey,
    requestIsComplete,
    findRun,
    percentage,
    overviewUrl,
    analysisUrl,
    renderTable,
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
