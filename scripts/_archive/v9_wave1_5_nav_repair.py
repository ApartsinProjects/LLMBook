"""Wave 1.5: repair broken nav and cross-refs after Wave 1 deletions.

Strategy:
  - Nav 'next'/'prev' pointing to deleted sections: rewrite to next non-deleted sibling
  - Body refs to deleted Ch 31, Ch 41, sec 8.3, industry .6 sections: rewrite to chapter index or canonical equivalent
  - Skip .book-update/ (preserved content, intentional)
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}

# Deleted entities and where their refs should now point
REWRITES = {
    # Sec 8.3 (Reasoning) → Ch 9 index (Reasoning is the whole chapter)
    'section-8.3.html': '../module-09-reasoning-test-time-compute/index.html',
    # Industry generic overview sections → chapter index of their chapter
    'section-73.6.html': 'index.html',
    'section-74.6.html': 'index.html',
    'section-76.6.html': 'index.html',
    'section-79.2.html': 'index.html',
    # Ch 31 (Multimodal overview) sections → Ch index of part-7
    'module-31-multimodal/section-31.1.html': 'module-32-audio-music-generation/index.html',
    'module-31-multimodal/section-31.2.html': 'module-32-audio-music-generation/index.html',
    'module-31-multimodal/section-31.3.html': 'module-34-document-understanding-ocr/index.html',
    'module-31-multimodal/section-31.4.html': 'module-37-unified-multimodal-omni/index.html',
    'module-31-multimodal/index.html': 'module-32-audio-music-generation/index.html',
    # Ch 41 (Embodied AI aggregator) sections → canonical replacement chapter
    'module-41-world-models-simulation/section-41.1.html': '../module-39-vla-models/index.html',
    'module-41-world-models-simulation/section-41.2.html': '../module-40-llm-robotics/index.html',
    'module-41-world-models-simulation/section-41.3.html': '../module-36-3d-generation-neural-scenes/index.html',
    'module-41-world-models-simulation/section-41.4.html': '../module-36-3d-generation-neural-scenes/index.html',
    'module-41-world-models-simulation/section-41.5.html': '../module-36-3d-generation-neural-scenes/index.html',
    'module-41-world-models-simulation/section-41.6.html': '../module-42-cross-modal-reasoning-rag/index.html',
    'module-41-world-models-simulation/section-41.7.html': '../module-42-cross-modal-reasoning-rag/index.html',
    'module-41-world-models-simulation/section-41.8.html': '../module-40-llm-robotics/index.html',
    'module-41-world-models-simulation/index.html': '../module-40-llm-robotics/index.html',
    # Sec 45.6 → moved to 44.12
    'module-45-testing-quality-gates/section-45.6.html': '../module-44-evaluation-foundations/section-44.12.html',
    'module-45-testing-quality-gates/index.html': '../module-44-evaluation-foundations/index.html',
}


def fix_nav_in_siblings():
    """Fix prev/next links in sibling sections of deleted files.

    For deletions that broke a chapter's section sequence, rewrite the
    surrounding sections' nav to skip the gap.
    """
    fixes = [
        # (section_to_fix, old_href, new_href, direction)
        # Sec 8.2 → 8.4 (skip 8.3)
        ('part-2-understanding-llms/module-08-modern-llm-landscape/section-8.2.html',
         'section-8.3.html', 'section-8.4.html'),
        ('part-2-understanding-llms/module-08-modern-llm-landscape/section-8.4.html',
         'section-8.3.html', 'section-8.2.html'),
        # Sec 73.5 → 74.1 (skip 73.6)
        ('part-12-applications-across-industries/module-73-finance-llms/section-73.5.html',
         'section-73.6.html', '../module-74-healthcare-llms/section-74.1.html'),
        ('part-12-applications-across-industries/module-74-healthcare-llms/section-74.1.html',
         '../module-73-finance-llms/section-73.6.html', '../module-73-finance-llms/section-73.5.html'),
        # Sec 74.5 → 75.1 (skip 74.6)
        ('part-12-applications-across-industries/module-74-healthcare-llms/section-74.5.html',
         'section-74.6.html', '../module-75-education-llms/section-75.1.html'),
        ('part-12-applications-across-industries/module-75-education-llms/section-75.1.html',
         '../module-74-healthcare-llms/section-74.6.html', '../module-74-healthcare-llms/section-74.5.html'),
        # Sec 76.5 → 77.1 (skip 76.6)
        ('part-12-applications-across-industries/module-76-cybersecurity-llms/section-76.5.html',
         'section-76.6.html', '../module-77-government-llms/section-77.1.html'),
        ('part-12-applications-across-industries/module-77-government-llms/section-77.1.html',
         '../module-76-cybersecurity-llms/section-76.6.html', '../module-76-cybersecurity-llms/section-76.5.html'),
        # Sec 79.1 → 79.3 (skip 79.2)
        ('part-12-applications-across-industries/module-79-creative-industries/section-79.1.html',
         'section-79.2.html', 'section-79.3.html'),
        ('part-12-applications-across-industries/module-79-creative-industries/section-79.3.html',
         'section-79.2.html', 'section-79.1.html'),
        # Sec 30.5 (Agentic Tools last) → Ch 32 (Audio) since 31 deleted
        ('part-6-agentic-ai/module-30-tools-of-the-trade/section-30.5.html',
         '../../part-7-multimodal-generation/module-31-multimodal/section-31.1.html',
         '../../part-7-multimodal-generation/module-32-audio-music-generation/section-32.1.html'),
        # Sec 32.1 (Audio first) → Ch 30 last (since 31 deleted)
        ('part-7-multimodal-generation/module-32-audio-music-generation/section-32.1.html',
         '../module-31-multimodal/section-31.4.html',
         '../../part-6-agentic-ai/module-30-tools-of-the-trade/section-30.5.html'),
        # Sec 40.7 (Robotics last) → Ch 42 (Cross-Modal RAG, since 41 deleted)
        ('part-7-multimodal-generation/module-40-llm-robotics/section-40.7.html',
         '../module-41-world-models-simulation/section-41.1.html',
         '../module-42-cross-modal-reasoning-rag/section-42.1.html'),
        # Sec 42.1 (Cross-Modal RAG first) → Ch 40 last (since 41 deleted)
        ('part-7-multimodal-generation/module-42-cross-modal-reasoning-rag/section-42.1.html',
         '../module-41-world-models-simulation/section-41.8.html',
         '../module-40-llm-robotics/section-40.7.html'),
        # Sec 44.11 → 44.12 (was last → still last, since 45.6 became 44.12)
        ('part-8-evaluation-production/module-44-evaluation-foundations/section-44.11.html',
         '../module-45-testing-quality-gates/section-45.6.html',
         'section-44.12.html'),
        # Sec 46.1 → 44.12 last (since 45.6 became 44.12)
        ('part-8-evaluation-production/module-46-specialized-evaluation/section-46.1.html',
         '../module-45-testing-quality-gates/section-45.6.html',
         '../module-44-evaluation-foundations/section-44.12.html'),
    ]

    n_fixed = 0
    for fp, old_href, new_href in fixes:
        p = ROOT / fp
        if not p.exists(): continue
        text = p.read_text(encoding='utf-8')
        orig = text
        text = text.replace(f'href="{old_href}"', f'href="{new_href}"')
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_fixed += 1
    print(f'Fixed nav in {n_fixed} sibling sections')


def fix_body_refs():
    """Walk every HTML file and rewrite refs to deleted entities."""
    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP: continue
        text = p.read_text(encoding='utf-8')
        orig = text
        for old_suffix, replacement in REWRITES.items():
            # Match href="...PREFIX/OLD_SUFFIX" — keep prefix, swap suffix
            def fix(m):
                href = m.group(1)
                if href.endswith(old_suffix):
                    prefix = href[:-len(old_suffix)]
                    return f'href="{prefix}{replacement}"'
                return m.group(0)
            text = re.sub(r'href="([^"]+)"', fix, text)
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'Fixed body refs in {n_files} files')


def main():
    print('=== WAVE 1.5: nav + body ref repair ===\n')
    fix_nav_in_siblings()
    fix_body_refs()
    print('\nDone.')


if __name__ == '__main__':
    main()
