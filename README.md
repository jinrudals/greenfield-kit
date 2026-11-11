# greenfield-kit

An agent plugin (a group of skills, in the style of superpowers) that takes a
greenfield project from "final goal" to an executable plan, and keeps that plan
consistent when goals change mid-project.

Design: [`docs/superpowers/specs/2026-11-11-greenfield-kit-design.md`](docs/superpowers/specs/2026-11-11-greenfield-kit-design.md)

## Skills

| Skill | What it does |
|---|---|
| `using-greenfield` | Entry point. Shared interview rules, stage detection, routing. |
| `greenfield-vision` | Interview → approved vision (problem, users, measurable success, constraints, non-goals). |
| `greenfield-roadmap` | Approved vision → milestones; M1 is the MVP; exclusions with reasons. |
| `greenfield-architecture` | Vision + roadmap → ADRs (2-3 options each) and Mermaid C4 views. |
| `greenfield-todo` | One milestone → tasks with IDs, dependencies and verifiable done-when. |

`greenfield-change` (mid-project goal/scope changes) is added next.

## Install

Add this repository as a plugin marketplace in Claude Code or Copilot CLI and
install `greenfield-kit` from it (the manifests live in `.claude-plugin/`).

## Checks

```
python scripts/validate_skills.py
python -m unittest discover -s tests
```
