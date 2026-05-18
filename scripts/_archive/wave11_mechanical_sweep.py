"""Wave 11: mechanical bulk sweeps from content-audit reports.

Handles low-risk, deterministic fixes:
  1. Appendix title/letter mismatches (Wave 9F leftover)
  2. Substitution corruptions ("softmax library", "for softmax")
  3. Sections 42.10/42.11 self-titling as 42.9
  4. Stale part-name breadcrumbs (set to current part based on file location)
  5. Stale pagefind-meta `part:` attributes
  6. Move Ch 0 to top of Part 1 index (was last)
  7. Drop stray "Section D.7" artifact in Reading Pathways
  8. Fix module-10 next-link pointing to self
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}

PART_NAMES = {
    'part-1-llm-building-blocks': ('Part I', 'LLM Building Blocks'),
    'part-2-understanding-llms': ('Part II', 'Understanding LLMs'),
    'part-3-working-with-llms': ('Part III', 'Working with LLMs'),
    'part-4-training-adaptation': ('Part IV', 'LLM Training and Adaptation'),
    'part-5-multimodal-llms': ('Part V', 'Multimodal LLMs'),
    'part-6-agentic-ai': ('Part VI', 'Agentic AI'),
    'part-7-retrieval-information-extraction-with-llms': ('Part VII', 'Retrieval &amp; Information Extraction with LLMs'),
    'part-8-conversational-ai-with-llms': ('Part VIII', 'Conversational AI with LLMs'),
    'part-9-llm-evaluation-observability': ('Part IX', 'LLM Evaluation &amp; Observability'),
    'part-10-llm-security-runtime-safety': ('Part X', 'LLM Security &amp; Runtime Safety'),
    'part-11-llm-ethics-trust-governance': ('Part XI', 'LLM Ethics, Trust &amp; Governance'),
    'part-12-llm-systems-at-scale': ('Part XII', 'LLM Systems at Scale'),
    'part-13-llmops-lifecycle': ('Part XIII', 'LLMOps Lifecycle'),
    'part-14-designing-llm-agent-products': ('Part XIV', 'Designing LLM/Agent Products'),
    'part-15-applications-of-llms-across-industries': ('Part XV', 'Applications of LLMs Across Industries'),
    'part-16-llm-agentic-ai-research-frontiers': ('Part XVI', 'LLM &amp; Agentic AI Research Frontiers'),
}


def fix_appendices():
    """Fix appendix B (Course Syllabi) and C (Reading Pathways) title/letter mismatches."""
    print('=== Fix 1: Appendix B/C self-references ===')

    APX_B = ROOT / 'appendices' / 'appendix-b-course-syllabi' / 'index.html'
    if APX_B.exists():
        t = APX_B.read_text(encoding='utf-8')
        o = t
        # File was originally course-syllabi (Apx C) but got partially renamed to A. We want B.
        t = t.replace('Appendix A: Course Syllabi', 'Appendix B: Course Syllabi')
        t = t.replace('chapter:Appendix A: Course Syllabi', 'chapter:Appendix B: Course Syllabi')
        t = t.replace('aria-label="Appendix A"', 'aria-label="Appendix B"')
        t = t.replace('bc-current">Appendix A<', 'bc-current">Appendix B<')
        t = t.replace('class="page-current">Appendix A<', 'class="page-current">Appendix B<')
        # Body ref: "Appendix B (ML Essentials)" should be "Chapter 0 (ML & PyTorch Foundations)"
        # since old Apx B (ML Essentials) was dropped in Wave 9F
        t = re.sub(
            r'<a href="[^"]*part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index\.html">Appendix B</a> \(ML Essentials\)',
            '<a href="../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html">Chapter 0</a> (ML &amp; PyTorch Foundations)',
            t
        )
        # Update next-nav: "Appendix B Reading Pathways" → "Appendix C Reading Pathways"
        t = re.sub(
            r'<span class="nav-num">Appendix B</span><span class="nav-title">Reading Pathways</span>',
            '<span class="nav-num">Appendix C</span><span class="nav-title">Reading Pathways</span>',
            t
        )
        if t != o:
            APX_B.write_text(t, encoding='utf-8')
            print(f'  Fixed {APX_B.relative_to(ROOT)}')

    APX_C = ROOT / 'appendices' / 'appendix-c-reading-pathways' / 'index.html'
    if APX_C.exists():
        t = APX_C.read_text(encoding='utf-8')
        o = t
        # File was originally reading-pathways (Apx D) but got partially renamed to B. We want C.
        t = t.replace('Appendix B: Reading Pathways', 'Appendix C: Reading Pathways')
        t = t.replace('chapter:Appendix B: Reading Pathways', 'chapter:Appendix C: Reading Pathways')
        t = t.replace('aria-label="Appendix B"', 'aria-label="Appendix C"')
        t = t.replace('bc-current">Appendix B<', 'bc-current">Appendix C<')
        # Body refs: "Appendix A (Course Syllabi)" → "Appendix B (Course Syllabi)"
        t = t.replace('Appendix A (Course Syllabi)', 'Appendix B (Course Syllabi)')
        t = t.replace('Appendix A</a> (Course Syllabi)', 'Appendix B</a> (Course Syllabi)')
        # nav prev: "Appendix A Course Syllabi" → "Appendix B Course Syllabi"
        t = re.sub(
            r'<span class="nav-num">Appendix A</span><span class="nav-title">Course Syllabi</span>',
            '<span class="nav-num">Appendix B</span><span class="nav-title">Course Syllabi</span>',
            t
        )
        # Drop stray "Section D.7" artifact
        t = t.replace('<div class="page-current">Section D.7</div>', '')
        # Drop dangling "Appendix E: Intermediate Projects" next-link if present
        t = re.sub(
            r'<a class="next"[^>]*>[\s\S]*?Appendix E[\s\S]*?</a>\s*',
            '',
            t
        )
        if t != o:
            APX_C.write_text(t, encoding='utf-8')
            print(f'  Fixed {APX_C.relative_to(ROOT)}')


def fix_corruptions():
    """Sweep substitution corruptions."""
    print('=== Fix 2: substitution corruptions ===')
    corruptions = [
        (r'Hugging Face softmax library', 'Hugging Face Transformers library'),
        (r'interpretability methods for softmax\b', 'interpretability methods for LLMs'),
        # Other potential corruptions to be added if found by audit
    ]
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        t = p.read_text(encoding='utf-8')
        o = t
        for pat, repl in corruptions:
            t = re.sub(pat, repl, t)
        if t != o:
            p.write_text(t, encoding='utf-8')
            n += 1
    print(f'  Fixed {n} files')


def fix_section_4210_4211():
    """Sections 42.10 and 42.11 self-title as 42.9. Fix to their real numbers."""
    print('=== Fix 3: sections 42.10 / 42.11 self-titling ===')
    ch42_dir = ROOT / 'part-9-llm-evaluation-observability' / 'module-42-evaluation-foundations'
    for n in (10, 11):
        p = ch42_dir / f'section-42.{n}.html'
        if not p.exists():
            continue
        t = p.read_text(encoding='utf-8')
        o = t
        t = re.sub(r'<title>Section 42\.9:', f'<title>Section 42.{n}:', t)
        t = re.sub(r'(<meta content=")Section 42\.9:', rf'\1Section 42.{n}:', t)
        t = re.sub(r'<div class="page-current">Section 42\.9</div>',
                   f'<div class="page-current">Section 42.{n}</div>', t)
        t = re.sub(r'<span class="bc-current">Section 42\.9</span>',
                   f'<span class="bc-current">Section 42.{n}</span>', t)
        if t != o:
            p.write_text(t, encoding='utf-8')
            print(f'  Fixed section-42.{n}.html')


def fix_part_breadcrumbs():
    """Set part breadcrumb / pagefind-meta to canonical per file location."""
    print('=== Fix 4: stale part-name breadcrumbs ===')
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        rel = p.relative_to(ROOT)
        parts = rel.parts
        if not parts or parts[0] not in PART_NAMES:
            continue
        part_roman, part_name = PART_NAMES[parts[0]]
        canonical = f'{part_roman}: {part_name}'
        t = p.read_text(encoding='utf-8')
        o = t
        # Breadcrumb link: <a href="...index.html">Part X: NAME</a>
        # Match any href pointing at the part-level index
        t = re.sub(
            r'(<a href="(?:\.\./)?(?:\.\./)?index\.html">)Part [IVXLCDM]+:\s*[^<]+(</a>)',
            rf'\1{canonical}\2',
            t
        )
        # pagefind-meta part attribute
        t = re.sub(
            r'data-pagefind-meta="part:Part [IVXLCDM]+:\s*[^"]+"',
            f'data-pagefind-meta="part:{canonical}"',
            t
        )
        # chapter-nav up label: <span class="nav-num">Part X</span><span class="nav-title">NAME</span>
        t = re.sub(
            r'(<span class="nav-num">)Part [IVXLCDM]+(</span><span class="nav-title">)[^<]+(</span>)',
            rf'\1{part_roman}\2{part_name}\3',
            t
        )
        if t != o:
            p.write_text(t, encoding='utf-8')
            n += 1
    print(f'  Updated {n} files')


def fix_part1_index_ch0_ordering():
    """Move Chapter 0 card to the top of part-1-llm-building-blocks/index.html."""
    print('=== Fix 5: Part 1 index Ch 0 ordering ===')
    p = ROOT / 'part-1-llm-building-blocks' / 'index.html'
    if not p.exists():
        return
    t = p.read_text(encoding='utf-8')
    # Find the Ch 0 chapter-card block
    m = re.search(
        r'(<div class="chapter-card">\s*<div class="chapter-card-header"><span class="mod-num">Chapter 0</span>[\s\S]*?</div>\s*</div>\s*)',
        t
    )
    if not m:
        print('  Ch 0 card not found; skipping')
        return
    ch0_block = m.group(1)
    # Remove the Ch 0 card from its current position
    t_without = t.replace(ch0_block, '', 1)
    # Find the first chapter-card block in the modified text and insert Ch 0 before it
    insert_match = re.search(r'<div class="chapter-card">', t_without)
    if not insert_match:
        print('  No insertion point found; skipping')
        return
    idx = insert_match.start()
    new_t = t_without[:idx] + ch0_block + t_without[idx:]
    if new_t != t:
        p.write_text(new_t, encoding='utf-8')
        print('  Moved Ch 0 card to top')


def fix_module10_next_link():
    """Module-10 interpretability index has next-link pointing to itself; fix it."""
    print('=== Fix 6: module-10 self-pointing next-link ===')
    p = ROOT / 'part-2-understanding-llms' / 'module-10-interpretability' / 'index.html'
    if not p.exists():
        return
    t = p.read_text(encoding='utf-8')
    o = t
    # Look for next link that points to ../module-10-interpretability or to "../module-10-interpretability/index.html"
    t = re.sub(
        r'<a class="next"[^>]*href="\.\./module-10-interpretability/[^"]*"[^>]*>[\s\S]*?</a>',
        '<a class="next" href="../../part-3-working-with-llms/module-11-llm-apis/index.html"><span class="nav-label">Next</span><span class="nav-num">Chapter 11</span><span class="nav-title">Working with LLM APIs</span></a>',
        t
    )
    # Also handle the image src double-prefix issue
    t = t.replace(
        '../../part-2-understanding-llms/module-10-interpretability/images/chapter-opener.png',
        'images/chapter-opener.png'
    )
    if t != o:
        p.write_text(t, encoding='utf-8')
        print('  Fixed module-10 index')


def fix_module08_self_ref():
    """Module-08 references 'Section 8.3' as if external; drop the self-ref."""
    print('=== Fix 7: module-08 self-reference ===')
    p = ROOT / 'part-2-understanding-llms' / 'module-08-reasoning-test-time-compute' / 'index.html'
    if not p.exists():
        return
    t = p.read_text(encoding='utf-8')
    o = t
    # Line ~36: "from Chapter 8" referring to self — fix to module-07 (Modern LLM Landscape)
    t = re.sub(
        r'\bfrom Chapter 8\b(?!\.)',
        'from Chapter 7 (Modern LLM Landscape)',
        t
    )
    # Line ~51: "Section 8.3" reference to self
    t = re.sub(
        r'<a [^>]*href="index\.html#[^"]*"[^>]*>Section 8\.3</a>',
        'Section 7.3 (Multilingual)',
        t
    )
    if t != o:
        p.write_text(t, encoding='utf-8')
        print('  Fixed module-08 index')


def main():
    fix_appendices()
    fix_corruptions()
    fix_section_4210_4211()
    fix_part_breadcrumbs()
    fix_part1_index_ch0_ordering()
    fix_module10_next_link()
    fix_module08_self_ref()


if __name__ == '__main__':
    main()
