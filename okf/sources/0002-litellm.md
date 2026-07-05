---
# --- OKF v0.1 ---
type: source
title: "LiteLLM — SDK & Proxy Server (AI Gateway)"
description: BerriAI's open-source unified API and self-hosted gateway for 100+ LLMs, with per-key/team/user cost tracking, budgets, and rate limits.
tags: [source, llm, gateway, infrastructure]
timestamp: 2026-07-05
resource: https://docs.litellm.ai/docs/
# --- integrity extension (NOT part of OKF) ---
status: verified
confidence: high
created: 2026-07-05
last_verified: 2026-07-05
verified_by: claude
review_by: 2027-01-05
# --- source evidence fields ---
source_type: web
author: BerriAI
publisher: "BerriAI (github.com/BerriAI/litellm)"
url: https://docs.litellm.ai/docs/
published:
accessed: 2026-07-05
credibility: high
---

# LiteLLM — SDK & Proxy Server (AI Gateway)

> BerriAI, *LiteLLM documentation* and *BerriAI/litellm* repository. Accessed 2026-07-05.
> Official product documentation and source repository (primary sources).

## What it supports

This is the evidence for the **gateway** decision in
[ADR-0003: Leadership chat interface](../decisions/0003-leadership-chat-interface.md) —
both the claim that routing model calls through LiteLLM gives central, backend-side
control over model selection and token / cost accounting, **and** the claim that the
gateway is the provider-abstraction layer that lets the system run on whatever LLM the
institution approves.

## Summary

Verified against the official docs (`docs.litellm.ai`) and the `BerriAI/litellm`
repository:

- **Two forms.** LiteLLM ships as (a) a **Python SDK** — `completion()`,
  `embedding()`, `image_generation()`, plus a Router with retry, fallback, and load
  balancing — and (b) a **Proxy Server / AI Gateway**: a self-hosted gateway for teams
  managing LLM access across an organization, with centralized logging and an admin UI.
- **Unified OpenAI-format API.** A single interface to "100+ LLMs — OpenAI, Anthropic,
  Vertex AI, Bedrock, and more — using the OpenAI format," where "every response
  follows the OpenAI Chat Completions format, regardless of provider." **Anthropic is
  explicitly supported.**
- **Cost & spend tracking.** Tracks "costs per key, team, and user across all
  providers," and automatically tracks spend for known models.
- **Budgets & rate limits.** **Virtual keys** with per-key / per-team / per-user
  **budgets** (multiple independent budget windows, each reset on its own schedule) and
  **rate limits** per team or user.
- **Routing.** Built-in retry / fallback logic across deployments via the Router; load
  balancing with automatic fallbacks.
- **Institutional-channel coverage (verified against the providers docs).** LiteLLM
  fronts the channels an institution is likely to sanction: **Azure OpenAI**, **AWS
  Bedrock**, **Google Vertex AI**, **self-hosted / on-prem open-weight models** (via
  **vLLM**, **Ollama**, or any **OpenAI-compatible endpoint**), and **Anthropic**. The
  app targets LiteLLM's single OpenAI-format API; which of these actually answers is a
  backend config change, so the approved model can be slotted in — or swapped — without
  touching the UI.
- **MCP Gateway (verified against the MCP docs).** Beyond model calls, the LiteLLM
  proxy is also an **MCP Gateway** — "a fixed endpoint for all MCP tools" — that connects
  to multiple MCP servers (Streamable HTTP / SSE / stdio) and exposes their tools to
  clients through one endpoint, with **permission management by key / team / organization**.
  Clients reach the tools via a direct MCP endpoint, REST routes
  (`/mcp-rest/tools/list`, `/mcp-rest/tools/call`), or the `/chat/completions` tool-calling
  path. This is why a LiteLLM-based gateway can govern *both* LLM traffic and MCP tool
  traffic through a single control point.
- **License.** The **core is MIT-licensed** (© Berri AI). Content under the
  `enterprise/` directory is governed by a **separate license** (`enterprise/LICENSE`);
  a paid enterprise tier adds features such as SSO, RBAC, and audit logs. The
  self-hosted core is free — you pay only for the infrastructure it runs on.

These properties are exactly what ADR-0003 requires of a gateway: model choice, keys,
rate limits, and token/cost accounting live on the **backend**, decoupled from the app
and swappable without touching the leadership-facing UI.

## Assessment

**Credibility: high, for the core claims.** These are drawn from **primary sources** —
the vendor's own documentation and the repository's `LICENSE` file (the MIT-core /
`enterprise/`-directory split is quoted directly from that file). The functional claims
(unified OpenAI-format API, virtual keys, budgets, spend tracking, Router
fallback/load-balancing) are stated plainly in the official docs and the repository's
description.

**Caveats:**

- **Enterprise pricing figures** (e.g. specific per-month / per-year numbers) appeared
  only in **third-party** write-ups, not the primary docs, so they are **deliberately
  omitted here** rather than cited as verified. Confirm current pricing directly with
  BerriAI before relying on it.
- **Recency.** LiteLLM is a fast-moving project with frequent releases; feature names
  and defaults drift. `review_by` is set six months out — re-check the docs before then
  for breaking changes.
