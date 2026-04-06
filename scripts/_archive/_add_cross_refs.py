"""
Cross-reference hyperlink pass for the LLMCourse textbook.
Adds cross-ref links for key concepts mentioned in sections outside their home chapter.
Only links the first mention per section, avoids code blocks, captions, and nav elements.
Max 5 links per section to avoid link fatigue.
"""

import re
import os
from pathlib import Path

BASE = Path(r"E:\Projects\LLMCourse")

# Concept map: concept_key -> {patterns, home_modules, target_href, display_text}
# home_modules = list of module directory name substrings where we should NOT add links
# target_href = path relative to BASE (we compute relative hrefs from each file)
# Priority order matters: higher-value cross-part links first
CONCEPTS = [
    # === HIGH VALUE: cross-part technique links ===
    {
        "name": "RAG",
        "patterns": [r"(?<![/\w])RAG(?!\w)", r"\b[Rr]etrieval-[Aa]ugmented [Gg]eneration\b"],
        "home_modules": ["module-20-rag", "module-19-rag"],
        "target": "part-5-retrieval-conversation/module-20-rag/section-20.1.html",
        "display": "RAG",
    },
    {
        "name": "fine-tuning",
        "patterns": [r"\bfine-tun(?:e|ing|ed)\b"],
        "home_modules": ["module-14-fine-tuning", "module-13-fine-tuning"],
        "target": "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.1.html",
        "display": "fine-tuning",
    },
    {
        "name": "RLHF",
        "patterns": [r"\bRLHF\b"],
        "home_modules": ["module-17-alignment", "module-16-alignment"],
        "target": "part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html",
        "display": "RLHF",
    },
    {
        "name": "DPO",
        "patterns": [r"(?<!\w)DPO(?!\w)"],
        "home_modules": ["module-17-alignment", "module-16-alignment"],
        "target": "part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.2.html",
        "display": "DPO",
    },
    {
        "name": "LoRA",
        "patterns": [r"\bLoRA\b"],
        "home_modules": ["module-15-peft", "module-14-peft"],
        "target": "part-4-training-adapting/module-15-peft/section-15.1.html",
        "display": "LoRA",
    },
    {
        "name": "QLoRA",
        "patterns": [r"\bQLoRA\b"],
        "home_modules": ["module-15-peft", "module-14-peft"],
        "target": "part-4-training-adapting/module-15-peft/section-15.2.html",
        "display": "QLoRA",
    },
    {
        "name": "chain-of-thought",
        "patterns": [r"\bchain-of-thought\b"],
        "home_modules": ["module-08-reasoning", "module-11-prompt-engineering", "module-10-prompt-engineering"],
        "target": "part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html",
        "display": "chain-of-thought",
    },
    {
        "name": "ReAct",
        "patterns": [r"\bReAct\b"],
        "home_modules": ["module-22-ai-agents", "module-11-prompt-engineering", "module-10-prompt-engineering"],
        "target": "part-3-working-with-llms/module-11-prompt-engineering/section-11.2.html",
        "display": "ReAct",
    },
    {
        "name": "prompt engineering",
        "patterns": [r"\bprompt engineering\b"],
        "home_modules": ["module-11-prompt-engineering", "module-10-prompt-engineering"],
        "target": "part-3-working-with-llms/module-11-prompt-engineering/section-11.1.html",
        "display": "prompt engineering",
    },
    {
        "name": "attention mechanism",
        "patterns": [r"\battention mechanism\b", r"\bself-attention\b", r"\bmulti-head attention\b"],
        "home_modules": ["module-03-sequence-models-attention", "module-04-transformer-architecture"],
        "target": "part-1-foundations/module-03-sequence-models-attention/section-3.2.html",
        "display": "attention mechanism",
    },
    {
        "name": "tokenization",
        "patterns": [r"\b[Tt]okenization\b", r"\b[Tt]okenizer(?:s)?\b"],
        "home_modules": ["module-02-tokenization"],
        "target": "part-1-foundations/module-02-tokenization-subword-models/section-2.1.html",
        "display": "tokenization",
    },
    {
        "name": "vector database",
        "patterns": [r"\bvector databas(?:e|es)\b", r"\bvector stor(?:e|es)\b"],
        "home_modules": ["module-19-embeddings", "module-18-embeddings"],
        "target": "part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.2.html",
        "display": "vector database",
    },
    {
        "name": "quantization",
        "patterns": [r"\bquantization\b"],
        "home_modules": ["module-09-inference", "module-08-inference"],
        "target": "part-2-understanding-llms/module-09-inference-optimization/section-9.2.html",
        "display": "quantization",
    },
    {
        "name": "knowledge distillation",
        "patterns": [r"\bknowledge distillation\b", r"\bmodel distillation\b"],
        "home_modules": ["module-16-distillation", "module-15-distillation"],
        "target": "part-4-training-adapting/module-16-distillation-merging/section-16.1.html",
        "display": "knowledge distillation",
    },
    {
        "name": "MCP",
        "patterns": [r"\bModel Context Protocol\b", r"(?<![/\w])MCP(?!\w)(?! server)"],
        "home_modules": ["module-23-tool-use"],
        "target": "part-6-agentic-ai/module-23-tool-use-protocols/section-23.3.html",
        "display": "MCP",
    },
    {
        "name": "prompt injection",
        "patterns": [r"\bprompt injection\b"],
        "home_modules": ["module-32-safety", "module-11-prompt-engineering"],
        "target": "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.1.html",
        "display": "prompt injection",
    },
    # === MEDIUM VALUE: model and framework references ===
    {
        "name": "transformer",
        "patterns": [r"\b[Tt]ransformer architecture\b"],
        "home_modules": ["module-04-transformer"],
        "target": "part-1-foundations/module-04-transformer-architecture/section-4.1.html",
        "display": "Transformer architecture",
    },
    {
        "name": "LLaMA",
        "patterns": [r"\bLLaMA\b", r"\bLlama[ -][23]\b"],
        "home_modules": ["module-07-modern"],
        "target": "part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html",
        "display": "LLaMA",
    },
    {
        "name": "vLLM",
        "patterns": [r"\bvLLM\b"],
        "home_modules": ["module-09-inference", "module-08-inference"],
        "target": "part-2-understanding-llms/module-09-inference-optimization/section-9.5.html",
        "display": "vLLM",
    },
    {
        "name": "Mamba",
        "patterns": [r"\bMamba\b"],
        "home_modules": ["module-34-emerging"],
        "target": "part-10-frontiers/module-34-emerging-architectures/section-34.1.html",
        "display": "Mamba",
    },
    {
        "name": "HuggingFace",
        "patterns": [r"\bHugging\s*Face\b"],
        "home_modules": ["module-10-llm-apis", "module-09-llm-apis"],
        "target": "part-3-working-with-llms/module-10-llm-apis/section-10.2.html",
        "display": "Hugging Face",
    },
    {
        "name": "LangChain",
        "patterns": [r"\bLangChain\b"],
        "home_modules": ["module-22-ai-agents", "module-23-tool-use", "module-24-multi-agent"],
        "target": "part-6-agentic-ai/module-22-ai-agents/section-22.5.html",
        "display": "LangChain",
    },
    {
        "name": "scaling laws",
        "patterns": [r"\bscaling laws?\b"],
        "home_modules": ["module-06-pretraining"],
        "target": "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html",
        "display": "scaling laws",
    },
    # === LOWER PRIORITY: very common terms, be more selective ===
    {
        "name": "text embeddings",
        "patterns": [r"\btext embeddings?\b", r"\bword embeddings?\b", r"\bsentence embeddings?\b", r"\bembedding model\b", r"\bembedding space\b"],
        "home_modules": ["module-19-embeddings", "module-18-embeddings", "module-01-foundations"],
        "target": "part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.1.html",
        "display": "embeddings",
    },
    {
        "name": "BERT",
        "patterns": [r"\bBERT\b"],
        "home_modules": ["module-06-pretraining", "module-07-modern"],
        "target": "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html",
        "display": "BERT",
    },
]


