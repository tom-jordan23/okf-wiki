---
# Reserved OKF file (log.md): dated change history — no `type`.
title: Activity & Decision Log
description: Chronological history of changes to this bundle, newest first.
tags: [meta, log]
timestamp: 2026-06-15
# --- integrity extension (NOT part of OKF) ---
status: verified
review_by: 2027-06-15
---

# Activity & Decision Log

Newest entries first. One entry per meaningful change or decision. Keep it terse; link
to the notes that hold the detail.

## 2026-07-06 — Added the phase-1 POC runbook for ADR-0003

- Added [leadership-chat POC runbook](runbooks/leadership-chat-poc.md) (`draft`): the
  headless phase-1 procedure to prove the agentic-navigation loop answers from the bundle
  while preserving citations, `status`-awareness, and grounded-vs-inferred separation.
  Includes the four-probe set (verified lookup / draft-only / scenario / unsupported) that
  seeds the phase-4 eval gate. Not yet executed — status stays `draft` until it is run.

## 2026-07-05 — ADR-0003: leave the door open to the platform team's AI gateway

- Recorded that a platform team is building a shared AI gateway (LiteLLM + MCP) to proxy
  LLM traffic *(internal roadmap, unverifiable here)*. Reframed the gateway (decision 3)
  as an **interface**, not a specific instance: consume the shared service when available,
  self-host [LiteLLM](sources/0002-litellm.md) only as interim — same OpenAI-format API
  either way, so switching is config, not a rewrite.
- Added decision 6: keep bundle-navigation packageable as an **MCP server** so it can
  register behind the gateway's MCP Gateway and become a reusable capability. Verified
  (LiteLLM MCP docs) and recorded the **MCP Gateway** feature in the LiteLLM source note.
- Added a build-vs-consume coordination open question.

## 2026-07-05 — ADR-0003: added the institutionally-approved-LLM constraint

- Recorded that the model must be an institutionally-approved LLM and the approved set is
  not yet fixed, so the design must be **provider-agnostic**. Reframed the agent loop as an
  ordinary tool-use loop over the gateway's OpenAI-format API; the
  [Claude Agent SDK](sources/0003-claude-agent-sdk.md) is demoted from foundation to a
  **Claude-only accelerator** (usable only if Claude is approved).
- Verified (LiteLLM providers docs) and recorded that the gateway fronts the likely
  institutional channels — Azure OpenAI, Bedrock, Vertex, self-hosted (vLLM / Ollama /
  OpenAI-compatible), Anthropic — so an approved model (incl. a self-hosted, no-egress
  one) slots in behind one API. Updated the [LiteLLM source](sources/0002-litellm.md).
- Added the caveat that integrity behaviours depend on model capability (the phase-4 eval
  gate certifies a chosen model) and an open question for the undetermined approved model.

## 2026-07-05 — Verified the Claude Agent SDK; closed ADR-0003's last load-bearing claim

- Added [Claude Agent SDK source note](sources/0003-claude-agent-sdk.md) (`verified`),
  checked against Anthropic's official Agent SDK docs: built-in `Read`/`Glob`/`Grep`
  tools, an automatic agent loop ("Claude handles tools autonomously" vs the Client SDK's
  manual loop), and `allowed_tools` scoping (docs' own read-only example is exactly
  `Read`/`Glob`/`Grep`).
- Updated [ADR-0003](decisions/0003-leadership-chat-interface.md) to cite it. Both
  load-bearing product claims (gateway + agentic navigation) are now sourced; the ADR
  stays `draft` only because the design is proposed, not built.

## 2026-07-05 — Verified LiteLLM as a source; sourced ADR-0003's gateway claim

- Added [LiteLLM source note](sources/0002-litellm.md) (`verified`), checked against the
  official docs and the `BerriAI/litellm` repo/LICENSE: unified OpenAI-format API across
  providers (incl. Anthropic), virtual keys, budgets, per-key/team/user spend tracking,
  MIT-licensed core. Enterprise pricing left out as unverified (secondary-source only).
- Updated [ADR-0003](decisions/0003-leadership-chat-interface.md) to cite it: the
  **gateway** claim is now sourced; the **agent-SDK** claim remains flagged unverified,
  and the ADR stays `draft` (design not yet built).

## 2026-07-05 — Proposed a leadership chat interface (ADR-0003)

- Recorded [ADR-0003](decisions/0003-leadership-chat-interface.md): a simple hosted web
  chat for non-technical leadership, backed by **agentic navigation** over a Git checkout
  of `okf/` (not an embedding pipeline at current scale), with answers that preserve
  note-level provenance and `status`, and model access through a **gateway** (candidate:
  LiteLLM) for central token/cost control.
- Status `draft` / *proposed*: design only, not built. LiteLLM and agent-SDK claims are
  flagged as unverified pending `source` notes.

## 2026-06-15 — Hosted on GitHub; added validator

- Renamed the template `llm-wiki` → `okf-wiki` and published it as a public GitHub
  template repository: https://github.com/tom-jordan23/okf-wiki
- Added `scripts/validate.py`: OKF conformance (errors) + integrity checks (warnings).
  See the Validation section in `CLAUDE.md`. Bundle currently passes.

## 2026-06-15 — Aligned the bundle to OKF v0.1

- Adopted [OKF v0.1](sources/okf-v0-1-spec.md) as the base format; see
  [ADR-0002](decisions/0002-adopt-okf-v0-1.md).
- Dropped the custom `id` field (OKF identity = file path), replaced `[[wikilinks]]`
  with relative Markdown links, added OKF's `timestamp`, and relabeled the integrity
  fields as OKF extension keys.
- Marked `index.md` / `log.md` as reserved files (no `type`).
- Recorded the relative-vs-absolute link divergence (for Obsidian navigability) in
  ADR-0002.

## 2026-06-15 — Template scaffolded

- Created the LLM-wiki template: operating manual (`CLAUDE.md`), the `okf/` knowledge
  base, per-type templates, and one worked example per note type.
- Baked in the academic-integrity extension: sources required, verification status,
  claim-level provenance, and `review_by` staleness cadence. See
  [ADR-0001](decisions/0001-markdown-frontmatter-project-memory.md).
- Enforcement is convention + Claude review for now; a validator and CI are on the
  roadmap in `CLAUDE.md`.
