# Cross-check against KD's written-test table

Independent verification of the stored SL written results against a reference table
supplied by KD. No evaluator output was modified and no model was rerun.

## Reference

- Image: `am_benchmark/source/performance-written-kd-sent.png` (read in place; not
  copied or moved)
- SHA-256: `764a8a8f9a402ab7dcfcebaa5bf1baae2d4af6476e0bad27bf41075fc66e98e8`
- Caption: *"Table 3: Written test set: parser performance by language, system, and
  training data (sorted by LAS within each language). Between brackets we indicate
  default (Def) or whether the system was trained on written data only (W) or both
  written and spoken data (W+S). Row shading indicates language: Dutch in blue,
  followed by English in orange, Slovene in reddish-purple."*

The Slovene block is therefore the third (reddish-purple) block. Two independent
confirmations: it is the only block containing `UDpipessj` and `UDpipesst` — the SSJ
and SST Slovene treebanks — and its LAS values coincide with the SL results.

Compared against `am_benchmark/reports/smoke_test/sl_spacy_stanza_results.tsv`
(rows with `language=SL`, `test_condition=writtentest`). The generated UI bundle
`ui/data/results.js` was confirmed to carry byte-identical values for these rows.

## Comparison

KD's table prints one decimal; stored values are rounded to one decimal for
comparison. `Feats` is compared against the evaluator's `AllTags` (see below).
For every row `Tokens = Sentences = Words = 100.00`, so precision, recall, F1 and
aligned accuracy are identical and the choice of score field does not affect any
comparison.

Format is `KD / ours`.

| System | UPOS | XPOS | Feats | Lem | LAS |
|---|---|---|---|---|---|
| stanza (Def) | 99.0 / 99.0 | 98.0 / 98.0 | 97.8 / 97.8 | 97.9 / 97.9 | 95.0 / 95.0 |
| spacy (W) | 98.9 / 98.9 | 97.3 / 97.3 | 24.5 / 24.5 | 97.8 / 97.8 | 93.4 / 93.4 |
| spacy (W+S) | 98.8 / 98.8 | 97.2 / 97.2 | 24.5 / 24.5 | 97.9 / 97.9 | 93.4 / 93.4 |
| stanza (W) | 98.2 / 98.2 | 95.1 / 95.1 | 94.5 / 94.5 | 97.6 / 97.6 | 89.9 / 89.9 |
| stanza (W+S) | 98.1 / 98.1 | 95.1 / 95.1 | 94.5 / 94.5 | 97.8 / 97.8 | 89.5 / 89.5 |
| spacy (Def) | 99.2 / 99.2 | 97.6 / 97.6 | 97.4 / 97.4 | 96.2 / 96.2 | 88.1 / 88.1 |

**Exact matches: 30 / 30. Mismatches: 0.**

No compared value is a rounding-boundary case: half-up and half-even rounding give
the same one-decimal result for all 30, so the agreement does not depend on which
convention KD used.

Full-precision stored values behind the table:

| System | UPOS | XPOS | AllTags | UFeats | Lemmas | LAS |
|---|---|---|---|---|---|---|
| stanza (Def) | 99.0252 | 98.0112 | 97.7596 | 98.1566 | 97.8893 | 95.0436 |
| spacy (W) | 98.8759 | 97.2997 | 24.5342 | 24.6679 | 97.8382 | 93.4007 |
| spacy (W+S) | 98.8012 | 97.2447 | 24.4556 | 24.6679 | 97.8579 | 93.3810 |
| stanza (W) | 98.1723 | 95.1380 | 94.5287 | 95.5114 | 97.6299 | 89.8868 |
| stanza (W+S) | 98.0505 | 95.1104 | 94.4619 | 95.3581 | 97.7793 | 89.5095 |
| spacy (Def) | 99.1589 | 97.6220 | 97.4177 | 97.8068 | 96.2424 | 88.0552 |

Coverage: KD's Slovene block has 11 rows. These 6 are our stable spaCy/Stanza subset.
Of the remaining 5, two (`Our (W)`, `Our (W+S)`) are KD's own system, for which we hold
no predictions; three (`trankit (W+S)`, `UDpipessj (Def)`, `UDpipesst (Def)`) correspond
to runs in our manifest marked `DEFER / RESULT MAY CHANGE`. Those three were checked
separately afterwards — see the addendum at the end of this file.

