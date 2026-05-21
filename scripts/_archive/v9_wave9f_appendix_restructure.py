"""Wave 9 step F finalization: drop Apx B.1-B.3, move B.4 to Ch 42, rename C→B, D→C.

Result:
  Apx A Mathematical Foundations (unchanged, 6 sections)
  Apx B Course Syllabi              (was Apx C)
  Apx C Reading Pathways            (was Apx D)

  Plus: new Section 42.12 "Classical ML Evaluation Metrics" (was Apx B.4)
        in Part 9 Ch 42 (Evaluation Foundations).

Steps:
  1. git mv section-b.4.html → part 9 Ch 42 section-42.12.html with metadata rewrite
  2. git rm section-b.1.html, section-b.2.html, section-b.3.html
  3. git rm appendix-b-ml-essentials/index.html and images
  4. git mv appendix-c-course-syllabi → appendix-b-course-syllabi (via __tmp__)
  5. git mv appendix-d-reading-pathways → appendix-c-reading-pathways (via __tmp__)
  6. Rewrite inbound refs globally:
     - section-b.4.html → section-42.12.html (cross-part)
     - section-b.1|2|3.html → ch 0.1 (cross-part)
     - appendix-b-ml-essentials/index.html → appendices/index.html (with note)
     - appendix-c-course-syllabi → appendix-b-course-syllabi
     - appendix-d-reading-pathways → appendix-c-reading-pathways
     - "Appendix B.4" prose → "Section 42.12"
     - "Appendix C" prose → "Appendix B"
     - "Appendix D" prose → "Appendix C"
  7. Update appendices/index.html and ToC
"""
from pathlib import Path
import re
import shutil
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}

APX_DIR = ROOT / 'appendices'
APX_B = APX_DIR / 'appendix-b-ml-essentials'
APX_C = APX_DIR / 'appendix-c-course-syllabi'
APX_D = APX_DIR / 'appendix-d-reading-pathways'
CH42_DIR = ROOT / 'part-9-llm-evaluation-observability' / 'module-42-evaluation-foundations'


def rewrite_b4_to_4212(file_path):
    """Rewrite the moved B.4 section file: metadata + breadcrumbs."""
    text = file_path.read_text(encoding='utf-8')

    # title and meta
    text = re.sub(
        r'<title>Section B\.4:[^<]*</title>',
        '<title>Section 42.12: Classical ML Evaluation Metrics | Building Conversational AI with LLMs and Agents</title>',
        text
    )
    text = re.sub(
        r'(<meta content=")Section B\.4:[^"]*(")',
        r'\1Section 42.12: Classical ML Evaluation Metrics (BLEU, ROUGE, perplexity, classification metrics)\2',
        text
    )
    # page-current
    text = re.sub(r'<div class="page-current">Section B\.4</div>',
                  '<div class="page-current">Section 42.12</div>', text)
    # breadcrumb current
    text = re.sub(r'<span class="bc-current">Section B\.4</span>',
                  '<span class="bc-current">Section 42.12</span>', text)
    # h1 — change "Evaluation Metrics" to "Classical ML Evaluation Metrics"
    text = re.sub(r'<h1>Evaluation Metrics</h1>',
                  '<h1>Classical ML Evaluation Metrics</h1>', text, count=1)
    # breadcrumb to chapter
    text = re.sub(
        r'<a href="\.\./\.\./appendices/index\.html">Appendices</a>',
        '<a href="../index.html">Part IX: LLM Evaluation &amp; Observability</a>',
        text
    )
    text = re.sub(
        r'<a href="\.\.[^"]*/appendix-b-ml-essentials/index\.html">[^<]*</a>',
        '<a href="index.html">Chapter 42</a>',
        text
    )
    # pagefind chapter meta
    text = re.sub(
        r'<span class="pagefind-meta-injected" data-pagefind-meta="chapter:[^"]+"',
        '<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter 42"',
        text
    )
    # styles/scripts paths: appendix lives at appendices/appendix-b/section-b.4.html
    # which means ../../styles/book.css; chapter sections also use ../../styles/book.css
    # so no change needed for those.

    # Anchor IDs
    text = re.sub(r'\bid="b-4-', 'id="42-12-', text)
    text = re.sub(r'\bhref="#b-4-', 'href="#42-12-', text)
    text = re.sub(r'\bSection B\.4\b', 'Section 42.12', text)
    text = re.sub(r'\bB\.4\.(\d+)\b', r'42.12.\1', text)

    # chapter-nav: prev was section-b.3 (gone); up was apx B (gone); next was capstone or similar
    # Replace the whole chapter-nav with a clean version pointing to Part 9 Ch 42's prev (sec 42.11) and next.
    # Just remove old nav links; rebuild_linear_nav.py will fix them.
    text = re.sub(
        r'<a class="prev"[^>]*>[\s\S]*?</a>\s*',
        '<a class="prev" href="section-42.11.html"><span class="nav-label">Previous</span><span class="nav-num">Section 42.11</span><span class="nav-title">Structured-Output Validity Testing</span></a>',
        text, count=1
    )
    text = re.sub(
        r'<a class="up"[^>]*>[\s\S]*?</a>\s*',
        '<a class="up" href="index.html"><span class="nav-label">Up</span><span class="nav-num">Chapter 42</span><span class="nav-title">Evaluation Foundations</span></a>',
        text, count=1
    )
    text = re.sub(
        r'<a class="next"[^>]*>[\s\S]*?</a>\s*',
        '<a class="next" href="../module-43-specialized-evaluation/section-43.1.html"><span class="nav-label">Next</span><span class="nav-num">Section 43.1</span><span class="nav-title">Specialized Evaluation</span></a>',
        text, count=1
    )

    file_path.write_text(text, encoding='utf-8')


