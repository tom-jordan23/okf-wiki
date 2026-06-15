---
# --- OKF v0.1 ---
type: runbook
title: "Add and Verify a Note"
description: How to add a note and move it honestly from draft to verified.
tags: [runbook, meta]
timestamp: 2026-06-15
# --- integrity extension (NOT part of OKF) ---
status: verified
confidence: high
created: 2026-06-15
last_verified: 2026-06-15
verified_by: claude
review_by: 2027-06-15
sources: []
---

# Add and Verify a Note

> How to add a note and move it honestly from `draft` to `verified`.

## Prerequisites

- You know which [note type](../architecture/knowledge-base-layout.md) you are writing.
- You have the evidence on hand for any factual claims.

## Steps

1. Copy the matching template from `okf/templates/` into the right folder.
2. Fill `type` (non-empty — required by OKF), `title`, `description`, and `timestamp`.
   Do **not** add an `id`; the file path is the note's identity.
3. Write the body. For each factual claim, link the supporting source inline with a
   relative Markdown link, e.g. `... rose 12% in 2025 ([source](../sources/the-source.md))`.
4. For each source, create or update a note in `okf/sources/` (copy
   `templates/source.md`) and add its relative path to the note's `sources:` list.
5. Set `status: draft` and leave `last_verified` blank for now.
6. **Verify:** actually read each source and confirm it supports the claim it is
   attached to. Only then set `status: verified`, `last_verified` to today, and
   `verified_by`.
7. Set `review_by` to when the note should be re-checked.
8. Add the note to its folder `index.md` and, if meaningful, a line to `okf/log.md`.

## Verification

- Every non-reserved note has a non-empty `type`; reserved `index.md`/`log.md` have no
  `type`.
- Every claim-bearing note has at least one entry in `sources:`.
- No note is `verified` without a real, checked source and a `last_verified` date.
- All relative Markdown links resolve to an existing file.

## Rollback / recovery

If you cannot verify a claim, do **not** upgrade its status. Leave it `draft`, or set
`disputed` and explain the conflict in the body. Honesty over completeness.

## Sources

- None. This procedure documents this template's own workflow; self-sourced.
