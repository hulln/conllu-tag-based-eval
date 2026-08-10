#!/usr/bin/env python3

from collections import Counter
from pathlib import Path

GOLD = Path("data/gold/sl_sst-ud-test.conllu")
OUTPUT = Path("results/output/20260810-stanza-1.13-vs-1.14_sl-sst-ud-test_full/main/stanza-1.13-vs-1.14-change-review.md")

RUNS = {
    "default": (
        Path("predictions/output/20260810-stanza-1.13-vs-1.14_sl-sst-ud-test_full_stanza-1.13.0-default_aligned_predicted.conllu"),
        Path("predictions/output/20260810-stanza-1.13-vs-1.14_sl-sst-ud-test_full_stanza-1.14.0-default_aligned_predicted.conllu"),
    ),
    "default_accurate": (
        Path("predictions/output/20260810-stanza-1.13-vs-1.14_sl-sst-ud-test_full_stanza-1.13.0-accurate_aligned_predicted.conllu"),
        Path("predictions/output/20260810-stanza-1.13-vs-1.14_sl-sst-ud-test_full_stanza-1.14.0-accurate_aligned_predicted.conllu"),
    ),
}

FIELDS = [
    ("LEMMA", 2),
    ("UPOS", 3),
    ("XPOS", 4),
    ("FEATS", 5),
    ("HEAD", 6),
    ("DEPREL", 7),
]


def read_conllu(path):
    sentences = []
    comments = {}
    rows = []

    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")

            if not line:
                if rows:
                    sentences.append((comments, rows))
                comments = {}
                rows = []
                continue

            if line.startswith("#"):
                if " = " in line:
                    key, value = line[2:].split(" = ", 1)
                    comments[key] = value
                continue

            cols = line.split("\t")
            if cols[0].isdigit():
                rows.append(cols)

    if rows:
        sentences.append((comments, rows))

    return sentences


def outcome(gold, old, new):
    if old == gold and new != gold:
        return "REGRESSION"
    if old != gold and new == gold:
        return "FIX"
    if old != gold and new != gold:
        return "BOTH WRONG"
    return "OTHER"


def validate_alignment(gold, old, new, mode):
    if not (len(gold) == len(old) == len(new)):
        raise ValueError(f"{mode}: sentence counts differ")

    for sent_no, ((_, g), (_, a), (_, b)) in enumerate(
        zip(gold, old, new), start=1
    ):
        if not (len(g) == len(a) == len(b)):
            raise ValueError(f"{mode}: token count differs in sentence {sent_no}")

        for token_no, (gr, ar, br) in enumerate(zip(g, a, b), start=1):
            if not (gr[0] == ar[0] == br[0]):
                raise ValueError(
                    f"{mode}: token ID mismatch in sentence {sent_no}, token {token_no}"
                )
            if not (gr[1] == ar[1] == br[1]):
                raise ValueError(
                    f"{mode}: FORM mismatch in sentence {sent_no}, token {token_no}"
                )


def analyse_mode(mode, gold, old, new):
    changed = []
    field_counts = Counter()
    dep_counts = Counter()

    for (comments, g_rows), (_, o_rows), (_, n_rows) in zip(gold, old, new):
        for g, o, n in zip(g_rows, o_rows, n_rows):
            differences = [(name, idx) for name, idx in FIELDS if o[idx] != n[idx]]

            if not differences:
                continue

            token_changes = []

            for name, idx in differences:
                status = outcome(g[idx], o[idx], n[idx])
                field_counts[(name, status)] += 1
                token_changes.append(
                    {
                        "field": name,
                        "gold": g[idx],
                        "old": o[idx],
                        "new": n[idx],
                        "outcome": status,
                    }
                )

            old_dep_correct = o[6] == g[6] and o[7] == g[7]
            new_dep_correct = n[6] == g[6] and n[7] == g[7]

            if not old_dep_correct and new_dep_correct:
                dep_status = "FIX"
            elif old_dep_correct and not new_dep_correct:
                dep_status = "REGRESSION"
            elif not old_dep_correct and not new_dep_correct:
                dep_status = "BOTH WRONG"
            else:
                dep_status = "BOTH CORRECT"

            dep_counts[dep_status] += 1

            changed.append(
                {
                    "sent_id": comments.get("sent_id", "?"),
                    "text": comments.get("text", ""),
                    "id": g[0],
                    "form": g[1],
                    "changes": token_changes,
                    "dependency_outcome": dep_status,
                }
            )

    return changed, field_counts, dep_counts


