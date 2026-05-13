"""Wave 14: enforce chapter-numbering and part-label consistency book-wide.

Root cause for the 177 detected mismatches: when chapters were renumbered
(v6.40 et seq.) the directory names were updated but the embedded
metadata in section/index HTML wasn't. Result: section-31.1 says it
belongs to Chapter 28 in pagefind metadata, section-32.1 says Chapter 29,
section-33/34 say Chapter 30/32, etc. A reader searching the book by
chapter number gets wrong results.

This script is the single source of truth: it reads each module
directory name and the canonical (h1 + part dir name) from the module
index file, then rewrites every section in that module so that:
  - <div class="chapter-label">  uses canonical "Chapter NN: Title"
  - data-pagefind-meta="chapter:..."  uses canonical
  - data-pagefind-meta="part:..."  uses canonical
  - any double-escape "&amp;amp;" -> "&amp;"

Idempotent. Run as detector (default) or with --fix to apply.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/')

PART_NAMES_FALLBACK = {
    'part-1-foundations': 'Part I: Foundations',
    'part-2-understanding-llms': 'Part II: Understanding LLMs',
    'part-3-working-with-llms': 'Part III: Working with LLMs',
    'part-4-training-adapting': 'Part IV: Training and Adapting',
    'part-5-retrieval-conversation': 'Part V: Retrieval and Conversation',
    'part-6-agentic-ai': 'Part VI: Agentic AI',
    'part-7-multimodal-applications': 'Part VII: Multimodal and Applications',
    'part-8-evaluation-production': 'Part VIII: Evaluation and Production',
    'part-9-safety-strategy': 'Part IX: Safety and Strategy',
    'part-10-frontiers': 'Part X: Frontiers',
    'part-11-idea-to-product': 'Part XI: From Idea to Product',
}


def canonical_for(module_dir: Path) -> dict | None:
    """Read each module's canonical (chapter_number, chapter_title, part_label)."""
    m = re.match(r'module-(\d+)', module_dir.name)
    if not m:
        return None
    chap_n = int(m.group(1))
    part_dir = module_dir.parent.name
    part_label = PART_NAMES_FALLBACK.get(part_dir, part_dir)

    # Read title from the module index
    idx = module_dir / 'index.html'
    if not idx.exists():
        return None
    text = idx.read_text(encoding='utf-8', errors='replace')
    h1_m = re.search(r'<h1[^>]*>([^<]+)</h1>', text)
    chap_title = h1_m.group(1).strip() if h1_m else f'Chapter {chap_n:02d}'

    # Use canonical chapter label "Chapter NN: Title" (NN = zero-padded)
    chapter_label = f'Chapter {chap_n}: {chap_title}'
    return {
        'chapter_n': chap_n,
        'chapter_title': chap_title,
        'chapter_label': chapter_label,
        'part_label': part_label,
        'index_path': idx,
    }


def fix_html(text: str, canonical: dict) -> tuple[str, list[str]]:
    """Apply 4 normalizations. Returns (new_text, list_of_changes_made)."""
    changes = []
    new_text = text

    # 1. Strip double-escape &amp;amp; -> &amp; (only inside metadata attributes
    # that arise from template-rendering bugs; we fix it everywhere as it's
    # always wrong in HTML body too).
    if '&amp;amp;' in new_text:
        new_text = new_text.replace('&amp;amp;', '&amp;')
        changes.append('strip &amp;amp; double-escape')

    # 2. <div class="chapter-label"> ... </div> body
    # Replace the FULL chapter-label div content.
    label_pattern = re.compile(
        r'(<div class="chapter-label"[^>]*>)(?:<a[^>]*>)?\s*Chapter\s+\d+[^<]*?(?:</a>)?(\s*</div>)',
        re.DOTALL,
    )
    canonical_label_html = (
        f'<a href="index.html">{canonical["chapter_label"]}</a>'
    )
    if label_pattern.search(new_text):
        new_text2, n = label_pattern.subn(
            lambda m: f'{m.group(1)}{canonical_label_html}{m.group(2)}',
            new_text,
        )
        if new_text2 != new_text:
            changes.append('chapter-label')
            new_text = new_text2

    # 3. data-pagefind-meta="chapter:..."  (in BOTH inline attrs and the
    # injected hidden span)
    pf_chap_pattern = re.compile(
        r'data-pagefind-meta="chapter:Chapter\s+\d+:[^"]*"'
    )
    canonical_pf_chap = f'data-pagefind-meta="chapter:{canonical["chapter_label"]}"'
    new_text2, n = pf_chap_pattern.subn(canonical_pf_chap, new_text)
    if new_text2 != new_text:
        changes.append(f'pf-chap x{n}')
        new_text = new_text2

    # 4. data-pagefind-meta="part:..."
    pf_part_pattern = re.compile(
        r'data-pagefind-meta="part:[^"]*"'
    )
    canonical_pf_part = f'data-pagefind-meta="part:{canonical["part_label"]}"'
    new_text2, n = pf_part_pattern.subn(canonical_pf_part, new_text)
    if new_text2 != new_text:
        changes.append(f'pf-part x{n}')
        new_text = new_text2

    return new_text, changes


def main() -> int:
    fix_mode = '--fix' in sys.argv
    n_files_changed = 0
    n_total_changes = 0
    n_defects = 0

    for module_dir in sorted(ROOT.glob('part-*/module-*')):
        canonical = canonical_for(module_dir)
        if not canonical:
            continue
        for html in sorted(module_dir.glob('*.html')):
            try:
                text = html.read_text(encoding='utf-8', errors='replace')
            except Exception:
                continue
            new_text, changes = fix_html(text, canonical)
            if changes:
                n_defects += len(changes)
                if fix_mode:
                    html.write_text(new_text, encoding='utf-8')
                    n_files_changed += 1
                    n_total_changes += len(changes)
                    print(f'  fixed: {html.relative_to(ROOT)}  [{", ".join(changes)}]')
                else:
                    print(f'  defect: {html.relative_to(ROOT)}  [{", ".join(changes)}]')

    print()
    if fix_mode:
        print(f'Applied {n_total_changes} changes across {n_files_changed} files.')
    else:
        print(f'Found {n_defects} defects. Re-run with --fix to apply.')
    return 1 if n_defects and not fix_mode else 0


if __name__ == '__main__':
    sys.exit(main())
