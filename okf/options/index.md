---
# Reserved OKF file (index.md): directory listing — no `type`.
title: Options Index
description: Options under evaluation, each on the same fixed schema.
tags: [meta, index, decision-support]
timestamp: 2026-07-23
# --- integrity extension (NOT part of OKF) ---
status: verified
review_by: 2027-06-15
---

# Options

One note per evaluated option. Every option uses the **same fixed schema** (thesis /
configures / retires / does not retire / cost / governance / risk / why viable) so none is
under-examined. Ruled-out options stay here with `viable: no` and the constraint that kills
them — so they don't resurface as "did you consider…". New note: copy `../templates/option.md`.

- [EXAMPLE: Managed Postgres](EXAMPLE-datastore-managed-pg.md) — OPT-1, `viable: yes`.
- [EXAMPLE: Shared company database (ruled out)](EXAMPLE-datastore-shared-db.md) — OPT-4, `viable: no`.
