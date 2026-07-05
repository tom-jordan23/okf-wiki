---
# --- OKF v0.1 ---
type: decision
title: "Leadership chat interface over the knowledge bundle"
description: A simple hosted web chat that answers from the bundle via provider-agnostic agentic navigation, preserves note-level provenance, and routes through a gateway for cost control and institutionally-approved-model portability.
tags: [adr, interface, rag, llm]
timestamp: 2026-07-05
# --- integrity extension (NOT part of OKF) ---
status: draft
confidence: medium
created: 2026-07-05
last_verified:
verified_by:
review_by: 2027-01-05
sources:
  - ../sources/okf-v0-1-spec.md
  - ../sources/0002-litellm.md
  - ../sources/0003-claude-agent-sdk.md
---

# ADR-0003: Leadership Chat Interface over the Knowledge Bundle

- **Status:** proposed
- **Date:** 2026-07-05
- **Deciders:** project owner

## Context

Leadership needs a way to query the project's knowledge base conversationally —
ask questions, get explanations on any topic, and run scenario planning — without
touching a terminal, a repo, or the raw Markdown. The target experience is a single
sentence handed to a non-technical audience: *"If you have questions, we've set up this
LLM-accessible knowledge source for the project at this URL."*

The forces at play:

- **Trust must survive the interface.** The bundle's value is that every claim-bearing
  note carries structured provenance — `status`, `confidence`, `sources`, `review_by`
  (see [frontmatter schema](../concepts/okf-frontmatter-schema.md)). A chat front-end
  that answers in confident prose while discarding that provenance would *launder* the
  integrity we deliberately built. The interface must inherit the integrity chain, not
  erase it.
- **The bundle is already navigable.** OKF v0.1's design — `index.md` progressive
  disclosure plus relative cross-links ([OKF spec](../sources/okf-v0-1-spec.md)) —
  makes `okf/` a filesystem an agent can traverse directly (read the index, follow
  links, grep, read the note). This is the same read/navigate loop a coding agent
  already performs over this repo.
- **Audience is non-technical.** Dead-simple, clean web UI. No terminal, no Git, no
  Markdown. One authenticated URL.
- **Cost and model choice must be governed centrally**, on the backend, not baked into
  the app or exposed to users.
- **The model must be an institutionally-approved LLM, and the approved set is not yet
  fixed.** The design cannot hard-depend on any single provider or model family. It must
  run on whatever the institution sanctions — a hosted model under agreement (Claude or
  otherwise) or a self-hosted open-weight model with no data egress — and tolerate that
  choice changing later.
- **A platform team is building a shared AI gateway service** to proxy LLM traffic, built
  on **LiteLLM** and **MCP** *(internal roadmap, 2026-07-05 — not externally verifiable)*.
  We should build to consume that service rather than duplicate it, without blocking on
  it while it is in progress.

## Decision

Build a **minimal hosted web chat** backed by an **agentic navigation** loop over a
Git checkout of the `okf/` bundle, with model access mediated by a **gateway** for cost
control. Specifically:

1. **Retrieval = agentic navigation, not an embedding/vector pipeline** — at the
   current corpus scale. The model is given read/list/grep tools scoped to a checkout of
   `okf/` and navigates via `index.md` and relative links. Rationale: exact citations
   (the model read the actual file), provenance is in-context (frontmatter travels with
   the note), no embedding/re-index infrastructure, and freshness is just `git pull`.
   Revisit embeddings only if the corpus outgrows reliable link-navigation (see Open
   questions). **The loop is provider-agnostic** — it is an ordinary tool-use loop over
   the [gateway](../sources/0002-litellm.md)'s OpenAI-format API, so it runs on whatever
   approved model answers. *If* Claude turns out to be the approved model, the
   **[Claude Agent SDK](../sources/0003-claude-agent-sdk.md)** supplies exactly this loop
   pre-built (built-in `Read` / `Glob` / `Grep`, automatic agent loop, read-only scoping
   via `allowed_tools`), saving the harness work; that SDK is a Claude-only accelerator,
   **not** a foundation the design may depend on.
2. **Answers preserve the integrity chain.** The system prompt requires the model to:
   cite the note path(s) each claim rests on; surface each cited note's `status`;
   **default to `verified` notes** and explicitly flag when support is only `draft` /
   `disputed` / `stale`; and **separate facts grounded in notes from its own
   inference** — critical for scenario planning, which is generative by nature. The
   `CLAUDE.md` rule *"never invent a source"* extends to runtime: no citation without a
   real note behind it.
