---
# --- OKF v0.1 ---
type: risk                # decision-support type (extension); one risk per note
title: ""
description: ""
tags: [risk, decision-support]
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
id: RISK-N               # stable cross-reference handle (OKF identity is still the path)
state: open              # open | mitigated | accepted | realized | closed  (append-only)
likelihood: medium       # low | medium | high
impact: medium           # low | medium | high
---

# 

> One line: the thing that could go wrong.

## The risk

What could happen, the condition that triggers it, and what it costs if it does. Link the
option / decision it attaches to.

## Mitigation

What reduces likelihood or impact, and who owns it. If the plan is to **accept** the risk
knowingly, say so and say who accepted it — an accepted risk is a decision, not an
oversight.

## Resolution log (append-only)

Never edit or delete an entry — append a new dated line.

- **YYYY-MM-DD** — logged (likelihood / impact).
- **YYYY-MM-DD** — mitigated / accepted / realized / closed. <what changed, by whom>.

## Sources

- [source](../sources/the-source.md) — evidence for likelihood / impact, if any.
