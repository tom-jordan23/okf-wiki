---
# --- OKF v0.1 ---
type: architecture
title: "Decision-Support Extension (roadmap)"
description: The planned decision-support layer — new note types, a presentation tier, and conventions — and its phasing.
tags: [architecture, decision-support, roadmap, meta]
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

# Decision-Support Extension (roadmap)

> The planned layer that turns this knowledge wiki into a decision-support toolkit,
> synthesized from a review of three private decision-support efforts built on clones of
> this template (institution-specific and **not** part of this public template). The
> decision to build it — and to extend OKF rather than fork — is
> [ADR-0006](../decisions/0006-decision-support-extension.md).

## The gap this closes

The base ships note types for **static knowledge**: `concept`, `decision`,
`architecture`, `runbook`, `source`. Decision-support work needs vocabulary for things
**in flight** — options being scored, findings being tracked, gates being closed,
recommendations being staged. Lacking it, two of three reviewed clones abandoned the
`okf/` bundle and lost the integrity backbone. This layer adds that vocabulary **inside**
OKF so the next effort stays on the rails.

## Planned additions

Ranked by how strongly the three efforts converged on them (all-three = strongest signal).

### Tier 1 — all three efforts built this independently

- **`preso/` deck-from-code tier** *(no schema change)*. Markdown speaker-script is the
  source of record; a `python-pptx` builder mirrors it; decks live **outside** `okf/`
  (a sibling to `docs/`) and carry no frontmatter; every slide claim traces back to a
  note. Ship `build.sh` + a skeletal builder + a README stating the contract.
- **Options → criteria → scored-matrix → phased-recommendation pattern.** A fixed
  per-option schema (thesis / what it configures / retires / does not retire / cost /
  governance / risk / why viable), a **ruled-out set** (each option tagged with the
  constraint that kills it), a **tradeoff matrix** (options × criteria, every cell
  anchored to a citation), and a recommendation framed **"for reaction, not decision"** —
  often a phased path with the open choices handed back.
- **Deterministic visuals from a declarative source** — regenerated, never hand-edited,
  so no fact lives only inside a diagram.

### Tier 2 — two of three efforts built this

- **Findings / review register** — a recorded, dated artifact that gates circulation
  (stable IDs, severity, status enum, append-only resolution notes), optionally fed by
  **multiple concurrent reviewer agents, each a distinct lens** (standards, security,
  red-team…), with "closed via alternate path" recording when advice was not taken.
- **Producer/checker agent separation** (`.claude/agents/`): pull ≠ synthesize ≠ write ≠
  check; the checker may not edit what it checks.
- **A `METHODOLOGY.md` companion** — how the recommendation was produced and how to
  reproduce it on a new program.
- **Audience/altitude document tiers** — research → analysis → deliverables → preso;
  only the top tier circulates; the recommendation is identical at every level.
- **`artifacts/` staging convention** *(no schema change)* — raw inputs land git-ignored;
  only sanitized `source` notes enter the bundle. Ships with hardened `.gitignore`.
- **Companion / adjacent-repo convention** — import a sibling effort's findings as
  `source` notes (`source_type: internal-doc`) rather than duplicating its analysis.

### Tier 3 — strong single-effort ideas

- **New `type:` values + templates + `validate.py` rules:** `option`, `criterion`,
  `gate` (decision-gate register), `finding`, `risk`, `recommendation`, `interface-memo`.
- **Standing evaluation rubric** — a re-runnable scorecard (Met / Partial / Gap / N/A),
  appended each iteration rather than overwritten.
- **Source-class-partitioned evidence** + a slug citation log with **dual-date discipline**
  (source's own "last updated" plus retrieval date).
- **`visual-vocabulary` design-system concept** — CVD-safe, colour encodes ownership only,
  shape/line lexicon, tiered Mermaid → SVG → pptx pipeline.

## Cross-cutting conventions

- **Append-only registers** — never edit a closed gate/finding/risk row; append a dated
  resolution note. The change history is the audit trail.
- **Confidence = feasibility, not desirability** — rate whether a mechanism works, kept
  separate from whether anyone should want it.
- **Recommendation "for reaction, not decision"** — publish the decision frame and a
  phased path; hand the genuinely-open choices back rather than pretending to close them.
- **Strength-of-evidence travels with each claim** (Strong / Moderate / Weak + reason).
- **Absence-of-evidence is an explicit finding** — marked separately from positive evidence.

## Phasing

1. **No-schema-change first:** `preso/` scaffold, `artifacts/` + `.gitignore`, and a
   decision-support runbook encoding the Tier-1 recommendation pattern.
2. **Extend the schema:** new `type:` values + templates + `validate.py` enforcement;
   `METHODOLOGY.md`.
3. **Agent + design layers:** `.claude/agents/` producer/checker + multi-lens review;
   `visual-vocabulary` concept.

Each phase must keep the decision-support layer **optional and deletable**, so a pure
knowledge-capture effort can clone the template and ignore it.

## Sources

- None yet. Synthesized from a first-party review of three private efforts built on
  clones of this template (anonymized; not part of this public template); stays `draft`
  until the extension is designed and built. See
  [ADR-0006](../decisions/0006-decision-support-extension.md).
