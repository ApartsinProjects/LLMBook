"""Wave 17g: rebuild chapter-nav prev/next in every module-N/index.html based on
numerical adjacency within the part (and across-part boundary at part edges).

The cycle-2 audit caught many chapters with stale chapter-nav pointers (e.g.
Ch 58 prev → Part 16 Ch 83, next → Part 16 Ch 85; Ch 42 next → self;
Ch 52/54/55 next → self; Ch 56/59/60/61 missing prev/next entirely).

For each chapter (module-NN-slug), this wave determines the canonical
prev / next by walking the global chapter sequence (across all parts in
order, then across all modules numerically within each part), and rewrites
the <nav class="chapter-nav"> block.
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}

PARTS_ORDER = [
    ('part-1-llm-building-blocks', 'Part I', 'LLM Building Blocks'),
    ('part-2-understanding-llms', 'Part II', 'Understanding LLMs'),
    ('part-3-working-with-llms', 'Part III', 'Working with LLMs'),
    ('part-4-training-adaptation', 'Part IV', 'LLM Training and Adaptation'),
    ('part-5-multimodal-llms', 'Part V', 'Multimodal LLMs'),
    ('part-6-agentic-ai', 'Part VI', 'Agentic AI'),
    ('part-7-retrieval-information-extraction-with-llms', 'Part VII', 'Retrieval &amp; Information Extraction with LLMs'),
    ('part-8-conversational-ai-with-llms', 'Part VIII', 'Conversational AI with LLMs'),
    ('part-9-llm-evaluation-observability', 'Part IX', 'LLM Evaluation &amp; Observability'),
    ('part-10-llm-security-runtime-safety', 'Part X', 'LLM Security &amp; Runtime Safety'),
    ('part-11-llm-ethics-trust-governance', 'Part XI', 'LLM Ethics, Trust &amp; Governance'),
    ('part-12-llm-systems-at-scale', 'Part XII', 'LLM Systems at Scale'),
    ('part-13-llmops-lifecycle', 'Part XIII', 'LLMOps Lifecycle'),
    ('part-14-designing-llm-agent-products', 'Part XIV', 'Designing LLM/Agent Products'),
    ('part-15-applications-of-llms-across-industries', 'Part XV', 'Applications of LLMs Across Industries'),
    ('part-16-llm-agentic-ai-research-frontiers', 'Part XVI', 'LLM &amp; Agentic AI Research Frontiers'),
]


def collect_chapters():
    """Build an ordered list of (part_slug, part_roman, part_name, module_slug, ch_num, title)."""
    chapters = []
    for part_slug, roman, name in PARTS_ORDER:
        part_dir = ROOT / part_slug
        if not part_dir.exists():
            continue
        modules = sorted(
            [d for d in part_dir.iterdir() if d.is_dir() and re.match(r'module-(\d+)-', d.name)],
            key=lambda d: int(re.match(r'module-(\d+)-', d.name).group(1))
        )
        for mod in modules:
            ch_num = int(re.match(r'module-(\d+)-', mod.name).group(1))
            idx = mod / 'index.html'
            title = mod.name
            if idx.exists():
                text = idx.read_text(encoding='utf-8')
                h1 = re.search(r'<h1>([^<]+)</h1>', text)
                if h1:
                    title = h1.group(1).strip()
            chapters.append({
                'part_slug': part_slug,
                'part_roman': roman,
                'part_name': name,
                'module_slug': mod.name,
                'ch_num': ch_num,
                'title': title,
            })
    return chapters


def build_nav(prev_info, up_info, next_info):
    parts = ['<nav class="chapter-nav">']
    if prev_info:
        href = prev_info['href']
        parts.append(
            f'<a class="prev" href="{href}">'
            f'<span class="nav-label">Previous Chapter</span>'
            f'<span class="nav-num">Chapter {prev_info["ch_num"]}</span>'
            f'<span class="nav-title">{prev_info["title"]}</span></a>'
        )
    parts.append(
        f'<a class="up" href="../index.html">'
        f'<span class="nav-label">In Part</span>'
        f'<span class="nav-num">{up_info["roman"]}</span>'
        f'<span class="nav-title">{up_info["name"]}</span></a>'
    )
    if next_info:
        href = next_info['href']
        parts.append(
            f'<a class="next" href="{href}">'
            f'<span class="nav-label">Next Chapter</span>'
            f'<span class="nav-num">Chapter {next_info["ch_num"]}</span>'
            f'<span class="nav-title">{next_info["title"]}</span></a>'
        )
    parts.append('</nav>')
    return '\n'.join(parts)


def main():
    chapters = collect_chapters()
    print(f'Collected {len(chapters)} chapters')

    n_updated = 0
    for i, ch in enumerate(chapters):
        idx_path = ROOT / ch['part_slug'] / ch['module_slug'] / 'index.html'
        if not idx_path.exists():
            continue
        text = idx_path.read_text(encoding='utf-8')

        # Determine prev
        prev_info = None
        if i > 0:
            prev_ch = chapters[i - 1]
            if prev_ch['part_slug'] == ch['part_slug']:
                href = f'../{prev_ch["module_slug"]}/index.html'
            else:
                href = f'../../{prev_ch["part_slug"]}/{prev_ch["module_slug"]}/index.html'
            prev_info = {'href': href, 'ch_num': prev_ch['ch_num'], 'title': prev_ch['title']}

        # Determine next
        next_info = None
        if i < len(chapters) - 1:
            next_ch = chapters[i + 1]
            if next_ch['part_slug'] == ch['part_slug']:
                href = f'../{next_ch["module_slug"]}/index.html'
            else:
                href = f'../../{next_ch["part_slug"]}/{next_ch["module_slug"]}/index.html'
            next_info = {'href': href, 'ch_num': next_ch['ch_num'], 'title': next_ch['title']}

        up_info = {'roman': ch['part_roman'], 'name': ch['part_name']}
        new_nav = build_nav(prev_info, up_info, next_info)

        # Replace existing chapter-nav block
        new_text = re.sub(
            r'<nav class="chapter-nav">[\s\S]*?</nav>',
            new_nav,
            text,
            count=1
        )
        if new_text == text:
            # Maybe no existing nav — insert before </main>
            new_text = text.replace(
                '</main>',
                f'{new_nav}\n</main>',
                1
            )

        if new_text != text:
            idx_path.write_text(new_text, encoding='utf-8')
            n_updated += 1

    print(f'Updated chapter-nav in {n_updated} chapters')


if __name__ == '__main__':
    main()
