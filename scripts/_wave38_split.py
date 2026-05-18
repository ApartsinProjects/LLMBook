"""Wave 38 GIANT_SECTION splitter.

Splits a long section file at a given h2 boundary into Xa/Xb files.
Preserves: header, epigraph, big-picture, prerequisites, post-content closing.
Adds: chained what's-next callouts (Xa -> Xb, Xb -> next).
Style: no em-dashes, no double-dashes.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def write(p: Path, c: str) -> None:
    p.write_text(c, encoding="utf-8")


def find_h2_positions(content: str) -> list[tuple[int, str, str]]:
    """Return list of (start_pos, raw_h2_tag, plain_text)."""
    results = []
    for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", content, re.DOTALL):
        plain = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        results.append((m.start(), m.group(0), plain))
    return results


def split_section(
    section_path: str,
    split_h2_index: int,  # 0-based index of h2 where Xb starts (this h2 goes into Xb)
    a_title_short: str,  # e.g., "Tokens in Practice: Special Tokens, Templates, Tiktoken"
    a_title_full: str,   # e.g., "Tokens in Practice: Special Tokens, Templates, Tiktoken"
    b_title_short: str,
    b_title_full: str,
    a_desc: str,
    b_desc: str,
    section_num: str,    # e.g., "1.7"
    b_intro_para: str,   # paragraph for Xb framing
    a_whatsnext_para: str,   # paragraph for "What's Next" callout in Xa (points to Xb)
    next_section_in_chapter: str | None,  # e.g., "../module-02-sequence-models-attention/section-2.1.html"
    next_section_label: str | None,       # e.g., "Section 2.1: Why RNNs Couldn't Scale"
    b_whatsnext_para: str,
) -> tuple[int, int]:
    """Execute the split. Returns (a_lines, b_lines)."""
    p = BASE / section_path
    content = read(p)

    h2s = find_h2_positions(content)
    if split_h2_index < 1 or split_h2_index >= len(h2s):
        raise ValueError(f"Bad split index {split_h2_index} for {section_path} (h2 count={len(h2s)})")

    split_pos = h2s[split_h2_index][0]

    # Find the closing structures: research-frontier, whats-next, bibliography, chapter-nav, footer, /main
    # We need to:
    # - extract the head (DOCTYPE through </header><main class="content"...> opener and epigraph+big-picture+prerequisites)
    # - find the end of "preamble" (after big-picture/prerequisites and before first h2)
    # - find the end of "body content" (just before research-frontier)
    # - find the closing tail (research-frontier + whats-next + bibliography + chapter-nav + footer + closing tags)

    # Locate the first h2 (start of content body)
    first_h2_pos = h2s[0][0]

    # Find the position of </main> (closing tag)
    main_close_match = re.search(r"</main>", content)
    if not main_close_match:
        raise ValueError(f"No </main> in {section_path}")
    main_close_pos = main_close_match.start()

    # Find positions of trailing structural elements
    # We want to keep everything from research-frontier (or whatever comes after content) inside both files,
    # but the canonical pattern is: content -> research-frontier -> whats-next -> bibliography -> chapter-nav -> footer -> /main
    # We will fabricate per-file: own whats-next callout + own bibliography? Actually bibliography stays mostly identical.
    # Simpler approach: the "tail" template includes our custom whats-next + bibliography + chapter-nav + footer
    # We keep the original bibliography intact in BOTH files (citations are reference info).

    # Find the start of research-frontier (or whats-next if no rf)
    rf_match = re.search(r'<div class="callout research-frontier">', content)
    wn_match = re.search(r'<div class="callout whats-next">', content)
    bib_match = re.search(r'(<details class="bibliography-collapsible">|<section class="bibliography">)', content)
    nav_match = re.search(r'<nav class="chapter-nav">', content)

    # tail_start: where the original trailing block begins (we will REPLACE the original tail with our own)
    if rf_match:
        tail_start = rf_match.start()
    elif wn_match:
        tail_start = wn_match.start()
    elif bib_match:
        tail_start = bib_match.start()
    else:
        tail_start = main_close_pos

    # Extract the original tail (research-frontier + whats-next + bibliography + chapter-nav + footer)
    # We strip the original whats-next from this tail since each new file needs its OWN whats-next.
    original_tail = content[tail_start:main_close_pos]
    # Remove the original whats-next callout from the tail so we can substitute our own
    original_tail = re.sub(
        r'<div class="callout whats-next">.*?</div>\s*',
        "",
        original_tail,
        flags=re.DOTALL,
        count=1,
    )
    # Also separate research-frontier (keep in both) from the rest
    # We'll keep: research-frontier (if present) + bibliography + chapter-nav + footer
    # And insert our own whats-next BEFORE bibliography

    # Find what's after </main>: the closing script + body + html
    after_main_close = content[main_close_pos:]

    # Compute Xa body: content[first_h2_pos:split_pos]
    a_body = content[first_h2_pos:split_pos].rstrip()
    # Compute Xb body: content[split_pos:tail_start]
    b_body = content[split_pos:tail_start].rstrip()

    # Find the preamble (epigraph + big-picture + prerequisites) — between <main ...> and first h2
    main_open_match = re.search(r'<main class="content" id="main-content">[^<]*(?:<span[^>]*></span>\s*)*', content)
    if not main_open_match:
        raise ValueError(f"No <main> opener in {section_path}")
    # Up to first h2
    head_to_main_close = content[:main_open_match.end()]
    preamble = content[main_open_match.end():first_h2_pos]

    # Build new head for Xa and Xb: rewrite title, meta description, h1, page-current, and chapter-nav at top isn't here, but the
    # h1 (current section title) + "Section X.Y" must change to "Section X.Ya" / "Section X.Yb"

    # Patch helpers
    def patch_head(head: str, suffix: str, title_full: str, desc: str) -> str:
        new_section_num = section_num + suffix
        out = head
        # Update <title>
        out = re.sub(
            r"<title>Section\s+" + re.escape(section_num) + r":[^<]+</title>",
            f"<title>Section {new_section_num}: {title_full}</title>",
            out,
            count=1,
        )
        # Update <meta description>
        out = re.sub(
            r'<meta content="Section\s+' + re.escape(section_num) + r':[^"]+"\s+name="description"/>',
            f'<meta content="Section {new_section_num}: {title_full}. {desc}" name="description"/>',
            out,
            count=1,
        )
        # Update <h1> line and page-current
        out = re.sub(
            r"<h1>[^<]+</h1><div class=\"page-current\">Section\s+" + re.escape(section_num) + r"</div>",
            f"<h1>{title_full}</h1><div class=\"page-current\">Section {new_section_num}</div>",
            out,
            count=1,
        )
        return out

    head_a = patch_head(head_to_main_close, "a", a_title_full, a_desc)
    head_b = patch_head(head_to_main_close, "b", b_title_full, b_desc)

    # Build the trailing tail with custom whats-next
    # We'll have: research-frontier (kept from original_tail) -> our whats-next -> bibliography -> chapter-nav -> footer
    # original_tail currently contains: [rf?] + [bib] + [chapter-nav] + [footer] (whats-next already removed)
    # We need to insert our whats-next right BEFORE the bibliography
    def insert_whatsnext(tail: str, wn_html: str) -> str:
        # find bibliography start
        m = re.search(r'<details class="bibliography-collapsible">|<section class="bibliography">', tail)
        if m:
            return tail[:m.start()] + wn_html + "\n" + tail[m.start():]
        # otherwise insert before chapter-nav
        m = re.search(r'<nav class="chapter-nav">', tail)
        if m:
            return tail[:m.start()] + wn_html + "\n" + tail[m.start():]
        return tail + "\n" + wn_html

    a_section_num = section_num + "a"
    b_section_num = section_num + "b"

    wn_a = f'''<div class="callout whats-next">
<div class="callout-title">What's Next</div>
<p>{a_whatsnext_para} Continue with <a href="section-{b_section_num}.html">Section {b_section_num}: {b_title_full}</a>.</p>
</div>'''

    if next_section_in_chapter and next_section_label:
        wn_b_target = f'<a href="{next_section_in_chapter}">{next_section_label}</a>'
    else:
        wn_b_target = '<a href="index.html">the chapter index</a>'

    wn_b = f'''<div class="callout whats-next">
<div class="callout-title">What's Next</div>
<p>{b_whatsnext_para} Continue with {wn_b_target}.</p>
</div>'''

    tail_a = insert_whatsnext(original_tail, wn_a)
    tail_b = insert_whatsnext(original_tail, wn_b)

    # Patch the chapter-nav inside tail_a so its "next" link points to Xb, and tail_b's "prev" points to Xa.
    def patch_chapternav_a(tail: str) -> str:
        # In Xa, prev should remain the same prev as original; next should point to Xb
        # Find the <a class="next" ...> ... </a> tag inside <nav class="chapter-nav">
        m = re.search(r'(<nav class="chapter-nav">)(.*?)(</nav>)', tail, flags=re.DOTALL)
        if not m:
            return tail
        nav_html = m.group(2)
        # Replace the <a class="next" ...>...</a> block
        nav_html = re.sub(
            r'<a class="next"[^>]*>.*?</a>',
            f'<a class="next" href="section-{b_section_num}.html"><span class="nav-label">Next</span><span class="nav-num">Section {b_section_num}</span><span class="nav-title">{b_title_short}</span></a>',
            nav_html,
            count=1,
            flags=re.DOTALL,
        )
        return tail[:m.start(2)] + nav_html + tail[m.end(2):]

    def patch_chapternav_b(tail: str) -> str:
        m = re.search(r'(<nav class="chapter-nav">)(.*?)(</nav>)', tail, flags=re.DOTALL)
        if not m:
            return tail
        nav_html = m.group(2)
        # prev should point to Xa
        nav_html = re.sub(
            r'<a class="prev"[^>]*>.*?</a>',
            f'<a class="prev" href="section-{a_section_num}.html"><span class="nav-label">Previous</span><span class="nav-num">Section {a_section_num}</span><span class="nav-title">{a_title_short}</span></a>',
            nav_html,
            count=1,
            flags=re.DOTALL,
        )
        return tail[:m.start(2)] + nav_html + tail[m.end(2):]

    tail_a = patch_chapternav_a(tail_a)
    tail_b = patch_chapternav_b(tail_b)

    # Build Xb intro paragraph (insert immediately after preamble, before first h2 of Xb)
    b_intro_html = f'<p class="continuation-intro">{b_intro_para}</p>\n'

    # Compose final files
    a_content = head_a + preamble + a_body + "\n" + tail_a + after_main_close
    b_content = head_b + preamble + b_intro_html + b_body + "\n" + tail_b + after_main_close

    # Write files
    out_dir = p.parent
    a_path = out_dir / f"section-{a_section_num}.html"
    b_path = out_dir / f"section-{b_section_num}.html"
    write(a_path, a_content)
    write(b_path, b_content)

    # Remove original
    p.unlink()

    return (a_content.count("\n"), b_content.count("\n"))


if __name__ == "__main__":
    # Each entry: section_path, split_h2_idx, ... params
    SPLITS = [
        # 1) section-1.7.html — split between h2[2] tiktoken (end of Xa) and h2[3] multilingual fertility (start of Xb)
        {
            "path": "part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html",
            "split_h2_index": 3,
            "section_num": "1.7",
            "a_title_short": "Special Tokens, Chat Templates, and Tiktoken",
            "a_title_full": "Special Tokens, Chat Templates, and Tiktoken",
            "b_title_short": "Multilingual Tokenization, Multimodal Tokens, and Cost Estimation",
            "b_title_full": "Multilingual Tokenization, Multimodal Tokens, and Cost Estimation",
            "a_desc": "Mechanics of special tokens, chat templates, and the tiktoken library for fast BPE encoding.",
            "b_desc": "Fertility differences across languages, multimodal tokenization, and how to budget API costs.",
            "b_intro_para": "Building on the special tokens, chat templates, and tiktoken mechanics from Section 1.7a, this part turns to the practical economics of tokenization across languages and modalities. We measure how unequal tokenizers are in practice, see how images and audio are tokenized for modern multimodal models, and close with a cost estimation framework you can apply to any production API integration.",
            "a_whatsnext_para": "You now know how to recognise special tokens, apply chat templates, and call tiktoken with the right encoding. Next we measure the fairness of these tokenizers across languages, study how images and audio are tokenized, and translate token counts into dollar costs.",
            "next_section_in_chapter": "../module-02-sequence-models-attention/section-2.1.html",
            "next_section_label": "Section 2.1: Why RNNs Couldn't Scale to Modern LLMs",
            "b_whatsnext_para": "You now know how text becomes token IDs in monolingual, multilingual, and multimodal settings, and how to translate tokens into dollar costs. In Chapter 2, you will learn how those token sequences are processed: first by recurrent neural networks that read one token at a time, then by the attention mechanism that lets the model look at all tokens simultaneously.",
        },
        # 2) section-40.6.html — split between h2[3] orchestration challenges (end of Xa) and h2[4] Vision in conversations (start of Xb)
        {
            "path": "part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.6.html",
            "split_h2_index": 4,
            "section_num": "40.6",
            "a_title_short": "Voice AI: STT, TTS, and Real-Time Pipelines",
            "a_title_full": "Voice AI: STT, TTS, and Real-Time Pipelines",
            "b_title_short": "Vision, Speech-to-Speech, and Voice AI Frameworks",
            "b_title_full": "Vision, Speech-to-Speech, and Voice AI Frameworks",
            "a_desc": "Speech-to-text and text-to-speech models, real-time voice pipelines, and voice-specific orchestration challenges.",
            "b_desc": "Vision input in voice conversations, native speech-to-speech models, and a comparison of voice AI orchestration frameworks.",
            "b_intro_para": "Building on the STT, TTS, and real-time pipeline foundations from Section 40.6a, this part extends conversational AI in two directions. First, we add vision so an assistant can see what the user is pointing at. Second, we look at the new wave of native speech-to-speech models that skip the text bottleneck, and we compare the orchestration frameworks (LiveKit, Pipecat, Vocode) that production teams actually deploy.",
            "a_whatsnext_para": "You have now seen the core voice AI stack: STT, TTS, real-time pipelines, and the orchestration challenges they create. Next we add vision to those conversations, study native speech-to-speech models that bypass the text bottleneck, and compare voice AI frameworks for production.",
            "next_section_in_chapter": "../module-41-tools-of-the-trade/section-41.1.html",
            "next_section_label": "Section 41.1 (Chapter 41 opening)",
            "b_whatsnext_para": "You have now surveyed the multimodal and framework landscape for voice and real-time AI. The next chapter walks through the production tooling used to ship these systems end to end.",
        },
        # 3) section-13.5.html — split between h2[4] data contracts (end of Xa) and h2[5] quality filtering (start of Xb)
        {
            "path": "part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html",
            "split_h2_index": 5,
            "section_num": "13.5",
            "a_title_short": "Building Training Datasets: Pipelines, Formatting, and Contracts",
            "a_title_full": "Building Training Datasets: Pipelines, Formatting, and Contracts",
            "b_title_short": "Quality Filtering and Data Mixing Strategies",
            "b_title_full": "Quality Filtering and Data Mixing Strategies",
            "a_desc": "Log-to-dataset pipelines, conversation formatting, preference data, tool-use datasets, and data contracts.",
            "b_desc": "Quality filtering techniques and data mixing strategies for instruction tuning and continued pretraining.",
            "b_intro_para": "Building on the dataset construction patterns from Section 13.5a (log-to-dataset pipelines, conversation formatting, preference data, tool-use datasets, and contracts), this part addresses two operational questions that determine whether a dataset is worth training on. How do we filter out the items that hurt performance, and how do we mix domains so the resulting model is balanced? These two levers (quality filtering and data mixing) often produce larger quality gains than collecting more data.",
            "a_whatsnext_para": "You can now produce a dataset that is well formatted, captures preferences, and is governed by a contract. The next half tackles two questions that decide whether the dataset is worth training on: which items hurt performance and how to blend domains.",
            "next_section_in_chapter": "../module-14-rag-fundamentals/index.html",
            "next_section_label": "Chapter 14: RAG Fundamentals",
            "b_whatsnext_para": "You now understand how to filter for quality and mix domains for balanced learning. In the next chapter, we move from preparing training data to retrieving knowledge at inference time with retrieval-augmented generation.",
        },
        # 4) section-70.3.html — split between h2[3] portable monogamy (end of Xa) and h2[4] multi-provider routing (start of Xb)
        {
            "path": "part-14-designing-llm-agent-products/module-70-shipping-products/section-70.3.html",
            "split_h2_index": 4,
            "section_num": "70.3",
            "a_title_short": "Vendor Lock-in, Continuity, and Portable Monogamy",
            "a_title_full": "Vendor Lock-in, Continuity, and Portable Monogamy",
            "b_title_short": "Multi-Provider Routing and the Portability Checklist",
            "b_title_full": "Multi-Provider Routing and the Portability Checklist",
            "a_desc": "Vendor lock-in versus cognitive lock-in, AI continuity planning, and the portable monogamy strategy.",
            "b_desc": "Multi-provider routing patterns, a portability checklist, an architecture diagram, and common anti-patterns.",
            "b_intro_para": "Building on the conceptual framing from Section 70.3a (vendor lock-in, continuity, and the portable monogamy strategy), this part turns those concepts into production-ready implementations. We work through multi-provider routing patterns, an end-to-end portability checklist, a reference architecture, and the anti-patterns that quietly re-introduce lock-in.",
            "a_whatsnext_para": "You have seen why portability matters and what the portable monogamy strategy looks like at a high level. Next we make the implementation concrete with multi-provider routing, a portability checklist, an architecture diagram, and the anti-patterns to avoid.",
            "next_section_in_chapter": "section-70.4.html",
            "next_section_label": "Section 70.4: Production Evaluation and Continuous Steering",
            "b_whatsnext_para": "You now have an architecture and a checklist for shipping LLM products without locking yourself in. Next we turn to running them in production: drift detection, A/B testing, and the continuous steering loop that keeps quality high.",
        },
        # 5) section-18.1.html — split between h2[2] PPO mechanics (end of Xa) and h2[3] GRPO (start of Xb)
        {
            "path": "part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html",
            "split_h2_index": 3,
            "section_num": "18.1",
            "a_title_short": "The Alignment Problem and RLHF with PPO",
            "a_title_full": "The Alignment Problem and RLHF with PPO",
            "b_title_short": "GRPO, Reward Hacking, and Choosing an Alignment Method",
            "b_title_full": "GRPO, Reward Hacking, and Choosing an Alignment Method",
            "a_desc": "The alignment problem, the three-stage RLHF pipeline, and PPO mechanics for LLM alignment.",
            "b_desc": "GRPO, reward hacking and mitigation, comparison of RLHF/DPO/GRPO, practical tips, and infrastructure at scale.",
            "b_intro_para": "Building on the alignment framing and the PPO pipeline from Section 18.1a, this part moves from the canonical RLHF recipe to the methods now competing with it. We start with GRPO, the group-relative variant that powers many reasoning-trained models, then study reward hacking and its mitigations, compare RLHF, DPO, and GRPO side by side, and close with practical tips and the infrastructure realities at scale.",
            "a_whatsnext_para": "You can now describe the alignment problem, walk through the three-stage RLHF pipeline, and explain PPO's clipped objective. Next we look at GRPO, reward hacking, the practical RLHF/DPO/GRPO trade-offs, and what alignment looks like at production scale.",
            "next_section_in_chapter": "section-18.2a.html",
            "next_section_label": "Section 18.2a (Direct Preference Optimization)",
            "b_whatsnext_para": "You now have a working map of the RL-based alignment landscape, from the choice of objective to the realities of running it at scale. Next we examine Direct Preference Optimization, a simpler offline alternative that has become a strong baseline for many alignment problems.",
        },
        # 6) section-31.2.html — split between h2[2] IVF (end of Xa) and h2[3] PQ (start of Xb)
        {
            "path": "part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.2.html",
            "split_h2_index": 3,
            "section_num": "31.2",
            "a_title_short": "ANN Search: HNSW and IVF",
            "a_title_full": "ANN Search: HNSW and IVF",
            "b_title_short": "Product Quantization, Composite Indexes, and FAISS",
            "b_title_full": "Product Quantization, Composite Indexes, and FAISS",
            "a_desc": "The nearest neighbor problem, HNSW graphs, and IVF inverted file indexes.",
            "b_desc": "Product quantization, composite indexes, index selection guidance, and the FAISS index factory.",
            "b_intro_para": "Building on the nearest neighbor problem and the graph and inverted-list indexes from Section 31.2a, this part adds the compression layer that lets these indexes scale to billions of vectors. Product quantization gives us aggressive memory savings, composite indexes combine the techniques we have seen, and the FAISS index factory provides a single notation for assembling them. We close with selection guidance.",
            "a_whatsnext_para": "You can now navigate an HNSW graph and search an IVF index. Next we add the compression layer that turns these indexes into billion-vector systems: product quantization, composite indexes, FAISS, and the index selection guide.",
            "next_section_in_chapter": "section-31.3.html",
            "next_section_label": "Section 31.3: Vector Databases in Production",
            "b_whatsnext_para": "You can now assemble compressed, composite vector indexes that scale to billions of vectors. The next section moves up the stack from raw indexes to vector databases that add metadata filtering, hybrid search, and operational tooling.",
        },
    ]

    for sp in SPLITS:
        print(f"Splitting {sp['path']} at h2[{sp['split_h2_index']}]...")
        a_lines, b_lines = split_section(
            section_path=sp["path"],
            split_h2_index=sp["split_h2_index"],
            a_title_short=sp["a_title_short"],
            a_title_full=sp["a_title_full"],
            b_title_short=sp["b_title_short"],
            b_title_full=sp["b_title_full"],
            a_desc=sp["a_desc"],
            b_desc=sp["b_desc"],
            section_num=sp["section_num"],
            b_intro_para=sp["b_intro_para"],
            a_whatsnext_para=sp["a_whatsnext_para"],
            next_section_in_chapter=sp["next_section_in_chapter"],
            next_section_label=sp["next_section_label"],
            b_whatsnext_para=sp["b_whatsnext_para"],
        )
        print(f"  -> a={a_lines} lines, b={b_lines} lines")
    print("Done.")
