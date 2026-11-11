---
version: 1
status: superseded
superseded_by: ADR-002
---

# ADR-001 — Storage: single JSON file

## Context
M1 needs persistence for at most a few thousand notes, no server, zero setup.

## Options
1. Single JSON file — simplest; whole-file rewrite on each add.
2. SQLite — indexed search; adds a dependency.
3. One file per note — easy to sync; slow to search.

## Decision
Option 1. Revisit if search exceeds the V-3 latency target.

Superseded by ADR-002.
