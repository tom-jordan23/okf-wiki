---
# --- OKF v0.1 ---
type: source
title: "Claude Agent SDK"
description: Anthropic's Python/TypeScript library that runs the Claude Code agent loop in-process, with built-in file-navigation tools and tool-scoping.
tags: [source, llm, agent, sdk, anthropic]
timestamp: 2026-07-05
resource: https://code.claude.com/docs/en/agent-sdk/overview
# --- integrity extension (NOT part of OKF) ---
status: verified
confidence: high
created: 2026-07-05
last_verified: 2026-07-05
verified_by: claude
review_by: 2027-01-05
# --- source evidence fields ---
source_type: web
author: Anthropic
publisher: Anthropic
url: https://code.claude.com/docs/en/agent-sdk/overview
published:
accessed: 2026-07-05
credibility: high
---

# Claude Agent SDK

> Anthropic, *Agent SDK overview* ("Build production AI agents with Claude Code as a
> library"). Accessed 2026-07-05. Official product documentation (primary source).

## What it supports

This is the evidence for the **agentic-navigation accelerator** in
[ADR-0003: Leadership chat interface](../decisions/0003-leadership-chat-interface.md) —
the claim that the Claude Agent SDK provides the read / navigate / grep agent loop out of
the box, so the leadership chat can traverse the `okf/` bundle and cite real files without
a bespoke retrieval pipeline. Note this is a **Claude-only accelerator**: ADR-0003's loop
is provider-agnostic, and the SDK applies only if Claude is the institutionally-approved
model.

## Summary

Verified against the official Agent SDK documentation:

- **What it is.** "The Agent SDK gives you the same tools, agent loop, and context
  management that power Claude Code, programmable in **Python and TypeScript**"
  (`claude_agent_sdk` / `@anthropic-ai/claude-agent-sdk`). It is Claude Code packaged as
  a library.
- **Built-in file-navigation tools — no tool execution to implement.** Ships with
  **`Read`** (read any file in the working directory), **`Glob`** (find files by
  pattern), **`Grep`** (regex search over file contents), plus `Write`, `Edit`, `Bash`,
  `WebSearch`, `WebFetch`, and others. This is exactly the navigate-and-read loop the
  ADR relies on.
- **Runs the agent loop automatically.** The docs contrast it with the plain Client
  SDK: with the Client SDK "you implement the tool loop"; with the Agent SDK "Claude
  handles tools autonomously." No manual `while stop_reason == "tool_use"` loop.
- **Tool scoping / permissions.** `allowed_tools` (Python) / `allowedTools`
  (TypeScript) restricts which tools the agent may use. The docs' own **read-only agent**
  example pre-approves exactly `["Read", "Glob", "Grep"]` — the configuration the ADR
  wants for a query-only leadership interface. Permission modes and lifecycle **hooks**
  (`PreToolUse`, `PostToolUse`, …) allow further gating, logging, and auditing.
- **Custom tools and MCP.** Supports in-process custom tools and Model Context Protocol
  servers, so extra capabilities can be added without leaving the loop.
- **License.** Governed by Anthropic's Commercial Terms of Service.

Together these confirm the ADR's design: point the SDK at a checkout of `okf/`, scope it
to read-only navigation tools, and let it read and cite the actual notes.

## Assessment

**Credibility: high.** Primary source — Anthropic's own product documentation for the
SDK, with runnable Python and TypeScript examples for each cited capability (built-in
tools, the read-only `allowed_tools` example, hooks, MCP). The claims used here are
structural facts about the SDK, quoted from that page, not performance or marketing
assertions.

**Caveat — recency.** The Agent SDK is an actively developed library; tool names,
option names, and defaults can change between releases. `review_by` is set six months
out — re-check the docs before then, especially the `allowed_tools` / permission surface
that the read-only design depends on.
