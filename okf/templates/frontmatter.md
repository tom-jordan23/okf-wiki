---
# --- OKF v0.1 ---
type: concept
title: "Frontmatter Schema Reference"
description: The canonical field list every note copies — OKF core plus integrity extension.
tags: [meta, schema, okf]
timestamp: 2026-07-23
# --- integrity extension (NOT part of OKF) ---
status: verified
confidence: high
created: 2026-06-15
last_verified: 2026-07-23
verified_by: claude
review_by: 2026-12-15
sources:
  - ../sources/okf-v0-1-spec.md
---

# Frontmatter Schema Reference

The canonical field list every note copies. Two layers: the **OKF v0.1 core** (from the
[spec](../sources/okf-v0-1-spec.md)) and our **integrity extension** (custom keys OKF
explicitly permits). See `CLAUDE.md` for the integrity rules these fields serve.

## OKF v0.1 core fields

| Field        | Required | Format        | Meaning |
|--------------|----------|---------------|---------|
| `type`       | **yes**  | string        | Note type, non-empty. The only field OKF requires. Omitted on reserved `index.md`/`log.md`. |
| `title`      | rec.     | string        | Human-readable title. |
| `description`| rec.     | string        | One-line summary. |
| `resource`   | opt.     | string/URL    | The underlying resource a concept describes (e.g. a source note's cited URL). |
| `tags`       | opt.     | list          | Free-form tags. |
| `timestamp`  | rec.     | `YYYY-MM-DD`  | Last meaningful update (OKF's recency field). |

## Integrity extension fields (ours, not OKF)

| Field           | Required | Values / format                          | Meaning |
|-----------------|----------|------------------------------------------|---------|
| `status`        | yes      | `draft \| verified \| disputed \| stale` | Verification state. `verified` requires checked sources. |
| `confidence`    | yes      | `low \| medium \| high`                   | Your confidence in the claims given the sources. |
| `created`       | yes      | `YYYY-MM-DD`                              | First written. |
| `last_verified` | when verified | `YYYY-MM-DD`                        | When claims were last checked against sources. Blank if never. |
| `verified_by`   | when verified | name or agent                       | Who verified. |
| `review_by`     | yes      | `YYYY-MM-DD`                              | Re-check by this date or flip to `stale`. |
| `sources`       | if it makes claims | list of relative paths to `okf/sources/*` | Evidence backing the note's claims. |

Source notes add evidence fields (`source_type`, `author`, `publisher`, `url`,
`published`, `accessed`, `credibility`) — see `source.md`.

## Decision-support fields (extension, optional)

The [decision-support types](../architecture/decision-support-extension.md) (`option`,
`criterion`, `gate`, `finding`, `risk`, `recommendation`) add the fields below. `validate.py`
checks each enum and emits a **warning** (never an error — OKF permits any `type:`) when one
is missing or invalid. Ignore this whole table if you do pure knowledge capture.

| Field        | Types                     | Values / format                                   | Meaning |
|--------------|---------------------------|---------------------------------------------------|---------|
| `id`         | all six                   | `OPT-1`, `CRIT-3`, `GATE-1`, `FND-1`, `RISK-1`, `REC-1` | Stable cross-reference handle. **Not** OKF identity (still the file path) — a citable label for matrices, decks, and links. |
| `decision`   | option, criterion, recommendation | link or one-line              | The decision this note serves. |
| `viable`     | option                    | `yes \| no`                                        | `no` ⇒ it's in the ruled-out set; pair with `ruled_out_by`. |
| `ruled_out_by`| option                   | constraint name                                    | The constraint that kills a `viable: no` option. |
| `weight`     | criterion                 | `high \| medium \| low`                            | Optional: how much the criterion counts. |
| `state`      | gate, finding, risk       | per-type enum (below)                              | Append-only lifecycle — distinct from `status` (verification). |
| `severity`   | finding                   | `low \| medium \| high \| critical`                | How bad the finding is. |
| `lens`       | finding                   | `standards \| security \| red-team \| integrity \| …` | Which review lens raised it. |
| `likelihood` | risk                      | `low \| medium \| high`                            | Chance the risk is realized. |
| `impact`     | risk                      | `low \| medium \| high`                            | Cost if it is. |
| `options`    | recommendation            | list of option ids/links                           | The options weighed. |

**Register `state` enums** (append-only — never rewrite a closed row, append a dated line):

- `gate`: `open \| closed \| closed-alternate`
- `finding`: `open \| resolved \| closed-alternate \| wontfix`
- `risk`: `open \| mitigated \| accepted \| realized \| closed`

A `recommendation` must also contain an `## Open decisions` section (the "for reaction, not
decision" convention) — `validate.py` warns if it's missing.

## Identity & links

- **No `id` field.** In OKF the file path is the concept's identity.
- **Cross-link with relative Markdown links** (`../concepts/x.md`, `sibling.md`):
  navigable in Obsidian and OKF-conformant. Avoid `[[wikilinks]]` and leading-slash
  paths.

## Status lifecycle

```text
draft ──(sources cited & checked)──> verified ──(review_by passes)──> stale
   │                                      │                              │
   └──────────── disputed <──────────────┴──────────────────────────────┘
        (a source is contradicted or found unreliable)
```

- **draft** — written, not yet verified. Default for new claim-bearing notes.
- **verified** — sources exist and have been checked against the claims.
- **disputed** — evidence conflicts or a source was found unreliable; explain in body.
- **stale** — was verified, but `review_by` has passed; re-check before relying on it.
