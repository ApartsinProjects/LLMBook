# Project Instructions

## Book Structure
- Book: "Building Conversational AI with LLMs and Agents"
- Hierarchy: Part > Chapter > Section
- 11 Parts, 38 Chapters (numbered 0-38), 22 Appendices (A-V)
- Single source of truth for structure: `BOOK_CONFIG.md`

## Agent Guidelines

When performing book production tasks, you MUST read the relevant agent description file under `agents/` before starting work. These files define style rules, output formats, and quality standards that override any defaults.

- When **writing section content**, read `agents/00-chapter-lead.html` for structure, artefact requirements, and integration patterns.
- When **generating illustrations**, read `agents/31-illustrator.html` for prompt templates, style palette (warm/whimsical/Kurzgesagt), embedding format (`<figure class="opener-illustration">`), and target count (5-8 per chapter).
- When **writing code examples**, read `agents/08-code-pedagogy.html` for caption placement (below blocks), the "right tool" principle, and library shortcut requirements.
- When **adding cross-references**, read `agents/13-cross-reference.html` for minimum count (3 per section) and progressive depth rules.
- When **writing epigraphs**, read `agents/32-epigraph-writer.html` for the AI agent persona attribution format.
- When **adding callout boxes**, read `agents/25-visual-identity-director.html` for the 15 callout types and required mix per section.
- When **writing bibliographies**, read `agents/35-bibliography.html` for card layout and annotation format.
- When **running quality control**, read `agents/37-controller.html` for conformance sweep and dispatch patterns.
- When **doing publication QA**, read `agents/38-publication-qa.html` for the pre-publication checklist.
- When **adding humor/engagement**, read `agents/34-fun-injector.html` for humor guidelines and fun-note callout conventions.
- When **checking facts in figures**, read `agents/39-figure-fact-checker.html` for diagram verification rules.
- When **adding code captions**, read `agents/40-code-caption-agent.html` for numbering format (Code Fragment X.Y.Z).

## Image Generation

- Script: `agents/book-skills/scripts/generate_icons_gemini.py`
- For multiple images, always use `--engine gemini --batch` (50% discount)
- For single images, use `C:/Users/apart/.claude/skills/gemini-imagegen/scripts/generate_image.py`
- Prompt style: warm cartoon, whimsical, no text in images, Kurzgesagt meets XKCD
- Embed with `<figure class="illustration">` pattern from `agents/31-illustrator.html`

## Global Rules
- NEVER use em dashes or double dashes in generated text
- Use "book", "part", "chapter", "section", "reader" (not "course", "module", "lecture", "student")
- All HTML files link to `styles/book.css` (shared stylesheet, no inline style blocks)
- Code captions go BELOW code blocks, never above
- Every figure, table, code block, and callout must be referenced in surrounding prose
