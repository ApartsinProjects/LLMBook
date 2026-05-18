"""Wave 17L: residual sweeps from cycle-3 audits + missed items from Wave 17k.

1. 347 files with <strong><strong>...</strong></strong> double-wrap (Wave 17c
   caption regex applied twice; need to collapse).
2. Part 16 module content prose still says "Part XII covers what it has not"
   etc. — non-href references missed by 17k's structural regex.
3. Capstone chapter-nav <span class="nav-label">Previous</span><span class="nav-title">
   Previous Previous Previous ... Capstone</span> — stacking is inside nav-title
   not nav-label.
4. Pagefind-meta span artifacts: "P:", "R:", "T:" prefixes in Part 5 second-half
   sections (similar to Wave 17a's fix to 24.13).
5. Ch 26/29 stale "Chapters 21 through 24" ranges in body prose.
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}


def fix_double_strong():
    """Collapse <strong><strong>...</strong></strong> to <strong>...</strong>."""
    print('=== Fix 1: double-wrapped <strong><strong> ===')
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # <strong><strong>X</strong></strong> → <strong>X</strong>
        # Apply repeatedly in case of triple-wrap
        while True:
            new_text = re.sub(
                r'<strong><strong>([\s\S]*?)</strong></strong>',
                r'<strong>\1</strong>',
                text
            )
            if new_text == text:
                break
            text = new_text
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n += 1
    print(f'  Fixed {n} files')


def fix_part16_prose_xii():
    """Part 16 module pages reference "Part XII" in body prose. Rewrite to "Part XVI"."""
    print('=== Fix 2: Part 16 module prose "Part XII" ===')
    part16 = ROOT / 'part-16-llm-agentic-ai-research-frontiers'
    n = 0
    for p in part16.rglob('*.html'):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # In Part 16's own pages, any "Part XII" reference that is about THIS part
        # (Frontiers) should be "Part XVI". Other refs (e.g. to "Part XII: LLM
        # Systems at Scale") should be left alone.
        # Heuristic: replace "Part XII covers" / "Part XII looks ahead" / "Part XII
        # surveys" / "Part XII contains" / standalone "Part XII," / "Part XII." with
        # "Part XVI".
        text = re.sub(
            r'\bPart XII(?= covers| looks ahead| surveys| contains| introduces| presents|,|\.)',
            'Part XVI',
            text
        )
        # Also "the previous chapters cover what the field has settled on. Part XII
        # covers what it has not" — match standalone Part XII followed by space + verb
        text = re.sub(
            r'\bPart XII (?=will |is |provides )',
            'Part XVI ',
            text
        )
        # Cross-refs WITHIN Part 16 prose mentioning "Chapter 62/63/64" (old numbering)
        # Per the agent: "Theory of reasoning, memory, interpretability, and the agency
        # question live in Chapter 62; hardware and systems live in Chapter 63;
        # AGI trajectories live in Chapter 64."
        # New mapping:
        # Old Ch 62 (Frontier Theory) → Ch 81
        # Old Ch 63 (Frontier Systems) → moved to Part 12 ch 58 (Frontier Systems Hardware)
        # Old Ch 64 (AGI Trajectories) → Ch 82
        # We're INSIDE module-80 prose discussing what comes later in this part
        # The current Part 16 is: module-80 (Frontier Arch), module-81 (Theory), module-82 (AGI), module-83 (Tools)
        # So "Theory live in Chapter 62" → "Chapter 81"
        # "hardware live in Chapter 63" → references Ch 58 (Part 12) but that's not in same part
        # "AGI live in Chapter 64" → "Chapter 82"
        text = text.replace(
            'live in Chapter 62; hardware and systems live in Chapter 63; AGI trajectories live in Chapter 64',
            'live in Chapter 81; hardware and systems live in <a href="../../part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/index.html">Chapter 58</a>; AGI trajectories live in Chapter 82'
        )
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n += 1
    print(f'  Fixed {n} Part 16 files')


def fix_capstone_nav_title_stacks():
    """Capstone has stacked text inside nav-title spans, not nav-label."""
    print('=== Fix 3: capstone nav-title stacking ===')
    cap_dir = ROOT / 'capstone'
    if not cap_dir.exists():
        return
    n = 0
    for f in cap_dir.glob('*.html'):
        text = f.read_text(encoding='utf-8')
        orig = text
        # Match patterns like:
        # <span class="nav-title">Previous Previous Previous Previous ... Title</span>
        # Keep only the last word(s) after the repeated prefix
        text = re.sub(
            r'<span class="nav-title">(?:Previous\s+)+([^<]+)</span>',
            r'<span class="nav-title">\1</span>',
            text
        )
        text = re.sub(
            r'<span class="nav-title">(?:Next\s+)+([^<]+)</span>',
            r'<span class="nav-title">\1</span>',
            text
        )
        # Also: "Previous Chapter Previous Chapter ..." → just "Previous Chapter"
        text = re.sub(
            r'<span class="nav-title">(?:Previous Chapter\s+)+([^<]+)</span>',
            r'<span class="nav-title">\1</span>',
            text
        )
        text = re.sub(
            r'<span class="nav-title">(?:Next Chapter\s+)+([^<]+)</span>',
            r'<span class="nav-title">\1</span>',
            text
        )
        if text != orig:
            f.write_text(text, encoding='utf-8')
            n += 1
    print(f'  Fixed {n} capstone files')


def fix_pagefind_meta_artifacts():
    """Botched pagefind-meta spans: '...injected" ... "T: VLA Models..." hidden>'
    pattern leaves visible P:/R:/T: text. Fix by re-emitting proper meta spans.
    """
    print('=== Fix 4: pagefind-meta span artifacts ===')
    # Search for the corruption pattern
    pattern = re.compile(
        r'<span class="pagefind-meta-injected" data-pagefind-meta="part:[^"]+" hidden=""></span>'
        r'([A-Z]):\s+([^"]+)" hidden=""></span>'
    )
    n = 0
    for p in sorted(ROOT.rglob('section-*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # The artifact pattern: a stray letter + ": ..." " hidden> after the part meta span
        # Match and remove the orphan text fragment
        def replace_artifact(m):
            letter = m.group(1)
            rest = m.group(2)
            # Determine chapter from filename
            section_path = str(p)
            m2 = re.search(r'module-(\d+)-([^/\\]+)', section_path)
            if m2:
                ch_num = int(m2.group(1).lstrip('0') or '0')
                # Get module h1 for the chapter title
                idx = p.parent / 'index.html'
                title = f'Chapter {ch_num}'
                if idx.exists():
                    idx_text = idx.read_text(encoding='utf-8')
                    h1 = re.search(r'<h1>([^<]+)</h1>', idx_text)
                    if h1:
                        title = f'Chapter {ch_num}: {h1.group(1).strip()}'
                # Replace artifact with proper chapter meta span
                return (
                    f'<span class="pagefind-meta-injected" data-pagefind-meta="part:'
                    + m.group(0).split('part:')[1].split('"')[0]
                    + f'" hidden=""></span>'
                    + f'<span class="pagefind-meta-injected" data-pagefind-meta="chapter:{title}" hidden=""></span>'
                )
            return m.group(0)
        text = pattern.sub(replace_artifact, text)
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n += 1
    print(f'  Fixed {n} pagefind-meta artifacts')


def fix_stale_chapter_ranges():
    """Ch 26 / Ch 29 in part-6 have stale 'Chapters 21 through 24' references."""
    print('=== Fix 5: stale chapter range refs ===')
    n = 0
    for p in (ROOT / 'part-6-agentic-ai').rglob('*.html'):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # "Chapters 21 through 24" → Part 6 is Chapters 26-30 in canonical
        text = text.replace('Chapters 21 through 24', 'Chapters 26 through 29')
        text = text.replace('Chapters 20-22', 'Chapters 26-28')
        text = text.replace('Chapters 22 through 24', 'Chapters 26 through 28')
        text = text.replace('Chapters 22-25', 'Chapters 26-29')
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n += 1
    print(f'  Fixed {n} files')


def main():
    fix_double_strong()
    fix_part16_prose_xii()
    fix_capstone_nav_title_stacks()
    fix_pagefind_meta_artifacts()
    fix_stale_chapter_ranges()


if __name__ == '__main__':
    main()
