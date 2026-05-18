"""Wave 3 v2: sibling merges with proper in-memory mapping.

Key fix vs v1: explicit mapping built during this run, applied with strict
scoping (only to refs that match BOTH the source module AND the source section).
Does NOT use git log (which can include unrelated historical renames).
"""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}

# Format: (part_dir, target_module, [source_modules])
MERGES = [
    ('part-1-foundations', 'module-01-foundations-nlp-text-representation',
     ['module-02-tokenization-subword-models']),
    ('part-2-understanding-llms', 'module-11-interpretability',
     ['module-12-tools-of-the-trade']),
    ('part-7-multimodal-generation', 'module-32-audio-music-generation',
     ['module-33-video-generation']),
    ('part-7-multimodal-generation', 'module-35-vision-language-models',
     ['module-37-unified-multimodal-omni']),
    ('part-7-multimodal-generation', 'module-39-vla-models',
     ['module-40-llm-robotics']),
    ('part-9-safety-security-ethics', 'module-53-bias-fairness',
     ['module-54-hallucination-truthfulness']),
    ('part-9-safety-security-ethics', 'module-56-watermarking-provenance',
     ['module-57-transparency-documentation']),
    ('part-9-safety-security-ethics', 'module-58-environmental-sustainability',
     ['module-59-frontier-safety-open-problems']),
    ('part-11-designing-llm-products', 'module-63-ideation',
     ['module-64-product-management', 'module-65-strategy-prioritization', 'module-68-prototype-to-production']),
    ('part-11-designing-llm-products', 'module-66-vibe-coding',
     ['module-67-mvp']),
    ('part-12-applications-across-industries', 'module-78-manufacturing-llms',
     ['module-79-creative-industries', 'module-80-recommendation-search']),
]


def get_ch_num(mod_name):
    m = re.match(r'module-(\d+)-', mod_name)
    return int(m.group(1)) if m else None


def merge_one(part_dir, target_mod, source_mods):
    """Returns list of mapping tuples: (src_mod, src_ch, src_y, tgt_mod, tgt_ch, tgt_y)"""
    part_path = ROOT / part_dir
    tgt = part_path / target_mod
    if not tgt.exists():
        return []
    tgt_ch = get_ch_num(target_mod)

    # Find next available section number in target
    existing = []
    for s in tgt.glob(f'section-{tgt_ch}.*.html'):
        m = re.match(rf'section-{tgt_ch}\.(\d+)\.html', s.name)
        if m: existing.append(int(m.group(1)))
    next_y = (max(existing) + 1) if existing else 1

    mappings = []
    for src_mod in source_mods:
        src = part_path / src_mod
        if not src.exists(): continue
        src_ch = get_ch_num(src_mod)
        src_sections = sorted(src.glob(f'section-{src_ch}.*.html'),
                            key=lambda p: int(re.match(rf'section-{src_ch}\.(\d+)\.html', p.name).group(1)))
        for s in src_sections:
            m = re.match(rf'section-{src_ch}\.(\d+)\.html', s.name)
            old_y = int(m.group(1))
            new_y = next_y
            next_y += 1
            new_path = tgt / f'section-{tgt_ch}.{new_y}.html'
            r = subprocess.run(['git', 'mv', str(s), str(new_path)],
                              cwd=ROOT, capture_output=True, text=True)
            if r.returncode != 0:
                continue
            # Rewrite in-file IDENTITY metadata
            rewrite_section_identity(new_path, src_ch, old_y, tgt_ch, new_y)
            mappings.append((src_mod, src_ch, old_y, target_mod, tgt_ch, new_y))
        # Delete source dir (gitwise)
        if src.exists():
            subprocess.run(['git', 'rm', '-rf', str(src)],
                          cwd=ROOT, capture_output=True, text=True)
    return mappings


def rewrite_section_identity(file_path, old_ch, old_y, new_ch, new_y):
    """Update only the FILE'S OWN identity (title, breadcrumb, page-current, anchor IDs).
    Doesn't touch refs to OTHER sections — those handled in cross-ref pass.
    """
    text = file_path.read_text(encoding='utf-8')
    orig = text
    new_label = f'{new_ch}.{new_y}'
    text = re.sub(rf'<title>Section {old_ch}\.{old_y}:',
                  f'<title>Section {new_label}:', text)
    text = re.sub(rf'(<meta content=")Section {old_ch}\.{old_y}:',
                  rf'\1Section {new_label}:', text)
    text = re.sub(r'<div class="page-current">Section [^<]+</div>',
                  f'<div class="page-current">Section {new_label}</div>', text)
    text = re.sub(r'<span class="bc-current">Section [^<]+</span>',
                  f'<span class="bc-current">Section {new_label}</span>', text)
    # Anchor IDs (own page anchors)
    text = re.sub(rf'\bid="{old_ch}-{old_y}-', f'id="{new_ch}-{new_y}-', text)
    text = re.sub(rf'\bhref="#{old_ch}-{old_y}-', f'href="#{new_ch}-{new_y}-', text)
    if text != orig:
        file_path.write_text(text, encoding='utf-8')


def apply_cross_refs(all_mappings):
    """Apply STRICT cross-ref rewrites: only rewrite when both source module AND section match."""
    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP: continue
        text = p.read_text(encoding='utf-8')
        orig = text
        for src_mod, src_ch, src_y, tgt_mod, tgt_ch, tgt_y in all_mappings:
            # Pattern: href="...src_mod/section-X.Y.html"
            text = re.sub(
                rf'(href="[^"]*?){re.escape(src_mod)}/section-{src_ch}\.{src_y}\.html',
                rf'\1{tgt_mod}/section-{tgt_ch}.{tgt_y}.html',
                text
            )
            # Within merged target dir: same-dir refs like "section-X.Y.html"
            # ONLY if the current file is INSIDE tgt_mod
            if tgt_mod in p.parts:
                text = re.sub(
                    rf'\bhref="section-{src_ch}\.{src_y}\.html',
                    f'href="section-{tgt_ch}.{tgt_y}.html',
                    text
                )
                text = re.sub(
                    rf'\bhref="section-{src_ch}\.{src_y}\.html#',
                    f'href="section-{tgt_ch}.{tgt_y}.html#',
                    text
                )
        # Index page refs: src_mod/index.html -> tgt_mod/index.html
        for src_mod, src_ch, src_y, tgt_mod, tgt_ch, tgt_y in all_mappings:
            text = re.sub(
                rf'(href="[^"]*?){re.escape(src_mod)}/index\.html',
                rf'\1{tgt_mod}/index.html',
                text
            )
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    return n_files


def main():
    print('=== Wave 3 v2: sibling merges with strict cross-ref scoping ===\n')
    all_mappings = []
    for part_dir, tgt_mod, src_mods in MERGES:
        print(f'MERGE: {tgt_mod} <- {src_mods}')
        mappings = merge_one(part_dir, tgt_mod, src_mods)
        all_mappings.extend(mappings)
        print(f'  {len(mappings)} sections moved')

    print(f'\nTotal: {len(all_mappings)} section moves')
    print('\n--- Applying cross-refs (strict scoping) ---')
    n = apply_cross_refs(all_mappings)
    print(f'Cross-refs applied in {n} files')


if __name__ == '__main__':
    main()