def compute_relative_path(from_file, to_target):
    """Compute relative href from from_file to to_target (both relative to BASE)."""
    from_dir = Path(from_file).parent
    to_path = Path(to_target)
    try:
        rel = os.path.relpath(to_path, from_dir).replace("\\", "/")
        return rel
    except ValueError:
        return None


def is_in_home_module(filepath, home_modules):
    """Check if filepath is within one of the home module directories."""
    fp = str(filepath).replace("\\", "/")
    for hm in home_modules:
        if hm in fp:
            return True
    return False


def should_skip_file(filepath):
    """Skip index files, appendices, front-matter, agents, etc."""
    fp = str(filepath).replace("\\", "/")
    if "/appendices/" in fp or "/front-matter/" in fp or "/agents/" in fp:
        return True
    if "/capstone/" in fp or "/templates/" in fp or "/_lab_fragments/" in fp:
        return True
    if fp.endswith("/index.html"):
        return True
    return False


def is_in_forbidden_context(html, match_start, match_end):
    """Check if the match position is inside an existing tag or element we should skip."""
    before = html[:match_start]

    # Inside an <a> tag?
    open_a = len(re.findall(r'<a\b', before))
    close_a = len(re.findall(r'</a>', before))
    if open_a > close_a:
        return True

    # Inside forbidden tags?
    forbidden_always = ['code', 'pre', 'figcaption', 'nav', 'header', 'h1', 'h2', 'h3', 'h4',
                        'title', 'cite', 'script', 'style', 'svg', 'text',
                        'button', 'label', 'option', 'select', 'th', 'caption']
    for tag in forbidden_always:
        open_tags = [m.start() for m in re.finditer(rf'<{tag}[\s>]', before)]
        close_tags = [m.start() for m in re.finditer(rf'</{tag}>', before)]
        if open_tags:
            last_open = max(open_tags)
            last_close = max(close_tags) if close_tags else -1
            if last_open > last_close:
                return True

    return False


