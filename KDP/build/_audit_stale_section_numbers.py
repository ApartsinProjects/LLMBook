"""Audit: section files whose internal section numbers (in headings, TOC items)
don't match the file's filename-derived section number.

Example: section-30.1.html has subsection IDs and labels "32.1.1, 32.1.2..."
indicating the file was renumbered but internal labels weren't updated.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'output', 'backup', 'KDP/build',
        'KDP/html2pub', 'pagefind', 'temp_epub', 'agents/', 'templates/']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


def get_filename_section_num(p):
    """Returns the expected section number from filename.
    section-30.1.html -> '30.1'
    section-t.4.html -> 't.4'
    """
    m = re.match(r'section-(\d+)\.(\d+)\.html', p.name)
    if m:
        return f'{m.group(1)}.{m.group(2)}'
    m = re.match(r'section-([a-z]+)\.(\d+)\.html', p.name)
    if m:
        return f'{m.group(1)}.{m.group(2)}'
    return None


issues = []
for p in ROOT.rglob('section-*.html'):
    if is_skip(p):
        continue
    expected = get_filename_section_num(p)
    if not expected:
        continue
    # Get expected major/minor parts
    if '.' in expected:
        major, minor = expected.split('.')
    else:
        major, minor = expected, None
    if not major:
        continue
    try:
        soup = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    except Exception:
        continue

    # Find IDs and visible numbering that look like X.Y.Z
    # Patterns: section-internal-toc with bold subsection numbers
    bold_nums = soup.find_all('strong')
    seen_majors = Counter()
    for b in bold_nums:
        txt = b.get_text(strip=True)
        m = re.match(r'^(\d+)\.(\d+)\.(\d+)$', txt)
        if m:
            seen_majors[m.group(1)] += 1

    if seen_majors:
        # Check if the dominant major doesn't match expected
        dom_major = seen_majors.most_common(1)[0][0]
        if str(dom_major) != str(major):
            issues.append({
                'file': str(p.relative_to(ROOT)),
                'expected_major': major,
                'found_major': dom_major,
                'count': seen_majors[dom_major],
            })

print(f'Files with stale internal section numbers: {len(issues)}')
for issue in issues[:50]:
    print(f'  {issue["file"]}')
    print(f'    filename says {issue["expected_major"]}.x but content shows {issue["found_major"]}.x.y ({issue["count"]} times)')
