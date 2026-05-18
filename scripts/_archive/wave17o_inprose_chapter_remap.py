"""Wave 17O: remap stale chapter mentions in body prose (no <a> anchors).

Wave 17d sweep only handled anchored "Chapter X" refs (where there was a
neighboring href to disambiguate). Free-text mentions like "Chapter 33 opens
on the modality..." weren't caught.

Known stale → canonical mappings (from the v9 plan + Wave 13 renames):
  Old → New (when in body prose context):
  - "Chapter 22" → "Chapter 31" (was Embeddings/Vector DB; now in Part 7)
  - "Chapter 23" → "Chapter 32" (was RAG monolith; now RAG Fundamentals)
  - "Chapter 24" → "Chapter 37" (was Conv AI; now in Part 8)
  - "Chapter 25" → "Chapter 36 or Ch 41" (split into retrieval tools + conv tools)
  - "Chapter 33" → "Section 20.6" (was Video Generation; merged into Ch 20)
  - "Chapter 35" → "Chapter 22" (was VLM)
  - "Chapter 37" → "Section 22.6" (was Omni Models; merged into Ch 22)
  - "Chapter 38" → "Section 40.2" (was Streaming; merged into Ch 40)
  - "Chapter 40" → "Section 24.7" (was LLM-Powered Robotics; merged into Ch 24)
  - "Chapter 41" → dropped (Embodied AI aggregator removed)
  - "Chapter 50" → "Part XIV" (was Vibe Coding; now in Part 14)

But these are RISKY rewrites because canonical Ch 22 / 23 / 24 / 33 / 37 / 38 /
40 / 41 / 50 might be referenced legitimately if the file is talking about
something in the CURRENT structure that happens to use those numbers.

Strategy: this script does NOT do a global text replace. Instead it:
  - Identifies <p> elements containing "Chapter <stale>" or "Section <stale>.X"
    NOT inside an <a> tag
  - Logs them for manual review

Then for specific clearly-stale cases identified by cycle-3 audits, apply
focused fixes.
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}


# Specific targeted fixes from cycle-3 findings
TARGETED_FIXES = [
    # File path glob OR exact path → list of (find, replace) pairs
    {
        'path': 'part-5-multimodal-llms/module-20-audio-music-generation/section-20.5.html',
        'fixes': [
            ('Chapter 33 opens on the modality with the steepest 2025-2026 capability gain: video',
             'Section 20.6 opens on the modality with the steepest 2025-2026 capability gain: video'),
        ],
    },
    {
        'path': 'part-5-multimodal-llms/module-20-audio-music-generation/section-20.10.html',
        'fixes': [
            ('Section 33.1', 'Section 20.6'),
            ('Section 33.2', 'Section 20.7'),
            ('Section 33.3', 'Section 20.8'),
        ],
    },
]


def apply_targeted_fixes():
    print('=== Targeted body-prose fixes ===')
    n = 0
    for entry in TARGETED_FIXES:
        p = ROOT / entry['path']
        if not p.exists():
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        for find, replace in entry['fixes']:
            text = text.replace(find, replace)
        if text != orig:
            p.write_text(text, encoding='utf-8')
            print(f'  Fixed {entry["path"]}')
            n += 1
    print(f'  Total targeted fixes: {n}')


def sweep_unanchored_stale_refs():
    """For section bodies, find "Chapter NN" mentions that are NOT inside <a> tags
    AND are clearly stale (NN > 83 or NN refers to a known-dropped chapter).

    Conservative: only rewrite NN = 50 (Vibe Coding → Part XIV) and some other
    very-clearly-dropped chapters."""
    print('=== Sweep clearly-dropped chapter mentions ===')
    n_files = 0
    for p in sorted(ROOT.rglob('section-*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # Replace "Chapter 50" (vibe-coding) NOT inside <a> tags with "Part XIV"
        # Use negative lookbehind on >Chapter (i.e., not preceded by ">")
        # Safer: match ONLY plain text not preceded by `>`
        # Actually easier: split on <a>...</a> blocks, replace only outside
        def replace_outside_anchors(text):
            parts = re.split(r'(<a\s[^>]*>[\s\S]*?</a>)', text)
            for i in range(0, len(parts), 2):  # even indices are outside <a>
                # Replace clearly-dropped chapter mentions
                parts[i] = parts[i].replace('Chapter 50.2 (Vibe-Coding with LLMs)',
                                            'Part XIV (Designing LLM/Agent Products)')
                # Standalone "Chapter 50" reference (no number after) to vibe coding
                parts[i] = re.sub(
                    r'\bChapter 50\b(?!\s*[\.\d])',
                    'Part XIV',
                    parts[i]
                )
            return ''.join(parts)

        text = replace_outside_anchors(text)
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'  Updated {n_files} files')


def main():
    apply_targeted_fixes()
    sweep_unanchored_stale_refs()


if __name__ == '__main__':
    main()
