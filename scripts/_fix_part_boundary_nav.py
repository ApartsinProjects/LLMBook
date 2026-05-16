"""Fix Class B (Part landing `next`) and Class C (cross-Part transitions).

Class B: each Part landing (Parts I-XI) has `next` pointing to the next
Part's landing. The convention (followed by Part XII) is that `next`
points to the first chapter of THIS Part.

Class C: at every Part-to-Part boundary, the last section of Part N has
`next` jumping directly to the first chapter of Part N+1, and the first
chapter of Part N+1 has `prev` jumping back to that same last section,
both skipping the Part N+1 landing page. The convention asks the chain
to route THROUGH the Part landing.

Reading-order target after these fixes:
    ...Part N last chapter -> Part N last section
       Part N last section [next] -> Part N+1 landing
       Part N+1 landing [prev] -> Part N last section
       Part N+1 landing [next] -> Part N+1 first chapter index
       Part N+1 first chapter index [prev] -> Part N+1 landing
       Part N+1 first chapter index [next] -> first section of first chapter
       ...

The Front Matter -> Part I transition is also fixed: Part I's first
chapter (module-00) currently has `prev` -> `front-matter/copyright.html`,
which is rewritten to `part-1-foundations/index.html`.

Run from project root:
    python scripts/_fix_part_boundary_nav.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# (part_landing_path, first_chapter_module_basename)
PART_FIRST_CHAPTERS = [
    ("part-1-foundations",                  "module-00-ml-pytorch-foundations"),
    ("part-2-understanding-llms",           "module-06-pretraining-scaling-laws"),
    ("part-3-working-with-llms",            "module-11-llm-apis"),
    ("part-4-training-adapting",            "module-14-synthetic-data"),
    ("part-5-retrieval-conversation",       "module-18-embeddings-vector-db"),
    ("part-6-agentic-ai",                   "module-21-ai-agents"),
    ("part-7-multimodal-applications",      "module-26-multimodal"),
    ("part-8-evaluation-production",        "module-28-evaluation-observability"),
    ("part-9-safety-strategy",              "module-30-safety-ethics-regulation"),
    ("part-10-frontiers",                   "module-33-emerging-architectures"),
    ("part-11-idea-to-product",             "module-34-idea-to-product"),
]


# (last_section_path_relative_to_root, last_section_currently_links_to,
#  next_part_landing, next_part_first_chapter)
# The transitions explicitly enumerated by the audit, Part N -> Part N+1.
CROSS_PART_TRANSITIONS = [
    # Part I -> Part II
    ("part-1-foundations/module-05-decoding-text-generation/section-5.4.html",
     "part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html",
     "part-2-understanding-llms/index.html"),
    # Part II -> Part III
    ("part-2-understanding-llms/module-10-interpretability/section-10.4.html",
     "part-3-working-with-llms/module-11-llm-apis/index.html",
     "part-3-working-with-llms/index.html"),
    # Part III -> Part IV
    ("part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html",
     "part-4-training-adapting/module-14-synthetic-data/index.html",
     "part-4-training-adapting/index.html"),
    # Part IV -> Part V
    ("part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.5.html",
     "part-5-retrieval-conversation/module-18-embeddings-vector-db/index.html",
     "part-5-retrieval-conversation/index.html"),
    # Part V -> Part VI
    ("part-5-retrieval-conversation/module-20-conversational-ai/section-20.5.html",
     "part-6-agentic-ai/module-21-ai-agents/index.html",
     "part-6-agentic-ai/index.html"),
    # Part VI -> Part VII
    ("part-6-agentic-ai/module-25-agent-safety-production/section-25.7.html",
     "part-7-multimodal-applications/module-26-multimodal/index.html",
     "part-7-multimodal-applications/index.html"),
    # Part VII -> Part VIII
    ("part-7-multimodal-applications/module-27-llm-applications/section-27.7.html",
     "part-8-evaluation-production/module-28-evaluation-observability/index.html",
     "part-8-evaluation-production/index.html"),
    # Part VIII -> Part IX
    ("part-8-evaluation-production/module-29-production-engineering/section-29.9.html",
     "part-9-safety-strategy/module-30-safety-ethics-regulation/index.html",
     "part-9-safety-strategy/index.html"),
    # Part IX -> Part X
    ("part-9-safety-strategy/module-31-strategy-product-roi/section-31.7.html",
     "part-10-frontiers/module-33-emerging-architectures/index.html",
     "part-10-frontiers/index.html"),
    # Part X -> Part XI
    ("part-10-frontiers/module-33-emerging-architectures/section-33.11.html",
     "part-11-idea-to-product/module-34-idea-to-product/index.html",
     "part-11-idea-to-product/index.html"),
]


def edit_file(path: Path, old: str, new: str, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        return False
    if dry_run:
        return True
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def fix_class_b(root: Path, dry_run: bool) -> int:
    """Rewrite each Part landing's `next` to point at its first chapter."""
    n = 0
    for part_dir, first_chapter in PART_FIRST_CHAPTERS:
        landing = root / part_dir / "index.html"
        if not landing.exists():
            print(f"  WARN: missing {landing.relative_to(root)}")
            continue
        # The current `next` in Part N landing points to the NEXT Part landing.
        # Match the line by class="next" + part-(N+1) pattern.
        text = landing.read_text(encoding="utf-8")
        m = re.search(
            r'<a class="next" href="(\.\./part-\d+-[a-z\-]+/index\.html)">[^<]*</a>',
            text,
        )
        if not m:
            print(f"  WARN: no 'next -> next part' link found in {landing.relative_to(root)}")
            continue
        old_href = m.group(1)
        new_href = f"{first_chapter}/index.html"
        # Replacement text and label
        new_link = f'<a class="next" href="{new_href}">Chapter {_chapter_num(first_chapter)} &#8594;</a>'
        old_link = m.group(0)
        if dry_run:
            print(f"  [B] {landing.relative_to(root)}: '{old_href}' -> '{new_href}'")
        else:
            landing.write_text(text.replace(old_link, new_link, 1), encoding="utf-8")
            print(f"  [B] {landing.relative_to(root)}: 'next' -> '{new_href}'")
        n += 1
    return n


