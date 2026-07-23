---
# Reserved OKF file (index.md): directory listing — no `type`.
title: Knowledge Base Index
description: Hand-maintained map of this OKF bundle.
tags: [meta, index]
timestamp: 2026-06-15
# --- integrity extension (NOT part of OKF) ---
status: verified
review_by: 2027-06-15
---

# Knowledge Base Index

The hand-maintained map of this bundle (the OKF bundle root). Update it when you add or
retire a note. Start here; follow the links.

## How this base works

- The operating manual is `CLAUDE.md` at the repo root (outside the bundle) — read it
  for the OKF alignment and integrity rules.
- This bundle is an [OKF v0.1](sources/okf-v0-1-spec.md) directory of Markdown files;
  every non-reserved note carries a non-empty `type`.
- Every claim-bearing note cites `sources:` and carries an honest `status`.
- The [frontmatter schema](templates/frontmatter.md) lists every field (OKF + our
  integrity extension).
- The [log](log.md) records what changed and why.

## Sections

| Section                                    | What lives here                          |
|--------------------------------------------|------------------------------------------|
| [Concepts](concepts/index.md)              | Reusable ideas, terms, factual claims.   |
| [Decisions](decisions/index.md)            | ADRs.                                     |
| [Architecture](architecture/index.md)      | How the effort/system is structured.     |
| [Runbooks](runbooks/index.md)              | Repeatable procedures.                    |
| [Sources](sources/index.md)                | The evidence store.                       |
| [Templates](templates/frontmatter.md)      | Frontmatter + per-type note templates.    |

### Decision-support extension (optional)

The layer for evaluating options into a phased recommendation, with the same provenance as
any note (ADR-[0006](decisions/0006-decision-support-extension.md)). Delete these six folders
+ `METHODOLOGY.md` for a pure knowledge-capture effort. Start from the
[runbook](runbooks/run-a-decision-support-effort.md).

| Section                                        | What lives here                          |
|------------------------------------------------|------------------------------------------|
| [Recommendations](recommendations/index.md)    | Phased recommendations, for reaction.    |
| [Options](options/index.md)                    | Options under evaluation.                |
| [Criteria](criteria/index.md)                  | Evaluation criteria (matrix columns).    |
| [Gates](gates/index.md)                        | Decision-gate register (append-only).    |
| [Findings](findings/index.md)                  | Review-findings register (append-only).  |
| [Risks](risks/index.md)                        | Risk register (append-only).             |

## Worked examples (delete when starting a real effort)

The notes currently in each section document this template itself. They are real,
verified notes that double as examples of the conventions in action. Replace them with
your effort's content.
