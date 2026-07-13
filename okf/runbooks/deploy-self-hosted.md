---
# --- OKF v0.1 ---
type: runbook
title: "Deploy the Self-Hosted Knowledge Assistant (Phase 1)"
description: Stand up the whole effort — dataset, gateway, and chat/voice interface — as one Compose environment, choosing a no-egress or approved-hosted profile via the trust-aware bootstrap.
tags: [runbook, deployment, docker, poc]
timestamp: 2026-07-13
# --- integrity extension (NOT part of OKF) ---
status: draft
confidence: medium
created: 2026-07-13
last_verified:
verified_by:
review_by: 2027-01-13
sources:
  - ../decisions/0005-self-deployable-environment.md
  - ../decisions/0003-leadership-chat-interface.md
  - ../decisions/0004-voice-interface.md
  - ../sources/0002-litellm.md
---

# Deploy the Self-Hosted Knowledge Assistant (Phase 1)

> Phase 1 of [ADR-0005](../decisions/0005-self-deployable-environment.md). Bring up the
> dataset + gateway + chat/voice interface as **one Compose environment**, with the egress
> profile and trust posture chosen by an interview. The implementation lives in `deploy/`
> and `chat/server.py` (outside the bundle — code, not notes).

## Prerequisites

- Docker + Docker Compose on the host.
- A validated OKF bundle to serve (this repo's `okf/`, or another that passes
  `scripts/validate.py`).
- For **hosted**: a key for an institutionally-approved cloud model. For **no-egress**:
  enough hardware to run an open-weight LLM + Whisper + a local TTS (GPU strongly advised).

## Steps

1. **Run the trust-aware bootstrap** — `python3 deploy/bootstrap.py`. It records, dated, the
   deployment's trust decisions before writing any config (ADR-0005 decision 4):
   - **Trusted dataset(s)** — validated with `scripts/validate.py` before use; who vouches is
     recorded. Provenance of the corpus itself.
   - **Data-sensitivity / egress posture** — selects `no-egress` (all inference local) or
     `hosted` (approved cloud, BYO key).
   - **Org / access** — who counts as "leadership", and the access token that gates them.
   It writes `deploy/.env` (secrets, git-ignored) and `deploy/deployment.manifest.md` (the
   dated trust record).
2. **Confirm the gateway config** for the chosen profile:
   - *hosted* — edit `deploy/gateway/litellm.hosted.yaml` so `okf-chat-model` /
     `okf-stt-model` / `okf-tts-model` point at your approved models.
   - *no-egress* — confirm the local STT/TTS **ports** in `docker-compose.yml` and
     `litellm.no-egress.yaml` match what your Whisper/Kokoro images actually expose.
3. **Bring it up.**
   - hosted: `cd deploy && docker compose up --build`
   - no-egress: `cd deploy && docker compose --profile no-egress up --build`, then pull the
     LLM: `docker compose exec ollama ollama pull llama3.1:8b-instruct`.
4. **Open the URL** (`http://localhost:8080`), paste the access token, and ask a question by
   text or push-to-talk. Confirm the answer shows its **Sources** panel (the `PROVENANCE`
   channel) beside the spoken answer.

## Verification

- The app reaches the gateway (`/api/health` returns `ok`, the right model, voice on/off).
- A verified-fact question answers **with a resolving Sources panel**; the UI flags any
  fabricated citation rather than hiding it.
- An unsupported question is **declined**, not answered with an invented note.
- **no-egress only:** confirm no outbound traffic to any cloud LLM/STT/TTS while asking
  (e.g. watch container network egress). No-egress must mean no-egress.
- The dataset mount is **read-only**; the app cannot write to `okf/`.
- `deploy/.env` and `deploy/deployment.manifest.md` are **git-ignored** (secrets/org detail).

## Rollback / recovery

- Gateway/model errors surface as `502` in the UI — check `docker compose logs gateway` and
  that the config's model/keys (hosted) or pulled model + service ports (no-egress) are right.
- If a self-hosted model can't hold the integrity behaviours (launders draft into fact,
  fabricates citations), that is a **model-capability finding** for the ADR-0003 phase-4 eval
  gate — record it; do **not** relax the integrity rules. Fall back to a stronger approved
  model rather than shipping an untrustworthy private one.
- Do not expose the port beyond localhost until an access token is set and TLS + real auth
  are in front (ADR-0005 phase 2).

## Sources

- [ADR-0005: Self-deployable environment](../decisions/0005-self-deployable-environment.md) —
  the design this procedure executes (phase 1).
- [ADR-0003](../decisions/0003-leadership-chat-interface.md) /
  [ADR-0004](../decisions/0004-voice-interface.md) — the loop, gateway boundary, and voice
  pipeline the deployment serves.
- [LiteLLM](../sources/0002-litellm.md) — the gateway container and the OpenAI-format model +
  audio endpoints both profiles route through.
