---
# --- OKF v0.1 ---
type: option
title: "EXAMPLE: Managed Postgres"
description: Deletable worked option — rent a managed SQL database from the cloud provider.
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
id: OPT-1
decision: ../recommendations/EXAMPLE-datastore-recommendation.md
viable: yes
ruled_out_by:
---

# EXAMPLE: Managed Postgres

> **Deletable worked example** (illustrative fiction, no real vendor cited — that is why it
> stays `draft` / `confidence: low` / empty `sources`). One option of the
> [datastore recommendation](../recommendations/EXAMPLE-datastore-recommendation.md);
> mirrors Option A of the Phase-1 [architecture example](../architecture/EXAMPLE-datastore-options.md).

- **Thesis** — rent a standard SQL database; let the provider run it.
- **Configures** — a provider-managed Postgres instance + automated backups.
- **Retires** — [time-to-first-write], [operational load].
- **Does not retire** — [cost at low scale] (a floor price), [reversibility](../criteria/EXAMPLE-reversibility.md) (some provider glue).
- **Cost** — low–medium, always-on.
- **Governance / operational load** — low; the provider patches and pages.
- **Risk** — low; standard engine, portable schema. See [RISK-1](../risks/EXAMPLE-serverless-lockin.md) (attaches to the serverless option, not this one).
- **Why viable** — standard SQL, portable schema, minimal ops.

## Evidence

- *Illustrative only.* In a real option every load-bearing claim (e.g. "portable schema")
  would be marked Strong / Moderate / Weak with a reason and linked to a `source` note.
  This example cites none, by design.

## Sources

- None. Illustrative fiction; makes no verifiable claims.
