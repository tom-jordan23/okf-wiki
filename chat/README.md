# Leadership-chat POC (ADR-0003, phase 1)

A headless proof of concept for the leadership-chat interface described in
[ADR-0003](../okf/decisions/0003-leadership-chat-interface.md), executing the
[phase-1 runbook](../okf/runbooks/leadership-chat-poc.md).

It proves — with **no UI and no hosting** — that a **provider-agnostic agentic-navigation
loop** over the `okf/` bundle can answer leadership-style questions **while keeping the
integrity chain**: real note-level citations, honest `status`, and grounded facts kept
separate from inference. This is the gate before any UI is built, and the probe set here
is the seed of the phase-4 eval fixture.

> Scope: this is phase 1 only. No web app, no auth, no `git pull` scheduling — those are
> phases 2+. It answers from whatever bundle checkout you point it at, right now.

## What's here

| File | Role |
|------|------|
| `navigator.py` | Read-only `read_file` / `list_dir` / `grep` tools **scoped to the `okf/` checkout** (path-escape rejected). The reusable bundle-navigation capability — the thing ADR-0003 decision 6 says to keep packaged so it can later become an MCP server. |
| `gateway.py` | Provider-agnostic **OpenAI-format** chat client (stdlib `urllib`). Selects the **internal** or **external** gateway from config. The app talks only to this — never a provider SDK. |
| `agent.py` | The tool-use loop: system prompt + navigator + gateway → answer + structured transcript. |
| `system_prompt.md` | The integrity system prompt (cite paths, surface `status`, separate inference, never invent a source). |
| `probes.json` | The fixed 4-probe set + expected behaviors (verified lookup / draft-only / scenario / unsupported). |
| `run_poc.py` | Runs the probe set, saves transcripts, auto-checks for **fabricated citations** and **decline** behavior. |
| `gateways/` | Internal LiteLLM starter config + `*.env.example` templates for both gateway modes. |

No third-party dependencies in the POC code itself — stdlib Python 3 only, same as
`scripts/validate.py`. (LiteLLM, if you self-host it, runs as a **separate process**; the
POC only ever speaks HTTP to it.)

## The two gateway modes

Per ADR-0003 the gateway is an *interface, not an instance*. Both modes speak the same
`POST {base_url}/chat/completions` API, so **switching between them is just the `.env`** —
no code change.

- **internal** — a LiteLLM proxy you self-host (`gateways/internal.litellm.yaml`). The
  interim option while the platform team's shared gateway is in progress. Which real model
  backs it is a backend config choice; the POC only ever asks for a model *alias*.
- **external** — the platform team's shared LiteLLM + MCP AI gateway (or any other
  OpenAI-compatible endpoint). Preferred once available — consuming it is a config change.

Configuration is read from the environment (keeps keys out of the repo). Three variables
carry everything: `OKF_CHAT_GATEWAY` (`internal`|`external`), `OKF_CHAT_BASE_URL`,
`OKF_CHAT_API_KEY`, `OKF_CHAT_MODEL`.

## Quick start

### 0. Offline smoke test — no gateway, no key

Exercises the whole loop (tool calls → results → final answer → citation check) with a
scripted fake model, so you can confirm the plumbing before wiring a real model:

```sh
python3 chat/run_poc.py --dry-run
```

### 1a. Internal gateway (self-hosted LiteLLM)

```sh
pip install 'litellm[proxy]'                       # separate process; POC imports no SDK
# edit chat/gateways/internal.litellm.yaml to point the `okf-chat-model` alias at a model
export MASTER_KEY=sk-local-dev-please-change
litellm --config chat/gateways/internal.litellm.yaml --port 4000 &

cp chat/gateways/internal.env.example chat/.env    # then edit chat/.env
python3 chat/run_poc.py --env-file chat/.env
```

### 1b. External gateway (platform team's service)

```sh
cp chat/gateways/external.env.example chat/.env    # fill in base URL, virtual key, model
python3 chat/run_poc.py --env-file chat/.env
```

### Ask one ad-hoc question

```sh
python3 chat/run_poc.py --env-file chat/.env --question "What does OKF require on a note?"
```

## Reading the results

`run_poc.py` prints a per-probe report and writes full transcripts to
`chat/transcripts/` (git-ignored — they may contain answer content).

**The automated checks only cover two things** — that every cited path resolves to a real
note (**zero fabricated citations**) and that the unsupported probe is **declined**. The
harder integrity judgments — is each note's `status` surfaced honestly? is inference kept
visibly separate from grounded fact? — are **human calls**. Open the transcripts and check
them (runbook step 6). A non-zero exit means a fabricated citation or a missing decline.

## Rollback rule (from the runbook)

If the model fabricates citations, launders `draft` support into confident fact, or blurs
inference into grounded claims: **do not advance to phase 2.** Tighten `system_prompt.md`,
narrow scope, or fall back to whole-bundle-in-context. If a weaker model simply can't hold
these behaviors, that's a **model-capability finding** for the phase-4 approved-model eval
gate — record it; do **not** relax the integrity rules to make the POC pass.
