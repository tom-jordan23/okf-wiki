---
# --- OKF v0.1 ---
type: option
title: "EXAMPLE: Shared company database (ruled out)"
description: Deletable worked option showing the ruled-out mechanic — viable no, killed by a constraint.
tags: [option, decision-support, example]
timestamp: 2026-07-23
# --- integrity extension (NOT part of OKF) ---
status: draft
confidence: low
created: 2026-07-23
last_verified:
verified_by:
review_by: 2027-01-23
sources: []
# --- decision-support fields ---
id: OPT-4
decision: ../recommendations/EXAMPLE-datastore-recommendation.md
viable: no
ruled_out_by: scope-isolation (services must not share a schema)
---

# EXAMPLE: Shared company database (ruled out)

> **Deletable worked example** (illustrative fiction). Shows an option in the **ruled-out
> set**: recorded with `viable: no` and the constraint that kills it, so it doesn't
> resurface later as "did you consider just using the shared DB?".

- **Thesis** — reuse the existing shared company database; write no new store.
- **Configures** — a schema inside the shared instance.
- **Retires** — [time-to-first-write] (nothing to stand up).
- **Does not retire** — [reversibility](../criteria/EXAMPLE-reversibility.md); creates cross-service coupling.
- **Ruled out by** — the **scope-isolation** constraint: services must not share a schema.
- **Failure mode** — cross-service coupling and a shared blast radius; a schema change for
  one service can break another.

*(Evaluated fairly, then set aside — fair on time-to-first-write, dominated once
scope-isolation is a hard constraint. A dominated option is walked through, not dismissed.)*

## Sources

- None. Illustrative fiction; makes no verifiable claims.
