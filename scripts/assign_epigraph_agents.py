#!/usr/bin/env python3
"""
Assign Wisdom Council agents to all section epigraphs.

Each section file with a <blockquote class="epigraph"> gets its <cite> block
replaced with a named agent avatar, link, and title. The epigraph quote text
is never changed.
"""

import json
import os
import re
import glob
from collections import defaultdict

ROOT = r"E:\Projects\LLMCourse"
COUNCIL_PATH = os.path.join(ROOT, "front-matter", "wisdom-council.json")

# Load agent data
with open(COUNCIL_PATH, "r", encoding="utf-8") as f:
    council = json.load(f)

AGENTS = {a["id"]: a for a in council["agents"]}

# -------------------------------------------------------------------------
# Section-number to agent-id mapping
# -------------------------------------------------------------------------
# This maps the numeric prefix of a section (e.g. "0", "1", "5.3") to an
# agent id.  More specific keys take priority over less specific ones.
# -------------------------------------------------------------------------
SECTION_AGENT_MAP = {
    # Part 1: Foundations
    "0":  "tensor",
    "1":  "lexica",
    "2":  "token",
    "3":  "attn",
    "4":  "norm",
    "5.1": "greedy",
    "5.2": "greedy",
    "5.3": "spectra",
    "5.4": "spectra",

    # Part 2: Understanding LLMs
    "6":  "scale",
    "7":  "bert",
    "8":  "chinchilla",
    "9":  "quant",

    # Part 3: Working with LLMs
    "10": "pip",
    "11": "prompt",
    "12": "label",

    # Part 4: Training & Adapting
    "13": "synth",
    "14": "finetune",
    "15": "lora",
    "16": "distill",
    "17": "reward",
    "18": "probe",

    # Part 5: Retrieval & Conversation
    "19": "vec",
    "20": "rag",
    "21": "echo",

    # Part 6: Agents & Applications (old numbering)
    "22": "agent-x",
    "23": "pip",
    "24": "census",
    "25": "agent-x",
    "26": "deploy",

    # Part 7: Multimodal / Applications
    "27": "pixel",
    "28": "deploy",

    # Part 8: Evaluation & Production
    "29": "eval",
    "30": "sentinel",
    "31": "deploy",

    # Part 9: Safety & Strategy
    "32": "guard",
    "33": "compass",

    # Part 10: Frontiers
    "34": "frontier",
    "35": "sage",
}

# -------------------------------------------------------------------------
# Path-based overrides: some directories use the same section numbers for
# different topics (old vs new layout).  We resolve by directory name.
# -------------------------------------------------------------------------
DIR_AGENT_OVERRIDES = {
    # Old part-4 modules that got renumbered
    "module-12-synthetic-data":        "synth",
    "module-13-synthetic-data":        "synth",
    "module-13-fine-tuning-fundamentals": "finetune",
    "module-14-fine-tuning-fundamentals": "finetune",
    "module-14-peft":                  "lora",
    "module-15-peft":                  "lora",
    "module-15-distillation-merging":  "distill",
    "module-16-distillation-merging":  "distill",
    "module-16-alignment-rlhf-dpo":    "reward",
    "module-17-alignment-rlhf-dpo":    "reward",
    "module-17-interpretability":      "probe",
    "module-18-interpretability":      "probe",

    # Old part-5 modules
    "module-18-embeddings-vector-db":  "vec",
    "module-19-embeddings-vector-db":  "vec",
    "module-19-rag":                   "rag",
    "module-20-rag":                   "rag",
    "module-20-conversational-ai":     "echo",
    "module-21-conversational-ai":     "echo",

    # Old part-6 agents-applications
    "module-21-ai-agents":             "agent-x",
    "module-22-ai-agents":             "agent-x",
    "module-22-multi-agent-systems":   "census",
    "module-23-multimodal":            "pixel",
    "module-24-llm-applications":      "deploy",
    "module-25-evaluation-observability": "eval",

    # New part-6 agentic-ai
    "module-23-tool-use-protocols":    "pip",
    "module-24-multi-agent-systems":   "census",
    "module-25-specialized-agents":    "agent-x",
    "module-26-agent-safety-production": "guard",

    # Old part-7 production-strategy
    "module-26-production-engineering": "deploy",
    "module-27-safety-ethics-regulation": "guard",
    "module-28-strategy-product-roi":  "compass",

    # New part-7 multimodal-applications
    "module-27-multimodal":            "pixel",
    "module-28-llm-applications":      "deploy",

    # New part-8 evaluation-production
    "module-29-evaluation-observability": "eval",
    "module-30-observability-monitoring": "sentinel",
    "module-31-production-engineering": "deploy",

    # New part-9
    "module-32-safety-ethics-regulation": "guard",
    "module-33-strategy-product-roi":  "compass",

    # New part-10
    "module-34-emerging-architectures": "frontier",
    "module-35-ai-society":            "sage",

    # Part 2 new numbering
    "module-06-pretraining-scaling-laws": "scale",
    "module-07-modern-llm-landscape":  "bert",
    "module-08-reasoning-test-time-compute": "chinchilla",
    "module-08-inference-optimization": "quant",
    "module-09-inference-optimization": "quant",
    "module-09-llm-apis":              "pip",

    # Part 3
    "module-10-prompt-engineering":     "prompt",
    "module-10-llm-apis":              "pip",
    "module-11-prompt-engineering":     "prompt",
    "module-11-hybrid-ml-llm":         "label",
    "module-12-hybrid-ml-llm":         "label",
}

# Front-matter sections get Sage (philosophical advisor)
FRONTMATTER_AGENT = "sage"