def _chapter_num(module_basename: str) -> str:
    """`module-06-pretraining-scaling-laws` -> `06`."""
    return module_basename.split("-")[1]


def fix_class_c(root: Path, dry_run: bool) -> int:
    """Route every Part-to-Part transition through the Part N+1 landing.

    For each transition:
      - In last-section-of-Part-N: rewrite `next` href so it points at the
        Part N+1 landing instead of Part N+1's first chapter directly.
      - In first-chapter-of-Part-N+1 index: rewrite `prev` href so it points
        at its own Part landing instead of Part N's last section.
    """
    n = 0
    for last_section_rel, current_next_target, next_part_landing in CROSS_PART_TRANSITIONS:
        # ---- Edit 1: last section's `next`
        last_section = root / last_section_rel
        if not last_section.exists():
            print(f"  WARN: missing {last_section_rel}")
            continue
        last_text = last_section.read_text(encoding="utf-8")
        # Build the relative path from last_section's dir up to next_part_landing
        depth = last_section_rel.count("/")
        new_href = "../" * depth + next_part_landing
        # Match the existing `class="next"` with the chapter-target href
        # which is `../../part-(N+1)/module-XX/index.html`
        old_pattern = re.compile(
            r'(<a class="next" href=")([^"]*' + re.escape(current_next_target.split("/", 1)[1]) + r')(">)',
            re.DOTALL,
        )
        # Simpler approach: match the full current_next_target as a suffix
        # The href in the file is some relative path ending in current_next_target
        current_suffix = current_next_target.rsplit("/", 2)
        # Just locate the literal href value in text
        m = re.search(r'<a class="next" href="([^"]+)">', last_text)
        if not m:
            print(f"  WARN: no next link in {last_section_rel}")
            continue
        current_href = m.group(1)
        # Reconstruct expected new href
        # current is e.g. ../../part-2-understanding-llms/module-06-.../index.html
        # we want ../../part-2-understanding-llms/index.html
        # Drop the module-* segment.
        new_href = re.sub(r"/module-[^/]+/index\.html$", "/index.html", current_href)
        if new_href == current_href:
            print(f"  SKIP (already routes via landing): {last_section_rel}")
        else:
            # Replace the href value, leave link text as-is.
            new_text = last_text.replace(
                f'<a class="next" href="{current_href}">',
                f'<a class="next" href="{new_href}">',
                1,
            )
            # Also update the link's visible text to point at the Part, not a chapter.
            # The label is right after the href and before </a>.
            # Find the part number from new_href
            part_match = re.search(r"part-(\d+)-", new_href)
            part_num = part_match.group(1) if part_match else "?"
            # Rewrite link text: look for current `[^<]*` between this href tag and </a>
            new_text = re.sub(
                r'(<a class="next" href="' + re.escape(new_href) + r'">)[^<]*(</a>)',
                lambda mm: f'{mm.group(1)}Part {_roman(part_num)} &#8594;{mm.group(2)}',
                new_text,
                count=1,
            )
            if dry_run:
                print(f"  [C-last] {last_section_rel}: next '{current_href}' -> '{new_href}'")
            else:
                last_section.write_text(new_text, encoding="utf-8")
                print(f"  [C-last] {last_section_rel}: next -> '{new_href}'")
            n += 1

        # ---- Edit 2: first chapter of next part's `prev`
        first_chapter_index = root / current_next_target
        if not first_chapter_index.exists():
            print(f"  WARN: missing {current_next_target}")
            continue
        fc_text = first_chapter_index.read_text(encoding="utf-8")
        m = re.search(r'<a class="prev" href="([^"]+)">', fc_text)
        if not m:
            print(f"  WARN: no prev link in {current_next_target}")
            continue
        current_prev = m.group(1)
        new_prev = "../index.html"
        if current_prev == new_prev:
            print(f"  SKIP (prev already routes to landing): {current_next_target}")
        else:
            new_text = fc_text.replace(
                f'<a class="prev" href="{current_prev}">',
                f'<a class="prev" href="{new_prev}">',
                1,
            )
            part_match = re.search(r"part-(\d+)-", current_next_target)
            part_num = part_match.group(1) if part_match else "?"
            new_text = re.sub(
                r'(<a class="prev" href="' + re.escape(new_prev) + r'">)[^<]*(</a>)',
                lambda mm: f'{mm.group(1)}&#8592; Part {_roman(part_num)}{mm.group(2)}',
                new_text,
                count=1,
            )
            if dry_run:
                print(f"  [C-first] {current_next_target}: prev '{current_prev}' -> '{new_prev}'")
            else:
                first_chapter_index.write_text(new_text, encoding="utf-8")
                print(f"  [C-first] {current_next_target}: prev -> '{new_prev}'")
            n += 1
    return n


