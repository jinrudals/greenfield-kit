---
version: 2
status: approved
inputs: [vision]
---

# Roadmap — cli-notes

## M1 — MVP: capture and find notes
Entry: vision approved. Exit: a user can add, list and search notes from the shell.

- **R-M1-1** Add and list notes from the command line; refs: V-1
- **R-M1-2** Search notes by keyword, case-insensitive, with highlighted matches; refs: V-3
- **R-M1-3** [dropped] Tag notes and filter by tag; refs: V-1 (reason: users only asked for search; tags deferred until requested)

## M2 — Sync and export
Entry: M1 exit met. Exit: notes available on a second machine and exportable.

- **R-M2-1** Sync notes to a cloud store; refs: V-2
- **R-M2-2** Export all notes as Markdown files; refs: V-4

## Excluded (post-MVP)
- Mobile client — needs a sync story first.

## Changelog
- v2: reworded R-M1-2 (highlighted matches); dropped R-M1-3 (tags); added R-M2-2 (export).
- v1: initial roadmap.
