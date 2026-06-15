---
# --- OKF v0.1 ---
type: decision
title: "Adopt OKF v0.1 as the bundle format"
description: Use the Open Knowledge Format v0.1 as the base, with relative links as a deliberate divergence.
tags: [adr, okf]
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

# ADR-0002: Adopt OKF v0.1 as the Bundle Format

- **Status:** accepted
- **Date:** 2026-06-15
- **Deciders:** project owner

## Context

[ADR-0001](0001-markdown-frontmatter-project-memory.md) chose Markdown + frontmatter for
project memory but defined a bespoke schema. A vendor-neutral standard for exactly this
shape now exists: [OKF v0.1](../sources/okf-v0-1-spec.md), published by Google Cloud on
2026-06-12. Adopting it buys portability and lets OKF-aware agents consume the bundle
without translation, at near-zero cost since our structure already matched.

We verified conformance against the spec before claiming it (the earlier draft asserted
"OKF-compatible" before the spec had been read — corrected here).

## Decision

Treat `okf/` as an OKF v0.1 bundle (bundle root = `okf/`):

- Every non-reserved note carries a non-empty `type`; `index.md`/`log.md` are reserved
  and carry no `type`.
- Use OKF fields (`type`, `title`, `description`, `tags`, `timestamp`, and `resource`
  on source notes) and keep our integrity fields as **extension keys**, clearly labeled
  as not part of OKF.
- Drop the custom `id` field — in OKF the file path is the concept's identity.

## Divergence (recorded deliberately)

OKF *recommends* bundle-root-absolute cross-links starting with `/` (e.g.
`/concepts/x.md`) for move-stability. **Obsidian does not resolve leading-slash paths**
(a deliberate Obsidian limitation, [open feature request]), so those links would not be
navigable in the vault. Because link style is **not** one of OKF's three conformance
criteria, we instead use **relative Markdown links** (`../concepts/x.md`). This keeps
the bundle conformant *and* navigable in Obsidian; the cost is slightly weaker
move-stability, mitigated by Obsidian's auto-update-on-move and Git history.

[open feature request]: https://forum.obsidian.md/t/start-absolute-path-with-a-leading-slash/32501

## Consequences

- **Easier:** portability to OKF tooling; a defensible "OKF v0.1" claim; one link style
  that works in Obsidian and for OKF consumers.
- **Harder:** we must track OKF's evolution — it is a three-day-old v0.1 (`review_by`
  set to 2026-12-15 on the [spec source](../sources/okf-v0-1-spec.md)).
- **Committed to:** path-as-identity; renaming/moving a file re-identifies its concept.

## Alternatives considered

- **Keep our bespoke schema, drop the OKF label** — fully honest, but forgoes interop
  for no real saving once conformance was this close. Rejected.
- **Use OKF's `/`-absolute links** — most idiomatic, but breaks Obsidian navigation,
  which the owner explicitly wanted. Rejected in favor of relative links.

## Sources

- [OKF v0.1 specification](../sources/okf-v0-1-spec.md)
