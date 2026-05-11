"""v5.5+ fix: repair orphan <a> tags + drop AI disclosure section.

Problem 1: Some prior cleanup script stripped the opening `<a ` from many
anchors, leaving `href="...">link text</a>` as visible plain text in the
rendered HTML. Re-insert the missing `<a ` before each orphan.

Detection: pattern `href="..." > body </a>` where the surrounding context
shows we are NOT inside an open tag (the last `<` before us was already
closed by a `>`).

Problem 2: copyright.html has an "AI-Generated Content Disclosure" section
the author wants removed from the website. Drop the entire <section>.

Idempotent. Run with no args.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

ORPHAN_PAT = re.compile(r'href="(?P<url>[^"]+)">(?P<body>[^<]{1,400}?)</a>')


def is_orphan(text: str, pos: int) -> bool:
    """True if `pos` is NOT inside an open HTML tag.

    We look back 600 chars (long enough to cover the longest paragraph
    text-only run between tags). Two cases mean orphan:
      1. Window has no `<` at all - we're in pure prose
      2. Last `<` is already closed by a `>`
    """
    snippet = text[max(0, pos - 600):pos]
    last_lt = snippet.rfind('<')
    last_gt = snippet.rfind('>')
    if last_lt == -1:
        return True              # case 1: pure prose
    return last_gt > last_lt     # case 2: last tag already closed


def fix_anchors(text: str) -> tuple[str, int]:
    fixed = 0

    def repl(m: re.Match) -> str:
        nonlocal fixed
        if not is_orphan(text, m.start()):
            return m.group(0)
        fixed += 1
        return f'<a href="{m.group("url")}">{m.group("body")}</a>'

    new_text = ORPHAN_PAT.sub(repl, text)
    return new_text, fixed


# Drop the "AI-Generated Content Disclosure" <section> from copyright.html
DISCLOSURE_PAT = re.compile(
    r'\s*<section\s+class="copyright-section">\s*'
    r'<h2>AI-Generated Content Disclosure</h2>'
    r'.*?</section>',
    re.DOTALL | re.IGNORECASE,
)


def drop_ai_disclosure(text: str) -> tuple[str, int]:
    new_text, n = DISCLOSURE_PAT.subn('', text)
    return new_text, n


def main() -> int:
    SKIP_DIRS = {
        'agents', 'KDP', 'node_modules', 'scripts',
        '.git', 'chapter_review', 'downloads',
    }

    candidates = []
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP_DIRS:
            continue
        candidates.append(p)

    print(f'Scanning {len(candidates)} HTML files...')

    total_anchor_fixes = 0
    total_disclosure_drops = 0
    files_anchor = 0

    for p in candidates:
        try:
            text = p.read_text('utf-8', errors='replace')
        except Exception as e:
            print(f'  SKIP {p.relative_to(ROOT)}: {e}')
            continue

        original = text
        text, n_anchor = fix_anchors(text)

        # Only process copyright.html for the disclosure removal
        n_disc = 0
        if p.name == 'copyright.html':
            text, n_disc = drop_ai_disclosure(text)

        if text != original:
            p.write_text(text, encoding='utf-8')
            if n_anchor:
                files_anchor += 1
                total_anchor_fixes += n_anchor
            if n_disc:
                total_disclosure_drops += n_disc
                print(f'  [drop disclosure] {p.relative_to(ROOT)}')

    print(f'\nAnchor repairs: {total_anchor_fixes} across {files_anchor} files')
    print(f'AI disclosure sections dropped: {total_disclosure_drops}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
