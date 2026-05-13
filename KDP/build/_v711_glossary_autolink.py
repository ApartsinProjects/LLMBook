"""9th edition Wave A5: auto-link the first occurrence of each
glossary term in each section to its glossary entry.

How it works:
1. Parse appendices/appendix-f-glossary/section-f.{1..5}.html, extract
   every <div class="glossary-entry" id="gl-XXX"><dt class="glossary-term">
   TERM</dt> ... </div> -> (term, anchor_url).
2. For each section/index file in the book:
   - Skip the glossary itself.
   - Find the FIRST occurrence of each term in PROSE text (not inside
     <a>, <code>, <pre>, headings, callout-title, script/style/title).
   - Wrap the occurrence with
     <a class="glossary-link" href="<rel>/appendices/appendix-f-glossary/
     section-f.N.html#gl-XXX" title="Glossary: TERM">TERM</a>
   - One link per term per file.

Conservative defaults:
- Only matches whole words/phrases (\b boundary on each end).
- Only first occurrence (don't pollute prose with repeats).
- Skips files that already contain `class="glossary-link"` for that
  exact term (idempotent).
- Skips terms whose name is too short (<= 3 chars) or generic
  (e.g. "AI", "ML") to avoid noise.
"""
from __future__ import annotations
import html as html_mod
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GLOSSARY_DIR = ROOT / 'appendices' / 'appendix-f-glossary'
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/',
        'appendix-f-glossary/')  # don't auto-link the glossary itself

# Tags whose interior we must not touch.
PROTECTED_TAGS = (
    'a', 'code', 'pre', 'script', 'style', 'title', 'option',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'dt', 'dd',
    'figcaption',
)
# Don't link terms shorter than this (lots of false positives at <=3 chars).
MIN_TERM_LEN = 4
# Hard blocklist (case-insensitive). These terms exist in the glossary
# but are too generic to safely auto-link.
BLOCKED_TERMS = {
    'ai', 'ml', 'cpu', 'gpu', 'tpu', 'os', 'cli', 'api',
    'json', 'html', 'css', 'sql', 'pdf', 'csv', 'jpg',
    'png', 'svg', 'cpu', 'mlp', 'pos', 'nlp',
}


ENTRY_RE = re.compile(
    r'<div\s+class="glossary-entry"\s+id="(gl-[^"]+)"[^>]*>\s*'
    r'<dt\s+class="glossary-term"[^>]*>(.+?)</dt>',
    re.IGNORECASE | re.DOTALL)


def load_glossary() -> list[tuple[str, str, str]]:
    """Return list of (term, anchor_id, filename) sorted by descending
    term length so multi-word terms win over their substrings."""
    entries: list[tuple[str, str, str]] = []
    for p in sorted(GLOSSARY_DIR.glob('section-f.*.html')):
        text = p.read_text(encoding='utf-8', errors='replace')
        for m in ENTRY_RE.finditer(text):
            anchor = m.group(1)
            term_html = m.group(2)
            # Strip any inline HTML (like parenthetical expansions in <em>).
            term_text = re.sub(r'<[^>]+>', '', term_html)
            # Some entries have "Term (Expansion)" — take just "Term" for
            # the match key, but also try the expansion separately.
            term_text = html_mod.unescape(term_text).strip()
            # Skip blocked / too-short.
            if (len(term_text) < MIN_TERM_LEN
                    or term_text.lower() in BLOCKED_TERMS):
                continue
            entries.append((term_text, anchor, p.name))
            # Also try the bare token before " ("
            if '(' in term_text:
                short = term_text.split('(', 1)[0].strip()
                if (len(short) >= MIN_TERM_LEN
                        and short.lower() not in BLOCKED_TERMS):
                    entries.append((short, anchor, p.name))
    # Sort by descending length so multi-word phrases win over substrings.
    entries.sort(key=lambda x: -len(x[0]))
    # Dedupe (keep first occurrence by sort order = longest first).
    seen_lower: set[str] = set()
    unique: list[tuple[str, str, str]] = []
    for term, anchor, fn in entries:
        key = term.lower()
        if key in seen_lower:
            continue
        seen_lower.add(key)
        unique.append((term, anchor, fn))
    return unique


