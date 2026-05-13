"""9th edition follow-up: audit prerequisite boxes book-wide.

Two patterns exist:
  A) <div class="prereqs"><ul><li>Chapter NN: ...</li>...</ul></div>
     Used on CHAPTER index pages. Often listed as PLAIN TEXT with no
     <a> links to the referenced chapters.
  B) <div class="prerequisites"><p>This section assumes ... <a>Section X.Y</a> ...</p></div>
     Used on SECTION pages. Usually has inline <a> links.

Audit checks:
  P1. EXISTENCE: does the page have a prereq box? (sections only; chapter
      indexes are exempt because they have a chapter-level prereq list).
  P2. BROKEN LINKS: every <a href> inside the prereq box resolves to a
      real file in the book.
  P3. BARE CHAPTER MENTIONS: chapter-level prereqs that name "Chapter NN"
      or "Section X.Y" without wrapping the name in an <a>. Reportable
      so we can auto-link them.
  P4. ORDER: a prereq pointing at a section that appears LATER in the
      reading order than the current page is a forward-reference and
      probably wrong. Reading order is determined by the spine manifest.

Read-only audit; reports per-file findings + summary.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')
SPINE = ROOT / 'KDP' / 'build' / 'spine_manifest.json'

PREREQ_BLOCK = re.compile(
    r'<div\s+class="prereq(?:s|uisites)"[^>]*>([\s\S]*?)</div>',
    re.IGNORECASE)
A_HREF = re.compile(r'<a\s([^>]*?)href="([^"]+)"([^>]*?)>([^<]*)</a>', re.IGNORECASE)
# Bare references: "Chapter NN" or "Section N.M" or "Module NN" not inside <a>.
BARE_REF = re.compile(
    r'\b(?:Chapter|Section|Module|Appendix)\s+(\d+(?:\.\d+)?[a-z]?|[A-Z]{1,3})\b')


def load_spine_order() -> dict[str, int]:
    """Return mapping path -> spine index."""
    try:
        with SPINE.open('r', encoding='utf-8') as f:
            spine = json.load(f)
    except Exception:
        return {}
    return {entry['path'].replace('\\', '/'): i
            for i, entry in enumerate(spine)}


def main() -> int:
    spine_order = load_spine_order()
    n_pages = 0
    n_with_prereq = 0
    n_broken = 0
    n_bare = 0
    n_forward = 0
    by_file: dict[str, list[str]] = {}
    chapter_level_unlinked: list[tuple[str, list[str]]] = []
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        rel = sp.split(ROOT.name + '/', 1)[-1] if ROOT.name in sp else sp
        # Normalize to repo-relative path used in spine
        try:
            relp = str(p.relative_to(ROOT)).replace('\\', '/')
        except ValueError:
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        is_section = relp.split('/')[-1].startswith('section-')
        if not (is_section or relp.endswith('/index.html')):
            continue
        # Appendices and front-matter are reference material, not
        # prerequisite-gated. Don't flag them as missing prereqs.
        is_reference = (relp.startswith('appendices/') or
                        relp.startswith('front-matter/') or
                        relp.startswith('capstone/'))
        n_pages += 1
        blocks = list(PREREQ_BLOCK.finditer(text))
        # P1: missing prereq on section pages
        page_issues: list[str] = []
        if not blocks:
            if is_section and not is_reference:
                page_issues.append('P1: no prereq box on this section page')
            else:
                # Chapter-index page without prereqs — OK on Part-Intro pages
                # which point at parts (not sections), but a chapter index
                # without prereqs is unusual. Allow it.
                pass
        else:
            n_with_prereq += 1
            for m in blocks:
                inner = m.group(1)
                # P2: validate links
                for a in A_HREF.finditer(inner):
                    attrs = (a.group(1) or '') + (a.group(3) or '')
                    # Skip auto-injected glossary-link tooltips
                    if 'glossary-link' in attrs:
                        continue
                    href = unquote(a.group(2)).split('#', 1)[0].strip()
                    if not href:
                        continue
                    if (href.startswith('http://') or href.startswith('https://')
                            or href.startswith('mailto:')):
                        continue
                    target = (p.parent / href).resolve()
                    if not target.exists():
                        n_broken += 1
                        page_issues.append(f'P2: broken link -> {href}')
                    elif spine_order:
                        try:
                            tgt_rel = str(target.relative_to(ROOT)
                                          ).replace('\\', '/')
                        except ValueError:
                            tgt_rel = ''
                        if tgt_rel in spine_order and relp in spine_order:
                            if spine_order[tgt_rel] >= spine_order[relp]:
                                # Forward / self reference
                                n_forward += 1
                                # Skip self-references (rel == tgt_rel)
                                if tgt_rel != relp:
                                    page_issues.append(
                                        f'P4: forward-ref -> {href} '
                                        f'(target later in spine)')
                # P3: bare chapter/section mentions
                # Strip <a>...</a> blocks first so we don't double-count
                inner_noa = re.sub(
                    r'<a\s[^>]*>[^<]*</a>', '', inner, flags=re.IGNORECASE)
                bare = list(BARE_REF.finditer(inner_noa))
                if bare:
                    n_bare += len(bare)
                    refs = ', '.join(
                        f'"{b.group(0)}"' for b in bare[:5])
                    page_issues.append(
                        f'P3: bare ref(s) (no <a> wrap): {refs}'
                        + (f' (+{len(bare)-5} more)' if len(bare) > 5 else ''))
                    if not is_section:
                        chapter_level_unlinked.append(
                            (relp, [b.group(0) for b in bare]))
        if page_issues:
            by_file[relp] = page_issues

    print(f'Pages scanned: {n_pages}')
    print(f'Pages with prereq box: {n_with_prereq}')
    print(f'Missing prereq (sections): {sum(1 for v in by_file.values() if any("P1" in x for x in v))}')
    print(f'Broken prereq links (P2): {n_broken}')
    print(f'Bare chapter/section mentions (P3): {n_bare}')
    print(f'Forward-references (P4): {n_forward}')
    print()
    # Per-file findings
    for relp, issues in sorted(by_file.items()):
        # Only print broken/forward/missing; skip pure-P3 noise (covered by summary)
        critical = [i for i in issues if 'P1' in i or 'P2' in i or 'P4' in i]
        if critical:
            print(f'  {relp}:')
            for i in critical:
                print(f'    - {i}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
