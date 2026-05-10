"""Random-sample EPUB chapters and check for common rendering issues."""
import argparse, random, zipfile, re
from pathlib import Path

EPUB_DEFAULT = Path('KDP/output/building-conversational-ai-llms-agents.epub')
KEPT_AGENTS = {'deploy', 'guard', 'eval', 'compass', 'sage', 'frontier', 'agent-x', 'pip'}


def _audit_chapter(text: str, name: str, all_ids_by_chapter: dict) -> list[str]:
    issues = []
    # 1. Raw $$...$$ math leakage (KaTeX should have rendered)
    if re.search(r'(?<!\\)\$\$[^$]', text):
        issues.append(f'raw $$ math leakage')
    if re.search(r'(?<!\\)\$[A-Za-z][A-Za-z0-9_]+\$', text):
        n = len(re.findall(r'(?<!\\)\$[A-Za-z][A-Za-z0-9_]+\$', text))
        issues.append(f'raw inline math: {n}')
    # 2. Pygments spans without highlighting class on enclosing <code>
    has_token_spans = bool(re.search(r'<span class="(c1|kn|nn|nb)"', text))
    has_pygments_class = 'pygments-highlighted' in text
    if has_token_spans and not has_pygments_class:
        issues.append('Pygments spans without .pygments-highlighted class')
    # 3. Broken anchor refs
    chapter_ids = set(re.findall(r'\bid="([^"]+)"', text))
    for href in re.findall(r'href="#([^"]+)"', text):
        if href not in chapter_ids:
            issues.append(f'orphan anchor: #{href}')
            break
    # 4. Broken cross-doc anchor refs
    for href, frag in re.findall(r'href="(ch_\d+_[^"]*?)#([^"]+)"', text):
        if href in all_ids_by_chapter:
            if frag not in all_ids_by_chapter[href]:
                issues.append(f'orphan x-doc anchor: {href}#{frag}')
                break
    # 5. Empty src or missing img
    for m in re.finditer(r'<img[^>]*>', text):
        if 'src=""' in m.group(0) or 'src=' not in m.group(0):
            issues.append('img with empty/missing src')
            break
    # 6. Wisdom-council orphan refs to dropped agents
    for m in re.finditer(r'wisdom-council\.xhtml#([a-z\-]+)', text):
        if m.group(1) not in KEPT_AGENTS:
            issues.append(f'wisdom-council ref to dropped: #{m.group(1)}')
            break
    # 7. Double-escaped entities
    if re.search(r'&amp;(amp|lt|gt|quot|apos)(?![a-zA-Z;])', text):
        issues.append('double-escaped entities')
    # 8. Empty code block
    for m in re.finditer(r'<pre>\s*<code[^>]*>(.*?)</code>\s*</pre>', text, re.DOTALL):
        body = m.group(1)
        if body and len(body) > 20 and body.strip() == '':
            issues.append('empty code block')
            break
    # 9. Visible "redirected" / "moved" stub markers
    body_text = re.sub(r'<[^>]+>', '', text).lower()
    if any(s in body_text for s in ('will be redirected', 'page reorganized', 'has been moved')):
        if len(body_text) < 1500:
            issues.append('redirect-stub leaked into EPUB')
    # 10. Suspect raw tex commands not rendered
    if re.search(r'\\(begin|end)\{(equation|align|matrix|cases)\}', text):
        issues.append('raw \\begin{...} TeX leakage')
    # 11. <table> with > 6 cols not wrapped
    for m in re.finditer(r'<table[^>]*>', text):
        # Find first row's td/th count
        m2 = re.search(r'<tr[^>]*>(.*?)</tr>', text[m.end():m.end()+5000], re.DOTALL)
        if m2:
            ncols = len(re.findall(r'<(td|th)\b', m2.group(1)))
            if ncols >= 6 and 'table-wide-wrap' not in text[max(0, m.start()-80):m.start()]:
                issues.append(f'wide table ({ncols} cols) not wrapped')
                break
    # 12. Visible double spaces in body (tone of finishing)
    n_doubled = len(re.findall(r'  +', body_text))
    if n_doubled > 50:
        issues.append(f'doubled spaces in body: {n_doubled}')
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=30, help='Number of random chapters to sample')
    ap.add_argument('--seed', type=int, default=42, help='Random seed')
    ap.add_argument('--epub', type=Path, default=EPUB_DEFAULT, help='EPUB path')
    args = ap.parse_args()

    random.seed(args.seed)
    with zipfile.ZipFile(args.epub) as z:
        chapters = sorted(n for n in z.namelist()
                          if n.startswith('EPUB/chapters/') and n.endswith('.xhtml'))
        sample = random.sample(chapters, min(args.n, len(chapters)))

        # Pre-build the all-ids map for cross-doc anchor resolution (only sampled chapters)
        all_ids_by_chapter = {}
        for ch in sample:
            txt = z.read(ch).decode('utf-8', errors='replace')
            chapter_filename = ch.split('/')[-1]
            all_ids_by_chapter[chapter_filename] = set(re.findall(r'\bid="([^"]+)"', txt))

        issues_per_chapter = {}
        for ch in sample:
            text = z.read(ch).decode('utf-8', errors='replace')
            issues = _audit_chapter(text, ch, all_ids_by_chapter)
            if issues:
                issues_per_chapter[ch] = issues

    print(f'Sampled {len(sample)} chapters from {args.epub.name}')
    print(f'Chapters with issues: {len(issues_per_chapter)} / {len(sample)}')
    print()
    for ch, iss in issues_per_chapter.items():
        short = ch.split('/')[-1].replace('.xhtml', '')
        print(f'  {short}')
        for i in iss[:5]:
            print(f'    - {i}')
        if len(iss) > 5:
            print(f'    ... and {len(iss)-5} more')


if __name__ == '__main__':
    main()
