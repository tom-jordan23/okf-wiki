---
# --- OKF v0.1 ---
type: risk
title: "EXAMPLE: Serverless API lock-in blocks a later move"
description: Deletable worked risk — choosing serverless makes a later re-platform expensive.
tags: [risk, decision-support, example]
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
id: RISK-1
state: open
likelihood: medium
impact: high
---

# EXAMPLE: Serverless API lock-in blocks a later move

> **Deletable worked example** (illustrative fiction). A risk attached to the serverless
> option of the [datastore recommendation](../recommendations/EXAMPLE-datastore-recommendation.md).

## The risk

If the "Next" phase adopts the serverless store for spiky workloads and its proprietary API
spreads through the app, a later migration to standard SQL becomes a multi-month rewrite.
Trigger: serverless usage growing past the narrow spiky-workload carve-out it was chosen for.

## Mitigation

Fence serverless behind a thin internal interface so its API doesn't leak app-wide; review
usage at the "Next → Later" boundary. If the team chooses to **accept** the lock-in for the
carve-out, record who accepted it here — an accepted risk is a decision, not an oversight.
Related: [FND-1](../findings/EXAMPLE-lockin-review.md).

## Resolution log (append-only)

- **2026-07-23** — logged (likelihood: medium, impact: high).

## Sources

- None. Illustrative fiction.
