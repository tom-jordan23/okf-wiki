---
# --- OKF v0.1 ---
type: recommendation      # decision-support type (extension); one recommendation per decision
title: ""
description: ""
tags: [recommendation, decision-support]
timestamp: YYYY-MM-DD
# --- integrity extension (NOT part of OKF) ---
status: draft
confidence: low
created: YYYY-MM-DD
last_verified:
verified_by:
review_by: YYYY-MM-DD
sources: []
# --- decision-support fields ---
id: REC-N                # stable cross-reference handle (OKF identity is still the path)
decision:                # one-line statement of the decision this recommends on (or link its frame)
options: []              # the option ids/links weighed, e.g. [OPT-1, OPT-2, OPT-3]
---

# 

> The decision, in one line, and who decides.

## Frame

What is being decided, who decides, and — explicitly — **what this is *not*** (the scope
boundary). Link the [criteria](../criteria/a-criterion.md) and [options](../options/an-option.md) weighed.

## Tradeoff matrix

Options × criteria. Every non-trivial cell is anchored to evidence (a link to a `source`
or an option's Evidence section); an unanchored cell is a placeholder, marked as one.

| Criterion | OPT-1 | OPT-2 | OPT-3 |
|-----------|:-----:|:-----:|:-----:|
| CRIT-1    |       |       |       |

## Recommendation (for reaction, not decision)

A **phased path** — now / next / later — not a single forced pick. Show a reviewer-proposed
option evaluated fairly and *then* set aside, never dismissed unheard.

## Open decisions

> This heading is required for a recommendation. "For reaction, not decision" means the
> genuinely-open choices are handed **back** to the reviewer, not silently closed.

1. <open choice the reviewer must make>
2. <the threshold / trigger that should reopen this>

## Sources

- [source](../sources/the-source.md) — evidence behind the matrix and the phased path.
