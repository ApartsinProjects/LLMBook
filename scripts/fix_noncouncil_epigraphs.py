"""
Fix non-council epigraph citations.

Converts plain-text <cite> elements to the wisdom council format
with avatar, link, and agent-desc.

Maps each file's section topic to an appropriate wisdom council agent.
"""

import re
import json
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

# Load agent data
with open(BOOK_ROOT / "scripts" / "wisdom_council_agents.json") as f:
    AGENTS = json.load(f)

# Section-to-agent mapping based on topic
SECTION_AGENT_MAP = {
    # Section 1.3: word embeddings
    "section-1.3": ("lexica", "Analogically Reckless"),
    # Part 5: RAG and conversation
    "section-20.8": ("rag", "Battle-Tested"),
    "section-20.9": ("rag", "Scrupulously Footnoted"),
    "section-21.6": ("echo", "Latency-Conscious"),
    # Part 6: Agents
    "section-22.2": ("agent-x", "Nostalgic but Context-Limited"),
    "section-22.3": ("agent-x", "Pragmatically Planning"),
    "section-22.4": ("agent-x", "Deeply Reasoned"),
    "section-22.5": ("eval", "Rigorously Benchmarked"),
    "section-22.6": ("deploy", "Production-Hardened"),
    "section-22.7": ("kv", "Carefully Curated"),
    # Tool use
    "section-23.1": ("pip", "Schema-Validated"),
    "section-23.2": ("pip", "Protocol-Weary"),
    "section-23.3": ("pip", "Diplomatically Networked"),
    "section-23.4": ("pip", "Defensively Programmed"),
    "section-23.5": ("rag", "Iteratively Augmented"),
    # Multi-agent
    "section-24.1": ("census", "Framework-Fatigued"),
    "section-24.2": ("census", "Hierarchically Orchestrated"),
    "section-24.3": ("census", "Conflict-Resolving"),
    "section-24.4": ("census", "Statefully Orchestrated"),
    "section-24.5": ("census", "Judiciously Supervised"),
    # Specialized agents
    "section-25.1": ("agent-x", "Suspiciously Confident"),
    "section-25.2": ("pixel", "Pixel-Parsing"),
    "section-25.3": ("agent-x", "Cautiously Optimistic"),
    "section-25.4": ("agent-x", "Methodically Analytical"),
    "section-25.5": ("agent-x", "Domain-Adapted"),
    "section-25.6": ("eval", "Humbly Benchmarked"),
    "section-25.7": ("agent-x", "Context-Aware"),
    # Agent safety
    "section-26.1": ("guard", "Paranoid but Prudent"),
    "section-26.2": ("guard", "Carefully Contained"),
    "section-26.3": ("sentinel", "Cost-Conscious"),
    "section-26.4": ("guard", "Resilient Circuit-Breaking"),
    "section-26.5": ("eval", "Thoroughly Tested"),
    "section-26.7": ("guard", "Supply-Chain-Aware"),
}


def get_section_id(filepath):
    """Extract section identifier from filename."""
    name = filepath.stem  # e.g. "section-23.1"
    return name


def build_cite(agent_id, adjective, depth):
    """Build the canonical cite HTML."""
    agent = AGENTS[agent_id]
    root = "/".join([".."] * depth)
    img_path = f"{root}/front-matter/images/agents/{agent['img']}"
    wc_path = f"{root}/front-matter/wisdom-council.html#{agent_id}"
    name = agent["name"]
    color = agent["color"]

    return (
        f'<span class="agent-avatar-inline" style="background-color: {color};">'
        f'<img src="{img_path}" alt="{name}"></span> '
        f'<a href="{wc_path}">{name}</a>, '
        f'<span class="agent-desc">{adjective} AI Agent</span>'
    )


def fix_file(filepath):
    content = filepath.read_text(encoding="utf-8")

    # Check for non-council epigraph
    cite_match = re.search(
        r'<blockquote class="epigraph">\s*<p>(.*?)</p>\s*<cite>(.*?)</cite>',
        content, re.DOTALL
    )
    if not cite_match:
        return False

    cite_text = cite_match.group(2).strip()

    # Skip if already council format
    if "agent-avatar-inline" in cite_text:
        return False

    section_id = get_section_id(filepath)
    if section_id not in SECTION_AGENT_MAP:
        print(f"  SKIPPED (no mapping): {filepath.relative_to(BOOK_ROOT)} - cite: {cite_text[:60]}")
        return False

    agent_id, adjective = SECTION_AGENT_MAP[section_id]

    # Calculate depth
    rel = filepath.relative_to(BOOK_ROOT)
    depth = len(rel.parts) - 1

    new_cite = build_cite(agent_id, adjective, depth)

    # Replace the cite content
    old_cite_full = f"<cite>{cite_text}</cite>"
    new_cite_full = f"<cite>{new_cite}</cite>"
    content = content.replace(old_cite_full, new_cite_full)

    filepath.write_text(content, encoding="utf-8")
    print(f"  FIXED: {filepath.relative_to(BOOK_ROOT)}")
    return True


def main():
    patterns = [
        "part-*/module-*/section-*.html",
        "part-*/module-*/index.html",
    ]

    all_files = []
    for pattern in patterns:
        all_files.extend(BOOK_ROOT.glob(pattern))
    all_files = sorted(set(all_files))

    fixed = 0
    for f in all_files:
        if fix_file(f):
            fixed += 1

    print(f"\nFixed: {fixed} files")

    # Verify
    cite_re = re.compile(r'<cite>(.*?)</cite>', re.DOTALL)
    remaining = 0
    for f in all_files:
        content = f.read_text(encoding="utf-8")
        if 'class="epigraph"' not in content:
            continue
        cites = cite_re.findall(content)
        for c in cites:
            if "agent-avatar-inline" not in c:
                remaining += 1
                print(f"  REMAINING: {f.relative_to(BOOK_ROOT)}: {c.strip()[:60]}")

    print(f"Remaining non-council: {remaining}")


if __name__ == "__main__":
    main()
