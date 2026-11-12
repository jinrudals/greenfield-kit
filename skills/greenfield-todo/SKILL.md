---
name: greenfield-todo
description: >
  Use to break one roadmap milestone into a task list with stable IDs,
  dependencies and verifiable completion criteria, stored per milestone in
  docs/greenfield/todo/M<n>.md. Triggers: "todo list", "task breakdown",
  "what do we do for M1", "tasks for the MVP". Fourth stage of
  greenfield-kit; also where greenfield-change records follow-up work.
---

# greenfield-todo

Produce `docs/greenfield/todo/M<n>.md` for one milestone. Follow the shared
interview rules in `using-greenfield`.

## Inputs

`roadmap.md` and `architecture.md`, both with `status: approved`. If either is
missing or `draft`, offer to run the earlier stage first; do not proceed
without them. Detail only the current milestone (M1 first); later milestones
get their file when they become current.

## Interview

1. Confirm which milestone this is for.
2. Propose a task breakdown for it; each task serves at least one roadmap item.
3. With the user, adjust size and order; capture dependencies between tasks.
4. For every task, agree a verifiable `done-when:` condition (a command and
   its expected result, or an observable behaviour).

Read the list back (stated vs assumed) and ask for corrections.

## Output

Write `docs/greenfield/todo/M<n>.md` from `templates/todo.md` with
`inputs: [roadmap, architecture]`. Item line:
`- **T-M<m>-<n>** [<status>] <task>; refs: R-...; deps: T-...; done-when: ...`
with status `pending | in_progress | done | dropped`. Plain Markdown only; no
issue-tracker integration. Keep `status: draft` until explicit approval, then
`status: approved`.

## Checklist

- [ ] Every task has `refs:` to a roadmap item and a verifiable `done-when:`.
- [ ] Dependencies reference existing task IDs and form no cycle.
- [ ] Only the current milestone is detailed.
- [ ] Approval was explicit before `status: approved`.
- [ ] `python scripts/check_artifacts.py docs/greenfield` reports 0 problems.
