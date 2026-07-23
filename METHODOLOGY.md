# METHODOLOGY.md — how a recommendation is produced (and how to reproduce it)

This is the companion to the [decision-support extension](okf/architecture/decision-support-extension.md)
(ADR-[0006](okf/decisions/0006-decision-support-extension.md)). The **runbook** —
[Run a Decision-Support Effort](okf/runbooks/run-a-decision-support-effort.md) — is the
step-by-step *procedure*. This file is the *why*: the principles a reviewer relies on, the
division of labour, and how to reproduce the result on a new program. It lives outside the
`okf/` bundle (like `README.md` and `CLAUDE.md`) and is optional — delete it if you do pure
knowledge capture.

## What a decision-support effort delivers

A **recommendation, for reaction not decision**: a phased path (now / next / later) with the
genuinely-open choices handed back, every claim traceable to evidence with the same
provenance guarantees as any other note in the bundle. The whole point of building this
*inside* OKF (rather than as prose registers) is that the recommendation, its options, its
findings, and its gates are all machine-checkable by `scripts/validate.py`.

## The artifacts and where they live

The decision-support layer promotes what used to be sections-in-a-note into first-class,
validated note types (Phase 2). One note per thing:

| Type             | Folder                  | Holds                                                    |
|------------------|-------------------------|---------------------------------------------------------|
| `recommendation` | `okf/recommendations/`  | The decision, the matrix, the phased path, open decisions. |
| `option`         | `okf/options/`          | One evaluated option on the fixed schema (incl. ruled-out). |
| `criterion`      | `okf/criteria/`         | One evaluation criterion — a column of the matrix.       |
| `gate`           | `okf/gates/`            | A decision gate; append-only.                            |
| `finding`        | `okf/findings/`         | A review finding; append-only, severity-ranked.          |
| `risk`           | `okf/risks/`            | A risk; append-only, likelihood × impact.                |

Supporting tiers (no schema change): [`preso/`](preso/README.md) renders leadership decks
from Markdown; [`artifacts/`](artifacts/README.md) is git-ignored staging for raw inputs;
[`visual-vocabulary`](okf/concepts/visual-vocabulary.md) governs diagrams and slides.

## The principles a reviewer relies on

These are non-negotiable, and are what make the recommendation trustworthy rather than
merely tidy:

1. **Feasibility ≠ desirability.** `confidence` rates whether a mechanism *works*, kept
   strictly separate from whether anyone should *want* it. The two are never conflated to
   make a preferred option look inevitable.
2. **Every option on the same fixed schema.** Asymmetric depth is the commonest way a
   preferred option quietly wins; the ruled-out set gets the same rigor as the finalists.
3. **Strength-of-evidence travels with each claim** (Strong / Moderate / Weak + a reason),
   linked inline to the `source` it rests on.
4. **Absence-of-evidence is an explicit finding**, not a silent omission — often the
   load-bearing signal.
5. **Recommendation "for reaction, not decision."** Publish the decision frame and a phased
   path; hand the open choices back rather than pretending to close them.
6. **Registers are append-only.** A closed gate/finding/risk is never rewritten — a dated
   line is appended. "Closed via alternate path" is recorded when advice was not taken. The
   change history is the audit trail.
7. **Nothing is invented.** No fabricated source, date, or verification. A named gap beats a
   confident guess.

## Division of labour (producer / checker / lenses)

Pulling, synthesizing, writing, and checking are **separate roles** so no one signs off on
their own work (`.claude/agents/`):

- **[`ds-producer`](.claude/agents/ds-producer.md)** — writes the notes. Has write tools.
- **[`ds-checker`](.claude/agents/ds-checker.md)** — verifies provenance, honest status, and
  append-only discipline. **Read-only: it may not edit what it checks.** Fixes go back to the
  producer.
- **Review lenses**, run concurrently and blind to each other, each feeding the
  [findings register](okf/findings/index.md):
  [standards](.claude/agents/review-standards.md),
  [security](.claude/agents/review-security.md),
  [red-team](.claude/agents/review-redteam.md),
  [integrity](.claude/agents/review-integrity.md).

## How to reproduce this on a new program

1. Clone the template; rewrite the `## Project` section of `CLAUDE.md`.
2. Frame the decision as a `recommendation` note (who decides, and explicitly *what this is
   not*). Fix the `criterion` notes before scoring anything.
3. Enumerate `option` notes on the fixed schema; record ruled-out options with `viable: no`
   and the constraint that kills each.
4. Gather evidence into git-ignored `artifacts/`; sanitize into `source` notes; **cite the
   source note, never the raw artifact.**
5. Score the matrix in the `recommendation`, anchoring every non-trivial cell.
6. Run the review lenses; capture their output as `finding` notes; track exposures as `risk`
   notes and go/no-go points as `gate` notes.
7. Have `ds-checker` verify. Run `python3 scripts/validate.py` — clean of new warnings.
8. Optionally render the deck via `preso/`. Every slide claim traces back to a note.
9. Add the notes to their `index.md` files and a dated entry to `okf/log.md`.

A recommendation is not "done" because it looks finished. It is done when its evidence is
real, its status is honest, and a reviewer can trace every claim to its source.
