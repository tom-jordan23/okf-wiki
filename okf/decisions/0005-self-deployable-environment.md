---
# --- OKF v0.1 ---
type: decision
title: "Self-deployable environment with a trust-aware bootstrap"
description: Package the whole effort — dataset, gateway, and the chat/voice interface — as a single Compose-first environment (Helm later) with two egress profiles (fully local no-egress, or approved-hosted BYO-key) chosen by an interactive bootstrap that records which datasets are trusted, the data-sensitivity posture, and who counts as leadership.
tags: [adr, deployment, infrastructure, docker, integrity]
timestamp: 2026-07-13
# --- integrity extension (NOT part of OKF) ---
status: draft
confidence: medium
created: 2026-07-13
last_verified:
verified_by:
review_by: 2027-01-13
sources:
  - ../decisions/0003-leadership-chat-interface.md
  - ../decisions/0004-voice-interface.md
  - ../sources/0002-litellm.md
---

# ADR-0005: Self-deployable environment with a trust-aware bootstrap

- **Status:** proposed
- **Date:** 2026-07-13
- **Deciders:** project owner
- **Builds on:** [ADR-0003 (chat)](0003-leadership-chat-interface.md),
  [ADR-0004 (voice)](0004-voice-interface.md)

## Context

ADR-0003 and ADR-0004 defined *what* the interface is: an agentic-navigation loop over the
`okf/` bundle, routed through a gateway, answered as text or voice while preserving the
integrity chain. What does not yet exist is a way for someone to **stand the whole thing
up** — the dataset, the gateway, an approved model, the STT/TTS, and a servable interface —
without hand-wiring processes. We want a **single self-deployable environment**: clone,
run one command, get a working private URL.

The forces at play:

- **The no-egress thesis must be deployable, not just designable.** ADR-0003's constraint
  was that a self-hosted route can keep data inside the institutional boundary. That only
  matters if it is *packaged* — a bundle that, on sensitive corpora, runs the LLM **and**
  the STT/TTS locally so no question, answer, or audio ever leaves the host. The gateway
  abstraction is what makes "local" vs "approved cloud" a config swap rather than a rewrite
  ([LiteLLM](../sources/0002-litellm.md)).
- **Trust is a deployment-time decision, and it is currently tribal.** *Which* dataset is
  the trusted corpus, *who* vouches for it, *how sensitive* the data is, and *who counts as
  leadership* are exactly the judgments this project treats as provenance for notes — yet at
  deploy time they live in someone's head. The same ethos that makes every claim cite its
  evidence should make every **deployment** record what it trusts.
- **The audience can't hand-edit YAML.** The people who deploy this for a team are not all
  infra engineers. The path from clone to running must be an interview, not a config-file
  archaeology dig.
- **Two very different homes.** A single VM / laptop self-host (Compose) and an org-scale
  Kubernetes cluster (Helm) are different targets; forcing one to serve both slows the
  first run for everyone.
- **The interface must actually be servable.** Only headless POCs exist
  ([leadership-chat](../runbooks/leadership-chat-poc.md),
  [voice-chat](../runbooks/voice-chat-poc.md)). A deployable environment implies building
  the thin web + voice service those POCs were the gate for (ADR-0003/0004 phase 2).

## Decision

Ship a **Compose-first self-deployable environment** whose profile and trust posture are
set by an **interactive bootstrap**. Specifically:

1. **One environment, all services, Compose first.** `docker compose up` brings up: the
   **dataset** (a read-only volume over a Git checkout of `okf/` — freshness stays `git
   pull`, ADR-0003 decision 5), the **gateway** ([LiteLLM](../sources/0002-litellm.md) as a
   container), and the **thin web + voice app** (below). **Helm is deferred** as the
   org-scale follow-on, and the layout is kept Helm-friendly (each concern a service, config
   via env) so the chart is a repackage, not a redesign.

2. **Two egress profiles, selected at bootstrap.** The gateway abstraction lets the *same*
   app target either:
   - **`no-egress`** — all inference is local and nothing leaves the host: an open-weight
     LLM (Ollama/vLLM), a self-hosted **Whisper** STT, and a local **TTS** (Kokoro/Piper),
     all OpenAI-format behind the gateway. This is the profile that fully honours the
     data-egress thesis; it costs the most (weights to pull, real hardware).
   - **`hosted`** — the gateway fronts an **approved cloud** LLM/STT/TTS with a
     bring-your-own key. Smallest footprint, fastest, but questions and audio egress to the
     vendor. Appropriate only when the corpus sensitivity allows it.
   Which one runs is the operator's **sensitivity answer**, not a code change.

3. **Build the thin web + voice service (ADR-0003/0004 phase 2).** A small **stdlib** HTTP
   service that reuses the **unchanged** navigation loop and the `SPOKEN`/`PROVENANCE`
   split: a dead-simple page with text chat and push-to-talk, the answer spoken back, and
   the **`PROVENANCE` channel shown on screen** beside it. The integrity contract is served,
   not just proven. The app still talks **only** to the gateway (ADR-0003 decision 3) — it
   holds no provider SDK and no keys.

