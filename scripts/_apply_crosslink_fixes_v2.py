#!/usr/bin/env python3
"""
P0 + P1 cross-link fixes (v2).

Skip strategy:
- Files in known agent scopes (per task description) are skipped.
- Files modified within the last 60 seconds (active write) are skipped.

Agent scopes (skip):
- front-matter/* (FM rewrite)
- part-7-multimodal-generation/module-31-*, module-32-* (Ch 31/32 dup resolution)
- part-10-idea-to-product/* (Part 10 review)
- part-11-applications-across-industries/* (Part 11 review)
- part-12-frontiers/module-63-*, module-64-*, module-65-* (Part 12 comprehensive)
- appendices/appendix-n-*, appendices/appendix-o-* (MLOps)
- */tools-of-the-trade/* (Tools enrichment)
- appendices/appendix-e-*/section-e.2.html, e.3.html
- appendices/appendix-f-*/section-f.2.html, f.3.html
- appendices/appendix-i-*/section-i.6.html, i.7.html
- Bibliography agent touches everything — accept overlap risk for non-bib changes.
"""
from __future__ import annotations

import re
import time
from pathlib import Path

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
NOW = time.time()
ACTIVE_WINDOW = 60  # seconds

def is_in_agent_scope(path: Path) -> str | None:
    """Return reason string if path is in an active agent's scope, else None."""
    rel = path.resolve().relative_to(ROOT.resolve())
    s = str(rel).replace("\\", "/")
    if s.startswith("front-matter/"):
        return "FM rewrite agent"
    if s.startswith("part-7-multimodal-generation/module-31-") or s.startswith("part-7-multimodal-generation/module-32-"):
        return "Ch 31/32 dup resolution"
    if s.startswith("part-10-idea-to-product/"):
        return "Part 10 review"
    if s.startswith("part-11-applications-across-industries/"):
        return "Part 11 review"
    if s.startswith("part-12-frontiers/module-63-") or s.startswith("part-12-frontiers/module-64-") or s.startswith("part-12-frontiers/module-65-"):
        return "Part 12 comprehensive"
    if s.startswith("appendices/appendix-n-") or s.startswith("appendices/appendix-o-"):
        return "MLOps authoring"
    if "tools-of-the-trade" in s:
        return "Tools enrichment"
    if re.search(r"appendices/appendix-e-[^/]+/section-e\.[23]\.html$", s):
        return "Stub authoring (E.2/E.3)"
    if re.search(r"appendices/appendix-f-[^/]+/section-f\.[23]\.html$", s):
        return "Stub authoring (F.2/F.3)"
    if re.search(r"appendices/appendix-i-[^/]+/section-i\.[67]\.html$", s):
        return "Stub authoring (I.6/I.7)"
    return None


def is_active(path: Path) -> bool:
    """Modified in last ACTIVE_WINDOW seconds."""
    try:
        return NOW - path.stat().st_mtime < ACTIVE_WINDOW
    except OSError:
        return False


stats: dict[str, int] = {}
files_modified: set[str] = set()
files_skipped: dict[str, str] = {}
errors: list[str] = []


def can_edit(path: Path, label: str) -> bool:
    if not path.exists():
        errors.append(f"missing: {path}")
        return False
    scope = is_in_agent_scope(path)
    if scope:
        files_skipped[str(path)] = scope
        return False
    if is_active(path):
        files_skipped[str(path)] = "active-write (< 60s ago)"
        return False
    return True


def add(k: str, n: int = 1):
    stats[k] = stats.get(k, 0) + n


def apply_regex(path: Path, pattern: str, replacement, label: str, flags=0) -> int:
    if not can_edit(path, label):
        return 0
    text = path.read_text(encoding="utf-8")
    new, n = re.subn(pattern, replacement, text, flags=flags)
    if n > 0:
        path.write_text(new, encoding="utf-8")
        files_modified.add(str(path))
        add(label, n)
    return n


def apply_replace(path: Path, old: str, new: str, label: str, allow_multi: bool = False) -> int:
    if not can_edit(path, label):
        return 0
    text = path.read_text(encoding="utf-8")
    if old not in text:
        return 0
    n = text.count(old)
    if n > 1 and not allow_multi:
        errors.append(f"{path.name}: ambiguous ({n}x) {old[:60]!r}")
        return 0
    new_text = text.replace(old, new)
    path.write_text(new_text, encoding="utf-8")
    files_modified.add(str(path))
    add(label, n)
    return n


