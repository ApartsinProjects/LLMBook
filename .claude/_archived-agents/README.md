# Archived: executable book-subagent snapshot (System B)

These 42 `book-XX-*.md` files were Claude Code **subagent type definitions**
(YAML frontmatter + condensed instructions) that lived in `.claude/agents/`
and showed up as spawnable types (`book-00-chapter-lead` … `book-41-lab-designer`)
in the Agent tool.

## Why archived (2026-06-15)

They were a **stale, trimmed snapshot** of the authoritative skill docs and
caused confusion against the live source of truth:

- **Source of truth (kept):** `agents/book-skills/agents/*.md`, a symlink/junction
  to `E:\Projects\claude-skills\book-skills\agents\`. The project `CLAUDE.md`
  instructs agents to **read** these before any book-production task. They are
  the latest, most complete versions.
- **This archive (System B):** generated from an earlier draft of those docs
  (~2026-04-05), wrapped with Claude Code YAML headers. Verified to be a strict
  **subset** of the central docs: every word here exists in the central version,
  which additionally carries sections the snapshot predates (e.g. the
  "Value Gate" section in code-pedagogy) and the 2026-05-31 illustrator /
  visual-identity refresh.

Moving them out of `.claude/agents/` de-registers them from the Agent tool so
there is exactly one canonical definition per agent (the central docs).
Nothing in the repo referenced these types by name, so removal breaks nothing.

## To restore as spawnable types

If you want the `book-XX-*` types spawnable again, regenerate them **from the
central docs** rather than reviving this snapshot (it is out of date):
re-attach the YAML frontmatter (`name`, `tools`, `model`) to the current bodies
in `agents/book-skills/agents/*.md` and write the results back into
`.claude/agents/`. Ask Claude Code to do this and it will keep them in sync.