4. **A trust-aware bootstrap that records what it trusts.** Before generating any config,
   an interactive script asks — and **writes down, dated** — the deployment's trust
   decisions:
   - **Trusted dataset(s):** which bundle(s) to serve (local path or Git URL), **validated**
     with `scripts/validate.py` before use, and **who vouches** for each. Provenance of the
     *corpus itself*, not just its notes.
   - **Data sensitivity / egress posture:** → selects `no-egress` vs `hosted`.
   - **Org structure / access:** who counts as "leadership" and the access boundary (an
     access token / auth) — the open question ADR-0003 flagged, now answered per deployment.
   It then writes the generated `.env` (secrets **git-ignored**), selects the compose
   profile + gateway config, and emits a dated **deployment provenance manifest** so the
   trust posture is recorded, not tribal. Extending the integrity ethos from notes to the
   deployment is the point, not a side effect.

5. **Secrets and dataset discipline.** Keys and the access token live only in the generated
   `.env` (never committed); the dataset volume is **read-only**; in `no-egress` there is no
   cloud fallback and no telemetry — no-egress means no-egress.

## Consequences

- **Easier:** hand someone the repo and one command; a genuinely private option for
  sensitive corpora; the trust posture of each deployment is captured instead of assumed;
  swapping local↔hosted or one model for another stays a config change (the ADR-0003 gateway
  dividend).
- **Harder:** we now own **container images and a hosted web service** to secure — TLS, real
  authn/authz, image patching; `no-egress` needs real (often GPU) hardware and raises
  **model-weight distribution + licensing** questions for air-gapped installs; secrets
  management beyond a `.env` file; a larger attack surface than a headless script.
- **Committed to:** the app talks only to the gateway (no keys in the app, no provider SDK);
  the dataset is read-only and Git-sourced; `no-egress` is airtight (no cloud fallback, no
  telemetry); trust decisions are recorded at deploy time.
- **Caveat — a self-hosted model must still clear the integrity bar.** ADR-0003's phase-4
  eval gate applies to whatever open-weight model the `no-egress` profile runs; a weak local
  model that launders `draft` into fact fails the gate regardless of how private it is.
  Privacy does not substitute for the integrity behaviours.

## Alternatives considered

- **One fat image with the model weights baked in.** Simplest to run, but huge and rigid,
  bakes in a single model (against the approved-model-is-swappable rule), and drags model
  **licensing** into our image. Rejected; keep models as separate, swappable services.
- **Helm / Kubernetes first.** The right org-scale target, but it assumes a cluster and
  slows the first run for the laptop/VM self-hoster who is the near-term user. **Deferred**,
  not rejected — the Compose layout is kept chart-friendly.
- **A managed PaaS / hosted SaaS deployment.** Fastest to a URL, but forfeits self-hosting
  and the no-egress option outright. Rejected for the same reason ADR-0003 rejected the
  docs-chat SaaS.
- **No bootstrap — ship example configs to hand-edit.** Less code, but the trust decisions
  (which dataset, how sensitive, who is admitted) then go **unrecorded** — precisely the
  tribal-knowledge failure this project exists to prevent. Rejected; the interview *is* the
  provenance step.

## Rollout (phased)

1. **Compose environment + thin web/voice app + bootstrap**, both profiles, over the local
   bundle. The self-contained first run. (See the
   [self-hosted deploy runbook](../runbooks/deploy-self-hosted.md).)
2. **Harden for a real audience** — TLS termination, real auth (SSO/OIDC), a `git pull`
   freshness sidecar, per-key gateway budgets.
3. **Helm chart** at parity with Compose for org-scale/K8s installs.
4. **Air-gapped `no-egress` install** — offline weight distribution and the approved
   open-weight model certified through the phase-4 eval gate.

## Open questions

- **Production auth & TLS** — the bootstrap sets a shared access token as a floor; SSO/OIDC
  and TLS termination are phase 2. This is the ADR-0003 "who is leadership" open question,
  now owned here.
- **Hardware & approved local model** — GPU/RAM floor for `no-egress`, and *which*
  open-weight LLM (and Whisper/TTS sizes) clear the integrity + latency bar. Ties to the
  phase-4 eval gate.
- **Model-weight distribution & licensing** for air-gapped installs — how weights are
  delivered and under what licence, kept out of our image.
- **Secrets management** — `.env` is the POC floor; a real deployment may need a secrets
  manager / mounted secrets.
- **Does the bootstrap-generated trust manifest belong in the bundle?** It is deployment
  provenance; whether it becomes a `draft` note in `okf/` or stays a deploy-side artifact is
  unsettled (it may carry org-specific detail).

## Sources

- [ADR-0003: Leadership chat interface](0003-leadership-chat-interface.md) — the gateway
  boundary and Git-checkout freshness this environment packages, and the "who is leadership"
  auth question it now answers per deployment.
- [ADR-0004: Voice interface](0004-voice-interface.md) — the voice pipeline the deployable
  interface serves, and the local STT/TTS the `no-egress` profile runs.
- [LiteLLM](../sources/0002-litellm.md) — the gateway as a container (official Docker images
  + Helm), the provider abstraction that makes `no-egress`↔`hosted` a config swap, and the
  OpenAI-format audio endpoints the local STT/TTS register behind.

> **Provenance note:** `status: draft` on purpose — a *proposed* packaging, not a proven
> one. Its factual claims — that the gateway ships as a container/Helm and fronts both local
> (Ollama/vLLM, self-hosted Whisper, local TTS) and cloud providers through one OpenAI-format
> API — are **verified** against the LiteLLM docs (accessed 2026-07-13) and recorded in
> [its source note](../sources/0002-litellm.md). What is unproven is the **design judgment**:
> that a Compose-first, two-profile, bootstrap-driven environment is the right shape. Only a
> real deployment — one command to a working, private, integrity-preserving URL — can move
> this to *accepted*.
