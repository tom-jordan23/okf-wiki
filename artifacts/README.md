# artifacts/ — raw-input staging (git-ignored)

A staging area for the **raw source material** a decision-support effort collects: exported
spreadsheets, PDFs, meeting transcripts, screenshots, draft diagrams, vendor docs. This
directory (everything except this README) is **git-ignored**.

## Why nothing here is committed

- Raw inputs are often **private** — they name individuals, quote internal discussions, or
  reproduce licensed material.
- They are **unverified** — dumping them into the repo would smuggle unchecked claims past
  the integrity contract.

The bundle only ever contains **sanitized, summarized `source` notes** in `okf/sources/`
derived from these artifacts. That is where a raw input becomes citable evidence: read it,
write a `source` note (copy `okf/templates/source.md`) capturing what it supports and how
credible it is, and cite *that* — never the raw file.

## Workflow

```text
artifacts/from-someone/quarterly-export.xlsx   (raw, git-ignored, private)
        │  read + assess + summarize
        ▼
okf/sources/0007-quarterly-export.md           (sanitized source note, committed)
        │  cited by
        ▼
okf/architecture/…                             (the claim, linked to its source)
```

Suggested layout: one subfolder per provider of material (`artifacts/from-<name>/`), so
provenance is obvious even before the `source` notes exist.

## If you don't need it

Delete this directory. It is part of the optional decision-support extension, not the OKF
core. See [the extension roadmap](../okf/architecture/decision-support-extension.md).
