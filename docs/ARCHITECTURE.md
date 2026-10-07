# Architecture

## Boundary

CaseFoundry is a portfolio-scale offline tool. The CLI parses one PRD, creates versioned candidates, writes JSON reports, and seeds a local review database. It does not call a model or execute arbitrary generated code.

## Decisions

| Decision | Reason | Tradeoff |
|---|---|---|
| Explicit `[R#]` syntax | Makes traceability deterministic and testable | Requires authors to structure the source |
| Per-clause generation | Makes coverage gaps measurable | Cross-clause conflicts are not yet modeled |
| Structured inputs/expectations | Enables executable mutation tests | Needs a domain adapter for new products |
| Stable SHA-256 IDs | Replays do not create duplicate review work | Meaningful edits should bump generator version |
| Jaccard dedupe | Zero-cost and explainable | Weak semantic recall |
| Human review before promotion | Prevents synthetic noise entering a golden set | Adds reviewer workload |
| Seeded mutation runner | Measures defect-detection ability | Synthetic defects can be unrealistic |

## Artifact contracts

`cases.json` is an array of candidate cases. `coverage.json` contains clause counts, difficulty counts, and a mutation matrix. `reviews.db` stores the immutable candidate payload plus review status, reason, optional edited expectation, and timestamp.

## Production hardening

Add versioned PRD snapshots, semantic clause extraction with reviewer confirmation, domain-specific oracle adapters, calibrated semantic deduplication, authenticated reviewer assignment, immutable audit events, and incremental regeneration from PRD diffs. Run generated code only inside a resource-limited sandbox; this MVP deliberately avoids that risk.

