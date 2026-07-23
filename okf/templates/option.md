---
# --- OKF v0.1 ---
type: option              # decision-support type (extension); one evaluated option per note
title: ""
description: ""
tags: [option, decision-support]
timestamp: YYYY-MM-DD
# --- integrity extension (NOT part of OKF) ---
status: draft
confidence: low           # rates FEASIBILITY (does the mechanism work?), not desirability
created: YYYY-MM-DD
last_verified:
verified_by:
review_by: YYYY-MM-DD
sources: []
# --- decision-support fields ---
id: OPT-N                 # stable cross-reference handle (OKF identity is still the path)
decision:                # relative link to the recommendation / frame note this option serves
viable: yes              # yes | no  (no => it belongs in the ruled-out set)
ruled_out_by:            # the constraint that kills it, when viable: no
---

# 

> One-line thesis of this option.

Every option in a decision uses this same fixed schema so none is under-examined —
asymmetric depth is how a preferred option quietly wins.

- **Thesis** — one line.
- **Configures** — what it sets up.
- **Retires** — which criteria / pains it satisfies (link each: [CRIT-1](../criteria/a-criterion.md)).
- **Does not retire** — what it leaves open.
- **Cost** — cash + staff time.
- **Governance / operational load** — who runs, patches, pages.
- **Risk** — the main failure mode; link any [risk](../risks/a-risk.md).
- **Why viable** — why it clears the bar to be evaluated at all.

## Evidence

Load-bearing claims, each with strength-of-evidence (Strong / Moderate / Weak + one-line
reason) and an inline link to the `source` note it rests on. Absence-of-evidence is an
explicit finding, not a silent omission.

## Sources

- [source](../sources/the-source.md) — what it supports.