def add_summary(lines, mode, changed, field_counts, dep_counts):
    lines += [
        f"## {mode}",
        "",
        f"Changed token rows: **{len(changed)}**",
        "",
        "### Changed fields",
        "",
        "| Field | Changed | Fixes | Regressions | Both wrong |",
        "|---|---:|---:|---:|---:|",
    ]

    for field, _ in FIELDS:
        fixes = field_counts[(field, "FIX")]
        regressions = field_counts[(field, "REGRESSION")]
        wrong = field_counts[(field, "BOTH WRONG")]
        total = fixes + regressions + wrong + field_counts[(field, "OTHER")]

        lines.append(
            f"| {field} | {total} | {fixes} | {regressions} | {wrong} |"
        )

    lines += [
        "",
        "### Exact dependency annotation (HEAD + DEPREL)",
        "",
        "| Outcome | Tokens |",
        "|---|---:|",
        f"| 1.14 fixes 1.13 error | {dep_counts['FIX']} |",
        f"| 1.14 regression | {dep_counts['REGRESSION']} |",
        f"| Both versions wrong | {dep_counts['BOTH WRONG']} |",
        f"| Both dependency-correct, another field changed | {dep_counts['BOTH CORRECT']} |",
        "",
    ]


def main():
    gold = read_conllu(GOLD)

    report = [
        "# Stanza 1.13.0 vs 1.14.0 — changed-token review",
        "",
        "Token-level comparison of Stanza 1.13.0 and 1.14.0 on the same",
        "pretokenized SST-UD gold test set.",
        "",
        "Only tokens whose predictions differ between versions are listed.",
        "`FIX`, `REGRESSION`, and `BOTH WRONG` are determined against the",
        "manually annotated gold values.",
        "",
    ]

    detailed_sections = []

    for mode, (old_path, new_path) in RUNS.items():
        old = read_conllu(old_path)
        new = read_conllu(new_path)

        validate_alignment(gold, old, new, mode)
        changed, field_counts, dep_counts = analyse_mode(mode, gold, old, new)

        add_summary(report, mode, changed, field_counts, dep_counts)

        detailed_sections += [
            f"# Detailed review: {mode}",
            "",
        ]

        for item in changed:
            detailed_sections += [
                f"## {item['sent_id']} — token {item['id']} `{item['form']}`",
                "",
                f"**Sentence:** {item['text']}",
                "",
                f"**Exact dependency outcome:** {item['dependency_outcome']}",
                "",
                "| Field | GOLD | 1.13 | 1.14 | Outcome |",
                "|---|---|---|---|---|",
            ]

            for change in item["changes"]:
                detailed_sections.append(
                    f"| {change['field']} | `{change['gold']}` | "
                    f"`{change['old']}` | `{change['new']}` | "
                    f"**{change['outcome']}** |"
                )

            detailed_sections.append("")

        print(f"{mode}: {len(changed)} changed token rows")
        for field, _ in FIELDS:
            total = sum(
                field_counts[(field, status)]
                for status in ("FIX", "REGRESSION", "BOTH WRONG", "OTHER")
            )
            if total:
                print(
                    f"  {field}: {total} changed "
                    f"(fixes={field_counts[(field, 'FIX')]}, "
                    f"regressions={field_counts[(field, 'REGRESSION')]}, "
                    f"both_wrong={field_counts[(field, 'BOTH WRONG')]})"
                )
        print(
            "  HEAD+DEPREL:",
            f"fixes={dep_counts['FIX']},",
            f"regressions={dep_counts['REGRESSION']},",
            f"both_wrong={dep_counts['BOTH WRONG']},",
            f"both_correct={dep_counts['BOTH CORRECT']}",
        )

    report += detailed_sections
    OUTPUT.write_text("\n".join(report).rstrip("\n") + "\n", encoding="utf-8")
    print(f"\nWrote {OUTPUT}")


if __name__ == "__main__":
    main()
