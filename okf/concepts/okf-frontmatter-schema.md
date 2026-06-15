---
# --- OKF v0.1 ---
type: concept
title: "OKF-Compatible Frontmatter Schema"
description: The OKF v0.1 fields plus our integrity extension, and why each exists.
tags: [meta, schema, okf]
timestamp: 2026-06-15
# --- integrity extension (NOT part of OKF) ---
status: verified
confidence: high
created: 2026-06-15
last_verified: 2026-06-15
verified_by: claude
review_by: 2026-12-15
sources:
  - ../sources/okf-v0-1-spec.md
---

# OKF-Compatible Frontmatter Schema

> Every note opens with a YAML frontmatter block: the OKF v0.1 core plus our
> integrity extension.

## Summary

The schema has two layers:

- **OKF v0.1 core** — `type` (the only required field), plus optional `title`,
  `description`, `resource`, `tags`, `timestamp`. These come from the
  [OKF spec](../sources/okf-v0-1-spec.md).
- **Integrity extension (ours, not OKF)** — `status`, `confidence`, `created`,
  `last_verified`, `verified_by`, `review_by`, `sources`. OKF explicitly permits such
  custom extension keys, so adding them keeps the bundle conformant.

The full field-by-field table lives in [the field reference](../templates/frontmatter.md).

## Claims

- **OKF v0.1 requires exactly one frontmatter field, `type`, and permits arbitrary
  extension keys.** This is what makes our integrity fields legal without breaking
  conformance. [OKF spec](../sources/okf-v0-1-spec.md)
- **Reserved files `index.md` and `log.md` are exempt from the `type` requirement** and
  must not be concept documents — which is why they carry no `type`.
  [OKF spec](../sources/okf-v0-1-spec.md)
- A note's `status` must reflect reality: `verified` is only valid once the listed
  `sources` have been checked against the note's claims. *(This is a convention of this
  template, defined in `CLAUDE.md` — self-sourced.)*

## Notes

See [knowledge base layout](../architecture/knowledge-base-layout.md) for where each
note type lives, and [add and verify a note](../runbooks/add-and-verify-a-note.md) for
the procedure that moves a note from `draft` to `verified`.

## Sources

- [OKF v0.1 specification](../sources/okf-v0-1-spec.md) — the required/optional fields,
  extension keys, and reserved-file rules.
