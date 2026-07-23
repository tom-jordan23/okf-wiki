---
# Reserved OKF file (index.md): directory listing — no `type`.
title: Findings Register
description: Review findings that gate circulation. Append-only, severity-ranked.
tags: [meta, index, decision-support]
timestamp: 2026-07-23
# --- integrity extension (NOT part of OKF) ---
status: verified
review_by: 2027-06-15
---

# Findings (review register)

One note per review finding, optionally raised by a distinct reviewer lens (standards,
security, red-team, integrity). **Append-only** — a finding closed by a path other than the
one advised is recorded as `closed-alternate`, never silently dropped. New note: copy
`../templates/finding.md`.

| ID | Finding | Severity | State |
|----|---------|----------|-------|
| [FND-1](EXAMPLE-lockin-review.md) | Serverless lock-in understated in the matrix | high | open |
