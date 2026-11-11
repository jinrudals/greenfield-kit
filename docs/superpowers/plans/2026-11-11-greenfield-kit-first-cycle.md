# greenfield-kit First Cycle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `greenfield-kit` plugin's first cycle: six interview-driven skills (vision, roadmap, architecture, todo, change, entry point), the validators that keep their artifacts consistent, a worked example, and CI.

**Architecture:** Skills are Markdown (`skills/<name>/SKILL.md` + templates). Two zero-dependency Python scripts guard them: `validate_skills.py` (skill structure and templates) and `check_artifacts.py` (consistency of `docs/greenfield/` artifacts, run against `examples/`). Artifact formats are defined once below and every skill/template/example follows them.

**Tech Stack:** Markdown, Python 3.12 stdlib (`unittest`), GitHub Actions, `.claude-plugin` manifests (also read by Copilot CLI).

**Spec:** `docs/superpowers/specs/2026-11-11-greenfield-kit-design.md`

## Global Constraints

- Work in a git worktree (`git worktree add .worktrees/<dir> -b <branch>`); never commit on `main`. Use branch `feat/first-cycle`.
- Commit trailer: `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
- Skill names: `using-greenfield` or `greenfield-<word>`; lowercase-hyphenated; frontmatter `name` equals the directory name; `description` non-empty.
- Interview rules (one question at a time; separate user statements from assumptions and read back; never fill gaps silently; no stage advance without explicit user approval) live only in `using-greenfield`; other skills reference them, not copy them.
- Skill text uses no vendor-specific tool names ("ask the user a question").
- Document frontmatter: `version` (integer), `status` (`draft` | `approved`); `## Changelog` section. ADR frontmatter: `status` (`accepted` | `superseded`), `superseded_by` when superseded.
- Item IDs: `V-<n>`, `R-M<m>-<n>`, `T-M<m>-<n>`, `ADR-<nnn>`. Removal = `[dropped]` tag + `(reason: ...)`, never deletion.
- Python: stdlib only; must pass `ruff check --select E9,F63,F7,F82`.
- Artifacts live in the target project under `docs/greenfield/`.

## Review Focus

- A document with missing/malformed/BOM/CRLF frontmatter must yield an error message, not a traceback.
- Duplicate item IDs inside one document.
- A todo item that references a roadmap item tagged `[dropped]` while the todo item is not itself `[dropped]`.
- A superseded ADR whose `superseded_by` target is missing, or a supersede cycle.
- A skill directory name that looks right but is not allowed (`greenfield_vision`, `greenfield`, uppercase).

## Artifact format (used everywhere)

- Item line: `- **<ID>** [<status>] <text>`; `[status]` optional, one of `pending|in_progress|done|dropped`; dropped needs `(reason: <text>)` on the same line.
- Roadmap/todo item references: `refs: <ID>[, <ID>...]` and todo dependencies `deps: <ID>[, ...]` appear on the item line after `;`.
- Document frontmatter `inputs: [vision, roadmap]` lists the documents this one was derived from (filenames without `.md`, relative to `docs/greenfield/`, ADRs excluded).
- Layout: `vision.md`, `roadmap.md`, `architecture.md`, `adr/ADR-<nnn>-<slug>.md`, `todo/M<n>.md`.

---

### Task 1: Repo skeleton, manifests, skill validator

