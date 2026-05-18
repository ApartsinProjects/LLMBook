"""Wave 9 step E bare-refs fixup: catch remaining bare hrefs after voice/realtime merge.

The first pass only caught module-prefixed cross-refs. This pass catches:
  - Bare `href="section-37.5.html"` inside Ch 40 (cross-module)
  - Bare `href="section-39.X.html"` inside Ch 40 (cross-module)
  - Bare `href="section-38.X.html"` inside Ch 41 (cross-module)
  - Bare `href="section-37.5.html"` inside Ch 37 sections (cross-module to Ch 40)
  - Index file refs to module-38/module-39 (these chapters were deleted/moved)
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
PART = 'part-8-conversational-ai-with-llms'
CH37_DIR = ROOT / PART / 'module-37-conversational-ai'
CH40_DIR = ROOT / PART / 'module-40-voice-realtime-multimodal'
CH41_DIR = ROOT / PART / 'module-41-conv-ai-tools'

# Section move map: (old_ch, old_y) -> (new_module, new_ch, new_y)
SECTION_MAP = {
    (37, 5): ('module-40-voice-realtime-multimodal', 40, 1),
    (39, 1): ('module-40-voice-realtime-multimodal', 40, 2),
    (39, 2): ('module-40-voice-realtime-multimodal', 40, 3),
    (39, 3): ('module-40-voice-realtime-multimodal', 40, 4),
    (39, 4): ('module-40-voice-realtime-multimodal', 40, 5),
    (38, 1): ('module-41-conv-ai-tools', 41, 1),
    (38, 2): ('module-41-conv-ai-tools', 41, 2),
    (38, 3): ('module-41-conv-ai-tools', 41, 3),
    (38, 4): ('module-41-conv-ai-tools', 41, 4),
    (38, 5): ('module-41-conv-ai-tools', 41, 5),
}

# Module renames (for index.html refs)
MODULE_REWRITES = [
    ('module-38-tools-of-the-trade', 'module-41-conv-ai-tools'),
    ('module-39-streaming-realtime-multimodal', 'module-40-voice-realtime-multimodal'),
]

SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}


def rewrite_bare_refs(file_path, current_module):
    """Rewrite href="section-X.Y.html" patterns based on SECTION_MAP."""
    text = file_path.read_text(encoding='utf-8')
    orig = text

    def replace(m):
        prefix = m.group(1)
        old_ch = int(m.group(2))
        old_y = int(m.group(3))
        anchor = m.group(4) or ''
        key = (old_ch, old_y)
        if key not in SECTION_MAP:
            return m.group(0)
        new_module, new_ch, new_y = SECTION_MAP[key]
        if new_module == current_module:
            return f'{prefix}section-{new_ch}.{new_y}.html{anchor}'
        else:
            return f'{prefix}../{new_module}/section-{new_ch}.{new_y}.html{anchor}'

    text = re.sub(
        r'(href=")section-(3[789])\.(\d+)\.html(#[^"]*)?',
        replace,
        text
    )
    if text != orig:
        file_path.write_text(text, encoding='utf-8')
        return True
    return False


def rewrite_module_paths(file_path):
    """Rewrite refs to module-38-* and module-39-* in index/toc files."""
    text = file_path.read_text(encoding='utf-8')
    orig = text
    for old_mod, new_mod in MODULE_REWRITES:
        text = text.replace(old_mod, new_mod)
    if text != orig:
        file_path.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    # 1. Fix bare refs in Ch 37 sections (refs to 37.5 should go to 40.1)
    n = 0
    for f in sorted(CH37_DIR.glob('section-*.html')):
        if rewrite_bare_refs(f, 'module-37-conversational-ai'):
            n += 1
    print(f'Ch 37: {n} sections updated')

    # 2. Fix bare refs in Ch 40 sections
    n = 0
    for f in sorted(CH40_DIR.glob('section-*.html')):
        if rewrite_bare_refs(f, 'module-40-voice-realtime-multimodal'):
            n += 1
    # Also fix bare 37.1, 37.2 etc in Ch 40 (refs back to Ch 37) — those are in same Part 8 just different module
    for f in sorted(CH40_DIR.glob('section-*.html')):
        text = f.read_text(encoding='utf-8')
        orig = text
        # Rewrite bare href="section-37.X.html" to ../module-37-conversational-ai/section-37.X.html
        text = re.sub(
            r'(href=")section-37\.([1-4])\.html',
            r'\1../module-37-conversational-ai/section-37.\2.html',
            text
        )
        if text != orig:
            f.write_text(text, encoding='utf-8')
    print(f'Ch 40: {n} sections updated (plus cross-module fixes)')

    # 3. Fix bare refs in Ch 41 sections
    n = 0
    for f in sorted(CH41_DIR.glob('section-*.html')):
        if rewrite_bare_refs(f, 'module-41-conv-ai-tools'):
            n += 1
    print(f'Ch 41: {n} sections updated')

    # 4. Rewrite module paths in toc.html and any index files referencing deleted modules
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        if rewrite_module_paths(p):
            n += 1
    print(f'Module-path refs rewritten in {n} files')


if __name__ == '__main__':
    main()
