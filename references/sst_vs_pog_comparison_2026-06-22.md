# SST (normalised) vs. SST-pog (colloquial): test-set comparison

_Prepared 2026-06-22. Compares the two spoken test sets used in the v5 evaluation
table: `sl_sst-ud-test.conllu` (normalised transcription) and
`sl_sst-ud-test-pog.conllu` (colloquial transcription)._

## Summary

The two sets are the **same spoken material** and their token-level gold tags are
effectively identical; they differ mainly in how each word is *spelled*
(normalised vs. colloquial surface form). The score drop from SST → pog therefore
mostly measures **robustness to non-standard surface forms**. The only structural
difference is two long spoken segments that are split into sentences in the
official SST file but kept as run-on sentences in the supplied pog/stan pair.
SPOT-Trankit 1.3 degrades modestly; CLASSLA-Stanza degrades 2–3× more, because
Trankit 1.3 was trained on exactly this kind of colloquial spoken data.

## How the two sets relate

| | SST (normalised) | pog (colloquial) |
|---|---|---|
| Sentences | 432 | 420 |
| Tokens | 11,443 | 11,443 |

- **Tokens are identical in count** (11,443). The token-level annotation layers are
  effectively identical too: among the aligned sentences, **0% of tokens differ in
  UPOS or XPOS** and only 2 tokens differ in lemma.
- **Surface forms differ in 12.2%** of aligned tokens — that is the colloquial
  transcription (e.g. `imado→imajo`, `mate→imate`, `və→v`, `potrebn→potreben`,
  `vržt→vreči`).

  Example sentences (normalised → colloquial):

  | normalised | colloquial |
  |---|---|
  | …boste **mogli opraviti**, če boste to nalogo **opravili**. | …boste **mogl opravt**, če boste to nalogo **opravl**. |
  | …trije **majhni otroci** pa še **pes** ne **grejo skupaj**. | …trije **məjhni otroc** pa še **pəs** ne **grəjo skupi**. |
  | **ker** vse leto sem **bila tako** lepo zbrana… | **kr** vse leto sem **bla tak** lepo zbrana… |
- **The 432 vs. 420 sentence difference is fully explained** and benign. 418 `sent_id`s
  are shared and identically segmented. The whole gap comes from **two spoken segments**:
  - `…reseg.1933` — split into 7 sub-sentences in SST (`.1933.1`–`.1933.7`, 434 tokens
    total) but kept as **one** sentence in pog (434 tokens).
  - `…reseg.1934` — split into 7 sub-sentences in SST (379 tokens total) but **one**
    sentence in pog (379 tokens).

  That is 14 SST sentences ↔ 2 pog sentences (net −12 = 432 − 420), with **identical
  tokens** on both sides. In the official UD SST these are split at sentence-final
  periods into 7 proper sentences each; in pog/stan they are single ~400-token run-ons
  (the periods become commas), e.g. UD `…ne morem poistovetiti .` + `vem , da…` vs.
  pog/stan `…ne morem poistovetiti , vem , da…`. UD's split is arguably the more
  standard segmentation — a small point in favour of keeping the official UD SST. So it is a sentence-boundary difference for two segments only,
  not missing/extra data. It has no effect on the token-level tagging metrics
  (UPOS/XPOS/lemma); it only changes the gold dependency structure (root/boundary
  attachments) within those two segments (~813 of 11,443 tokens).
  → *This difference exists only because the normalised set is the **official UD SST**
  (which splits those two segments), while pog comes from the supplied zip. The zip also
  contains a paired **stan** (standardised) file — see below.*

## Dataset choice: official UD SST vs. the zip's `stan` file for the normalised set

The supplied zip contains both `pog` and a paired `stan` (standardised) transcription.
Comparison of the three gold files:

| file | sentences | tokens | relation to pog |
|---|---|---|---|
| `sl_sst-ud-test.conllu` (official UD SST) | 432 | 11,443 | not 1:1 — 2 segments split differently |
| `sl_sst-ud-test-stan.conllu` (zip) | 420 | 11,443 | **perfect pair** with pog |
| `sl_sst-ud-test-pog.conllu` (zip) | 420 | 11,443 | — |

- **stan ↔ pog is a perfect minimal pair:** same 420 sentences, identical tokens, and
  **only the surface spelling differs (12.3%)** — lemma, UPOS, XPOS, head and deprel are
  100% identical. Any score gap is then attributable purely to transcription style.
- **stan is effectively the official UD SST**, differing only in the segmentation of
  those two segments and 2 lemma tokens (surface forms and all tags identical).

**Options:**
1. **Keep official UD SST** as the normalised set — canonical, publicly citable, but not
   perfectly aligned with pog (the 432 vs 420 / 2-segment difference).
2. **Use `stan` for the normalised set** — makes stan/pog a controlled minimal pair
   (recommended if the goal is a direct normalised-vs-colloquial comparison); numbers are
   essentially identical to UD SST since the two files barely differ.

## Performance drop, SST → pog

| Metric | SPOT-Trankit 1.3 | CLASSLA-Stanza |
|---|---|---|
| Lemma | 98.71 → 95.84  (**−2.87**) | 99.23 → 89.38  (**−9.85**) |
| UPOS  | 98.78 → 97.88  (**−0.90**) | 98.16 → 93.25  (**−4.91**) |
| XPOS  | 97.43 → 95.58  (**−1.85**) | 96.75 → 89.66  (**−7.09**) |
| UAS   | 89.20 → 86.45  (**−2.75**) | 85.24 → 78.97  (**−6.27**) |
| LAS   | 86.86 → 83.76  (**−3.10**) | 82.08 → 73.96  (**−8.12**) |

## Where the degradation concentrates (UPOS, by gold frequency)

| Tag | n | Trankit Δ | CLASSLA Δ |
|---|---|---|---|
| X (residual/foreign) | 85 | −11.4 | −82.7 |
| PART (particles) | 569 | −1.2 | −15.4 |
| ADV | 736 | −1.8 | −10.9 |
| VERB | 996 | −1.0 | −7.0 |
| NOUN | 1687 | −0.8 | −6.5 |
| ADJ | 790 | −0.8 | −5.2 |

CLASSLA loses most on closed-class/function words and on the residual `X` class —
the items whose colloquial spelling diverges most from the lexicon it relies on.
Trankit stays robust across the board.

## Takeaway for the report

1. SST and pog are the same spoken material with identical token count and nearly
   identical token-level tags; pog uses non-standard (spoken/phonetic) spelling
   for ~12% of tokens.
2. The score gap is therefore primarily a measure of **non-standard-input
   robustness**.
3. SPOT-Trankit 1.3 is markedly more robust than CLASSLA on colloquial input — which
   is the practical argument for deploying 1.3.
4. The 432 vs. 420 sentence difference is explained (two segments split in SST,
   merged in pog; identical tokens) and does not affect the tagging comparison. The
   only optional follow-up is whether to re-split those two pog segments to match SST.
