"""v14.8: scrub residual appendix-isms from Part XII chapters.

After moving appendices W-AC → Part XII modules 36-42, the body content
still uses appendix-style section numbering (W.1, X.2, AC.3) and prose
referring to "this appendix". Convert to chapter-style numbering and
chapter prose.

Transformations:
  - <h2>W.1 ...</h2>  → <h2>36.1 ...</h2>
  - <h2>X.3 ...</h2>  → <h2>37.3 ...</h2>
  - <h2>AA.2 ...</h2> → <h2>40.2 ...</h2>
  - "this appendix" → "this chapter"
  - "This appendix" → "This chapter"
  - "the appendix" → "the chapter" (case-preserved)
  - "Appendix W" → "Chapter 36" (already done by previous move script for
    most, but stragglers may remain in plain prose)

DO NOT modify:
  - Glossary URLs (path is appendices/appendix-f-glossary)
  - Other appendix cross-refs (appendix-r, appendix-s, etc.)
  - .glossary-link / .concept-link href attributes
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]

# Migration map
MIGRATION = [
    ('module-36-legal-llms',          36, 'W'),
    ('module-37-finance-llms',        37, 'X'),
    ('module-38-healthcare-llms',     38, 'Y'),
    ('module-39-education-llms',      39, 'Z'),
    ('module-40-cybersecurity-llms',  40, 'AA'),
    ('module-41-government-llms',     41, 'AB'),
    ('module-42-manufacturing-llms',  42, 'AC'),
]


def fix_file(p: Path, ch: int, letter: str, dry: bool) -> int:
    t = p.read_text(encoding='utf-8')
    orig = t
    n = 0

    # 1. Replace W.N section numbering in <h2>/<h3>/<h4> headings
    # Pattern: a heading that starts with the letter+. followed by digit
    pattern = re.compile(rf'(<h[234][^>]*>){re.escape(letter)}\.(\d+)\s')
    t = pattern.sub(lambda m: f'{m.group(1)}{ch}.{m.group(2)} ', t)

    # 2. Plain text "W.N" outside headings (e.g., references like "see W.3")
    # Only match if W.N is followed by space or punctuation, not part of a longer token
    # Use word-boundary
    pattern2 = re.compile(rf'\b{re.escape(letter)}\.(\d+)\b')
    # But skip occurrences inside href attributes (don't touch URLs)
    # Strategy: split on <a ... > tags and only fix outside them
    # Simpler approach: only run on text content via BeautifulSoup
    from bs4 import BeautifulSoup, NavigableString
    s = BeautifulSoup(t, 'html.parser')
    for el in s.find_all(string=True):
        # Skip text inside <a>, <code>, <pre>, <script>, <style>
        if el.parent and el.parent.name in ('a', 'code', 'pre', 'script', 'style'):
            continue
        text = str(el)
        new_text = pattern2.sub(lambda m: f'{ch}.{m.group(1)}', text)
        # Also "this appendix" -> "this chapter" (case-preserved)
        new_text = re.sub(r'\bthis appendix\b', 'this chapter', new_text)
        new_text = re.sub(r'\bThis appendix\b', 'This chapter', new_text)
        new_text = re.sub(r'\bthe appendix\b', 'the chapter', new_text)
        new_text = re.sub(r'\bThe appendix\b', 'The chapter', new_text)
        # "Appendix W" → "Chapter 36" (capital + letter)
        new_text = re.sub(rf'\bAppendix\s+{letter}\b', f'Chapter {ch}', new_text)
        new_text = re.sub(rf'\bappendix\s+{letter}\b', f'chapter {ch}', new_text)
        if new_text != text:
            n += 1
            el.replace_with(NavigableString(new_text))

    new_t = str(s)
    # Also handle the heading replacement on the serialized string (BS4 may
    # not handle it via text replacement if heading text was actually
    # serialized differently)
    new_t = pattern.sub(lambda m: f'{m.group(1)}{ch}.{m.group(2)} ', new_t)

    if new_t != orig and not dry:
        p.write_text(new_t, encoding='utf-8')
    return n + (orig.count(f'{letter}.') - new_t.count(f'{letter}.'))


def main():
    dry = '--apply' not in sys.argv
    print('DRY RUN.' if dry else 'APPLY mode.')
    print()

    base = ROOT / 'part-12-llm-applications-across-industries'
    total = 0
    for mod_dir, ch, letter in MIGRATION:
        p = base / mod_dir / 'index.html'
        if not p.exists():
            print(f'  SKIP missing: {mod_dir}')
            continue
        n = fix_file(p, ch, letter, dry)
        if n > 0:
            print(f'  {mod_dir}/index.html: {n} replacements (Ch {ch}, was {letter})')
            total += n
    print(f'\nTotal: {total}')


if __name__ == '__main__':
    main()
