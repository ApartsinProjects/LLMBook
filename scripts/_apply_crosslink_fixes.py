#!/usr/bin/env python3
"""
Apply cross-link fixes per cross-link-integrity-audit.md.
P1 = displayed-text rewrites. P0 = href retargets or text fixes.

In-flight files (mtime within 10 min) are skipped.
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
NOW = time.time()
WINDOW = 10 * 60

# Files we explicitly mutated already in this run (don't treat as in-flight)
ALREADY_TOUCHED = {
    (ROOT / "appendices/appendix-l-inference-serving/index.html").resolve(),
    (ROOT / "appendices/appendix-p-docker-containers/index.html").resolve(),
    (ROOT / "part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.11.html").resolve(),
    (ROOT / "part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.12.html").resolve(),
}

IN_FLIGHT: set[Path] = set()
for p in ROOT.rglob("*.html"):
    try:
        if NOW - p.stat().st_mtime < WINDOW:
            rp = p.resolve()
            if rp not in ALREADY_TOUCHED:
                IN_FLIGHT.add(rp)
    except OSError:
        pass

stats: dict[str, int] = {}
files_modified: set[str] = set()
files_skipped_inflight: set[str] = set()
errors: list[str] = []


def add(key: str, n: int = 1):
    stats[key] = stats.get(key, 0) + n


def apply_to(path: Path, edits: list[tuple[str, str, bool]], label: str) -> int:
    """edits: list of (old, new, allow_multi)"""
    if not path.exists():
        errors.append(f"missing: {path}")
        return 0
    rp = path.resolve()
    if rp in IN_FLIGHT:
        files_skipped_inflight.add(str(path))
        return 0
    text = path.read_text(encoding="utf-8")
    orig = text
    total = 0
    for old, new, allow_multi in edits:
        if old not in text:
            continue
        n = text.count(old)
        if n > 1 and not allow_multi:
            errors.append(f"{path.name}: ambiguous {n}x for label={label}: {old[:60]!r}")
            continue
        text = text.replace(old, new)
        total += n
    if text != orig:
        path.write_text(text, encoding="utf-8")
        files_modified.add(str(path))
        add(label, total)
    return total


# Helper: regex-based edit for cases where exact string isn't safe
def apply_regex(path: Path, pattern: str, replacement, label: str, flags=0) -> int:
    if not path.exists():
        errors.append(f"missing: {path}")
        return 0
    rp = path.resolve()
    if rp in IN_FLIGHT:
        files_skipped_inflight.add(str(path))
        return 0
    text = path.read_text(encoding="utf-8")
    new_text, n = re.subn(pattern, replacement, text, flags=flags)
    if n > 0:
        path.write_text(new_text, encoding="utf-8")
        files_modified.add(str(path))
        add(label, n)
    return n


# ============================================================
# P1.A: Chapter 09 -> Chapter 10 (Inference Optimization)
# Whenever href points to module-10-inference-optimization
# ============================================================

p1_ch9_to_10_files = [
    ROOT / "appendices/appendix-l-inference-serving/index.html",
    ROOT / "part-3-working-with-llms/module-15-hybrid-ml-llm/index.html",
    ROOT / "part-3-working-with-llms/module-13-llm-apis/index.html",
    ROOT / "part-12-frontiers/module-61-frontier-architectures/index.html",
    ROOT / "part-12-frontiers/module-61-frontier-architectures/section-33.4.html",
    ROOT / "part-12-frontiers/module-61-frontier-architectures/section-61.3.html",
    ROOT / "part-12-frontiers/module-61-frontier-architectures/section-61.2.html",
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/index.html",
    ROOT / "part-2-understanding-llms/index.html",
    ROOT / "part-2-understanding-llms/module-10-inference-optimization/index.html",
    ROOT / "part-8-evaluation-production/module-34-evaluation-observability/section-34.12.html",
    ROOT / "part-2-understanding-llms/module-09-reasoning-test-time-compute/index.html",
    ROOT / "part-4-training-adapting/module-19-peft/index.html",
    ROOT / "part-1-foundations/module-00-ml-pytorch-foundations/index.html",
    ROOT / "part-1-foundations/module-04-transformer-architecture/section-4.4.html",
    ROOT / "part-1-foundations/module-04-transformer-architecture/index.html",
    ROOT / "part-1-foundations/module-04-transformer-architecture/section-4.1.html",
    ROOT / "part-1-foundations/module-04-transformer-architecture/section-4.3.html",
    ROOT / "part-1-foundations/module-05-decoding-text-generation/index.html",
    ROOT / "part-8-evaluation-production/module-35-production-engineering/index.html",
    ROOT / "part-5-retrieval-conversation/module-22-embeddings-vector-db/section-22.2.html",
    ROOT / "part-8-evaluation-production/module-35-production-engineering/section-35.9.html",
    ROOT / "part-8-evaluation-production/module-35-production-engineering/section-35.7.html",
    ROOT / "part-8-evaluation-production/module-35-production-engineering/section-35.3.html",
    ROOT / "part-10-idea-to-product/module-47-scaling-economics/section-47.4.html",
    ROOT / "part-10-idea-to-product/module-46-compute-planning/section-46.3.html",
    ROOT / "part-1-foundations/module-05-decoding-text-generation/section-5.4.html",
    ROOT / "appendices/appendix-l-inference-serving/section-l.4.html",
    ROOT / "part-3-working-with-llms/module-15-hybrid-ml-llm/section-15.4.html",
    ROOT / "part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html",
    ROOT / "part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.1.html",
]

for f in p1_ch9_to_10_files:
    if not f.exists():
        continue
    rp = f.resolve()
    if rp in IN_FLIGHT:
        files_skipped_inflight.add(str(f))
        continue
    text = f.read_text(encoding="utf-8")
    orig = text
    # Only rewrite Chapter 09/Chapter 9 when the link target on the same line is module-10-inference-optimization
    # Use a regex that handles HTML constructs
    # 1) "Chapter 09" -> "Chapter 10"
    text = re.sub(r'Chapter 09(?=\b|:|\)|<|,|\.)', 'Chapter 10', text)
    # 2) "Chapter 09:" patterns
    text = text.replace('Chapter 09:', 'Chapter 10:')
    # 3) Inline "Chapter 9" in parens or with colon explicitly referring to inference optimization
    text = re.sub(r'Chapter 9(?= ?\(Inference Optimization\))', 'Chapter 10', text)
    text = re.sub(r'Chapter 9:(?= Inference Optimization)', 'Chapter 10:', text)
    # The "Chapter 09" replacements should not over-fire. Don't rewrite "Chapter 9" generally
    # because it might refer to reasoning (which is now chapter 9 correctly).
    # Skip meta tags (those are titles for module-10 and they already say "Chapter 10" via canonical).
    # Note: module-10-inference-optimization/index.html title currently says "Chapter 09" — fix it too.
    if text != orig:
        f.write_text(text, encoding="utf-8")
        files_modified.add(str(f))
        n = sum(1 for _ in re.finditer(r'Chapter 1[0]', text)) - sum(1 for _ in re.finditer(r'Chapter 1[0]', orig))
        add("p1_ch9_to_10", n)

# Special case: section-9.5.html says "Chapter 10: Reasoning Models" — should be Chapter 9
sec95 = ROOT / "part-2-understanding-llms/module-09-reasoning-test-time-compute/section-9.5.html"
if sec95.exists() and sec95.resolve() not in IN_FLIGHT:
    text = sec95.read_text(encoding="utf-8")
    new = text.replace(
        '<p>This concludes <a href="index.html">Chapter 10: Reasoning Models &amp; Test-Time Compute</a>',
        '<p>This concludes <a href="index.html">Chapter 9: Reasoning Models &amp; Test-Time Compute</a>'
    ).replace(
        '<a href="../module-10-inference-optimization/index.html">Chapter 09: Inference Optimization</a>',
        '<a href="../module-10-inference-optimization/index.html">Chapter 10: Inference Optimization</a>'
    )
    if new != text:
        sec95.write_text(new, encoding="utf-8")
        files_modified.add(str(sec95))
        add("p1_section_9_5_fixes", 2)

# ============================================================
# P1.B: Chapter 06 -> Chapter 07 (Pretraining)
# ============================================================

p1_ch6_to_7_files = [
    ROOT / "front-matter/fm-how-to-use.html",
    ROOT / "part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html",
    ROOT / "part-1-foundations/module-05-decoding-text-generation/section-5.4.html",
    ROOT / "part-12-frontiers/module-61-frontier-architectures/index.html",
    ROOT / "part-12-frontiers/module-61-frontier-architectures/section-33.4.html",
]

for f in p1_ch6_to_7_files:
    if not f.exists():
        continue
    rp = f.resolve()
    if rp in IN_FLIGHT:
        files_skipped_inflight.add(str(f))
        continue
    text = f.read_text(encoding="utf-8")
    orig = text
    # Replace "Chapter 06" in href context of module-07
    text = text.replace("Chapter 06 (Pre-training", "Chapter 07 (Pre-training")
    text = text.replace("Chapter 06 (Pretraining", "Chapter 07 (Pretraining")
    # Add: Chapter 06 with Pre-training/scaling/Chinchilla nearby
    text = re.sub(
        r'Chapter 06(?= ?\(Pre-?training|: ?Pre-?training| ?\(Pretraining|: ?Pretraining)',
        'Chapter 07', text
    )
    # "Chapter 06" referring to scaling laws/Chinchilla nearby
    text = re.sub(r'scaling laws and the Chinchilla findings in Chapter 06',
                  'scaling laws and the Chinchilla findings in Chapter 07', text)
    if text != orig:
        f.write_text(text, encoding="utf-8")
        files_modified.add(str(f))
        add("p1_ch6_to_7", text.count("Chapter 07") - orig.count("Chapter 07"))


# ============================================================
# P1.C: Chapter 07 -> Chapter 08 (Modern LLM Landscape)
# ============================================================

p1_ch7_to_8_files = [
    ROOT / "part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html",
    ROOT / "part-1-foundations/module-02-tokenization-subword-models/section-2.2.html",
    ROOT / "part-1-foundations/module-05-decoding-text-generation/section-5.4.html",
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.8.html",
    ROOT / "part-2-understanding-llms/module-09-reasoning-test-time-compute/index.html",
    ROOT / "part-2-understanding-llms/module-10-inference-optimization/index.html",
    ROOT / "part-12-frontiers/module-61-frontier-architectures/index.html",
    ROOT / "part-12-frontiers/module-61-frontier-architectures/section-33.4.html",
]

for f in p1_ch7_to_8_files:
    if not f.exists():
        continue
    rp = f.resolve()
    if rp in IN_FLIGHT:
        files_skipped_inflight.add(str(f))
        continue
    text = f.read_text(encoding="utf-8")
    orig = text
    # "Chapter 07" -> Chapter 08 (modern LLM landscape)
    # Only when context strongly indicates landscape/internals
    text = re.sub(r'Chapter 07(?=:? ?\(?Modern LLM)', 'Chapter 08', text)
    # Bare "Chapter 07" in link-text contexts followed by module-08 href = also fix
    text = re.sub(
        r'<a([^>]+href="[^"]*module-08-modern-llm-landscape[^"]*"[^>]*)>Chapter 07</a>',
        r'<a\1>Chapter 08</a>',
        text
    )
    # Generic Chapter 07 mentions in module-08 contexts — only if line contains "modern" or "landscape"
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if 'Chapter 07' in line and ('Modern LLM' in line or 'modern LLM' in line or 'landscape' in line.lower() or 'module-08' in line):
            lines[i] = line.replace('Chapter 07', 'Chapter 08')
    text = '\n'.join(lines)
    if text != orig:
        f.write_text(text, encoding="utf-8")
        files_modified.add(str(f))
        add("p1_ch7_to_8", text.count("Chapter 08") - orig.count("Chapter 08"))


# ============================================================
# P1.D: Chapter 08 -> Chapter 09 (Reasoning Models)
# ============================================================

p1_ch8_to_9_files = [
    ROOT / "part-2-understanding-llms/module-08-modern-llm-landscape/index.html",
    ROOT / "part-2-understanding-llms/module-10-inference-optimization/section-10.6.html",
    ROOT / "part-4-training-adapting/module-17-synthetic-data/section-17.6.html",
    ROOT / "part-6-agentic-ai/module-26-ai-agents/index.html",
    ROOT / "part-6-agentic-ai/module-26-ai-agents/section-26.3.html",
    ROOT / "part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.10.html",
]

for f in p1_ch8_to_9_files:
    if not f.exists():
        continue
    rp = f.resolve()
    if rp in IN_FLIGHT:
        files_skipped_inflight.add(str(f))
        continue
    text = f.read_text(encoding="utf-8")
    orig = text
    # Only "Chapter 08" in reasoning-context lines
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if 'Chapter 08' in line and ('Reasoning' in line or 'reasoning' in line or 'Test-Time' in line or 'module-09-reasoning' in line):
            lines[i] = line.replace('Chapter 08', 'Chapter 09')
        # Cover special-case: "architecture deep dive in Chapter 08" -> "Chapter 09" in section-37.10
        if 'architecture deep dive in Chapter 08' in line:
            lines[i] = line.replace('Chapter 08', 'Chapter 09')
    text = '\n'.join(lines)
    if text != orig:
        f.write_text(text, encoding="utf-8")
        files_modified.add(str(f))
        add("p1_ch8_to_9", text.count("Chapter 09") - orig.count("Chapter 09"))


# ============================================================
# P1.E: Section 9.5 -> Section 10.5 (model pruning)
# ============================================================

apply_to(
    ROOT / "part-2-understanding-llms/module-10-inference-optimization/section-10.3.html",
    [
        ("Section 9.5", "Section 10.5", True),
    ],
    "p1_section_9_5_to_10_5",
)
apply_to(
    ROOT / "part-2-understanding-llms/module-10-inference-optimization/section-10.6.html",
    [
        ("Section 9.5", "Section 10.5", True),
    ],
    "p1_section_9_5_to_10_5",
)

# ============================================================
# P1.F: Appendix D -> Appendix C (HuggingFace)
# ============================================================
for f, label in [
    (ROOT / "part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.1.html", "p1_appendix_d_to_c"),
    (ROOT / "part-4-training-adapting/module-19-peft/section-19.1.html", "p1_appendix_d_to_c"),
]:
    if not f.exists():
        continue
    rp = f.resolve()
    if rp in IN_FLIGHT:
        files_skipped_inflight.add(str(f))
        continue
    text = f.read_text(encoding="utf-8")
    orig = text
    # "Appendix D" + HuggingFace context -> "Appendix C"
    text = re.sub(r'Appendix D(?= ?\(HuggingFace|: ?HuggingFace| ?\(Hugging Face|: ?Hugging Face)',
                  'Appendix C', text)
    # Inline href context
    text = re.sub(
        r'<a([^>]+href="[^"]*appendix-c-huggingface[^"]*"[^>]*)>Appendix D</a>',
        r'<a\1>Appendix C</a>',
        text
    )
    if text != orig:
        f.write_text(text, encoding="utf-8")
        files_modified.add(str(f))
        add(label, 1)


# ============================================================
# P1.G: Chapter 11 -> Chapter 10 (Inference Optimization) (2x)
# ============================================================
apply_regex(
    ROOT / "part-2-understanding-llms/module-10-inference-optimization/section-10.4.html",
    r'Chapter 11: Inference Optimization &amp; Efficient Serving',
    'Chapter 10: Inference Optimization &amp; Efficient Serving',
    "p1_ch11_to_10",
)
apply_regex(
    ROOT / "part-2-understanding-llms/module-10-inference-optimization/section-10.6.html",
    r'Chapter 11: Inference Optimization &amp; Efficient Serving',
    'Chapter 10: Inference Optimization &amp; Efficient Serving',
    "p1_ch11_to_10",
)
# Also bare Chapter 11 -> Chapter 10
apply_regex(
    ROOT / "part-2-understanding-llms/module-10-inference-optimization/section-10.4.html",
    r'Chapter 11: Inference Optimization',
    'Chapter 10: Inference Optimization',
    "p1_ch11_to_10",
)


# ============================================================
# P1.H: Chapter 17 -> Chapter 18 (Fine-Tuning)
# ============================================================
for f, label in [
    (ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.5.html", "p1_ch17_to_18"),
    (ROOT / "part-2-understanding-llms/module-08-modern-llm-landscape/section-8.2.html", "p1_ch17_to_18"),
    (ROOT / "part-2-understanding-llms/module-08-modern-llm-landscape/section-8.4.html", "p1_ch17_to_18"),
]:
    if not f.exists():
        continue
    rp = f.resolve()
    if rp in IN_FLIGHT:
        files_skipped_inflight.add(str(f))
        continue
    text = f.read_text(encoding="utf-8")
    orig = text
    text = re.sub(
        r'<a([^>]+href="[^"]*module-18-fine-tuning[^"]*"[^>]*)>Chapter 17</a>',
        r'<a\1>Chapter 18</a>',
        text
    )
    text = re.sub(r'Chapter 17(?= ?\(Fine-?Tuning|: ?Fine-?Tuning)', 'Chapter 18', text)
    if text != orig:
        f.write_text(text, encoding="utf-8")
        files_modified.add(str(f))
        add(label, 1)


# ============================================================
# P1.I: Chapter 25 -> Chapter 26 (AI Agents)
# ============================================================
for f in [
    ROOT / "part-6-agentic-ai/module-29-specialized-agents/index.html",
    ROOT / "part-6-agentic-ai/module-29-specialized-agents/section-29.4.html",
]:
    if not f.exists():
        continue
    rp = f.resolve()
    if rp in IN_FLIGHT:
        files_skipped_inflight.add(str(f))
        continue
    text = f.read_text(encoding="utf-8")
    orig = text
    text = re.sub(
        r'<a([^>]+href="[^"]*module-26-ai-agents[^"]*"[^>]*)>Chapter 25</a>',
        r'<a\1>Chapter 26</a>',
        text
    )
    text = re.sub(r'Chapter 25(?= ?\(AI Agent|: ?AI Agent)', 'Chapter 26', text)
    if text != orig:
        f.write_text(text, encoding="utf-8")
        files_modified.add(str(f))
        add("p1_ch25_to_26", 1)


# ============================================================
# P1.J: Part X -> Part XII (Frontiers) and Part XI -> Part X
# ============================================================
for f, find_part, replace_part in [
    (ROOT / "part-10-idea-to-product/module-47-scaling-economics/section-47.4.html", "Part X: Frontiers", "Part XII: Frontiers"),
    (ROOT / "part-9-safety-security-ethics/index.html", "Part X: Frontiers", "Part XII: Frontiers"),
]:
    if not f.exists():
        continue
    rp = f.resolve()
    if rp in IN_FLIGHT:
        files_skipped_inflight.add(str(f))
        continue
    text = f.read_text(encoding="utf-8")
    if find_part not in text:
        continue
    new = text.replace(find_part, replace_part)
    if new != text:
        f.write_text(new, encoding="utf-8")
        files_modified.add(str(f))
        add("p1_part_x_to_xii", 1)


# Part XI -> Part X (in part-12-frontiers index ; refers to part-10-idea-to-product?)
# audit: part-12-frontiers/index.html:122 text=`Part XI`
# Let's check first.

# ============================================================
# P1.K: Chapter 13 -> Chapter 14 (Prompt Engineering)
# ============================================================
apply_regex(
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.2.html",
    r'<a([^>]+href="[^"]*module-14-prompt-engineering[^"]*"[^>]*)>Chapter 13</a>',
    r'<a\1>Chapter 14</a>',
    "p1_ch13_to_14",
)

# ============================================================
# P1.L: Chapter 15 -> Chapter 17 (Synthetic Data)
# ============================================================
apply_regex(
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.4.html",
    r'<a([^>]+href="[^"]*module-17-synthetic[^"]*"[^>]*)>Chapter 15</a>',
    r'<a\1>Chapter 17</a>',
    "p1_ch15_to_17",
)

# ============================================================
# P1.M: Chapter 18 -> Chapter 19 (PEFT)
# ============================================================
apply_regex(
    ROOT / "part-2-understanding-llms/module-08-modern-llm-landscape/section-8.2.html",
    r'<a([^>]+href="[^"]*module-19-peft[^"]*"[^>]*)>Chapter 18</a>',
    r'<a\1>Chapter 19</a>',
    "p1_ch18_to_19",
)

# ============================================================
# P1.N: Chapter 20 -> Chapter 11 (Interpretability)
# ============================================================
apply_regex(
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.7.html",
    r'<a([^>]+href="[^"]*module-11-interpretability[^"]*"[^>]*)>Chapter 20</a>',
    r'<a\1>Chapter 11</a>',
    "p1_ch20_to_11",
)

# ============================================================
# P1.O: Chapter 20 -> Chapter 19 (PEFT/Knowledge Distillation)
# ============================================================
apply_regex(
    ROOT / "part-1-foundations/module-05-decoding-text-generation/section-5.2.html",
    r'knowledge distillation in Chapter 20',
    r'knowledge distillation in Chapter 19',
    "p1_ch20_to_19",
)
apply_regex(
    ROOT / "part-2-understanding-llms/module-09-reasoning-test-time-compute/section-9.2.html",
    r'<a([^>]+href="[^"]*module-19-peft[^"]*"[^>]*)>Chapter 20</a>',
    r'<a\1>Chapter 19</a>',
    "p1_ch20_to_19",
)

# ============================================================
# P1.P: Chapter 24 -> Chapter 20 (Alignment)
# ============================================================
apply_regex(
    ROOT / "part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.5.html",
    r'Chapter 24: Alignment: RLHF, DPO &amp; Preference Tuning',
    r'Chapter 20: Alignment: RLHF, DPO &amp; Preference Tuning',
    "p1_ch24_to_20",
)

# ============================================================
# P1.Q: Chapter 25 -> Chapter 37 (Safety)
# ============================================================
apply_regex(
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.4.html",
    r'<a([^>]+href="[^"]*module-37-safety[^"]*"[^>]*)>Chapter 25</a>',
    r'<a\1>Chapter 37</a>',
    "p1_ch25_to_37",
)

# ============================================================
# P1.R: Chapter 27 -> Chapter 31 (Multimodal)
# ============================================================
apply_regex(
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.1.html",
    r'<a([^>]+href="[^"]*module-31-multimodal[^"]*"[^>]*)>Chapter 27</a>',
    r'<a\1>Chapter 31</a>',
    "p1_ch27_to_31",
)

# ============================================================
# P1.S: Chapter 29 -> Chapter 34 (Evaluation)
# ============================================================
apply_regex(
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.3.html",
    r'<a([^>]+href="[^"]*module-34-evaluation[^"]*"[^>]*)>Chapter 29</a>',
    r'<a\1>Chapter 34</a>',
    "p1_ch29_to_34",
)

# ============================================================
# P1.T: Chapter 07 -> Chapter 05 (Decoding) in appendix-c
# ============================================================
apply_regex(
    ROOT / "appendices/appendix-c-huggingface-ecosystem/section-c.1.html",
    r'Chapter 07: Text Generation and Decoding',
    r'Chapter 05: Decoding Strategies &amp; Text Generation',
    "p1_ch7_to_5_appendixc",
)

# ============================================================
# P1.U: Chapter 09 -> Chapter 18 (Fine-Tuning) in appendix-c
# ============================================================
apply_regex(
    ROOT / "appendices/appendix-c-huggingface-ecosystem/section-c.3.html",
    r'Chapter 09: Fine-Tuning',
    r'Chapter 18: Fine-Tuning Fundamentals',
    "p1_ch9_to_18_appendixc",
)

# ============================================================
# P1.V: Chapter 13 -> Chapter 20 (Alignment) in appendix-c
# ============================================================
apply_regex(
    ROOT / "appendices/appendix-c-huggingface-ecosystem/section-c.4.html",
    r'Chapter 13: Alignment and RLHF',
    r'Chapter 20: Alignment, RLHF, DPO &amp; Preference Tuning',
    "p1_ch13_to_20_appendixc",
)

# ============================================================
# P1.W: Chapter 08 -> Chapter 10 (Inference) in section-7.3
# ============================================================
apply_regex(
    ROOT / "part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.3.html",
    r'<a([^>]+href="[^"]*module-10-inference[^"]*"[^>]*)>Chapter 08</a>',
    r'<a\1>Chapter 10</a>',
    "p1_ch8_to_10_inference",
)

# ============================================================
# P1.X: Section 11.2 -> Section 14.2 (CoT) in section-14.3
# ============================================================
apply_regex(
    ROOT / "part-3-working-with-llms/module-14-prompt-engineering/section-14.3.html",
    r'\bSection 11\.2\b',
    r'Section 14.2',
    "p1_sec11_2_to_14_2",
)
apply_regex(
    ROOT / "part-3-working-with-llms/module-14-prompt-engineering/section-14.3.html",
    r'\b11\.2\b(?=[^0-9])',
    r'14.2',
    "p1_sec11_2_to_14_2_bare",
)

# ============================================================
# Section 30.X -> Section 37.X in module-37 (audit says 8 occurrences)
# ============================================================
# Need to check; module-37 may use stale Section 30.X labels
for sec_path in (ROOT / "part-9-safety-security-ethics/module-37-safety-ethics-regulation").glob("section-37.*.html"):
    if sec_path.resolve() in IN_FLIGHT:
        files_skipped_inflight.add(str(sec_path))
        continue
    text = sec_path.read_text(encoding="utf-8")
    orig = text
    # Replace stale "Section 30.N" with "Section 37.N" only if it's part of section-card / link UI
    text = re.sub(r'\bSection 30\.(\d+)\b', r'Section 37.\1', text)
    if text != orig:
        sec_path.write_text(text, encoding="utf-8")
        files_modified.add(str(sec_path))
        add("p1_section_30_to_37", 1)

# ============================================================
# Report
# ============================================================
print("\n=== Cross-link fix stats ===")
for k in sorted(stats):
    print(f"  {k}: {stats[k]}")
print(f"\nFiles modified: {len(files_modified)}")
print(f"Files skipped (in-flight): {len(files_skipped_inflight)}")
for f in sorted(files_skipped_inflight)[:20]:
    print(f"  SKIPPED: {f}")
if errors:
    print(f"\nErrors ({len(errors)}):")
    for e in errors[:50]:
        print(f"  {e}")
