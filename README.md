# okf-wiki

A clonable template for an **LLM-wiki**: a durable, inspectable knowledge base for a
single effort, kept as plain Markdown + YAML frontmatter under version control.

The knowledge base in [`okf/`](okf/) is an **[Open Knowledge Format (OKF) v0.1]** bundle
— Google Cloud's vendor-neutral spec (published 2026-06-12) for agent-readable Markdown
knowledge — with an **academic-integrity extension** layered on top: every claim-bearing
note carries its sources, a verification status, and a re-review date, so the repository
stays trustworthy as it grows. Read [`CLAUDE.md`](CLAUDE.md) for the full operating
rules.

[Open Knowledge Format (OKF) v0.1]: okf/sources/okf-v0-1-spec.md

## Start a new effort

1. Clone or use this repo as a GitLab/GitHub template.
2. Rewrite the **Project** section at the bottom of `CLAUDE.md`.
3. Empty the worked-example notes in `okf/*/` (keep each reserved `index.md` and
   `templates/`), then start writing from the templates in `okf/templates/`.
4. Decide what to keep of the shipped **assistant** (below):
   - `chat/`, `deploy/`, and `scripts/` are reusable infrastructure — keep them as-is.
   - ADRs `0003`–`0005` and the sources they cite (`sources/0002-litellm.md`,
     `sources/0003-claude-agent-sdk.md`) *document that assistant* — keep them if you want
     the design recorded in your bundle, or delete them with the other examples. If you
     delete them, also drop the runbooks that reference them
     (`runbooks/{leadership-chat,voice-chat}-poc.md`, `runbooks/deploy-self-hosted.md`).
   - `chat/probes.json` is seeded against this template's example notes. The offline
     `--dry-run` still works against any bundle (it only reads `index.md`), but before a
     **real** probe run, re-point the probe questions/`expect_notes` at your own notes.

No build step or tooling is required for the notes — it's Markdown all the way down.

## Use it in Obsidian

Open the **`okf/` folder itself** as your vault (so the vault equals the OKF bundle).
Then, in Settings → *Files and links*:

- Turn **"Use [[Wikilinks]]" off**.
- Set **"New link format" → "Relative path to file."**

Now Obsidian inserts the same relative Markdown links we use, and graph view, backlinks,
and click-through all work. (We avoid Obsidian wikilinks and leading-slash absolute paths
so the bundle stays portable and OKF-consumable; see
[`okf/decisions/0002-adopt-okf-v0-1.md`](okf/decisions/0002-adopt-okf-v0-1.md).)

## Layout

```text
CLAUDE.md            # operating manual + integrity rules (read this first)
README.md            # this file
okf/                 # the OKF v0.1 bundle (bundle root = this dir; open as Obsidian vault)
  index.md           # reserved: hand-maintained map of the bundle (no type)
  log.md             # reserved: dated change history (no type)
  concepts/          # reusable ideas, terms, factual claims
  decisions/         # ADRs
  architecture/      # how the effort/system is structured
  runbooks/          # repeatable procedures
  sources/           # the evidence store: one note per cited source
  templates/         # frontmatter + per-type note templates
chat/                # the chat + voice assistant over the bundle (code, not notes)
deploy/              # one-command self-hosted deployment (Docker Compose)
docs/                # optional, portable publish surface
preso/               # optional: build leadership decks from Markdown (decision-support ext.)
artifacts/           # optional: git-ignored staging for raw inputs (decision-support ext.)
```

## Decision-support extension (optional)

The template started as a knowledge wiki, but its common use is **decision support** —
evaluate options against criteria and hand a reviewer a phased recommendation. An optional
extension supports that *inside* OKF, so recommendations keep the same provenance the rest
of the bundle has. It is additive and deletable; a pure knowledge-capture effort can ignore
it. See [ADR-0006](okf/decisions/0006-decision-support-extension.md) and the
[roadmap](okf/architecture/decision-support-extension.md). Phase 1 ships:

- The [Run a Decision-Support Effort](okf/runbooks/run-a-decision-support-effort.md) runbook
  (options → criteria → tradeoff matrix → recommendation *for reaction, not decision*), with
  a deletable worked example, [EXAMPLE: Datastore options](okf/architecture/EXAMPLE-datastore-options.md).
- [`preso/`](preso/README.md) — decks built from Markdown (Markdown is the source of record;
  every slide traces to a note). The only third-party dependency in the repo, and it is
  needed *only* here.
- [`artifacts/`](artifacts/README.md) — a git-ignored staging area for raw inputs; only
  sanitized `source` notes ever enter the bundle.

## Talk to your knowledge base (chat + voice)

The bundle ships with an optional **assistant**: an agentic read/grep loop over `okf/`
that answers questions **while keeping the integrity chain** — every answer shows the
exact notes it rests on and their `status`, flags draft support, and declines rather than
inventing a citation. It talks only to a model **gateway** (never a provider SDK), so
which model backs it is config, not code. Voice is the same loop with a speech-in / spoken
-answer shell around it. See the ADRs
([0003](okf/decisions/0003-leadership-chat-interface.md),
[0004](okf/decisions/0004-voice-interface.md),
[0005](okf/decisions/0005-self-deployable-environment.md)) for the design.

```sh
# 1. Prove the whole loop offline first — no gateway, no API key, no Docker:
python3 chat/run_poc.py --dry-run          # text; should end "exit 0", all probes [ok]
python3 chat/run_voice_poc.py --dry-run    # + STT/TTS pipeline, dual spoken/shown channels

# 2. Spin up the real web UI (text + push-to-talk) as one environment:
python3 deploy/bootstrap.py                # interview: dataset, egress posture, access token
cd deploy && docker compose up --build     # hosted (approved cloud model, BYO key)
#   ...or fully local, nothing leaves the host:
#   docker compose --profile no-egress up --build
open http://localhost:8080
```

Full instructions: [`chat/README.md`](chat/README.md) (the headless POC + gateway modes),
[`deploy/README.md`](deploy/README.md) (the deployable web/voice app and its two egress
profiles), and the runbooks for
[chat](okf/runbooks/leadership-chat-poc.md),
[voice](okf/runbooks/voice-chat-poc.md), and
[deployment](okf/runbooks/deploy-self-hosted.md).

## The integrity contract, in one breath

A note that makes factual claims must cite `sources:`; it is only `status: verified`
once those sources are actually checked; specific claims link inline to the source note
they rest on; and each note has a `review_by` date after which it is considered `stale`.
Never invent a source or a verification.

See `okf/templates/frontmatter.md` for the schema and
`okf/concepts/okf-frontmatter-schema.md` for a worked example.
