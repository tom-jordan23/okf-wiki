#!/usr/bin/env python3
"""Phase-1 POC runner for ADR-0003 (leadership chat).

Runs the fixed probe set (probes.json) through the agentic-navigation loop over a
read-only `okf/` checkout, routed through the configured gateway (internal self-hosted
LiteLLM or the external platform gateway), then reports on the integrity behaviors the
runbook demands:

  * every cited note path actually resolves in the bundle   -> ZERO fabricated citations
  * the unsupported probe is declined, not answered
  * (human check) statuses surfaced honestly; inference labeled -- see saved transcripts

Usage:
  python3 chat/run_poc.py --env-file chat/.env            # run the probe set
  python3 chat/run_poc.py --question "..."                # one ad-hoc question
  python3 chat/run_poc.py --dry-run                       # offline: exercise the loop with
                                                          #   a scripted fake model (no key)

Exit code is non-zero if any fabricated citation is found or the unsupported probe is not
declined. No third-party dependencies.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

import agent
from gateway import GatewayError, from_env, load_env_file
from navigator import Navigator

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BUNDLE = os.path.join(HERE, os.pardir, "okf")
DEFAULT_PROBES = os.path.join(HERE, "probes.json")
DEFAULT_OUT = os.path.join(HERE, "transcripts")

# A path-like token ending in .md, e.g. concepts/foo.md or okf/concepts/foo.md
_CITATION_RX = re.compile(r"(?<![\w/])((?:[\w.-]+/)*[\w.-]+\.md)")


def extract_citations(text: str) -> list[str]:
    """Pull candidate bundle-relative note paths out of an answer, normalized."""
    out = []
    for m in _CITATION_RX.findall(text or ""):
        p = m.strip().lstrip("./")
        if p.startswith("okf/"):  # tolerate the model prefixing the bundle name
            p = p[len("okf/"):]
        if p not in out:
            out.append(p)
    return out


def check_citations(nav: Navigator, cited: list[str]) -> tuple[list[str], list[str]]:
    """Split cited paths into (resolved, fabricated) against the real checkout."""
    resolved, fabricated = [], []
    for path in cited:
        target = os.path.realpath(os.path.join(nav.root, path))
        inside = target == nav.root or target.startswith(nav.root + os.sep)
        (resolved if inside and os.path.isfile(target) else fabricated).append(path)
    return resolved, fabricated


# --- offline dry-run model -----------------------------------------------------------

class _FakeGateway:
    """A scripted stand-in for a real gateway: proves the loop plumbing (tool calls ->
    results -> final answer) with no network and no API key. It navigates for real via
    the tools, then cites the note it read -- so the citation check exercises too."""

    def __init__(self, navigator: Navigator):
        self.nav = navigator
        self.model = "dry-run-fake"
        self.base_url = "(none)"
        self.api_key = ""
        self._step = 0
        # The runner sets this per-probe so the scripted model demonstrates the decline
        # path too: cite for answerable probes, decline (no citation) for the unsupported
        # one. Keeps the offline smoke test green while still exercising every check.
        self.decline_next = False

    def chat(self, messages, tools=None, tool_choice="auto"):
        if len(messages) == 2:  # fresh conversation (system + user) -> restart the script
            self._step = 0
        self._step += 1
        if self._step == 1:
            return self._tool_call("list_dir", {"path": "."})
        if self._step == 2:
            return self._tool_call("read_file", {"path": "index.md"})
        # Final turn. For a must-decline probe, decline with NO citation (exercises the
        # decline check); otherwise cite the note we actually read (exercises the
        # citation resolver). No file path appears in the decline text.
        if self.decline_next:
            text = ("[dry-run] The knowledge base has no note covering this, so I can't "
                    "answer it from the notes. Plumbing check: navigation ran, nothing to "
                    "cite.")
        else:
            text = ("[dry-run] Loop verified: the model listed the bundle and read "
                    "`index.md` (status per its frontmatter). This is a plumbing check, "
                    "not a real answer.")
        return {"choices": [{"message": {"role": "assistant", "content": text}}]}

    def _tool_call(self, name, args):
        return {"choices": [{"message": {
            "role": "assistant", "content": None,
            "tool_calls": [{
                "id": f"call_{self._step}", "type": "function",
                "function": {"name": name, "arguments": json.dumps(args)},
            }],
        }}]}


# --- reporting -----------------------------------------------------------------------

def run_one(probe, gw, nav, system_prompt, max_turns):
    result = agent.answer(
        probe["question"], gateway=gw, navigator=nav,
        system_prompt=system_prompt, max_turns=max_turns,
    )
    cited = extract_citations(result["final_text"])
    resolved, fabricated = check_citations(nav, cited)

    # Pass/fail signals the runbook's Verification section can be automated on.
    must_decline = probe.get("must_decline", False)
    failures = []
    if fabricated:
        failures.append(f"fabricated citation(s): {fabricated}")
    if must_decline and resolved:
        failures.append(f"expected a decline but the answer cited notes: {resolved}")
    if result["stopped"] == "max_turns":
        failures.append("hit max_turns without a final answer")

    return {
        "id": probe["id"], "type": probe["type"], "question": probe["question"],
        "expected_behavior": probe["expected_behavior"],
        "final_text": result["final_text"],
        "files_read": result["files_read"],
        "citations_resolved": resolved,
        "citations_fabricated": fabricated,
        "auto_failures": failures,
        "needs_human_review": True,  # status-honesty + inference-labeling are human-judged
        "transcript": result["transcript"],
    }


def print_report(reports):
    print("\n=== PROBE REPORT ===\n")
    any_fail = False
    for r in reports:
        status = "FAIL" if r["auto_failures"] else "ok"
        if r["auto_failures"]:
            any_fail = True
        print(f"[{status}] {r['id']} ({r['type']})")
        print(f"   Q: {r['question']}")
        print(f"   expected: {r['expected_behavior']}")
        print(f"   files read: {r['files_read'] or '(none)'}")
        print(f"   citations resolved: {r['citations_resolved'] or '(none)'}")
        if r["citations_fabricated"]:
            print(f"   !! FABRICATED: {r['citations_fabricated']}")
        for f in r["auto_failures"]:
            print(f"   !! {f}")
        answer_preview = (r["final_text"] or "(empty)").strip().replace("\n", " ")
        print(f"   answer: {answer_preview[:280]}")
        print()
    print("Automated checks cover fabricated citations + decline behavior only.")
    print("READ THE SAVED TRANSCRIPTS to judge status-honesty and inference-labeling")
    print("(runbook step 6 / Verification) -- those are human calls.\n")
    return any_fail


def main() -> int:
    ap = argparse.ArgumentParser(description="Run the ADR-0003 phase-1 POC probe set.")
    ap.add_argument("--bundle", default=DEFAULT_BUNDLE, help="okf/ checkout (default: ../okf)")
    ap.add_argument("--probes", default=DEFAULT_PROBES, help="probe set JSON")
    ap.add_argument("--env-file", help="KEY=VALUE file with gateway config (e.g. chat/.env)")
    ap.add_argument("--gateway", help="override profile: internal | external")
    ap.add_argument("--question", help="run a single ad-hoc question instead of the probe set")
    ap.add_argument("--out", default=DEFAULT_OUT, help="transcript output dir")
    ap.add_argument("--max-turns", type=int, default=12)
    ap.add_argument("--dry-run", action="store_true",
                    help="offline: exercise the loop with a scripted fake model (no gateway)")
    args = ap.parse_args()

    if args.env_file:
        load_env_file(args.env_file)

    try:
        nav = Navigator(args.bundle)
    except (NotADirectoryError, FileNotFoundError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    system_prompt = agent.load_system_prompt()

    if args.dry_run:
        gw = _FakeGateway(nav)
        print(f"[dry-run] fake model over bundle {nav.root} -- no network, no key.")
    else:
        try:
            gw = from_env(args.gateway)
        except GatewayError as e:
            print(f"gateway config error: {e}", file=sys.stderr)
            print("Hint: copy chat/gateways/internal.env.example to chat/.env and pass "
                  "--env-file chat/.env (or use --dry-run to test the loop offline).",
                  file=sys.stderr)
            return 2
        print(f"gateway profile via base_url={gw.base_url} model={gw.model}")

    # Single ad-hoc question.
    if args.question:
        probe = {"id": "adhoc", "type": "adhoc", "question": args.question,
                 "expected_behavior": "(ad-hoc)", "must_decline": False}
        if args.dry_run:
            gw.decline_next = False
        try:
            report = run_one(probe, gw, nav, system_prompt, args.max_turns)
        except GatewayError as e:
            print(f"gateway error: {e}", file=sys.stderr)
            return 2
        os.makedirs(args.out, exist_ok=True)
        with open(os.path.join(args.out, "adhoc.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        any_fail = print_report([report])
        return 1 if any_fail else 0

    # Full probe set.
    with open(args.probes, encoding="utf-8") as f:
        probes = json.load(f)["probes"]

    os.makedirs(args.out, exist_ok=True)
    reports = []
    for probe in probes:
        print(f"running probe: {probe['id']} ...")
        if args.dry_run:
            gw.decline_next = probe.get("must_decline", False)
        try:
            report = run_one(probe, gw, nav, system_prompt, args.max_turns)
        except GatewayError as e:
            print(f"gateway error on {probe['id']}: {e}", file=sys.stderr)
            return 2
        with open(os.path.join(args.out, f"{probe['id']}.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        reports.append(report)

    with open(os.path.join(args.out, "_summary.json"), "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2)

    any_fail = print_report(reports)
    print(f"transcripts saved to {args.out}/")
    return 1 if any_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
