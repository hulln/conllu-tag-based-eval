#!/usr/bin/env python3
"""Sentence examples for the Dutch spoken test set, for the v2 prototype only.

``build_examples_data.py`` extracts examples only for the test sets on its
allowlist, which leaves out Dutch spoken because its source corpus and licence are
not yet confirmed. The v2 prototype shows examples for every test set, so this
wrapper runs the same generator with Dutch spoken added, and writes the six Dutch
spoken runs into the prototype's own folder. The generator, its allowlist and the
current interface's example files are unchanged.

Do not publish the files this writes until the source and licence of the Dutch
spoken test set are confirmed.
"""

from __future__ import annotations

import sys

import build_examples_data as examples

OUTPUT_DIR = "tables/am_benchmark_v2/data/examples"

# No corpus is named: the test set's source is not identified.
examples.COHORT_SOURCES["NL:spokentest"] = [
    {"corpus": "Dutch spoken test set", "section": "6196 sentences",
     "release": "", "url": "", "licence": ""},
]
examples.WITHHELD_COHORTS.clear()

if __name__ == "__main__":
    sys.argv = [sys.argv[0], "--language", "NL", "--test-condition", "spokentest",
                "--output-dir", OUTPUT_DIR] + sys.argv[1:]
    raise SystemExit(examples.main())