# ============================================================
# P0: Hugging Face -> Appendix C
# Retarget href when anchor is "Hugging Face"/"HuggingFace" and href points to
# either module-13-llm-apis/section-13.2.html or module-18-fine-tuning-fundamentals/section-18.5.html
# ============================================================

def get_relpath_to_appendix_c(html_path: Path) -> str:
    target = (ROOT / "appendices/appendix-c-huggingface-ecosystem/index.html").resolve()
    src_dir = html_path.parent.resolve()
    src_parts = src_dir.relative_to(ROOT.resolve()).parts
    target_rel = target.relative_to(ROOT.resolve()).as_posix()
    return "../" * len(src_parts) + target_rel


for html_path in ROOT.rglob("*.html"):
    if not can_edit(html_path, "p0_huggingface_retarget"):
        continue
    text = html_path.read_text(encoding="utf-8")
    orig = text
    rel_target = get_relpath_to_appendix_c(html_path)

    for bad_suffix in [
        "module-13-llm-apis/section-13.2.html",
        "module-18-fine-tuning-fundamentals/section-18.5.html",
    ]:
        # Use a non-greedy match and constrain to single <a> tag
        pattern = re.compile(
            r'(<a\b[^>]*?href=")([^"]*' + re.escape(bad_suffix) + r'[^"]*)("[^>]*?>)(Hugging\s*Face|HuggingFace)(\s*</a>)',
            re.IGNORECASE,
        )
        def repl(m):
            return m.group(1) + rel_target + m.group(3) + m.group(4) + m.group(5)
        text2, n = pattern.subn(repl, text)
        if n:
            add("p0_huggingface_retarget", n)
            text = text2

    if text != orig:
        html_path.write_text(text, encoding="utf-8")
        files_modified.add(str(html_path))


# ============================================================
# P0: structured output(s) -> section-13.2.html (was section-13.3.html)
# ============================================================
for html_path in ROOT.rglob("*.html"):
    if not can_edit(html_path, "p0_structured_output_retarget"):
        continue
    text = html_path.read_text(encoding="utf-8")
    orig = text
    pattern = re.compile(
        r'(<a\b[^>]*?href=")([^"]*module-13-llm-apis/section-13\.)3(\.html[^"]*)("[^>]*?>)((?:S|s)tructured\s+outputs?)(</a>)',
    )
    def repl_so(m):
        return m.group(1) + m.group(2) + "2" + m.group(3) + m.group(4) + m.group(5) + m.group(6)
    text, n = pattern.subn(repl_so, text)
    if n:
        add("p0_structured_output_retarget", n)
    if text != orig:
        html_path.write_text(text, encoding="utf-8")
        files_modified.add(str(html_path))


# ============================================================
# P0: open-weight models / Mixture-of-Experts -> section-8.2.html (was section-8.1.html)
# ============================================================
for html_path in ROOT.rglob("*.html"):
    if not can_edit(html_path, "p0_open_weight_retarget"):
        continue
    text = html_path.read_text(encoding="utf-8")
    orig = text
    pattern = re.compile(
        r'(<a\b[^>]*?href=")([^"]*module-08-modern-llm-landscape/section-8\.)1(\.html[^"]*)("[^>]*?>)([Oo]pen-weight models?|Mixture-of-[Ee]xperts|mixture-of-experts)(</a>)',
    )
    def repl_ow(m):
        return m.group(1) + m.group(2) + "2" + m.group(3) + m.group(4) + m.group(5) + m.group(6)
    text, n = pattern.subn(repl_ow, text)
    if n:
        add("p0_open_weight_retarget", n)
    if text != orig:
        html_path.write_text(text, encoding="utf-8")
        files_modified.add(str(html_path))


# ============================================================
# P0: Rate limit -> retarget to correct section in module-35
# First find what section actually covers rate limiting.
# ============================================================
m35_dir = ROOT / "part-8-evaluation-production/module-35-production-engineering"
rate_target = None
if m35_dir.exists():
    for sp in sorted(m35_dir.glob("section-*.html")):
        try:
            t = sp.read_text(encoding="utf-8")
            m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.DOTALL)
            if m:
                title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
                if "rate" in title.lower() and ("limit" in title.lower() or "throttl" in title.lower()):
                    rate_target = sp.name
                    break
        except Exception:
            pass

