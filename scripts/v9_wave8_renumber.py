"""Wave 8: cascade renumber chapters to v9 canonical numbering.

Existing 70 chapters get renumbered to their canonical v9 positions,
leaving gaps where Wave 9 will author missing chapters.

Target numbering (with reserved gaps for Wave 9):
  Part 1   (LLM Building Blocks):     0-5
  Part 2   (Understanding LLMs):       6-10
  Part 3   (Working with LLMs):        11-14
  Part 4   (Training & Adaptation):    15-19
  Part 5   (Multimodal LLMs):          20-25
  Part 6   (Agentic AI):               26-30
  Part 7   (Retrieval & IE w/ LLMs):   31-33 (gaps 34-36 for new chapters)
  Part 8   (Conversational AI w/ LLMs):37-39 (gaps 40-41 for new chapters)
  Part 9   (Eval & Observability):     42-45 (gap 46 for LLM-as-Judge)
  Part 10  (Security & Runtime Safety):47-51
  Part 11  (Ethics, Trust, Governance):52-55 (gap 56 for Tools)
  Part 12  (LLM Systems at Scale):     57-58 (gaps 59-61 for new chapters)
  Part 13  (LLMOps & Lifecycle):       62 (gaps 63-66 for new chapters)
  Part 14  (Designing Products):       67-71
  Part 15  (Applications):             72-79
  Part 16  (Research Frontiers):       80-83

Total: 70 chapters renumbered, 14 gaps reserved for Wave 9.
"""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
             'source_fix_backups', 'pagefind', 'templates', '.claude',
             '.book-update', 'vendor', 'docs'}

# (part_dir, [old_chapter_num, new_chapter_num] pairs in order)
# I'll iterate parts in order; chapters in each part get reassigned sequentially
RENUMBERING = [
    # (part_slug, [(old_ch, new_ch), ...])
    ('part-1-llm-building-blocks', [(0, 0), (1, 1), (3, 2), (4, 3), (5, 4), (6, 5)]),
    ('part-2-understanding-llms', [(7, 6), (8, 7), (9, 8), (10, 9), (11, 10)]),
    ('part-3-working-with-llms', [(13, 11), (14, 12), (15, 13), (16, 14)]),
    ('part-4-training-adaptation', [(17, 15), (18, 16), (19, 17), (20, 18), (21, 19)]),
    ('part-5-multimodal-llms', [(32, 20), (34, 21), (35, 22), (36, 23), (39, 24), (43, 25)]),
    ('part-6-agentic-ai', [(26, 26), (27, 27), (28, 28), (29, 29), (30, 30)]),
    ('part-7-retrieval-information-extraction-with-llms', [(22, 31), (23, 32), (42, 33)]),
    ('part-8-conversational-ai-with-llms', [(24, 37), (25, 38), (38, 39)]),
    ('part-9-llm-evaluation-observability', [(44, 42), (46, 43), (47, 44), (48, 45)]),
    ('part-10-llm-security-runtime-safety', [(49, 47), (50, 48), (51, 49), (52, 50), (60, 51)]),
    ('part-11-llm-ethics-trust-governance', [(53, 52), (55, 53), (56, 54), (58, 55)]),
    ('part-12-llm-systems-at-scale', [(61, 57), (84, 58)]),
    ('part-13-llmops-lifecycle', [(62, 62)]),
    ('part-14-designing-llm-agent-products', [(63, 67), (66, 68), (69, 69), (70, 70), (71, 71)]),
    ('part-15-applications-of-llms-across-industries',
     [(72, 72), (73, 73), (74, 74), (75, 75), (76, 76), (77, 77), (78, 78), (81, 79)]),
    ('part-16-llm-agentic-ai-research-frontiers', [(82, 80), (83, 81), (85, 82), (86, 83)]),
]


def get_module_dir(part_dir, ch_num):
    """Find the module-N-... dir for chapter N inside part_dir."""
    for d in part_dir.glob(f'module-{ch_num:02d}-*/') if ch_num < 10 else part_dir.glob(f'module-{ch_num}-*/'):
        return d
    # Try non-zero-padded too
    for d in part_dir.glob(f'module-{ch_num}-*/'):
        return d
    return None


