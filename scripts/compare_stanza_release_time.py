#!/usr/bin/env python3

from pathlib import Path
import argparse
import filecmp

METRICS = (
    "LAS", "UAS", "MLAS", "BLEX", "CLAS",
    "UPOS", "XPOS", "UFeats", "Lemmas", "AllTags",
)

ROOT = Path(__file__).resolve().parents[1]


def parse_eval(path: Path):
    scores = {}

    for line in path.read_text(encoding="utf-8").splitlines():
        parts = [part.strip() for part in line.split("|")]
        if not parts or parts[0] not in METRICS:
            continue

        metric = parts[0]

        # CoNLL evaluator layout:
        # metric | Precision | Recall | F1 | AlignedAcc
        # Use F1 consistently for every reported metric.
        if len(parts) < 4:
            raise ValueError(f"Missing F1 column in {path}: {line}")
        value = float(parts[3])

        scores[metric] = value

    missing = set(METRICS) - set(scores)
    if missing:
        raise ValueError(f"Missing metrics in {path}: {sorted(missing)}")

    return scores


def release113(corpus, package):
    return ROOT / (
        f"results/output/20260811-stanza-1.13-release-defaults_"
        f"sl-{corpus}-ud-test_full/main/"
        f"stanza-1.13.0-release-{package}_aligned_eval.txt"
    )


def current113(corpus, package):
    return ROOT / (
        f"results/output/20260810-stanza-1.13-vs-1.14_"
        f"sl-{corpus}-ud-test_full/main/"
        f"stanza-1.13.0-{package}_aligned_eval.txt"
    )


def release114(corpus, package):
    return ROOT / (
        f"results/output/20260811-stanza-1.14-release-defaults_"
        f"sl-{corpus}-ud-test_full/main/"
        f"stanza-1.14.0-release-{package}_aligned_eval.txt"
    )


def original114(corpus, package):
    return ROOT / (
        f"results/output/20260810-stanza-1.13-vs-1.14_"
        f"sl-{corpus}-ud-test_full/main/"
        f"stanza-1.14.0-{package}_aligned_eval.txt"
    )


def prediction114(corpus, package, release):
    if release:
        return ROOT / (
            f"predictions/output/20260811-stanza-1.14-release-defaults_"
            f"sl-{corpus}-ud-test_full_"
            f"stanza-1.14.0-release-{package}_aligned_predicted.conllu"
        )

    return ROOT / (
        f"predictions/output/20260810-stanza-1.13-vs-1.14_"
        f"sl-{corpus}-ud-test_full_"
        f"stanza-1.14.0-{package}_aligned_predicted.conllu"
    )


def verify_release114_identity():
    """Independent check that the reconstruction reproduces the original 1.14 run.

    This is a verification step in its own right. No comparison below depends on
    it: each block reads the artifacts named in its own title, so skipping this
    check cannot silently change which files are compared.
    """
    for corpus in ("ssj", "sst"):
        for package in ("default", "accurate"):
            old_eval = original114(corpus, package)
            new_eval = release114(corpus, package)
            old_pred = prediction114(corpus, package, False)
            new_pred = prediction114(corpus, package, True)

            if not filecmp.cmp(old_eval, new_eval, shallow=False):
                raise AssertionError(
                    f"1.14 evaluator files differ: {corpus}/{package}"
                )

            if not filecmp.cmp(old_pred, new_pred, shallow=False):
                raise AssertionError(
                    f"1.14 prediction files differ: {corpus}/{package}"
                )


def print_comparison(title, left_fn, right_fn):
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)

    for corpus in ("ssj", "sst"):
        for package in ("default", "accurate"):
            left = parse_eval(left_fn(corpus, package))
            right = parse_eval(right_fn(corpus, package))

            print(f"\n{corpus.upper()} / {package}")
            print(f"{'Metric':<10} {'Left':>8} {'Right':>8} {'Delta':>9}")

            for metric in METRICS:
                delta = right[metric] - left[metric]
                print(
                    f"{metric:<10} "
                    f"{left[metric]:8.2f} "
                    f"{right[metric]:8.2f} "
                    f"{delta:+9.2f}"
                )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-identity-check",
        action="store_true",
        help="Do not verify that original and reconstructed 1.14 artifacts are byte-identical.",
    )
    args = parser.parse_args()

    if not args.skip_identity_check:
        verify_release114_identity()
        print(
            "VERIFY: all four reconstructed release-time Stanza 1.14 "
            "prediction and evaluator files are byte-identical to the original 1.14 run."
        )

    print_comparison(
        "MAIN: release-time 1.13 -> release-time 1.14",
        release113,
        release114,
    )

    print_comparison(
        "RESOURCE DRIFT: release-time 1.13 -> present-day-resource 1.13",
        release113,
        current113,
    )

    # Right side is original114, not release114: this block reports what the
    # 2026-08-10 experiment measured, so it must read that run's own artifacts.
    print_comparison(
        "ORIGINAL EXPERIMENT: present-day-resource 1.13 -> 1.14",
        current113,
        original114,
    )


if __name__ == "__main__":
    main()
