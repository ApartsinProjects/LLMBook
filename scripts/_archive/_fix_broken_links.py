"""Fix all broken internal links across HTML files.

Handles five categories of broken links:
1. Leading zero mismatch: section-0X.Y -> section-X.Y (modules 0-9)
2. Old directory names from renumbering (full path replacements)
3. Wrong section file references within same module directory
4. Section number mismatch after module renumbering (cross-module refs)
5. Cross-part relative path fixes (../module-X when module is in different part)
"""

import os
import re
from pathlib import Path

ROOT = Path(r"E:/Projects/LLMCourse")

# ── Category 1: Leading zero mismatch ──────────────────────────────────
CAT1_PATTERN = re.compile(r'(href="[^"]*?)section-0(\d\.\d+\.html)')

# ── Category 2: Old directory names from renumbering ───────────────────
CAT2_REPLACEMENTS = [
    ("part-6-agents-applications/module-22-ai-agents/", "part-6-agentic-ai/module-22-ai-agents/"),
    ("part-6-agents-applications/module-25-evaluation-observability/", "part-8-evaluation-production/module-29-evaluation-observability/"),
    ("part-6-agents-applications/module-21-ai-agents/", "part-6-agentic-ai/module-22-ai-agents/"),
    ("part-4-training-adapting/module-14-peft/", "part-4-training-adapting/module-15-peft/"),
    ("part-4-training-adapting/module-13-fine-tuning-fundamentals/", "part-4-training-adapting/module-14-fine-tuning-fundamentals/"),
    ("part-4-training-adapting/module-12-synthetic-data/", "part-4-training-adapting/module-13-synthetic-data/"),
    ("part-2-understanding-llms/module-08-inference-optimization/", "part-2-understanding-llms/module-09-inference-optimization/"),
    ("part-3-working-with-llms/module-10-prompt-engineering/", "part-3-working-with-llms/module-11-prompt-engineering/"),
    ("part-4-training-adapting/module-16-alignment-rlhf-dpo/", "part-4-training-adapting/module-17-alignment-rlhf-dpo/"),
    ("part-4-training-adapting/module-15-distillation-merging/", "part-4-training-adapting/module-16-distillation-merging/"),
    ("part-5-retrieval-conversation/module-18-embeddings-vector-db/", "part-5-retrieval-conversation/module-19-embeddings-vector-db/"),
    ("part-5-retrieval-conversation/module-19-rag/", "part-5-retrieval-conversation/module-20-rag/"),
    ("part-4-training-adapting/module-17-interpretability/", "part-2-understanding-llms/module-18-interpretability/"),
    ("part-4-training-adapting/module-18-interpretability/", "part-2-understanding-llms/module-18-interpretability/"),
    ("part-3-working-with-llms/module-09-llm-apis/", "part-3-working-with-llms/module-10-llm-apis/"),
    ("part-3-working-with-llms/module-11-hybrid-ml-llm/", "part-3-working-with-llms/module-12-hybrid-ml-llm/"),
    ("part-7-production-strategy/module-26-production-safety-ethics/", "part-9-safety-strategy/module-32-safety-ethics-regulation/"),
    ("part-6-agentic-ai/module-23-multi-agent-systems/", "part-6-agentic-ai/module-24-multi-agent-systems/"),
    # Residual old module name that lands in wrong part
    ("part-8-evaluation-production/module-32-safety-ethics-regulation/", "part-9-safety-strategy/module-32-safety-ethics-regulation/"),
]

# ── Category 3: Wrong section file references (same-module only) ───────
CAT3_FIXES = [
    ("module-30-observability-monitoring", "section-26.", "section-30."),
    ("module-30-observability-monitoring", "section-27.", "section-30."),
    ("module-34-emerging-architectures", "section-30.", "section-34."),
    ("module-34-emerging-architectures", "section-31.", "section-34."),
    ("module-35-ai-society", "section-30.", "section-35."),
    ("module-35-ai-society", "section-32.", "section-35."),
    ("module-25-specialized-agents", "section-22.", "section-25."),
]

# ── Category 4: Section number mismatch after module renumbering ───────
SECTION_RENUM = [
    ("module-09-inference-optimization/section-8.", "module-09-inference-optimization/section-9."),
    ("module-10-llm-apis/section-9.", "module-10-llm-apis/section-10."),
    ("module-11-prompt-engineering/section-10.", "module-11-prompt-engineering/section-11."),
    ("module-12-hybrid-ml-llm/section-11.", "module-12-hybrid-ml-llm/section-12."),
    ("module-13-synthetic-data/section-12.", "module-13-synthetic-data/section-13."),
    ("module-14-fine-tuning-fundamentals/section-13.", "module-14-fine-tuning-fundamentals/section-14."),
    ("module-15-peft/section-14.", "module-15-peft/section-15."),
    ("module-16-distillation-merging/section-15.", "module-16-distillation-merging/section-16."),
    ("module-17-alignment-rlhf-dpo/section-16.", "module-17-alignment-rlhf-dpo/section-17."),
    ("module-18-interpretability/section-17.", "module-18-interpretability/section-18."),
    ("module-19-embeddings-vector-db/section-18.", "module-19-embeddings-vector-db/section-19."),
    ("module-20-rag/section-19.", "module-20-rag/section-20."),
    ("module-22-ai-agents/section-21.", "module-22-ai-agents/section-22."),
    ("module-24-multi-agent-systems/section-23.", "module-24-multi-agent-systems/section-24."),
    ("module-29-evaluation-observability/section-25.", "module-29-evaluation-observability/section-29."),
    ("module-32-safety-ethics-regulation/section-26.", "module-32-safety-ethics-regulation/section-32."),
    ("module-32-safety-ethics-regulation/section-35.", "module-32-safety-ethics-regulation/section-32."),
]