def step1_rename_dirs_to_tmp():
    """Rename each module-OLD-name to module-NEWNUM-name.__tmp__ to avoid collisions."""
    print('--- Step 1: rename module dirs to .__tmp__ ---')
    n = 0
    for part_slug, ch_mapping in RENUMBERING:
        part_dir = ROOT / part_slug
        if not part_dir.exists():
            print(f'  SKIP: {part_slug} missing')
            continue
        for old_ch, new_ch in ch_mapping:
            old_dir = get_module_dir(part_dir, old_ch)
            if not old_dir:
                continue
            # Extract slug suffix
            m = re.match(r'module-\d+-(.+)$', old_dir.name)
            if not m: continue
            slug = m.group(1)
            new_name = f'module-{new_ch:02d}-{slug}.__tmp__' if new_ch < 10 else f'module-{new_ch}-{slug}.__tmp__'
            new_dir = part_dir / new_name
            if new_dir.exists(): continue
            r = subprocess.run(['git', 'mv', str(old_dir), str(new_dir)],
                              cwd=ROOT, capture_output=True, text=True)
            if r.returncode == 0:
                n += 1
    print(f'  Renamed {n} to .__tmp__')


def step2_rename_tmp_to_final():
    """Rename .__tmp__ to final name."""
    print('--- Step 2: rename .__tmp__ -> final ---')
    n = 0
    for part_slug, ch_mapping in RENUMBERING:
        part_dir = ROOT / part_slug
        if not part_dir.exists(): continue
        for old_ch, new_ch in ch_mapping:
            # Find the tmp dir
            for tmp_dir in part_dir.glob(f'*.__tmp__'):
                m = re.match(rf'module-{new_ch:02d}-(.+)\.__tmp__$' if new_ch < 10 else rf'module-{new_ch}-(.+)\.__tmp__$', tmp_dir.name)
                if not m: continue
                final_name = f'module-{new_ch:02d}-{m.group(1)}' if new_ch < 10 else f'module-{new_ch}-{m.group(1)}'
                final_dir = part_dir / final_name
                if final_dir.exists(): continue
                r = subprocess.run(['git', 'mv', str(tmp_dir), str(final_dir)],
                                  cwd=ROOT, capture_output=True, text=True)
                if r.returncode == 0:
                    n += 1
                break
    print(f'  Renamed {n} .__tmp__ to final')


def step3_rename_section_files():
    """Inside each renamed module, rename section-OLD.Y.html → section-NEW.Y.html."""
    print('--- Step 3: rename section files ---')
    n = 0
    for part_slug, ch_mapping in RENUMBERING:
        part_dir = ROOT / part_slug
        if not part_dir.exists(): continue
        for old_ch, new_ch in ch_mapping:
            if old_ch == new_ch: continue  # nothing to rename
            new_dir = get_module_dir(part_dir, new_ch)
            if not new_dir: continue
            for sec in list(new_dir.glob(f'section-{old_ch}.*.html')):
                m = re.match(rf'section-{old_ch}\.(\d+)\.html', sec.name)
                if not m: continue
                new_sec = new_dir / f'section-{new_ch}.{m.group(1)}.html'
                if new_sec.exists(): continue
                r = subprocess.run(['git', 'mv', str(sec), str(new_sec)],
                                  cwd=ROOT, capture_output=True, text=True)
                if r.returncode == 0:
                    n += 1
    print(f'  Renamed {n} section files')