if rate_target:
    for html_path in ROOT.rglob("*.html"):
        if not can_edit(html_path, "p0_rate_limit_retarget"):
            continue
        text = html_path.read_text(encoding="utf-8")
        orig = text
        pattern = re.compile(
            r'(<a\b[^>]*?href=")([^"]*module-35-production-engineering/)section-35\.2\.html(["#][^"]*?"[^>]*?>)([Rr]ate limit(?:ing)?)(</a>)',
        )
        def repl_rl(m):
            return m.group(1) + m.group(2) + rate_target + m.group(3) + m.group(4) + m.group(5)
        text, n = pattern.subn(repl_rl, text)
        if n:
            add("p0_rate_limit_retarget", n)
        if text != orig:
            html_path.write_text(text, encoding="utf-8")
            files_modified.add(str(html_path))


# ============================================================
# P0: Knowledge graph -> downgrade (no canonical home in module-23-rag/section-23.4)
# ============================================================
for html_path in ROOT.rglob("*.html"):
    if not can_edit(html_path, "p0_kg_downgrade"):
        continue
    text = html_path.read_text(encoding="utf-8")
    orig = text
    # Downgrade <a ...section-23.4...>knowledge graph(s)</a> to bare text
    pattern = re.compile(
        r'<a\b[^>]*?href="[^"]*module-23-rag/section-23\.4\.html[^"]*"[^>]*?>(knowledge graphs?)</a>',
    )
    text, n = pattern.subn(r"\1", text)
    if n:
        add("p0_kg_downgrade", n)
    if text != orig:
        html_path.write_text(text, encoding="utf-8")
        files_modified.add(str(html_path))


# ============================================================
# P1 leftover patterns: Chapter 09 / 9 -> Chapter 10 in non-in-flight files
# These were skipped in v1 due to too-aggressive window
# ============================================================

# Specific patterns we can do mechanically
specific_p1_edits = [
    # Chapter 09 -> Chapter 10 (Inference Optimization)
    (ROOT / "part-12-frontiers/module-61-frontier-architectures/index.html",
     "Chapter 09</a>: Inference Optimization (KV cache, quantization, speculative decoding)",
     "Chapter 10</a>: Inference Optimization (KV cache, quantization, speculative decoding)",
     "p1_ch9_to_10"),
    (ROOT / "part-2-understanding-llms/module-09-reasoning-test-time-compute/index.html",
     "Chapter 09</a>: Inference Optimization, we cover",
     "Chapter 10</a>: Inference Optimization, we cover",
     "p1_ch9_to_10"),
    (ROOT / "part-3-working-with-llms/module-13-llm-apis/index.html",
     "Chapter 09</a>: Inference Optimization and Efficient Serving (context for why APIs are structured as they are)",
     "Chapter 10</a>: Inference Optimization and Efficient Serving (context for why APIs are structured as they are)",
     "p1_ch9_to_10"),
    (ROOT / "part-3-working-with-llms/module-15-hybrid-ml-llm/index.html",
     "Chapter 09</a>: Inference Optimization (",
     "Chapter 10</a>: Inference Optimization (",
     "p1_ch9_to_10"),
    (ROOT / "part-4-training-adapting/module-19-peft/index.html",
     "Chapter 09</a>: Inference Optimization (quantization basics, GPU memory concepts)",
     "Chapter 10</a>: Inference Optimization (quantization basics, GPU memory concepts)",
     "p1_ch9_to_10"),
    # appendix-c stuff
    (ROOT / "appendices/appendix-c-huggingface-ecosystem/section-c.1.html",
     "Chapter 07: Text Generation and Decoding",
     "Chapter 05: Decoding Strategies &amp; Text Generation",
     "p1_ch7_to_5"),
    (ROOT / "appendices/appendix-c-huggingface-ecosystem/section-c.3.html",
     "Chapter 09: Fine-Tuning",
     "Chapter 18: Fine-Tuning Fundamentals",
     "p1_ch9_to_18"),
    (ROOT / "appendices/appendix-c-huggingface-ecosystem/section-c.4.html",
     "Chapter 13: Alignment and RLHF",
     "Chapter 20: Alignment, RLHF, DPO &amp; Preference Tuning",
     "p1_ch13_to_20"),
    # module-10 meta tags
    (ROOT / "part-2-understanding-llms/module-10-inference-optimization/index.html",
     "Chapter 09: Inference Optimization &amp; Efficient Serving",
     "Chapter 10: Inference Optimization &amp; Efficient Serving",
     "p1_ch9_to_10_meta"),
]

