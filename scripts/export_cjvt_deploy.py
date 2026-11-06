#!/usr/bin/env python3
"""Copy the published pages into the CJVT deploy repository (webapps/oznacevalnik-eval).

    python3 scripts/export_cjvt_deploy.py ../oznacevalnik-eval

CJVT's nginx serves that repository's folder at both
https://orodja.cjvt.si/oznacevalnik/eval/en/ and .../sl/, so the files there
have version-neutral names and a new table version only needs a pull:

    en.html, sl.html    the EN and SL pages (index files of /en/ and /sl/)
    data.js             the shared data bundle
    favicon*, logos/    as in tables/

The EN/SL switch links to ../en/ and ../sl/.
"""
import shutil
import sys
from pathlib import Path

TABLES = Path(__file__).resolve().parent.parent / "tables"
VERSION = "v6"
LOGOS = ("aris.svg", "cjvt.png", "clarin-si.png")

PAGES = {
    "en.html": (f"comparison_table_{VERSION}.html", [
        (f'<a href="comparison_table_{VERSION}_sl.html" hreflang="sl">SL</a>', '<a href="../sl/" hreflang="sl">SL</a>'),
        (f'<a href="comparison_table_{VERSION}.html" aria-current="page">EN</a>', '<a href="../en/" aria-current="page">EN</a>'),
    ]),
    "sl.html": (f"comparison_table_{VERSION}_sl.html", [
        (f'<a href="comparison_table_{VERSION}_sl.html" aria-current="page">SL</a>', '<a href="../sl/" aria-current="page">SL</a>'),
        (f'<a href="comparison_table_{VERSION}.html" hreflang="en">EN</a>', '<a href="../en/" hreflang="en">EN</a>'),
    ]),
}
DATA_SCRIPT = (f'<script src="comparison_table_{VERSION}_data.js"></script>', '<script src="data.js"></script>')


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    out = Path(sys.argv[1])
    if not (out / ".git").is_dir():
        raise SystemExit(f"{out} is not a git checkout of the deploy repository")

    for dst, (src, edits) in PAGES.items():
        s = (TABLES / src).read_text(encoding="utf-8")
        for old, new in edits + [DATA_SCRIPT]:
            if s.count(old) != 1:
                raise SystemExit(f"{src}: expected 1 match, found {s.count(old)}: {old!r}")
            s = s.replace(old, new)
        if "comparison_table_" in s:
            raise SystemExit(f"{dst}: still refers to a comparison_table_ file")
        (out / dst).write_text(s, encoding="utf-8")

    shutil.copyfile(TABLES / f"comparison_table_{VERSION}_data.js", out / "data.js")
    for name in ("favicon.svg", "favicon-32.png"):
        shutil.copyfile(TABLES / name, out / name)
    (out / "logos").mkdir(exist_ok=True)
    for name in LOGOS:
        shutil.copyfile(TABLES / "logos" / name, out / "logos" / name)
    print(f"exported {VERSION} to {out}")


if __name__ == "__main__":
    main()
