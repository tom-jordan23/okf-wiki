---
# --- OKF v0.1 ---
type: decision
title: "Use Markdown + Frontmatter for Project Memory"
description: Store project memory as Markdown files with YAML frontmatter under Git.
tags: [adr]
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

# ADR-0001: Use Markdown + Frontmatter for Project Memory

- **Status:** accepted (base format later specified by [ADR-0002](0002-adopt-okf-v0-1.md))
- **Date:** 2026-06-15
- **Deciders:** project owner

## Context

The effort needs durable, inspectable project memory that survives outside chat
transcripts, is reviewable in merge requests, and is portable across tools (Obsidian,
GitLab/GitHub rendering, a future docs site). It also needs to carry provenance and
verification state per note so the knowledge base stays trustworthy as it grows.

## Decision

Store project memory as plain Markdown files with YAML frontmatter, under Git, in the
`okf/` tree. Encode integrity metadata (sources, status, verification, review cadence)
in the frontmatter — see [OKF-Compatible Frontmatter Schema](../concepts/okf-frontmatter-schema.md).
[ADR-0002](0002-adopt-okf-v0-1.md) later adopts OKF v0.1 as the concrete format.

## Consequences

- **Easier:** diff/review in MRs, full-text search, tool portability, agent parsing.
- **Easier:** integrity rules become mechanical fields rather than vibes.
- **Harder:** no automated enforcement yet — discipline relies on curation + review
  until a validator and CI are added (see roadmap in `CLAUDE.md`).
- **Committed to:** stable file paths as link/identity targets; moving a file is a
  deliberate act.

## Alternatives considered

- **A database / structured KM tool** — richer queries, but not diff-reviewable, less
  portable, heavier to start. Rejected for a first version.
- **Freeform notes without frontmatter** — lower friction, but loses the provenance and
  verification guarantees that are the whole point. Rejected.

## Sources

- None. This is an internal design decision, self-sourced.