for path, old, new, label in specific_p1_edits:
    apply_replace(path, old, new, label, allow_multi=True)


# Appendix index pages: Section 9.5 in module-10-inference-optimization
apply_replace(
    ROOT / "part-2-understanding-llms/module-10-inference-optimization/section-10.3.html",
    "Section 9.5", "Section 10.5",
    "p1_section_9_5_to_10_5", allow_multi=True,
)
apply_replace(
    ROOT / "part-2-understanding-llms/module-10-inference-optimization/section-10.6.html",
    "Section 9.5", "Section 10.5",
    "p1_section_9_5_to_10_5", allow_multi=True,
)


# ============================================================
# Part 9 index: "Part X: Frontiers" -> "Part XII: Frontiers"
# ============================================================
apply_replace(
    ROOT / "part-9-safety-security-ethics/index.html",
    "Part X: Frontiers", "Part XII: Frontiers",
    "p1_part_x_to_xii", allow_multi=True,
)


# ============================================================
# appendix-l section-l.4.html: Chapter 09 -> Chapter 10
# ============================================================
apply_regex(
    ROOT / "appendices/appendix-l-inference-serving/section-l.4.html",
    r"Chapter 09",
    "Chapter 10",
    "p1_ch9_to_10",
)


# ============================================================
# Audit-specific Section 30 -> Section 37 fixes in module-37 (8 occurrences)
# These are likely in section cards or breadcrumbs
# ============================================================
m37_dir = ROOT / "part-9-safety-security-ethics/module-37-safety-ethics-regulation"
if m37_dir.exists():
    for sp in sorted(m37_dir.glob("*.html")):
        if not can_edit(sp, "p1_section_30_to_37"):
            continue
        text = sp.read_text(encoding="utf-8")
        orig = text
        # Only rewrite display text "Section 30.N" -> "Section 37.N"
        text = re.sub(r"\bSection 30\.(\d+)\b", r"Section 37.\1", text)
        # Also rewrite ">30.N<" patterns in display contexts
        if text != orig:
            sp.write_text(text, encoding="utf-8")
            files_modified.add(str(sp))
            add("p1_section_30_to_37", 1)


# ============================================================
# Audit P1: Appendix M.x -> Appendix L.x in section-k.4 specifically (audit cited 2x)
# ============================================================
apply_regex(
    ROOT / "appendices/appendix-k-experiment-tracking/section-k.4.html",
    r"Appendix P\b",
    "Appendix L",
    "p1_appendix_p_to_l",
)


# ============================================================
# Audit P1: Chapter 25 -> Chapter 26 (AI Agents) in module-29-specialized-agents
# ============================================================
for p in [
    ROOT / "part-6-agentic-ai/module-29-specialized-agents/index.html",
    ROOT / "part-6-agentic-ai/module-29-specialized-agents/section-29.4.html",
]:
    apply_regex(p,
        r'(href="[^"]*module-26-ai-agents[^"]*"[^>]*>)Chapter 25(</a>)',
        r"\1Chapter 26\2",
        "p1_ch25_to_26",
    )


# ============================================================
# Audit P1: Chapter 13 -> Chapter 14 (Prompt Engineering)
# ============================================================
apply_regex(
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.2.html",
    r'(href="[^"]*module-14-prompt-engineering[^"]*"[^>]*>)Chapter 13(</a>)',
    r"\1Chapter 14\2",
    "p1_ch13_to_14",
)


# ============================================================
# Audit P1: Chapter 15 -> Chapter 17 (Synthetic Data)
# ============================================================
apply_regex(
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.4.html",
    r'(href="[^"]*module-17-synthetic[^"]*"[^>]*>)Chapter 15(</a>)',
    r"\1Chapter 17\2",
    "p1_ch15_to_17",
)


