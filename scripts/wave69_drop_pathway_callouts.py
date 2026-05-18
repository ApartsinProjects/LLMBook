"""Wave 69: Drop the "pathway" callout type from the style catalogue and the
text content.

Decisions:
- HTML: convert `<div class="callout pathway">` to `<div class="callout note">`.
  The prose content is informational and worth keeping; "note" is the
  closest canonical type for general informational content.
- Callout title: drop any "Learning Objectives:" or "Pathway:" prefix and
  replace with a "Note:" prefix to match the new class. Strip leading
  numbering hooks like "1. " when they were used purely to enumerate
  multiple pathway boxes on the same page (the new "Note:" title carries
  enough context).
- CSS: remove `.callout.pathway`-specific rules from book.css. The
  `.pathway-*` rules used by the Reading-Pathways front matter (FM.8b,
  appendix C) are a separate concept and STAY.
- Audit plugins: remove "pathway" from CANONICAL_TYPES, CANONICAL_PREFIXES,
  and pseudo-callout regex.
- Icon file `styles/icons/callout-pathway.svg` left in place (harmless,
  no rule references it after CSS prune); listed for optional later cleanup.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# 1. HTML: convert <div class="callout pathway"> → <div class="callout note">
#    and rewrite the callout-title.
PATHWAY_OPEN_RE = re.compile(
    r'<div\s+class="callout pathway"([^>]*)>',
    re.IGNORECASE,
)
# Title rewrite: <div class="callout-title">Learning Objectives: ...</div>
#                <div class="callout-title">Pathway: ...</div>
TITLE_REWRITE_RE = re.compile(
    r'(<div\s+class="callout-title"[^>]*>)\s*'
    r'(?:Learning Objectives?|Pathway|Objectives?|Learning Objective)\s*:\s*'
    r'(?:\d+\.\s*)?'
    r'([^<]+)'
    r'(</div>)',
    re.IGNORECASE,
)


def rewrite_html(text: str) -> tuple[str, int]:
    n = 0
    # Walk pathway opens, find matching close, rewrite class and title
    out = []
    pos = 0
    for m in PATHWAY_OPEN_RE.finditer(text):
        out.append(text[pos:m.start()])
        rest_attrs = m.group(1)
        # Find balanced </div>
        depth = 1
        scan_pos = m.end()
        max_scan = 8000
        while scan_pos < len(text) and depth > 0 and scan_pos - m.end() < max_scan:
            next_open = text.find('<div', scan_pos)
            next_close = text.find('</div>', scan_pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                scan_pos = next_open + 4
            else:
                depth -= 1
                scan_pos = next_close + 6
                if depth == 0:
                    break
        if depth != 0:
            # Unbalanced — leave as-is
            out.append(text[m.start():scan_pos])
            pos = scan_pos
            continue
        block_inner = text[m.end():scan_pos - len('</div>')]
        # Rewrite title
        new_inner = TITLE_REWRITE_RE.sub(
            lambda mm: f'{mm.group(1)}Note: {mm.group(2).strip()}{mm.group(3)}',
            block_inner,
            count=1,
        )
        out.append(f'<div class="callout note"{rest_attrs}>{new_inner}</div>')
        pos = scan_pos
        n += 1
    out.append(text[pos:])
    return ''.join(out), n


def main():
    n_html = 0
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        new, n = rewrite_html(text)
        if n > 0:
            p.write_text(new, encoding='utf-8')
            files_touched += 1
            n_html += n
    print(f'HTML: {n_html} <div class="callout pathway"> → <div class="callout note"> across {files_touched} files')

    # 2. CSS: remove pathway-callout-specific rules (keep Reading Pathway rules)
    css_path = ROOT / 'styles' / 'book.css'
    css = css_path.read_text(encoding='utf-8')
    orig_css = css
    # Drop these specific lines/rules:
    #   .callout.pathway .callout-title::before { background-image: ... }
    #   .callout.pathway { ... }
    #   .callout.pathway .callout-title { color: ... }
    #   .callout.pathway .callout-title::after { content: ... }
    css = re.sub(
        r'^\.callout\.pathway\s+\.callout-title::before\s*\{[^}]*\}\s*\n',
        '', css, flags=re.MULTILINE,
    )
    css = re.sub(
        r'^\.callout\.pathway\s*\{[^}]*\}\s*\n',
        '', css, flags=re.MULTILINE,
    )
    css = re.sub(
        r'^\.callout\.pathway\s+\.callout-title\s*\{[^}]*\}\s*\n',
        '', css, flags=re.MULTILINE,
    )
    css = re.sub(
        r'^\.callout\.pathway\s+\.callout-title::after\s*\{[^}]*\}\s*\n',
        '', css, flags=re.MULTILINE,
    )
    if css != orig_css:
        css_path.write_text(css, encoding='utf-8')
        print('CSS: removed .callout.pathway rules from book.css')
    else:
        print('CSS: no .callout.pathway rules matched (already removed?)')

    # 3. Audit plugin updates
    plugin_dir = ROOT / 'agents' / 'book-skills' / 'scripts' / 'audit' / 'checks'

    # 3a. p2_callout_canonical_structure.py: remove "pathway" from CANONICAL_TYPES
    p = plugin_dir / 'p2_callout_canonical_structure.py'
    text = p.read_text(encoding='utf-8')
    new = re.sub(r'\s*"pathway",', '', text, count=1)
    if new != text:
        p.write_text(new, encoding='utf-8')
        print('Plugin: removed "pathway" from p2_callout_canonical_structure CANONICAL_TYPES')

    # 3b. p2_callout_title_prefix.py: remove "pathway" entry
    p = plugin_dir / 'p2_callout_title_prefix.py'
    text = p.read_text(encoding='utf-8')
    new = re.sub(
        r'\s*"pathway":\s*\[[^\]]*\],\s*\n',
        '\n', text,
    )
    new = re.sub(
        r'\s*pathway\s+->\s*"Learning Objectives" or "Pathway"\s*\n',
        '\n', new,
    )
    if new != text:
        p.write_text(new, encoding='utf-8')
        print('Plugin: removed "pathway" from p2_callout_title_prefix mapping')

    # 3c. p2_pseudo_callout.py: remove "pathway" from regex alternatives
    p = plugin_dir / 'p2_pseudo_callout.py'
    text = p.read_text(encoding='utf-8')
    new = text.replace('|pathway', '').replace('pathway|', '')
    new = re.sub(r',\s*pathway,', ',', new)
    if new != text:
        p.write_text(new, encoding='utf-8')
        print('Plugin: removed "pathway" from p2_pseudo_callout regex/docstring')

    # 3d. p1_structural_violations.py: remove 'Pathway' title from CANONICAL_TITLES
    p = plugin_dir / 'p1_structural_violations.py'
    text = p.read_text(encoding='utf-8')
    new = re.sub(r"\s*'Pathway',", '', text)
    if new != text:
        p.write_text(new, encoding='utf-8')
        print('Plugin: removed "Pathway" from p1_structural_violations CANONICAL_TITLES')


if __name__ == '__main__':
    main()
