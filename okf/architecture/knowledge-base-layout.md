---
# --- OKF v0.1 ---
type: architecture
title: "Knowledge Base Layout"
description: The OKF bundle's folders, note types, reserved files, and cross-linking.
tags: [architecture, meta, okf]
timestamp: 2026-07-23
# --- integrity extension (NOT part of OKF) ---
status: verified
confidence: high
created: 2026-06-15
last_verified: 2026-07-23
verified_by: claude
review_by: 2026-12-15
sources:
  - ../sources/okf-v0-1-spec.md
---

# Knowledge Base Layout

> The folders, note types, reserved files, and links that make up this OKF bundle.

## Overview

```text
okf/                 OKF bundle root (open as the Obsidian vault)
  index.md           reserved: map of the bundle (no type)
  log.md             reserved: dated change history (no type)
  concepts/          reusable ideas, terms, factual claims
  decisions/         ADRs
  architecture/      structure notes (this note lives here)
  runbooks/          repeatable procedures
  sources/           the evidence store
  templates/         frontmatter + per-type templates
  # --- decision-support extension (optional, deletable) ---
  recommendations/   phased recommendations (for reaction, not decision)
  options/           one evaluated option per note
  criteria/          one evaluation criterion per note
  gates/             decision-gate register (append-only)
  findings/          review-findings register (append-only)
  risks/             risk register (append-only)
```

## Components

- **`okf/index.md`** and per-folder **`index.md`** — reserved OKF directory listings
  (progressive disclosure); they carry no `type`. [OKF spec](../sources/okf-v0-1-spec.md)
- **`okf/log.md`** — reserved OKF change history.
- **Note-type folders** — each holds notes of one `type`. Every non-reserved note has a
  non-empty `type`, per OKF.
- **`sources/`** — the evidence store. Factual claims elsewhere link here so a fact can
  be traced to its evidence ([claim-level provenance](../concepts/okf-frontmatter-schema.md)).
- **`templates/`** — copy these to create new notes consistently.
- **Decision-support folders** (`recommendations/`, `options/`, `criteria/`, `gates/`,
  `findings/`, `risks/`) — the optional [decision-support extension](decision-support-extension.md).
  One note per option/criterion/gate/finding/risk/recommendation, each a real `type:` that
  `validate.py` checks. Deletable in full for pure knowledge-capture efforts.

## Constraints & rationale

- One effort per bundle; clone the template per effort. See
  [ADR-0001](../decisions/0001-markdown-frontmatter-project-memory.md) and
  [ADR-0002](../decisions/0002-adopt-okf-v0-1.md).
- **Identity is the file path** (OKF), so there is no `id` field; moving a file
  re-identifies its concept.
- **Cross-links are relative Markdown links** (`../concepts/x.md`) — navigable in
  Obsidian and OKF-conformant. OKF's `/`-absolute idiom is avoided because Obsidian
  cannot resolve leading slashes; see [ADR-0002](../decisions/0002-adopt-okf-v0-1.md).
- The bundle must remain readable as plain files — no required tooling.

## Sources

- [OKF v0.1 specification](../sources/okf-v0-1-spec.md) — bundle structure, reserved
  files, and cross-linking rules.
