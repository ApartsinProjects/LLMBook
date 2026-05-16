#!/usr/bin/env python3
"""
P0 fixes for cross-link-integrity-audit.md - mismatched topic/destination.
Re-target hrefs (and sometimes anchor text) based on audit analysis.

Skips files modified in the last 10 minutes (in-flight from other agents).
"""
from __future__ import annotations

import re
import time
from pathlib import Path

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
NOW = time.time()
WINDOW = 10 * 60

IN_FLIGHT: set[Path] = set()
for p in ROOT.rglob("*.html"):
    try:
        if NOW - p.stat().st_mtime < WINDOW:
            IN_FLIGHT.add(p.resolve())
    except OSError:
        pass

stats: dict[str, int] = {}
files_modified: set[str] = set()
files_skipped: set[str] = set()
errors: list[str] = []


def add(k: str, n: int = 1):
    stats[k] = stats.get(k, 0) + n


def replace_in_file(path: Path, pattern: str, replacement, label: str, flags=0) -> int:
    if not path.exists():
        errors.append(f"missing: {path}")
        return 0
    if path.resolve() in IN_FLIGHT:
        files_skipped.add(str(path))
        return 0
    text = path.read_text(encoding="utf-8")
    new, n = re.subn(pattern, replacement, text, flags=flags)
    if n > 0:
        path.write_text(new, encoding="utf-8")
        files_modified.add(str(path))
        add(label, n)
    return n


def retarget_links(path: Path, old_href_pattern: str, new_href: str, expected_anchor_text: str | None, label: str) -> int:
    """Find <a ...href="OLD_HREF"...>ANCHOR_TEXT</a> and rewrite href."""
    if not path.exists():
        errors.append(f"missing: {path}")
        return 0
    if path.resolve() in IN_FLIGHT:
        files_skipped.add(str(path))
        return 0
    text = path.read_text(encoding="utf-8")
    if expected_anchor_text:
        # Match <a ... href="...module-X..." ...>EXACT_TEXT</a> and replace href
        pattern = rf'(<a[^>]*?href=")({old_href_pattern})(")([^>]*>)({re.escape(expected_anchor_text)})(</a>)'
    else:
        pattern = rf'(<a[^>]*?href=")({old_href_pattern})(")'
    new_text, n = re.subn(
        pattern,
        lambda m: m.group(1) + new_href + m.group(3) + (m.group(4) + m.group(5) + m.group(6) if expected_anchor_text else ""),
        text,
    )
    if n > 0:
        path.write_text(new_text, encoding="utf-8")
        files_modified.add(str(path))
        add(label, n)
    return n


# ============================================================
# P0: "Hugging Face" -> Appendix C
# Affected: 33 occurrences across many files
# Re-target href to ../../appendices/appendix-c-huggingface-ecosystem/index.html
# Anchor text stays "Hugging Face" or "HuggingFace"
# ============================================================

# Match links whose href ends with module-13-llm-apis/section-13.2.html OR
# module-18-fine-tuning-fundamentals/section-18.5.html, with text "Hugging Face" or "HuggingFace"

for html_path in ROOT.rglob("*.html"):
    if html_path.resolve() in IN_FLIGHT:
        continue
    text = html_path.read_text(encoding="utf-8")
    orig = text

    # The audit cited specific URLs:
    #   ../../part-3-working-with-llms/module-13-llm-apis/section-13.2.html  -> wrong: that's Structured Output
    #   ../../part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.5.html -> Fine-Tuning for Repr Learning
    # Re-point to appendix-c.
    # Compute relative path from html_path to appendix-c/index.html

    target_abs = ROOT / "appendices/appendix-c-huggingface-ecosystem/index.html"
    try:
        rel = Path(target_abs).relative_to(html_path.parent) if False else None
    except Exception:
        rel = None
    # Build relative path manually
    src_parts = html_path.parent.resolve().relative_to(ROOT).parts
    target_parts = target_abs.resolve().relative_to(ROOT).parts
    up = "../" * len(src_parts)
    rel_target = up + "/".join(target_parts)

    # Pattern 1: Anchor text exactly "Hugging Face" or "HuggingFace" with href to module-13-llm-apis/section-13.2.html
    for bad_href_suffix in [
        "module-13-llm-apis/section-13.2.html",
        "module-18-fine-tuning-fundamentals/section-18.5.html",
    ]:
        pattern = re.compile(
            r'(<a[^>]*?href=")([^"]*' + re.escape(bad_href_suffix) + r')("[^>]*>)(Hugging\s?Face|HuggingFace)(</a>)',
            re.IGNORECASE | re.DOTALL,
        )
        def repl(m):
            return m.group(1) + rel_target + m.group(3) + m.group(4) + m.group(5)
        text, n = pattern.subn(repl, text)
        if n:
            add("p0_huggingface_retarget", n)

    if text != orig:
        html_path.write_text(text, encoding="utf-8")
        files_modified.add(str(html_path))


