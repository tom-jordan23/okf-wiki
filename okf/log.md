---
# Reserved OKF file (log.md): dated change history — no `type`.
title: Activity & Decision Log
description: Chronological history of changes to this bundle, newest first.
tags: [meta, log]
timestamp: 2026-06-15
# --- integrity extension (NOT part of OKF) ---
status: verified
review_by: 2027-06-15
---

# Activity & Decision Log

Newest entries first. One entry per meaningful change or decision. Keep it terse; link
to the notes that hold the detail.

## 2026-06-15 — Hosted on GitHub; added validator

- Renamed the template `llm-wiki` → `okf-wiki` and published it as a public GitHub
  template repository: https://github.com/tom-jordan23/okf-wiki
- Added `scripts/validate.py`: OKF conformance (errors) + integrity checks (warnings).
  See the Validation section in `CLAUDE.md`. Bundle currently passes.

## 2026-06-15 — Aligned the bundle to OKF v0.1

- Adopted [OKF v0.1](sources/okf-v0-1-spec.md) as the base format; see
  [ADR-0002](decisions/0002-adopt-okf-v0-1.md).
- Dropped the custom `id` field (OKF identity = file path), replaced `[[wikilinks]]`
  with relative Markdown links, added OKF's `timestamp`, and relabeled the integrity
  fields as OKF extension keys.
- Marked `index.md` / `log.md` as reserved files (no `type`).
- Recorded the relative-vs-absolute link divergence (for Obsidian navigability) in
  ADR-0002.

## 2026-06-15 — Template scaffolded

- Created the LLM-wiki template: operating manual (`CLAUDE.md`), the `okf/` knowledge
  base, per-type templates, and one worked example per note type.
- Baked in the academic-integrity extension: sources required, verification status,
  claim-level provenance, and `review_by` staleness cadence. See
  [ADR-0001](decisions/0001-markdown-frontmatter-project-memory.md).
- Enforcement is convention + Claude review for now; a validator and CI are on the
  roadmap in `CLAUDE.md`.
