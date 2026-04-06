"""
Audit sequential navigation links across the entire book.
Checks that every file's "next" and "prev" footer links form a correct chain.
"""

import os
import re
from pathlib import Path

ROOT = Path(r"E:/Projects/LLMCourse")

# ── Build the expected reading order from BOOK_CONFIG ──

# Parts in order, with their chapters (dir names)
PARTS = [
    ("part-1-foundations", [
        "module-00-ml-pytorch-foundations",
        "module-01-foundations-nlp-text-representation",
        "module-02-tokenization-subword-models",
        "module-03-sequence-models-attention",
        "module-04-transformer-architecture",
        "module-05-decoding-text-generation",
    ]),
    ("part-2-understanding-llms", [
        "module-06-pretraining-scaling-laws",
        "module-07-modern-llm-landscape",
        "module-08-reasoning-test-time-compute",
        "module-09-inference-optimization",
        "module-18-interpretability",
    ]),
    ("part-3-working-with-llms", [
        "module-10-llm-apis",
        "module-11-prompt-engineering",
        "module-12-hybrid-ml-llm",
    ]),
    ("part-4-training-adapting", [
        "module-13-synthetic-data",
        "module-14-fine-tuning-fundamentals",
        "module-15-peft",
        "module-16-distillation-merging",
        "module-17-alignment-rlhf-dpo",
    ]),
    ("part-5-retrieval-conversation", [
        "module-19-embeddings-vector-db",
        "module-20-rag",
        "module-21-conversational-ai",
    ]),
    ("part-6-agentic-ai", [
        "module-22-ai-agents",
        "module-23-tool-use-protocols",
        "module-24-multi-agent-systems",
        "module-25-specialized-agents",
        "module-26-agent-safety-production",
    ]),
    ("part-7-multimodal-applications", [
        "module-27-multimodal",
        "module-28-llm-applications",
    ]),
    ("part-8-evaluation-production", [
        "module-29-evaluation-observability",
        "module-30-observability-monitoring",
        "module-31-production-engineering",
    ]),
    ("part-9-safety-strategy", [
        "module-32-safety-ethics-regulation",
        "module-33-strategy-product-roi",
    ]),
    ("part-10-frontiers", [
        "module-34-emerging-architectures",
        "module-35-ai-society",
    ]),
    ("part-11-idea-to-product", [
        "module-36-idea-to-product",
        "module-37-building-steering",
        "module-38-shipping-scaling",
    ]),
]

# Appendices in order
APPENDICES = [
    "appendix-a-mathematical-foundations",
    "appendix-b-ml-essentials",
    "appendix-c-python-for-llm",
    "appendix-d-environment-setup",
    "appendix-e-git-collaboration",
    "appendix-f-glossary",
    "appendix-g-hardware-compute",
    "appendix-h-model-cards",
    "appendix-i-prompt-templates",
    "appendix-j-datasets-benchmarks",
    "appendix-k-huggingface-ecosystem",
    "appendix-l-langchain",
    "appendix-m-langgraph",
    "appendix-n-crewai",
    "appendix-o-llamaindex",
    "appendix-p-semantic-kernel",
    "appendix-q-dspy",
    "appendix-r-experiment-tracking",
    "appendix-s-inference-serving",
    "appendix-t-distributed-ml",
    "appendix-u-docker-containers",
    "appendix-v-tooling-ecosystem",
]

def find_sections(directory):
    """Find all section HTML files in a directory, sorted by number."""
    sections = []
    if not directory.exists():
        return sections
    for f in directory.iterdir():
        if f.name.startswith("section-") and f.name.endswith(".html"):
            sections.append(f.name)
    # Sort by numeric parts
    def sort_key(name):
        # Extract all numbers/letters after "section-"
        parts = name.replace("section-", "").replace(".html", "")
        # Handle patterns like "fm.1", "fm.1a", "0.1", "29.10" etc.
        segments = parts.split(".")
        result = []
        for seg in segments:
            # Try to extract leading number and trailing letters
            m = re.match(r'^(\d+)(.*)', seg)
            if m:
                result.append((0, int(m.group(1)), m.group(2)))
            else:
                result.append((1, 0, seg))
        return result
    sections.sort(key=sort_key)
    return sections


def build_reading_order():
    """Build the complete reading order as a list of absolute paths."""
    order = []

    # Front matter
    fm_dir = ROOT / "front-matter"
    if fm_dir.exists():
        fm_index = fm_dir / "index.html"
        if fm_index.exists():
            order.append(fm_index)
        # Add front-matter sections
        fm_sections = find_sections(fm_dir)
        for s in fm_sections:
            order.append(fm_dir / s)

    # Main parts
    for part_name, chapters in PARTS:
        part_dir = ROOT / part_name
        part_index = part_dir / "index.html"
        if part_index.exists():
            order.append(part_index)

        for ch_name in chapters:
            ch_dir = part_dir / ch_name
            ch_index = ch_dir / "index.html"
            if ch_index.exists():
                order.append(ch_index)

            # Add sections
            sections = find_sections(ch_dir)
            for s in sections:
                order.append(ch_dir / s)

    # Appendices
    app_base = ROOT / "appendices"
    app_index = app_base / "index.html"
    if app_index.exists():
        order.append(app_index)

    for app_name in APPENDICES:
        app_dir = app_base / app_name
        if not app_dir.exists():
            continue
        app_ch_index = app_dir / "index.html"
        if app_ch_index.exists():
            order.append(app_ch_index)
        sections = find_sections(app_dir)
        for s in sections:
            order.append(app_dir / s)

    return order


