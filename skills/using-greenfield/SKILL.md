---
name: using-greenfield
description: >
  Use when starting a new (greenfield) project, defining or revisiting its
  vision, roadmap, MVP, architecture or todo list, or when the goal or scope
  of a project in progress changes ("the goal changed", "let's add/drop a
  feature", "pivot"). Entry point of the greenfield-kit skill group: holds
  the shared interview rules and routes to greenfield-vision,
  greenfield-roadmap, greenfield-architecture, greenfield-todo and
  greenfield-change.
---

# Using greenfield-kit

Takes a greenfield project from a final goal to an executable plan, one
approved document at a time, and keeps the plan consistent when goals change.
Artifacts live in the target project under `docs/greenfield/`.

## Shared interview rules

Every greenfield-* skill follows these. They are defined here once.

1. Ask the user one question at a time. Prefer a choice list when the likely
   answers are known; allow free text.
2. Separate what the user said from your assumptions. Read your understanding
   back as two short lists (stated / assumed) and let the user correct it.
3. Never fill a gap silently. If an answer is missing or vague, ask again.
4. Do not advance to the next stage, and do not mark a document
   `status: approved`, without the user's explicit approval of the stage you
   actually presented.

Word instructions as "ask the user a question"; do not rely on any one agent
product's tool names.

## Stage detection

Look at `docs/greenfield/` and each document's `status` frontmatter, then
route:

| Situation | Next skill |
|---|---|
| No `vision.md`, or `status: draft` | `greenfield-vision` |
| Approved vision, no approved `roadmap.md` | `greenfield-roadmap` |
| Approved roadmap, no approved `architecture.md` | `greenfield-architecture` |
| Approved architecture, milestone has no `todo/M<n>.md` | `greenfield-todo` |
| Documents exist and the user reports a changed goal, added/changed/removed scope or a pivot | `greenfield-change` |

Each stage skill can also be started alone. A stage that needs an input
document refuses to proceed unless that document exists with
`status: approved`; offer to create or approve it first.

## Artifact format

- Layout: `vision.md`, `roadmap.md`, `architecture.md`,
  `adr/ADR-<nnn>-<slug>.md`, `todo/M<n>.md`.
- Frontmatter on documents: `version` (integer), `status` (`draft` or
  `approved`), and `inputs: [vision, roadmap]` naming the documents it was
  derived from. ADRs use `status: accepted | superseded` and `superseded_by`.
  Each document has a `## Changelog`.
- Item line: `- **<ID>** [<status>] <text>`; `[status]` is optional
  (`pending | in_progress | done | dropped`). Removal is never deletion:
  `[dropped]` plus `(reason: ...)` on the same line.
- References after a `;` on the item line: `refs: <ID>, ...`, and for todo
  items `deps: <ID>, ...`.
- IDs: `V-<n>`, `R-M<m>-<n>`, `T-M<m>-<n>`, `ADR-<nnn>`.

## Checklist (manual check after changing any skill)

- [ ] Follow the stages on `examples/cli-notes/` inputs; every produced
  document has the frontmatter and item format above.
- [ ] Each stage asked one question at a time and read back stated vs assumed.
- [ ] No stage advanced, and no document approved, without explicit approval.
- [ ] `python scripts/check_artifacts.py <your docs/greenfield>` reports 0 problems.
