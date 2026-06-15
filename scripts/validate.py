#!/usr/bin/env python3
"""Validate the okf/ knowledge bundle.

Checks two layers:

1. OKF v0.1 conformance (the three spec rules)
   - every non-reserved .md file in the bundle has a parseable YAML frontmatter block
   - every such block has a non-empty `type`
   - reserved files (index.md, log.md) carry NO `type`
2. Integrity extension (this template's conventions)
   - claim-bearing notes should cite `sources`
   - notes past their `review_by` date are flagged stale

Cross-links are also resolved and reported, but OKF requires consumers to tolerate
broken links, so unresolved links are warnings, never errors.

Usage:
    python3 scripts/validate.py [bundle_dir] [--today YYYY-MM-DD]

Exit code is non-zero if any OKF conformance ERROR is found. Warnings never fail.
No third-party dependencies (frontmatter is parsed with a small built-in reader, so
this runs anywhere Python 3 does).
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys

RESERVED = {"index.md", "log.md"}
# Fields whose presence implies the note makes verifiable claims and so should cite sources.
CLAIM_STATUSES = {"verified", "disputed"}


def split_frontmatter(text: str):
    """Return (frontmatter_str | None, body_str). Frontmatter is the block between the
    leading '---' and the next '---' line."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    return text[3:end], text[end + 4:]


def scalar(fm: str, key: str):
    """Crude single-line scalar extractor. Good enough for our flat frontmatter."""
    m = re.search(rf"(?m)^{re.escape(key)}:\s*(.*)$", fm)
    if not m:
        return None
    return m.group(1).strip().strip('"').strip("'")


def has_nonempty_list(fm: str, key: str) -> bool:
    """True if `key:` is a non-empty inline list ([a, b]) or a block list with items."""
    inline = re.search(rf"(?m)^{re.escape(key)}:\s*\[(.*?)\]\s*$", fm)
    if inline:
        return bool(inline.group(1).strip())
    # block form: key: on its own line, followed by `  - ...` items
    block = re.search(rf"(?m)^{re.escape(key)}:\s*$\n((?:\s*-\s+.*\n?)+)", fm)
    return bool(block)


def parse_date(value: str | None):
    if not value:
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate the OKF knowledge bundle.")
    ap.add_argument("bundle", nargs="?", default="okf", help="bundle directory (default: okf)")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD) for staleness checks")
    args = ap.parse_args()

    today = parse_date(args.today) or dt.date.today()
    bundle = args.bundle

    if not os.path.isdir(bundle):
        print(f"error: bundle directory not found: {bundle}", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    checked = 0

    md_files = []
    for root, _, files in os.walk(bundle):
        for fn in files:
            if fn.endswith(".md"):
                md_files.append(os.path.join(root, fn))

    for path in sorted(md_files):
        checked += 1
        fn = os.path.basename(path)
        reserved = fn in RESERVED
        with open(path, encoding="utf-8") as f:
            text = f.read()
        fm, body = split_frontmatter(text)

        # --- OKF rule 1: parseable frontmatter present ---
        if fm is None:
            errors.append(f"{path}: no parseable YAML frontmatter block")
            continue

        type_val = scalar(fm, "type")
        has_type = bool(type_val)

        # --- OKF rule 2 + reserved-file exemption ---
        if reserved:
            if has_type:
                errors.append(f"{path}: reserved file (index.md/log.md) must NOT carry a `type`")
        else:
            if not has_type:
                errors.append(f"{path}: non-reserved file missing a non-empty `type`")

        # --- Integrity: claim-bearing notes should cite sources ---
        status = scalar(fm, "status")
        if not reserved and status in CLAIM_STATUSES and not has_nonempty_list(fm, "sources"):
            # self-sourced meta notes legitimately have empty sources; flag as warning, not error
            warnings.append(f"{path}: status '{status}' but `sources` is empty (ok only if self-sourced)")

        # --- Integrity: staleness ---
        review_by = parse_date(scalar(fm, "review_by"))
        if review_by and review_by < today and status != "stale":
            warnings.append(f"{path}: review_by {review_by} has passed; mark `stale` and re-verify")

        # --- Link resolution (warnings only; OKF tolerates broken links) ---
        for target in re.findall(r"\]\(([^)]+)\)", body):
            t = target.split("#")[0].strip()
            if not t or t.startswith(("http://", "https://", "mailto:")):
                continue
            if t.endswith(".md"):
                resolved = os.path.normpath(os.path.join(os.path.dirname(path), t))
                if not os.path.exists(resolved):
                    warnings.append(f"{path}: unresolved link -> {target}")

    print(f"Checked {checked} markdown files in {bundle}/\n")
    print("OKF v0.1 conformance:")
    print(f"  [{'FAIL' if errors else 'PASS'}] frontmatter parseable; non-empty `type` on "
          f"non-reserved files; no `type` on reserved files")
    for e in errors:
        print(f"   x {e}")

    print("\nIntegrity + links (warnings, non-fatal):")
    if warnings:
        for w in warnings:
            print(f"   ! {w}")
    else:
        print("   none")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
