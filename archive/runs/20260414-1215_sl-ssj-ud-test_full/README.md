# 20260414-1215_sl-ssj-ud-test_full

Archived verification run.

Purpose:

- Keep a timestamped snapshot where full gold sentence metadata comments
  (`newdoc`, `newpar`, `sent_id`, `text`, `document_genre`) are preserved in
  aligned prediction files.

Relationship to canonical run:

- Canonical reporting run remains `20260409-2248_sl-ssj-ud-test_full`.
- Token-level aligned prediction rows are identical to canonical run.
- Aligned evaluation outputs are identical to canonical run.

Why archived:

- Avoid duplicate active run trees with identical aligned metrics.
- Keep active paths (`predictions/runs/`, `results/runs/`) easy to read for external readers.