# ── Category 5: Cross-part relative path fixes ────────────────────────
MODULE_LOCATIONS = {
    "module-15-peft": "part-4-training-adapting",
    "module-17-alignment-rlhf-dpo": "part-4-training-adapting",
    "module-18-interpretability": "part-2-understanding-llms",
    "module-22-ai-agents": "part-6-agentic-ai",
    "module-23-multi-agent-systems": "part-6-agentic-ai",
    "module-24-multi-agent-systems": "part-6-agentic-ai",
    "module-27-multimodal": "part-7-multimodal-applications",
    "module-28-llm-applications": "part-7-multimodal-applications",
    "module-29-evaluation-observability": "part-8-evaluation-production",
    "module-30-observability-monitoring": "part-8-evaluation-production",
    "module-31-production-engineering": "part-8-evaluation-production",
    "module-32-safety-ethics-regulation": "part-9-safety-strategy",
    "module-33-strategy-product-roi": "part-9-safety-strategy",
}

CROSS_PART_PATTERN = re.compile(r'(href=")\.\./(' + '|'.join(
    re.escape(m) for m in MODULE_LOCATIONS.keys()
) + r')(/[^"]*")')


def find_html_files(root):
    result = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ('node_modules', '.git')]
        for f in filenames:
            if f.endswith('.html'):
                result.append(Path(dirpath) / f)
    return result


def get_part_dir(filepath):
    rel = filepath.relative_to(ROOT)
    for p in rel.parts:
        if p.startswith("part-"):
            return p
    return None


def fix_category1(content):
    count = 0
    def replacer(m):
        nonlocal count
        count += 1
        return m.group(1) + "section-" + m.group(2)
    new_content = CAT1_PATTERN.sub(replacer, content)
    return new_content, count


def fix_category2(content):
    count = 0
    for old, new in CAT2_REPLACEMENTS:
        n = content.count(old)
        if n > 0:
            content = content.replace(old, new)
            count += n
    return content, count


def fix_category3(content, filepath):
    count = 0
    parent_name = filepath.parent.name
    for module_dir, old_prefix, new_prefix in CAT3_FIXES:
        if parent_name == module_dir:
            old_pattern = re.compile(r'(href="[^"]*?)' + re.escape(old_prefix))
            def make_replacer(np):
                def replacer(m):
                    nonlocal count
                    count += 1
                    return m.group(1) + np
                return replacer
            content = old_pattern.sub(make_replacer(new_prefix), content)
    return content, count


def fix_category4(content):
    count = 0
    for old, new in SECTION_RENUM:
        n = content.count(old)
        if n > 0:
            content = content.replace(old, new)
            count += n
    return content, count


def fix_category5(content, filepath):
    count = 0
    source_part = get_part_dir(filepath)
    if not source_part:
        return content, 0

    def replacer(m):
        nonlocal count
        prefix = m.group(1)
        module_name = m.group(2)
        suffix = m.group(3)
        target_part = MODULE_LOCATIONS.get(module_name)
        if target_part is None or target_part == source_part:
            return m.group(0)
        count += 1
        return f'{prefix}../../{target_part}/{module_name}{suffix}'

    content = CROSS_PART_PATTERN.sub(replacer, content)
    return content, count


def main():
    html_files = find_html_files(ROOT)
    print(f"Found {len(html_files)} HTML files")

    totals = [0, 0, 0, 0, 0]
    files_modified = 0

    for fpath in sorted(html_files):
        content = fpath.read_text(encoding='utf-8', errors='replace')
        original = content

        content, c1 = fix_category1(content)
        content, c2 = fix_category2(content)
        content, c3 = fix_category3(content, fpath)
        content, c4 = fix_category4(content)
        content, c5 = fix_category5(content, fpath)

        if content != original:
            fpath.write_text(content, encoding='utf-8')
            files_modified += 1
            totals[0] += c1
            totals[1] += c2
            totals[2] += c3
            totals[3] += c4
            totals[4] += c5
            rel = fpath.relative_to(ROOT)
            print(f"  Fixed {rel}: cat1={c1}, cat2={c2}, cat3={c3}, cat4={c4}, cat5={c5}")

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Files scanned:    {len(html_files)}")
    print(f"Files modified:   {files_modified}")
    print(f"Cat 1 (leading zero):       {totals[0]}")
    print(f"Cat 2 (old directories):    {totals[1]}")
    print(f"Cat 3 (same-module section):{totals[2]}")
    print(f"Cat 4 (cross-mod section):  {totals[3]}")
    print(f"Cat 5 (cross-part paths):   {totals[4]}")
    print(f"Total fixes:                {sum(totals)}")


if __name__ == "__main__":
    main()