3. **Model access via a gateway — also the compliance boundary.** The app talks to a
   **gateway** for model access, so model selection, API keys, rate limits (virtual keys),
   and **token / cost accounting** (per-key/team/user spend tracking) live on the backend,
   decoupled from the app and swappable without touching the UI. The gateway is an
   **interface, not a specific instance**: it can be our own
   **[LiteLLM](../sources/0002-litellm.md)** deployment (MIT-licensed, self-hostable) *or*
   the **platform team's shared AI gateway service** (itself LiteLLM-based) once available
   — the app targets the same OpenAI-format API either way, so consuming theirs is a
   configuration change, not a rewrite. Prefer consuming the shared service; self-host
   only as an interim while it is in progress. The gateway also satisfies the
   **institutionally-approved-LLM** constraint: LiteLLM fronts Azure OpenAI, AWS Bedrock,
   Google Vertex AI, self-hosted open-weight models (vLLM / Ollama / any OpenAI-compatible
   endpoint), and Anthropic, all behind one API — so the approved model is a backend config
   choice, and a self-hosted route keeps data inside the institutional boundary.
   [LiteLLM](../sources/0002-litellm.md)
4. **Interface: a single authenticated web URL.** Clean chat UI, no terminal. Auth
   gates who counts as "leadership."
5. **Freshness via `git pull`** on a schedule or a merge webhook; Git remains the single
   source of truth, the running service only ever reads a checkout.
6. **Stay MCP-compatible so the bundle can ride the platform gateway.** Keep the
   bundle-navigation capability (read / list / grep over the `okf/` checkout) packaged so
   it can be exposed as an **MCP server**, not welded into the app. A LiteLLM-based gateway
   is also an **MCP Gateway** — "a fixed endpoint for all MCP tools" with permission
   management by key / team / organization ([LiteLLM](../sources/0002-litellm.md)) — so an
   `okf/` MCP server could register behind the platform team's gateway and be governed
   through the same control point as model traffic. This also turns the knowledge base into
   a **reusable capability** other approved agents can consume, not a single-purpose chat
   backend. Treat this as a door to leave open, not a phase-1 commitment: the phase-1 proof
   of concept can call read/grep tools directly and be refactored behind MCP later.

## Consequences

- **Easier:** trustworthy answers with traceable, note-level citations; central control
  over model choice and token spend; a URL simple enough to hand to anyone.
- **Harder:** we now own a hosted, authenticated web app (deploy, secure, maintain);
  we must build **runtime guardrails and an eval set** to protect the grounding rule at
  answer time, not just at curation time; the gateway is another component to run.
- **Committed to:** the backend reads from a bundle checkout (source of truth stays in
  Git); a **provider-agnostic app boundary** — the app talks only to the gateway's
  OpenAI-format API, never a provider SDK directly, so no approved-model choice is baked
  in; the integrity extension becoming a *runtime* contract, not only a curation
  convention.
- **Caveat — integrity depends on model capability.** The integrity behaviours (accurate
  note-level citation, `status`-awareness, separating grounded facts from inference)
  lean on the model's instruction-following and agentic ability. A weaker self-hosted
  model may degrade them, so the eval gate (phase 4) is what certifies a given approved
  model as good enough — and may push a low-capability model toward the whole-bundle
  fallback or a smaller answer scope.

## Alternatives considered

- **Embedding / vector RAG now** — the reflex architecture. Premature at this corpus
  scale: weaker citation fidelity (chunk offsets vs. real files), a re-index burden on
  every change, and infrastructure that buys nothing until the bundle is far larger.
  Deferred, not rejected — it is the documented upgrade path.
- **Load the whole bundle into context each turn (no retrieval)** — viable while the
  bundle is tiny and simplest of all, but wastes tokens and stops scaling. Navigation
  is the more durable default; whole-context can be a fallback for very small bundles.
- **Direct provider SDK, no gateway** — fewer moving parts, but forfeits the central
  token/cost governance the owner explicitly wants. Rejected.
- **Off-the-shelf "chat with your docs" SaaS** — fastest to stand up, but cannot honor
  the integrity extension (status-aware answering, note-level provenance) and hands the
  corpus to a third party. Rejected.

