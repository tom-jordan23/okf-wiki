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
3. Empty the worked examples in `okf/*/` (keep each reserved `index.md` and `templates/`).
4. Start writing notes from the templates in `okf/templates/`.

No build step or tooling is required — it's Markdown all the way down.

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
docs/                # optional, portable publish surface
```

## The integrity contract, in one breath

A note that makes factual claims must cite `sources:`; it is only `status: verified`
once those sources are actually checked; specific claims link inline to the source note
they rest on; and each note has a `review_by` date after which it is considered `stale`.
Never invent a source or a verification.

See `okf/templates/frontmatter.md` for the schema and
`okf/concepts/okf-frontmatter-schema.md` for a worked example.