## The "Feats" column is AllTags, not UFeats

Determined numerically, not from the label.

| System | KD Feats | our UFeats → 1 dp | our AllTags → 1 dp |
|---|---|---|---|
| stanza (Def) | 97.8 | 98.1566 → 98.2 | 97.7596 → **97.8** |
| spacy (W) | 24.5 | 24.6679 → 24.7 | 24.5342 → **24.5** |
| spacy (W+S) | 24.5 | 24.6679 → 24.7 | 24.4556 → **24.5** |
| stanza (W) | 94.5 | 95.5114 → 95.5 | 94.5287 → **94.5** |
| stanza (W+S) | 94.5 | 95.3581 → 95.4 | 94.4619 → **94.5** |
| spacy (Def) | 97.4 | 97.8068 → 97.8 | 97.4177 → **97.4** |

**UFeats: 0/6. AllTags: 6/6.**

Two rows make this decisive rather than coincidental:

- `stanza (W)` and `stanza (W+S)`: UFeats and AllTags are a full point apart
  (95.5 vs 94.5, 95.4 vs 94.5). KD prints 94.5 in both.
- `spacy (W)` and `spacy (W+S)`: UFeats is *identical* for the two runs (24.6679),
  so UFeats cannot distinguish them and would print 24.7 twice. AllTags differs
  (24.5342, 24.4556) and rounds to 24.5 twice, which is what KD prints.

KD's "Feats" therefore corresponds to the evaluator's **AllTags** — correct UPOS,
XPOS *and* FEATS jointly — not to universal features alone. Worth confirming with
KD whether the column label is shorthand or whether UFeats was intended, since the
two differ by up to a full point here. This affects the reading of their table, not
our stored values.

The very low retrained-spaCy feature scores (24.5) appear in KD's own table at the
same magnitude. They are a property of the supplied spaCy predictions, independently
corroborated, not an artifact of our resolution or evaluation. This also explains the
low MLAS (5.04 / 5.07) visible for the same runs, since MLAS requires FEATS to match.

## What this establishes

- **Prediction selection is correct** for these six runs. Thirty independent values
  reproduce exactly; a wrong file would not.
- **Training-condition parsing is correct.** Def / W / W+S are not merely
  self-consistent but discriminated: swapping `spacy (W)` with `spacy (W+S)` would
  contradict KD on UPOS (98.9 vs 98.8) and XPOS (97.3 vs 97.2), and swapping the
  stanza pair would contradict UPOS, Lemmas and LAS.
- **Evaluator and output semantics agree with KD's**, once "Feats" is read as AllTags.
- **`data/gold/sl_ssj-ud-test.conllu` behaves as the corresponding written test set.**
  Thirty values across six systems cannot be reproduced against different test data.

## What this does not establish

- **Not gold provenance, version or authority.** The agreement shows our gold has the
  same content as whatever KD scored against. It does not document which UD release
  that is, nor that it is the file AM/KD consider authoritative. If KD used the same
  unconfirmed file, the agreement is circular with respect to provenance. Written
  confirmation is still required and the results stay provisional.
- **Nothing about EN or NL.** Those blocks exist in the image, but we hold no EN/NL
  gold and produced no EN/NL results, so nothing was compared.
- **Nothing about the spoken or dialect conditions.** This is the written-test table
  only; the SL spoken gold candidate `sl_sst-ud-test.conllu` is untested here.
- **Nothing, in this section, about the deferred families** (trankit, UDpipe, diaparser,
  singletask*). The addendum extends the check to trankit and the two UDpipe runs;
  diaparser and the singletask* families remain uncompared, as KD's table has no rows
  for them.
- Agreement is at one decimal, so differences below roughly ±0.05 are undetectable.

## Conclusion

All 30 comparable values for the six stable SL written spaCy/Stanza runs reproduce
KD's table exactly after rounding, independent of rounding convention. KD's "Feats"
column is the evaluator's AllTags. No mismatch was found, and no problem was
identified in prediction selection, training-condition mapping, or evaluator
integration. Gold provenance remains the open item and is unaffected by this check.