def is_in_prerequisites(html, pos):
    """Check if position is inside a prerequisites div."""
    prereq_start = html.rfind('class="prerequisites"', 0, pos)
    if prereq_start != -1:
        # Find the closing </div> for this prerequisites block
        depth = 0
        i = prereq_start
        while i < len(html) and i < pos + 500:
            if html[i:i+4] == '<div':
                depth += 1
            elif html[i:i+6] == '</div>':
                depth -= 1
                if depth <= 0:
                    if i < pos:
                        return False  # prerequisites ended before our position
                    return True  # we're inside prerequisites
            i += 1
        # If we're still inside, it means pos is within prerequisites
        if i >= pos:
            return True
    return False


def is_in_epigraph(html, pos):
    """Check if position is inside an epigraph blockquote."""
    epigraph_start = html.rfind('class="epigraph"', 0, pos)
    if epigraph_start != -1:
        blockquote_end = html.find('</blockquote>', epigraph_start)
        if blockquote_end > pos:
            return True
    return False


def is_in_whats_next(html, pos):
    """Check if position is inside a whats-next div."""
    wn_start = html.rfind('class="whats-next"', 0, pos)
    if wn_start != -1:
        div_end = html.find('</div>', wn_start)
        # whats-next divs may have nested divs, but typically short
        if div_end > pos:
            return True
    return False


