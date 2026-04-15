# Random-20 Evaluation Demo

This folder is a small, visible copy of the evaluation workflow.

It uses 20 selected sentences from `data/gold/sl_ssj-ud-test.conllu`, writes predictions into this folder, runs the official eval script, then builds the same style of diagnostics and table files.

Run from the repository root:

```bash
./conllu_eval_demo_20/run_random20_demo.sh
```

By default this extracts the same 20 sentence IDs from the already-created full-run prediction files. That avoids slow model loading and focuses on what the evaluator is doing.

Optional live predictor run:

```bash
./conllu_eval_demo_20/run_random20_demo.sh live
```

The live mode reruns CLASSLA and Trankit on only these 20 examples, but it can be slow on low memory.

Main outputs:

- `data/random20.gold.conllu`: the 20 gold examples.
- `predictions/classla_random20_aligned.conllu`: CLASSLA predictions aligned to the gold tokenization.
- `predictions/trankit_random20_aligned.conllu`: Trankit predictions aligned to the gold tokenization.
- `diagnostics/alignment_check.txt`: proof that the same examples/tokens are compared.
- `results/classla_eval.txt`: official eval output for CLASSLA.
- `results/trankit_eval.txt`: official eval output for Trankit.
- `tables/comparison_table.html`: clickable interactive comparison table for this 20-example demo.

## Manual Step-By-Step Reviewer (Subfolder-Only)

If you want to inspect each sentence one-by-one and decide which model output is better:

From repository root:

```bash
.venv/bin/python conllu_eval_demo_20/build_manual_review_ui.py
```

From inside `conllu_eval_demo_20`:

```bash
../.venv/bin/python build_manual_review_ui.py
```

This writes:

- `tables/manual_review.html`

Open that HTML in a browser. It shows each sentence with token-level Gold/CLASSLA/Trankit columns, lets you mark a decision (`Prefer Trankit`, `Prefer CLASSLA`, `Tie`, `Needs follow-up`), save notes, and exports your manual decisions as JSON.

Important: the evaluator does not guess which examples match. It reads the gold file and prediction file in order, checks that the concatenated token text matches, then aligns equivalent token spans. The demo verifier adds an easier human-readable check: same sentence IDs, same token counts, and same token forms.
