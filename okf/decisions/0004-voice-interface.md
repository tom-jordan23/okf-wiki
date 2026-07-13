---
# --- OKF v0.1 ---
type: decision
title: "Voice interface over the leadership chat"
description: Ask the knowledge bundle by voice and hear grounded answers, built as a thin STT → existing agentic-navigation loop → TTS pipeline with audio routed through the same gateway, and note-level provenance preserved on an audio channel via dual-channel (spoken + shown) answering.
tags: [adr, interface, voice, rag, llm]
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
  - ../sources/0002-litellm.md
  - ../sources/okf-v0-1-spec.md
---

# ADR-0004: Voice interface over the leadership chat

- **Status:** proposed
- **Date:** 2026-07-13
- **Deciders:** project owner
- **Extends:** [ADR-0003: Leadership chat interface](0003-leadership-chat-interface.md)

## Context

[ADR-0003](0003-leadership-chat-interface.md) established a text chat over the `okf/`
bundle: a provider-agnostic agentic-navigation loop, routed through a gateway, that
answers leadership questions **while preserving the integrity chain** — note-level
citations, honest `status`, and grounded facts kept visibly apart from inference. We now
want a **voice** modality: ask the bundle a question by speaking, and hear the answer
back, hands- and screen-free.

The forces at play:

- **Trust must survive *this* interface too.** ADR-0003's central rule was that the
  interface must inherit the integrity chain, not launder it. Voice makes that harder, not
  easier: an audio channel has **no clickable citation and no `status` badge**, and reading
  "concepts slash okf-frontmatter-schema dot md, status draft" aloud is unusable. The
  provenance that text renders visually has to survive a channel that is heard, not seen.
  This is the ADR-0003 tension — *trust must survive the interface* — recast for audio, and
  it is the crux of this decision.
- **The text loop is already the hard, proven part.** The agentic-navigation loop and its
  integrity system prompt are what earn a trustworthy answer. Voice should be a **transport
  shell around that loop**, not a reimplementation of it — anything that answers *without*
  going through the loop cannot cite the bundle.
- **Governance must not spring a leak.** ADR-0003 made the gateway the compliance + cost +
  approved-model boundary: the app talks only to the gateway's OpenAI-format API, spend is
  tracked per virtual key, and a self-hosted route can keep data inside the institutional
  boundary. Speech-to-text and text-to-speech are **additional model calls** — if they go
  to some convenient cloud voice API, they punch a hole in exactly that boundary (audio of
  every question egressing to an unapproved vendor).
- **Audience is non-technical and the appeal of voice is accessibility.** The reason to add
  voice is a lower-friction, more inclusive way in (eyes-free, hands-free, mobility). That
  same audience is least equipped to notice when an answer quietly overclaims — so audible
  honesty ("this is only a draft note" / "this is my own inference") matters *more* here,
  not less.
- **Model choice is still unfixed and must stay swappable.** As in ADR-0003, which STT and
  TTS models are institutionally approved is not yet decided; the design must not hard-bind
  to any provider and must tolerate that choice changing.

## Decision

Build voice as a **thin pipeline wrapped around the unchanged ADR-0003 text loop**, with
audio governed by the same gateway and provenance preserved on a dual channel:

1. **Voice = STT → the existing text loop → TTS.** A spoken question is transcribed to
   text, handed to the **unchanged** agentic-navigation loop (the source of truth for
   grounding and citation), and the answer is spoken back. The text loop, its tools, and
   its integrity system prompt are **not modified** — voice adds only a transcribe step
   before and a synthesize step after. Retrieval and grounding stay exactly where ADR-0003
   proved they work.

2. **Audio routes through the same gateway — the compliance boundary does not move.** STT
   and TTS are ordinary OpenAI-format calls to the same gateway the app already uses:
   **`/v1/audio/transcriptions`** and **`/v1/audio/speech`**, both confirmed supported by
   [LiteLLM](../sources/0002-litellm.md) with per-key spend tracking, logging, and
   provider fallback. So audio inherits ADR-0003's governance for free — virtual-key cost
   accounting, an approved-provider set that is a backend config choice, and a
   **self-hostable STT/TTS route** (e.g. self-hosted Whisper, on-prem TTS) that keeps audio
   inside the institutional boundary. The app targets the gateway's audio API the same way
   it targets its chat API; **no separate voice vendor** is introduced.

