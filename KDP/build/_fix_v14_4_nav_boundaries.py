"""v14.4: targeted fixes for the 10 cross-boundary nav asymmetries.

Each is a specific boundary where the chain disagrees with itself. Fix
direction chosen to match the natural reading order:

  toc -> front-matter/* -> part-1/module-00/index -> sections -> ... ->
  part-11/module-35/sections -> appendices/index -> appendix-a -> ... ->
  appendix-ak -> capstone

For each fix: update the broken anchor href + text. Direct edits via
BeautifulSoup.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import os
import sys

ROOT = Path(__file__).resolve().parents[2]


def set_nav_link(html_path, kind, target_path, title=None):
    """Set the .prev/.up/.next anchor in html_path to point to target_path."""
    p = ROOT / html_path
    if not p.exists():
        print(f'  SKIP (not found): {html_path}')
        return False
    s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    nav = s.find('nav', class_='chapter-nav')
    if not nav:
        print(f'  SKIP (no chapter-nav): {html_path}')
        return False
    a = nav.find('a', class_=kind)
    if not a:
        print(f'  SKIP (no {kind} anchor): {html_path}')
        return False

    tgt = ROOT / target_path
    rel = os.path.relpath(tgt, p.parent).replace('\\', '/')

    if title is None:
        # Read target's <h1> for title
        if tgt.exists():
            tgt_s = BeautifulSoup(tgt.read_text(encoding='utf-8'), 'html.parser')
            h1 = tgt_s.find('h1')
            title = h1.get_text(strip=True) if h1 else 'Next'
        else:
            title = 'Next'

    old_href = a.get('href', '')
    if old_href == rel:
        return False  # already correct

    a['href'] = rel
    a.clear()
    a.append(title[:55])
    return s, p


def apply(fixes, dry):
    n = 0
    for fix in fixes:
        result = set_nav_link(fix['file'], fix['kind'], fix['target'],
                              fix.get('title'))
        if result:
            soup, p = result
            n += 1
            print(f'  fix {fix["kind"]} in {fix["file"]} -> {fix["target"]}')
            if not dry:
                p.write_text(str(soup), encoding='utf-8')
    return n


FIXES = [
    # 1. module-00/index.prev should be copyright (not toc)
    {
        'file': 'part-1-foundations/module-00-ml-pytorch-foundations/index.html',
        'kind': 'prev',
        'target': 'front-matter/copyright.html',
        'title': 'Copyright & Legal',
    },
    # 2. module-35.4.next should be appendices/index (not module-06)
    {
        'file': 'part-11-idea-to-product/module-35-shipping-scaling/section-35.4.html',
        'kind': 'next',
        'target': 'appendices/index.html',
        'title': 'Appendices',
    },
    # 3. appendix-a/index.prev should be appendices/index (not module-17.5)
    {
        'file': 'appendices/appendix-a-mathematical-foundations/index.html',
        'kind': 'prev',
        'target': 'appendices/index.html',
        'title': 'Appendices',
    },
    # 4. capstone/index.prev should be appendix-ak (not appendix-ai)
    {
        'file': 'capstone/index.html',
        'kind': 'prev',
        'target': 'appendices/appendix-ak-course-syllabi/index.html',
        'title': 'Course Syllabi',
    },
    # 5. appendix-t/section-t.7.next should be appendix-u/index (not u.1)
    {
        'file': 'appendices/appendix-t-distributed-ml/section-t.7.html',
        'kind': 'next',
        'target': 'appendices/appendix-u-docker-containers/index.html',
        'title': 'Docker Containerization',
    },
    # 6. appendix-w/index.prev should be appendix-v/section-v.3 (not v/index)
    {
        'file': 'appendices/appendix-w-legal-llms/index.html',
        'kind': 'prev',
        'target': 'appendices/appendix-v-tooling-ecosystem/section-v.3.html',
    },
    # 7. appendices/index.prev — that was module-17/17.5 historically. Should
    #    be the LAST page of part-11 (35.4).
    {
        'file': 'appendices/index.html',
        'kind': 'prev',
        'target': 'part-11-idea-to-product/module-35-shipping-scaling/section-35.4.html',
    },
]


if __name__ == '__main__':
    dry = '--apply' not in sys.argv
    print('DRY RUN. Pass --apply.' if dry else 'APPLY mode.')
    print()
    n = apply(FIXES, dry)
    print(f'\nTotal fixes applied: {n}')
