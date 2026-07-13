---
# --- OKF v0.1 ---
type: runbook
title: "Stand Up the Voice-Chat Proof of Concept (Phase 1)"
description: How to prove the integrity chain survives an audio channel — STT → the unchanged text loop → TTS, dual-channel spoken/shown answers — before any voice UI.
tags: [runbook, interface, voice, poc]
timestamp: 2026-07-13
# --- integrity extension (NOT part of OKF) ---
status: draft
confidence: medium
created: 2026-07-13
last_verified:
verified_by:
review_by: 2027-01-13
sources:
  - ../decisions/0004-voice-interface.md
  - ../decisions/0003-leadership-chat-interface.md
  - ../sources/0002-litellm.md
---

# Stand Up the Voice-Chat Proof of Concept (Phase 1)

> Phase 1 of [ADR-0004](../decisions/0004-voice-interface.md). Prove — headless, no UI —
> that wrapping the [phase-1 text loop](leadership-chat-poc.md) in a voice shell keeps the
> integrity chain **across an audio channel**: the answer is spoken honestly (draft flagged
> by ear, inference kept separate), no raw citation is read aloud, and a question spoken and
> transcribed back still drives the same grounded answer. This de-risks voice before any UI,
> latency, or turn-taking work.

## Prerequisites

- A working [leadership-chat phase-1 POC](leadership-chat-poc.md) — voice **reuses its loop
  unchanged**; do that runbook first.
- The same gateway, now also exposing the OpenAI-format **audio** endpoints
  `/v1/audio/transcriptions` (STT) and `/v1/audio/speech` (TTS)
  ([LiteLLM](../sources/0002-litellm.md) supports both). Any STT/TTS models you can
  legitimately call today are enough to prove the loop — certifying the *approved* audio
  stack is phase 4, not here.
- The voice-mode prompt addendum (step 3) appended to the text integrity system prompt.

## Steps

1. **Reuse the text loop unchanged.** Voice adds only a transcribe step before and a
   synthesize step after (ADR-0004 decision 1). Do **not** modify the navigation loop or the
   integrity system prompt — that is the proven, grounded part.
2. **Route STT and TTS through the same gateway** as chat (decision 2), so audio inherits
   the same virtual-key spend tracking and provider abstraction, and a self-hosted STT/TTS
   route can keep audio inside the institutional boundary. No separate voice vendor.
3. **Append the voice-mode addendum to the system prompt** (decision 4). It requires the
   model to emit **two channels**: `SPOKEN` (read aloud — no file paths; confidence carried
   in words like *"according to a verified note"* / *"this is only a draft, so treat it as
   provisional"* / *"this is my own analysis, not from the notes"*) and `PROVENANCE` (shown /
   logged — the note paths and each note's `status`). One integrity contract, two renderings.
4. **Run the reused probe set through the audio round-trip.** For each probe: speak the
   question (TTS), transcribe it back (STT), answer via the loop, split the answer, then TTS
   the `SPOKEN` track. This exercises STT mishearing on the way in and TTS on the way out
   without needing recordings.
5. **Read AND listen.** Confirm on each probe that: every path in `PROVENANCE` resolves to a
   real note; **no path leaked into `SPOKEN`**; the unsupported probe is declined with no
   citation; and — by ear — draft/stale support is flagged and inference is kept separate.

## Verification

- **Zero fabricated citations** in `PROVENANCE` — every cited path exists in the checkout.
- **Zero path leaks** into the `SPOKEN` channel — raw citations are never read aloud.
- The unsupported question is **declined**, spoken and in provenance, with no invented note.
- The audio round-trip does not change the answer's grounding — STT mishearings that flip the
  question are a finding, not a pass.
- By ear: draft/stale never sounds settled; inference never sounds like a cited fact.

`run_voice_poc.py` automates the first three (fabricated citations, path leaks, decline) and
reports whether a spoken grounding cue is present; the honesty-by-ear judgments are human
calls on the saved transcripts/audio.

## Rollback / recovery

If the spoken track launders draft into confident fact, blurs inference into grounded claims,
reads citations aloud, or STT mishearings silently change answers: **do not advance to phase
2.** Tighten the voice addendum, keep voice **screen-paired** (show `PROVENANCE` while
speaking), or fall back to a text-with-audio-readout mode. If a weaker STT/TTS or model simply
can't hold these behaviours, that is a **capability finding** for the phase-4 approved-stack
eval gate — record it; do **not** relax the integrity rules to make the POC pass.

## Sources

- [ADR-0004: Voice interface](../decisions/0004-voice-interface.md) — the design this
  procedure executes (phase 1).
- [ADR-0003: Leadership chat interface](../decisions/0003-leadership-chat-interface.md) —
  the text loop and integrity contract voice reuses unchanged.
- [LiteLLM](../sources/0002-litellm.md) — the gateway's audio endpoints STT/TTS route through.
