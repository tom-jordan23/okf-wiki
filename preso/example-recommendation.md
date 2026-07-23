# Datastore for the new service
> A recommendation for reaction — not a decision to rubber-stamp.

Notes:
This deck renders the worked example note okf/architecture/EXAMPLE-datastore-options.md.
Every slide below traces back to a section of that note. Delete this deck (and that note)
when you start a real effort. All figures are illustrative fiction.

---

## The decision
> Which datastore backs the new internal service at launch?

- Three viable paths: managed Postgres, self-hosted Postgres, serverless store
- Not in scope: analytics/warehouse and caching — transactional primary store only

Notes:
Traces to the "Frame" section. Lead with the scope boundary; it is the most common place
a recommendation drifts.

---

## How we judged them
> Five criteria, fixed before any scoring.

- Time-to-first-write, operational load, reversibility
- Cost at low scale, scale headroom

Notes:
Traces to "Criteria". Criteria are the matrix columns — fixed up front so options can't be
scored on a moving target.

---

## The options at a glance
> Same schema for each, so none is under-examined.

- A — Managed Postgres: least ops, some managed lock-in
- B — Self-hosted Postgres: fully portable, ops load is ours
- C — Serverless store: cheapest when idle, highest lock-in

Notes:
Traces to "Options". Asymmetric depth is how a preferred option quietly wins, so each gets
the identical thesis/cost/risk schema in the note.

---

## Recommendation
> A phased path, with the open choices handed back.

- Now: start on A (managed Postgres) — retires launch-critical criteria at lowest risk
- Next: evaluate C for spiky workloads only, lock-in accepted knowingly
- Later: revisit B only if residency/cost forces self-hosting

Notes:
Traces to "Recommendation (for reaction, not decision)". Open decisions for the reviewer:
(1) is managed lock-in acceptable, or is portability a day-one requirement? (2) what traffic
threshold triggers the "next" re-evaluation?
