#!/usr/bin/env python3
"""Phase-1 voice POC runner for ADR-0004 (voice over the leadership chat).

Proves -- headless, no UI -- that wrapping the ADR-0003 text loop in a voice shell keeps
the integrity chain across an audio channel:

  question  --[STT]-->  heard text  --[unchanged agent.py loop]-->  answer
  answer split into SPOKEN (heard) + PROVENANCE (shown)  --[TTS]-->  spoken audio

It reuses the ADR-0003 probe set and its citation checks verbatim (run on the PROVENANCE
channel), and adds the voice-specific gate from ADR-0004 decision 3: **no note path may
leak into the SPOKEN channel** (raw citations are unlistenable and must be carried as
spoken confidence cues, not read aloud).

Both STT and TTS go through the SAME gateway as chat (ADR-0004 decision 2); see voice.py.

Usage:
  python3 chat/run_voice_poc.py --dry-run                    # offline: fake STT/TTS + model
  python3 chat/run_voice_poc.py --env-file chat/.env         # probe set through the gateway
  python3 chat/run_voice_poc.py --env-file chat/.env --round-trip
                                                             # TTS each probe Q, STT it back,
                                                             # then answer -- exercises STT
  python3 chat/run_voice_poc.py --env-file chat/.env --audio q.wav
                                                             # answer one spoken question file

Exit code is non-zero if any probe fabricates a citation, fails to decline the unsupported
probe, or leaks a note path into the spoken channel. No third-party dependencies.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import agent
from gateway import GatewayError, from_env as gateway_from_env, load_env_file
from navigator import Navigator
from run_poc import DEFAULT_BUNDLE, DEFAULT_PROBES, check_citations, extract_citations
import voice as voice_mod

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.join(HERE, "transcripts", "voice")
VOICE_ADDENDUM = os.path.join(HERE, "voice_addendum.md")

# Plain-speech grounding cues the SPOKEN channel is supposed to use instead of paths/badges
# (ADR-0004 decision 3). Presence is a *reported* signal, not a hard gate -- honest phrasing
# is a human call -- but a grounded answer with none of these is worth flagging for review.
_GROUNDING_CUES = ("verified note", "draft", "provisional", "my own", "my analysis",
                   "not from the notes", "doesn't have", "does not have", "not covered",
                   "knowledge base doesn")


def voice_system_prompt() -> str:
    base = agent.load_system_prompt()
    with open(VOICE_ADDENDUM, encoding="utf-8") as f:
        return base + "\n\n" + f.read()


# --- offline dry-run doubles ---------------------------------------------------------

class _FakeVoiceGateway:
    """Scripted model that navigates for real, then answers in SPOKEN/PROVENANCE form
    citing the note it actually read -- so both the citation check and the leak check
    exercise on real output. No network, no key."""

    def __init__(self, navigator):
        self.nav = navigator
        self.model = "dry-run-fake"
        self.base_url = "(none)"
        self.api_key = ""
        self._step = 0

    def chat(self, messages, tools=None, tool_choice="auto"):
        if len(messages) == 2:
            self._step = 0
        self._step += 1
        if self._step == 1:
            return self._tool_call("list_dir", {"path": "."})
        if self._step == 2:
            return self._tool_call("read_file", {"path": "index.md"})
        text = (
            "SPOKEN:\n"
            "According to a verified note, this is a plumbing check: I listed the bundle "
            "and read its index. This is my own note, not a real answer. I can show you "
            "the exact notes if you'd like.\n\n"
            "PROVENANCE:\n"
            "index.md - verified"
        )
        return {"choices": [{"message": {"role": "assistant", "content": text}}]}

    def _tool_call(self, name, args):
        return {"choices": [{"message": {
            "role": "assistant", "content": None,
            "tool_calls": [{"id": f"call_{self._step}", "type": "function",
                            "function": {"name": name, "arguments": json.dumps(args)}}],
        }}]}


class _FakeVoice:
    """STT = identity (returns the text it was 'given'); TTS = a stub byte string.
    Lets the whole pipeline run offline so plumbing is proven before wiring real models."""

    tts_format = "txt"

    def __init__(self):
        self._last_text = ""

    def synthesize(self, text: str) -> bytes:
        self._last_text = text
        return ("[dry-run fake audio for]: " + text).encode("utf-8")

    def transcribe(self, audio: bytes, filename: str = "q.wav") -> str:
        # Identity round-trip: recover the text we 'spoke', mimicking a clean STT pass.
        s = audio.decode("utf-8", errors="replace")
        prefix = "[dry-run fake audio for]: "
        return s[len(prefix):] if s.startswith(prefix) else s


# --- one probe -----------------------------------------------------------------------

def run_one(probe, gw, vc, nav, system_prompt, *, max_turns, round_trip, out_dir,
            heard_override=None, dry_run=False):
    question = probe["question"]

    # 1. Get the "heard" question. --audio supplies it directly; --round-trip speaks the
    #    probe question and transcribes it back (exercising STT); otherwise text goes
    #    straight in.
    stt_note = "text (no STT)"
    if heard_override is not None:
        heard = heard_override
        stt_note = "from --audio"
    elif round_trip:
        audio = vc.synthesize(question)
        heard = vc.transcribe(audio)
        stt_note = "TTS->STT round-trip" + (" (faked)" if dry_run else "")
    else:
        heard = question

    # 2. Unchanged agentic-navigation loop over the heard text.
    result = agent.answer(heard, gateway=gw, navigator=nav,
                          system_prompt=system_prompt, max_turns=max_turns)

    # 3. Split the answer into the heard channel and the shown channel.
    spoken, provenance = voice_mod.split_channels(result["final_text"])

    # 4. ADR-0003 citation checks -- run on the PROVENANCE (shown) channel.
    cited = extract_citations(provenance)
    resolved, fabricated = check_citations(nav, cited)

    # 5. ADR-0004 voice gate -- no note path may leak into the SPOKEN (heard) channel.
    leaks = voice_mod.leaked_paths(spoken)

    must_decline = probe.get("must_decline", False)
    has_cue = any(c in spoken.lower() for c in _GROUNDING_CUES)
    failures = []
    if fabricated:
        failures.append(f"fabricated citation(s) in PROVENANCE: {fabricated}")
    if must_decline and resolved:
        failures.append(f"expected a decline but PROVENANCE cited notes: {resolved}")
    if leaks:
        failures.append(f"note path(s) leaked into the SPOKEN channel: {leaks}")
    if not spoken:
        failures.append("no SPOKEN channel produced")
    if result["stopped"] == "max_turns":
        failures.append("hit max_turns without a final answer")

    # 6. Synthesize the spoken track to an audio file (proves the TTS leg end to end).
    audio_path = None
    tts_error = None
    try:
        audio_bytes = vc.synthesize(spoken) if spoken else b""
        if audio_bytes:
            os.makedirs(out_dir, exist_ok=True)
            audio_path = os.path.join(out_dir, f"{probe['id']}.{vc.tts_format}")
            with open(audio_path, "wb") as f:
                f.write(audio_bytes)
    except GatewayError as e:
        tts_error = str(e)

    return {
        "id": probe["id"], "type": probe["type"], "question": question,
        "heard_question": heard, "stt": stt_note,
        "expected_behavior": probe["expected_behavior"],
        "spoken": spoken, "provenance": provenance,
        "spoken_has_grounding_cue": has_cue,
        "citations_resolved": resolved, "citations_fabricated": fabricated,
        "spoken_path_leaks": leaks,
        "audio_out": audio_path, "tts_error": tts_error,
        "auto_failures": failures,
        "needs_human_review": True,  # is the spoken track honestly phrased? human call.
        "files_read": result["files_read"],
        "transcript": result["transcript"],
    }


def print_report(reports):
    print("\n=== VOICE PROBE REPORT ===\n")
    any_fail = False
    for r in reports:
        status = "FAIL" if r["auto_failures"] else "ok"
        any_fail = any_fail or bool(r["auto_failures"])
        print(f"[{status}] {r['id']} ({r['type']})  [{r['stt']}]")
        print(f"   Q (asked): {r['question']}")
        if r["heard_question"].strip() != r["question"].strip():
            print(f"   Q (heard): {r['heard_question']}")
        print(f"   expected: {r['expected_behavior']}")
        print(f"   PROVENANCE cited: {r['citations_resolved'] or '(none)'}")
        cue = "yes" if r["spoken_has_grounding_cue"] else "NO -- review phrasing"
        print(f"   spoken grounding cue: {cue}")
        if r["spoken_path_leaks"]:
            print(f"   !! PATH LEAK in spoken channel: {r['spoken_path_leaks']}")
        if r["citations_fabricated"]:
            print(f"   !! FABRICATED: {r['citations_fabricated']}")
        for f in r["auto_failures"]:
            print(f"   !! {f}")
        spoken_preview = (r["spoken"] or "(empty)").strip().replace("\n", " ")
        print(f"   SPOKEN: {spoken_preview[:240]}")
        print(f"   audio out: {r['audio_out'] or ('(TTS error: ' + r['tts_error'] + ')' if r['tts_error'] else '(none)')}")
        print()
    print("Automated checks: fabricated citations, decline behavior, and spoken-channel")
    print("path leaks. Whether the SPOKEN track is *honestly phrased* (draft flagged by")
    print("ear, inference kept separate) is a HUMAN call -- listen to the audio / read the")
    print("saved transcripts (ADR-0004 phase-1 runbook).\n")
    return any_fail


def main() -> int:
    ap = argparse.ArgumentParser(description="Run the ADR-0004 phase-1 voice POC.")
    ap.add_argument("--bundle", default=DEFAULT_BUNDLE, help="okf/ checkout (default ../okf)")
    ap.add_argument("--probes", default=DEFAULT_PROBES, help="probe set JSON")
    ap.add_argument("--env-file", help="KEY=VALUE gateway config (e.g. chat/.env)")
    ap.add_argument("--question", help="one ad-hoc text question instead of the probe set")
    ap.add_argument("--audio", help="one spoken question (audio file) -- STT then answer")
    ap.add_argument("--round-trip", action="store_true",
                    help="TTS each probe question then STT it back before answering")
    ap.add_argument("--out", default=DEFAULT_OUT, help="output dir for audio + transcripts")
    ap.add_argument("--max-turns", type=int, default=12)
    ap.add_argument("--dry-run", action="store_true",
                    help="offline: fake STT/TTS + scripted model (no gateway, no key)")
    args = ap.parse_args()

    if args.env_file:
        load_env_file(args.env_file)

    try:
        nav = Navigator(args.bundle)
    except (NotADirectoryError, FileNotFoundError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    system_prompt = voice_system_prompt()

    if args.dry_run:
        gw = _FakeVoiceGateway(nav)
        vc = _FakeVoice()
        print(f"[dry-run] fake model + fake STT/TTS over bundle {nav.root} -- no network.")
    else:
        try:
            gw = gateway_from_env()
            vc = voice_mod.from_env()
        except GatewayError as e:
            print(f"gateway/voice config error: {e}", file=sys.stderr)
            print("Hint: copy chat/gateways/internal.env.example to chat/.env, add the STT/TTS "
                  "model vars, and pass --env-file chat/.env (or --dry-run to test offline).",
                  file=sys.stderr)
            return 2
        print(f"gateway base_url={gw.base_url} chat={gw.model} "
              f"stt={vc.stt_model or 'UNSET'} tts={vc.tts_model or 'UNSET'}")

    heard_override = None
    probes = None
    if args.audio:
        if args.dry_run:
            print("--audio needs a real gateway (STT); use --round-trip with --dry-run instead.",
                  file=sys.stderr)
            return 2
        with open(args.audio, "rb") as f:
            heard_override = vc.transcribe(f.read(), filename=os.path.basename(args.audio))
        probes = [{"id": "audio", "type": "adhoc", "question": "(from audio)",
                   "expected_behavior": "(ad-hoc spoken question)", "must_decline": False}]
    elif args.question:
        probes = [{"id": "adhoc", "type": "adhoc", "question": args.question,
                   "expected_behavior": "(ad-hoc)", "must_decline": False}]
    else:
        with open(args.probes, encoding="utf-8") as f:
            probes = json.load(f)["probes"]

    os.makedirs(args.out, exist_ok=True)
    reports = []
    for probe in probes:
        print(f"running voice probe: {probe['id']} ...")
        try:
            report = run_one(probe, gw, vc, nav, system_prompt,
                             max_turns=args.max_turns, round_trip=args.round_trip,
                             out_dir=args.out, heard_override=heard_override,
                             dry_run=args.dry_run)
        except GatewayError as e:
            print(f"gateway error on {probe['id']}: {e}", file=sys.stderr)
            return 2
        with open(os.path.join(args.out, f"{probe['id']}.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        reports.append(report)

    with open(os.path.join(args.out, "_summary.json"), "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2)

    any_fail = print_report(reports)
    print(f"transcripts + audio saved to {args.out}/")
    return 1 if any_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
