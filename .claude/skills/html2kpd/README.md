# html2kpd quick-start

Convert HTML book sources to a Kindle-validated KPF file.

## Pipeline

```
HTML sources -> EPUB (html2pub) -> EPUB validated (EPUBCheck)
                                        |
                                        v
                            Kindle Previewer 3 (-convert -qualitychecks)
                                        |
                                        v
                                     .kpf (validated by KPV)
                                        |
                                        v
                                  Amazon KDP upload
```

## Files in this skill

- `SKILL.md`: main skill spec; KPV error map; workflow; tooling locations.
- `LESSONS.md`: 48 specific lessons from production books (math rendering,
  tables, navigation chains, code blocks, image format, CSS sanitization,
  self-closing elements, etc.).
- `CSS_SNIPPETS.md`: copy-paste CSS that fixes the most common Kindle
  layout bugs (table flow, author cards, section cards, math centering,
  callouts, code blocks).
- `scripts/`: read-only audits and idempotent fixes:
  - `audit_navigation.py`: prev/next chain integrity (broken targets,
    asymmetric A.next != B.prev).
  - `audit_phantom_cards.py`: duplicate resolved hrefs and broken targets
    in `<a class="section-card">` lists.
  - `audit_math_kpv.py`: math patterns that trip KPV (empty mtable attrs,
    function-application chars in msub, math-in-p HTML5 auto-close bug).
  - `audit_tables_kpv.py`: wide tables, math-in-tables, code-in-tables,
    rowspan/colspan.
  - `audit_code_indent.py`: leading/trailing blank lines, over-indent.
  - `audit_stale_refs.py`: "Section X.Y" prose refs where X.Y has no file.
  - `fix_nav_chain.py`: sequential prev/next rebuild.
  - `fix_phantom_cards.py`: dedup + reorder section cards.
  - `kpv_convert.py`: wrapper around Kindle Previewer 3 CLI.
  - `kpv_smoke_test.py`: small subset test before full conversion.

## Quick start

All scripts accept `--root <book-root>` to specify the source directory.
Audits are read-only; fixes are dry-run by default and require `--apply`
to write.

```bash
SKILL="C:/Users/apart/.claude/skills/html2kpd"
BOOK="<path-to-book-root>"

# 1. Source audit (read-only; flag KPV-risky patterns)
python "$SKILL/scripts/audit_navigation.py"     --root "$BOOK"
python "$SKILL/scripts/audit_phantom_cards.py"  --root "$BOOK"
python "$SKILL/scripts/audit_math_kpv.py"       --root "$BOOK"
python "$SKILL/scripts/audit_tables_kpv.py"     --root "$BOOK"
python "$SKILL/scripts/audit_code_indent.py"    --root "$BOOK"
python "$SKILL/scripts/audit_stale_refs.py"     --root "$BOOK"

# 2. Apply structural fixes (idempotent; dry-run by default)
python "$SKILL/scripts/fix_nav_chain.py"        --root "$BOOK" --apply
python "$SKILL/scripts/fix_phantom_cards.py"    --root "$BOOK" --apply

# 3. Build EPUB (uses html2pub skill)
python -m html2pub build "$BOOK"

# 4. Validate EPUB (EPUBCheck)
java -jar "$EPUBCHECK_HOME/epubcheck.jar" "$BOOK/<output>/book.epub"

# 5. Smoke test (small subset through KPV)
python "$SKILL/scripts/kpv_smoke_test.py" --epub "$BOOK/<output>/book.epub"

# 6. Full KPV conversion + qualitychecks
python "$SKILL/scripts/kpv_convert.py" \
    --epub "$BOOK/<output>/book.epub" \
    --output "$BOOK/<output>/book.kpf"
```

## Prerequisites

- Python 3.11+ with `beautifulsoup4`, `lxml`
- `html2pub` skill installed (see `~/.claude/skills/html2pub/SKILL.md`)
- Kindle Previewer 3 (download from
  `https://kdp.amazon.com/en_US/help/topic/G202131170`)
- EPUBCheck (from
  `https://github.com/w3c/epubcheck/releases`)
- Java (bundled with EPUBCheck or on PATH)

Set env vars to override default locations:

```bash
export KINDLE_PREVIEWER="C:/Program Files/Amazon/Kindle Previewer 3/Kindle Previewer 3.exe"
export EPUBCHECK_HOME="C:/Tools/epubcheck"
```

## Triggers

This skill activates on phrases like:
- "convert to KPF" / "build KPF"
- "kindle previewer" / "KPV"
- "qualitychecks" / "KPV qualitychecks"
- "ship to KDP" / "KDP submission"
- "html2kpd"
- "fix E21018" / any KPV error code

## When to NOT use this skill

- Plain EPUB-only build (no Kindle target) -> use `html2pub` directly.
- HTML to DOCX -> use `html2doc`.
- One-shot Markdown to EPUB -> `pandoc`.
