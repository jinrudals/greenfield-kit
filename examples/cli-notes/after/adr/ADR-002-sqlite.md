---
version: 1
status: accepted
---

# ADR-002 — Storage: SQLite

## Context
Supersedes ADR-001. The V-3 target (search among 1,000 notes under 1 second, with
highlighted case-insensitive matches in R-M1-2) is not met cheaply by scanning one
JSON file, and V-4 export wants structured rows.

## Options
1. Keep JSON, add an in-memory index — rebuilds on every run.
2. SQLite with FTS — indexed, one file, one extra dependency.

## Decision
Option 2. Existing JSON notes are migrated once (T-M1-5).
