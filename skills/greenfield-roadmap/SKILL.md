---
name: greenfield-roadmap
description: >
  Use to turn an approved vision into a milestone roadmap whose first
  milestone M1 is the MVP (the smallest verifiable flow), with later
  milestones, entry/exit criteria and a post-MVP exclusion list. Triggers:
  "roadmap", "MVP scope", "milestones", "what should we build first".
  Second stage of greenfield-kit. Produces docs/greenfield/roadmap.md.
---

# greenfield-roadmap

Turn an approved vision into `docs/greenfield/roadmap.md`. Follow the shared
interview rules in `using-greenfield`.

## Inputs

`docs/greenfield/vision.md` with `status: approved`. If it is missing or
`draft`, offer to run `greenfield-vision` first; do not proceed without it.

## Interview

1. Candidate capabilities — list what the vision implies; ask the user to add
   or remove.
2. Fix M1 (the MVP) first: the smallest flow that can be verified against a
   success criterion in the vision. Include only capabilities that flow needs;
   move the rest to later milestones or to the exclusions list with a reason.
3. Plan later milestones backwards from the vision, each with entry and exit
   criteria that can be observed.
4. Confirm exclusions (post-MVP) and their reasons.

Read the plan back (stated vs assumed) and ask for corrections.

## Output

Write `docs/greenfield/roadmap.md` from `templates/roadmap.md` with
`inputs: [vision]`: items `R-M<m>-<n>`, each with `refs:` to the vision items
it serves. Keep `status: draft` until explicit approval, then set
`status: approved`; the next stage is `greenfield-architecture`.

## Checklist

- [ ] M1 can be verified end to end; nothing in M1 is unneeded for that flow.
- [ ] Every item has `refs:` to at least one vision item.
- [ ] Every milestone has observable entry and exit criteria.
- [ ] Exclusions each carry a reason.
- [ ] Approval was explicit before `status: approved`.
- [ ] `python scripts/check_artifacts.py docs/greenfield` reports 0 problems.