def step4_rewrite_in_file_metadata():
    """For each renumbered chapter, rewrite the chapter num in section files and chapter index."""
    print('--- Step 4: rewrite in-file metadata ---')
    n = 0
    for part_slug, ch_mapping in RENUMBERING:
        part_dir = ROOT / part_slug
        if not part_dir.exists(): continue
        for old_ch, new_ch in ch_mapping:
            if old_ch == new_ch: continue
            mod_dir = get_module_dir(part_dir, new_ch)
            if not mod_dir: continue
            for f in mod_dir.glob('*.html'):
                text = f.read_text(encoding='utf-8')
                orig = text
                # In-file section refs
                text = re.sub(rf'\bsection-{old_ch}\.(\d+)\.html\b',
                             rf'section-{new_ch}.\1.html', text)
                # Chapter num spans
                text = re.sub(rf'\bChapter {old_ch}(?!\d)', f'Chapter {new_ch}', text)
                # Section X.Y references
                text = re.sub(rf'\bSection {old_ch}\.(\d+)\b',
                             rf'Section {new_ch}.\1', text)
                # span.sec-num and toc-sec-num
                text = re.sub(
                    rf'(<span class="(?:sec-num|toc-sec-num|nav-num|section-num)"[^>]*>){old_ch}\.(\d+)(</span>)',
                    rf'\g<1>{new_ch}.\2\g<3>', text
                )
                # span.mod-num
                text = re.sub(rf'(<span class="mod-num"[^>]*>Chapter ){old_ch}(</span>)',
                             rf'\g<1>{new_ch}\2', text)
                # Anchor IDs
                text = re.sub(rf'\bid="{old_ch}-(\d+)-', rf'id="{new_ch}-\1-', text)
                text = re.sub(rf'\bhref="#{old_ch}-(\d+)-', rf'href="#{new_ch}-\1-', text)
                if text != orig:
                    f.write_text(text, encoding='utf-8')
                    n += 1
    print(f'  Updated in-file metadata in {n} files')


def step5_rewrite_cross_refs():
    """Walk every HTML and rewrite cross-refs from old chapter num to new."""
    print('--- Step 5: rewrite cross-refs ---')
    # Build comprehensive mapping
    mod_renames = {}  # old_mod_name -> new_mod_name
    section_renames = {}  # (mod_name, old_y) -> (new_mod_name, ...) — not really, sections renumber WITHIN module
    for part_slug, ch_mapping in RENUMBERING:
        part_dir = ROOT / part_slug
        if not part_dir.exists(): continue
        for old_ch, new_ch in ch_mapping:
            if old_ch == new_ch: continue
            new_dir = get_module_dir(part_dir, new_ch)
            if not new_dir: continue
            new_name = new_dir.name
            # Old name was: module-OLD_CH-{slug-part}
            m = re.match(r'module-\d+-(.+)$', new_name)
            slug_part = m.group(1) if m else ''
            old_name_candidates = [
                f'module-{old_ch:02d}-{slug_part}' if old_ch < 10 else f'module-{old_ch}-{slug_part}',
            ]
            for old_name in old_name_candidates:
                mod_renames[old_name] = new_name

    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP_DIRS: continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # Module dir renames in hrefs
        for old_name, new_name in mod_renames.items():
            text = text.replace(f'/{old_name}/', f'/{new_name}/')
            text = text.replace(f'"{old_name}/', f'"{new_name}/')
        # Section file refs: section-OLD_CH.Y.html → section-NEW_CH.Y.html
        # Use a more specific pattern — old chapter num must be paired with the matching module name
        for part_slug, ch_mapping in RENUMBERING:
            for old_ch, new_ch in ch_mapping:
                if old_ch == new_ch: continue
                # Find the matching module name
                part_dir = ROOT / part_slug
                if not part_dir.exists(): continue
                new_dir = get_module_dir(part_dir, new_ch)
                if not new_dir: continue
                # Match href="...module-NEW_CH-name/section-OLD_CH.Y.html"
                text = re.sub(
                    rf'({re.escape(new_dir.name)}/section-){old_ch}\.(\d+)\.html',
                    rf'\g<1>{new_ch}.\2.html', text
                )
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'  Cross-refs rewritten in {n_files} files')


def main():
    print('=== WAVE 8: cascade renumber to canonical scheme ===\n')
    step1_rename_dirs_to_tmp()
    step2_rename_tmp_to_final()
    step3_rename_section_files()
    step4_rewrite_in_file_metadata()
    step5_rewrite_cross_refs()
    print('\nWave 8 cascade renumber complete.')


if __name__ == '__main__':
    main()
