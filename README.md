# greenfield-kit

An agent plugin (a group of skills, in the style of superpowers) that takes a
greenfield project from "final goal" to an executable plan, and keeps that plan
consistent when goals change mid-project.

Design: [`docs/superpowers/specs/2026-11-11-greenfield-kit-design.md`](docs/superpowers/specs/2026-11-11-greenfield-kit-design.md)

## Skills

| Skill | What it does |
|---|---|
| `using-greenfield` | Entry point. Shared interview rules, stage detection, routing. |

More rows are added as skills land (vision, roadmap, architecture, todo, change).

## Install

Add this repository as a plugin marketplace in Claude Code or Copilot CLI and
install `greenfield-kit` from it (the manifests live in `.claude-plugin/`).

## Checks

```
python scripts/validate_skills.py
python -m unittest discover -s tests
```
