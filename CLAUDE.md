# Project Instructions

## Book Structure
- Book: "Building Conversational AI with LLMs and Agents"
- Hierarchy: Part > Chapter > Section
- 11 Parts, 38 Chapters (numbered 0-38), 22 Appendices (A-V)
- Single source of truth for structure: `BOOK_CONFIG.md`

## Agent Guidelines

When performing book production tasks, you MUST read the relevant agent description file under `agents/book-skills/agents/` before starting work. These `.md` files are the single source of truth for agent skills. (HTML versions in `agents/archive/` are legacy and should not be used.)

- When **writing section content**, read `agents/book-skills/agents/00-chapter-lead.md`
- When **generating illustrations**, read `agents/book-skills/agents/31-illustrator.md`
- When **writing code examples**, read `agents/book-skills/agents/08-code-pedagogy.md` (includes Value Gate, "right tool" pattern, caption rules)
- When **adding cross-references**, read `agents/book-skills/agents/13-cross-reference.md`
- When **writing epigraphs**, read `agents/book-skills/agents/32-epigraph-writer.md`
- When **adding callout boxes**, read `agents/book-skills/agents/25-visual-identity-director.md`
- When **writing bibliographies**, read `agents/book-skills/agents/35-bibliography.md`
- When **running quality control**, read `agents/book-skills/agents/37-controller.md`
- When **doing publication QA**, read `agents/book-skills/agents/38-publication-qa.md`
- When **adding humor/engagement**, read `agents/book-skills/agents/34-fun-injector.md`
- When **checking facts in figures**, read `agents/book-skills/agents/39-figure-fact-checker.md`
- When **adding code captions**, read `agents/book-skills/agents/40-code-caption-agent.md`
- When **auditing agent quality**, read `agents/book-skills/agents/36-meta-agent.md`

## Image Generation

- Script: `agents/book-skills/scripts/generate_icons_gemini.py`
- For multiple images, always use `--engine gemini --batch` (50% discount)
- For single images, use `C:/Users/apart/.claude/skills/gemini-imagegen/scripts/generate_image.py`
- Prompt style: warm cartoon, whimsical, no text in images, Kurzgesagt meets XKCD
- Embed with `<figure class="illustration">` pattern from `agents/book-skills/agents/31-illustrator.md`

## Global Rules
- NEVER use em dashes or double dashes in generated text
- Use "book", "part", "chapter", "section", "reader" (not "course", "module", "lecture", "student")
- All HTML files link to `styles/book.css` (shared stylesheet, no inline style blocks)
- Code captions go BELOW code blocks, never above
- Every figure, table, code block, and callout must be referenced in surrounding prose
