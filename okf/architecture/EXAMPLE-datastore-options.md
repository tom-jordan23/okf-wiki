---
# --- OKF v0.1 ---
type: architecture
title: "EXAMPLE: Datastore options for a new service"
description: A domain-neutral worked example of the decision-support pattern — delete when starting a real effort.
tags: [architecture, decision-support, example]
timestamp: 2026-07-23
# --- integrity extension (NOT part of OKF) ---
status: draft
confidence: low
created: 2026-07-23
last_verified:
verified_by:
review_by: 2027-01-23
sources: []
---

# EXAMPLE: Datastore options for a new service

> **This is a deletable worked example** showing the [decision-support runbook](../runbooks/run-a-decision-support-effort.md)
> in action. The scenario and every number below are **illustrative fiction** — no real
> product, benchmark, or vendor is cited (which is exactly why this note stays `draft`
> with `confidence: low` and empty `sources`: it makes no verified claims). Delete it, and
> copy its shape, when you start a real effort.
>
> This is the **Phase-1 form** — the whole decision as sections in one `architecture` note.
> The same decision split into **Phase-2 first-class notes** (one per option/criterion/gate/
> finding/risk, tied together by a `recommendation`) is
> [EXAMPLE: Datastore recommendation](../recommendations/EXAMPLE-datastore-recommendation.md).
> Both forms are valid; pick one per decision.

## Frame

- **Decision:** which datastore backs a new internal service at launch.
- **Decider:** the service's tech lead; reviewed by the platform team.
- **What this is *not*:** not a data-warehouse or analytics decision, and not a caching
  decision — transactional primary store only.

## Criteria

1. **Time-to-first-write** — how fast a small team gets a working store.
2. **Operational load** — who patches, backs up, and pages at 3am.
3. **Reversibility** — cost to migrate off later (lock-in).
4. **Cost at low scale** — spend in the first year at modest traffic.
5. **Scale headroom** — how far it stretches before a re-platform.

## Options

Each option uses the same fixed schema so none is under-examined.

### Option A — Managed Postgres (cloud provider)
- **Thesis:** rent a standard SQL database; let the provider run it.
- **Configures:** a provider-managed Postgres instance + automated backups.
- **Retires:** time-to-first-write, operational load.
- **Does not retire:** cost at low scale (a floor price), reversibility (some provider glue).
- **Cost:** low–medium, always-on. · **Governance/op load:** low. · **Risk:** low.
- **Why viable:** standard SQL, portable schema, minimal ops.

### Option B — Self-hosted Postgres (containers we run)
- **Thesis:** run the same engine ourselves for maximum control and portability.
- **Configures:** a container we deploy, patch, back up, and monitor.
- **Retires:** reversibility (fully portable), cost at low scale (no managed premium).
- **Does not retire:** operational load (it's now ours), time-to-first-write.
- **Cost:** low cash, higher staff time. · **Governance/op load:** high. · **Risk:** medium (self-run).
- **Why viable:** identical engine to A, zero managed lock-in.

### Option C — Serverless document/SQL store
- **Thesis:** a pay-per-request store that scales to zero.
- **Configures:** a provider API; no instance to size.
- **Retires:** cost at low scale (scale-to-zero), operational load, scale headroom.
- **Does not retire:** reversibility (proprietary API — highest lock-in).
- **Cost:** near-zero idle. · **Governance/op load:** low. · **Risk:** medium (lock-in).
- **Why viable:** cheapest at spiky low traffic; least ops.

## Ruled out

- **A single shared company database** — ruled out by the *scope-isolation* constraint
  (services must not share a schema). Failure mode: cross-service coupling and blast radius.
- **A brand-new/niche engine** — ruled out by the *team-familiarity* constraint. Failure
  mode: no in-house expertise to operate it under load.

## Tradeoff matrix

Cells are `✓ strong / ~ partial / ✗ weak`. In a real note each non-trivial cell links to a
`source` note; here they are illustrative and deliberately unlinked.

| Criterion             | A — Managed PG | B — Self-hosted PG | C — Serverless |
|-----------------------|:--------------:|:------------------:|:--------------:|
| Time-to-first-write   | ✓              | ~                  | ✓              |
| Operational load      | ✓              | ✗                  | ✓              |
| Reversibility         | ~              | ✓                  | ✗              |
| Cost at low scale     | ~              | ✓                  | ✓              |
| Scale headroom        | ~              | ~                  | ✓              |

## Recommendation (for reaction, not decision)

A **phased path**, not a single forced pick:

- **Now:** start on **Option A (managed Postgres)** — it retires the two criteria that
  matter most at launch (time-to-first-write, op load) with the least risk, and keeps
  schema portable.
- **Next:** if idle cost becomes the pain, evaluate **C** for the specific spiky workloads
  only — accepting its lock-in knowingly, not by default.
- **Later:** revisit **B** only if managed premium or data-residency needs force
  self-hosting; the portable schema from A keeps that door open.

**Open decisions handed back to the reviewer:**
1. Is provider lock-in (A's managed glue) acceptable, or is B's portability a hard
   requirement from day one?
2. What traffic threshold should *trigger* the "next" re-evaluation?

*(Reviewer-proposed option, evaluated then set aside: "just use the existing shared
database" — fair on time-to-first-write, but dominated once scope-isolation is a hard
constraint; see Ruled out.)*

## Sources

- None. Every figure here is illustrative fiction for teaching the pattern; the note makes
  no verifiable claims and is intentionally never promoted past `draft`.
