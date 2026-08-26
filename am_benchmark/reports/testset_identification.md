# Test-set identification

Source-identification only. Nothing was modified: no benchmark file, manifest, evaluator
output, UI file or source datum was touched, and no model was run. Public reference files
were downloaded to session scratch space for comparison and then discarded; none was added
to the repository.

## Method

For each cohort a representative canonical `_clean` prediction file was read for metadata,
and a stable fingerprint was computed: the SHA-256 of the complete ordered sequence of
ordinary-token FORM values (one per line, multiword-token and empty-node rows excluded).
Candidates were accepted only when that whole-sequence hash reproduced exactly; the
`sent_id` sequence was checked as a second, independent key wherever the cohort carried one.

## Cohort fingerprints

| Cohort | Sentences | Ordinary tokens | MWT rows | SHA-256 of ordered FORM sequence |
|---|---:|---:|---:|---|
| EN written | 881 | 17285 | 151 | `98e3f42c333055d1ff3b75817d5ae2cd42258b193ee672ef93d4bcfc5cd7a27e` |
| EN spoken | 583 | 11112 | 260 | `9227ca64145592becad4e2b02fa03c8c0e0a521f36bd31cd258e7e4266f5cecc` |
| NL written | 2357 | 40041 | 0 | `4d43e104b33dfa007ee207479abdd7e2ed79ff3a4d7c38ae1c911654b529f4f2` |
| NL spoken | 6196 | 53069 | 0 | `c86be76a056db6fc77a19f27c6853dabbaba0a63ce2d6df9ffacbc9234e17fee` |
| NL dialect | 6196 | 53069 | 0 | `c86be76a056db6fc77a19f27c6853dabbaba0a63ce2d6df9ffacbc9234e17fee` |
| SL written | 1282 | 25442 | 0 | `0fcfd1befeef9905f0e1cb39a28d1018fd7c4f5ce50bebad261b0191531d0497` |
| SL spoken | 432 | 11443 | 0 | `433a46f2561b5dac611f4e5f47ac060bef753eff2f7c475cfada774218889233` |

NL spoken and NL dialect share one fingerprint. Every other cohort is distinct.

## Findings

| Language | Condition | Candidate dataset/treebank | Candidate release | Evidence | Full-text match? | Confidence |
|---|---|---|---|---|---|---|
| EN | written | UD_English-GUM, test split, 9 written genres | r2.16 or r2.17 (identical test text; also current master) | `newdoc id = GUM_*`, GUM `global.Entity` scheme, `meta::*` fields, `s_type`/`s_prominence`/`transition` | **EXACT** — FORM sequence and all 881 `sent_id`s | EXACT |
| EN | spoken | UD_English-GUM, test split, 6 spoken genres | r2.16 or r2.17 (identical test text; also current master) | same metadata; genres conversation, court, interview, podcast, speech, vlog | **EXACT** — FORM sequence and all 583 `sent_id`s | EXACT |
| NL | written | UD_Dutch-LassySmall test **+** UD_Dutch-Alpino test, concatenated in that order | r2.16 or r2.17 (identical test text) | `archive = nl_lassysmallenhanced-ud-test.collection` (876), `WR-P-E-I-enhanced-test.collection` (885), `nl_alpinodev-ud-test.collection` (596); `sent_id` prefixes `nl_lassysmall-ud-test-` / `nl_alpino-ud-test-` | **EXACT** — FORM sequence and all 2357 `sent_id`s | EXACT |
| NL | spoken | unidentified; GCND (Spoken Corpus of Southern Dutch Dialects) is a plausible but unverified candidate | unknown | Kloeke-style location codes (`N038p`, `Q162p`, `H081a`, `I122p`); `auto = ALUD2.17` Alpino-to-UD conversion; content is spontaneous dialect speech naming Kaatsheuvel (NL) and Gazet van Antwerpen (BE) | **No** — no public file obtainable to test | WEAK |
| NL | dialect | unidentified; same material as NL spoken | unknown | identical FORM sequence *and* identical 6196-item `sent_id` sequence to NL spoken | **No** — same as above | WEAK |
| SL | written | UD_Slovenian-SSJ test | **r2.17** (local gold file is byte-identical to r2.17; differs from r2.16) | confirms existing repository documentation | **EXACT** | EXACT |
| SL | spoken | UD_Slovenian-SST test | r2.16 or r2.17 (the file is byte-identical in both) | confirms existing repository documentation | **EXACT** | EXACT |

### EN — UD_English-GUM, partitioned by modality

GUM's test split is 30 documents, two per genre, across 15 genres. Reddit is absent because
GUM ships it separately as UD_English-GUMReddit without underlying text. The benchmark
splits that one test file by genre:

- written (9 genres, 18 docs, 881 sentences): academic, bio, essay, fiction, letter, news,
  textbook, voyage, whow
- spoken (6 genres, 12 docs, 583 sentences): conversation, court, interview, podcast,
  speech, vlog

881 + 583 = 1464 sentences and 17285 + 11112 = 28397 tokens, which are exactly the totals of
`en_gum-ud-test.conllu`. Filtering that file by genre reproduces both cohorts' FORM
sequences and `sent_id` sequences exactly.

Release sweep of `en_gum-ud-test.conllu`:

| Release | Docs | Written sents/tokens | Spoken sents/tokens | Reproduces our cohorts |
|---|---:|---|---|---|
| r2.11–r2.13 | 22 | 662 / 12987 | 434 / 6918 | no |
| r2.14–r2.15 | 26 | 780 / 15239 | 505 / 8752 | no |
| **r2.16** | 30 | 881 / 17285 | 583 / 11112 | **yes** |
| **r2.17** | 30 | 881 / 17285 | 583 / 11112 | **yes** |
| master (Aug 2026) | 30 | 881 / 17285 | 583 / 11112 | yes |

