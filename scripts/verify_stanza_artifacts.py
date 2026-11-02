#!/usr/bin/env python3
"""Read-only check that a Stanza cache holds exactly the pinned model artifacts.

Verifies, against references/stanza-1.14.0-default_accurate.json (or another pins file):

1. $STANZA_RESOURCES_DIR/resources.json has the pinned SHA-256, and its Slovenian
   default_accurate mapping equals the pinned mapping;
2. every pinned artifact exists under $STANZA_RESOURCES_DIR/sl/ with the pinned size and SHA-256;
3. the Hugging Face cache resolves refs/main of the transformer to the pinned revision, and the
   files the pipeline loads from that snapshot have the pinned SHA-256.

Nothing is downloaded or written, except the optional --report JSON.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

# Files transformers needs to load a BERT model and tokenizer from a PyTorch snapshot.
REQUIRED_SNAPSHOT_FILES = ("config.json", "vocab.txt", "tokenizer_config.json", "pytorch_model.bin")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pins", default="references/stanza-1.14.0-default_accurate.json")
    parser.add_argument("--stanza-dir", default=os.environ.get("STANZA_RESOURCES_DIR"),
                        help="Stanza resources dir (default: $STANZA_RESOURCES_DIR)")
    parser.add_argument("--hf-home", default=os.environ.get("HF_HOME"), help="Hugging Face home (default: $HF_HOME)")
    parser.add_argument("--lang", default="sl")
    parser.add_argument("--report", default=None, help="Optional JSON report path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.stanza_dir or not args.hf_home:
        print("ERROR: --stanza-dir/--hf-home (or STANZA_RESOURCES_DIR/HF_HOME) must be set", file=sys.stderr)
        return 2
    pins = json.loads(Path(args.pins).read_text(encoding="utf-8"))
    stanza_dir, hf_home = Path(args.stanza_dir), Path(args.hf_home)
    checks = []

    def record(name: str, ok: bool, detail: str) -> None:
        checks.append({"check": name, "ok": ok, "detail": detail})
        print(f"[{'OK' if ok else 'FAIL'}] {name}: {detail}")

    resources = stanza_dir / "resources.json"
    if resources.is_file():
        actual = sha256_file(resources)
        expected = pins["resources"]["resources_json_sha256"]
        record("resources.json sha256", actual == expected, f"{actual} (expected {expected})")
        try:
            mapping = json.loads(resources.read_text(encoding="utf-8"))[args.lang]["packages"][pins["system"]["package"]]
            subset = {k: mapping.get(k) for k in pins["resources"]["default_accurate"]}
            record("resources.json package mapping", subset == pins["resources"]["default_accurate"], json.dumps(subset))
        except (KeyError, ValueError) as exc:
            record("resources.json package mapping", False, f"cannot read mapping: {exc}")
    else:
        record("resources.json present", False, str(resources))

    for rel, meta in pins["artifacts"].items():
        path = stanza_dir / args.lang / rel
        if not path.is_file():
            record(f"artifact {rel}", False, f"missing: {path}")
            continue
        size = path.stat().st_size
        actual = sha256_file(path)
        ok = size == meta["size_bytes"] and actual == meta["sha256"]
        record(f"artifact {rel}", ok, f"size {size} sha256 {actual}")

    tf = pins["transformer"]
    repo_dir = hf_home / "hub" / ("models--" + tf["model"].replace("/", "--"))
    ref_main = repo_dir / "refs" / "main"
    if ref_main.is_file():
        rev = ref_main.read_text(encoding="utf-8").strip()
        record("transformer refs/main", rev == tf["revision"], f"{rev} (expected {tf['revision']})")
    else:
        record("transformer refs/main", False, f"missing: {ref_main}")
    snapshot = repo_dir / "snapshots" / tf["revision"]
    for name, meta in sorted(tf["snapshot_files"].items()):
        path = snapshot / name
        if not path.exists():
            if name in REQUIRED_SNAPSHOT_FILES:
                record(f"transformer {name}", False, f"missing: {path}")
            else:
                print(f"[--] transformer {name}: not in snapshot (not needed for PyTorch loading)")
            continue
        actual = sha256_file(path.resolve())
        record(f"transformer {name}", actual == meta["sha256"], actual)

    failed = [c for c in checks if not c["ok"]]
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(json.dumps({
            "pins": args.pins, "stanza_dir": str(stanza_dir), "hf_home": str(hf_home),
            "status": "PASS" if not failed else "FAIL", "checks": checks}, indent=1) + "\n", encoding="utf-8")
    print(f"Artifact verification: {'PASS' if not failed else 'FAIL'} ({len(checks) - len(failed)}/{len(checks)} checks)")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