def fix_part1_first_chapter(root: Path, dry_run: bool) -> int:
    """Part I's first chapter `prev` -> Part I landing (was: copyright)."""
    path = root / "part-1-foundations" / "module-00-ml-pytorch-foundations" / "index.html"
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    m = re.search(r'<a class="prev" href="([^"]+)">', text)
    if not m:
        return 0
    current = m.group(1)
    new = "../index.html"
    if current == new:
        print(f"  SKIP Part I first chapter prev (already correct)")
        return 0
    new_text = text.replace(
        f'<a class="prev" href="{current}">',
        f'<a class="prev" href="{new}">',
        1,
    )
    new_text = re.sub(
        r'(<a class="prev" href="' + re.escape(new) + r'">)[^<]*(</a>)',
        lambda mm: f'{mm.group(1)}&#8592; Part I: Foundations{mm.group(2)}',
        new_text,
        count=1,
    )
    if dry_run:
        print(f"  [C-front] part-1-foundations/module-00-.../index.html: "
              f"prev '{current}' -> '{new}'")
    else:
        path.write_text(new_text, encoding="utf-8")
        print(f"  [C-front] part-1-foundations/module-00-.../index.html: prev -> '{new}'")
    return 1


def _roman(part_num: str) -> str:
    table = {
        "1": "I", "2": "II", "3": "III", "4": "IV", "5": "V",
        "6": "VI", "7": "VII", "8": "VIII", "9": "IX", "10": "X",
        "11": "XI", "12": "XII",
    }
    return table.get(part_num, part_num)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if not (root / "toc.html").exists():
        print(f"error: toc.html not found in {root}", file=sys.stderr)
        return 1
    print("=== Class B: Part landings 'next' -> own first chapter ===")
    n_b = fix_class_b(root, args.dry_run)
    print()
    print("=== Class C: route cross-Part transitions through landings ===")
    n_c = fix_class_c(root, args.dry_run)
    n_c += fix_part1_first_chapter(root, args.dry_run)
    print()
    print(f"TOTAL changes: B={n_b}, C={n_c}")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
