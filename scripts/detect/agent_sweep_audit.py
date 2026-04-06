"""
Agent sweep audit for Parts 3-4: identifies gaps in cross-references,
callouts, code pedagogy, and prose pacing across all section files.
"""
import re
import os
from pathlib import Path
from collections import defaultdict

ROOT = Path(r"E:/Projects/LLMCourse")

PART3_DIRS = [
    ROOT / "part-3-working-with-llms" / "module-10-llm-apis",
    ROOT / "part-3-working-with-llms" / "module-11-prompt-engineering",
    ROOT / "part-3-working-with-llms" / "module-12-hybrid-ml-llm",
]
PART4_DIRS = [
    ROOT / "part-4-training-adapting" / "module-13-synthetic-data",
    ROOT / "part-4-training-adapting" / "module-14-fine-tuning-fundamentals",
    ROOT / "part-4-training-adapting" / "module-15-peft",
    ROOT / "part-4-training-adapting" / "module-16-distillation-merging",
    ROOT / "part-4-training-adapting" / "module-17-alignment-rlhf-dpo",
]

ALL_DIRS = PART3_DIRS + PART4_DIRS

def get_section_files():
    files = []
    for d in ALL_DIRS:
        if d.exists():
            for f in sorted(d.glob("section-*.html")):
                files.append(f)
    return files

def audit_file(fpath):
    text = fpath.read_text(encoding="utf-8", errors="replace")
    results = {}
    results["file"] = str(fpath.relative_to(ROOT))

    # 1. Cross-references: count <a> tags with href pointing to other chapters
    # Exclude nav footer links and same-chapter links
    chapter_dir = fpath.parent.name  # e.g. module-10-llm-apis
    cross_refs = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>', text)
    cross_chapter = []
    for href in cross_refs:
        # Skip anchors, external, same-chapter, nav links
        if href.startswith("#") or href.startswith("http"):
            continue
        if "module-" in href and chapter_dir not in href:
            cross_chapter.append(href)
    results["cross_refs"] = len(cross_chapter)

    # 2. Callout types present
    callout_types = re.findall(r'class="callout\s+(\w[\w-]*)"', text)
    results["callout_types"] = list(set(callout_types))
    results["has_key_insight"] = "key-insight" in callout_types
    results["has_practical_example"] = "practical-example" in callout_types
    results["has_fun_note"] = "fun-note" in callout_types

    # 3. Code blocks and captions
    code_blocks = re.findall(r'<pre><code', text) or re.findall(r'<pre[^>]*><code', text)
    code_count = len(code_blocks)
    caption_count = len(re.findall(r'class="code-caption"', text))
    results["code_blocks"] = code_count
    results["code_captions"] = caption_count
    results["missing_captions"] = max(0, code_count - caption_count)

    # 4. Check for heading directly followed by code (no prose bridge)
    heading_to_code = re.findall(r'</h[23]>\s*\n\s*<pre', text)
    results["heading_to_code"] = len(heading_to_code)

    # 5. Prose monotony: find 3+ consecutive <p> tags without any visual break
    # (no callout, figure, pre, table, div between them)
    paragraphs = re.split(r'(<(?:div|figure|pre|table|blockquote|svg|h[1-6])[^>]*>)', text)
    consecutive_p = 0
    max_consecutive_p = 0
    for chunk in paragraphs:
        if chunk.strip().startswith('<p') or chunk.strip().startswith('<p>'):
            consecutive_p += 1
        elif re.match(r'<(div|figure|pre|table|blockquote|svg|h[1-6])', chunk.strip()):
            max_consecutive_p = max(max_consecutive_p, consecutive_p)
            consecutive_p = 0
    max_consecutive_p = max(max_consecutive_p, consecutive_p)
    # Alternative: count runs of <p>...</p> with nothing but whitespace between
    p_runs = re.findall(r'((?:</p>\s*<p[^>]*>){3,})', text)
    results["long_p_runs"] = len(p_runs)

    # 6. Em dashes check
    em_dashes = len(re.findall(r'\u2014', text))
    double_dashes = len(re.findall(r'(?<!\-)--(?!>)(?!\-)', text))
    results["em_dashes"] = em_dashes
    results["double_dashes"] = double_dashes

    return results

def main():
    files = get_section_files()
    print(f"Auditing {len(files)} section files...\n")

    # Summary categories
    need_cross_refs = []
    need_key_insight = []
    need_practical = []
    need_fun_note = []
    need_captions = []
    have_heading_to_code = []
    have_long_p_runs = []
    have_em_dashes = []

    for f in files:
        r = audit_file(f)
        fname = r["file"]

        if r["cross_refs"] < 3:
            need_cross_refs.append((fname, r["cross_refs"]))
        if not r["has_key_insight"]:
            need_key_insight.append(fname)
        if not r["has_practical_example"]:
            need_practical.append(fname)
        if not r["has_fun_note"]:
            need_fun_note.append(fname)
        if r["missing_captions"] > 0:
            need_captions.append((fname, r["code_blocks"], r["code_captions"]))
        if r["heading_to_code"] > 0:
            have_heading_to_code.append((fname, r["heading_to_code"]))
        if r["long_p_runs"] > 0:
            have_long_p_runs.append((fname, r["long_p_runs"]))
        if r["em_dashes"] > 0 or r["double_dashes"] > 0:
            have_em_dashes.append((fname, r["em_dashes"], r["double_dashes"]))

    print("=== CROSS-REFERENCES (< 3 cross-chapter links) ===")
    for fname, count in need_cross_refs:
        print(f"  {fname}: {count} cross-chapter links")

    print(f"\n=== MISSING KEY-INSIGHT CALLOUT ({len(need_key_insight)} files) ===")
    for fname in need_key_insight:
        print(f"  {fname}")

    print(f"\n=== MISSING PRACTICAL-EXAMPLE CALLOUT ({len(need_practical)} files) ===")
    for fname in need_practical:
        print(f"  {fname}")

    print(f"\n=== MISSING FUN-NOTE CALLOUT ({len(need_fun_note)} files) ===")
    for fname in need_fun_note:
        print(f"  {fname}")

    print(f"\n=== MISSING CODE CAPTIONS ({len(need_captions)} files) ===")
    for fname, blocks, caps in need_captions:
        print(f"  {fname}: {blocks} code blocks, {caps} captions")

    print(f"\n=== HEADING -> CODE (no prose bridge) ({len(have_heading_to_code)} files) ===")
    for fname, count in have_heading_to_code:
        print(f"  {fname}: {count} occurrences")

    print(f"\n=== LONG PARAGRAPH RUNS (3+ consecutive <p> without break) ({len(have_long_p_runs)} files) ===")
    for fname, count in have_long_p_runs:
        print(f"  {fname}: {count} runs")

    print(f"\n=== EM DASHES / DOUBLE DASHES ===")
    for fname, em, dd in have_em_dashes:
        print(f"  {fname}: {em} em dashes, {dd} double dashes")

if __name__ == "__main__":
    main()
