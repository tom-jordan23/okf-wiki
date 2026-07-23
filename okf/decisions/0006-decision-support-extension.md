---
# --- OKF v0.1 ---
type: decision
title: "Adopt a decision-support extension to the base template"
description: Add decision-support note types, a presentation tier, and a methodology doc, extending OKF rather than forking to prose registers.
tags: [adr, decision-support, roadmap]
timestamp: 2026-07-23
# --- integrity extension (NOT part of OKF) ---
status: draft
confidence: medium
created: 2026-07-23
last_verified:
verified_by:
review_by: 2027-01-23
sources: []
---

# ADR-0006: Adopt a Decision-Support Extension to the Base Template

- **Status:** proposed
- **Date:** 2026-07-23
- **Deciders:** project owner
- **Roadmap:** [Decision-Support Extension](../architecture/decision-support-extension.md)

## Context

This template was designed for **static knowledge** — a claim-bearing note (`concept`,
`architecture`, `source`) that is written once and re-verified on a cadence. In practice
the owner has used clones of it mainly for **decision-support / recommendation** work:
evaluate a set of options against criteria, score them, and hand leadership a phased
recommendation with its provenance intact.

Three private decision-support efforts built on clones of this template were reviewed to
see how they diverged from this base (the efforts are institution-specific and are **not**
part of this public template; they are referenced here only as anonymized Effort A/B/C):

- **Effort A** — abandoned the `okf/` bundle entirely; rebuilt as prose "register"
  documents (decision-gate register, findings/review log, standing evaluation rubric,
  risk register) plus a lift-and-shift methodology doc and a `preso/` deck builder.
- **Effort B** — also abandoned `okf/`; built a source-class-partitioned evidence tree,
  a slug-based citation log, scoped producer/checker subagents, a recorded fact-check
  artifact, decision/capability matrices, and a methodology doc.
- **Effort C** — the only one that **kept the OKF core byte-identical** and grew
  additively: a `preso/` tier, an `artifacts/` staging convention, a visual design-system
  concept, and the full options→criteria→matrix→phased-recommendation pattern expressed
  **in ordinary `architecture` notes with no schema change**.

Two signals dominate. First, **two of three efforts left the rails** — the base gave
them no vocabulary for options-in-flight, findings, gates, or recommendations, so they
rebuilt from scratch and lost the OKF+`validate.py` integrity backbone in the process.
Second, the patterns they rebuilt **converged**: all three independently produced a
deck-from-Markdown `preso/` tier, an options→criteria→scored-matrix→phased-recommendation
spine, and a "how this was produced" methodology doc.

Effort C is the existence proof that this work fits inside OKF. One effort's own review
reached the same conclusion: the opportunity is to marry the decision-support artifact
vocabulary to okf-wiki's validation backbone.

## Decision

Adopt a **decision-support extension** to the base template, and build it by
**extending OKF** — new artifacts become real `type:` values with templates and
`validate.py` enforcement — rather than forking to unvalidated prose registers.

Scope, phased (full plan in the [roadmap note](../architecture/decision-support-extension.md)):

1. **No-schema-change additions first:** a `preso/` deck-from-code tier (sibling to
   `docs/`), an `artifacts/` git-ignored staging convention, and a **decision-support
   runbook** encoding options→criteria→matrix→ruled-out→phased-recommendation→open-decisions.
2. **New note types + templates + validation:** `option`, `criterion`, `gate`, `finding`,
   `risk`, `recommendation`; teach `validate.py` their statuses and required fields; add a
   `METHODOLOGY.md` companion.
3. **Agent + design layers:** a `.claude/agents/` producer/checker + multi-lens review
   roster, and a `visual-vocabulary` design-system concept.

Cross-cutting conventions to bake in: append-only registers (never edit a closed row —
append a dated resolution note), confidence rated on **feasibility, not desirability**,
recommendations framed **"for reaction, not decision,"** strength-of-evidence travelling
with each claim, and absence-of-evidence recorded as an explicit finding.

## Consequences

- **Easier:** the next decision-support effort stays on the OKF rails instead of
  rebuilding; recommendations inherit the same provenance/verification guarantees as
  concept notes; findings and gates become machine-checkable, which the prose-register
  versions never were.
- **Harder:** more note types and `validate.py` rules to maintain; the template grows
  past a pure "wiki" into a decision-support toolkit — the `## Project` clone step must
  make the decision-support pieces clearly optional.
- **Committed to:** OKF conformance for the new types (non-empty `type`, reserved-file
  rules) and to keeping the decision-support layer deletable for efforts that are pure
  knowledge capture.

## Alternatives considered

- **Bless the prose-register style** as a parallel convention outside `okf/` (the
  approach Efforts A and B took). Lower friction to author, but forfeits validation and
  leaves two idioms in one template. Rejected in favor of extending OKF.
- **Do nothing / keep it a pure knowledge wiki.** Honest, but ignores that the template's
  actual use is decision-support and that clones keep leaving the rails. Rejected.
- **Decide the schema fork per-artifact later.** Defers the core call that shapes every
  template and validator rule; the review already showed OKF can carry this work. Rejected
  in favor of committing to the OKF-extension direction now.

## Sources

- None yet. This ADR rests on a first-party review of three private efforts built on
  clones of this template (anonymized as Effort A/B/C above; not part of this public
  template), not on external sources; it stays `draft`/proposed until the extension is
  designed and a first artifact is built. When built, capture the reviewed methodology
  docs as `source` notes (`source_type: internal-doc`) in the effort that cites them, so
  this decision's basis is traceable there.
