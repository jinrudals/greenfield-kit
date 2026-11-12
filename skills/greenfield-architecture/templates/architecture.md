---
version: 1
status: draft
inputs: [vision, roadmap]
---

# Architecture — <project name>

Decisions are recorded as ADRs in `adr/`. Sized for M1; later milestones are
checked against it below.

## Context

```mermaid
C4Context
  Person(user, "<user>", "<role>")
  System(system, "<system>", "<what it does>")
  Rel(user, system, "<uses>")
```

## Containers

```mermaid
C4Container
  Person(user, "<user>")
  Container(app, "<container>", "<technology>", "<responsibility>")
  Rel(user, app, "<uses>")
```

## Decisions
- ADR-001 — <topic>: <decision>.

## Later milestones check
<for each later milestone: does the M1 architecture still hold? what would break?>

## Changelog
- v1: initial architecture.
