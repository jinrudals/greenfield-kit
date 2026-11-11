---
name: greenfield-vision
description: >
  Use to define or revise the vision of a greenfield project: the problem,
  users, measurable success criteria, constraints and non-goals. First stage
  of greenfield-kit. Triggers: "define the vision", "what are we building
  and why", "project goal", "success criteria", "non-goals". Produces
  docs/greenfield/vision.md. Use greenfield-change instead when an approved
  vision already exists and the goal changes.
---

# greenfield-vision

Turn the user's idea into an approved `docs/greenfield/vision.md`. Follow the
shared interview rules in `using-greenfield`.

## Inputs

None required. If `vision.md` already exists with `status: approved`, stop and
route to `greenfield-change`; if it is `draft`, continue editing it.

## Interview

Ask in this order, adapting to what the user already said:

1. Problem — what is going wrong or missing today, in the user's words.
2. Users — who has the problem; who is the primary user.
3. Success criteria — how will we know it worked? Push until each criterion is
   measurable (a number, a threshold, an observable behaviour).
4. Constraints — time, budget, technology; only what the user states.
5. Non-goals — what this project will explicitly not do.

Then read the understanding back (stated vs assumed) and ask for corrections.

## Output

Write `docs/greenfield/vision.md` from `templates/vision.md`: items
`V-1`, `V-2`, ... one per distinct statement. Keep `status: draft` until the
user explicitly approves the document, then set `status: approved` and tell
the user the next stage is `greenfield-roadmap`.

## Checklist

- [ ] Every success criterion is measurable.
- [ ] Non-goals section is filled in (or the user explicitly said none).
- [ ] Stated and assumed points were separated and read back.
- [ ] Approval was explicit before `status: approved`.
- [ ] `python scripts/check_artifacts.py docs/greenfield` reports 0 problems.
