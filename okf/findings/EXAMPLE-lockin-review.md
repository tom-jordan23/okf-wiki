---
# --- OKF v0.1 ---
type: finding
title: "EXAMPLE: Serverless lock-in understated in the matrix"
description: Deletable worked finding — a red-team lens flags that the matrix soft-pedals lock-in.
tags: [finding, decision-support, example]
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
id: FND-1
state: open
severity: high
lens: red-team
---

# EXAMPLE: Serverless lock-in understated in the matrix

> **Deletable worked example** (illustrative fiction). A review finding against the
> [datastore recommendation](../recommendations/EXAMPLE-datastore-recommendation.md).

## Finding

The tradeoff matrix scores the serverless option `~` on reversibility, but its proprietary
API is pervasive enough to warrant `✗`. Understating this makes the "Next: evaluate
serverless" phase look cheaper to reverse than it is. Lands on
[CRIT-3 reversibility](../criteria/EXAMPLE-reversibility.md) and the serverless option.

## Recommendation

Rescore serverless to `✗` on reversibility, and make the "accept its lock-in knowingly"
caveat explicit in the phased path. Tracked separately as [RISK-1](../risks/EXAMPLE-serverless-lockin.md).

## Resolution log (append-only)

- **2026-07-23** — raised (severity: high, lens: red-team).

## Sources

- None. Illustrative fiction.
