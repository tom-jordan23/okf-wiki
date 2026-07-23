---
# --- OKF v0.1 ---
type: criterion           # decision-support type (extension); one evaluation criterion per note
title: ""
description: ""
tags: [criterion, decision-support]
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
id: CRIT-N               # stable cross-reference handle (OKF identity is still the path)
decision:                # relative link to the recommendation / frame note this criterion serves
weight: medium           # optional: high | medium | low — how much this criterion counts
---

# 

> One line: what this criterion measures.

## What "good" means

Define the criterion so two people would score an option the same way — e.g.
*reversibility: how cheaply can we back out later?* State the scale you score on and
what the top and bottom of it look like.

## Why it matters here

Tie the criterion to the decision it serves. A criterion nobody would trade on is noise;
say what it discriminates between.

## Sources

- Self-sourced (a framing choice for this decision), or link the [source](../sources/the-source.md)
  that makes this a real constraint.
