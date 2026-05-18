"""Wave 51: Reduce excess bold in big-picture paragraphs.

The industry-expansion agent produced big-picture paragraphs where the opening
sentence is wholly wrapped in <strong>...</strong>, making >40% of the paragraph
bold. Reserve <strong> for key terms only.

Strategy: if the big-picture paragraph starts with a leading <strong>SENTENCE.</strong>
that spans an entire sentence, unwrap it. Embedded <strong>term</strong> uses inside
the rest of the paragraph are preserved.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Match the big-picture callout's first <p>, capturing structure
BIGPIC_P_RE = re.compile(
    r'(<div\s+class="callout big-picture"[^>]*>\s*<div\s+class="callout-title">[^<]*</div>\s*<p>)'
    r'(<strong>[^<]+?[.!?]\s*</strong>)'
    r'(\s*[^<].*?</p>)',
    re.DOTALL | re.IGNORECASE,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        prefix = m.group(1)
        strong_block = m.group(2)
        suffix = m.group(3)
        # Strip <strong> tags from strong_block
        inner = re.sub(r'</?strong>', '', strong_block)
        return prefix + inner + suffix

    new_text = BIGPIC_P_RE.sub(repl, text)
    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
    return n


def main():
    n_total = 0
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n > 0:
            n_total += n
            files_touched += 1
    print(f'Big-picture lead-strong unwrapped: {n_total}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
