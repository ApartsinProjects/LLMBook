"""v6.14: Normalize the bottom-nav on every chapter index page.

USER REPORT
"module-36-idea-to-product/index.html, bottom navigation (middle panel)
 is non-standard, root cause and fix everywhere"

ROOT CAUSE
Every chapter index file (35 of 35) has its <nav class="chapter-nav">
rendered as:

  <nav class="chapter-nav">
    <a class="prev" href="...">prev section title</a>
    Part XI: From Idea to AI Product            <-- PLAIN TEXT, not a link
    <a class="next" href="section-X.1.html">next section</a>
  </nav>

Section pages use a three-link pattern (prev / up / next) with `<a class="up">`
pointing to the chapter index. But chapter index pages have:
  - prev with a real <a>
  - middle PLAIN TEXT (not navigable; visually inconsistent)
  - next with a real <a>

Module-00 is doubly broken: prev is also plain text.

FIX
Rewrite every chapter index nav to use a uniform 3-link pattern:

  <nav class="chapter-nav">
    <a class="prev" href="...">prev label</a>     (LAST section of previous chapter,
                                                   OR Table of Contents for chapter 0)
    <a class="up"   href="../index.html">Part R: Title</a>
    <a class="next" href="section-N.1.html">first-section title</a>
  </nav>

The part-spine is built from the on-disk directory structure (the canonical
order used in v5.9's chapter-spine work).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


PART_ORDER = [
    'part-1-foundations',
    'part-2-understanding-llms',
    'part-3-working-with-llms',
    'part-4-training-adapting',
    'part-5-retrieval-conversation',
    'part-6-agentic-ai',
    'part-7-multimodal-applications',
    'part-8-evaluation-production',
    'part-9-safety-strategy',
    'part-10-frontiers',
    'part-11-idea-to-product',
]

# Roman numeral for each part — match the canonical labels used in v5.9.
PART_LABEL = {
    'part-1-foundations':             'Part I: Foundations',
    'part-2-understanding-llms':      'Part II: Understanding LLMs',
    'part-3-working-with-llms':       'Part III: Working with LLMs',
    'part-4-training-adapting':       'Part IV: Training and Adapting',
    'part-5-retrieval-conversation':  'Part V: Retrieval and Conversation',
    'part-6-agentic-ai':              'Part VI: Agentic AI',
    'part-7-multimodal-applications': 'Part VII: AI Applications',
    'part-8-evaluation-production':   'Part VIII: Evaluation and Production',
    'part-9-safety-strategy':         'Part IX: Safety and Strategy',
    'part-10-frontiers':              'Part X: Frontiers',
    'part-11-idea-to-product':        'Part XI: From Idea to AI Product',
}


def build_spine() -> list[tuple[str, str, int]]:
    """Return [(part_dir, module_dir, chapter_num)] in reading order."""
    spine = []
    for pdir in PART_ORDER:
        p = ROOT / pdir
        if not p.exists():
            continue
        mods = sorted(p.glob('module-*'),
                      key=lambda d: int(re.match(r'module-0*(\d+)-', d.name).group(1)))
        for m in mods:
            n = int(re.match(r'module-0*(\d+)-', m.name).group(1))
            spine.append((pdir, m.name, n))
    return spine


def section_title(p: Path) -> str:
    """Pull the <h1> title (or chapter-label) from a section/index file."""
    text = p.read_text(encoding='utf-8', errors='replace')
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', text)
    if not m:
        return p.stem
    return m.group(1).strip()


def last_section_of(part_dir: str, module_dir: str) -> Path | None:
    """Return the path to the LAST section file in a chapter, or None."""
    mod = ROOT / part_dir / module_dir
    sections = sorted(mod.glob('section-*.html'))
    return sections[-1] if sections else None


def first_section_of(part_dir: str, module_dir: str) -> Path | None:
    """Return the path to the FIRST section file (section-N.1.html style)."""
    mod = ROOT / part_dir / module_dir
    sections = sorted(mod.glob('section-*.html'))
    return sections[0] if sections else None


def fix_chapter_index(idx: int, spine: list[tuple[str, str, int]]) -> bool:
    """Rewrite the chapter-nav of spine[idx]'s index.html. Returns True if changed."""
    part_dir, module_dir, num = spine[idx]
    idx_path = ROOT / part_dir / module_dir / 'index.html'
    if not idx_path.exists():
        return False
    text = idx_path.read_text(encoding='utf-8')

    # --- Determine prev ---
    if idx == 0:
        prev_href = '../../toc.html'
        prev_label = 'Table of Contents'
    else:
        prev_pdir, prev_mdir, _ = spine[idx - 1]
        prev_last = last_section_of(prev_pdir, prev_mdir)
        if prev_last:
            # Relative path from idx_path to prev_last
            # idx_path lives at part/module/index.html
            # prev_last is at prev_part/prev_module/section-X.Y.html
            if prev_pdir == part_dir:
                # Same part — go up one (out of this module dir) then into prev module
                rel_href = f'../{prev_mdir}/{prev_last.name}'
            else:
                rel_href = f'../../{prev_pdir}/{prev_mdir}/{prev_last.name}'
            prev_label = section_title(prev_last)
            # Strip section-number prefix from label
            prev_label = re.sub(r'^\d+\.\d+(?:\.\d+)?\s+', '', prev_label)
            prev_href = rel_href
        else:
            prev_href = '../../toc.html'
            prev_label = 'Table of Contents'

    # --- up ---
    up_href = '../index.html'
    up_label = PART_LABEL[part_dir]

    # --- next ---
    first_sec = first_section_of(part_dir, module_dir)
    if first_sec:
        next_label = section_title(first_sec)
        next_label = re.sub(r'^\d+\.\d+(?:\.\d+)?\s+', '', next_label)
        next_href = first_sec.name
    else:
        next_href = '#'
        next_label = 'No sections yet'

    # --- build new nav ---
    new_nav = (
        '<nav class="chapter-nav">\n'
        f'<a class="prev" href="{prev_href}">{prev_label}</a>\n'
        f'<a class="up" href="{up_href}">{up_label}</a>\n'
        f'<a class="next" href="{next_href}">{next_label}</a>\n'
        '</nav>'
    )

    # Idempotent: skip if already correct (cheap check on up-link presence + label match)
    if f'class="up" href="{up_href}">{up_label}</a>' in text \
            and f'class="prev" href="{prev_href}"' in text \
            and f'class="next" href="{next_href}"' in text:
        return False

    # Replace the existing nav
    new_text, n = re.subn(
        r'<nav class="chapter-nav">.*?</nav>',
        new_nav,
        text,
        count=1,
        flags=re.DOTALL,
    )
    if n == 0:
        return False
    idx_path.write_text(new_text, encoding='utf-8')
    return True


def main() -> int:
    spine = build_spine()
    print(f'Built chapter spine: {len(spine)} chapters\n')

    fixed = 0
    for i, (pdir, mdir, num) in enumerate(spine):
        if fix_chapter_index(i, spine):
            print(f'  rewrote nav: Ch {num}  {pdir}/{mdir}/index.html')
            fixed += 1

    print(f'\nNormalized {fixed} chapter-index navs.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
