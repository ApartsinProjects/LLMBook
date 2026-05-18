"""Wave 4: cross-part content moves.

Moves chapters/sections from one part to another. Each move is:
  - git mv the chapter dir or section file
  - rewrite in-file metadata (chapter num, breadcrumb, etc.)
  - update cross-refs across the book

The moves themselves DON'T renumber to final canonical scheme — that's Wave 8.
Wave 4 just gets content into roughly the right parts.

Moves:
  1. Ch 42 (Cross-Modal RAG) from part-7 -> part-5 (Retrieval & Conversation)
     [later will be in new VII Retrieval]
  2. Ch 38 (Streaming Multimodal) from part-7 -> part-5 (Retrieval & Conversation)
     [later will be in new VIII Conversational AI]
  3. Ch 84 (Frontier Hardware) from part-13 -> part-10-llmops
     [later will be in new XII Scale]
  4. Sec 7.6, 7.8 (Distributed Training Systems) from part-2 Ch 7 -> part-10 Ch 61
     [later will be in new XII Scale, as new chapter]
  5. Sec 15.5 (Structured Information Extraction) from part-3 Ch 15 -> part-5 (Retrieval)
     [later: promote to chapter status in new VII Retrieval]
  6. Sec 70.5 (Application Architecture & Deployment) from part-11 Ch 70 -> part-10-llmops
     [later: in LLMOps]
"""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}


def move_chapter_dir(src_path, dst_path):
    """git mv an entire chapter directory."""
    if not src_path.exists():
        print(f'  SKIP {src_path.name}: does not exist')
        return False
    if dst_path.exists():
        print(f'  SKIP {dst_path.name}: target exists')
        return False
    r = subprocess.run(['git', 'mv', str(src_path), str(dst_path)],
                      cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        print(f'  ERR: {r.stderr.strip()}')
        return False
    return True


def update_cross_refs_for_move(old_part, old_mod, new_part, new_mod):
    """When a chapter moves from old_part/old_mod to new_part/new_mod, rewrite refs."""
    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP: continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # Pattern: href="...old_part/old_mod/..." -> "...new_part/new_mod/..."
        text = re.sub(
            rf'(href="[^"]*?){re.escape(old_part)}/{re.escape(old_mod)}/',
            rf'\1{new_part}/{new_mod}/',
            text
        )
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    return n_files


def move1_cross_modal_rag():
    """Ch 42 (Cross-Modal RAG) from part-7 -> part-5."""
    print('--- Move 1: Cross-Modal RAG (Ch 42) part-7 -> part-5 ---')
    src = ROOT / 'part-7-multimodal-generation/module-42-cross-modal-reasoning-rag'
    # Park temporarily in part-5; Wave 8 will reorganize into new VII (Retrieval+IE)
    dst = ROOT / 'part-5-retrieval-conversation/module-42-cross-modal-reasoning-rag'
    if move_chapter_dir(src, dst):
        n = update_cross_refs_for_move(
            'part-7-multimodal-generation', 'module-42-cross-modal-reasoning-rag',
            'part-5-retrieval-conversation', 'module-42-cross-modal-reasoning-rag'
        )
        print(f'  Updated cross-refs in {n} files')


def move2_streaming():
    """Ch 38 (Streaming Multimodal) from part-7 -> part-5.

    Will end up in new VIII (Conversational AI) Ch Voice & Realtime, alongside 24.5.
    """
    print('--- Move 2: Streaming Multimodal (Ch 38) part-7 -> part-5 ---')
    src = ROOT / 'part-7-multimodal-generation/module-38-streaming-realtime-multimodal'
    dst = ROOT / 'part-5-retrieval-conversation/module-38-streaming-realtime-multimodal'
    if move_chapter_dir(src, dst):
        n = update_cross_refs_for_move(
            'part-7-multimodal-generation', 'module-38-streaming-realtime-multimodal',
            'part-5-retrieval-conversation', 'module-38-streaming-realtime-multimodal'
        )
        print(f'  Updated cross-refs in {n} files')


def move3_frontier_hardware():
    """Ch 84 (Frontier Systems & Hardware) from part-13 -> part-10-llmops."""
    print('--- Move 3: Frontier Hardware (Ch 84) part-13 -> part-10-llmops ---')
    src = ROOT / 'part-13-frontiers/module-84-frontier-systems-hardware'
    dst = ROOT / 'part-10-llmops/module-84-frontier-systems-hardware'
    if move_chapter_dir(src, dst):
        n = update_cross_refs_for_move(
            'part-13-frontiers', 'module-84-frontier-systems-hardware',
            'part-10-llmops', 'module-84-frontier-systems-hardware'
        )
        print(f'  Updated cross-refs in {n} files')


def main():
    print('=== WAVE 4: cross-part content moves ===\n')
    move1_cross_modal_rag()
    print()
    move2_streaming()
    print()
    move3_frontier_hardware()
    print()
    print('Wave 4 complete. (Section-level moves 7.6/7.8, 15.5, 70.5, 44.8 deferred to Wave 8 cascade renumber.)')


if __name__ == '__main__':
    main()
