---
# --- OKF v0.1 ---
type: concept
title: "Frontmatter Schema Reference"
description: The canonical field list every note copies — OKF core plus integrity extension.
tags: [meta, schema, okf]
timestamp: 2026-06-15
# --- integrity extension (NOT part of OKF) ---
status: verified
confidence: high
created: 2026-06-15
last_verified: 2026-06-15
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
