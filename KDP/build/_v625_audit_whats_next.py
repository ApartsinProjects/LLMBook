"""Audit "What's Next" / "What Comes Next" boxes for accurate alignment.

Each section ending should preview the next section / chapter / part. If the
box mentions a section by name or number, that target should:
  1. Exist on disk
  2. Match the actual NEXT section in reading order (per chapter spine)
  3. Have its real title (not a stale or rewritten one)
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PARTS_ORDER = [
    'part-1-foundations', 'part-2-understanding-llms', 'part-3-working-with-llms',
    'part-4-training-adapting', 'part-5-retrieval-conversation', 'part-6-agentic-ai',
    'part-7-multimodal-applications', 'part-8-evaluation-production',
    'part-9-safety-strategy', 'part-10-frontiers', 'part-11-idea-to-product',
]


def get_h1(p: Path) -> str:
    text = p.read_text(encoding='utf-8', errors='replace')
    m = re.search(r'<h1[^>]*>(.+?)</h1>', text, re.DOTALL)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return p.stem


def build_spine() -> list[Path]:
    """Linear order of all section pages."""
    spine = []
    for pdir in PARTS_ORDER:
        p = ROOT / pdir
        if not p.exists():
            continue
        mods = sorted(p.glob('module-*'),
                      key=lambda d: int(re.match(r'module-0*(\d+)-', d.name).group(1)))
        for m in mods:
            # Sort sections by NUMERIC tail (10 > 2, not '10' < '2')
            def _num_key(path):
                m2 = re.match(r'section-(\d+)\.(\d+)(?:\.(\d+))?', path.stem)
                if not m2:
                    return (9999, 9999, 9999)
                a = int(m2.group(1))
                b = int(m2.group(2))
                c = int(m2.group(3)) if m2.group(3) else 0
                return (a, b, c)
            sections = sorted(m.glob('section-*.html'), key=_num_key)
            spine.extend(sections)
    return spine


def main() -> int:
    spine = build_spine()
    spine_map = {p: i for i, p in enumerate(spine)}
    print(f'Spine: {len(spine)} sections')

    issues = []
    for i, p in enumerate(spine):
        text = p.read_text(encoding='utf-8', errors='replace')
        # Find <div class="whats-next">...</div>
        wn = re.search(r'<div class="whats-next">(.*?)</div>', text, re.DOTALL)
        if not wn:
            continue
        body = wn.group(1)
        # Pull the first <a href="..."> in the box — that's the "next" target
        link = re.search(r'<a href="([^"]+)"[^>]*>([^<]+)</a>', body)
        if not link:
            continue
        href, label = link.group(1), link.group(2)
        # Resolve href to a real file relative to this section's directory
        if href.startswith('http://') or href.startswith('https://'):
            continue  # external link, skip
        target = (p.parent / href).resolve()
        # Check existence
        if not target.exists():
            issues.append((str(p.relative_to(ROOT)), 'BROKEN', f'href={href}'))
            continue
        # Check target is the real next section
        if i + 1 < len(spine):
            actual_next = spine[i + 1]
            if target != actual_next:
                # OK if it's a chapter index (intentional jump to chapter wrap)
                if target.name == 'index.html':
                    pass
                else:
                    actual_rel = str(actual_next.relative_to(ROOT)).replace('\\', '/')
                    target_rel = str(target.relative_to(ROOT)).replace('\\', '/')
                    issues.append((
                        str(p.relative_to(ROOT)).replace('\\', '/'),
                        'WRONG-TARGET',
                        f'whats-next says {target_rel} but actual next is {actual_rel}',
                    ))

    print(f'\n{len(issues)} issues found:\n')
    for f, kind, detail in issues[:30]:
        print(f'  [{kind}] {f}')
        print(f'         {detail}')
    if len(issues) > 30:
        print(f'  ... +{len(issues) - 30} more')
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
