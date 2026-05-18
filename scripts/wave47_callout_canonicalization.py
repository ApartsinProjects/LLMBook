"""Wave 47: Three callout canonicalization sweeps.

1. Lab/exercise callouts using <h3 class="lab-title">...</h3> instead of
   <div class="callout-title">...</div>. Convert in place.

2. Bare <h2>Key Takeaways</h2> followed by <ul>...</ul> not wrapped in a
   callout. Wrap both into a canonical <div class="callout key-takeaway">.

3. CamelCase callout-title prefixes (NumericExample, KeyInsight, LookingBack,
   WhatsNext, ResearchFrontier, etc.) need a space between words. Map:
     NumericExample -> Numeric Example
     KeyInsight     -> Key Insight
     KeyTakeaway    -> Key Takeaway
     LookingBack    -> Looking Back
     WhatsNext      -> What's Next
     ResearchFrontier -> Research Frontier
     ProductionPattern -> Production Pattern
     PracticalExample -> Practical Example
     ThesisThread   -> Thesis Thread
     CrossRef       -> Cross-Reference
     SelfCheck      -> Self-Check
     BigPicture     -> Big Picture
     FunFact        -> Fun Fact
     RealWorldScenario -> Real-World Scenario
     LibraryShortcut -> Library Shortcut
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# --- Sweep 1: lab/exercise h3 -> callout-title ---
# Match the h3 inside the callout-title slot. Use a non-greedy multi-line.
LAB_H3_RE = re.compile(
    r'(<div\s+class="callout (?:lab|exercise)"[^>]*>\s*)<h[34]\b[^>]*class="(?:lab-title|exercise-title)"[^>]*>([^<]+)</h[34]>',
    re.IGNORECASE,
)

# --- Sweep 2: Key Takeaways h2 + ul wrap ---
KEY_TAKEAWAYS_RE = re.compile(
    r'<h2\s+id="key-takeaways"[^>]*>Key Takeaways?</h2>\s*<ul>',
    re.IGNORECASE,
)

# --- Sweep 3: camelCase prefix fixes ---
PREFIX_MAP = [
    ('NumericExample', 'Numeric Example'),
    ('KeyInsight', 'Key Insight'),
    ('KeyTakeaway', 'Key Takeaway'),
    ('KeyTakeaways', 'Key Takeaways'),
    ('LookingBack', 'Looking Back'),
    ('WhatsNext', "What's Next"),
    ('ResearchFrontier', 'Research Frontier'),
    ('ProductionPattern', 'Production Pattern'),
    ('PracticalExample', 'Practical Example'),
    ('ThesisThread', 'Thesis Thread'),
    ('CrossRef', 'Cross-Reference'),
    ('SelfCheck', 'Self-Check'),
    ('BigPicture', 'Big Picture'),
    ('FunFact', 'Fun Fact'),
    ('RealWorldScenario', 'Real-World Scenario'),
    ('LibraryShortcut', 'Library Shortcut'),
]
# Build a single regex: match the camelCase forms inside <div class="callout-title">
TITLE_PREFIX_RE = re.compile(
    r'(<div\s+class="callout-title"[^>]*>\s*)('
    + '|'.join(re.escape(k) for k, _ in PREFIX_MAP)
    + r')(?=[:\s])',
    re.IGNORECASE,
)
PREFIX_LOOKUP = {k.lower(): v for k, v in PREFIX_MAP}


def fix_lab_h3(text: str) -> tuple[str, int]:
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        prefix = m.group(1)
        title = m.group(2)
        return f'{prefix}<div class="callout-title">{title}</div>'

    return LAB_H3_RE.sub(repl, text), n


def fix_key_takeaways(text: str) -> tuple[str, int]:
    """Wrap <h2>Key Takeaways</h2><ul>...</ul> in a callout key-takeaway div.

    Only acts when:
      - The h2 is NOT already inside a <div class="callout">
      - A </ul> end exists within 4000 chars after the open
    """
    n = 0
    new_parts: list[str] = []
    last_end = 0
    for m in KEY_TAKEAWAYS_RE.finditer(text):
        # Find the matching </ul>
        ul_end = text.find('</ul>', m.end())
        if ul_end == -1 or ul_end - m.end() > 4000:
            continue
        # Check if already inside a callout — look back up to 1000 chars for
        # a <div class="callout" that's not yet closed.
        before = text[max(0, m.start() - 1000):m.start()]
        last_callout = before.rfind('<div class="callout ')
        last_callout_close = before.rfind('</div>')
        if last_callout > last_callout_close:
            continue
        # Build the new wrapped content
        original = text[m.start():ul_end + 5]
        ul_content = original[m.end() - m.start() - 4:]  # '<ul>' + ... + '</ul>'
        # Actually rewrap: open callout, callout-title, then the ul (keeping
        # the original structure intact), then close callout.
        new_block = (
            '<div class="callout key-takeaway">\n'
            '<div class="callout-title">Key Takeaways</div>\n'
            + ul_content
            + '\n</div>'
        )
        new_parts.append(text[last_end:m.start()])
        new_parts.append(new_block)
        last_end = ul_end + 5
        n += 1
    new_parts.append(text[last_end:])
    return (''.join(new_parts) if n > 0 else text), n


def fix_title_prefix(text: str) -> tuple[str, int]:
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        opener = m.group(1)
        kw = m.group(2)
        canonical = PREFIX_LOOKUP[kw.lower()]
        return f'{opener}{canonical}'

    return TITLE_PREFIX_RE.sub(repl, text), n


def main():
    n_lab = 0
    n_kt = 0
    n_prefix = 0
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        text, c1 = fix_lab_h3(text)
        text, c2 = fix_key_takeaways(text)
        text, c3 = fix_title_prefix(text)
        if text != orig:
            p.write_text(text, encoding='utf-8')
            files_touched += 1
            n_lab += c1
            n_kt += c2
            n_prefix += c3
    print(f'Lab/exercise h3 -> callout-title: {n_lab}')
    print(f'Key Takeaways wrapped in callout: {n_kt}')
    print(f'CamelCase title prefixes fixed:   {n_prefix}')
    print(f'Files touched:                    {files_touched}')


if __name__ == '__main__':
    main()
