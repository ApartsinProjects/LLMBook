"""Wave 20: typography, callout, code-block, and format unification across the book.

Findings from the style audit:

1. **Callout variant typos / outliers**:
   - "fun-fact" (6 instances) → should be "fun-note" (689 canonical, in CSS)
   - "numerical-example" (1) → should be "numeric-example" (22 canonical, in CSS)
   - "whats-next" (15) → no CSS rule defined; remap to "looking-back" (existing
     CSS variant for forward-pointing prose; pairs with looking-back for backward)
     Actually whats-next is forward-pointing; looking-back is backward. Better:
     add CSS for whats-next or remap to "tip" which is the closest existing.
     Choice: add CSS for whats-next using same style as looking-back (since they're
     paired conceptually). Apply book-wide.

2. **Em-dashes (style rule violation)**:
   - 13 em-dashes ("—") in 9 files
   - Replace with appropriate punctuation:
     - In epigraph cites "— Author" → ", Author" (or just "Author")
     - In prose "X — Y" → "X, Y" or "X (Y)" or split into two sentences

3. **Code block class ordering inconsistency**:
   - "pygments-highlighted lang-X" (3398) - canonical
   - "lang-X pygments-highlighted" (403) - reversed order
   - "language-none" (21) - different convention; → "lang-text"
   Normalize to "pygments-highlighted lang-X"

4. **CSS: add .callout.whats-next rule** (paired with looking-back).

The heading-hierarchy skips (225 files with h1 → h3) are a separate concern,
generally driven by appendix sections using h3 for sub-sections of h1. Not
addressing in this pass since it requires structural judgment.
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}


def fix_callout_typos():
    """Fix fun-fact → fun-note, numerical-example → numeric-example."""
    print('=== Fix 1: callout class typos ===')
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        text = text.replace('class="callout fun-fact"', 'class="callout fun-note"')
        text = text.replace('class="callout numerical-example"', 'class="callout numeric-example"')
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n += 1
    print(f'  Fixed {n} files')


def remap_whats_next_to_looking_back():
    """The whats-next callout class has no CSS rule. Remap to looking-back which
    is its conceptual pair (both are narrative bridges to neighboring content)."""
    print('=== Fix 2: whats-next → looking-back ===')
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        text = text.replace('class="callout whats-next"', 'class="callout whats-next"')
        # Actually instead of remapping, let's keep whats-next as a distinct variant
        # and add CSS for it. So no rewrites here.
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n += 1
    print(f'  Kept whats-next; will add CSS rule')


def add_whats_next_css():
    """Add .callout.whats-next CSS rule paired with .callout.looking-back."""
    print('=== Fix 3: add .callout.whats-next CSS ===')
    css_path = ROOT / 'styles' / 'book.css'
    text = css_path.read_text(encoding='utf-8')

    # Find the .callout.looking-back rule to insert next to it
    if '.callout.whats-next' in text:
        print('  Already defined')
        return

    # Match the looking-back block (rule + any companion lines)
    pattern = re.compile(
        r'(\.callout\.looking-back\s*\{[^}]*\})',
        re.DOTALL
    )
    m = pattern.search(text)
    if not m:
        # Try title rule
        pattern2 = re.compile(r'(\.callout\.looking-back\.callout-title[^}]*\})',
                              re.DOTALL)
        m = pattern2.search(text)

    if m:
        # Add whats-next as forward pair: same shape as looking-back but with
        # a different accent color (forward = teal/green; backward = blue/grey)
        new_rule = (
            m.group(1)
            + '\n\n.callout.whats-next {\n'
              '    background: #e8f8f4;\n'
              '    border-left-color: #16a085;\n'
              '}\n'
              '.callout.whats-next .callout-title { color: #117a65; }\n'
              '.callout.whats-next .callout-title::after { content: "\\2192"; color: #117a65; }\n'
        )
        text = text.replace(m.group(1), new_rule, 1)
        css_path.write_text(text, encoding='utf-8')
        print('  Added .callout.whats-next CSS rule paired with looking-back')
    else:
        print('  Could not find looking-back rule to anchor; manual insertion needed')


def remove_em_dashes():
    """Replace em-dashes with appropriate punctuation per context."""
    print('=== Fix 4: remove em-dashes ===')
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        if '—' not in p.read_text(encoding='utf-8'):
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # Pattern 1: cite epigraph attribution "— Author" → ", Author"
        text = re.sub(
            r'<cite>\s*—\s*([^<]+)</cite>',
            r'<cite>, \1</cite>',
            text
        )
        # Pattern 2: general em-dash → comma + space (most common substitute)
        text = text.replace('—', ',')
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n += 1
    print(f'  Fixed {n} files')


def normalize_code_block_classes():
    """Standardize <pre><code class="..."> class ordering and language naming.

    Canonical: <pre><code class="pygments-highlighted lang-X">
    Variants to normalize:
      - "lang-X pygments-highlighted" → swap order
      - "language-none" → "lang-text"
      - other "language-X" → "pygments-highlighted lang-X"
    """
    print('=== Fix 5: code block class ordering ===')
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # "lang-X pygments-highlighted" → "pygments-highlighted lang-X"
        text = re.sub(
            r'(<pre><code class=")lang-([a-z]+)(\s+)pygments-highlighted(")',
            r'\1pygments-highlighted\3lang-\2\4',
            text
        )
        # "language-none" → "pygments-highlighted lang-text"
        text = text.replace(
            '<pre><code class="language-none"',
            '<pre><code class="pygments-highlighted lang-text"'
        )
        # "language-X" → "pygments-highlighted lang-X" (e.g. language-bash, language-yaml)
        text = re.sub(
            r'<pre><code class="language-([a-z]+)"',
            r'<pre><code class="pygments-highlighted lang-\1"',
            text
        )
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n += 1
    print(f'  Normalized {n} files')


def main():
    fix_callout_typos()
    remap_whats_next_to_looking_back()
    add_whats_next_css()
    remove_em_dashes()
    normalize_code_block_classes()


if __name__ == '__main__':
    main()
