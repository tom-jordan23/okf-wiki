---
# --- OKF v0.1 ---
type: finding             # decision-support type (extension); one review finding per note
title: ""
description: ""
tags: [finding, decision-support]
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
id: FND-N                # stable cross-reference handle (OKF identity is still the path)
state: open              # open | resolved | closed-alternate | wontfix  (append-only)
severity: medium         # low | medium | high | critical
lens:                    # optional: which review lens raised it — standards | security | red-team | integrity
---

# 

> One line: what the review found.

## Finding

What is wrong or missing, where, and why it matters. Point at the specific note / option /
claim it lands on (link it). A finding with no target is an opinion.

## Recommendation

What would resolve it. Keep it separable from the finding itself so the finding can stand
even if the fix changes.

## Resolution log (append-only)

Never edit or delete an entry — append a new dated line.

- **YYYY-MM-DD** — raised (severity, lens).
- **YYYY-MM-DD** — resolved / closed-alternate / wontfix. <what was done, by whom, or why
  the advice was deliberately not taken — "closed via alternate path" is a legitimate,
  recorded outcome, not a silent drop>.

## Sources

- [source](../sources/the-source.md) — evidence the finding rests on, if any.
