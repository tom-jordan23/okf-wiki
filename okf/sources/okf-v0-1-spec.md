---
# --- OKF v0.1 ---
type: source
title: "Open Knowledge Format (OKF) v0.1"
description: Google Cloud's vendor-neutral spec for agent-readable Markdown knowledge bundles.
tags: [source, okf, standard]
timestamp: 2026-06-15
resource: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/
# --- integrity extension (NOT part of OKF) ---
status: verified
confidence: high
created: 2026-06-15
last_verified: 2026-06-15
verified_by: claude
review_by: 2026-12-15
# --- source evidence fields ---
source_type: standard
author: "Sam McVeety, Amir Hormati (Google Cloud)"
publisher: Google Cloud
url: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/
published: 2026-06-12
accessed: 2026-06-15
credibility: high
---

# Open Knowledge Format (OKF) v0.1

> Google Cloud, "How the Open Knowledge Format can improve data sharing," 2026-06-12.
> Apache-2.0 spec released on GitHub alongside sample bundles and two reference
> implementations.

## What it supports

This is the base-format authority for the whole bundle. It backs the claims in:

- [ADR-0002: Adopt OKF v0.1](../decisions/0002-adopt-okf-v0-1.md)
- [OKF-Compatible Frontmatter Schema](../concepts/okf-frontmatter-schema.md)
- [Knowledge Base Layout](../architecture/knowledge-base-layout.md)

## Summary

OKF v0.1 represents organizational knowledge as a **directory of Markdown files with
YAML frontmatter**. Verified facts from the spec and Google Cloud's announcement:

- **One required field:** `type` (non-empty). Recommended-but-optional fields:
  `title`, `description`, `resource`, `tags`, `timestamp`. Producers may add custom
  extension keys.
- **Conformance (3 rules):** every non-reserved `.md` file has parseable YAML
  frontmatter; every such block has a non-empty `type`; reserved filenames follow their
  prescribed structure.
- **Reserved filenames:** `index.md` (directory listing / progressive disclosure) and
  `log.md` (dated change history). They must not be used as concept documents.
- **Cross-linking:** standard Markdown links using bundle-root-absolute paths starting
  with `/` (e.g. `[customers](/tables/customers.md)`), chosen for move-stability;
  consumers must tolerate broken links.
- The full v0.1 spec fits on a single page (~451 lines) and is Apache-2.0 on GitHub.

## Assessment

**Credibility: high, with one caveat.** Primary source: the spec and announcement come
directly from the Google Cloud team that authored it (Sam McVeety, Amir Hormati), under
an open license with reference implementations — corroborated across multiple
independent write-ups. The caveat is **recency/stability**: as of access this is a
three-day-old v0.1 that may evolve, which is why `review_by` is set six months out
rather than a year. Re-check the spec for breaking changes before then.
