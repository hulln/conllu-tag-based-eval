# data/

Input datasets used by the pipeline.

- [gold](gold/): authoritative gold CoNLL-U input for aligned evaluation. Local-only and gitignored.
- [raw](raw/): optional sentence-per-line text used only for supplementary base-mode runs.

Methodology note:

- Primary evaluation uses gold sentence segmentation and gold tokenization from [data/gold](gold/).
- The models then predict lemma, POS/morphology, and dependency annotation on top of that fixed structure.
- Base mode is optional supplementary analysis only.

Provenance note:

- SSJ source: https://github.com/UniversalDependencies/UD_Slovenian-SSJ
- Local copy obtainment date used in this project: 2026-04-10

Primary files:

- [gold/sl_ssj-ud-test.conllu](gold/sl_ssj-ud-test.conllu)
- [raw/sl_ssj-ud-test.sentences.txt](raw/sl_ssj-ud-test.sentences.txt) for optional base mode only
