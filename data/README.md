# data/

Input datasets used by the pipeline.

- [gold](gold/): authoritative gold CoNLL-U input for aligned evaluation. Local-only and gitignored.
- [raw](raw/): optional sentence-per-line text used only for supplementary base-mode runs.

Methodology note:

- Primary evaluation uses gold sentence segmentation and gold tokenization from [data/gold](gold/).
- The models then predict lemma, POS/morphology, and dependency annotation on top of that fixed structure.
- Base mode is optional supplementary analysis only.

## Datasets

### SSJ-UD (written Slovenian)

- Source: https://github.com/UniversalDependencies/UD_Slovenian-SSJ
- Version: v2.17 (2025-10-22)
- Local copy obtained: 2026-04-10
- Primary file: [gold/sl_ssj-ud-test.conllu](gold/sl_ssj-ud-test.conllu) (local only)

### SST-UD (spoken Slovenian)

- Source: https://github.com/UniversalDependencies/UD_Slovenian-SST
- Version: v2.16 (2024-12-20)
- Local copy obtained: 2026-04-20
- Primary file: [gold/sl_sst-ud-test.conllu](gold/sl_sst-ud-test.conllu) (local only)
