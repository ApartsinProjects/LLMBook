"""Wave 22: bibliography format + math rendering root-cause fixes.

Bibliography (root cause): 9 section files in Part 5 modules 21-22 use the
legacy `<div class="bibliography"><ol><li>...</li></ol></div>` template instead
of the canonical book-wide format which is:

  <details class="bibliography-collapsible" open>
  <summary><strong>Further Reading</strong></summary>
  <section class="bibliography">
  <div class="bib-entry-card">
  <div class="bib-ref">Author (Year). <a ...>"Title."</a> Venue.</div>
  </div>
  ...
  </section>
  </details>

The legacy form doesn't get the "Further Reading" collapsible header, doesn't
use bib-entry-card cards (which have hover/border styling), and uses <em>
italics for titles instead of quoted titles inside the link.

Math (root cause): the same 9 files were authored without KaTeX includes in
their <head>. They use ASCII math inside <code> blocks like:

  <p><code>L = -1/(2N) * [ Sum_i log( ... ) ]</code></p>

which renders as a plain monospaced code line. The canonical form uses KaTeX:

  <p>$L = -\\frac{1}{2N} \\left[ \\sum_i \\log\\frac{...}{...} \\right]$</p>

with KaTeX <link>/<script> tags in <head> for auto-render.

This wave:
  1. Adds the KaTeX include block to the <head> of each affected file
  2. Converts <div class="bibliography"><ol> blocks to the canonical
     Further Reading + bib-entry-card form
  3. Audits each affected file's body for ASCII-math-in-<code> patterns
     and emits a manual-review list (a few specific known cases get
     auto-converted; the rest are flagged for review).
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

# Files identified by audit as using legacy <div class="bibliography"><ol>:
LEGACY_BIB_FILES = [
    'part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.1.html',
    'part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.2.html',
    'part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.3.html',
    'part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.4.html',
    'part-5-multimodal-llms/module-22-vision-language-models/section-22.1.html',
    'part-5-multimodal-llms/module-22-vision-language-models/section-22.2.html',
    'part-5-multimodal-llms/module-22-vision-language-models/section-22.3.html',
    'part-5-multimodal-llms/module-22-vision-language-models/section-22.4.html',
    'part-5-multimodal-llms/module-22-vision-language-models/section-22.5.html',
]

KATEX_HEAD_BLOCK = '''<link href="../../vendor/katex/katex.min.css" rel="stylesheet"/>
<script defer="" src="../../vendor/katex/katex.min.js"></script>
<script defer="" onload="renderMathInElement(document.body, {
            delimiters: [
                {left: '$$', right: '$$', display: true},
                {left: '$', right: '$', display: false}
            ],
            throwOnError: false
        });" src="../../vendor/katex/contrib/auto-render.min.js"></script>'''


def convert_bibliography(text: str) -> str:
    """Convert <div class="bibliography"><ol><li>...</li></ol></div> to canonical."""
    def replace(m):
        items_html = m.group(1)
        # Extract each <li>...</li>
        items = re.findall(r'<li>([\s\S]*?)</li>', items_html)
        if not items:
            return m.group(0)
        cards = []
        for item in items:
            # Item content is like: Author (Year). <em>Title</em>. Venue. <a ...>arXiv:...</a>.
            # Reformat to: Author (Year). <a href="...">"Title."</a> Venue.
            # Try to extract <em>Title</em> and any <a href> separately
            cleaned = item.strip()
            # If there's <em>Title</em>, wrap title in quotes and link it if a URL follows
            # Pattern: ... <em>Title</em>. <a href="URL"...>arXiv:...</a>
            m_em_link = re.match(
                r'^(.*?)<em>([^<]+)</em>\.\s*(.*?)\s*<a href="([^"]+)"[^>]*>([^<]+)</a>\.?\s*$',
                cleaned,
                re.DOTALL,
            )
            if m_em_link:
                prefix = m_em_link.group(1).strip()
                title = m_em_link.group(2).strip()
                middle = m_em_link.group(3).strip()
                url = m_em_link.group(4)
                # Format: Prefix. <a href="URL" rel="noopener" target="_blank">"Title."</a> Middle.
                bib = f'{prefix} <a href="{url}" rel="noopener" target="_blank">"{title}."</a>'
                if middle:
                    bib += f' {middle.rstrip(".") + "."}'
                cards.append(f'<div class="bib-entry-card">\n<div class="bib-ref">{bib}</div>\n</div>')
            else:
                # Fallback: keep <em> → quoted form, leave as is
                fallback = re.sub(r'<em>([^<]+)</em>', r'"\1"', cleaned)
                cards.append(f'<div class="bib-entry-card">\n<div class="bib-ref">{fallback}</div>\n</div>')

        body = '\n'.join(cards)
        return (
            '<details class="bibliography-collapsible" open>\n'
            '<summary><strong>Further Reading</strong></summary>\n'
            '<section class="bibliography">\n'
            f'{body}\n'
            '</section>\n'
            '</details>'
        )

    new_text = re.sub(
        r'<div class="bibliography">\s*<ol>([\s\S]*?)</ol>\s*</div>',
        replace,
        text,
    )
    return new_text


def add_katex_head(text: str) -> str:
    """Insert KaTeX <link>+<script> block into <head> if not present."""
    if 'vendor/katex' in text:
        return text
    # Find pygments.css or book.css inside head, insert KaTeX block after
    m = re.search(
        r'(<link href="\.\./\.\./styles/pygments\.css" rel="stylesheet"/>|<link href="\.\./\.\./styles/book\.css" rel="stylesheet"/>)',
        text,
    )
    if not m:
        # Try without pygments — just match book.css
        m = re.search(r'<link href="\.\./\.\./styles/book\.css" rel="stylesheet"/>', text)
        if not m:
            return text
    insert_pos = m.end()
    return text[:insert_pos] + '\n' + KATEX_HEAD_BLOCK + text[insert_pos:]


def convert_clip_infonce_math(text: str) -> str:
    """Convert the specific InfoNCE loss in section 22.2 from ASCII to KaTeX."""
    old = (
        '<p><code>L = -1/(2N) * [ Sum_i log( exp(s_ii / T) / Sum_j exp(s_ij / T) ) '
        '+ Sum_i log( exp(s_ii / T) / Sum_j exp(s_ji / T) ) ]</code></p>'
    )
    new = (
        '<p>$$L = -\\frac{1}{2N} \\left[ \\sum_i \\log \\frac{\\exp(s_{ii}/\\tau)}'
        '{\\sum_j \\exp(s_{ij}/\\tau)} + \\sum_i \\log \\frac{\\exp(s_{ii}/\\tau)}'
        '{\\sum_j \\exp(s_{ji}/\\tau)} \\right]$$</p>'
    )
    return text.replace(old, new)


def main():
    n_bib = 0
    n_katex = 0
    n_math = 0
    flag_files = []
    for rel in LEGACY_BIB_FILES:
        p = ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding='utf-8')
        orig = text

        # Step 1: bibliography
        text = convert_bibliography(text)
        if text != orig:
            n_bib += 1

        # Step 2: KaTeX includes
        after_bib = text
        text = add_katex_head(text)
        if text != after_bib:
            n_katex += 1

        # Step 3: specific known math conversions
        after_katex = text
        text = convert_clip_infonce_math(text)
        if text != after_katex:
            n_math += 1

        # Step 4: flag any remaining ASCII-math-in-<code> in <p> for review
        for m in re.finditer(r'<p><code>([^<]{20,300})</code></p>', text):
            payload = m.group(1)
            if 'Sum_' in payload or '/ T' in payload or 'exp(' in payload:
                flag_files.append((rel, payload[:120]))

        if text != orig:
            p.write_text(text, encoding='utf-8')

    print(f'Bibliography converted in: {n_bib} files')
    print(f'KaTeX includes added to:    {n_katex} files')
    print(f'Specific math conversions:  {n_math} files')
    if flag_files:
        print('\nFlagged ASCII-math-in-<code> for manual review:')
        for rel, snippet in flag_files:
            print(f'  {rel}: {snippet}')


if __name__ == '__main__':
    main()
