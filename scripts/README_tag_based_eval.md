# CoNLL-U Tag-Based Evaluation Script

A CoNLL-U evaluation script for dependency parsing, adapted from the official [CoNLL 2018 UD Shared Task](https://universaldependencies.org/conll18/) evaluation script. In addition to the standard CoNLL18 metrics, it supports regex-based breakdowns for **UPOS**, **XPOS**, and **DEPREL-filtered UAS/LAS** evaluation.

## Requirements

- Python 2.7 or Python 3.2+
- No external dependencies

## Usage

```bash
python conll18_ud_eval_tag-based.py <gold_file> <system_file> [options]
```

### Arguments

| Argument | Description |
|---|---|
| `gold_file` | Path to the gold-standard CoNLL-U file |
| `system_file` | Path to the predicted CoNLL-U file |

### Options

| Flag | Description |
|---|---|
| `-v`, `--verbose` | Print all metrics (Precision, Recall, F1, Aligned Accuracy) |
| `-c`, `--counts` | Print raw counts (Correct / Gold / Predicted / Aligned) instead of Precision / Recall / F1 |
| `--upos <regex>` | Show UPOS results for tags matching the regex (e.g. `"NOUN"`, `"N.*"`) |
| `--xpos <regex>` | Show XPOS results for tags matching the regex |
| `--las <regex>` | Show LAS results for dependency relations (`DEPREL`) matching the regex (e.g. `"nsubj"`) |
| `--uas <regex>` | Show UAS results for dependency relations (`DEPREL`) matching the regex |

## Examples

### Basic (default output)

Prints only the three main CoNLL18 scores:

```bash
python conll18_ud_eval_tag-based.py gold.conllu prediction.conllu
```

**Example output:**

```text
LAS F1 Score: 94.59
MLAS Score: 89.52
BLEX Score: 90.44
```

### Verbose output

Prints the full table with all metrics:

```bash
python conll18_ud_eval_tag-based.py gold.conllu prediction.conllu --verbose
```

**Example output:**

```text
Metric     | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
AllTags    |     97.07 |     97.07 |     97.07 |     97.07
BLEX       |     90.43 |     90.45 |     90.44 |     90.45
CLAS       |     93.00 |     93.02 |     93.01 |     93.02
LAS        |     94.59 |     94.59 |     94.59 |     94.59
Lemmas     |     98.05 |     98.05 |     98.05 |     98.05
MLAS       |     89.51 |     89.53 |     89.52 |     89.53
Sentences  |    100.00 |    100.00 |    100.00 |
Tokens     |    100.00 |    100.00 |    100.00 |
UAS        |     95.79 |     95.79 |     95.79 |     95.79
UFeats     |     97.56 |     97.56 |     97.56 |     97.56
UPOS       |     98.99 |     98.99 |     98.99 |     98.99
Words      |    100.00 |    100.00 |    100.00 |
XPOS       |     97.49 |     97.49 |     97.49 |     97.49
```

### Raw counts

Prints absolute numbers (correct / gold / predicted / aligned) instead of percentages:

```bash
python conll18_ud_eval_tag-based.py gold.conllu prediction.conllu --counts
```

**Example output:**

```text
Metric     | Correct   |      Gold | Predicted | Aligned
-----------+-----------+-----------+-----------+-----------
AllTags    |     24697 |     25442 |     25442 |     25442
BLEX       |     13874 |     15339 |     15343 |     15339
CLAS       |     14269 |     15339 |     15343 |     15339
LAS        |     24066 |     25442 |     25442 |     25442
Lemmas     |     24946 |     25442 |     25442 |     25442
MLAS       |     13733 |     15339 |     15343 |     15339
Sentences  |      1282 |      1282 |      1282 |
Tokens     |     25442 |     25442 |     25442 |
UAS        |     24372 |     25442 |     25442 |     25442
UFeats     |     24822 |     25442 |     25442 |     25442
UPOS       |     25186 |     25442 |     25442 |     25442
Words      |     25442 |     25442 |     25442 |     25442
XPOS       |     24804 |     25442 |     25442 |     25442
```

### Filtered evaluation

To see UPOS accuracy for selected tags:

```bash
python conll18_ud_eval_tag-based.py gold.conllu prediction.conllu --upos "NOUN|PROPN"
```

To filter LAS by a specific dependency relation:

```bash
python conll18_ud_eval_tag-based.py gold.conllu prediction.conllu --las "nsubj"
```

## Metrics explained

| Metric | Description |
|---|---|
| **LAS** | Labelled Attachment Score — correct **HEAD + DEPREL** match |
| **UAS** | Unlabelled Attachment Score — correct **HEAD** match only |
| **CLAS** | Content-word LAS — LAS restricted to words with content dependency relations |
| **MLAS** | Morphology-aware LAS — CLAS extended with **UPOS**, **UFeats**, and selected functional-child information |
| **BLEX** | Bi-lexical dependency score — CLAS extended with **lemma** matching |
| **UPOS / XPOS** | Match of universal POS tags (**UPOS**) and language-specific POS tags (**XPOS**) on aligned words |
| **UFeats** | Match of universal morphological features (**FEATS**) on aligned words |
| **Lemmas** | Match of **LEMMA** values on aligned words |
| **AllTags** | Joint match of **UPOS + XPOS + FEATS** on aligned words |

## Notes

- The gold and system files must contain the same underlying text; otherwise evaluation fails.
- Dependency relation subtypes are ignored during evaluation.
- Multi-word tokens are supported.

## Credits

Based on the official CoNLL 2018 UD Shared Task evaluation script by Milan Straka and Martin Popel (UFAL, Charles University). Extended with tag-based filtering functionality.