# ============================================================
# P0: "structured output" / "structured outputs" -> section-13.2.html
# Currently incorrectly pointing at section-13.3.html (API Engineering Best Practices)
# ============================================================

for html_path in ROOT.rglob("*.html"):
    if html_path.resolve() in IN_FLIGHT:
        continue
    text = html_path.read_text(encoding="utf-8")
    orig = text

    # Pattern: <a href="...module-13-llm-apis/section-13.3.html"...>structured output(s)</a>
    pattern = re.compile(
        r'(<a[^>]*?href=")([^"]*module-13-llm-apis/section-13\.3\.html)("[^>]*>)((?:S|s)tructured\s+outputs?)(</a>)',
        re.DOTALL,
    )
    def repl_so(m):
        new_href = m.group(2).replace("section-13.3.html", "section-13.2.html")
        return m.group(1) + new_href + m.group(3) + m.group(4) + m.group(5)
    text, n = pattern.subn(repl_so, text)
    if n:
        add("p0_structured_output_retarget", n)

    # Also "Instructor library" -> section-13.2.html (currently the audit says it IS pointing there already
    # Wait: "Instructor library" in module-14-prompt-engineering/index.html:78 href=`../module-13-llm-apis/section-13.2.html`
    # Audit says destination is "Structured Output & Tool Integration". The anchor "Instructor library" doesn't match
    # the section title -- but the section IS about structured output, so Instructor is a relevant tool there.
    # This is a P0 because the topic noun "Instructor library" doesn't overlap with the section title.
    # However, section 13.2 IS the right destination. The audit flagged it because of the topic-overlap heuristic.
    # We can leave this — it's actually correct semantically.

    if text != orig:
        html_path.write_text(text, encoding="utf-8")
        files_modified.add(str(html_path))


# ============================================================
# P0: "open-weight models" / "Open-weight models" / "open-weight model" -> section-8.2.html
# Currently incorrectly pointing at section-8.1.html (Closed-Source Frontier)
# ============================================================

for html_path in ROOT.rglob("*.html"):
    if html_path.resolve() in IN_FLIGHT:
        continue
    text = html_path.read_text(encoding="utf-8")
    orig = text

    pattern = re.compile(
        r'(<a[^>]*?href=")([^"]*module-08-modern-llm-landscape/section-8\.1\.html)("[^>]*>)([Oo]pen-weight models?|Mixture-of-[Ee]xperts|mixture-of-experts)(</a>)',
        re.DOTALL,
    )
    def repl_ow(m):
        new_href = m.group(2).replace("section-8.1.html", "section-8.2.html")
        return m.group(1) + new_href + m.group(3) + m.group(4) + m.group(5)
    text, n = pattern.subn(repl_ow, text)
    if n:
        add("p0_open_weight_retarget", n)

    if text != orig:
        html_path.write_text(text, encoding="utf-8")
        files_modified.add(str(html_path))


# ============================================================
# P0: Chapter 11 Interpretability link pointing to book root '../../index.html'
# In section-10.7.html, re-target to actual interpretability module-11
# ============================================================

replace_in_file(
    ROOT / "part-2-understanding-llms/module-10-inference-optimization/section-10.7.html",
    r'<a([^>]+?)href="\.\./\.\./index\.html"([^>]*?)>Chapter 11: Interpretability and Mechanistic Understanding</a>',
    r'<a\1href="../module-11-interpretability/index.html"\2>Chapter 11: Interpretability and Mechanistic Understanding</a>',
    "p0_ch11_interp_retarget",
)


