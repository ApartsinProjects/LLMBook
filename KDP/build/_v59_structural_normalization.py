"""v5.9: Structural normalization across the book.

Six related issues from the latest user audit:

A. section-10.3 figure numbering went 10.3.1 ... 10.3.4, then jumped to
   10.3.9 (the v5.8 figcaption fixer assigned next-K wrong because it
   misread an h3 like "10.3.4.2 Semantic Caching" as a Figure 10.3.4).
   Fix: walk section-10.3.html figures in order, RENUMBER sequentially
   from 1 (using only the actual figcaption/diagram-caption tags).

B. 8 last-of-chapter sections have a "next" link pointing to the wrong
   target (e.g., section-9.7's "next" goes to root index.html with text
   "Chapter 18", but the canonical part-spine order has Ch 10 next).
   Build the canonical chapter spine from the part directories, then
   for each LAST section in each chapter, rewrite the next link to
   point at the next chapter's index.html with its h1 as link text.

C. Part header inconsistencies (7 issues):
     - Parts 1-5 lack the " | Building Conversational AI..." title suffix
     - Parts 8 and 9 use "&" in title but "and" in h1
   Fix: enforce title format
     "Part R: Title | Building Conversational AI with LLMs and Agents"
   AND make the h1 match the title (canonical "and" prose).

D. Chapter label-vs-h1 mismatches (6 modules):
     - Ch 0  : label "Machine Learning & PyTorch Foundations" vs h1 "ML and PyTorch Foundations"
     - Ch 3  : label "Sequence Models and Attention" vs h1 "Sequence Models & the Attention Mechanism"
     - Ch 5  : label "Decoding and Text Generation" vs h1 "Decoding Strategies & Text Generation"
     - Ch 6  : label "Pretraining & Scaling Laws" vs h1 "Pre-training, Scaling Laws & Data Curation"
     - Ch 36 : label just "Chapter 36" (no title)
     - Ch 38 : label just "Chapter 38" (no title)
   Fix: rewrite each label to "Chapter NN: <h1 text>".

E. The "Part II Chapter 18 after Chapter 09" effect: comes from the
   wrong next-links above. Fixing C (chapter spine) resolves it.

F. Hero / header format consistency: parts 1-5 had a slightly different
   header layout (one-line title vs subtitle line). Audit shows they
   already use the same <h1>Part R: Title</h1> pattern; the differences
   are only in the lede paragraph. We do not auto-rewrite leading prose
   in this pass.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = {'agents', 'KDP', 'node_modules', 'scripts', '.git',
        'chapter_review', 'downloads', '_archive', '_lab_fragments',
        'templates'}

# ----- Canonical part spine -----------------------------------------

PART_ORDER = [
    'part-1-foundations',
    'part-2-understanding-llms',
    'part-3-working-with-llms',
    'part-4-training-adapting',
    'part-5-retrieval-conversation',
    'part-6-agentic-ai',
    'part-7-multimodal-applications',
    'part-8-evaluation-production',
    'part-9-safety-strategy',
    'part-10-frontiers',
    'part-11-idea-to-product',
]


def build_chapter_spine() -> list[tuple[str, str, int]]:
    """Return [(part_dir, module_dir, chapter_num)] in reading order."""
    spine = []
    for pdir in PART_ORDER:
        p = ROOT / pdir
        if not p.exists():
            continue
        mods = sorted(p.glob('module-*'),
                      key=lambda d: int(re.match(r'module-0*(\d+)-', d.name).group(1)))
        for m in mods:
            n = int(re.match(r'module-0*(\d+)-', m.name).group(1))
            spine.append((pdir, m.name, n))
    return spine


# ----- A. section-10.3 figure renumber ------------------------------

def fix_section_10_3_figures() -> int:
    p = ROOT / 'part-3-working-with-llms/module-10-llm-apis/section-10.3.html'
    text = p.read_text(encoding='utf-8')
    # Renumber every <strong>Figure 10.3.K</strong> in document order.
    # Walk all figcaption/diagram-caption with Figure 10.3.K label.
    pat = re.compile(r'<strong>Figure 10\.3\.(\d+)</strong>')
    counter = [1]

    def repl(m: re.Match) -> str:
        new_k = counter[0]
        counter[0] += 1
        return f'<strong>Figure 10.3.{new_k}</strong>'

    new_text, n = pat.subn(repl, text)
    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
    return n


# ----- B. Wrong next-links --------------------------------------------

def fix_wrong_next_links() -> int:
    spine = build_chapter_spine()
    fixed = 0

    for i, (pdir, mname, num) in enumerate(spine):
        if i + 1 >= len(spine):
            continue
        next_pdir, next_mname, next_num = spine[i + 1]

        # Find the LAST section in current module
        cur_mod = ROOT / pdir / mname
        sections = sorted(cur_mod.glob('section-*.html'))
        if not sections:
            continue
        last_sec = sections[-1]

        text = last_sec.read_text(encoding='utf-8')
        nav_m = re.search(r'(<nav class="chapter-nav">)(.*?)(</nav>)',
                          text, re.DOTALL)
        if not nav_m:
            continue

        nav = nav_m.group(2)
        # Read next chapter's h1 to use as link text
        next_idx_path = ROOT / next_pdir / next_mname / 'index.html'
        if not next_idx_path.exists():
            continue
        next_idx_text = next_idx_path.read_text(encoding='utf-8')
        next_h1_m = re.search(r'<h1[^>]*>([^<]+)</h1>', next_idx_text)
        next_h1 = next_h1_m.group(1).strip() if next_h1_m else f'Chapter {next_num}'
        # Strip "Chapter NN: " prefix if present, then add canonical prefix
        next_h1 = re.sub(r'^Chapter \d+:\s*', '', next_h1).strip()
        next_label = f'Chapter {next_num}: {next_h1}'

        # Compute relative href from cur_mod to next_idx_path
        from os.path import relpath
        rel = relpath(next_idx_path, last_sec.parent).replace('\\', '/')

        # Replace the existing <a class="next" ...>..</a>
        new_nav, sub_n = re.subn(
            r'<a class="next"\s+href="[^"]+"[^>]*>[^<]+</a>',
            f'<a class="next" href="{rel}">{next_label}</a>',
            nav, count=1,
        )
        if sub_n and new_nav != nav:
            new_text = text[:nav_m.start(2)] + new_nav + text[nav_m.end(2):]
            last_sec.write_text(new_text, encoding='utf-8')
            print(f'  fixed next-link in {last_sec.relative_to(ROOT)}: → {rel}')
            fixed += 1

    return fixed


# ----- C. Part header normalization -----------------------------------

PART_TITLES = {
    'part-1-foundations':            ('Part I',    'Foundations'),
    'part-2-understanding-llms':     ('Part II',   'Understanding LLMs'),
    'part-3-working-with-llms':      ('Part III',  'Working with LLMs'),
    'part-4-training-adapting':      ('Part IV',   'Training and Adapting'),
    'part-5-retrieval-conversation': ('Part V',    'Retrieval and Conversation'),
    'part-6-agentic-ai':             ('Part VI',   'Agentic AI'),
    'part-7-multimodal-applications': ('Part VII', 'AI Applications'),
    'part-8-evaluation-production':  ('Part VIII', 'Evaluation and Production'),
    'part-9-safety-strategy':        ('Part IX',   'Safety and Strategy'),
    'part-10-frontiers':             ('Part X',    'Frontiers'),
    'part-11-idea-to-product':       ('Part XI',   'From Idea to AI Product'),
}

BOOK_SUFFIX = ' | Building Conversational AI with LLMs and Agents'


def fix_part_headers() -> int:
    fixed = 0
    for pdir, (roman, title) in PART_TITLES.items():
        p = ROOT / pdir / 'index.html'
        if not p.exists():
            continue
        text = p.read_text(encoding='utf-8')
        canonical = f'{roman}: {title}'
        # Title:
        new_title = canonical + BOOK_SUFFIX
        new_text, n1 = re.subn(
            r'<title>[^<]*</title>',
            f'<title>{new_title}</title>', text, count=1,
        )
        # h1 — replace only if mismatch
        new_text, n2 = re.subn(
            r'<h1[^>]*>[^<]*</h1>',
            f'<h1 class="part-title">{canonical}</h1>',
            new_text, count=1,
        )
        if new_text != text:
            p.write_text(new_text, encoding='utf-8')
            fixed += 1
            print(f'  normalized {pdir}/index.html')
    return fixed


# ----- D. Chapter label normalization ---------------------------------

def fix_chapter_labels() -> int:
    """For each chapter, rewrite the <div class="chapter-label">...</div>
    to "Chapter NN: <h1 title>"."""
    spine = build_chapter_spine()
    fixed = 0
    for pdir, mname, num in spine:
        idx = ROOT / pdir / mname / 'index.html'
        if not idx.exists():
            continue
        text = idx.read_text(encoding='utf-8')
        h1_m = re.search(r'<h1[^>]*>([^<]+)</h1>', text)
        if not h1_m:
            continue
        h1 = re.sub(r'^Chapter \d+:?\s*', '', h1_m.group(1)).strip()
        canonical_label = f'Chapter {num:02d}: {h1}'
        # The chapter-label may contain a nested <a> linking to index.html
        # Pattern in index.html:
        #   <div class="chapter-label">Chapter NN: SOMETHING</div>
        new_text, n = re.subn(
            r'(<div class="chapter-label"[^>]*>)([^<]*)(</div>)',
            lambda m: m.group(1) + canonical_label + m.group(3),
            text, count=1,
        )
        if new_text != text:
            idx.write_text(new_text, encoding='utf-8')
            fixed += 1
            print(f'  normalized chapter-label in {idx.relative_to(ROOT)}: "{canonical_label}"')
    return fixed


# ----- Driver ---------------------------------------------------------

def main() -> int:
    print('A. section-10.3 figure renumber')
    n_a = fix_section_10_3_figures()
    print(f'   renumbered {n_a} figures\n')

    print('B. Wrong next-link fixes')
    n_b = fix_wrong_next_links()
    print(f'   fixed {n_b} next-links\n')

    print('C. Part header normalization')
    n_c = fix_part_headers()
    print(f'   normalized {n_c} part index pages\n')

    print('D. Chapter label normalization')
    n_d = fix_chapter_labels()
    print(f'   normalized {n_d} chapter labels\n')

    print(f'TOTAL EDITS: A={n_a} B={n_b} C={n_c} D={n_d}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
