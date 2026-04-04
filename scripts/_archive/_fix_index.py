#!/usr/bin/env python3
"""
Fix index.html chapter numbering based on the actual directory paths referenced.
Uses the topic name in each href to determine the correct chapter number.
Also adds missing entries for Ch 08 (Reasoning) and Ch 30 (Frontiers).
"""
import re
import os

ROOT = r"E:\Projects\LLMCourse"
INDEX = os.path.join(ROOT, "index.html")

# Canonical mapping: directory topic suffix -> correct chapter number
TOPIC_TO_NUM = {
    "ml-pytorch-foundations": 0,
    "foundations-nlp-text-representation": 1,
    "tokenization-subword-models": 2,
    "sequence-models-attention": 3,
    "transformer-architecture": 4,
    "decoding-text-generation": 5,
    "pretraining-scaling-laws": 6,
    "modern-llm-landscape": 7,
    "reasoning-test-time-compute": 8,
    "inference-optimization": 9,
    "llm-apis": 10,
    "prompt-engineering": 11,
    "hybrid-ml-llm": 12,
    "synthetic-data": 13,
    "fine-tuning-fundamentals": 14,
    "peft": 15,
    "distillation-merging": 16,
    "alignment-rlhf-dpo": 17,
    "interpretability": 18,
    "embeddings-vector-db": 19,
    "rag": 20,
    "conversational-ai": 21,
    "ai-agents": 22,
    "multi-agent-systems": 23,
    "multimodal": 24,
    "llm-applications": 25,
    "evaluation-observability": 26,
    "production-engineering": 27,
    "safety-ethics-regulation": 28,
    "strategy-product-roi": 29,
    "frontiers": 30,
}

with open(INDEX, 'r', encoding='utf-8') as f:
    text = f.read()

# Strategy: find all module directory references and fix their numbers

# Step 1: Fix module directory paths in hrefs
# Pattern: module-XX-topicname where XX might be wrong
for topic, correct_num in TOPIC_TO_NUM.items():
    # Match any module-NN-topic pattern and replace NN with correct number
    pattern = rf'module-\d+[a-z]?-{re.escape(topic)}'
    replacement = f'module-{correct_num:02d}-{topic}'
    text = re.sub(pattern, replacement, text)

# Step 2: Fix section file references
# Pattern: section-X.N.html where X might be wrong, associated with a specific module
# We need to find section refs near their module refs
for topic, correct_num in TOPIC_TO_NUM.items():
    # Don't touch sections for chapters 0-7 (they were never renumbered)
    if correct_num <= 7:
        continue
    # We need to figure out what wrong number each section might have
    # The double-run could have shifted by +1 extra
    for wrong_num in range(correct_num - 2, correct_num + 3):
        if wrong_num == correct_num:
            continue
        if wrong_num < 0:
            continue
        # Fix section-WRONG.N -> section-CORRECT.N only near the module's context
        # Simple approach: just fix globally since section numbers should be unique
        # to their chapter
        old_section = f"section-{wrong_num}."
        new_section = f"section-{correct_num}."
        # But this is dangerous globally. Only fix within href to the right module dir
        pattern = rf'(module-{correct_num:02d}-{re.escape(topic)}/section-){wrong_num}\.'
        replacement = rf'\g<1>{correct_num}.'
        text = re.sub(pattern, replacement, text)

# Step 3: Fix id="chN" attributes based on surrounding content
# Find each book-chapter div and fix its id based on the module it references
def fix_chapter_card_id(match):
    block = match.group(0)
    # Find the module reference in this block
    module_match = re.search(r'module-(\d+)-(\S+?)/', block)
    if module_match:
        num = int(module_match.group(1))
        # Fix the id
        block = re.sub(r'id="ch\d+"', f'id="ch{num}"', block)
        # Fix Chapter NN display
        block = re.sub(r'<span class="chapter-num">Chapter \d+</span>',
                       f'<span class="chapter-num">Chapter {num:02d}</span>', block)
        # Fix lesson-num spans
        for old_lesson in re.findall(r'<span class="lesson-num">(\d+)\.\d+</span>', block):
            old_n = int(old_lesson)
            if old_n != num:
                block = re.sub(rf'<span class="lesson-num">{old_n}\.(\d+)</span>',
                              rf'<span class="lesson-num">{num}.\1</span>', block)
        # Fix section hrefs within the block
        for old_sec in re.findall(rf'section-(\d+)\.\d+\.html', block):
            old_n = int(old_sec)
            if old_n != num:
                block = re.sub(rf'section-{old_n}\.(\d+)\.html',
                              rf'section-{num}.\1.html', block)
    return block