**Files:**
- Create: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (modelled on superpowers' manifests; name `greenfield-kit`, version `0.1.0`, `source: "./"`)
- Create: `scripts/validate_skills.py`, `tests/test_validate_skills.py`, `README.md`

**Interfaces:**
- Produces: `validate_skills.validate(skills_dir: Path) -> list[tuple[Path, str]]` (empty list = valid); `parse_frontmatter(text: str) -> dict[str, str] | None` (tolerates BOM and CRLF); CLI `python scripts/validate_skills.py [skills_dir]`, exit 1 on errors.

- [ ] **Step 1: Write failing tests** in `tests/test_validate_skills.py` using temp dirs: `test_valid_skill_passes`, `test_name_must_match_directory`, `test_missing_description_fails`, `test_disallowed_name_fails` (each of `greenfield_vision`, `greenfield`, `Greenfield-Vision`, `other-skill` → errors), `test_allowed_names_pass` (`using-greenfield`, `greenfield-vision`), `test_bom_and_crlf_frontmatter_parsed`, `test_template_requires_version_and_status` (a `skills/greenfield-vision/templates/x.md` without `version`/`status` → error naming the file).
- [ ] **Step 2: Run** `python -m unittest discover -s tests -v` → FAIL (module missing).
- [ ] **Step 3: Implement** `scripts/validate_skills.py` by adapting `ai-skills/scripts/validate_skills.py` (same frontmatter parser and GitHub `::error` output) plus: allowed-name regex `^(using-greenfield|greenfield-[a-z0-9]+)$`; for every `skills/*/templates/*.md`, require frontmatter keys `version` and `status`.
- [ ] **Step 4: Create manifests and README** (README: purpose, skill table filled as skills land, install instructions for the Claude/Copilot marketplace, link to the spec).
- [ ] **Step 5: Run tests** → PASS; `python scripts/validate_skills.py` on an empty `skills/` prints `0 problem(s) found`.
- [ ] **Step 6: Commit** `feat: add manifests and skill validator`.

### Task 2: Artifact consistency checker

**Files:**
- Create: `scripts/check_artifacts.py`, `tests/test_check_artifacts.py`

**Interfaces:**
- Consumes: `validate_skills.parse_frontmatter`.
- Produces: `check_artifacts.check(root: Path) -> list[str]` where `root` is a `docs/greenfield/` directory; CLI `python scripts/check_artifacts.py <root>...`, exit 1 on any error. Checks: (a) every doc has frontmatter with integer `version` and `status` in {draft, approved}; (b) item IDs unique per document and match the ID patterns; (c) every `refs:`/`deps:` ID exists in some document under `root`; (d) a document with `status: approved` has every `inputs` document present and `approved`; (e) every `[dropped]` item has `(reason: ...)`; (f) a non-dropped todo item must not reference a dropped roadmap item; (g) ADR `superseded` requires an existing `superseded_by` target, no cycles.

- [ ] **Step 1: Write failing tests**, one per check using temp trees: `test_missing_frontmatter_reports_not_crashes` (BOM + CRLF + empty file), `test_duplicate_id`, `test_dangling_ref`, `test_approved_doc_with_draft_input`, `test_dropped_without_reason`, `test_todo_references_dropped_roadmap_item`, `test_superseded_adr_missing_target`, `test_supersede_cycle`, `test_valid_tree_has_no_errors`. Each asserts the exact error substring (file name + ID where relevant).
- [ ] **Step 2: Run** → FAIL.
- [ ] **Step 3: Implement** the checks; each error string is `"<relative path>: <message>"`. Parse items with regex `^- \*\*(?P<id>[A-Z]+-[A-Za-z0-9-]+)\*\*(?: \[(?P<status>\w+)\])?`.
- [ ] **Step 4: Run** → PASS; run ruff.
- [ ] **Step 5: Commit** `feat: add artifact consistency checker`.

### Task 3: Worked example and change scenario

**Files:**
- Create: `examples/cli-notes/before/` and `examples/cli-notes/after/`, each directory is itself the `docs/greenfield/` root (contains `vision.md`, `roadmap.md`, `architecture.md`, `adr/ADR-001-*.md`, `todo/M1.md`); `examples/cli-notes/change-scenario.md`
- Create: `tests/test_examples.py`

**Interfaces:**
- Consumes: `check_artifacts.check`.
- Produces: golden artifacts that every skill's templates/instructions must reproduce in shape.

- [ ] **Step 1: Write failing tests** `test_examples_are_consistent` (calls `check` on both trees, asserts `[]`) and `test_after_contains_each_change_kind` (in `after`: one new item, one item with bumped `version` + changelog entry, one `[dropped]` item with reason, one superseded ADR).
- [ ] **Step 2: Run** → FAIL (trees missing).
- [ ] **Step 3: Author the example**: fictional small CLI note-taking tool; `before` = approved docs v1 (M1 with ≥3 todo items, one `done`); `after` = v2 after a scope change: 1 added (`V-4`), 1 changed (`R-M1-2` reworded, version bump, changelog), 1 removed (`R-M2-1` `[dropped]` with reason, its todo `[dropped]`), ADR-001 superseded by ADR-002. `change-scenario.md` records the user's change statements and the expected impact table (keep / rework / discard columns).
- [ ] **Step 4: Run** → PASS.
- [ ] **Step 5: Commit** `feat: add cli-notes example and change scenario`.

### Task 4: `using-greenfield` and the shared rules

**Files:**
- Create: `skills/using-greenfield/SKILL.md`, `tests/test_skill_content.py`

**Interfaces:**
- Produces: headings `## Shared interview rules` (the four rules from Global Constraints) and `## Stage detection` (maps `docs/greenfield/` contents + `status` to the next skill: nothing → `greenfield-vision`; approved vision → `greenfield-roadmap`; + roadmap → `greenfield-architecture`; + architecture → `greenfield-todo`; change signals such as "the goal changed", "scope changed", "drop/add feature" while documents exist → `greenfield-change`).
- `tests/test_skill_content.py` helper `skill_text(name: str) -> str`, reused by Tasks 5–6.

- [ ] **Step 1: Write failing tests**: `test_using_greenfield_has_shared_rules_and_routing` (asserts both headings and that each of the five skill names appears), `test_no_vendor_tool_names` (across all `skills/**/*.md`, none of `AskUserQuestion`, `ask_user`, `TodoWrite`).
- [ ] **Step 2: Run** → FAIL.
- [ ] **Step 3: Write `SKILL.md`**: description triggers on starting a new project, "greenfield", vision/roadmap/MVP/architecture planning, and goal/scope change; body = Shared interview rules, Stage detection, artifact format summary (copy of "Artifact format" above), and a Checklist for manual example runs.
- [ ] **Step 4: Run** tests and `validate_skills.py` → PASS.
- [ ] **Step 5: Commit** `feat: add using-greenfield entry skill`.

### Task 5: Document-stage skills (vision, roadmap, architecture, todo)

**Files:**
- Create: `skills/greenfield-vision/SKILL.md` + `templates/vision.md`; `skills/greenfield-roadmap/SKILL.md` + `templates/roadmap.md`; `skills/greenfield-architecture/SKILL.md` + `templates/architecture.md`, `templates/adr.md`; `skills/greenfield-todo/SKILL.md` + `templates/todo.md`
- Modify: `tests/test_skill_content.py`, `README.md` (skill table)

**Interfaces:**
- Consumes: `skill_text` (Task 4), artifact format and shared rules (referenced, not copied).
- Produces: each SKILL.md has `## Inputs`, `## Interview`, `## Output`, `## Checklist`; each template satisfies the document frontmatter rules and the item line format.

- [ ] **Step 1: Write failing tests** (parametrized over the four skills): `test_stage_skill_sections` (the four headings exist), `test_stage_skill_defers_to_shared_rules` (mentions `using-greenfield`, does not contain the phrase "one question at a time"), `test_stage_skill_requires_approved_inputs` (roadmap/architecture/todo mention `status: approved`), `test_templates_parse_with_checker` (copy each template into a temp tree as the right document and assert `check_artifacts.check` reports no format errors).
- [ ] **Step 2: Run** → FAIL.
- [ ] **Step 3: Author each skill** following spec §3: vision interview order problem → users → measurable success criteria → constraints → non-goals; roadmap fixes M1 (= MVP, smallest verifiable flow) first then later milestones backwards, with entry/exit criteria and a post-MVP exclusions section with reasons; architecture presents 2–3 options per decision, writes ADRs + Mermaid C4 context/container, checks M1 decisions against later milestones, points to the `c4-architecture` skill when available; todo details only the current milestone, item fields per the artifact format plus `done-when:`.
- [ ] **Step 4: Run** all tests and `validate_skills.py` → PASS.
- [ ] **Step 5: Commit** `feat: add vision, roadmap, architecture and todo skills`.

### Task 6: `greenfield-change`

**Files:**
- Create: `skills/greenfield-change/SKILL.md` + `templates/impact-table.md` (frontmatter `version: 1`, `status: draft`)
- Modify: `tests/test_skill_content.py`, `README.md`

**Interfaces:**
- Consumes: `examples/cli-notes/change-scenario.md` (the skill's steps must be able to produce its impact table).
- Produces: `SKILL.md` steps 1–5 per spec §4: change interview (added/changed/removed, item by item), current-state check (done/in progress/not started), impact table (affected vision/roadmap/architecture/ADR/todo/code; keep/rework/discard), approval gate before any document edit, follow-up task list; documents the conventions for version bump, changelog, ADR supersede, `[dropped]` with reason, new IDs linked to old for rework; states that changing code is out of scope.

- [ ] **Step 1: Write failing tests**: `test_change_skill_has_gate_and_conventions` (asserts it mentions approval before edits, `superseded_by`, `[dropped]`, `Changelog`, and "out of scope" for code), `test_impact_table_template_columns` (template header contains `keep`, `rework`, `discard`).
- [ ] **Step 2: Run** → FAIL.
- [ ] **Step 3: Author the skill and template**; headings `## Inputs`, `## Interview`, `## Output`, `## Checklist` as in Task 5.
- [ ] **Step 4: Run** all tests, `validate_skills.py`, and `check_artifacts.py examples/cli-notes/before examples/cli-notes/after` → PASS.
- [ ] **Step 5: Commit** `feat: add greenfield-change skill`.

### Task 7: CI and manual end-to-end run

**Files:**
- Create: `.github/workflows/pr-checks.yml`
- Modify: `README.md`

- [ ] **Step 1: Write the workflow** by adapting `ai-skills/.github/workflows/pr-checks.yml`: jobs `skills-structure` (`validate_skills.py`), `artifacts` (`check_artifacts.py` on both example trees), `python` (compileall, `ruff check --select E9,F63,F7,F82`, `python -m unittest discover -s tests`), `secrets` (gitleaks, full history).
- [ ] **Step 2: Run locally** every command from the workflow → all pass.
- [ ] **Step 3: Manual run** (per each SKILL.md Checklist): in a scratch directory outside the repo, follow `using-greenfield` → vision → roadmap with the example's inputs and confirm the produced documents pass `check_artifacts.py`; record the result in the PR description.
- [ ] **Step 4: Commit** `ci: add PR checks`; create the GitHub remote `greenfield-kit` if absent, push the branch, and open a PR against `main`.

## Out of scope

`greenfield-harness`, `greenfield-loop`, `greenfield-scaffold` (later cycles); the separate `ai-skills` PR removing `agent-harness` and `agent-harness-evolve`.
