---
# --- OKF v0.1 ---
type: gate
title: "EXAMPLE: Backup/restore proven before launch"
description: Deletable worked gate — the datastore choice cannot ship until a restore is demonstrated.
tags: [gate, decision-support, example]
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
id: GATE-1
state: open
decision: ../recommendations/EXAMPLE-datastore-recommendation.md
owner: service tech lead
---

# EXAMPLE: Backup/restore proven before launch

> **Deletable worked example** (illustrative fiction). A decision gate on the
> [datastore recommendation](../recommendations/EXAMPLE-datastore-recommendation.md).

## The gate

Launch is blocked until a **full restore from backup has been demonstrated** into a clean
environment, with the measured restore time recorded. "Backups are configured" is not the
pass condition — a restore actually completing is.

## Resolution log (append-only)

- **2026-07-23** — opened. Blocks go-live for any option chosen. Owner: service tech lead.

## Sources

- None. Illustrative fiction.
