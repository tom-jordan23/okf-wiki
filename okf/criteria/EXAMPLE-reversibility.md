---
# --- OKF v0.1 ---
type: criterion
title: "EXAMPLE: Reversibility"
description: Deletable worked criterion — how cheaply can we back out of the datastore choice later?
tags: [criterion, decision-support, example]
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
id: CRIT-3
decision: ../recommendations/EXAMPLE-datastore-recommendation.md
weight: high
---

# EXAMPLE: Reversibility

> **Deletable worked example** (illustrative fiction). One criterion of the
> [datastore recommendation](../recommendations/EXAMPLE-datastore-recommendation.md).

## What "good" means

The cost — in engineering time and downtime — to migrate off this datastore onto another
later. Score high when the schema and query surface are portable (standard SQL, no
proprietary API); score low when the store's API is proprietary and pervasive, so leaving
means a rewrite.

- **Top of scale (✓ strong):** standard engine, portable schema, days-to-migrate.
- **Bottom (✗ weak):** proprietary API woven through the app, months-to-migrate.

## Why it matters here

At launch the team cannot predict scale or cost trajectory, so the ability to change stores
cheaply *later* is worth paying a little for *now*. This criterion discriminates the
managed/self-hosted SQL options (portable) from the serverless option (locked-in).

## Sources

- Self-sourced: a framing choice for this example decision. Makes no external claim.