# ============================================================
# Audit P1: Chapter 20 -> Chapter 11 (Interpretability)
# ============================================================
apply_regex(
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.7.html",
    r'(href="[^"]*module-11-interpretability[^"]*"[^>]*>)Chapter 20(</a>)',
    r"\1Chapter 11\2",
    "p1_ch20_to_11",
)


# ============================================================
# Audit P1: Chapter 17 -> Chapter 18 (Fine-Tuning) in three sections
# ============================================================
for p in [
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.5.html",
    ROOT / "part-2-understanding-llms/module-08-modern-llm-landscape/section-8.2.html",
    ROOT / "part-2-understanding-llms/module-08-modern-llm-landscape/section-8.4.html",
]:
    apply_regex(p,
        r'(href="[^"]*module-18-fine-tuning[^"]*"[^>]*>)Chapter 17(</a>)',
        r"\1Chapter 18\2",
        "p1_ch17_to_18",
    )


# Audit P1: Chapter 25 -> Chapter 37 in section-7.4
apply_regex(
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.4.html",
    r'(href="[^"]*module-37-safety[^"]*"[^>]*>)Chapter 25(</a>)',
    r"\1Chapter 37\2",
    "p1_ch25_to_37",
)

# Audit P1: Chapter 27 -> Chapter 31 in section-7.1
apply_regex(
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.1.html",
    r'(href="[^"]*module-31-multimodal[^"]*"[^>]*>)Chapter 27(</a>)',
    r"\1Chapter 31\2",
    "p1_ch27_to_31",
)

# Audit P1: Chapter 29 -> Chapter 34 in section-7.3
apply_regex(
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.3.html",
    r'(href="[^"]*module-34-evaluation[^"]*"[^>]*>)Chapter 29(</a>)',
    r"\1Chapter 34\2",
    "p1_ch29_to_34",
)

# Audit P1: Chapter 18 -> Chapter 19 (PEFT)
apply_regex(
    ROOT / "part-2-understanding-llms/module-08-modern-llm-landscape/section-8.2.html",
    r'(href="[^"]*module-19-peft[^"]*"[^>]*>)Chapter 18(</a>)',
    r"\1Chapter 19\2",
    "p1_ch18_to_19",
)

# Audit P1: Chapter 20 -> Chapter 19 (PEFT / Knowledge Distillation)
apply_regex(
    ROOT / "part-2-understanding-llms/module-09-reasoning-test-time-compute/section-9.2.html",
    r'(href="[^"]*module-19-peft[^"]*"[^>]*>)Chapter 20(</a>)',
    r"\1Chapter 19\2",
    "p1_ch20_to_19",
)

# Audit P1: Chapter 24 -> Chapter 20 (Alignment)
apply_replace(
    ROOT / "part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.5.html",
    "Chapter 24: Alignment: RLHF, DPO &amp; Preference Tuning",
    "Chapter 20: Alignment: RLHF, DPO &amp; Preference Tuning",
    "p1_ch24_to_20",
)

# Audit P1: section 11.2 -> 14.2 in module-14
apply_regex(
    ROOT / "part-3-working-with-llms/module-14-prompt-engineering/section-14.3.html",
    r"\bSection 11\.2\b",
    "Section 14.2",
    "p1_sec11_2_to_14_2",
)


# Audit P1: Chapter 8 -> Chapter 10 (Inference Optimization) in section-7.3
apply_regex(
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.3.html",
    r'(href="[^"]*module-10-inference[^"]*"[^>]*>)Chapter 08(</a>)',
    r"\1Chapter 10\2",
    "p1_ch8_to_10_inference",
)


# ============================================================
# Report
# ============================================================
print("\n=== Stats ===")
for k in sorted(stats):
    print(f"  {k}: {stats[k]}")
print(f"\nFiles modified: {len(files_modified)}")
print(f"Files skipped: {len(files_skipped)}")
# Print breakdown
from collections import Counter
reasons = Counter(files_skipped.values())
for reason, count in reasons.most_common():
    print(f"  [{count}] {reason}")
if errors:
    print(f"\nErrors ({len(errors)}):")
    for e in errors[:30]:
        print(f"  {e}")
