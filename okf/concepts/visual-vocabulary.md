---
# --- OKF v0.1 ---
type: concept
title: "Visual Vocabulary (decision-support design system)"
description: The house rules for diagrams and decks — CVD-safe, colour encodes ownership only, a shape/line lexicon, and a tiered Mermaid→SVG→pptx pipeline.
tags: [concept, decision-support, design-system, visual]
timestamp: 2026-07-23
# --- integrity extension (NOT part of OKF) ---
status: draft
confidence: medium
created: 2026-07-23
last_verified:
verified_by:
review_by: 2027-01-23
sources: []
---

# Visual Vocabulary (decision-support design system)

> A small, fixed set of rules so every diagram and deck slide in a decision-support effort
> reads as one system — and so no fact ever lives only inside a picture. Part of the
> optional [decision-support extension](../architecture/decision-support-extension.md);
> delete it with the rest if you do pure knowledge capture.

## Summary

Decision-support visuals fail in two ways: they encode meaning no colour-blind reader can
see, and they drift from the notes they claim to summarize. This vocabulary fixes both. It
is a **convention**, not a tool — the rules apply whether a diagram is hand-drawn Mermaid or
a generated slide.

## The rules

- **CVD-safe first.** Assume ~8% of male readers cannot distinguish red from green. Never
  encode meaning by hue alone — pair every colour with a second channel (shape, label,
  position, or line style). A diagram must survive being printed greyscale.
- **Colour encodes ownership only.** Hue means *who owns / who runs this* — one team, one
  colour — and nothing else. Status, severity, and recommendation strength are carried by
  **shape and label**, never by colour, so a reader never has to ask "does red mean *bad* or
  mean *team B*?".
- **A fixed shape / line lexicon.** Decide the lexicon once and reuse it:
  rectangle = component, rounded = external boundary, diamond = a [gate](../gates/index.md);
  solid line = data/control flow, dashed = proposed/not-yet-built, dotted = out of scope.
  A new shape means a new meaning — don't improvise.
- **Recommendation-strength is explicit, not chromatic.** `✓ strong / ~ partial / ✗ weak`
  in matrices; "now / next / later" for phasing. The same marks the runbook and templates use.

## The tiered pipeline

Visuals are **generated from a declarative source, never hand-edited** — so no fact lives
only inside a diagram (the same contract `preso/` enforces for decks):

1. **Mermaid** in a note — the default. Version-controlled text, diffs cleanly, renders in
   Obsidian and most viewers. The Markdown is the source of record.
2. **SVG** — when a diagram outgrows Mermaid, generate SVG from a declarative source; keep
   the source in the repo, treat the SVG as a build artifact.
3. **pptx** — the [`preso/`](../../preso/README.md) deck tier renders the final slide. Every
   slide claim still traces back to an `okf/` note.

Regenerate at every tier; never tweak the output and let it fork from the source.

## Claims

- CVD-safe encoding (not relying on hue alone) is an accessibility baseline, not a
  preference. *(Stated here as a house rule; when an effort needs to defend it, cite a WCAG
  / colour-vision source note — this concept ships none, so it stays `draft`.)*
- The "generated, never hand-edited" contract is the same one
  [`preso/`](../../preso/README.md) already enforces for decks; this concept extends it to
  all visuals. *(Self-sourced convention.)*

## Sources

- None yet. These are house rules for this template's decision-support layer (self-sourced).
  Promote to `verified` only once the accessibility claims are backed by a real `source`
  note (e.g. WCAG contrast / colour-vision guidance).