def rel_to_glossary(p: Path) -> str:
    """Relative path from p's parent directory to the glossary dir."""
    depth = len(p.parent.relative_to(ROOT).parts)
    return '../' * depth + 'appendices/appendix-f-glossary'


# Mask out regions we must not modify.
def mask_protected(text: str) -> list[tuple[int, int]]:
    """Return list of (start, end) char ranges that are inside protected
    tags or HTML attributes."""
    ranges: list[tuple[int, int]] = []
    # Each protected tag
    for tag in PROTECTED_TAGS:
        pat = re.compile(rf'<{tag}\b[^>]*>.*?</{tag}>', re.IGNORECASE | re.DOTALL)
        for m in pat.finditer(text):
            ranges.append((m.start(), m.end()))
    # All HTML start-tags (so we don't touch attribute values)
    for m in re.finditer(r'<[^>]+>', text):
        ranges.append((m.start(), m.end()))
    # All HTML comments
    for m in re.finditer(r'<!--.*?-->', text, re.DOTALL):
        ranges.append((m.start(), m.end()))
    ranges.sort()
    return ranges


def in_any_range(idx: int, ranges: list[tuple[int, int]]) -> bool:
    # Binary search would be faster but the list is small per file.
    for s, e in ranges:
        if idx < s:
            return False
        if idx < e:
            return True
    return False


def autolink_file(text: str, glossary: list[tuple[str, str, str]],
                  rel_pref: str) -> tuple[str, int]:
    ranges = mask_protected(text)
    new_chunks: list[str] = []
    cursor = 0
    linked_terms: set[str] = set()
    n_links = 0
    # Build a combined regex per call: one big alternation, longest-first.
    # Use a sentinel to avoid catastrophic backtracking.
    if not glossary:
        return text, 0
    # We linearize by scanning each term sequentially (simpler than one
    # mega-regex, easier to enforce "first occurrence only").
    # To make this efficient and correct, walk char-by-char NOT — but
    # since each term is independent, do them in length-desc order and
    # mutate `text` as we go.
    for term, anchor, fn in glossary:
        if term.lower() in linked_terms:
            continue
        # Build regex for this term
        # Word boundary: term may contain non-word chars (parens, dashes).
        # Use lookarounds for word boundaries.
        escaped = re.escape(term)
        pat = re.compile(rf'(?<![\w-]){escaped}(?![\w-])', re.IGNORECASE)
        # Recompute protected ranges after prior mutations (cheap enough
        # for 100 terms).
        ranges = mask_protected(text)
        for m in pat.finditer(text):
            if in_any_range(m.start(), ranges):
                continue
            # Wrap this match.
            link = (f'<a class="glossary-link" '
                    f'href="{rel_pref}/{fn}#{anchor}" '
                    f'title="Glossary: {html_mod.escape(term)}">'
                    f'{m.group(0)}</a>')
            text = text[:m.start()] + link + text[m.end():]
            linked_terms.add(term.lower())
            n_links += 1
            break  # one link per term per file
    return text, n_links


def main() -> int:
    fix = '--fix' in sys.argv
    glossary = load_glossary()
    print(f'Loaded {len(glossary)} glossary terms.')
    n_files = 0
    n_links = 0
    for p in sorted(ROOT.rglob('section-*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        # Skip if already auto-linked (idempotent)
        if 'class="glossary-link"' in text:
            continue
        rel_pref = rel_to_glossary(p)
        new_text, k = autolink_file(text, glossary, rel_pref)
        if k > 0:
            n_files += 1
            n_links += k
            if fix:
                p.write_text(new_text, encoding='utf-8')
    print(f'\nFiles touched: {n_files}; glossary links added: {n_links}')
    if not fix:
        print('Re-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
