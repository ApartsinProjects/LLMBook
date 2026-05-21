"""
Update chapter index.html files, prev/next neighboring section nav, and all cross-references
across the book for the 8 new splits.

For each (module_rel, old_basename, a_basename, b_basename):
  - Replace single section-card in module index.html with two cards (A then B).
  - Rewrite prev/next nav in the section BEFORE and AFTER the original.
  - Rewrite hrefs to old basename across all HTML in the book using anchor-aware routing.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOOK = ROOT.parent

SPLITS = [
    # (module_rel, old, a, b, a_title, b_title, a_desc, b_desc, a_badge, b_badge)
    (
        "part-1-llm-building-blocks/module-02-sequence-models-attention",
        "section-2.3.html", "section-2.3a.html", "section-2.3b.html",
        "QKV, Scaled Dot-Product &amp; Causal Masking",
        "Multi-Head Attention, Complexity &amp; Lab",
        "The query-key-value abstraction, scaled dot-product attention, self vs cross attention, and causal masking for autoregressive models.",
        "Multi-head attention, a from-scratch lab, the quadratic complexity problem, and a complete worked example tying it all together.",
        "advanced", "advanced",
    ),
    (
        "part-1-llm-building-blocks/module-03-transformer-architecture",
        "section-3.2.html", "section-3.2a.html", "section-3.2b.html",
        "Build a Transformer: Architecture &amp; Data Prep",
        "Transformer: Training Loop, Shapes &amp; Debugging",
        "Build a decoder-only Transformer from scratch in PyTorch: the model implementation walked through line by line, and the data preparation pipeline.",
        "The training loop, tracing tensor shapes through the network, running the lab end to end, and the bugs every from-scratch Transformer build hits.",
        "basic", "basic",
    ),
    (
        "part-2-understanding-llms/module-07-modern-llm-landscape",
        "section-7.1.html", "section-7.1a.html", "section-7.1b.html",
        "Frontier Models: OpenAI &amp; Anthropic",
        "Frontier: Gemini, Architecture &amp; Benchmarks",
        "The frontier model landscape, OpenAI's GPT-4o and the o-series, and Anthropic's Claude family.",
        "Google's Gemini, second-tier providers, multimodal architectural unification, attention variants, rate limits, the convergence trend, and benchmarking with contamination.",
        "advanced", "advanced",
    ),
    (
        "part-2-understanding-llms/module-09-inference-optimization",
        "section-9.1.html", "section-9.1a.html", "section-9.1b.html",
        "Quantization: Why, Math &amp; Data Types",
        "Quantization: Algorithms, Practice &amp; QAT",
        "Why inference is expensive, the mathematics of quantization, and the data types (INT8, INT4, NF4, FP8) used to store quantized weights.",
        "Post-training quantization algorithms (GPTQ, AWQ, bitsandbytes), calibration, the GGUF format, and quantization-aware training.",
        "advanced", "advanced",
    ),
    (
        "part-2-understanding-llms/module-09-inference-optimization",
        "section-9.4.html", "section-9.4a.html", "section-9.4b.html",
        "Serving Stack &amp; vLLM Deep Dive",
        "Serving Runtimes: SGLang, TGI, TensorRT &amp; Edge",
        "The LLM serving stack and a deep dive into vLLM, the most widely deployed open-source LLM serving framework.",
        "SGLang, TGI, TensorRT-LLM, LMDeploy, Ollama and llama.cpp, edge inference, Triton, framework comparison, benchmarking, and disaggregated inference.",
        "intermediate", "intermediate",
    ),
    (
        "part-4-training-adaptation/module-18-alignment-rlhf-dpo",
        "section-18.2.html", "section-18.2a.html", "section-18.2b.html",
        "DPO: Derivation &amp; Single-Model Alignment",
        "DPO Variants, Datasets &amp; Iterative DPO",
        "The DPO derivation that lets a language model serve as its own reward model, and the single-model alignment objective.",
        "DPO variants (KTO, IPO, ORPO, SimPO), creating and synthesizing preference datasets, practical training considerations, and online and iterative DPO.",
        "advanced", "advanced",
    ),
    (
        "part-6-agentic-ai/module-30-tools-of-the-trade",
        "section-30.2.html", "section-30.2a.html", "section-30.2b.html",
        "Agent Libraries: LangChain &amp; Framework Deep Dive",
        "Multi-Agent Patterns &amp; Topologies",
        "Agent library landscape, LangChain Agents (Legacy), and a deep dive into modern agent frameworks (LangGraph, CrewAI, AutoGen, OpenAI Agents SDK, Semantic Kernel, smolagents, PydanticAI).",
        "The four multi-agent topologies in production (hierarchical, peer / debate, pipeline, competitive) with failure modes and canonical frameworks for each.",
        "", "",  # original has no level-badge
    ),
    (
        "part-8-conversational-ai-with-llms/module-37-conversational-ai",
        "section-37.5.html", "section-37.5a.html", "section-37.5b.html",
        "Long-Term Memory: Vector, MemGPT &amp; Profiles",
        "Memory Consolidation, Evaluation &amp; End-to-End",
        "Long-term memory architectures: vector store memory, MemGPT/Letta self-managing agents, session persistence with user profiles, memory-as-a-service.",
        "Memory consolidation patterns, evaluating memory quality with the right metrics, and an end-to-end example that wires short-term and long-term memory together.",
        "advanced", "advanced",
    ),
]

# Targeted prev/next neighbor rewrites in surrounding sections.
# (file relative to BOOK, current href substring, replacement href)
PREV_NEXT_REWRITES = [
    # 2.2 next -> 2.3a; 3.1b next stays as 3.2 -> 3.2a (cross-chapter)
    ("part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.2.html",
     '<a class="next" href="section-2.3.html"><span class="nav-label">Next</span><span class="nav-num">Section 2.3</span><span class="nav-title">Scaled Dot-Product &amp; Multi-Head Attention</span></a>',
     '<a class="next" href="section-2.3a.html"><span class="nav-label">Next</span><span class="nav-num">Section 2.3a</span><span class="nav-title">QKV, Scaled Dot-Product &amp; Causal Masking</span></a>'),
    # section-2.3 originally had next pointing to module-03/section-3.1a (already-split). The new 2.3b uses this same next.
    # 3.1b next -> 3.2a; 3.3 prev -> 3.2b
    ("part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1b.html",
     '<a class="next" href="section-3.2.html"><span class="nav-label">Next</span><span class="nav-num">Section 3.2</span><span class="nav-title">Build a Transformer from Scratch</span></a>',
     '<a class="next" href="section-3.2a.html"><span class="nav-label">Next</span><span class="nav-num">Section 3.2a</span><span class="nav-title">Build a Transformer: Architecture &amp; Data Prep</span></a>'),
    ("part-1-llm-building-blocks/module-03-transformer-architecture/section-3.3.html",
     '<a class="prev" href="section-3.2.html"><span class="nav-label">Previous</span><span class="nav-num">Section 3.2</span><span class="nav-title">Build a Transformer from Scratch</span></a>',
     '<a class="prev" href="section-3.2b.html"><span class="nav-label">Previous</span><span class="nav-num">Section 3.2b</span><span class="nav-title">Transformer: Training Loop, Shapes &amp; Debugging</span></a>'),
    # 6.9 next -> 7.1a (already there as section-7.1.html); 7.2 prev -> 7.1b
    ("part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html",
     '<a class="next" href="../module-07-modern-llm-landscape/section-7.1.html"><span class="nav-label">Next</span><span class="nav-num">Section 7.1</span><span class="nav-title">Closed-Source Frontier Models</span></a>',
     '<a class="next" href="../module-07-modern-llm-landscape/section-7.1a.html"><span class="nav-label">Next</span><span class="nav-num">Section 7.1a</span><span class="nav-title">Frontier Models: OpenAI &amp; Anthropic</span></a>'),
    ("part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html",
     '<a class="prev" href="section-7.1.html"><span class="nav-label">Previous</span><span class="nav-num">Section 7.1</span><span class="nav-title">Closed-Source Frontier Models</span></a>',
     '<a class="prev" href="section-7.1b.html"><span class="nav-label">Previous</span><span class="nav-num">Section 7.1b</span><span class="nav-title">Frontier: Gemini, Architecture &amp; Benchmarks</span></a>'),
    # Chapter 8 ends -> 9.1a; 9.2 prev -> 9.1b
    # Need to find what previous of 9.1 looks like first (assume it's section-8.last or chapter-prev)
    ("part-2-understanding-llms/module-09-inference-optimization/section-9.2.html",
     '<a class="prev" href="section-9.1.html"><span class="nav-label">Previous</span><span class="nav-num">Section 9.1</span><span class="nav-title">Model Quantization</span></a>',
     '<a class="prev" href="section-9.1b.html"><span class="nav-label">Previous</span><span class="nav-num">Section 9.1b</span><span class="nav-title">Quantization: Algorithms, Practice &amp; QAT</span></a>'),
    # 9.3 next -> 9.4a; 9.5 prev -> 9.4b
    ("part-2-understanding-llms/module-09-inference-optimization/section-9.3.html",
     '<a class="next" href="section-9.4.html"><span class="nav-label">Next</span><span class="nav-num">Section 9.4</span><span class="nav-title">Serving Infrastructure</span></a>',
     '<a class="next" href="section-9.4a.html"><span class="nav-label">Next</span><span class="nav-num">Section 9.4a</span><span class="nav-title">Serving Stack &amp; vLLM Deep Dive</span></a>'),
    ("part-2-understanding-llms/module-09-inference-optimization/section-9.5.html",
     '<a class="prev" href="section-9.4.html"><span class="nav-label">Previous</span><span class="nav-num">Section 9.4</span><span class="nav-title">Serving Infrastructure</span></a>',
     '<a class="prev" href="section-9.4b.html"><span class="nav-label">Previous</span><span class="nav-num">Section 9.4b</span><span class="nav-title">Serving Runtimes: SGLang, TGI, TensorRT &amp; Edge</span></a>'),
    # 18.1 next -> 18.2a; 18.3 prev -> 18.2b
    ("part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html",
     '<a class="next" href="section-18.2.html"><span class="nav-label">Next</span><span class="nav-num">Section 18.2</span><span class="nav-title">DPO &amp; Modern Preference Optimization</span></a>',
     '<a class="next" href="section-18.2a.html"><span class="nav-label">Next</span><span class="nav-num">Section 18.2a</span><span class="nav-title">DPO: Derivation &amp; Single-Model Alignment</span></a>'),
    ("part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.3.html",
     '<a class="prev" href="section-18.2.html"><span class="nav-label">Previous</span><span class="nav-num">Section 18.2</span><span class="nav-title">DPO &amp; Modern Preference Optimization</span></a>',
     '<a class="prev" href="section-18.2b.html"><span class="nav-label">Previous</span><span class="nav-num">Section 18.2b</span><span class="nav-title">DPO Variants, Datasets &amp; Iterative DPO</span></a>'),
    # 30.1 next -> 30.2a; 30.3 prev -> 30.2b
    ("part-6-agentic-ai/module-30-tools-of-the-trade/section-30.1.html",
     '<a class="next" href="section-30.2.html"><span class="nav-label">Next</span><span class="nav-num">Section 30.2</span><span class="nav-title">Libraries &amp; Frameworks</span></a>',
     '<a class="next" href="section-30.2a.html"><span class="nav-label">Next</span><span class="nav-num">Section 30.2a</span><span class="nav-title">Agent Libraries: LangChain &amp; Framework Deep Dive</span></a>'),
    ("part-6-agentic-ai/module-30-tools-of-the-trade/section-30.3.html",
     '<a class="prev" href="section-30.2.html"><span class="nav-label">Previous</span><span class="nav-num">Section 30.2</span><span class="nav-title">Libraries &amp; Frameworks</span></a>',
     '<a class="prev" href="section-30.2b.html"><span class="nav-label">Previous</span><span class="nav-num">Section 30.2b</span><span class="nav-title">Multi-Agent Patterns &amp; Topologies</span></a>'),
    # 37.4 next -> 37.5a; 40.1 prev -> 37.5b (cross-chapter)
    ("part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.4.html",
     '<a class="next" href="section-37.5.html"><span class="nav-label">Next</span><span class="nav-num">Section 37.5</span><span class="nav-title">Long-Term Memory &amp; Self-Managing Architectures</span></a>',
     '<a class="next" href="section-37.5a.html"><span class="nav-label">Next</span><span class="nav-num">Section 37.5a</span><span class="nav-title">Long-Term Memory: Vector, MemGPT &amp; Profiles</span></a>'),
    ("part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.1.html",
     '<a class="prev" href="../module-37-conversational-ai/section-37.5.html"><span class="nav-label">Previous</span><span class="nav-num">Section 37.5</span><span class="nav-title">Long-Term Memory &amp; Self-Managing Architectures</span></a>',
     '<a class="prev" href="../module-37-conversational-ai/section-37.5b.html"><span class="nav-label">Previous</span><span class="nav-num">Section 37.5b</span><span class="nav-title">Memory Consolidation, Evaluation &amp; End-to-End</span></a>'),
]


def update_chapter_indexes():
    """For each split, replace the single section-card with two cards."""
    n = 0
    for module_rel, old, a, b, a_title, b_title, a_desc, b_desc, a_badge, b_badge in SPLITS:
        idx_path = BOOK / module_rel / "index.html"
        text = idx_path.read_text(encoding="utf-8")
        old_num = old.replace("section-", "").replace(".html", "")  # e.g. "2.3"
        a_num = a.replace("section-", "").replace(".html", "")  # e.g. "2.3a"
        b_num = b.replace("section-", "").replace(".html", "")

        # Build the regex to match the entire <li><a class="section-card" href="<old>">...</a></li>
        # It is a multi-line block. Match the open tag through </li>.
        pat = re.compile(
            r'<li><a class="section-card" href="' + re.escape(old) + r'">\s*\n'
            r'<span class="section-num">[^<]+</span>\s*\n'
            r'<span class="section-title">[^<]+</span>\s*\n'
            r'<span class="section-desc">[^<]*</span>\s*\n'
            r'(?:<span class="level-badge [^"]+" title="[^"]+">[^<]+</span>\s*\n)?'
            r'</a></li>',
            re.MULTILINE,
        )

        def make_card(href, num, title, desc, badge):
            parts = [
                f'<li><a class="section-card" href="{href}">',
                f'<span class="section-num">{num}</span>',
                f'<span class="section-title">{title}</span>',
                f'<span class="section-desc">{desc}</span>',
            ]
            if badge:
                badge_title = {"basic": "Entry", "intermediate": "Intermediate", "advanced": "Advanced"}.get(badge, "Entry")
                parts.append(f'<span class="level-badge {badge} " title="{badge_title}">{badge_title}</span>'.replace("  ", " "))
            parts.append('</a></li>')
            return "\n".join(parts)

        a_card = make_card(a, a_num, a_title, a_desc, a_badge)
        b_card = make_card(b, b_num, b_title, b_desc, b_badge)
        replacement = a_card + "\n" + b_card

        new_text, m = pat.subn(replacement, text, count=1)
        if m == 0:
            print(f"  WARN: chapter index card not matched for {module_rel}/{old}")
        else:
            idx_path.write_text(new_text, encoding="utf-8")
            n += m
            print(f"  OK: {module_rel}/index.html  ({old_num} -> {a_num}, {b_num})")
    return n


def apply_prev_next_rewrites():
    n = 0
    for rel, old, new in PREV_NEXT_REWRITES:
        p = BOOK / rel
        if not p.exists():
            print(f"  MISS: file not found: {p}")
            continue
        t = p.read_text(encoding="utf-8")
        if old in t:
            t = t.replace(old, new)
            p.write_text(t, encoding="utf-8")
            n += 1
            print(f"  OK: {rel}")
        else:
            if new in t:
                print(f"  ALREADY: {rel}")
            else:
                print(f"  MISS: {rel} (couldn't find exact old block)")
    return n


def collect_ids(html_path: Path):
    text = html_path.read_text(encoding="utf-8")
    return set(m.group(1) for m in re.finditer(r' id="([^"]+)"', text))


def build_id_maps():
    """For each split, build dict mapping {anchor_id: 'a' or 'b'} (full basename)."""
    maps = {}
    for module_rel, old, a, b, *_ in SPLITS:
        a_path = BOOK / module_rel / a
        b_path = BOOK / module_rel / b
        if not a_path.exists() or not b_path.exists():
            print(f"  WARN: split file missing: {a_path} or {b_path}")
            maps[(module_rel, old)] = {}
            continue
        ids_a = collect_ids(a_path)
        ids_b = collect_ids(b_path)
        m = {}
        for i in ids_a:
            m[i] = a
        for i in ids_b:
            if i not in m:
                m[i] = b
        maps[(module_rel, old)] = m
    return maps


def apply_xref_fixes(maps):
    """Walk the book and rewrite href="...section-X.Y.html" references."""
    book_files = list(BOOK.rglob("*.html"))
    exclude_substrings = ["KDP", "node_modules", "pagefind", "vendor", "_archive"]
    book_files = [f for f in book_files if not any(s in str(f) for s in exclude_substrings)]

    changes = 0
    for f in book_files:
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        orig = text

        for module_rel, old, a, b, *_ in SPLITS:
            id_map = maps[(module_rel, old)]
            pattern = re.compile(r'href="([^"]*?)(' + re.escape(old) + r')(#([^"]+))?"')

            def repl(m):
                prefix = m.group(1)
                hash_part = m.group(3) or ""
                anchor = m.group(4)
                if anchor:
                    new_base = id_map.get(anchor, a)
                else:
                    new_base = a
                return f'href="{prefix}{new_base}{hash_part}"'

            new_text = pattern.sub(repl, text)
            if new_text != text:
                text = new_text

        if text != orig:
            f.write_text(text, encoding="utf-8")
            changes += 1
    return changes


if __name__ == "__main__":
    print("Updating chapter indexes...")
    n1 = update_chapter_indexes()
    print(f"  Updated {n1} chapter index cards.")

    print()
    print("Building ID maps...")
    maps = build_id_maps()
    for k, v in maps.items():
        print(f"  {k[0]}/{k[1]}: {len(v)} ids")

    print()
    print("Applying targeted prev/next block rewrites...")
    n2 = apply_prev_next_rewrites()
    print(f"  Rewrote {n2} prev/next blocks.")

    print()
    print("Applying generic xref rewrites...")
    n3 = apply_xref_fixes(maps)
    print(f"  Rewrote {n3} files.")
