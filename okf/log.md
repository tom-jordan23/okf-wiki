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

## 2026-07-23 — Decision-support extension, Phases 2 & 3 (schema + agents/design)

- Built Phases 2–3 of [ADR-0006](decisions/0006-decision-support-extension.md). The layer
  stays optional and deletable; `validate.py` stays stdlib-only; OKF conformance unchanged
  (still `PASS`, and the new checks are **warnings**, never errors — OKF permits any `type:`).
- **Phase 2 — schema.** Promoted the decision-support artifacts from sections-in-a-note to
  six first-class `type:` values, one note per thing, each in its own folder:
  [recommendations](recommendations/index.md), [options](options/index.md),
  [criteria](criteria/index.md), [gates](gates/index.md), [findings](findings/index.md),
  [risks](risks/index.md). Added a [template](templates/frontmatter.md) per type and taught
  `validate.py` the extension fields (`id`, register `state`, `severity`,
  `likelihood`/`impact`) and the `recommendation` `## Open decisions` rule — verified the
  rules both fire on bad input and pass the worked examples. One-note-per-entry (not a prose
  table) is deliberate: it's what makes findings/gates machine-checkable, ADR-0006's stated
  win.
- Added a **deletable worked set** reusing the datastore scenario so both forms coexist:
  [REC-1](recommendations/EXAMPLE-datastore-recommendation.md) tying together a viable
  [option](options/EXAMPLE-datastore-managed-pg.md), a
  [ruled-out option](options/EXAMPLE-datastore-shared-db.md), a
  [criterion](criteria/EXAMPLE-reversibility.md), a [gate](gates/EXAMPLE-datastore-launch-gate.md),
  a [finding](findings/EXAMPLE-lockin-review.md), and a [risk](risks/EXAMPLE-serverless-lockin.md)
  — all illustrative fiction, so they never leave `draft`. Cross-linked to the Phase-1
  [architecture example](architecture/EXAMPLE-datastore-options.md).
- Added **`METHODOLOGY.md`** (repo root, outside the bundle) — the why/how-to-reproduce
  companion to the runbook.
- **Phase 3 — agents + design.** Added `.claude/agents/`: a **producer/checker split**
  (`ds-producer` writes; `ds-checker` is **read-only by design** — it may not edit what it
  checks) plus four concurrent, mutually-blind **review lenses** (`review-standards`,
  `review-security`, `review-redteam`, `review-integrity`) that feed the findings register.
  Added the [`visual-vocabulary`](concepts/visual-vocabulary.md) concept (CVD-safe; colour
  encodes ownership only; fixed shape/line lexicon; Mermaid→SVG→pptx, generated never
  hand-edited).
- Wired it through `CLAUDE.md` (note-types table, schema note, validation + roadmap,
  decision-support section), the [layout note](architecture/knowledge-base-layout.md), the
  [roadmap note](architecture/decision-support-extension.md) phasing, and the bundle/section
  indexes. `interface-memo` (a Tier-3 single-effort idea) intentionally deferred.

## 2026-07-23 — Decision-support extension, Phase 1 (no schema change)

- Built the Phase-1, no-schema-change part of [ADR-0006](decisions/0006-decision-support-extension.md).
  All additive and deletable; the OKF core and `validate.py` are unchanged and stay
  stdlib-only.
- Added the [Run a Decision-Support Effort](runbooks/run-a-decision-support-effort.md)
  runbook (`draft`): options → criteria → ruled-out set → tradeoff matrix → recommendation
  *for reaction, not decision*, expressed as sections inside ordinary `architecture` notes.
  Conventions baked in: feasibility ≠ desirability, strength-of-evidence per claim,
  absence-of-evidence as an explicit finding.
- Added a deletable worked example, [EXAMPLE: Datastore options](architecture/EXAMPLE-datastore-options.md)
  (`draft`, illustrative fiction — makes no verifiable claims, so it never leaves `draft`).
- Added `preso/` (outside the bundle): a `python-pptx` deck builder driven by Markdown
  speaker-scripts (Markdown = source of record; every slide traces to a note). It is the
  only third-party dependency in the repo, scoped to `preso/requirements.txt`; `build.sh`
  fails helpfully when it's absent. Built and verified the example deck renders (title + 4
  slides + speaker notes); the generated `.pptx` is not committed (regenerable).
- Added `artifacts/` (git-ignored staging for raw inputs; only sanitized `source` notes
  enter the bundle) and hardened `.gitignore` (raw artifacts, branded deck templates,
  Office lock files, depth-agnostic Obsidian ignores for the vault opened at `okf/`).
- Wired it into `README.md`, `CLAUDE.md` (new "Decision-support extension (optional)"
  section + Phase 2–3 roadmap), and the runbook/architecture indexes. Bundle passes
  `validate.py` with no new warnings.

## 2026-07-23 — ADR-0006: decision-support extension (roadmap)

- Reviewed three private efforts built on clones of this template (institution-specific;
  anonymized here, not part of this public template) to synthesize a decision-support
  feature set. Key finding: **two of three abandoned the `okf/` bundle** because the base
  has no vocabulary for options-in-flight, findings, gates, or recommendations; only one
  kept OKF and did the work in ordinary `architecture` notes with **no schema change**.
- Added [ADR-0006](decisions/0006-decision-support-extension.md) (`draft`/proposed): adopt
  a decision-support extension and build it by **extending OKF** (new `type:` values +
  `validate.py` enforcement), not forking to unvalidated prose registers.