# Match each book-chapter div (they span many lines)
text = re.sub(
    r'<div class="book-chapter" id="ch\d+">\s*.*?(?=<div class="book-chapter"|<div style="margin: 2rem)',
    fix_chapter_card_id,
    text,
    flags=re.DOTALL
)

# Step 4: Fix TOC entries
# Pattern: <a class="toc-item" href="#chN"><span class="toc-num">NN</span> Title</a>
# We need to match each TOC entry to the right chapter
# Strategy: fix based on the chapter card ids we just corrected
toc_fixes = {
    "Inference Optimization": (9, "09"),
    "Working with LLM APIs": (10, "10"),
    "Prompt Engineering": (11, "11"),
    "Hybrid ML+LLM": (12, "12"),
    "Synthetic Data": (13, "13"),
    "Fine-Tuning": (14, "14"),
    "Parameter-Efficient": (15, "15"),
    "Knowledge Distillation": (16, "16"),
    "Alignment": (17, "17"),
    "Interpretability": (18, "18"),
    "Embeddings": (19, "19"),
    "Retrieval-Augmented": (20, "20"),
    "Conversational AI": (21, "21"),
    "AI Agents": (22, "22"),
    "Multi-Agent": (23, "23"),
    "Multimodal": (24, "24"),
    "LLM Applications": (25, "25"),
    "Evaluation": (26, "26"),
    "Production Engineering": (27, "27"),
    "Safety, Ethics": (28, "28"),
    "LLM Strategy": (29, "29"),
}

for title_fragment, (correct_id, correct_toc) in toc_fixes.items():
    # Fix: <a class="toc-item" href="#chWRONG"><span class="toc-num">WRONG</span> ...Title...
    pattern = rf'(<a class="toc-item" href="#ch)\d+("><span class="toc-num">)\d+(</span> [^<]*{re.escape(title_fragment)})'
    replacement = rf'\g<1>{correct_id}\g<2>{correct_toc}\g<3>'
    text = re.sub(pattern, replacement, text)

# Step 5: Add missing TOC entry for Ch 08 (Reasoning)
# Insert after Ch 07 line
if "Reasoning" not in text.split("</div>")[0]:  # Check TOC area
    text = text.replace(
        '<a class="toc-item" href="#ch7"><span class="toc-num">07</span> Modern LLM Landscape &amp; Model Internals</a>',
        '<a class="toc-item" href="#ch7"><span class="toc-num">07</span> Modern LLM Landscape &amp; Model Internals</a>\n            <a class="toc-item" href="#ch8"><span class="toc-num">08</span> Reasoning Models &amp; Test-Time Compute</a>'
    )

# Step 6: Add missing TOC entry for Ch 30 (Frontiers)
if "Frontiers" not in text.split("Appendices")[0]:
    text = text.replace(
        '<a class="toc-item" href="#ch29"><span class="toc-num">29</span> LLM Strategy, Product Management &amp; ROI</a>',
        '<a class="toc-item" href="#ch29"><span class="toc-num">29</span> LLM Strategy, Product Management &amp; ROI</a>\n            <a class="toc-item" href="#ch30"><span class="toc-num">30</span> Frontiers: Open Problems &amp; the Road Ahead</a>'
    )

# Step 7: Fix the HTML comment chapter numbers
text = re.sub(r'<!-- CHAPTER 8: Inference', '<!-- CHAPTER 9: Inference', text)

with open(INDEX, 'w', encoding='utf-8', newline='') as f:
    f.write(text)

print("Fixed index.html:")
print("  - Module directory paths corrected")
print("  - Section file references corrected")
print("  - Chapter card IDs and numbers corrected")
print("  - TOC entry numbers corrected")
print("  - Added Ch 08 (Reasoning) TOC entry")
print("  - Added Ch 30 (Frontiers) TOC entry")