# ============================================================
# P0: "10.3 Hardware Landscape" pointing to section-10.3.html (Speculative Decoding)
# Should likely point to a different section. Let's check the actual destination.
# section-10.3.html is "Speculative Decoding" per audit. There IS no "Hardware Landscape" in module-10.
# Drop the link / fix text. Need to inspect.
# ============================================================

# Defer to manual review — single occurrence in appendix-g.
# Note in report.

# ============================================================
# P0: "RAG pipeline" with href to module-22-embeddings-vector-db/index.html (Embeddings, Vector DB)
# Should be retargeted to module-23-rag/index.html (RAG)
# Just one occurrence in section-45.5.html
# ============================================================

replace_in_file(
    ROOT / "part-10-idea-to-product/module-45-prototype-to-production/section-45.5.html",
    r'<a([^>]+?)href="([^"]*module-22-embeddings-vector-db/index\.html)"([^>]*?)>RAG pipeline</a>',
    r'<a\1href="\2"\3>vector database</a>',
    "p0_rag_pipeline_text",
)


# ============================================================
# P0: "knowledge graph(s)" with href to section-23.4.html (Deep Research & Agentic RAG)
# Section 23.4 doesn't define knowledge graphs. Re-target or downgrade.
# Section 23.4 is "Deep Research & Agentic RAG" — knowledge graphs are mentioned but not defined there.
# Likely meant section 23.3 (Advanced RAG patterns) or 24.5 (knowledge graphs in conv AI).
# Looking at the modules, the most likely home for KGs is section-23.3.html or as part of section-24.5.
# Safe move: downgrade to plain text since there isn't a clear canonical home for "knowledge graph" alone.
# ============================================================

for html_path in [
    ROOT / "part-3-working-with-llms/module-15-hybrid-ml-llm/section-15.5.html",
    ROOT / "part-5-retrieval-conversation/module-24-conversational-ai/section-24.3.html",
    ROOT / "part-6-agentic-ai/module-27-tool-use-protocols/section-27.5.html",
    ROOT / "part-10-idea-to-product/module-42-strategy-prioritization/section-42.4.html",
]:
    # Downgrade <a href=...section-23.4...>knowledge graph(s)</a> to bare text
    n = replace_in_file(
        html_path,
        r'<a[^>]+?href="[^"]*module-23-rag/section-23\.4\.html"[^>]*?>(knowledge graphs?)</a>',
        r'\1',
        "p0_knowledge_graph_downgrade",
    )


# ============================================================
# P0: "rate limit" / "Rate limiting" pointing to section-35.2.html (Frontend & UI)
# Should be section-35.3.html or similar (Rate Limiting and Throttling).
# Let's inspect: module-35-production-engineering has sections that cover rate limiting.
# ============================================================

# Find correct target for rate limiting in module-35
# Section 35.4 might be "Latency Budgets & Performance" or similar. Try section-35.3.

# Check destinations first
m35 = ROOT / "part-8-evaluation-production/module-35-production-engineering"
if m35.exists():
    section_titles = {}
    for sp in sorted(m35.glob("section-*.html")):
        try:
            t = sp.read_text(encoding="utf-8")
            m = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.DOTALL)
            if m:
                section_titles[sp.name] = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        except Exception:
            pass
    rate_limit_target = None
    for sname, title in section_titles.items():
        if 'rate limit' in title.lower() or 'throttl' in title.lower():
            rate_limit_target = sname
            break
    # If found, fix the links
    if rate_limit_target:
        for html_path in [
            ROOT / "part-4-training-adapting/module-17-synthetic-data/section-17.3.html",
            ROOT / "part-5-retrieval-conversation/module-23-rag/section-23.6.html",
            ROOT / "part-6-agentic-ai/module-27-tool-use-protocols/section-27.2.html",
            ROOT / "part-6-agentic-ai/module-27-tool-use-protocols/section-27.4.html",
            ROOT / "part-8-evaluation-production/module-34-evaluation-observability/section-34.3.html",
            ROOT / "part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.1.html",
        ]:
            replace_in_file(
                html_path,
                r'(href="[^"]*module-35-production-engineering/)section-35\.2\.html(")',
                rf'\1{rate_limit_target}\2',
                "p0_rate_limit_retarget",
            )