- Added the [Decision-Support Extension roadmap](architecture/decision-support-extension.md)
  (`draft`): the convergent features ranked by cross-project signal (Tier 1 = all three
  built it) — a `preso/` deck-from-code tier, the options→criteria→matrix→phased-
  recommendation pattern, findings/review registers, producer/checker agents, a
  `METHODOLOGY.md`, and new note types — plus a three-phase plan that keeps the layer
  optional and deletable.
- Stays `draft` until the extension is designed and a first artifact is built; the
  reviewed methodology docs should then be captured as `internal-doc` `source` notes so
  the decision's basis is traceable.

## 2026-07-13 — ADR-0005: self-deployable environment + thin web/voice app

- Added [ADR-0005](decisions/0005-self-deployable-environment.md) (`draft`/proposed): package
  the whole effort — dataset, gateway, and the chat/voice interface — as a **single
  Compose-first environment** (Helm deferred), with two egress profiles chosen at bootstrap:
  **no-egress** (open-weight LLM via Ollama + self-hosted Whisper + local Kokoro TTS, nothing
  leaves the host) or **hosted** (gateway → approved cloud, BYO key). The gateway abstraction
  makes the choice a config swap, not a code change.
- Built the interface ADR-0003/0004 phase 2 implied and only POCs existed for: a **stdlib web
  + voice server** (`chat/server.py` + `chat/web/index.html`) reusing the unchanged loop and
  the `SPOKEN`/`PROVENANCE` split — text chat + push-to-talk, with the Sources panel shown on
  screen. App holds no keys and talks only to the gateway.
- Packaged it under `deploy/`: `Dockerfile` (stdlib-only, tiny), `docker-compose.yml` (app +
  gateway always on; ollama/whisper/kokoro behind the `no-egress` profile), two gateway
  configs, and `.env.example`. Verified the image references against upstream (LiteLLM
  `ghcr.io/berriai/litellm`; OpenAI-compatible `hwdsl2/whisper-server` + `hwdsl2/kokoro-server`).
- Added a **trust-aware `deploy/bootstrap.py`**: an interview that records — dated — which
  datasets are trusted (validated via `scripts/validate.py`) and who vouches, the
  sensitivity/egress posture (→ profile), and the access boundary (who is "leadership" + an
  access token), then writes `.env` (git-ignored) and a `deployment.manifest.md` provenance
  record. Extends the integrity ethos from notes to the deployment.
- Extended the [LiteLLM source note](sources/0002-litellm.md): it ships official Docker images
  + a Helm chart (verified against the deploy docs, 2026-07-13). Added the
  [self-hosted deploy runbook](runbooks/deploy-self-hosted.md).
- Stays `draft` until a real deployment reaches a working, private, integrity-preserving URL.

## 2026-07-13 — ADR-0004: voice interface over the leadership chat

- Added [ADR-0004](decisions/0004-voice-interface.md) (`draft`/proposed): ask the bundle by
  voice, hear grounded answers. Voice is a thin **STT → the unchanged ADR-0003 text loop →
  TTS** pipeline — the proven grounding stays put and voice is a transport shell around it.
- Both STT and TTS route through the **same gateway** as chat (verified: LiteLLM exposes
  `/v1/audio/transcriptions` and `/v1/audio/speech` in OpenAI format — see
  [source note](sources/0002-litellm.md), re-verified 2026-07-13), so audio inherits the
  gateway's spend tracking, approved-provider abstraction, and self-hostable no-egress route.
- Provenance survives the audio channel via **dual-channel answering**: a `SPOKEN` track
  (heard, confidence in words, no paths) plus a `PROVENANCE` track (shown/logged, paths +
  `status`). One integrity contract, two renderings — voice is an opt-in prompt addendum, not
  a fork of the text path.
- Built the phase-1 voice POC under `chat/` (`voice.py`, `run_voice_poc.py`,
  `voice_addendum.md`) reusing the phase-1 loop and probe set verbatim, adding an audio
  round-trip and a new gate: **no note path may leak into the spoken channel**. Stdlib only;
  offline `--dry-run` passes the plumbing. See the [voice-chat POC runbook](runbooks/voice-chat-poc.md).
- Stays `draft` until the probes run on a real audio stack and the spoken track is judged
  honest by ear (phase-1 verification); only that can move ADR-0004 toward *accepted*.

## 2026-07-08 — Built the phase-1 POC for ADR-0003 (leadership chat)

- Implemented the [phase-1 POC runbook](runbooks/leadership-chat-poc.md) as runnable code
  under `chat/` (outside the bundle — implementation, not a note): a provider-agnostic
  OpenAI-format tool-use loop over read-only `read_file`/`list_dir`/`grep` scoped to the
  `okf/` checkout, driven by the integrity system prompt, with a runner that executes the
  four-probe set and auto-flags fabricated citations and missing declines. Stdlib only.
- Gateway (decision 3) built as an **interface** with two interchangeable profiles —
  **internal** self-hosted [LiteLLM](sources/0002-litellm.md) or an **external** shared
  gateway — switchable by env/config alone, no code change. Navigator kept as a standalone
  module so it can later become the MCP server of decision 6.
- Not yet run against a model, so [ADR-0003](decisions/0003-leadership-chat-interface.md)
  and the runbook stay `draft`: the POC de-risks the design but only executing the probes
  on an approved model can move them toward `verified` / *accepted* (phase 4).

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