def extract_nav_links(filepath):
    """Extract prev and next hrefs from footer navigation."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as e:
        return None, None, str(e)

    prev_href = None
    next_href = None

    # Look for <nav class="chapter-nav"> blocks
    # Pattern 1: <a href="..." class="prev">
    # Pattern 2: <a class="prev" href="...">
    # Also handle class="nav-button prev" etc.

    # Find all <a> tags with class containing "prev" or "next"
    a_tags = re.findall(r'<a\s+[^>]*?(?:class\s*=\s*"[^"]*(?:prev|next)[^"]*"|href\s*=\s*"[^"]*")[^>]*>', content, re.IGNORECASE)

    for tag in a_tags:
        href_m = re.search(r'href\s*=\s*"([^"]*)"', tag)
        class_m = re.search(r'class\s*=\s*"([^"]*)"', tag)
        if not href_m or not class_m:
            continue
        href = href_m.group(1)
        cls = class_m.group(1)
        if "prev" in cls and "next" not in cls:
            prev_href = href
        elif "next" in cls:
            next_href = href

    return prev_href, next_href, None


def resolve_href(base_file, href):
    """Resolve a relative href to an absolute path."""
    if not href or href == "#":
        return None
    base_dir = base_file.parent
    resolved = (base_dir / href).resolve()
    return resolved


def main():
    order = build_reading_order()

    print(f"Total files in reading chain: {len(order)}")
    print()

    # Check which files exist
    missing_files = []
    for p in order:
        if not p.exists():
            missing_files.append(p)

    if missing_files:
        print(f"FILES IN EXPECTED ORDER THAT DO NOT EXIST: {len(missing_files)}")
        for p in missing_files:
            print(f"  MISSING: {p.relative_to(ROOT)}")
        print()

    # Check navigation for each file
    no_nav = []
    wrong_next = []
    wrong_prev = []
    correct_next = 0
    correct_prev = 0

    for i, filepath in enumerate(order):
        if not filepath.exists():
            continue

        prev_href, next_href, error = extract_nav_links(filepath)

        if error:
            no_nav.append((filepath, f"Error: {error}"))
            continue

        rel_path = filepath.relative_to(ROOT)

        # Check next link
        if i < len(order) - 1:
            expected_next = order[i + 1]
            if next_href:
                actual_next = resolve_href(filepath, next_href)
                if actual_next and actual_next.resolve() == expected_next.resolve():
                    correct_next += 1
                else:
                    wrong_next.append((
                        str(rel_path),
                        next_href,
                        str(expected_next.relative_to(ROOT)),
                        str(actual_next.relative_to(ROOT)) if actual_next and actual_next.is_relative_to(ROOT) else str(actual_next)
                    ))
            else:
                wrong_next.append((
                    str(rel_path),
                    "(no next link)",
                    str(expected_next.relative_to(ROOT)),
                    "(missing)"
                ))
        else:
            # Last file, should not have a next link (or it could point to something)
            if next_href:
                pass  # Could optionally flag this

        # Check prev link
        if i > 0:
            expected_prev = order[i - 1]
            if prev_href:
                actual_prev = resolve_href(filepath, prev_href)
                if actual_prev and actual_prev.resolve() == expected_prev.resolve():
                    correct_prev += 1
                else:
                    wrong_prev.append((
                        str(rel_path),
                        prev_href,
                        str(expected_prev.relative_to(ROOT)),
                        str(actual_prev.relative_to(ROOT)) if actual_prev and actual_prev.is_relative_to(ROOT) else str(actual_prev)
                    ))
            else:
                wrong_prev.append((
                    str(rel_path),
                    "(no prev link)",
                    str(expected_prev.relative_to(ROOT)),
                    "(missing)"
                ))
        else:
            # First file, should not have prev
            if prev_href:
                pass

        # Check if file has no nav at all
        if prev_href is None and next_href is None:
            no_nav.append((filepath, "No navigation found"))

    print(f"=== NEXT LINK AUDIT ===")
    print(f"Correct next links: {correct_next}")
    print(f"Wrong/missing next links: {len(wrong_next)}")
    print()

    if wrong_next:
        print("WRONG/MISSING NEXT LINKS:")
        for rel_path, current, expected, resolved in wrong_next:
            print(f"  FILE: {rel_path}")
            print(f"    Current next:  {current}")
            print(f"    Resolves to:   {resolved}")
            print(f"    Expected next: {expected}")
            print()

    print(f"=== PREV LINK AUDIT ===")
    print(f"Correct prev links: {correct_prev}")
    print(f"Wrong/missing prev links: {len(wrong_prev)}")
    print()

    if wrong_prev:
        print("WRONG/MISSING PREV LINKS:")
        for rel_path, current, expected, resolved in wrong_prev:
            print(f"  FILE: {rel_path}")
            print(f"    Current prev:  {current}")
            print(f"    Resolves to:   {resolved}")
            print(f"    Expected prev: {expected}")
            print()

    print(f"=== FILES WITH NO NAVIGATION ===")
    print(f"Count: {len(no_nav)}")
    for filepath, reason in no_nav:
        print(f"  {filepath.relative_to(ROOT)}: {reason}")

    print()
    print("=== READING ORDER (for reference) ===")
    for i, p in enumerate(order):
        exists = "OK" if p.exists() else "MISSING"
        print(f"  {i:3d}. [{exists}] {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
