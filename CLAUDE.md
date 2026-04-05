# Project Instructions

## Book Structure
- Book: "Building Conversational AI with LLMs and Agents"
- Hierarchy: Part > Chapter > Section
- 11 Parts, 38 Chapters (numbered 0-38), 22 Appendices (A-V)
- Single source of truth for structure: `BOOK_CONFIG.md`

## Agent Guidelines

When performing book production tasks, consult the relevant agent description files under `agents/` before starting. These files define style rules, output formats, and quality standards.

| Task | Agent File | Key Rules |
|------|-----------|-----------|
| Writing section content | `agents/00-chapter-lead.html` | Structure, artefact requirements, integration |
| Generating illustrations | `agents/31-illustrator.html` | Prompt template, style palette, embedding format, target 5-8 per chapter |
| Writing code examples | `agents/08-code-pedagogy.html` | Caption placement, "right tool" principle, library shortcuts |
| Cross-references | `agents/13-cross-reference.html` | At least 3 per section, progressive depth |
| Epigraphs | `agents/32-epigraph-writer.html` | Agent persona attribution format |
| Callout boxes | `agents/25-visual-identity-director.html` | 15 callout types, required mix per section |
| Bibliography | `agents/35-bibliography.html` | Card layout, annotation format |
| Quality control | `agents/37-controller.html` | Conformance sweep, dispatch pattern |
| Publication QA | `agents/38-publication-qa.html` | Pre-publication checklist |
| Fun/engagement | `agents/34-fun-injector.html` | Humor guidelines, fun-note callouts |

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
