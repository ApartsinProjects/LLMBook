"""Move misplaced "second illustration" figures from chapter-opener stack
to their semantically-correct subsection.

Root cause: an early illustration-insertion script batched all body
illustrations near the section's prerequisites block instead of placing
each one next to the prose it illustrates. Result: each affected
section opens with the proper chapter-opener cartoon followed
immediately by an unrelated body illustration, then the actual h2
"X.Y.1" begins with no breathing room.

This script applies 7 specific relocations identified by manual review.
Each move:
  1. Locates the misplaced <figure>...</figure> block
  2. Removes it from its current spot
  3. Inserts it immediately after the target heading

After running, _v655_find_adjacent_figures.py should report only
intentional pairs (chapter-opener + technical-diagram, like Wave 10's
evol-instruct + operators figure).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Each move:
#   path: section file
#   img_marker: substring inside the misplaced <img alt="..."> to find it
#   target_heading: substring of the <h2>/<h3> tag to insert after
MOVES = [
    {
        'path': 'part-5-retrieval-conversation/module-17-embeddings-vector-db/section-17.3.html',
        'img_marker': 'metadata-filtering-bouncer.png',
        'target_heading': '<h2>17.3.5 Metadata Filtering</h2>',
    },
    {
        'path': 'part-5-retrieval-conversation/module-17-embeddings-vector-db/section-17.4.html',
        'img_marker': 'chunking-sushi-chef.png',
        'target_heading': '<h3>Semantic Chunking</h3>',
    },
    {
        'path': 'part-5-retrieval-conversation/module-17-embeddings-vector-db/section-17.5.html',
        'img_marker': 'late-interaction-judges.png',
        'target_heading': '<h3>MaxSim: Late Interaction Scoring</h3>',
    },
    {
        'path': 'part-5-retrieval-conversation/module-18-rag/section-18.2.html',
        'img_marker': 'reranking-judges-panel.png',
        'target_heading': '<h2>18.2.3 Re-Ranking with Cross-Encoders</h2>',
    },
    {
        'path': 'part-7-multimodal-applications/module-25-multimodal/section-25.1.html',
        'img_marker': 'diffusion-restoration.png',
        'target_heading': '<h2>25.1.1 Diffusion Models for Image Generation</h2>',
    },
    {
        'path': 'part-5-retrieval-conversation/module-17-embeddings-vector-db/section-17.1.html',
        'img_marker': 'contrastive-learning-magnets.png',
        'target_heading': '<h2>17.1.2 Training Embedding Models: Contrastive Learning</h2>',
    },
    {
        'path': 'part-4-training-adapting/module-13-synthetic-data/section-13.2.html',
        'img_marker': 'prompt-template-cookie-cutter.png',
        'target_heading': '<h3>13.2.1.1 The Self-Instruct Pipeline</h3>',
    },
]


def relocate_one(text: str, img_marker: str, target_heading: str) -> tuple[str, bool, str]:
    """Move the <figure> containing img_marker to immediately after target_heading.

    Returns (new_text, changed, message).
    """
    # Match the entire <figure class="illustration">...</figure> block that
    # contains the marker. Use a non-greedy block match.
    pattern = re.compile(
        r'(<figure[^>]*>\s*<img[^>]*' + re.escape(img_marker) + r'[^>]*>'
        r'\s*<figcaption>[^<]*(?:<[^>]*>[^<]*)*</figcaption>\s*</figure>)\s*\n?',
        re.MULTILINE,
    )
    m = pattern.search(text)
    if not m:
        return text, False, f'figure block for {img_marker} not found'

    figure_block = m.group(1)
    # Remove the figure (and the trailing newline)
    text_no_fig = text[: m.start()] + text[m.end():]

    # Find the target heading line and insert the figure after the next <p>
    # (or right after the heading if no <p>). Also add a leading newline for
    # readability.
    if target_heading not in text_no_fig:
        return text, False, f'target heading not found: {target_heading}'
    insert_at = text_no_fig.find(target_heading) + len(target_heading)
    # Ensure we land at end of that line
    nl = text_no_fig.find('\n', insert_at)
    if nl == -1:
        return text, False, 'unexpected end of file at heading'

    new_text = (text_no_fig[: nl + 1]
                + figure_block + '\n'
                + text_no_fig[nl + 1:])
    return new_text, True, f'moved {img_marker} to after {target_heading}'


def main() -> int:
    n_done = 0
    for move in MOVES:
        p = ROOT / move['path']
        if not p.exists():
            print(f'SKIP (missing): {move["path"]}')
            continue
        text = p.read_text(encoding='utf-8')
        new_text, changed, msg = relocate_one(text, move['img_marker'], move['target_heading'])
        if changed:
            p.write_text(new_text, encoding='utf-8')
            print(f'OK  {move["path"]}: {msg}')
            n_done += 1
        else:
            print(f'NO  {move["path"]}: {msg}')
    print(f'\nApplied {n_done}/{len(MOVES)} relocations.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
