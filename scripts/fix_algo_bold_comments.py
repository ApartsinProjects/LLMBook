"""Fix <b> tags to algo-line-keyword and add algo-line-comment in algorithm callout blocks."""

import re
from pathlib import Path

BASE = Path(r"E:\Projects\LLMCourse")

target_files = [
    "part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html",
    "part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html",
    "part-5-retrieval-conversation/module-20-rag/section-20.1.html",
    "part-6-agentic-ai/module-22-ai-agents/section-22.1.html",
    "part-5-retrieval-conversation/module-19-rag/section-19.1.html",
    "part-6-agentic-ai/module-24-multi-agent-systems/section-24.2.html",
    "part-8-evaluation-production/module-29-evaluation-observability/section-29.2.html",
]

fixed_count = 0
for rel in target_files:
    f = BASE / Path(rel)
    if not f.exists():
        print(f"  NOT FOUND: {rel}")
        continue

    text = f.read_text(encoding="utf-8")
    orig = text
    lines = text.split("\n")
    new_lines = []

    in_algo = False
    in_pre = False

    for line in lines:
        if 'class="callout algorithm"' in line:
            in_algo = True
        if in_algo and "<pre" in line:
            in_pre = True
        if in_algo and in_pre:
            # Replace <b>text</b> with algo-line-keyword span
            if "<b>" in line and "algo-line-keyword" not in line:
                line = re.sub(
                    r"<b>([^<]+)</b>",
                    r'<span class="algo-line-keyword">\1</span>',
                    line,
                )
            # Add algo-line-comment to comment lines
            if "algo-line-comment" not in line:
                stripped = re.sub(r"<[^>]+>", "", line).strip()
                if stripped.startswith("//"):
                    cm = re.search(r"(//[^<]*)", line)
                    if cm:
                        c = cm.group(1)
                        line = line.replace(c, f'<span class="algo-line-comment">{c}</span>', 1)
                elif stripped.startswith("#") and not stripped.startswith("#!"):
                    cm = re.search(r"(#[^<]*)", line)
                    if cm:
                        c = cm.group(1)
                        line = line.replace(c, f'<span class="algo-line-comment">{c}</span>', 1)
        if in_pre and "</pre>" in line:
            in_pre = False
        # Reset algo flag when we hit the closing div after the pre
        if in_algo and not in_pre and "</div>" in line:
            in_algo = False

        new_lines.append(line)

    new_text = "\n".join(new_lines)
    if new_text != orig:
        f.write_text(new_text, encoding="utf-8")
        fixed_count += 1
        bold_fixes = orig.count("<b>") - new_text.count("<b>")
        comment_adds = new_text.count("algo-line-comment") - orig.count("algo-line-comment")
        print(f"  Fixed: {rel} ({bold_fixes} bold->keyword, {comment_adds} comments)")
    else:
        print(f"  No changes: {rel}")

print(f"\nTotal: {fixed_count} files updated")
