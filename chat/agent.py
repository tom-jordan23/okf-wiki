#!/usr/bin/env python3
"""The provider-agnostic agentic-navigation loop (ADR-0003 decision 1, runbook step 2/3).

An ordinary OpenAI-format tool-use loop: the model is given the read-only `Navigator`
tools over an `okf/` checkout plus the integrity system prompt, and it navigates the
bundle (`index.md` -> links -> grep -> read) to answer. It is deliberately NOT tied to
any provider -- it drives whatever approved model answers behind the gateway. (If the
approved model turns out to be Claude, the Claude Agent SDK supplies this same loop
pre-built; that is a Claude-only accelerator, never a dependency here.)

Returns a structured transcript so the POC runner can inspect *how* an answer was reached
-- which notes were actually opened -- not just the final prose.

No third-party dependencies -- stdlib only.
"""
from __future__ import annotations

import json
import os

from gateway import Gateway
from navigator import Navigator

DEFAULT_SYSTEM_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "system_prompt.md")


def load_system_prompt(path: str | None = None) -> str:
    with open(path or DEFAULT_SYSTEM_PROMPT_PATH, encoding="utf-8") as f:
        return f.read()


def _assistant_msg(raw: dict) -> dict:
    """Normalize the API's assistant message for echoing back into `messages`."""
    msg = {"role": "assistant", "content": raw.get("content")}
    if raw.get("tool_calls"):
        msg["tool_calls"] = raw["tool_calls"]
    return msg


def answer(question: str, *, gateway: Gateway, navigator: Navigator,
           system_prompt: str, max_turns: int = 12) -> dict:
    """Run the loop for one question.

    Returns a dict:
      {question, final_text, turns, tools_used, files_read, transcript, stopped}
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]
    tools = navigator.tool_specs()
    transcript = []
    files_read: list[str] = []
    tools_used: list[str] = []

    for turn in range(1, max_turns + 1):
        resp = gateway.chat(messages, tools=tools)
        choice = resp["choices"][0]
        raw = choice["message"]
        messages.append(_assistant_msg(raw))

        tool_calls = raw.get("tool_calls") or []
        if raw.get("content"):
            transcript.append({"turn": turn, "role": "assistant", "text": raw["content"]})

        if not tool_calls:
            return {
                "question": question,
                "final_text": raw.get("content") or "",
                "turns": turn,
                "tools_used": tools_used,
                "files_read": files_read,
                "transcript": transcript,
                "stopped": "final_answer",
            }

        # Execute each requested tool call and feed results back.
        for tc in tool_calls:
            name = tc["function"]["name"]
            try:
                arguments = json.loads(tc["function"].get("arguments") or "{}")
            except json.JSONDecodeError:
                arguments = {}
            result = navigator.dispatch(name, arguments)
            tools_used.append(name)
            if name == "read_file" and "path" in arguments:
                files_read.append(arguments["path"])
            transcript.append({
                "turn": turn, "role": "tool", "tool": name,
                "arguments": arguments, "result_preview": result[:500],
            })
            messages.append({
                "role": "tool", "tool_call_id": tc["id"], "content": result,
            })

    # Ran out of turns without a final text answer.
    return {
        "question": question,
        "final_text": "",
        "turns": max_turns,
        "tools_used": tools_used,
        "files_read": files_read,
        "transcript": transcript,
        "stopped": "max_turns",
    }
