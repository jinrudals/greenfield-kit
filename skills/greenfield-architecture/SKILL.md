---
name: greenfield-architecture
description: >
  Use to decide the architecture of a greenfield project from its approved
  vision and roadmap: key decisions with 2-3 options and trade-offs recorded
  as ADRs, plus Mermaid C4 context and container diagrams. Triggers:
  "architecture", "design the system", "tech stack decision", "ADR", "C4".
  Third stage of greenfield-kit. Produces docs/greenfield/architecture.md and
  docs/greenfield/adr/.
---

# greenfield-architecture

Produce `docs/greenfield/architecture.md` and ADRs. Follow the shared
interview rules in `using-greenfield`.

## Inputs

`vision.md` and `roadmap.md`, both with `status: approved`. If either is
missing or `draft`, offer to run the earlier stage first; do not proceed
without them.

## Interview

1. List the decisions M1 forces (language/runtime, storage, deployment,
   boundaries, anything else the user raises); ask the user to confirm the list.
2. For each decision, one at a time: present 2-3 options with trade-offs and
   your recommendation; the user chooses. Record the choice as an ADR.
3. Draw the C4 context and container views (Mermaid). If a `c4-architecture`
   skill is available, use it for deeper diagrams.
4. Check the M1 decisions against each later milestone and report what would
   break; ask whether to adjust.

Read the result back (stated vs assumed) and ask for corrections.

## Output

- `docs/greenfield/adr/ADR-<nnn>-<slug>.md` from `templates/adr.md`, one per
  decision; `status: accepted`. ADRs are never edited later: a replaced ADR
  is marked `status: superseded` with `superseded_by: ADR-<nnn>`.
- `docs/greenfield/architecture.md` from `templates/architecture.md` with
  `inputs: [vision, roadmap]`. Keep `status: draft` until explicit approval,
  then `status: approved`; the next stage is `greenfield-todo`.

## Checklist

- [ ] Each decision shows 2-3 options with trade-offs and a stated reason.
- [ ] Each ADR cites the V-/R- items that drive it.
- [ ] Later-milestone check is filled in.
- [ ] Approval was explicit before `status: approved`.
- [ ] `python scripts/check_artifacts.py docs/greenfield` reports 0 problems.
