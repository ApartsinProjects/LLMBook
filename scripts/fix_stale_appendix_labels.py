"""Fix stale 'Appendix X' / 'Section X.Y' labels in body text that point at
consolidated section content but still display old appendix letters.

Examples we want to fix:
  <a href=".../section-21.2.html#...">Appendix J (Experiment Tracking)</a>
  <a href=".../section-12.2.html#...">Appendix K (Inference Serving)</a>
  <a href=".../section-6.2.html#...">Appendix G Section G.3</a>
  <a href=".../section-12.2.html#...">Appendix K</a>
  <a href=".../section-16.1.html#...">Section H.7</a>
  (Appendix K) inline-text reference
"""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]

SKIP = {"node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
        "source_fix_backups", "pagefind", "templates", ".claude",
        ".book-update", "vendor", "docs"}


def get_h1(p):
    if not p.exists(): return None
    text = p.read_text(encoding='utf-8')
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', text)
    return m.group(1).strip() if m else None


def fix_anchor_label(href, label, source_file):
    """Given an <a>'s href and current label, compute the new label.

    Rules:
      - If href points at an appendix INDEX (appendices/appendix-X-NAME/index.html),
        and the label uses an OLD letter (C-N, O, P, Q, R, S, T), use the NEW
        canonical "Appendix X (Title)" where X is the current appendix letter.
      - If href points at a SECTION file (part-X/module-Y/section-Z.html), the
        label should be "Section Z (Title)" where Title comes from the target's H1.
      - If we can't resolve the target, leave the label alone.
    """
    if href.startswith('http') or href.startswith('mailto:') or href.startswith('#'):
        return label
    # Strip anchor
    target_path = href.split('#', 1)[0]
    try:
        target = (source_file.parent / target_path).resolve()
    except Exception:
        return label
    if not target.exists():
        return label

    name = target.name

    # Appendix index page (e.g. appendix-c-course-syllabi/index.html)
    if name == 'index.html' and 'appendix-' in target.parent.name:
        m = re.match(r'appendix-([a-z])-', target.parent.name)
        if not m: return label
        letter = m.group(1).upper()
        title = get_h1(target) or label
        # Strip "Appendix X: " prefix from H1 if present
        title_clean = re.sub(rf'^Appendix\s+{letter}\s*:?\s*', '', title, flags=re.IGNORECASE)
        return f'Appendix {letter} ({title_clean})'

    # Section file
    sec_m = re.match(r'section-(\d+\.\d+)\.html', name)
    if sec_m:
        sec_num = sec_m.group(1)
        title = get_h1(target)
        if not title: return label
        # If existing label says "Appendix X (Topic)" we want "Section N (Topic)"
        # If existing label says "Appendix X Section X.Y", drop the appendix prefix
        # If existing label says "Section X.Y", strip and replace
        return f'Section {sec_num} ({title})'

    # Some other kind of HTML page (chapter index?)
    if name == 'index.html' and 'module-' in target.parent.name:
        m = re.match(r'module-(\d+)-', target.parent.name)
        if not m: return label
        ch_num = m.group(1)
        title = get_h1(target) or label
        title_clean = re.sub(r'^Chapter\s+\d+\s*:?\s*', '', title, flags=re.IGNORECASE)
        return f'Chapter {ch_num} ({title_clean})'

    return label


def fix_file(p):
    text = p.read_text(encoding='utf-8')
    orig = text

    def fix_anchor(m):
        href = m.group(1)
        label = m.group(2)
        # Only relabel if label uses an OLD appendix letter (C-N, O, P, Q, R, S, T)
        # OR if label is mismatched generically
        # Match labels starting with "Appendix [letter]"
        appendix_m = re.match(r'^(Appendix\s+([A-Z]))[\.\s]', label)
        section_m = re.match(r'^(Section\s+([A-Z])\.)', label)

        is_old_appendix_letter = appendix_m and appendix_m.group(2) in 'CDEFGHIJKLMNO'
        is_old_section_letter = section_m and section_m.group(2) in 'CDEFGHIJKLMNO'

        if not (is_old_appendix_letter or is_old_section_letter):
            return m.group(0)

        # If href targets the SAME letter appendix (e.g. appendix-c-... when label is "Appendix C"),
        # the label is fine — keep it.
        if appendix_m and 'appendices/appendix-' + appendix_m.group(2).lower() + '-' in href:
            return m.group(0)

        new_label = fix_anchor_label(href, label, p)
        if new_label == label:
            return m.group(0)
        return f'<a href="{href}">{new_label}</a>'

    # Match <a href="X">label</a> where label may contain whitespace, dots, parens
    text = re.sub(
        r'<a\s+href="([^"]+)"[^>]*>([^<]+)</a>',
        fix_anchor,
        text
    )

    if text != orig:
        p.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP: continue
        if fix_file(p):
            n += 1
    print(f'Fixed stale labels in {n} files')


if __name__ == '__main__':
    main()
