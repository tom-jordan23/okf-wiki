---
# --- OKF v0.1 ---
type: runbook
title: "Stand Up the Leadership-Chat Proof of Concept (Phase 1)"
description: How to prove the provider-agnostic agentic-navigation loop answers from the bundle while preserving the integrity chain, before any UI or hosting.
tags: [runbook, interface, poc]
timestamp: 2026-07-06
# --- integrity extension (NOT part of OKF) ---
status: draft
confidence: medium
created: 2026-07-06
last_verified:
verified_by:
review_by: 2027-01-06
sources:
  - ../decisions/0003-leadership-chat-interface.md
  - ../sources/0003-claude-agent-sdk.md
  - ../sources/0002-litellm.md
---

# Stand Up the Leadership-Chat Proof of Concept (Phase 1)

> Phase 1 of [ADR-0003](../decisions/0003-leadership-chat-interface.md). Prove — headless,
> no UI, no hosting — that an agentic read/grep loop over the `okf/` bundle answers
> leadership-style questions **and keeps the integrity chain**: real note-level citations,
> honest `status`, and grounded facts kept separate from inference. This exists to de-risk
> the design before any UI is built; its question set is the seed of the phase-4 eval gate.

## Prerequisites

- A local **git checkout of `okf/`**, mounted read-only for the agent.
- **One runnable LLM** reachable through a gateway's OpenAI-format API. It need **not** be
  the final institutionally-approved model — any model you can legitimately call today
  (dev key or self-hosted) is enough to prove the loop. Certifying the *approved* model is
  phase 4, not here.
- Read / list / grep tooling scoped to the checkout (see step 2).
- The integrity system prompt (step 3).

## Steps

1. **Point at a read-only checkout of `okf/`.** The agent only ever reads; freshness later
   comes from `git pull` (ADR decision 5).
2. **Give the model navigation tools scoped to `okf/`.** Read, list/glob, grep — nothing
   that writes.
   - *If Claude is the model you're testing with:* the
     [Claude Agent SDK](../sources/0003-claude-agent-sdk.md) supplies this loop out of the
     box — `allowed_tools=["Read", "Glob", "Grep"]`.
   - *Otherwise:* a generic tool-use loop over the gateway's OpenAI-format API. Keep the
     loop provider-agnostic (ADR decision 1) — the Agent SDK is a Claude-only accelerator,
     never a dependency.
3. **Load the integrity system prompt.** It must require the model to: cite the note
   path(s) each claim rests on; surface each cited note's `status`; default to `verified`
   notes and explicitly flag when support is only `draft` / `disputed` / `stale`; separate
   facts grounded in notes from its own inference; and **never invent a source** — no
   citation without a real note behind it.
4. **Route model calls through the gateway** ([LiteLLM](../sources/0002-litellm.md) interim,
   or the platform team's shared service) even in the POC, so model choice and cost stay
   centralized and swapping models is config, not code (ADR decision 3).
5. **Run a fixed probe set** covering the behaviors that matter — at minimum one of each:
   - **Verified lookup** — a fact backed by a `verified` note. *Expect:* correct answer
     citing that note's path.
   - **Draft-only topic** — a claim supported only by a `draft` note. *Expect:* answered
     but explicitly flagged provisional / unverified.
   - **Scenario planning** — an open-ended "what if". *Expect:* grounded facts cited to
     notes, and the generative/inferred part clearly labeled as inference.
   - **Unsupported question** — something the bundle has no note for. *Expect:* the model
     says so and declines — it must **not** fabricate a citation.
6. **Read the transcripts, don't just eyeball the answers.** For each probe, confirm every
   claimed citation resolves to a real note path, statuses are surfaced honestly, and
   inference is labeled. Save the probe set + expected behaviors — this becomes the phase-4
   eval fixture.

## Verification

- All four probe types behave as specified above.
- **Zero fabricated citations** — every cited path exists in the checkout.
- The unsupported question is declined, not answered with an invented source.
- Draft/stale support is never presented as settled fact; inference is never presented as
  grounded.

## Rollback / recovery

If the model fabricates citations, launders `draft` support into confident fact, or blurs
inference into grounded claims: **do not advance to phase 2.** Tighten the system prompt,
narrow the answer scope, or fall back to whole-bundle-in-context (ADR alternative). If a
weaker model simply cannot hold these behaviors, that is a **model-capability finding** that
feeds the approved-model eval gate (phase 4) — record it; do **not** relax the integrity
rules to make the POC pass.

## Sources

- [ADR-0003: Leadership chat interface](../decisions/0003-leadership-chat-interface.md) —
  the design this procedure executes (phase 1).
- [Claude Agent SDK](../sources/0003-claude-agent-sdk.md) — the built-in read/grep loop and
  `allowed_tools` scoping, used only in the Claude case.
- [LiteLLM](../sources/0002-litellm.md) — the gateway the POC routes model calls through.
