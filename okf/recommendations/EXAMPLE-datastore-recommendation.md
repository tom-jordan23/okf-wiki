---
# --- OKF v0.1 ---
type: recommendation
title: "EXAMPLE: Datastore recommendation"
description: Deletable worked recommendation — a phased datastore path, framed for reaction not decision.
tags: [recommendation, decision-support, example]
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
id: REC-1
decision: Which datastore backs a new internal service at launch.
options: [OPT-1, OPT-4]
---

# EXAMPLE: Datastore recommendation

> **Deletable worked example** (illustrative fiction — every figure is made up, which is why
> this stays `draft` / `confidence: low` / empty `sources`). This is the **first-class-note**
> form of the Phase-1 [architecture example](../architecture/EXAMPLE-datastore-options.md):
> the same decision, now split into linked [option](../options/index.md),
> [criterion](../criteria/index.md), [gate](../gates/index.md), [finding](../findings/index.md),
> and [risk](../risks/index.md) notes. Delete the whole worked set when you start a real effort.

## Frame

- **Decision:** which datastore backs a new internal service at launch.
- **Decider:** the service's tech lead; reviewed by the platform team.
- **What this is *not*:** not a data-warehouse/analytics decision, and not a caching
  decision — transactional primary store only.
- **Options weighed:** [OPT-1 Managed Postgres](../options/EXAMPLE-datastore-managed-pg.md),
  self-hosted Postgres, and a serverless store; ruled out —
  [OPT-4 shared company DB](../options/EXAMPLE-datastore-shared-db.md).
- **Criteria:** time-to-first-write, operational load,
  [CRIT-3 reversibility](../criteria/EXAMPLE-reversibility.md), cost at low scale, scale headroom.

## Tradeoff matrix

Cells are `✓ strong / ~ partial / ✗ weak`; illustrative and deliberately unlinked here (a real
matrix anchors each non-trivial cell to a `source`).

| Criterion            | OPT-1 Managed PG | Self-hosted PG | Serverless |
|----------------------|:----------------:|:--------------:|:----------:|
| Time-to-first-write  | ✓                | ~              | ✓          |
| Operational load     | ✓                | ✗              | ✓          |
| Reversibility        | ~                | ✓              | ✗ *(see [FND-1](../findings/EXAMPLE-lockin-review.md))* |
| Cost at low scale    | ~                | ✓              | ✓          |
| Scale headroom       | ~                | ~              | ✓          |

## Recommendation (for reaction, not decision)

- **Now:** start on **[OPT-1 Managed Postgres](../options/EXAMPLE-datastore-managed-pg.md)** —
  it retires the two criteria that matter most at launch with the least risk, and keeps the
  schema portable. Blocked by [GATE-1](../gates/EXAMPLE-datastore-launch-gate.md) (prove a
  restore before go-live).
- **Next:** if idle cost becomes the pain, evaluate serverless for the spiky workloads only,
  accepting [RISK-1 lock-in](../risks/EXAMPLE-serverless-lockin.md) *knowingly* — not by default.
- **Later:** revisit self-hosted only if a managed premium or data-residency need forces it;
  the portable schema from OPT-1 keeps that door open.

## Open decisions

1. Is provider lock-in (OPT-1's managed glue) acceptable, or is full portability a hard
   day-one requirement?
2. What traffic threshold should *trigger* the "Next" re-evaluation?

## Sources

- None. Illustrative fiction for teaching the pattern; makes no verifiable claims.
