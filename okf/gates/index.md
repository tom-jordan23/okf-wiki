---
# Reserved OKF file (index.md): directory listing — no `type`.
title: Gates Register
description: Decision gates — what must be true before the effort proceeds. Append-only.
tags: [meta, index, decision-support]
timestamp: 2026-07-23
# --- integrity extension (NOT part of OKF) ---
status: verified
review_by: 2027-06-15
---

# Gates (decision-gate register)

One note per decision gate: a question that must be answered before the effort proceeds.
**Append-only** — never rewrite a closed gate; append a dated resolution line. `state` is
`open | closed | closed-alternate` (use *closed-alternate* when the effort went a different
way than the gate contemplated). New note: copy `../templates/gate.md`.

| ID | Gate | State |
|----|------|-------|
| [GATE-1](EXAMPLE-datastore-launch-gate.md) | Backup/restore proven before launch | open |
