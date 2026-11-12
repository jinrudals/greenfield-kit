# greenfield-kit — Design

Date: 2026-11-11
Status: draft (pending user review)

## 1. Purpose

`greenfield-kit` is an agent plugin (a group of skills, in the style of
superpowers) that takes a greenfield project from "final goal" to an
executable plan: vision, roadmap (MVP = first milestone), architecture, and
per-milestone todo lists. It also handles mid-project change (goals or scope
shifting after development has started).

Later cycles add the harness layer (AGENTS.md, verification guardrails,
project skills), loop/graph execution setup, and repo scaffolding. Those are
out of scope for this spec.

## 2. Decisions and context

- Distributed as a plugin only (installed into Copilot / Claude style agents);
  no standalone CLI.
- Independent repo `greenfield-kit` (renamed from the empty `harness-generator`).
  `ai-skills` stays separate; `agent-harness` and `agent-harness-evolve` are
  removed from it in a separate PR (not part of this repo's work).
- Skills are interview-driven. Common rules (defined once in
  `using-greenfield`, referenced by every skill):
  - Ask one question at a time.
  - Separate what the user said from the assistant's assumptions, and read the
    understanding back for correction.
  - Do not fill gaps silently; ask again.
  - Do not advance to the next stage without explicit user approval.
- Skill text avoids vendor-specific tool names ("ask the user a question",
  not a specific tool).

## 3. Skill group (first cycle)

```
skills/
  using-greenfield/        entry point: stage order, shared rules, routing
  greenfield-vision/       -> docs/greenfield/vision.md
  greenfield-roadmap/      -> docs/greenfield/roadmap.md
  greenfield-architecture/ -> docs/greenfield/architecture.md (+ adr/)
  greenfield-todo/         -> docs/greenfield/todo/M<n>.md
  greenfield-change/       -> updates of all of the above
```

Flow: vision -> roadmap -> architecture -> todo. Each skill is also callable
alone (e.g. start at roadmap when a vision already exists). Each stage refuses
to run on an input document whose `status` is not `approved` and offers to
create/approve it first.

Artifacts live in the target project under `docs/greenfield/`.

### using-greenfield
Detects the current stage from the documents in `docs/greenfield/` and their
`status`, routes to the next skill, and routes change signals ("the goal
changed", "let's change scope") to `greenfield-change`.

### greenfield-vision
Interview order: problem -> users -> measurable success criteria ->
constraints (time, budget, tech) -> non-goals. Reads the summary back; on
approval saves `vision.md` with `status: approved`.

### greenfield-roadmap
Input: approved vision. Fixes M1 (= MVP, the smallest verifiable flow) first,
then plans later milestones working backwards from the vision. Each milestone
has entry/exit criteria. Excluded items are kept with a reason (post-MVP).

### greenfield-architecture
Input: approved vision and roadmap. For each key decision (language/runtime,
storage, deployment, boundaries) presents 2-3 options with trade-offs. Decisions
become ADRs; context/container views are Mermaid C4 diagrams. Decided for M1,
then checked against later milestones for breakage.

### greenfield-todo
Input: approved roadmap and architecture. One file per milestone; only the
current milestone (M1 first) is detailed, later ones are created when needed.
Item fields: stable ID (`T-M1-3`), linked roadmap item (`R-M1-2`),
dependencies, verifiable completion criteria, status
(`pending | in_progress | done | dropped`). The breakdown is proposed and
adjusted together with the user. Markdown files only; no GitHub Issues
integration.

## 4. Change management

### Document conventions
- Frontmatter: `version`, `status` (`draft | approved`); a `## Changelog`
  section. An approved change bumps `version` and keeps `status: approved`.
- Stable item IDs: `V-3` (vision), `R-M2-1` (roadmap), `T-M1-3` (todo),
  `ADR-007`.
- ADRs are never edited: a replaced ADR is marked `superseded by ADR-012` and
  the new ADR records why.
- Removal is never deletion: items get `status: dropped` plus a reason.

### greenfield-change
1. Change interview: what changed and why, item by item (added / changed /
   removed), one question at a time.
2. Current-state check: compare already-developed work against roadmap/todo
   items (done / in progress / not started).
3. Impact table: changed item -> affected vision / roadmap / architecture /
   ADR / todo / code, with already-implemented parts classified as keep,
   rework, or discard.
4. User approves the table; only then update documents (version bump,
   changelog, ADR supersede, todo statuses, new items). Rework items get new
   IDs linked to the old ones.
5. Emit a follow-up task list. Changing the code itself is out of scope.

## 5. Repository layout

```
<plugin manifest(s)>                   exact format confirmed against each
                                       tool's docs at implementation time
skills/<name>/SKILL.md (+ references/, templates)
scripts/validate_skills.py
scripts/check_artifacts.py             consistency checker for examples
examples/                              sample project + change scenario
.github/workflows/pr-checks.yml
README.md
```

## 6. Verification

- `validate_skills.py` (adapted from `ai-skills`): `SKILL.md` frontmatter
  `name` matches directory, non-empty `description`, allowed names only
  (`using-greenfield`, `greenfield-*`), template documents contain required
  frontmatter (`version`, `status`) and ID formats.
- `examples/`: one fictional project (e.g. a small CLI tool) with golden
  outputs for vision -> roadmap -> architecture -> todo, plus a change
  scenario (1 added, 1 changed, 1 removed item) with the expected impact table
  and todo updates.
- `check_artifacts.py` validates example outputs: no dangling ID references,
  no document used as input while not `approved`, every `dropped` item has a
  reason.
- Interview quality cannot be automated; each SKILL.md carries a checklist and
  the convention is to run the example manually after changing a skill.
- CI (`pr-checks.yml`): structure check, artifact check, Python syntax + ruff,
  gitleaks.

## 7. Out of scope (later cycles)

`greenfield-harness` (AGENTS.md, test/lint/CI/hooks, project skills),
`greenfield-loop` (loop/graph config: exit conditions, budgets, checkpoints),
`greenfield-scaffold` (repo layout and toolchain). Their input formats depend
on the artifacts defined here.

## 8. Housekeeping

- Create the GitHub remote `greenfield-kit` (none exists yet).
- Separate PR in `ai-skills`: delete `agent-harness`, `agent-harness-evolve`,
  update its README table.