r2.16, r2.17 and master differ as whole files — annotations changed — but carry identical
test *text*. The release therefore cannot be narrowed below "r2.16 or later" from the text
alone.

### NL written — two treebanks concatenated

`nl_lassysmall-ud-test.conllu` (1761 sentences) followed by `nl_alpino-ud-test.conllu`
(596 sentences) gives 2357 sentences and 40041 tokens, matching the cohort's FORM hash
exactly. The full `sent_id` sequence also matches once the treebank prefix is restored:
ours are `nl_lassysmall-ud-test-<id>` for the first 1761 and `nl_alpino-ud-test-<id>` for
the last 596. The reverse concatenation order does not match, so the order is fixed.

Two details worth noting. The internal archive names split the LassySmall portion into
876 + 885 sentences, which is how the modern LassySmall test set is composed — LassySmall
test grew from 876 to 1761 sentences at r2.14. And the third archive is named
`nl_alpinodev-ud-test.collection`, but its 596 sentences are the Alpino **test** set, not
the 718-sentence dev set; the "dev" in that label does not reflect the content.

Release sweep of the concatenation:

| Release | LassySmall test | Alpino test | Reproduces our cohort |
|---|---:|---:|---|
| r2.11–r2.13 | 876 | 596 | no |
| r2.14–r2.15 | 1761 | 596 | no |
| **r2.16** | 1761 | 596 | **yes** |
| **r2.17** | 1761 | 596 | **yes** |

### NL spoken and NL dialect — the same material, not identified

The two cohorts are not merely similar: they share the same 6196 sentences, the same FORM
sequence, and the same 6196-item `sent_id` sequence, verified across six prediction files
from three systems. For `stanza (Def)` the two prediction files are byte-identical.

The metadata carries only `source`, `sent_id`, `text`, `auto` and a few `debug` lines, and
never names a corpus. The identifiers (`N038p_1--N038p_1_1--a1916--01--0721`,
`H081a_1--H081a_1_1--0833`) begin with what appear to be Kloeke codes, the standard
geographic reference system in Dutch dialectology; the leading letters present are I (2745),
O (1028), H (685), N (511), P (493), K (441), Q (147) and L (143). `auto = ALUD2.17` shows
Alpino-to-UD automatic conversion. The content is spontaneous dialect speech, referring to
places and papers on both sides of the border (Kaatsheuvel, Gazet van Antwerpen).

No Universal Dependencies treebank matches. UD has only `UD_Dutch-Alpino` and
`UD_Dutch-LassySmall` for Dutch; `UD_Low_Saxon-LSDC` and `UD_Frisian_Dutch-Fame` use
entirely different identifier conventions and were ruled out.

The **GCND** (*Gesproken Corpus van de zuidelijk-Nederlandse Dialecten*, Ghent/INT) fits the
circumstantial profile: dialect recordings from 768 places in Belgium, northern France and
the southern Netherlands; Kloeke codes in its metadata; POS, lemma and syntax produced with
the Alpino parser. Its full parsed corpus requires a CLARIN login, so **no exact comparison
was possible** and it is recorded as WEAK, not as an identification.

**On the special NL check.** GCND provides two transcription layers, one closer to the
dialect and one closer to Standard Dutch. That design could in principle justify two test
conditions over one set of recordings. It does not, however, explain what was supplied:
two transcription layers would produce *different* token sequences, exactly as the Slovene
SST `-pog` and `-stan` files do. Here the token sequences and the sentence identifiers are
identical. So the evidence is consistent with either (a) two gold annotation layers over one
identical token stream, or (b) the same file having been supplied for both conditions. The
prediction files alone cannot distinguish these, and this is not called a mix-up. It is a
question for AM/KD.

## Dataset identity, split, release, and provenance

These are four separate claims and only the first three were tested here.

- **Dataset/treebank identity** — established exactly for EN, NL written, and both SL cohorts.
- **Exact split** — established for all four: the full official test split in each case, with
  EN additionally partitioned by genre and NL written additionally concatenated from two
  treebanks.
- **Exact release** — narrowed to r2.16/r2.17 for EN and NL written, which share identical
  test text and cannot be separated on text alone. For SL it is pinned by byte hash:
  `data/gold/sl_ssj-ud-test.conllu` is byte-identical to UD_Slovenian-SSJ **r2.17** (and
  differs from r2.16), and `data/gold/sl_sst-ud-test.conllu` is byte-identical to
  UD_Slovenian-SST at r2.16 and r2.17, which ship the same file.
- **Authoritative benchmark provenance** — *not established, and not establishable here.*
  Identifying the public source of the text does not confirm which release AM/KD intend as
  authoritative for this benchmark, nor which genre partition or concatenation order they
  consider canonical. That still requires their written confirmation.

## Reference files used

Downloaded to scratch space for comparison, then discarded. All are public
(CC BY-SA / CC BY-NC-SA) UD releases from `github.com/UniversalDependencies`:

- `UD_English-GUM` `en_gum-ud-test.conllu` at tags r2.11–r2.17 and master
- `UD_Dutch-LassySmall` `nl_lassysmall-ud-test.conllu` at tags r2.11–r2.17
- `UD_Dutch-Alpino` `nl_alpino-ud-test.conllu` at tags r2.11–r2.17
- `UD_Slovenian-SSJ` `sl_ssj-ud-test.conllu` and `UD_Slovenian-SST` `sl_sst-ud-test.conllu`
  at r2.16 and r2.17
