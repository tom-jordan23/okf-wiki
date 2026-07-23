---
# --- OKF v0.1 ---
type: runbook
title: "Run a Decision-Support Effort"
description: The repeatable options→criteria→matrix→phased-recommendation procedure, kept inside OKF with provenance intact.
tags: [runbook, decision-support]
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

# Run a Decision-Support Effort

> How to take a decision from "here are some options" to a phased recommendation a
> reviewer can react to — **without** leaving the OKF rails or losing provenance. This is
> the Phase-1 (no-schema-change) form of the [decision-support extension](../architecture/decision-support-extension.md):
> options, criteria, and the recommendation live as **sections inside ordinary
> `architecture` notes**. A later phase promotes them to first-class note types.

## When to run this

You have a decision with more than one viable path and a reviewer who must choose. Use it
for vendor/tool selection, an architecture direction, a build-vs-buy call — anything where
the value is a *defensible recommendation*, not a single fact.

## Prerequisites

- You can name the decision in one sentence and say who decides.
- You have (or can gather) evidence for the claims each option will rest on. Raw inputs go
  in git-ignored [`artifacts/`](../../artifacts/README.md); only sanitized `source` notes
  enter the bundle.

## Steps

1. **Frame the decision.** Start an `architecture` note (copy `../templates/architecture.md`).
   State the decision, who decides, and — explicitly — **what this is *not*** (the scope
   boundary). Vague scope is the most common way a recommendation drifts.

2. **Name the criteria.** List the evaluation criteria as a numbered set, each with what
   "good" means (e.g. *reversibility — how cheaply can we back out?*). Criteria are the
   columns of your matrix later, so fix them before scoring anything.

3. **Enumerate the options.** Give **every** option the same fixed schema so none is
   under-examined (a real anti-bias rule — asymmetric depth is how a preferred option
   quietly wins):

   > **Thesis** — one line. · **Configures** — what it sets up. · **Retires** — which
   > criteria/pains it satisfies. · **Does not retire** — what it leaves open. ·
   > **Cost** · **Governance/operational load** · **Risk** · **Why viable**.

4. **Record the ruled-out set.** Options eliminated up front go in their own list, each
   tagged with **the constraint that kills it** and its failure mode — so they don't
   resurface later as "did you consider…".

5. **Score the tradeoff matrix.** Build an options × criteria table. Every non-trivial
   cell is **anchored to evidence** — an inline link to a `source` note or an analysis
   section. A cell with no anchor is a placeholder; mark it as one.

6. **Write the recommendation — for reaction, not decision.** Publish the *decision frame*
   and a **phased path** (now / next / later), not a single forced pick. Hand the
   genuinely-open choices back as an explicit **"open decisions"** list. If a
   reviewer-proposed option is dominated, show it evaluated fairly and *then* dominated —
   as a walk-through, not a dismissal.

7. **Wire it up.** Add the note to `../architecture/index.md`, and a line to `../log.md`.
   Optionally render a leadership deck from the note via [`preso/`](../../preso/README.md)
   (every slide claim must trace back to this note).

## Verification

- **Feasibility ≠ desirability.** `confidence` on each option rates whether the mechanism
  *works*, kept separate from whether anyone should *want* it. Don't conflate them.
- **Strength-of-evidence travels with each claim** — mark load-bearing claims Strong /
  Moderate / Weak with a one-line reason.
- **Absence-of-evidence is a finding.** "We looked and found nothing" is recorded
  explicitly, not silently omitted — it is often the load-bearing signal.
- **Provenance holds end to end.** Every score, verdict, and recommendation links to the
  `source`/analysis it rests on; the note's `sources:` frontmatter lists them; the note is
  not `verified` until those sources are actually checked (see
  [Add and Verify a Note](add-and-verify-a-note.md)).
- `python3 scripts/validate.py` passes with no new warnings.

## Rollback / recovery

If the evidence is not there yet, **do not** manufacture a recommendation. Publish the
decision frame with the recommendation section held as *"to be filled in once evidence
lands,"* and keep the note `draft`. A named, honest gap beats a confident guess.

## Sources

- None. This procedure documents this template's own decision-support workflow;
  self-sourced. A worked, domain-neutral example is
  [EXAMPLE: Datastore options](../architecture/EXAMPLE-datastore-options.md).