def get_relative_path_to_council(filepath):
    """Return the correct relative path from filepath to front-matter/wisdom-council.html."""
    rel = os.path.relpath(filepath, ROOT).replace("\\", "/")
    parts = rel.split("/")

    # front-matter/ files
    if parts[0] == "front-matter":
        return "wisdom-council.html"

    # Root-level files
    if len(parts) == 1:
        return "front-matter/wisdom-council.html"

    # Everything else: count directory depth
    depth = len(parts) - 1  # subtract the filename
    return "/".join([".."] * depth) + "/front-matter/wisdom-council.html"


def resolve_agent_for_file(filepath):
    """Determine which agent should own the epigraph in this file."""
    rel = os.path.relpath(filepath, ROOT).replace("\\", "/")
    parts = rel.split("/")
    filename = parts[-1]

    # Front-matter sections
    if parts[0] == "front-matter":
        return FRONTMATTER_AGENT

    # Extract module directory name for DIR_AGENT_OVERRIDES
    module_dir = None
    for p in parts:
        if p.startswith("module-"):
            module_dir = p
            break

    if module_dir and module_dir in DIR_AGENT_OVERRIDES:
        return DIR_AGENT_OVERRIDES[module_dir]

    # Extract section number from filename: section-X.Y.html
    m = re.match(r"section-(\d+)\.(\d+)\.html", filename)
    if m:
        chapter = m.group(1)
        section = m.group(2)
        # Try specific match first (e.g. "5.3"), then chapter-level (e.g. "5")
        specific_key = f"{chapter}.{section}"
        if specific_key in SECTION_AGENT_MAP:
            return SECTION_AGENT_MAP[specific_key]
        if chapter in SECTION_AGENT_MAP:
            return SECTION_AGENT_MAP[chapter]

    # Fallback for appendix sections or unmatched
    return None


def build_cite_html(agent_id, council_path):
    """Build the new <cite> inner HTML for the given agent."""
    agent = AGENTS[agent_id]
    initial = agent["name"][0].upper()
    color = agent["color"]
    name = agent["name"]
    aid = agent["id"]
    title = agent["title"]

    return (
        f'<cite>'
        f'<span class="agent-avatar-inline" style="background-color: {color};">{initial}</span> '
        f'<a href="{council_path}#{aid}">{name}</a>, '
        f'<span class="agent-desc">{title}</span>'
        f'</cite>'
    )


def process_file(filepath):
    """Process a single file, replacing the cite in its epigraph. Returns True if changed."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Must have an epigraph
    if 'class="epigraph"' not in content:
        return False, None

    agent_id = resolve_agent_for_file(filepath)
    if agent_id is None:
        return False, None

    council_rel = get_relative_path_to_council(filepath)
    new_cite = build_cite_html(agent_id, council_rel)

    # Match the <cite>...</cite> inside the epigraph blockquote.
    # The epigraph pattern: find the blockquote, then replace the cite within it.
    # We use a regex that finds <cite> followed by any content up to </cite>,
    # but only within the epigraph blockquote context.

    # Strategy: find the epigraph block, then replace the cite inside it.
    epigraph_pattern = re.compile(
        r'(<blockquote\s+class="epigraph".*?)'   # everything up to cite
        r'<cite>.*?</cite>'                        # the old cite
        r'(.*?</blockquote>)',                     # rest of blockquote
        re.DOTALL
    )

    match = epigraph_pattern.search(content)
    if not match:
        return False, None

    new_content = content[:match.start()] + match.group(1) + new_cite + match.group(2) + content[match.end():]

    if new_content != content:
        with open(filepath, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)
        return True, agent_id
    return False, agent_id


def main():
    # Find all section HTML files
    patterns = [
        os.path.join(ROOT, "part-*", "module-*", "section-*.html"),
        os.path.join(ROOT, "front-matter", "section-*.html"),
        os.path.join(ROOT, "appendices", "appendix-*", "section-*.html"),
    ]

    all_files = []
    for pat in patterns:
        all_files.extend(glob.glob(pat))

    all_files.sort()
    print(f"Found {len(all_files)} section files total")

    # Count epigraphs
    files_with_epigraphs = []
    files_without_epigraphs = []
    for f in all_files:
        with open(f, "r", encoding="utf-8") as fh:
            if 'class="epigraph"' in fh.read():
                files_with_epigraphs.append(f)
            else:
                files_without_epigraphs.append(f)

    print(f"Files with epigraphs: {len(files_with_epigraphs)}")
    print(f"Files without epigraphs: {len(files_without_epigraphs)}")
    print()

    updated = 0
    skipped = 0
    no_agent = 0
    agent_counts = defaultdict(int)

    for filepath in files_with_epigraphs:
        changed, agent_id = process_file(filepath)
        if changed:
            updated += 1
            agent_counts[agent_id] += 1
        elif agent_id:
            skipped += 1
            agent_counts[agent_id] += 1
        else:
            no_agent += 1
            rel = os.path.relpath(filepath, ROOT).replace("\\", "/")
            print(f"  WARNING: No agent resolved for {rel}")

    print(f"\nResults:")
    print(f"  Updated: {updated}")
    print(f"  Already correct (skipped): {skipped}")
    print(f"  No agent found: {no_agent}")
    print()

    print("Agent assignment counts:")
    for agent_id in sorted(agent_counts.keys()):
        agent = AGENTS[agent_id]
        print(f"  {agent['name']:15s} ({agent_id:15s}): {agent_counts[agent_id]:3d} sections")


if __name__ == "__main__":
    main()