def main():
    # =========== Step 1: move B.4 → Ch 42.12 ===========
    print('Step 1: move B.4 → Ch 42.12')
    src = APX_B / 'section-b.4.html'
    tmp = CH42_DIR / 'section-42.12.html.__tmp__'
    dst = CH42_DIR / 'section-42.12.html'
    if src.exists() and not dst.exists():
        subprocess.run(['git', 'mv', str(src), str(tmp)], cwd=ROOT, capture_output=True)
        subprocess.run(['git', 'mv', str(tmp), str(dst)], cwd=ROOT, capture_output=True)
        rewrite_b4_to_4212(dst)
        print(f'  Moved + rewrote {dst.relative_to(ROOT)}')

    # =========== Step 2: delete B.1, B.2, B.3 ===========
    print('Step 2: delete B.1, B.2, B.3')
    for n in ('b.1', 'b.2', 'b.3'):
        p = APX_B / f'section-{n}.html'
        if p.exists():
            subprocess.run(['git', 'rm', str(p)], cwd=ROOT, capture_output=True)
            print(f'  rm {p.relative_to(ROOT)}')

    # =========== Step 3: delete rest of Apx B ===========
    print('Step 3: delete rest of Apx B')
    for child in list(APX_B.rglob('*')):
        if child.is_file():
            subprocess.run(['git', 'rm', '-f', str(child)], cwd=ROOT, capture_output=True)
    if APX_B.exists():
        try:
            shutil.rmtree(APX_B)
            print(f'  Removed {APX_B.relative_to(ROOT)}/')
        except OSError as e:
            print(f'  Could not remove {APX_B}: {e}')

    # =========== Step 4: rename C → B ===========
    print('Step 4: rename Apx C → Apx B (Course Syllabi)')
    new_b = APX_DIR / 'appendix-b-course-syllabi'
    tmp_b = APX_DIR / 'appendix-b-course-syllabi.__tmp__'
    if APX_C.exists() and not new_b.exists():
        subprocess.run(['git', 'mv', str(APX_C), str(tmp_b)], cwd=ROOT, capture_output=True)
        subprocess.run(['git', 'mv', str(tmp_b), str(new_b)], cwd=ROOT, capture_output=True)
        # Update internal letters: C → B (in titles, breadcrumbs, anchors)
        for p in new_b.rglob('*.html'):
            t = p.read_text(encoding='utf-8')
            o = t
            t = re.sub(r'\bAppendix C\b', 'Appendix B', t)
            t = re.sub(r'<title>([^<]*?)\bC([:.]\s*)', r'<title>\1B\2', t)  # be cautious — only at start of title
            t = re.sub(r'<span class="toc-chapter-num"[^>]*>C</span>',
                       '<span class="toc-chapter-num" aria-label="Appendix B">B</span>', t)
            t = re.sub(r'aria-label="Appendix C"', 'aria-label="Appendix B"', t)
            t = re.sub(r'>Appendix C<', '>Appendix B<', t)
            # nav-num "Appendix C" → "Appendix B"
            t = re.sub(r'<span class="nav-num">Appendix C</span>',
                       '<span class="nav-num">Appendix B</span>', t)
            if t != o:
                p.write_text(t, encoding='utf-8')
        print(f'  Renamed → {new_b.relative_to(ROOT)}')

    # =========== Step 5: rename D → C ===========
    print('Step 5: rename Apx D → Apx C (Reading Pathways)')
    new_c = APX_DIR / 'appendix-c-reading-pathways'
    tmp_c = APX_DIR / 'appendix-c-reading-pathways.__tmp__'
    if APX_D.exists() and not new_c.exists():
        subprocess.run(['git', 'mv', str(APX_D), str(tmp_c)], cwd=ROOT, capture_output=True)
        subprocess.run(['git', 'mv', str(tmp_c), str(new_c)], cwd=ROOT, capture_output=True)
        for p in new_c.rglob('*.html'):
            t = p.read_text(encoding='utf-8')
            o = t
            t = re.sub(r'\bAppendix D\b', 'Appendix C', t)
            t = re.sub(r'aria-label="Appendix D"', 'aria-label="Appendix C"', t)
            t = re.sub(r'>Appendix D<', '>Appendix C<', t)
            t = re.sub(r'<span class="toc-chapter-num"[^>]*>D</span>',
                       '<span class="toc-chapter-num" aria-label="Appendix C">C</span>', t)
            t = re.sub(r'<span class="nav-num">Appendix D</span>',
                       '<span class="nav-num">Appendix C</span>', t)
            if t != o:
                p.write_text(t, encoding='utf-8')
        print(f'  Renamed → {new_c.relative_to(ROOT)}')

    # =========== Step 6: global cross-ref rewrites ===========
    print('Step 6: global cross-ref rewrite')

    # The path depth varies — we need to handle both `..` patterns.
    # Patterns to find and rewrite:
    rewrites = [
        # B.4 → 42.12 (could be 1 or 2 ../ prefix; both replaced with appropriate target)
        (re.compile(r'\.\./\.\./appendices/appendix-b-ml-essentials/section-b\.4\.html(#[^"]*)?'),
         r'../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.12.html\1'),
        # From within appendices/ subdir (1 ../)
        (re.compile(r'\.\./appendix-b-ml-essentials/section-b\.4\.html(#[^"]*)?'),
         r'../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.12.html\1'),
        # B.1, B.2, B.3 → Ch 0.1 (covered material)
        (re.compile(r'\.\./\.\./appendices/appendix-b-ml-essentials/section-b\.[123]\.html(#[^"]*)?'),
         r'../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html\1'),
        (re.compile(r'\.\./appendix-b-ml-essentials/section-b\.[123]\.html(#[^"]*)?'),
         r'../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html\1'),
        # Apx B index → Ch 0 (covered material)
        (re.compile(r'\.\./\.\./appendices/appendix-b-ml-essentials/index\.html'),
         r'../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html'),
        (re.compile(r'\.\./appendix-b-ml-essentials/index\.html'),
         r'../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html'),
        # Apx C dir → Apx B dir
        (re.compile(r'appendix-c-course-syllabi'),
         r'appendix-b-course-syllabi'),
        # Apx D dir → Apx C dir
        (re.compile(r'appendix-d-reading-pathways'),
         r'appendix-c-reading-pathways'),
    ]

    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        for pat, repl in rewrites:
            text = pat.sub(repl, text)
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'  Cross-refs rewritten in {n_files} files')

    # Step 6b: in prose, "Appendix B" should not appear (we dropped B); "Appendix B.4" → "Section 42.12"
    # But "Appendix B" might now correctly refer to NEW Apx B (former C, Course Syllabi). Keep careful.
    # For files OUTSIDE the appendices/ dir, "Appendix B" prose was almost certainly meant for the OLD B (ML Essentials).
    # However, we already rewrote the href, so the prose still says "Appendix B" but links to Ch 0 now.
    # Let's pragmatically rewrite "Appendix B.4" → "Section 42.12" and "Appendix B" → "Chapter 0" in prose (excluding appendices/ files).
    # NEW Apx B (Course Syllabi) only gets linked, no one says "Appendix B" in prose about it pre-rename.

    n_prose = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        rel = str(p.relative_to(ROOT))
        if rel.startswith('appendices/appendix-b-course-syllabi/') or rel.startswith('appendices/appendix-c-reading-pathways/'):
            continue  # in new Apx B and C dirs, "Appendix B/C" are their own self-refs
        text = p.read_text(encoding='utf-8')
        orig = text
        text = re.sub(r'\bAppendix B\.4\b', 'Section 42.12', text)
        text = re.sub(r'\bAppendix B\.[123]\b', 'Chapter 0 (Section 0.1)', text)
        # Standalone "Appendix B" (in prose, not href context) → "Chapter 0 (Section 0.1)"
        # Be careful: don't touch HTML attributes.
        text = re.sub(r'(?<!"|=|>)Appendix B(?!\s*\.\d|\s*</)\b', 'Chapter 0 (Section 0.1)', text)
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_prose += 1
    print(f'  Prose mentions updated in {n_prose} files')

    # =========== Step 7: update Ch 42 index (add 42.12 card) ===========
    print('Step 7: update Ch 42 index')
    ch42_idx = CH42_DIR / 'index.html'
    if ch42_idx.exists():
        text = ch42_idx.read_text(encoding='utf-8')
        if 'section-42.12.html' not in text:
            new_card = (
                '<li><a class="section-card" href="section-42.12.html">\n'
                '<span class="section-num">42.12</span>\n'
                '<span class="section-title">Classical ML Evaluation Metrics</span>\n'
                '<span class="section-desc">Reference: BLEU, ROUGE, perplexity, classification metrics (precision/recall/F1, AUC), and language-generation metrics. Promoted from former Apx B.4.</span>\n'
                '</a></li>'
            )
            # Insert before closing </ul> of the sections-list
            text = re.sub(
                r'(</ul>)(\s*<nav class="chapter-nav">)',
                new_card + r'\n\1\2',
                text,
                count=1
            )
            ch42_idx.write_text(text, encoding='utf-8')
            print('  Added 42.12 card to Ch 42 index')


if __name__ == '__main__':
    main()
