---
# --- OKF v0.1 ---
type: gate                # decision-support type (extension); one decision gate per note
title: ""
description: ""
tags: [gate, decision-support]
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
id: GATE-N               # stable cross-reference handle (OKF identity is still the path)
state: open              # open | closed | closed-alternate  (append-only — never rewrite a closed gate)
decision:                # relative link to the decision / recommendation this gate guards
owner:                   # optional: who owns closing it
---

# 

> One line: the question this gate must answer before the effort proceeds.

## The gate

What must be true (or decided) to pass. State the pass condition precisely enough that
"is it closed?" is not a judgment call.

## Resolution log (append-only)

Never edit or delete an entry — append a new dated line. The change history is the audit
trail; a rewritten gate is a lost one.

- **YYYY-MM-DD** — opened. <what is blocked until it closes>
- **YYYY-MM-DD** — closed / closed-alternate. <the decision taken, and by whom>. Use
  **closed-alternate** when the effort proceeded by a different path than the gate
  originally contemplated — record what path, so "we didn't do what the gate said" is
  visible, not buried.

## Sources

- [source](../sources/the-source.md) — evidence the pass condition rests on, if any.