3. **Provenance survives audio via dual-channel answering.** The model produces one answer
   in **two renderings**: a **`SPOKEN`** track — listenable prose, no file paths, that
   carries confidence **verbally** ("according to a verified note…", "this is only a draft,
   so treat it as provisional…", "the notes don't cover this…", "this next part is my own
   analysis, not from the notes…") — and a **`PROVENANCE`** track — the machine/eye channel
   holding the note paths and each note's `status`, to be displayed and logged, **not
   spoken**. TTS voices only `SPOKEN`; the citation checks run on `PROVENANCE`. The ear gets
   a trustworthy, honest answer; the eye/log gets the traceable chain. Confidence must be
   **audible**, not merely available.

4. **Voice is an opt-in *addendum* to the integrity prompt, not a fork.** The
   `SPOKEN`/`PROVENANCE` formatting is a small addendum appended to the ADR-0003 system
   prompt in voice mode — **one** integrity contract (cite, surface `status`, separate
   inference, never invent a source), **two** renderings of it. The text interface is
   untouched; there is no second, drifting copy of the rules to keep honest.

5. **POC-first, mirroring ADR-0003.** Prove — headless, no UI, no hosting — that the
   integrity behaviours survive an **audio round-trip** (a question spoken and transcribed
   back still drives the same grounded answer; the spoken track stays honest and leaks no
   raw citation) before building any voice UI, latency budget, or turn-taking. The phase-1
   voice runbook and probe reuse are the gate.

## Consequences

- **Easier:** an eyes-free, hands-free way in for a non-technical audience, reusing the
  entire proven text stack; audio cost/spend governed through the same virtual key as
  chat; swapping STT/TTS models is a backend config change, like chat.
- **Harder:** two more model calls per turn (latency and audio-token cost); a new
  **audio-native provenance UX** problem (how a listener perceives "draft vs verified" by
  ear, and how the `PROVENANCE` channel is surfaced when there is no screen); a bigger
  eval surface — the phase-4 gate must now also cover STT mishearings and spoken-track
  honesty, not just text answers.
- **Committed to:** voice never bypasses the text loop (no answer without navigation);
  audio never bypasses the gateway (no unapproved voice vendor); the spoken track never
  carries a fact the `PROVENANCE` channel can't back; the integrity contract stays single,
  with voice as a rendering of it.
- **Caveat — integrity now also depends on STT/TTS quality.** A mishearing can silently
  change the question; a robotic or wrong-emphasis TTS can undercut the spoken grounding
  cues. As in ADR-0003, a weaker approved model (or STT) may degrade these behaviours —
  the eval gate certifies a given audio stack as good enough, and may narrow scope or fall
  back to text-with-audio-readout if it isn't.

## Alternatives considered

- **Realtime speech-to-speech model (audio in → audio out, one model).** Lowest latency
  and the shiny default. **Rejected as the core:** it bypasses the agentic-navigation loop
  entirely — it cannot traverse the bundle, cite `okf/…` paths, or surface `status`, so it
  launders exactly the provenance ADR-0003 fought to keep. It is the "chat-with-your-docs
  SaaS" alternative in a new costume. Revisit only as a latency optimisation *after* a
  grounded pipeline works, and only if it can be constrained to the loop's tool outputs.
- **Client-side browser speech (Web Speech API) for STT/TTS.** Zero backend audio cost and
  no audio egress to the gateway. Tempting, but STT/TTS quality and availability vary by
  browser/OS, it forfeits central governance and a consistent approved-model choice, and it
  can't offer a self-hosted on-prem audio route. Keep as a possible thin-client *option*
  later; not the governed default.
- **A dedicated third-party voice-bot / IVR SaaS.** Fastest to a demo, but hands the audio
  of every question to a third party and can't honour the integrity extension. Rejected for
  the same reasons ADR-0003 rejected the docs-chat SaaS.
- **Bake `SPOKEN`/`PROVENANCE` into the shared ADR-0003 system prompt.** Simpler wiring, but
  couples a voice concern into the text loop and bloats the shared contract. Kept as an
  opt-in addendum instead, so the text path stays exactly as proven.

## Rollout (phased)

1. **Proof of concept** — STT → existing loop → TTS, headless, over a local checkout,
   through the gateway. Prove the spoken track stays honest and leaks no raw citation, and
   that an audio round-trip of the probe questions still yields grounded answers. (See the
   [voice-chat POC runbook](../runbooks/voice-chat-poc.md).)
2. **Voice in the thin hosted chat** — add push-to-talk to the ADR-0003 phase-2 web UI:
   mic capture → gateway STT → loop → gateway TTS → audio playback, with the `PROVENANCE`
   channel shown on screen alongside the audio.
3. **Audio-native integrity UX** — how "verified vs draft" reads by ear (earcons, spoken
   prefixes, a "show me the sources" affordance); a verified-only spoken mode.
4. **Guardrails & eval** — extend the phase-4 eval set with spoken-answer honesty and
   STT-robustness probes (mishearings, homophones, accents); wire into CI alongside
   `scripts/validate.py`.

## Open questions

- **Approved STT/TTS models & channel** — which the institution sanctions, and whether a
  self-hosted audio route (on-prem Whisper / TTS) is required for the data-egress posture.
  All candidates sit behind the [gateway](../sources/0002-litellm.md) either way.
- **Latency & turn-taking** — end-to-end budget across STT + loop (multi-turn navigation) +
  TTS; whether to stream partial TTS; barge-in / interruption handling. Deferred past the
  POC but the main UX risk.
- **Audio-only provenance** — if there is ever no screen (phone call, smart speaker), how
  the `PROVENANCE` channel is delivered at all, and whether voice should be screen-paired
  by policy.
- **Capturing spoken scenario-plans** — as in ADR-0003, whether notable generated analyses
  get captured back into the bundle as `draft` notes (now from a spoken exchange).
- **Cost** — audio tokens/minutes vs text; whether voice needs its own budget/virtual key
  under the gateway for separate accounting.

## Sources

- [ADR-0003: Leadership chat interface](0003-leadership-chat-interface.md) — the text loop,
  gateway boundary, and integrity contract this ADR wraps in a voice shell without changing.
- [LiteLLM](../sources/0002-litellm.md) — evidence that STT (`/v1/audio/transcriptions`)
  and TTS (`/v1/audio/speech`) are available in the same OpenAI format, through the same
  gateway, with per-key spend tracking and self-hostable audio routes.
- [OKF v0.1 specification](../sources/okf-v0-1-spec.md) — the navigable-bundle design the
  reused text loop depends on.

> **Provenance note:** this ADR is `status: draft` on purpose — a *proposed* design, not a
> built one. Its one hard **factual** claim — that STT/TTS run through the same
> OpenAI-format gateway with the same governance — is **verified** against the LiteLLM docs
> (accessed 2026-07-13) and recorded in [its source note](../sources/0002-litellm.md). What
> remains unproven is the **design judgment**: that a dual-channel spoken/shown answer keeps
> provenance honest on an audio channel for a real audience. Only the phase-1 POC — the
> integrity behaviours holding across an audio round-trip on an approved model — can move
> this to `verified` / *accepted*.
