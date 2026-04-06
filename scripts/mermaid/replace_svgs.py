#!/usr/bin/env python3
"""Replace inline SVGs in HTML files with img tags pointing to Mermaid-rendered PNGs.

Archives each original SVG to _archive/replaced-svgs/ before modifying.

Run with: /c/Python314/python scripts/mermaid/replace_svgs.py
"""

import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ARCHIVE_DIR = BASE_DIR / "_archive" / "replaced-svgs"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)


# Each entry: (html_file, svg_index (1-based), img_src, alt_text, archive_name)
REPLACEMENTS = [
    # 1. section-l.1.html: LCEL chain data flow
    {
        "file": "appendices/appendix-l-langchain/section-l.1.html",
        "svg_index": 1,
        "img_src": "images/lcel-chain-data-flow.png",
        "alt": "Data flow through an LCEL chain: PromptTemplate, ChatModel, OutputParser, and Result connected by pipe operators",
        "archive": "section-l.1-lcel-chain.svg",
    },
    # 2. section-l.2.html: RunnableWithMessageHistory
    {
        "file": "appendices/appendix-l-langchain/section-l.2.html",
        "svg_index": 1,
        "img_src": "images/runnable-message-history.png",
        "alt": "RunnableWithMessageHistory flow: User Input through history wrapper, LCEL Chain, to Response, with History Store providing and saving messages",
        "archive": "section-l.2-message-history.svg",
    },
    # 3. section-l.5.html: Agent execution loop
    {
        "file": "appendices/appendix-l-langchain/section-l.5.html",
        "svg_index": 1,
        "img_src": "images/agent-execution-loop.png",
        "alt": "Agent execution loop: User Input to LLM, which calls tools and observes results in a loop, then produces a Final Answer",
        "archive": "section-l.5-agent-loop.svg",
    },
    # 4. section-o.1.html: LlamaIndex ingestion pipeline
    {
        "file": "appendices/appendix-o-llamaindex/section-o.1.html",
        "svg_index": 1,
        "img_src": "images/ingestion-pipeline.png",
        "alt": "LlamaIndex ingestion pipeline: Data Sources to Connectors to Documents to TextNodes in an Index",
        "archive": "section-o.1-ingestion-pipeline.svg",
    },
    # 5. section-6.8.html: Production training architecture
    {
        "file": "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html",
        "svg_index": 1,
        "img_src": "images/production-training-architecture.png",
        "alt": "Production LLM training architecture showing Data Pipeline, Training Framework, Fault Tolerance, Checkpointing, Monitoring, and GPU Cluster layers",
        "archive": "section-6.8-training-architecture.svg",
    },
    # 6. section-7.1.html svg_index 2: Reasoning token flow
    {
        "file": "part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html",
        "svg_index": 2,
        "img_src": "images/reasoning-token-flow.png",
        "alt": "Reasoning token flow: Prompt to Thinking Tokens to Answer Tokens to API Response, with KV Cache impact note",
        "archive": "section-7.1-reasoning-flow.svg",
    },
    # 7. section-7.1.html svg_index 3: Bolt-on vs native multimodal
    {
        "file": "part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html",
        "svg_index": 3,
        "img_src": "images/bolt-on-vs-native-multimodal.png",
        "alt": "Comparison of bolt-on multimodal architecture (separate encoders with adapter) versus native multimodal architecture (unified embedding and transformer stack)",
        "archive": "section-7.1-multimodal-arch.svg",
    },
    # 8. section-15.4.html svg_index 2: PEFT decision flowchart
    {
        "file": "part-4-training-adapting/module-15-peft/section-15.4.html",
        "svg_index": 2,
        "img_src": "images/peft-decision-flowchart.png",
        "alt": "Decision flowchart for choosing PEFT method: Prompt Tuning for 10B+ models, Prefix Tuning for generation tasks, P-Tuning v2 for NLU, and LoRA/QLoRA as the default",
        "archive": "section-15.4-peft-decision.svg",
    },
    # 9. section-22.7.html: Five-layer memory taxonomy
    {
        "file": "part-6-agentic-ai/module-22-ai-agents/section-22.7.html",
        "svg_index": 1,
        "img_src": "images/memory-taxonomy-five-layers.png",
        "alt": "Five-layer agent memory taxonomy with Working Memory at center, surrounded by Episodic, Semantic, Profile, and Retrieval memories",
        "archive": "section-22.7-memory-taxonomy.svg",
    },
]


def find_svg_blocks(html: str):
    """Find all <svg ...>...</svg> blocks and their positions in the HTML."""
    # Match <svg ...>...</svg> accounting for nested elements
    pattern = re.compile(r'<svg\b[^>]*>.*?</svg>', re.DOTALL)
    return list(pattern.finditer(html))


def replace_svg_in_file(spec: dict) -> bool:
    """Replace the nth SVG in the HTML file with an img tag."""
    filepath = BASE_DIR / spec["file"]
    if not filepath.exists():
        print(f"  ERROR: {filepath} not found")
        return False

    html = filepath.read_text(encoding="utf-8")
    svg_matches = find_svg_blocks(html)
    idx = spec["svg_index"] - 1  # Convert 1-based to 0-based

    if idx >= len(svg_matches):
        print(f"  ERROR: Only {len(svg_matches)} SVGs found in {spec['file']}, need index {spec['svg_index']}")
        return False

    match = svg_matches[idx]
    svg_text = match.group(0)

    # Archive the SVG
    archive_path = ARCHIVE_DIR / spec["archive"]
    archive_path.write_text(svg_text, encoding="utf-8")
    print(f"  Archived: {archive_path.name}")

    # Build the replacement img tag
    img_tag = f'<img src="{spec["img_src"]}" alt="{spec["alt"]}" loading="lazy" style="max-width: 100%; height: auto;">'

    # Check if the SVG is wrapped in a <div class="diagram"> and replace accordingly
    # Look at surrounding context to determine the wrapper structure
    start = match.start()
    end = match.end()

    new_html = html[:start] + img_tag + html[end:]

    filepath.write_text(new_html, encoding="utf-8")
    print(f"  Replaced SVG #{spec['svg_index']} in {spec['file']}")
    return True


def main():
    print("=" * 60)
    print("Replacing inline SVGs with Mermaid PNG images")
    print("=" * 60)

    # Process files with multiple replacements in reverse order
    # to maintain correct SVG indices (section-7.1.html has svgs 2 and 3)
    # Sort by file path, then by descending svg_index so later indices are replaced first
    sorted_specs = sorted(REPLACEMENTS, key=lambda s: (s["file"], -s["svg_index"]))

    success = 0
    for spec in sorted_specs:
        print(f"\nProcessing: {spec['file']} (SVG #{spec['svg_index']})")
        if replace_svg_in_file(spec):
            success += 1

    print(f"\n{'=' * 60}")
    print(f"Replaced {success}/{len(REPLACEMENTS)} SVGs successfully.")
    print(f"Archived originals in: {ARCHIVE_DIR}")
    return 0 if success == len(REPLACEMENTS) else 1


if __name__ == "__main__":
    sys.exit(main())
