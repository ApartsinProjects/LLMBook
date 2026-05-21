"""Wave 17k: residual fixes for parts 13-16 + appendices from cycle-3 audit.

1. Part 15 index still says "Part XI" in part-label, hero alt, overview prose
2. "Part XII" still in module-80, module-82, module-83 index files + section-83.4
3. Section breadcrumbs in modules 67/78 still pre-merge chapter labels
4. Apx A.6 missed by Wave 17c (file is section-a.6.html, regex required numeric N)
5. Sec 80.4 malformed H2: literal "2&gt;1. The Universal Recipe" instead of <h2>80.4.1
6. Capstone chapter-nav has stacked Previous/Next labels (Wave 17g not idempotent)
7. Capstone requirements.html uses old chapter numbers ("Chapters: 05, 12, 13")
8. Appendix B/C: figure captions still C.0.1 / D.0.1 (should be B.0.1 / C.0.1)
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]


def fix_part15_xi_to_xv():
    """Part 15 index still has Part XI labels."""
    print('=== Fix 1: Part 15 "Part XI" → "Part XV" ===')
    p = ROOT / 'part-15-applications-of-llms-across-industries' / 'index.html'
    if not p.exists():
        return
    text = p.read_text(encoding='utf-8')
    orig = text
    # Replace Part XI (not Part XII or Part XIII!) only when it's about THIS part
    # Use bounded replacements:
    text = re.sub(
        r'(<div class="part-label"[^>]*>)Part XI(</div>)',
        r'\1Part XV\2',
        text
    )
    # Hero alt-text
    text = text.replace(
        "'Part XI: Real-World",
        "'Part XV: Real-World"
    )
    text = text.replace(
        "'Part XI:",
        "'Part XV:"
    )
    # Overview prose - if it says "Part XI covers" or similar
    text = re.sub(
        r'\bPart XI\b(?! Ethics)',  # don't change "Part XI Ethics" if it's a real ref
        'Part XV',
        text
    )
    # Subtitle vs overview mismatch: "Seven verticals" vs "nine industries"
    # The actual count is currently 8 modules (72-78 = 7 chapters originally + ch 78 covers 3 industries
    # so really 7 chapter slots, 8 cards in part-index)
    # Fix subtitle if it says "Seven verticals" and overview says different
    if text != orig:
        p.write_text(text, encoding='utf-8')
        print('  Fixed part-15 index')


def fix_part16_modules_xii_to_xvi():
    """Module index pages in Part 16 still have Part XII labels."""
    print('=== Fix 2: Part 16 modules "Part XII" → "Part XVI" ===')
    part16 = ROOT / 'part-16-llm-agentic-ai-research-frontiers'
    n = 0
    for f in list(part16.rglob('*.html')):
        if 'docs' in f.parts:
            continue
        text = f.read_text(encoding='utf-8')
        orig = text
        text = text.replace('Part XII:', 'Part XVI:')
        # "Part XII " (with trailing space) — be careful not to break references in
        # in-prose text to e.g. "Part XII: LLM Systems at Scale" which IS Part XII.
        # Actually Part XII is the current correct name for LLM Systems at Scale. So
        # we should NOT change "Part XII: LLM Systems at Scale". Only "Part XII"
        # references to FRONTIERS (the old name) should change.
        # Looking at agent finding: "'Part XII' still in module-80, module-82, module-83"
        # — those are clearly frontier-self-references using old part number.
        # Reverse the over-broad replacement and only target the specific obsolete
        # phrasings.
        text = orig  # reset
        # Specific stale phrasings:
        text = text.replace(
            "Part XII: Frontiers",
            "Part XVI: Research Frontiers"
        )
        text = text.replace(
            "Part XII: Research Frontiers",
            "Part XVI: Research Frontiers"
        )
        # "Part XII" used as breadcrumb / pagefind-meta of THIS file is wrong
        # if THIS file is in part-16
        # Replace nav-num spans referring to "Part XII" within Part 16 files
        text = re.sub(
            r'(<span class="nav-num">)Part XII(</span>)',
            r'\1Part XVI\2',
            text
        )
        # part-label in breadcrumb data-pagefind
        text = re.sub(
            r'(<div class="part-label"[^>]*>)Part XII(</div>)',
            r'\1Part XVI\2',
            text
        )
        # pagefind-meta part:Part XII
        text = re.sub(
            r'data-pagefind-meta="part:Part XII([^"]*)"',
            lambda m: (
                f'data-pagefind-meta="part:Part XVI{m.group(1)}"'
                # Only update if the surrounding part name is frontier-ish, not LLM Systems at Scale
                if ('Frontier' in m.group(1) or m.group(1).strip() == '' or
                    'Research' in m.group(1) or 'AGI' in m.group(1))
                else m.group(0)
            ),
            text
        )
        if text != orig:
            f.write_text(text, encoding='utf-8')
            n += 1
    print(f'  Fixed {n} Part 16 files')


def fix_apx_a6_numbering():
    """Wave 17c missed section-a.6.html. Renumber its H2/H3 to use A.6 prefix."""
    print('=== Fix 3: Appendix A.6 H2/H3 numbering ===')
    p = ROOT / 'appendices' / 'appendix-a-mathematical-foundations' / 'section-a.6.html'
    if not p.exists():
        return
    text = p.read_text(encoding='utf-8')
    orig = text

    # H2 visible like "4.1.2 X" → "A.6.2 X" (use the actual third component as the sub-section)
    # H3 visible like "4.1.2.3 X" → "A.6.2.3 X"
    # Anchor IDs like "4-1-2-slug" → "a-6-2-slug"
    # Figure / Code Fragment / Table captions: "Figure 4.1.1" → "Figure A.6.1"

    def rewrite_h2(m):
        h_id = m.group(1)
        visible = m.group(2)
        rest = m.group(3)
        parts = visible.split('.')
        if len(parts) >= 3:
            new_vis = f'A.6.{parts[2]}'
        else:
            new_vis = visible
        id_parts = h_id.split('-', 2)
        if len(id_parts) >= 3:
            new_id = f'a-6-{id_parts[2]}'
        else:
            new_id = h_id
        return f'<h2 id="{new_id}">{new_vis}{rest}</h2>'

    text = re.sub(
        r'<h2 id="([^"]+)">(\d+\.\d+\.\d+)([^<]*)</h2>',
        rewrite_h2,
        text
    )

    def rewrite_h3(m):
        h_id = m.group(1)
        visible = m.group(2)
        rest = m.group(3)
        parts = visible.split('.')
        if len(parts) >= 4:
            new_vis = f'A.6.{parts[2]}.{parts[3]}'
        else:
            new_vis = visible
        id_parts = h_id.split('-', 3)
        if len(id_parts) >= 4:
            new_id = f'a-6-{id_parts[2]}-{id_parts[3]}'
        else:
            new_id = h_id
        return f'<h3 id="{new_id}">{new_vis}{rest}</h3>'

    text = re.sub(
        r'<h3 id="([^"]+)">(\d+\.\d+\.\d+\.\d+)([^<]*)</h3>',
        rewrite_h3,
        text
    )

    # Figure / Code Fragment / Table captions
    def rewrite_cap(m):
        kind = m.group(1)
        num = m.group(2)
        parts = num.split('.')
        if len(parts) >= 3:
            new_num = f'A.6.{parts[2]}'
            if len(parts) > 3:
                new_num += '.' + '.'.join(parts[3:])
            return f'<strong>{kind} {new_num}</strong>'
        return m.group(0)

    text = re.sub(
        r'<strong>(Figure|Table|Code Fragment) (\d+\.\d+\.\d+(?:\.\d+)?)</strong>',
        rewrite_cap,
        text
    )

    # Anchor href same-page
    def rewrite_anchor(m):
        prefix = m.group(1)
        anchor_id = m.group(2)
        parts = anchor_id.split('-')
        if len(parts) >= 3 and parts[0].isdigit():
            rest = '-'.join(parts[2:])
            return f'{prefix}#a-6-{rest}'
        return m.group(0)

    text = re.sub(
        r'(href=")#(\d+-\d+-[^"]+)',
        rewrite_anchor,
        text
    )

    # "Chapter 04" / "originated as a section of Chapter 04" type prose
    text = text.replace(
        'originated as a section of Chapter 04',
        'originated as a section of the Transformer Architecture chapter'
    )
    text = re.sub(r'\bChapter 04\b', 'Chapter 3', text)

    # Next-nav block labelling Chapter 0 as "Appendix B Machine Learning Essentials" — fix
    text = re.sub(
        r'<span class="nav-num">Appendix B</span><span class="nav-title">Machine Learning Essentials</span>',
        '<span class="nav-num">Chapter 0</span><span class="nav-title">ML &amp; PyTorch Foundations</span>',
        text
    )

    if text != orig:
        p.write_text(text, encoding='utf-8')
        print('  Fixed Apx A.6 numbering and prose')


def fix_apx_bc_captions():
    """Appendix B figure cap C.0.1 → B.0.1; Appendix C figure cap D.0.1 → C.0.1.
    Plus assorted "Section O.4" / "Table p.0.X" gibberish in Apx B; "Chapter 0 (Section 0.1)"
    in Apx C pagefind chapter meta.
    """
    print('=== Fix 4: Appendix B/C figure captions + meta ===')
    apx_b = ROOT / 'appendices' / 'appendix-b-course-syllabi' / 'index.html'
    if apx_b.exists():
        text = apx_b.read_text(encoding='utf-8')
        orig = text
        text = re.sub(
            r'<strong>Figure C\.0\.(\d+)</strong>',
            r'<strong>Figure B.0.\1</strong>',
            text
        )
        text = re.sub(
            r'\bTable p\.0\.(\d+)\b',
            r'Table B.0.\1',
            text
        )
        text = text.replace('Section O.4', 'Section B.4')
        if text != orig:
            apx_b.write_text(text, encoding='utf-8')
            print('  Fixed Apx B captions/meta')

    apx_c = ROOT / 'appendices' / 'appendix-c-reading-pathways' / 'index.html'
    if apx_c.exists():
        text = apx_c.read_text(encoding='utf-8')
        orig = text
        text = re.sub(
            r'<strong>Figure D\.0\.(\d+)</strong>',
            r'<strong>Figure C.0.\1</strong>',
            text
        )
        text = re.sub(
            r'data-pagefind-meta="chapter:Chapter 0 \(Section 0\.1\): Reading Pathways"',
            'data-pagefind-meta="chapter:Appendix C: Reading Pathways"',
            text
        )
        if text != orig:
            apx_c.write_text(text, encoding='utf-8')
            print('  Fixed Apx C captions/meta')


def fix_section_80_4_h2():
    """Sec 80.4: literal "2&gt;1. The Universal Recipe" should be <h2>80.4.1 The Universal Recipe</h2>."""
    print('=== Fix 5: section 80.4 malformed H2 ===')
    p = ROOT / 'part-16-llm-agentic-ai-research-frontiers' / 'module-80-frontier-architectures' / 'section-80.4.html'
    if not p.exists():
        return
    text = p.read_text(encoding='utf-8')
    orig = text
    text = text.replace(
        '2&gt;1. The Universal Recipe',
        '<h2 id="80-4-1-the-universal-recipe">80.4.1 The Universal Recipe'
    )
    # Also check if there's a missing </h2> after — look for context
    if text != orig:
        p.write_text(text, encoding='utf-8')
        print('  Fixed section-80.4 malformed H2')


def fix_capstone_chapter_nav_dups():
    """Capstone files have stacked Previous/Next labels — Wave 17g re-ran without
    idempotency. Strip the duplicates."""
    print('=== Fix 6: capstone chapter-nav stacking ===')
    capstone_dir = ROOT / 'capstone'
    if not capstone_dir.exists():
        return
    n = 0
    for f in capstone_dir.glob('*.html'):
        text = f.read_text(encoding='utf-8')
        orig = text
        # If there are multiple "Previous" or "Next" labels stacked, collapse to single
        # Pattern: <span class="nav-label">Previous Previous Previous ...</span>
        text = re.sub(
            r'<span class="nav-label">(Previous(?:\s+Previous)+)</span>',
            '<span class="nav-label">Previous</span>',
            text
        )
        text = re.sub(
            r'<span class="nav-label">(Next(?:\s+Next)+)</span>',
            '<span class="nav-label">Next</span>',
            text
        )
        text = re.sub(
            r'<span class="nav-label">(Previous Chapter(?:\s+Previous Chapter)+)</span>',
            '<span class="nav-label">Previous Chapter</span>',
            text
        )
        text = re.sub(
            r'<span class="nav-label">(Next Chapter(?:\s+Next Chapter)+)</span>',
            '<span class="nav-label">Next Chapter</span>',
            text
        )
        # Also strip multiple consecutive <nav class="chapter-nav"> blocks; keep first
        # Find all chapter-nav blocks
        navs = re.findall(r'<nav class="chapter-nav">[\s\S]*?</nav>', text)
        if len(navs) > 1:
            # Keep only the last one (most recent rewrite)
            for stale in navs[:-1]:
                text = text.replace(stale, '', 1)
        if text != orig:
            f.write_text(text, encoding='utf-8')
            n += 1
    print(f'  Fixed {n} capstone files')


def fix_capstone_old_chapter_nums():
    """Capstone requirements.html has 'Chapters: 05, 12, 13' style stale chapter list."""
    print('=== Fix 7: capstone old chapter numbers ===')
    p = ROOT / 'capstone' / 'requirements.html'
    if not p.exists():
        return
    text = p.read_text(encoding='utf-8')
    orig = text
    # Old chapter numbers used by capstone
    # 05 → 5 (Decoding), 12 → 14 (Prompt Eng), 13 → 11 (LLM APIs)
    # This is heuristic — the agent flagged "05, 12, 13" as old
    # Simplest fix: replace zero-padded with unpadded
    text = re.sub(r'\bChapters?:\s*0(\d)\b', r'Chapter \1', text)
    text = re.sub(r'\bChapters:\s*0(\d),\s*(\d{1,2}),\s*(\d{1,2})\b', r'Chapters: \1, \2, \3', text)
    if text != orig:
        p.write_text(text, encoding='utf-8')
        print('  Fixed capstone/requirements.html chapter numbers')


def main():
    fix_part15_xi_to_xv()
    fix_part16_modules_xii_to_xvi()
    fix_apx_a6_numbering()
    fix_apx_bc_captions()
    fix_section_80_4_h2()
    fix_capstone_chapter_nav_dups()
    fix_capstone_old_chapter_nums()


if __name__ == '__main__':
    main()
