#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "experiments/20260812-stanza-1.12-vs-1.14"

METRICS = ("LAS", "UAS", "Lemmas", "UPOS", "UFeats")


def parse_eval(path):
    scores = {}

    for line in path.read_text(encoding="utf-8").splitlines():
        parts = [part.strip() for part in line.split("|")]
        if parts and parts[0] in METRICS:
            scores[parts[0]] = float(parts[3])

    missing = set(METRICS) - set(scores)
    if missing:
        raise ValueError(f"Missing metrics in {path}: {sorted(missing)}")

    return scores


def eval112(corpus, package):
    return ROOT / (
        f"results/output/20260812-stanza-1.12-release-defaults_"
        f"sl-{corpus}-ud-test_full/main/"
        f"stanza-1.12.0-release-{package}_aligned_eval.txt"
    )


def eval114(corpus, package):
    return ROOT / (
        f"results/output/20260811-stanza-1.14-release-defaults_"
        f"sl-{corpus}-ud-test_full/main/"
        f"stanza-1.14.0-release-{package}_aligned_eval.txt"
    )


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("Stanza 1.12.0 -> 1.14.0 release-time comparison")
    lines.append("")

    for corpus in ("ssj", "sst"):
        for package in ("default", "accurate"):
            left = parse_eval(eval112(corpus, package))
            right = parse_eval(eval114(corpus, package))

            lines.append(f"{corpus.upper()} / {package}")
            lines.append(f"{'Metric':<8} {'1.12':>7} {'1.14':>7} {'Delta':>8}")

            for metric in METRICS:
                delta = right[metric] - left[metric]
                lines.append(
                    f"{metric:<8} "
                    f"{left[metric]:7.2f} "
                    f"{right[metric]:7.2f} "
                    f"{delta:+8.2f}"
                )

            lines.append("")

    comparison = "\n".join(lines).rstrip() + "\n"
    (OUT_DIR / "comparison.txt").write_text(comparison, encoding="utf-8")

    table = [
        "| Stanza | Configuration | SSJ LAS | SSJ UAS | SSJ Lemma | SSJ UPOS | SSJ UFeats | SST LAS | SST UAS | SST Lemma | SST UPOS | SST UFeats |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for version, fn in (("1.12", eval112), ("1.14", eval114)):
        for package, label in (
            ("default", "default"),
            ("accurate", "default_accurate"),
        ):
            ssj = parse_eval(fn("ssj", package))
            sst = parse_eval(fn("sst", package))

            table.append(
                f"| {version} | {label} | "
                f"{ssj['LAS']:.2f} | {ssj['UAS']:.2f} | "
                f"{ssj['Lemmas']:.2f} | {ssj['UPOS']:.2f} | {ssj['UFeats']:.2f} | "
                f"{sst['LAS']:.2f} | {sst['UAS']:.2f} | "
                f"{sst['Lemmas']:.2f} | {sst['UPOS']:.2f} | {sst['UFeats']:.2f} |"
            )

    (OUT_DIR / "table.md").write_text("\n".join(table) + "\n", encoding="utf-8")

    print(comparison)
    print("Wrote:")
    print(OUT_DIR / "comparison.txt")
    print(OUT_DIR / "table.md")


if __name__ == "__main__":
    main()
