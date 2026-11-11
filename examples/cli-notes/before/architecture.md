---
version: 1
status: approved
inputs: [vision, roadmap]
---

# Architecture — cli-notes

Decisions are recorded as ADRs in `adr/`. Sized for M1; M2 (sync) is checked
against it: a file-based store can be synced by a later adapter.

## Context

```mermaid
C4Context
  Person(dev, "Developer", "Uses the shell all day")
  System(notes, "cli-notes", "Captures and finds notes")
  Rel(dev, notes, "add / list / search")
```

## Containers

```mermaid
C4Container
  Person(dev, "Developer")
  Container(cli, "notes CLI", "Go binary", "Command parsing and output")
  ContainerDb(store, "Notes store", "JSON file", "One file in the user's data dir")
  Rel(dev, cli, "runs")
  Rel(cli, store, "reads/writes")
```

## Decisions
- ADR-001 — storage: single JSON file.

## Changelog
- v1: initial architecture.