def add_cross_refs_to_file(filepath_rel, concepts, dry_run=False):
    """Add cross-reference links to a single file. Returns list of changes made."""
    filepath = BASE / filepath_rel
    if not filepath.exists():
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html
    changes = []
    links_added = 0
    MAX_LINKS_PER_FILE = 5

    # Find where <main> content starts
    main_start = html.find('<main')
    if main_start == -1:
        return []

    for concept in concepts:
        if links_added >= MAX_LINKS_PER_FILE:
            break

        # Skip if this file is in the concept's home module
        if is_in_home_module(filepath_rel, concept["home_modules"]):
            continue

        # Check if target file exists
        target_abs = BASE / concept["target"]
        if not target_abs.exists():
            continue

        # Compute relative href
        href = compute_relative_path(filepath_rel, concept["target"])
        if not href:
            continue

        # Check if there's already a cross-ref link to this target in the file
        if href in html:
            continue

        # Check if there's already a cross-ref with the concept name
        display = concept["display"]
        # Check for any existing link containing the concept name
        existing_link_pattern = rf'<a[^>]*>[^<]*{re.escape(display)}[^<]*</a>'
        if re.search(existing_link_pattern, html, re.IGNORECASE):
            continue

        # Try each pattern, find the first unlinked mention in the body
        found = False
        for pattern in concept["patterns"]:
            for match in re.finditer(pattern, html):
                start, end = match.start(), match.end()
                matched_text = match.group()

                # Must be after <main>
                if start < main_start:
                    continue

                # Skip forbidden HTML contexts
                if is_in_forbidden_context(html, start, end):
                    continue

                # Skip prerequisites (they have their own cross-refs)
                if is_in_prerequisites(html, start):
                    continue

                # Skip epigraphs
                if is_in_epigraph(html, start):
                    continue

                # Skip whats-next sections
                if is_in_whats_next(html, start):
                    continue

                # Skip if inside big-picture callout (those often already have cross-refs)
                bp_start = html.rfind('class="callout big-picture"', 0, start)
                if bp_start != -1:
                    bp_end = html.find('</div>', bp_start + 200)
                    if bp_end > start:
                        continue

                # Build the replacement
                link = f'<a class="cross-ref" href="{href}">{matched_text}</a>'
                html = html[:start] + link + html[end:]
                changes.append(f"  {concept['name']}: '{matched_text}' -> {concept['target']}")
                links_added += 1
                found = True
                break  # Only first mention per concept

            if found:
                break

    if html != original and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

    return changes


def get_all_section_files():
    """Get all section HTML files from parts 1-10."""
    parts = [
        "part-1-foundations",
        "part-2-understanding-llms",
        "part-3-working-with-llms",
        "part-4-training-adapting",
        "part-5-retrieval-conversation",
        "part-6-agentic-ai",
        "part-7-multimodal-applications",
        "part-8-evaluation-production",
        "part-9-safety-strategy",
        "part-10-frontiers",
    ]
    files = []
    for part in parts:
        part_dir = BASE / part
        if not part_dir.exists():
            continue
        for html_file in sorted(part_dir.rglob("section-*.html")):
            rel = html_file.relative_to(BASE)
            if not should_skip_file(rel):
                files.append(str(rel).replace("\\", "/"))
    return files


def main():
    files = get_all_section_files()
    print(f"Found {len(files)} section files to process")

    # Verify target files exist
    print("\nVerifying concept targets...")
    for c in CONCEPTS:
        target = BASE / c["target"]
        status = "OK" if target.exists() else "MISSING"
        print(f"  {status}: {c['name']} -> {c['target']}")

    print("\nProcessing files...")
    total_changes = 0
    files_changed = 0
    for filepath_rel in files:
        changes = add_cross_refs_to_file(filepath_rel, CONCEPTS, dry_run=False)
        if changes:
            print(f"\n{filepath_rel}:")
            for change in changes:
                print(change)
            total_changes += len(changes)
            files_changed += 1

    print(f"\nTotal cross-references added: {total_changes}")
    print(f"Files modified: {files_changed}")


if __name__ == "__main__":
    main()
