"""
Fix stale section-num spans in chapter index files.
For each stale chapter index in the audit, rewrite the chapter prefix on all
<span class="section-num">N.M</span> spans.
"""
import re
from pathlib import Path

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")

# (relative path, stale prefix, target prefix)
FIXES = [
    # Part 2
    ("part-2-understanding-llms/module-07-pretraining-scaling-laws/index.html", 6, 7),
    ("part-2-understanding-llms/module-08-modern-llm-landscape/index.html", 7, 8),
    ("part-2-understanding-llms/module-09-reasoning-test-time-compute/index.html", 8, 9),
    ("part-2-understanding-llms/module-10-inference-optimization/index.html", 9, 10),
    ("part-2-understanding-llms/module-11-interpretability/index.html", 10, 11),
    # Part 3
    ("part-3-working-with-llms/module-13-llm-apis/index.html", 11, 13),
    ("part-3-working-with-llms/module-14-prompt-engineering/index.html", 12, 14),
    ("part-3-working-with-llms/module-15-hybrid-ml-llm/index.html", 13, 15),
    # Part 4
    ("part-4-training-adapting/module-17-synthetic-data/index.html", 14, 17),
    ("part-4-training-adapting/module-18-fine-tuning-fundamentals/index.html", 15, 18),
    ("part-4-training-adapting/module-19-peft/index.html", 16, 19),
    ("part-4-training-adapting/module-20-alignment-rlhf-dpo/index.html", 17, 20),
    # Part 5
    ("part-5-retrieval-conversation/module-22-embeddings-vector-db/index.html", 18, 22),
    ("part-5-retrieval-conversation/module-23-rag/index.html", 19, 23),
    ("part-5-retrieval-conversation/module-24-conversational-ai/index.html", 20, 24),
    # Part 6
    ("part-6-agentic-ai/module-26-ai-agents/index.html", 21, 26),
    ("part-6-agentic-ai/module-27-tool-use-protocols/index.html", 22, 27),
    ("part-6-agentic-ai/module-28-multi-agent-systems/index.html", 23, 28),
    ("part-6-agentic-ai/module-29-specialized-agents/index.html", 24, 29),
    # Part 7
    ("part-7-multimodal-generation/module-31-multimodal/index.html", 26, 31),
    # Part 8
    ("part-8-evaluation-production/module-34-evaluation-observability/index.html", 28, 34),
    ("part-8-evaluation-production/module-35-production-engineering/index.html", 29, 35),
    # Part 9
    ("part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html", 30, 37),
    # Part 10
    ("part-10-idea-to-product/module-45-prototype-to-production/index.html", 34, 45),
    ("part-10-idea-to-product/module-48-shipping-deploying/index.html", 35, 48),
]

count = 0
for rel, stale, target in FIXES:
    path = ROOT / rel
    if not path.exists():
        print(f"  MISSING: {rel}")
        continue
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r'(<span class="section-num">)' + re.escape(str(stale)) + r'(\.\d+)(</span>)'
    )
    def replace(m):
        return f'{m.group(1)}{target}{m.group(2)}{m.group(3)}'
    new_text, n = pattern.subn(replace, text)
    if n > 0:
        path.write_text(new_text, encoding="utf-8")
        print(f"  {rel}: rewrote {n} section-num spans ({stale}.x -> {target}.x)")
        count += n
    else:
        print(f"  {rel}: no stale spans found")

print(f"\nTotal section-card spans rewritten: {count}")
