# CLAUDE.md

## What this repository is

This is an **LLM-wiki**: a durable, inspectable knowledge base for a single effort,
kept as plain Markdown with YAML frontmatter under version control.

The knowledge base in `okf/` is an **[Open Knowledge Format (OKF) v0.1]** bundle — the
vendor-neutral spec Google Cloud published on 2026-06-12 for representing knowledge as
a directory of Markdown files that agents can read and exchange without translation. On
top of OKF's minimal core we add an **academic-integrity extension** so that every
claim carries its provenance and verification state.

This repo is itself a **clonable template**. To start a new effort: clone it, rewrite
the "Project" section below, empty the worked examples in `okf/*/` (keep the reserved
`index.md` files and `templates/`), and start writing notes.

[Open Knowledge Format (OKF) v0.1]: okf/sources/okf-v0-1-spec.md

## Claude's role

You are the curator and implementation assistant for this knowledge base. You help
capture, structure, verify, and maintain notes, and you treat knowledge artifacts as
project memory to be reviewed alongside code or project changes.

You maintain the wiki **when explicitly asked**, not automatically on every change.

## OKF alignment (the base format)

The `okf/` directory is the **OKF bundle**; the bundle root is `okf/` itself. OKF v0.1
requires exactly three things for conformance:

1. Every **non-reserved** `.md` file in the bundle has a parseable YAML frontmatter
   block.
2. Every such frontmatter block has a **non-empty `type`** field. (`type` is the only
   field OKF requires.)
3. The **reserved filenames** `index.md` (directory listing / progressive disclosure)
   and `log.md` (chronological change history) follow their prescribed role and are
   **not** used as concept documents.

OKF's other fields — `title`, `description`, `resource`, `tags`, `timestamp` — are
recommended but optional, and producers may add their own **extension keys**. Our
integrity fields (below) are exactly that: extension keys, **not part of OKF**.

**Reserved files (`index.md`, `log.md`) therefore carry no `type`.** Every other note
must.

See `okf/sources/okf-v0-1-spec.md` for the cited spec, and
`okf/decisions/0002-adopt-okf-v0-1.md` for why we adopted it (and where we diverge).

## Academic integrity — the core rule (our OKF extension)

This knowledge base is only as valuable as it is trustworthy. The following are
**baked-in conventions**, enforced by curation and review (not yet by CI):

1. **Sources required.** Any note that asserts a fact must cite evidence in its
   `sources:` frontmatter and in a `## Sources` section. A claim-bearing note with no
   sources is `status: draft` at best — never `verified`.
2. **Verification status.** Every note carries `status` (`draft | verified | disputed
   | stale`), plus `last_verified` and `verified_by`. Only mark `verified` when the
   sources have actually been checked against the claims.
3. **Claim-level provenance.** Where a specific claim rests on a specific source, link
   it inline to that source note so a reader can trace the fact to its evidence — not
   just the document as a whole.
4. **Staleness / review cadence.** Every note carries `review_by`. Past that date the
   note is due for re-verification; flip it to `stale` until re-checked.

When you add or edit a note, keep these fields honest. **Never invent a source, a
date, or a verification you did not perform.** If you cannot verify a claim, say so and
leave it `draft` or `disputed` — do not upgrade status to make a note look finished.

## Frontmatter schema

Standard (non-reserved) note — OKF fields first, then our extension block:

```yaml
---
# --- OKF v0.1 ---
type: concept            # REQUIRED, non-empty. concept | decision | architecture | runbook | source
title: Human Readable Title
description: One-line summary.
tags: [example]
timestamp: YYYY-MM-DD    # last meaningful update (OKF's recency field)
# --- integrity extension (NOT part of OKF) ---
status: draft            # draft | verified | disputed | stale
confidence: low          # low | medium | high
created: YYYY-MM-DD
last_verified:           # blank until actually verified
verified_by:
review_by: YYYY-MM-DD     # when this note must be re-checked
sources: []              # relative links to okf/sources/* notes; required if it makes claims
---
```

Reserved files (`index.md`, `log.md`) use a minimal block with **no `type`** — see
`okf/index.md` for the pattern. Source notes add evidence fields and may use OKF's
`resource` for the cited URL — see `okf/templates/source.md`.

## Note types

| Type           | Folder               | Reserved? | Use for                                       |
|----------------|----------------------|-----------|-----------------------------------------------|
| concept        | `okf/concepts/`      | no        | A reusable idea, term, or factual claim.      |
| decision       | `okf/decisions/`     | no        | An ADR: a decision, its context, consequences.|
| architecture   | `okf/architecture/`  | no        | How the system / effort is structured.        |
| runbook        | `okf/runbooks/`      | no        | A repeatable procedure.                        |
| source         | `okf/sources/`       | no        | The evidence store: one note per cited source.|
| (index)        | any folder           | **yes**   | `index.md` — directory listing. No `type`.    |
| (log)          | `okf/log.md`         | **yes**   | Dated change history. No `type`.              |

## Linking & Obsidian

- **Cross-link with relative Markdown links**: `[Schema](../concepts/okf-frontmatter-schema.md)`
  or `[Sibling](sibling.md)`. These are navigable in Obsidian (graph, backlinks,
  click-through) and resolvable by OKF consumers.
- OKF *recommends* bundle-root-absolute links (`/concepts/x.md`) for move-stability,
  but **Obsidian does not resolve leading-slash paths**, so we deliberately use relative
  links instead. Link style is not an OKF conformance criterion, so this stays
  conformant. See `okf/decisions/0002-adopt-okf-v0-1.md`.
- **Open `okf/` as the Obsidian vault** (not the repo root) so the vault equals the OKF
  bundle. In Settings → *Files and links*, turn **"Use [[Wikilinks]]" off** and set
  **"New link format" → "Relative path to file"** so Obsidian inserts links in the same
  style we use. `CLAUDE.md`/`README.md` live outside the bundle and are referenced in
  prose, not linked from notes.
- OKF consumers must tolerate broken links, so a link to a not-yet-written note is fine.

## Working principles

- Prefer plain Markdown, YAML frontmatter, and Git history before adding tooling.
- Keep notes small and single-purpose; link liberally with relative links.
- Update the relevant `index.md` and add a dated entry to `okf/log.md` for meaningful
  changes.
- Treat `docs/` as the optional publish surface; keep markdown portable.

## Roadmap (not built yet)

Deferred by choice, in rough order:

1. A `scripts/validate.py` that checks OKF conformance (frontmatter parseable,
   non-empty `type` on non-reserved files, reserved-file roles) plus our integrity
   rules (required `sources`, overdue `review_by`) — runnable locally.
2. CI (GitLab CI / GitHub Actions) that runs the validator on merge requests.
3. Issue + MR/PR templates wired to the integrity workflow.
4. A docs-site generator config for publishing `docs/`.

## Project

> Rewrite this section per effort when you clone the template.

- **Effort:** _(name and one-line purpose)_
- **Audience:** _(you / team / leadership / auditors / future agents)_
- **Hosting:** GitLab and/or GitHub; optional published docs site.
- **Sensitivity:** _(assume private by default; note any institutional constraints)_