## Rollout (phased)

1. **Proof of concept** — agentic loop + integrity system prompt over a local checkout,
   run headless. Prove the citation / provenance behavior before any UI.
2. **Thin hosted chat** — minimal authenticated web UI; backend holds the checkout and
   `git pull`s; model calls through the gateway.
3. **Integrity UX** — render citations as clickable note links with a `status` badge;
   add a "verified-only" answering toggle.
4. **Guardrails & eval** — a question → expected-sources eval set to catch ungrounded
   assertions; wire into CI alongside `scripts/validate.py` (see the Roadmap in
   `CLAUDE.md`).

## Open questions

- **Hosting + auth**: where it runs and who is admitted — the largest non-LLM decision,
  and the gate on what "leadership access" means in practice.
- **Corpus size**: the real bundle's expected note count is the trigger for
  reconsidering embeddings (decision 1).
- **Approved model & channel** *(not yet determined — 2026-07-05)*: which LLM(s) the
  institution sanctions, and through what channel, fixes two things — (a) the data-egress
  posture (a cloud model under agreement vs a self-hosted model that keeps data on-prem),
  and (b) whether the [Claude Agent SDK](../sources/0003-claude-agent-sdk.md) accelerator
  is available (Claude approved) or the loop is built on the generic tool-use pattern.
  All candidate channels sit behind the [gateway](../sources/0002-litellm.md) either way.
  The eval gate (phase 4) then certifies the chosen model meets the integrity bar.
- **Gateway choice**: LiteLLM confirmed against its docs and repo — see
  [source](../sources/0002-litellm.md). Enterprise pricing is not yet verified (omitted
  from the source note); confirm with BerriAI if a paid tier is needed.
- **Scenario-plan outputs**: whether notable generated analyses get captured back into
  the bundle as `draft` notes for later verification.
- **Platform gateway — build vs. consume, and timing**: coordinate with the team building
  the shared LiteLLM + MCP AI gateway. Decide whether phase 2 consumes their service or
  runs an interim self-hosted LiteLLM, and confirm the OpenAI-format + MCP contract we
  build against matches theirs so the switch is a config change. (Their roadmap is internal
  and unverifiable here — track it with them, don't assume it.)

## Sources

- [OKF v0.1 specification](../sources/okf-v0-1-spec.md) — the progressive-disclosure
  (`index.md`) and relative-link design that makes agentic navigation of the bundle
  viable without an embedding layer.
- [LiteLLM](../sources/0002-litellm.md) — the gateway's capabilities: unified
  OpenAI-format API across providers, virtual keys, budgets, per-key/team/user spend
  tracking, coverage of the institutional channels (Azure OpenAI, Bedrock, Vertex,
  self-hosted vLLM / Ollama / OpenAI-compatible, Anthropic) that lets an approved model
  be slotted in behind one API, and the **MCP Gateway** (one governed endpoint for MCP
  tools) that the platform team's service builds on.
- [Claude Agent SDK](../sources/0003-claude-agent-sdk.md) — the agentic-navigation loop
  built-in (`Read` / `Glob` / `Grep`, automatic agent loop, `allowed_tools` read-only
  scoping); a Claude-only accelerator, applicable only if Claude is the approved model.

> **Provenance note:** this ADR is `status: draft` on purpose — it records a *proposed*
> design, not a built one. Its **factual** claims are all verified against cited sources:
> the bundle's navigability ([OKF spec](../sources/okf-v0-1-spec.md)); the **gateway**, its
> **institutional-channel coverage**, and its **MCP Gateway** ([LiteLLM](../sources/0002-litellm.md)); and the
> Claude-only **agentic-navigation accelerator** ([Claude Agent SDK](../sources/0003-claude-agent-sdk.md)),
> whose *applicability* is contingent on Claude being the approved model — the loop itself
> is provider-agnostic. What remains unproven is the *design judgment* — that this
> composition is the right one — which only implementation can settle. The **platform AI
> gateway** (LiteLLM + MCP) is an *internal roadmap* item, cited as such, not externally
> verifiable — it is a dependency to coordinate, not a proven fact. Move to `verified` /
> *accepted* once the phase-1 proof of concept demonstrates the citation/provenance
> behaviour on an approved model.