---

## Addendum: the three deferred SL written runs

Bounded follow-up. The three remaining rows of KD's Slovene block for which we hold
predictions were evaluated against the same provisional `data/gold/sl_ssj-ud-test.conllu`,
using the existing evaluator and the existing `_clean` prediction files. No model was
run. These runs keep their `DEFER / RESULT MAY CHANGE` status, were not added to the
manifests or the draft interface, and their output is kept separately in
`reports/smoke_test/sl_deferred_crosscheck.tsv` (non-canonical, gitignored).

Reproduce with:

~~~text
python3 scripts/run_benchmark_evaluation.py --execute --smoke-test --language SL \
  --test-condition writtentest --model trankit --model UDpipessj --model UDpipesst \
  --repeat-check --output reports/smoke_test/sl_deferred_crosscheck.tsv
~~~

Format is `KD / ours`, `Feats` compared against `AllTags`.

| System | UPOS | XPOS | Feats | Lem | LAS |
|---|---|---|---|---|---|
| trankit (W+S) | 99.1 / 99.1 | 98.2 / 98.2 | 97.8 / 97.8 | 97.9 / 97.9 | 95.0 / 95.0 |
| UDpipessj (Def) | 98.9 / 98.9 | 97.1 / 97.1 | 96.7 / 96.7 | 98.7 / 98.7 | 93.1 / 93.1 |
| UDpipesst (Def) | 98.8 / 98.8 | 97.0 / 97.0 | 96.5 / 96.5 | 98.7 / 98.7 | 92.8 / 92.8 |

**Exact matches: 15 / 15. Mismatches: 0.** All three evaluated successfully and returned
identical numeric output on a second execution. No value is a rounding-boundary case.

Cumulative across both passes: **45 / 45** over nine of KD's eleven Slovene rows. The two
not covered (`Our (W)`, `Our (W+S)`) are KD's own system, for which we hold no predictions.

The `Feats` = `AllTags` identification holds again: **AllTags 3/3, UFeats 0/3**
(trankit 97.7832 vs 98.2313; UDpipessj 96.6551 vs 97.1582; UDpipesst 96.5333 vs 97.0954).
Across both passes the count is AllTags 9/9, UFeats 0/9.

Full precision:

| System | UPOS | XPOS | AllTags | Lemmas | LAS |
|---|---|---|---|---|---|
| trankit (W+S) | 99.1392 | 98.2116 | 97.7832 | 97.8539 | 95.0436 |
| UDpipessj (Def) | 98.9073 | 97.0993 | 96.6551 | 98.7344 | 93.1020 |
| UDpipesst (Def) | 98.8405 | 96.9578 | 96.5333 | 98.6676 | 92.8386 |

### Run-identity parsing

This pass exercised the one filename shape nothing else tested: `UDpipessj` and
`UDpipesst` embed a treebank name (SSJ, SST) inside the model identifier, and differ
only in their final characters. Both parsed correctly, were kept distinct, and matched
KD's distinct values (LAS 93.1 vs 92.8); a confusion between them would have shown up.
`trankit` was likewise not conflated with the `trankit_1epochs` / `trankit_2epochs` /
`trankit_50epochs` families.

### Note on the LAS tie

`trankit (W+S)` and `stanza (Def)` return byte-identical LAS (95.04362864554673) — both
score exactly 24181 correct labelled arcs out of 25442 words. This is a genuine tie, not
a duplicated file: the two prediction files differ in size and SHA-256, and every other
metric differs (UPOS 99.1392 vs 99.0252, BLEX 90.4355 vs 90.5777). KD's table shows the
same tie, printing 95.0 for both and bolding both.

### Effect on the conclusions

No new concern. The validation now covers four system families rather than two, and the
additional agreement further supports prediction selection, training-condition and model
parsing, evaluator semantics, and `sl_ssj-ud-test.conllu` as the corresponding written
test set. It does not change the gold-provenance position: the release and authority of
that file are still undocumented and still require confirmation from AM/KD.
