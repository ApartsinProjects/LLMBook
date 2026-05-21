"""Wave 29: convert raw <h2>Self-Check / Whats-Next / Bibliography</h2> sections
to canonical callouts + Further Reading bib-entry-card form.

13 section files (mostly module-24-vla-models) use raw <h2>...</h2> headings
followed by <ol>/<p> instead of the canonical:

  Self-Check:  <div class="callout self-check"><div class="callout-title">Self-Check</div><ol>...</ol></div>
  What's Next: <div class="callout whats-next"><div class="callout-title">What's Next</div><p>...</p></div>
  Bibliography: <details class="bibliography-collapsible" open>
                <summary><strong>Further Reading</strong></summary>
                <section class="bibliography">
                <div class="bib-entry-card"><div class="bib-ref">Author. "Title." Venue.</div></div>
                ...
                </section></details>
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs', 'agents'}


def convert_self_check(text: str) -> tuple[str, int]:
    """<h2 id="self-check">Self-Check</h2><ol>...</ol> →
       <div class="callout self-check"><div class="callout-title">Self-Check</div><ol>...</ol></div>
    """
    n = [0]

    def repl(m):
        n[0] += 1
        ol = m.group(1)
        return (
            '<div class="callout self-check">\n'
            '<div class="callout-title">Self-Check</div>\n'
            f'<ol>{ol}</ol>\n'
            '</div>'
        )

    text = re.sub(
        r'<h2 id="self-check">Self.Check</h2>\s*<ol>([\s\S]*?)</ol>',
        repl,
        text,
    )
    return text, n[0]


def convert_whats_next(text: str) -> tuple[str, int]:
    """<h2 id="whats-next">What's Next</h2><p>...</p> →
       <div class="callout whats-next">...</div>
    """
    n = [0]

    def repl(m):
        n[0] += 1
        body = m.group(1)
        # body may contain multiple <p> tags
        return (
            '<div class="callout whats-next">\n'
            '<div class="callout-title">What\'s Next</div>\n'
            f'{body}\n'
            '</div>'
        )

    text = re.sub(
        r'<h2 id="whats-next">What\'s Next</h2>\s*((?:<p>[\s\S]*?</p>\s*)+)',
        repl,
        text,
    )
    return text, n[0]


def convert_bibliography_h2(text: str) -> tuple[str, int]:
    """<h2 id="bibliography">Bibliography</h2><ol>...</ol> → canonical
       <details class="bibliography-collapsible"><summary>Further Reading</summary>
       <section class="bibliography"><div class="bib-entry-card"><div class="bib-ref">...</div></div></section></details>
    """
    n = [0]

    def repl(m):
        n[0] += 1
        items_html = m.group(1)
        items = re.findall(r'<li>([\s\S]*?)</li>', items_html)
        cards = []
        for item in items:
            cleaned = item.strip()
            # Convert <em>Title</em> to "Title" with optional link
            m_em_link = re.match(
                r'^(.*?)<em>([^<]+)</em>\.\s*(.*?)\s*<a href="([^"]+)"[^>]*>([^<]+)</a>\.?\s*$',
                cleaned, re.DOTALL,
            )
            if m_em_link:
                prefix = m_em_link.group(1).strip()
                title = m_em_link.group(2).strip()
                middle = m_em_link.group(3).strip()
                url = m_em_link.group(4)
                bib = f'{prefix} <a href="{url}" rel="noopener" target="_blank">"{title}."</a>'
                if middle:
                    bib += f' {middle.rstrip(".") + "."}'
                cards.append(f'<div class="bib-entry-card">\n<div class="bib-ref">{bib}</div>\n</div>')
            else:
                # Fallback: replace <em>...</em> with quoted form
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

    text = re.sub(
        r'<h2 id="bibliography">Bibliography</h2>\s*<ol>([\s\S]*?)</ol>',
        repl,
        text,
    )
    return text, n[0]


def main():
    total_sc = total_wn = total_bib = 0
    files_changed = 0
    for p in sorted(ROOT.rglob('section-*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        text, sc = convert_self_check(text)
        text, wn = convert_whats_next(text)
        text, bib = convert_bibliography_h2(text)
        total_sc += sc
        total_wn += wn
        total_bib += bib
        if text != orig:
            p.write_text(text, encoding='utf-8')
            files_changed += 1
    print(f'Self-Check h2 → callout: {total_sc}')
    print(f"What's Next h2 → callout: {total_wn}")
    print(f'Bibliography h2 → Further Reading: {total_bib}')
    print(f'Files changed: {files_changed}')


if __name__ == '__main__':
    main()
