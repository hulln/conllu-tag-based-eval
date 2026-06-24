# v5 QA audit - 2026-06-22

Scope: `tables/comparison_table_v5.html`, `tables/comparison_table_v5_sl.html`,
`tables/comparison_table_v5_data.js`,
`scripts/build_interactive_comparison_table_v5.py`, and the three v5 run
artifacts with run stamp `20260622-0810-tk13`.

## Scope coverage

- Page title and subtitle match the project scope.
- Visible selectors use `Tool` and `Test set`.
- Details are collapsed by default and show selected tool, test set, size, and
  evaluation setup.
- Overall metric cards use metric descriptions rather than repeating the tool
  name.
- Required table titles, notes, `Gold count`, `Error count`, and `Error pair`
  labels are present.
- Acknowledgement, recommended citation, copyable BibTeX, and ARIS/CJVT/CLARIN.SI
  logos are present.
- Website-facing copy uses UK spelling for checked terms: `standardised`,
  `lemmatisation`, `Unlabelled`, `Labelled`, and
  `Acknowledgement`.

## Gold files and provenance

| Test set | File | Sentences | Tokens | Verification |
|---|---:|---:|---:|---|
| SSJ written | `data/gold/sl_ssj-ud-test.conllu` | 1,282 | 25,442 | Exact SHA-256 match to UD Slovenian SSJ `r2.17` |
| SST standardised | `data/gold/sl_sst-ud-test.conllu` | 432 | 11,443 | Exact SHA-256 match to UD Slovenian SST `r2.16` and `r2.17` |
| SST colloquial | `data/gold/sl_sst-ud-test-pog.conllu` | 420 | 11,443 | Exact SHA-256 match to `pog/sl_sst-ud-test-pog.conllu` inside supplied `sst2.15-dev3-pog.zip` |

Relevant hashes:

- `sl_ssj-ud-test.conllu`: `c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0`
- `sl_sst-ud-test.conllu`: `6824234edf98cbbedb2e981644c324a3058c2920ed6cdcd7f467e835cfe25eeb`
- `sl_sst-ud-test-stan.conllu`: `cc6d8d67ad5de54802450047d5d3b3363711a9f4c8591cfdc126cebe37a612ad`
- `sl_sst-ud-test-pog.conllu`: `898fdadbde212991f9e93388fa6e2aae4fbf65fa18a103539066c329b7c0d756`
- `sst2.15-dev3-pog.zip`: `d40e34feac76ed023e3615d87f38174ad3e1ca990b4eeeb246fd09fdf42258bd`

## Model and run checks

All v5 table entries use run stamp `20260622-0810-tk13`.

| Test set | Run ID | Trankit | CLASSLA |
|---|---|---|---|
| SSJ written | `20260622-0810-tk13_sl-ssj-ud-test_full` | SPOT-Trankit 1.3 | `classla.Pipeline('sl', pos_use_lexicon=True)` |
| SST standardised | `20260622-0810-tk13_sl-sst-ud-test_full` | SPOT-Trankit 1.3 | `classla.Pipeline('sl', type='spoken')` |
| SST colloquial | `20260622-0810-tk13_sl-sst-ud-test-pog_full` | SPOT-Trankit 1.3 | `classla.Pipeline('sl', type='spoken')` |

For all six prediction files, sentence count, token count, and `sent_id`
sequence match the selected gold file. Re-run `qa_validate_run.py` reports
`PASS` for all three v5 runs.

## Metrics checked against eval summaries

| Test set | Tool | LAS | UAS | UPOS | XPOS | Lemma |
|---|---|---:|---:|---:|---:|---:|
| SSJ written | SPOT-Trankit | 94.48 | 95.72 | 98.99 | 97.43 | 97.95 |
| SSJ written | CLASSLA-Stanza | 90.48 | 92.12 | 98.60 | 97.08 | 98.94 |
| SST standardised | SPOT-Trankit | 86.86 | 89.20 | 98.78 | 97.43 | 98.71 |
| SST standardised | CLASSLA-Stanza | 82.08 | 85.24 | 98.16 | 96.75 | 99.23 |
| SST colloquial | SPOT-Trankit | 83.76 | 86.45 | 97.88 | 95.58 | 95.84 |
| SST colloquial | CLASSLA-Stanza | 73.96 | 78.97 | 93.25 | 89.66 | 89.38 |

`tables/comparison_table_v5_data.js` is reproducible from
`scripts/build_interactive_comparison_table_v5.py`.

## SST standardised/pog pairing note

The supplied zip contains a paired `stan`/`pog` test set. The local `stan` and
`pog` files have the same 420 sentence IDs, the same 11,443 tokens, and no
structural differences except surface forms/text. The current v5 table uses the
official UD SST standardised test file for the standardised row instead. That file
has the same 11,443 tokens but 432 sentence blocks.

This is accurate as documented. If the intended comparison is strictly paired
standardised-vs-colloquial transcription from the supplied zip, v5 needs an
additional evaluation run for `data/gold/sl_sst-ud-test-stan.conllu` before the
table is released.

## Technical checks run

- HTML parsed successfully with Python `html.parser`.
- Inline JavaScript parsed successfully with Node `new Function(...)`.
- `node --check tables/comparison_table_v5_data.js` passed.
- Rebuilding v5 data to `/tmp/comparison_table_v5_data.check.js` produced an
  exact byte match to `tables/comparison_table_v5_data.js`.
- Local logo files referenced by the page exist and are non-empty; source URLs
  are documented in [tables/logos/README.md](../tables/logos/README.md).
- Key links checked on 2026-06-22: SPOT English page HTTP 200, LLM4DH English
  page HTTP 200, MAPCASE current page HTTP 200 with Slovenian content language.
  Tested likely MAPCASE English variants returned 404.
