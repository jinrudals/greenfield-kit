---
version: 2
status: approved
inputs: [vision, roadmap]
---

# Architecture — cli-notes

Decisions are recorded as ADRs in `adr/`. Sized for M1; M2 (sync, export) is
checked against it: SQLite rows export cleanly to Markdown and sync as a snapshot.

## Context

```mermaid
C4Context
  Person(dev, "Developer", "Uses the shell all day")
  System(notes, "cli-notes", "Captures and finds notes")
  Rel(dev, notes, "add / list / search / export")
```

## Containers

```mermaid
C4Container
  Person(dev, "Developer")
  Container(cli, "notes CLI", "Go binary", "Command parsing and output")
  ContainerDb(store, "Notes store", "SQLite file", "One file in the user's data dir")
  Rel(dev, cli, "runs")
  Rel(cli, store, "reads/writes")
```

## Decisions
- ADR-001 — storage: single JSON file (superseded by ADR-002).
- ADR-002 — storage: SQLite.

## Changelog
- v2: storage moved to SQLite (ADR-002).
- v1: initial architecture.
