"""v6.48c: Drop the linear-step diagrams that add no pedagogical value.

For each chosen diagram, this script:
  1. Removes the <figure>...</figure> block containing the <img> reference
     from each HTML page where it appears.
  2. Deletes the .mmd, .png, and .svg files in module's images/ dir.

Per-diagram triage decision (made manually after reviewing each .mmd's
node labels and the surrounding section prose):

DROP — pure step-list, prose says the same thing:
  - fig-2.2.6-bpe-merges  (Step 0..4 boxes of BPE merges; prose lists the
    same merges explicitly)
  - fig-1.2.1-nlp-pipeline (Raw->Normalize->Tokenize->StopWords->Stem->
    Features; pure label sequence)
  - fig-7.1.3-reasoning-token-flow (Prompt->Thinking->Answer->API; trivial)

DROP (redundant with matplotlib version):
  - fig-6.4.3-data-pipeline (the matplotlib curation funnel
    fig-6.4.3-curation-funnel.png is in the same section and is richer)
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Each entry: image basename (without extension or extra suffix)
DROPS = [
    ('part-1-foundations/module-02-tokenization-subword-models', 'fig-2.2.6-bpe-merges'),
    ('part-1-foundations/module-01-foundations-nlp-text-representation', 'fig-1.2.1-nlp-pipeline'),
    ('part-2-understanding-llms/module-07-modern-llm-landscape',
     'fig-7.1.3-reasoning-token-flow-in-inference-time-compute-models-think'),
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws', 'fig-6.4.3-data-pipeline'),
]


def remove_figure_from_html(html_path: Path, img_basename: str) -> bool:
    """Remove the <figure>...</figure> wrapping the <img src=".../<basename>.*">
    from html_path. Returns True if removed."""
    text = html_path.read_text(encoding='utf-8')
    original = text
    # Pattern: <figure ...>...<img ... src="...<basename>..."...>...</figure>
    fig_re = re.compile(
        rf'(\n?\s*<figure[^>]*>.*?<img[^>]*src="[^"]*{re.escape(img_basename)}[^"]*"[^>]*/?>.*?</figure>\s*)',
        re.DOTALL,
    )
    new_text = fig_re.sub('\n', text)
    # Also handle the case where the image lives in a <div class="diagram-container">
    # or a bare <img> + <div class="diagram-caption">
    if new_text == text:
        bare_re = re.compile(
            rf'(\n?\s*<img[^>]*src="[^"]*{re.escape(img_basename)}[^"]*"[^>]*/?>'
            rf'\s*<div class="diagram-caption">.*?</div>\s*)',
            re.DOTALL,
        )
        new_text = bare_re.sub('\n', text)
    if new_text == text:
        # Just delete the bare <img>
        bare_img = re.compile(
            rf'(\n?\s*<img[^>]*src="[^"]*{re.escape(img_basename)}[^"]*"[^>]*/?>\s*)'
        )
        new_text = bare_img.sub('\n', text)
    if new_text == original:
        return False
    html_path.write_text(new_text, encoding='utf-8')
    return True


def main() -> int:
    removed_files = 0
    rewrote_html = 0
    for dir_rel, basename in DROPS:
        mod_dir = ROOT / dir_rel
        # Delete .mmd, .png, .svg, .png.bak* matching basename
        img_dir = mod_dir / 'images'
        for ext in ('.mmd', '.png', '.svg'):
            f = img_dir / f'{basename}{ext}'
            if f.exists():
                f.unlink()
                removed_files += 1
                print(f'  deleted: {f.relative_to(ROOT)}')
        # Find and rewrite every HTML page in the module that references it
        for html_path in mod_dir.glob('*.html'):
            if remove_figure_from_html(html_path, basename):
                rewrote_html += 1
                print(f'  stripped from: {html_path.relative_to(ROOT)}')

    print(f'\nDeleted {removed_files} image files.')
    print(f'Rewrote {rewrote_html} HTML pages.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