# ============================================================
# P0: "catastrophic forgetting" -> section-18.3.html (SFT). Audit says SFT only mentions it in passing.
# Check if section-18.3 actually defines catastrophic forgetting. If yes, leave it.
# If no, downgrade.
# ============================================================
sft = ROOT / "part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.3.html"
if sft.exists():
    sft_text = sft.read_text(encoding="utf-8")
    if "catastrophic forgetting" in sft_text.lower():
        # It IS mentioned. Check whether it's defined or just referenced.
        idx = sft_text.lower().find("catastrophic forgetting")
        snippet = sft_text[max(0, idx - 200):idx + 400].lower()
        # Heuristic: if the term appears multiple times AND has a definition-like context, leave.
        # Otherwise, leave link as-is since the section does cover it.
        # The audit said "destination only mentions in passing" — but if it's the only home, leaving the link is acceptable.
        # Defer to manual review.
        pass


# ============================================================
# P0: "Error Recovery, Resilience and Graceful Degradation" -> wrong neighbor
# audit: section-48.5.html:214 href="section-48.4.html"
# We need to find the correct destination
# ============================================================

# Find section that matches "Error Recovery" or "Resilience" in module-48
m48 = ROOT / "part-10-idea-to-product/module-48-shipping-deploying"
if m48.exists():
    for sp in sorted(m48.glob("section-*.html")):
        try:
            t = sp.read_text(encoding="utf-8")
            m = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.DOTALL)
            if m:
                title = re.sub(r'<[^>]+>', '', m.group(1)).strip().lower()
                if ('error recovery' in title or 'resilience' in title or 'graceful' in title):
                    target_section = sp.name
                    # Fix the link in section-48.5.html
                    replace_in_file(
                        ROOT / "part-10-idea-to-product/module-48-shipping-deploying/section-48.5.html",
                        r'(href=")section-48\.4\.html(">Error Recovery, Resilience and Graceful Degradation</a>)',
                        rf'\1{target_section}\2',
                        "p0_error_recovery_retarget",
                    )
                    break
        except Exception:
            pass


# ============================================================
# P0: "Testing Multi-Agent Systems" -> wrong destination
# audit: section-38.2.html:264 href="section-38.3.html" with text "Production Observability and Cost Control"
# Hmm audit says "Production Observability" is the LINK TEXT, "Agentic Security Benchmarks" is what destination delivers
# We need to find correct destination for "Production Observability" in module-38
# ============================================================

m38 = ROOT / "part-9-safety-security-ethics/module-38-agent-safety-security"
if m38.exists():
    for sp in sorted(m38.glob("section-*.html")):
        try:
            t = sp.read_text(encoding="utf-8")
            m = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.DOTALL)
            if m:
                title = re.sub(r'<[^>]+>', '', m.group(1)).strip().lower()
                if 'production observability' in title or 'cost control' in title:
                    target = sp.name
                    replace_in_file(
                        ROOT / "part-9-safety-security-ethics/module-38-agent-safety-security/section-38.2.html",
                        r'(href=")section-38\.3\.html(">Production Observability and Cost Control</a>)',
                        rf'\1{target}\2',
                        "p0_observability_retarget",
                    )
                    break
        except Exception:
            pass


# ============================================================
# P0: "architecture deep dive in Chapter 08" -> Chapter 9: Reasoning
# In section-37.10.html href to module-09-reasoning/index.html
# The href is to a reasoning chapter but text says Chapter 08 (architecture).
# Likely the actual reference should be to module-08-modern-llm-landscape (architecture deep dive)
# ============================================================

replace_in_file(
    ROOT / "part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.10.html",
    r'<a([^>]+?)href="\.\./\.\./part-2-understanding-llms/module-09-reasoning-test-time-compute/index\.html"([^>]*?)>architecture deep dive in Chapter 08</a>',
    r'<a\1href="../../part-2-understanding-llms/module-08-modern-llm-landscape/index.html"\2>architecture deep dive in Chapter 08</a>',
    "p0_architecture_ch8_retarget",
)


# ============================================================
# Report
# ============================================================

print("\n=== P0 fix stats ===")
for k in sorted(stats):
    print(f"  {k}: {stats[k]}")
print(f"\nFiles modified: {len(files_modified)}")
print(f"Files skipped (in-flight): {len(files_skipped)}")
for f in sorted(files_skipped)[:10]:
    print(f"  SKIPPED: {f}")
if errors:
    print(f"\nErrors ({len(errors)}):")
    for e in errors[:30]:
        print(f"  {e}")
