"""Wave 17M: residual fixes for parts 9-12 from cycle-3 audit agent 3.

1. Ch 47 index <title> says "Chapter 47: Safety, Ethics & Regulation" but
   H1 says "Adversarial Security and Red Teaming" — sync to H1
2. Ch 48 index all-front-matter says "Chapter 40" (off by 8)
3. Ch 54 index says "Chapter 46: Watermarking, Provenance, and Deepfake
   Defense" — already renamed by Wave 15, but title/meta drifted
4. Section breadcrumbs in 43, 52, 54, 55, 56, 59, 61 use stale chapter
   names/numbers; sync to canonical (chapter title from module index)
5. Sec 49.3 / 49.4 <title> say "Section 49.6" / "Section 49.7"
6. Ch 42 What's Next links to "Chapter 55: LLM Evaluation & Quality Metrics"
   (self-link with wrong number)
7. Part 9 Ch 42 card in part-index still has dup-42.9 + missing 42.10-12
8. Ch 44 chapter index breadcrumb says "Part VIII"
9. Sec 57.4 has Chapter 44 breadcrumb/pagefind/captions (off by 13)
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]


def sync_chapter_index_titles(part_slug):
    """For each module index in part_slug, ensure <title>, <meta>, breadcrumb,
    and pagefind chapter meta all use the canonical chapter number + title from H1."""
    print(f'=== Sync chapter index titles in {part_slug} ===')
    part_dir = ROOT / part_slug
    n = 0
    for mod_dir in sorted(part_dir.iterdir()):
        if not mod_dir.is_dir():
            continue
        m = re.match(r'module-(\d+)-', mod_dir.name)
        if not m:
            continue
        ch_num = int(m.group(1))
        idx = mod_dir / 'index.html'
        if not idx.exists():
            continue
        text = idx.read_text(encoding='utf-8')
        h1 = re.search(r'<h1>([^<]+)</h1>', text)
        if not h1:
            continue
        canonical_title = h1.group(1).strip()

        orig = text
        # Use re.escape to avoid issues with & or other regex chars in the title
        # but the replacement uses literal strings, not backreferences with the title
        text = re.sub(
            r'<title>Chapter \d+:[^|<]*\|',
            lambda m: f'<title>Chapter {ch_num}: {canonical_title} |',
            text
        )
        text = re.sub(
            r'(<meta content=")Chapter \d+:[^.]*\.',
            lambda m: f'{m.group(1)}Chapter {ch_num}: {canonical_title}.',
            text
        )
        text = re.sub(
            r'(data-pagefind-meta="chapter:Chapter )\d+:[^"]*(")',
            lambda m: f'{m.group(1)}{ch_num}: {canonical_title}{m.group(2)}',
            text
        )
        text = re.sub(
            r'(<span class="bc-current">)Chapter \d+(:[^<]*)?(</span>)',
            lambda m: f'{m.group(1)}Chapter {ch_num}{m.group(3)}',
            text
        )

        if text != orig:
            idx.write_text(text, encoding='utf-8')
            n += 1
    print(f'  Updated {n} chapter indices')


def sync_section_breadcrumbs(part_slug):
    """For each section in part_slug, ensure breadcrumb to chapter, pagefind chapter
    meta, and chapter-nav up label use the canonical chapter number/title."""
    print(f'=== Sync section breadcrumbs in {part_slug} ===')
    part_dir = ROOT / part_slug
    n = 0
    for mod_dir in sorted(part_dir.iterdir()):
        if not mod_dir.is_dir():
            continue
        m = re.match(r'module-(\d+)-', mod_dir.name)
        if not m:
            continue
        ch_num = int(m.group(1))
        idx = mod_dir / 'index.html'
        if not idx.exists():
            continue
        idx_text = idx.read_text(encoding='utf-8')
        h1m = re.search(r'<h1>([^<]+)</h1>', idx_text)
        if not h1m:
            continue
        canonical_title = h1m.group(1).strip()

        for sf in sorted(mod_dir.glob('section-*.html')):
            text = sf.read_text(encoding='utf-8')
            orig = text
            # Use lambdas to avoid issues with & in title being treated as regex backreference
            text = re.sub(
                r'<a href="index\.html">Chapter \d+(:[^<]*)?</a>',
                lambda m: f'<a href="index.html">Chapter {ch_num}: {canonical_title}</a>',
                text
            )
            text = re.sub(
                r'(data-pagefind-meta="chapter:Chapter )\d+(?::[^"]*)?(")',
                lambda m: f'{m.group(1)}{ch_num}: {canonical_title}{m.group(2)}',
                text
            )
            text = re.sub(
                r'(<a class="up"[^>]*>[\s\S]*?<span class="nav-num">)Chapter \d+(</span><span class="nav-title">)[^<]*(</span>)',
                lambda m: f'{m.group(1)}Chapter {ch_num}{m.group(2)}{canonical_title}{m.group(3)}',
                text
            )

            if text != orig:
                sf.write_text(text, encoding='utf-8')
                n += 1
    print(f'  Updated {n} section files in {part_slug}')


def fix_sec_49_3_4_title():
    """Sec 49.3 and 49.4 have <title>Section 49.6 / 49.7."""
    print('=== Fix sec 49.3 / 49.4 self-titling ===')
    for num in (3, 4):
        p = ROOT / 'part-10-llm-security-runtime-safety' / 'module-49-agent-safety-autonomy' / f'section-49.{num}.html'
        if not p.exists():
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        text = re.sub(
            r'<title>Section 49\.[67]:',
            f'<title>Section 49.{num}:',
            text
        )
        text = re.sub(
            r'(<meta content=")Section 49\.[67]:',
            rf'\1Section 49.{num}:',
            text
        )
        text = re.sub(
            r'<div class="page-current">Section 49\.[67]</div>',
            f'<div class="page-current">Section 49.{num}</div>',
            text
        )
        text = re.sub(
            r'<span class="bc-current">Section 49\.[67]</span>',
            f'<span class="bc-current">Section 49.{num}</span>',
            text
        )
        if text != orig:
            p.write_text(text, encoding='utf-8')
            print(f'  Fixed section-49.{num}.html')


def fix_part9_ch42_card():
    """Part 9 Ch 42 card in part-index has dup-42.9 + missing 42.10-12.
    Rebuild from module-42 index (Wave 17e should have already fixed module-42's
    sections-list but the part-9 card has its own static section list that
    Wave 12's rebuild generated from the THEN-stale module-42 index)."""
    print('=== Fix Part 9 Ch 42 card ===')
    # Just re-run Wave 12 rebuild for Part 9 — it'll pick up the now-correct
    # module-42 index
    part9_idx = ROOT / 'part-9-llm-evaluation-observability' / 'index.html'
    if not part9_idx.exists():
        return

    # Get all module dirs in numerical order
    part_dir = part9_idx.parent
    modules = sorted(
        [d for d in part_dir.iterdir() if d.is_dir() and re.match(r'module-(\d+)-', d.name)],
        key=lambda d: int(re.match(r'module-(\d+)-', d.name).group(1))
    )

    cards = []
    for mod in modules:
        ch_num = int(re.match(r'module-(\d+)-', mod.name).group(1))
        mod_idx = mod / 'index.html'
        if not mod_idx.exists():
            continue
        mod_text = mod_idx.read_text(encoding='utf-8')
        h1m = re.search(r'<h1>([^<]+)</h1>', mod_text)
        title = h1m.group(1).strip() if h1m else f'Chapter {ch_num}'

        # Get sections from filesystem
        sections = sorted(mod.glob('section-*.html'),
                          key=lambda p: [int(x) for x in re.findall(r'\d+', p.name)])
        if not sections:
            continue

        card = f'<div class="chapter-card">\n'
        card += f'<div class="chapter-card-header"><span class="mod-num">Chapter {ch_num}</span> {title}</div>\n'
        card += '<div class="chapter-card-body">\n<ul class="section-list">\n'
        for sf in sections:
            sm = re.match(r'section-(\d+)\.(\d+)\.html', sf.name)
            if not sm:
                continue
            sec_num = f'{sm.group(1)}.{sm.group(2)}'
            sf_text = sf.read_text(encoding='utf-8')
            sh1 = re.search(r'<h1>([^<]+)</h1>', sf_text)
            sec_title = sh1.group(1).strip() if sh1 else f'Section {sec_num}'
            card += f'<li><a href="{mod.name}/{sf.name}"><span class="sec-num">{sec_num}</span> {sec_title}</a></li>\n'
        card += '</ul>\n</div>\n</div>'
        cards.append(card)

    if not cards:
        return

    text = part9_idx.read_text(encoding='utf-8')
    new_cards = '\n'.join(cards)
    # Replace existing chapter-card-list or chapter-cards
    if '<div class="chapter-card-list">' in text:
        text = re.sub(
            r'<div class="chapter-card-list">[\s\S]*?</div>\s*(?=</main>|<h2|<footer)',
            f'<div class="chapter-card-list">\n{new_cards}\n</div>\n',
            text
        )
    else:
        # Find first chapter-card and replace range up to </main>
        first = text.find('<div class="chapter-card">')
        if first >= 0:
            after_match = re.search(r'(</main>|<footer)', text[first:])
            if after_match:
                text = (
                    text[:first]
                    + f'<div class="chapter-card-list">\n{new_cards}\n</div>\n'
                    + text[first:][after_match.start():]
                )
    part9_idx.write_text(text, encoding='utf-8')
    print(f'  Rebuilt Part 9 part-index with {len(cards)} chapter cards')


def main():
    for part in ['part-9-llm-evaluation-observability',
                 'part-10-llm-security-runtime-safety',
                 'part-11-llm-ethics-trust-governance',
                 'part-12-llm-systems-at-scale']:
        sync_chapter_index_titles(part)
        sync_section_breadcrumbs(part)

    fix_sec_49_3_4_title()
    fix_part9_ch42_card()


if __name__ == '__main__':
    main()
