# Interactive table adaptation notes

> Historical note: This planning document predates the local UI prototype.
> Current implementation status is documented in `ui_prototype_notes.md`.

## Current assumptions

The v5 interface assumes two tools and three Slovenian test corpora. Its state is
only `{model, corpus}`. The data bundle provides:

- a fixed `models` mapping and `model_order` list;
- a fixed `corpus_order` and corpus objects for SSJ, SST, and POG;
- metrics nested as `corpus.metrics[model]`;
- corpus/model-specific provenance, accuracy rows, error rows, and examples.

The HTML loads `comparison_table_v5_data.js` into
`window.TABLE_DATA_V5`. JavaScript builds the Tool and Test set controls, reads
the selected corpus/model block, and renders five overview metrics: Lemmas,
UPOS, XPOS, UAS, and LAS. URL state is encoded as `#model/corpus`.

## Hard-coded areas

- Model keys, labels, order, and the assumption that the other model is the only
  comparison target.
- SSJ/SST/POG definitions, old run IDs, file paths, and provenance HTML in the
  Python builder.
- A Slovenian-only corpus vocabulary and MULTEXT-East/JOS description for XPOS.
- Selector labels and URL routing limited to model/corpus.
- Corpus-level metric nesting, which cannot distinguish training conditions.
- Static model/corpus combinations rather than manifest-derived availability.

## Minimum future change

The new evaluation TSV can replace the hard-coded combination matrix for run
selection and overview metrics. A small data adapter should:

1. read successful, permitted result rows;
2. build dictionaries for labels and provenance separately from numeric rows;
3. expose only combinations present in the result data;
4. map the five existing cards to `Lemmas_f1`, `UPOS_f1`, `XPOS_f1`, `UAS_f1`,
   and `LAS_f1`;
5. carry gold status and provisional notices into the page state;
6. add richer error/accuracy blocks only when those artifacts have been built.

The technically simplest selector hierarchy is:

~~~text
language -> model -> training condition -> test condition
~~~

Each control should be populated from rows matching the choices already made.
This avoids invalid cross-product combinations and produces one logical run at
the final selection. The URL state can use the same four keys. A comparison view
should select two complete run keys rather than assume exactly two globally
fixed models.

## What can proceed before gold confirmation

The data adapter, selector generation, URL routing, empty/error states, metric
formatting, provisional banner, and generic table interactions can all be built
and tested from manifests plus isolated SL fixture results. Existing sorting,
filtering, CSV/Markdown export, examples-panel, and deep-link code can largely
be retained.

Official EN/NL options, official SL scores, complete comparisons, and published
provenance text must wait for authoritative gold mapping. Language-specific
explanatory copy, especially XPOS terminology, should be selected by language
rather than generalized from Slovenian.
