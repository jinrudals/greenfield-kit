---
name: greenfield-change
description: >
  Use when the goal, vision or scope of a greenfield project changes after
  documents are approved or development has started: items added, changed or
  removed. Interviews the change, checks what is already built, produces an
  impact table (keep / rework / discard), and only after approval updates the
  vision, roadmap, architecture, ADRs and todo lists with version bumps,
  changelog entries and dropped/superseded markers. Triggers: "the goal
  changed", "pivot", "change the scope", "drop this feature", "add a
  requirement".
---

# greenfield-change

Apply a change to the approved `docs/greenfield/` documents without losing
history. Follow the shared interview rules in `using-greenfield`.

## Inputs

The existing `docs/greenfield/` documents (any that exist) and knowledge of
what has already been built (the user's account, the todo statuses, the repo).

## Interview

1. Change interview: ask what changed and why, item by item, sorted into
   added / changed / removed. Reference existing IDs (V-, R-, T-, ADR-).
2. Current-state check: for each affected roadmap/todo item, find out whether
   it is done, in progress or not started, and what code already depends on it.
3. Build the impact table (`templates/impact-table.md`): changed item →
   affected vision / roadmap / architecture / ADR / todo / code, with every
   already-implemented part classified keep, rework or discard.
4. Present the table and ask for approval. Make no document edit before the
   user approves it.

## Output

After approval, update the documents:

- Bump `version` (integer) of each edited document, keep `status: approved`,
  and add a line to its `## Changelog`.
- Added items get new IDs. Removed items are never deleted: tag them
  `[dropped]` with `(reason: ...)` on the same line; dropped roadmap items
  drop their todo items too.
- A replaced architectural decision: write a new ADR, set the old ADR to
  `status: superseded` with `superseded_by: ADR-<nnn>`; never edit its body.
- Rework gets new todo IDs linked to the old ones through `deps:`; amend
  `inputs:` only if the document set itself changed.
- Emit the follow-up task list (also appended to the current `todo/M<n>.md`).
  Changing the code itself is out of scope for this skill.

## Checklist

- [ ] The user approved the impact table before any document was edited.
- [ ] Every edited document has a bumped `version` and a changelog line.
- [ ] No item was deleted; removals carry `[dropped]` and a reason.
- [ ] Superseded ADRs point to their replacement via `superseded_by`.
- [ ] Every already-implemented affected part is classified keep, rework or discard.
- [ ] `python scripts/check_artifacts.py docs/greenfield` reports 0 problems.
