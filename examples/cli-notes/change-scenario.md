# Change scenario — cli-notes

Starting point: `before/` (all documents v1, approved; T-M1-1 done). Result: `after/`.

## What the user said

1. Added: "Early users want to get their notes out as Markdown." → V-4, R-M2-2.
2. Changed: "Search must be case-insensitive and highlight matches." → R-M1-2 reworded;
   this makes scanning a JSON file too slow for V-3.
3. Removed: "Nobody asked for tags; drop them for now." → R-M1-3 and T-M1-3 dropped.

## Current state

| Item | State |
|---|---|
| T-M1-1 (CLI + JSON store) | done |
| T-M1-2 (search) | not started |
| T-M1-3 (tags) | not started |

## Impact table

| Changed item | Affects | Already implemented? | Verdict |
|---|---|---|---|
| V-4 added | roadmap (R-M2-2), todo (none yet) | no | keep everything; add R-M2-2 |
| R-M1-2 changed | roadmap, todo T-M1-2, new T-M1-4 | no | keep T-M1-2; add T-M1-4 |
| R-M1-2 changed | ADR-001, architecture, T-M1-1 (JSON store, done) | yes | rework: ADR-001 superseded by ADR-002; T-M1-5 migrates the store |
| R-M1-3 removed | roadmap, T-M1-3 | no | discard: both marked dropped with reason |

## Follow-up tasks (code is out of scope for the change skill)

- T-M1-5 — migrate the store from JSON to SQLite.
- T-M1-4 — highlight search matches.
