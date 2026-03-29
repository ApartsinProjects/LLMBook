"""
Book Restructuring Script
Performs all structural changes as specified in the restructuring plan.
"""

import os
import shutil
import re
import glob

BASE = r"E:\Projects\LLMCourse"
LOG = []

def log(msg):
    LOG.append(msg)
    print(msg)


def read_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def replace_in_file(path, old, new, count=0):
    """Replace text in a file. count=0 means replace all."""
    content = read_file(path)
    if old not in content:
        return False
    if count:
        updated = content.replace(old, new, count)
    else:
        updated = content.replace(old, new)
    if updated != content:
        write_file(path, updated)
        return True
    return False


def replace_in_all_html(old, new, description=""):
    """Replace a string in all HTML files under BASE."""
    changed = []
    for root, dirs, files in os.walk(BASE):
        # Skip .git and __pycache__
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules')]
        for fn in files:
            if fn.endswith('.html'):
                fpath = os.path.join(root, fn)
                if replace_in_file(fpath, old, new):
                    changed.append(fpath)
    if changed:
        log(f"  Replaced '{old}' with '{new}' in {len(changed)} files" + (f" ({description})" if description else ""))
    return changed


# ============================================================
# 1. Move Interpretability from Part IV to Part II
# ============================================================
def move_interpretability():
    log("\n=== TASK 1: Move Interpretability (Ch 18) from Part IV to Part II ===")

    src = os.path.join(BASE, "part-4-training-adapting", "module-18-interpretability")
    dst = os.path.join(BASE, "part-2-understanding-llms", "module-18-interpretability")

    if not os.path.isdir(src):
        log(f"  WARNING: Source dir does not exist: {src}")
        return
    if os.path.isdir(dst):
        log(f"  WARNING: Destination already exists: {dst}")
        return

    # Copy the directory (we will delete old orphans later)
    shutil.copytree(src, dst)
    log(f"  Copied {src} -> {dst}")

    # Update part-label in moved files to say Part II
    for fn in glob.glob(os.path.join(dst, "*.html")):
        content = read_file(fn)
        # Fix part-label references
        content = content.replace("Part IV: Training &amp; Adapting LLMs", "Part II: Understanding LLMs")
        content = content.replace("Part IV: Training &amp; Adapting", "Part II: Understanding LLMs")
        content = content.replace("Part IV: Training and Adapting", "Part II: Understanding LLMs")
        content = content.replace("Part 4: Training &amp; Adapting", "Part II: Understanding LLMs")
        # The parent index link: ../index.html still works (points to part-2 index now)
        write_file(fn, content)
    log("  Updated part-label in moved chapter files")

    # Now remove Ch 18 from Part IV index
    p4_index = os.path.join(BASE, "part-4-training-adapting", "index.html")
    content = read_file(p4_index)

    # Remove the chapter-card block for module-18-interpretability
    # Find and remove the entire chapter-card div
    pattern = r'\s*<div class="chapter-card">\s*<div class="chapter-card-header">\s*<a href="module-18-interpretability/index\.html">.*?</div>\s*</div>\s*'
    content = re.sub(pattern, '\n', content, flags=re.DOTALL)

    # Update chapter count: "Chapters: 6 (Chapters 13 through 18)" -> "Chapters: 5 (Chapters 13 through 17)"
    content = content.replace("Chapters: 6 (Chapters 13 through 18)", "Chapters: 5 (Chapters 13 through 17)")
    # Also update the subtitle to remove "interpreting what models learn"
    content = content.replace(
        "Generating data, fine-tuning models, distilling knowledge, aligning with human preferences, and interpreting what models learn.",
        "Generating data, fine-tuning models, distilling knowledge, and aligning with human preferences."
    )
    write_file(p4_index, content)
    log("  Removed Ch 18 from Part IV index.html")

    # Add Ch 18 to Part II index
    p2_index = os.path.join(BASE, "part-2-understanding-llms", "index.html")
    content = read_file(p2_index)

    # Insert before </div>\n\n<footer> (after the last chapter-card)
    ch18_card = """
    <div class="chapter-card">
        <div class="chapter-card-header">
            <a href="module-18-interpretability/index.html"><span class="mod-num">Chapter 18</span> Interpretability &amp; Mechanistic Understanding</a>
        </div>
        <div class="chapter-card-body">
            <p>Looking inside the black box: attention visualization, probing classifiers, mechanistic interpretability, circuit analysis, sparse autoencoders, and tools for understanding model behavior.</p>
            <ul class="section-list">
                <li><a href="module-18-interpretability/section-18.1.html"><span class="sec-num">18.1</span> Attention Analysis &amp; Probing</a></li>
                <li><a href="module-18-interpretability/section-18.2.html"><span class="sec-num">18.2</span> Mechanistic Interpretability</a></li>
                <li><a href="module-18-interpretability/section-18.3.html"><span class="sec-num">18.3</span> Practical Interpretability for Applications</a></li>
                <li><a href="module-18-interpretability/section-18.4.html"><span class="sec-num">18.4</span> Explaining Transformers</a></li>
            </ul>
        </div>
    </div>
"""
    # Insert before </div>\n\n<footer
    content = content.replace("\n</div>\n\n<footer>", ch18_card + "\n</div>\n\n<footer>")

    # Update chapter count
    content = content.replace("Chapters: 4 (Chapters 6 through 9)", "Chapters: 5 (Chapters 6 through 9, plus 18)")
    write_file(p2_index, content)
    log("  Added Ch 18 to Part II index.html")

    # Update all cross-references pointing to part-4 interpretability to point to part-2
    replace_in_all_html(
        "part-4-training-adapting/module-18-interpretability",
        "part-2-understanding-llms/module-18-interpretability",
        "interpretability cross-refs"
    )

    # Also fix any references via the old module-17-interpretability that pointed to part-4
    replace_in_all_html(
        "part-4-training-adapting/module-17-interpretability",
        "part-2-understanding-llms/module-18-interpretability",
        "old module-17 interpretability cross-refs"
    )

    # Now delete the source directory from part-4 (it was copied, not moved)
    shutil.rmtree(src)
    log(f"  Deleted original: {src}")


# ============================================================
# 2. Replace Section 7.3 with cross-reference to Chapter 8
# ============================================================
def fix_section_73():
    log("\n=== TASK 2: Replace Section 7.3 with cross-reference to Chapter 8 ===")

    sec73 = os.path.join(BASE, "part-2-understanding-llms", "module-07-modern-llm-landscape", "section-7.3.html")
    if not os.path.isfile(sec73):
        log(f"  WARNING: File not found: {sec73}")
        return

    content = read_file(sec73)

    # We keep the file but replace the main content with a brief summary and redirect
    # Keep the head, header, and nav structure
    new_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Section 7.3: Reasoning Models (see Chapter 8)</title>
    <link rel="stylesheet" href="../../styles/book.css">
</head>
<body>
<div class="book-title-bar">
    <a href="../../index.html">Building Conversational AI with LLMs and Agents</a>
</div>
<header class="chapter-header">
    <div class="part-label"><a href="../index.html" style="color: rgba(255,255,255,0.85); text-decoration: none;">Part II: Understanding LLMs</a></div>
    <div class="chapter-label"><a href="index.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Chapter 07: The Modern LLM Landscape</a></div>
    <h1>Reasoning Models &amp; Test-Time Compute</h1>
</header>

<main class="content">

    <div class="callout callout-info" style="margin: 2rem 0; padding: 1.5rem; background: linear-gradient(135deg, #e3f2fd, #f3e5f5); border-left: 4px solid var(--accent, #0f3460); border-radius: 8px;">
        <h3 style="margin-top: 0;">This Topic Has Its Own Chapter</h3>
        <p>
            Reasoning models and test-time compute scaling have become such an important paradigm that this topic
            now has a dedicated, expanded treatment in <a href="../module-08-reasoning-test-time-compute/index.html" style="color: var(--accent, #0f3460); font-weight: bold;">Chapter 8: Reasoning Models &amp; Test-Time Compute</a>.
        </p>
        <p>
            Chapter 8 covers the full landscape: the test-time compute paradigm shift, reasoning model architectures
            (o1, o3, DeepSeek R1, QwQ), training reasoning models with RLVR and GRPO, prompting strategies for
            reasoning models, and compute-optimal inference. Head there for the complete treatment.
        </p>
        <p style="margin-bottom: 0;">
            <a href="../module-08-reasoning-test-time-compute/index.html" style="color: var(--accent, #0f3460); font-weight: bold;">Go to Chapter 8: Reasoning Models &amp; Test-Time Compute &rarr;</a>
        </p>
    </div>

</main>

<nav class="chapter-nav">
    <a href="section-7.2.html" class="prev">&#8592; Previous: 7.2 Open-Source &amp; Open-Weight Models</a>
    <a href="section-7.4.html" class="next">Next: 7.4 Multilingual &amp; Cross-Cultural LLMs &#8594;</a>
</nav>

<footer>
    <p><a href="../../toc.html">Back to Table of Contents</a></p>
    <p>Building Conversational AI using LLM and Agents</p>
</footer>
</body>
</html>
"""
    write_file(sec73, new_content)
    log("  Replaced section-7.3.html with brief summary + cross-reference to Chapter 8")


# ============================================================
# 3. Rename Part VII directory and title
# ============================================================
def rename_part7():
    log("\n=== TASK 3: Rename Part VII directory and title ===")

    old_dir = os.path.join(BASE, "part-7-llm-applications")
    new_dir = os.path.join(BASE, "part-7-multimodal-applications")

    if not os.path.isdir(old_dir):
        log(f"  WARNING: Directory not found: {old_dir}")
        return
    if os.path.isdir(new_dir):
        log(f"  WARNING: New directory already exists: {new_dir}")
        return

    # First, update all references in all HTML files
    replace_in_all_html(
        "part-7-llm-applications",
        "part-7-multimodal-applications",
        "Part VII directory refs"
    )

    # Rename the directory
    os.rename(old_dir, new_dir)
    log(f"  Renamed directory: part-7-llm-applications -> part-7-multimodal-applications")

    # Update the Part VII index title
    p7_index = os.path.join(new_dir, "index.html")
    content = read_file(p7_index)
    content = content.replace(
        "<title>Part VII: LLM Applications</title>",
        "<title>Part VII: Multimodal AI &amp; Industry Applications</title>"
    )
    content = content.replace(
        "<h1>Part VII: LLM Applications</h1>",
        "<h1>Part VII: Multimodal AI &amp; Industry Applications</h1>"
    )
    content = content.replace(
        "Part VII: LLM Applications",
        "Part VII: Multimodal AI &amp; Industry Applications"
    )
    write_file(p7_index, content)
    log("  Updated Part VII index title to 'Multimodal AI & Industry Applications'")

    # Update part-label in chapter files inside Part VII
    for fn in glob.glob(os.path.join(new_dir, "**", "*.html"), recursive=True):
        content = read_file(fn)
        updated = content.replace("Part VII: LLM Applications", "Part VII: Multimodal AI &amp; Industry Applications")
        if updated != content:
            write_file(fn, updated)


# ============================================================
# 4. Rename Chapter 25
# ============================================================
def rename_ch25():
    log("\n=== TASK 4: Rename Chapter 25 to 'LLM Applications Across Industries' ===")

    # After Part VII rename, the path is under the new directory
    ch25_dir = os.path.join(BASE, "part-7-multimodal-applications", "module-25-llm-applications")
    if not os.path.isdir(ch25_dir):
        log(f"  WARNING: Directory not found: {ch25_dir}")
        return

    ch25_index = os.path.join(ch25_dir, "index.html")
    content = read_file(ch25_index)

    # Update title tag
    content = content.replace(
        "<title>Chapter 25: LLM Applications</title>",
        "<title>Chapter 25: LLM Applications Across Industries</title>"
    )
    # Update h1
    content = content.replace(
        "<h1>LLM Applications</h1>",
        "<h1>LLM Applications Across Industries</h1>"
    )
    write_file(ch25_index, content)
    log("  Updated Chapter 25 index title")


# ============================================================
# 5. Rename Chapter 7
# ============================================================
def rename_ch7():
    log("\n=== TASK 5: Rename Chapter 7 to 'The Modern LLM Landscape' ===")

    ch7_dir = os.path.join(BASE, "part-2-understanding-llms", "module-07-modern-llm-landscape")
    ch7_index = os.path.join(ch7_dir, "index.html")

    content = read_file(ch7_index)
    content = content.replace(
        "<title>Chapter 07: Modern LLM Landscape &amp; Model Internals</title>",
        "<title>Chapter 07: The Modern LLM Landscape</title>"
    )
    content = content.replace(
        "<h1>Modern LLM Landscape &amp; Model Internals</h1>",
        "<h1>The Modern LLM Landscape</h1>"
    )
    write_file(ch7_index, content)
    log("  Updated Chapter 7 index title")

    # Update in Part II index
    p2_index = os.path.join(BASE, "part-2-understanding-llms", "index.html")
    replace_in_file(p2_index, "Modern LLM Landscape and Model Internals", "The Modern LLM Landscape")
    replace_in_file(p2_index, "Modern LLM Landscape &amp; Model Internals", "The Modern LLM Landscape")
    log("  Updated Part II index reference")


# ============================================================
# 6. Delete orphaned old-numbered module directories
# ============================================================
def delete_orphans():
    log("\n=== TASK 6: Delete orphaned old-numbered module directories ===")

    # Define orphan pairs: (part_dir, old_module, new_module)
    orphans = [
        # Part 2: old module-08-inference-optimization -> current module-09-inference-optimization
        ("part-2-understanding-llms", "module-08-inference-optimization", "module-09-inference-optimization"),

        # Part 3
        ("part-3-working-with-llms", "module-09-llm-apis", "module-10-llm-apis"),
        ("part-3-working-with-llms", "module-10-prompt-engineering", "module-11-prompt-engineering"),
        ("part-3-working-with-llms", "module-11-hybrid-ml-llm", "module-12-hybrid-ml-llm"),

        # Part 4
        ("part-4-training-adapting", "module-12-synthetic-data", "module-13-synthetic-data"),
        ("part-4-training-adapting", "module-13-fine-tuning-fundamentals", "module-14-fine-tuning-fundamentals"),
        ("part-4-training-adapting", "module-14-peft", "module-15-peft"),
        ("part-4-training-adapting", "module-15-distillation-merging", "module-16-distillation-merging"),
        ("part-4-training-adapting", "module-16-alignment-rlhf-dpo", "module-17-alignment-rlhf-dpo"),
        ("part-4-training-adapting", "module-17-interpretability", None),  # moved to part-2/module-18

        # Part 5
        ("part-5-retrieval-conversation", "module-18-embeddings-vector-db", "module-19-embeddings-vector-db"),
        ("part-5-retrieval-conversation", "module-19-rag", "module-20-rag"),
        ("part-5-retrieval-conversation", "module-20-conversational-ai", "module-21-conversational-ai"),
    ]

    for part_dir, old_mod, new_mod in orphans:
        old_path = os.path.join(BASE, part_dir, old_mod)

        if not os.path.isdir(old_path):
            log(f"  SKIP (not found): {part_dir}/{old_mod}")
            continue

        if new_mod:
            new_path = os.path.join(BASE, part_dir, new_mod)
            if not os.path.isdir(new_path):
                # Special case: module-17-interpretability was moved to part-2
                log(f"  SKIP (no matching new dir): {part_dir}/{old_mod} (expected {new_mod})")
                continue

            # Compare: check that new dir has at least as many HTML files
            old_htmls = set(f for f in os.listdir(old_path) if f.endswith('.html'))
            new_htmls = set(f for f in os.listdir(new_path) if f.endswith('.html'))

            # The new dir should have similar section files (with renumbered names)
            old_count = len(old_htmls)
            new_count = len(new_htmls)

            if new_count < old_count:
                log(f"  WARNING: New dir has fewer HTML files ({new_count}) than old ({old_count}): {part_dir}/{old_mod}")
                log(f"    Old: {sorted(old_htmls)}")
                log(f"    New: {sorted(new_htmls)}")
                log(f"    Deleting anyway since old numbering is superseded.")

        shutil.rmtree(old_path)
        log(f"  DELETED: {part_dir}/{old_mod}")


# ============================================================
# 8. Update toc.html with all changes
# ============================================================
def update_toc():
    log("\n=== TASK 8: Update toc.html ===")

    toc_path = os.path.join(BASE, "toc.html")
    content = read_file(toc_path)

    # 3. Part VII name in toc banner and links (directory refs already updated by replace_in_all_html)
    content = content.replace(
        "Part VII: LLM Applications",
        "Part VII: Multimodal AI &amp; Industry Applications"
    )

    # 4. Chapter 25 title
    content = content.replace(
        '>LLM Applications</a>',
        '>LLM Applications Across Industries</a>'
    )
    # Also the toc-item version at the top
    content = content.replace(
        '<span class="toc-num">25</span> LLM Applications</a>',
        '<span class="toc-num">25</span> LLM Applications Across Industries</a>'
    )

    # 5. Chapter 7 title: drop "& Model Internals"
    content = content.replace(
        "Modern LLM Landscape &amp; Model Internals",
        "The Modern LLM Landscape"
    )
    content = content.replace(
        "Modern LLM Landscape and Model Internals",
        "The Modern LLM Landscape"
    )

    # 1. Move Ch 18 from Part IV section to Part II section in toc
    # In the toc grid at top: Ch 18 line needs to move from after Part IV chapters to after Part II chapters
    # The toc-item for ch18 in the grid
    ch18_toc_line = '            <a class="toc-item" href="#ch18"><span class="toc-num">18</span> Interpretability &amp; Mechanistic Understanding</a>\n'

    # Remove ch18 from wherever it is (Part IV area)
    content = content.replace(ch18_toc_line, "")

    # Insert after ch9 line (last Part II chapter in the grid)
    ch9_toc_line = '<a class="toc-item" href="#ch9"><span class="toc-num">09</span> Inference Optimization &amp; Efficient Serving</a>'
    content = content.replace(
        ch9_toc_line,
        ch9_toc_line + '\n' + '            <a class="toc-item" href="#ch18"><span class="toc-num">18</span> Interpretability &amp; Mechanistic Understanding</a>'
    )

    # Now move the full chapter block (the big #ch18 div) from Part IV section to Part II section
    # Find the ch18 block
    ch18_block_match = re.search(
        r'(\s*<!-- =+\s*\n\s*<!-- CHAPTER 18:.*?<!-- =+\s*-->\s*\n\s*<div class="book-chapter" id="ch18">.*?</div>\s*</div>\s*</div>)',
        content,
        re.DOTALL
    )

    if ch18_block_match:
        ch18_block = ch18_block_match.group(1)
        # Remove it from its current location
        content = content.replace(ch18_block, "")

        # Update the block: change part-4-training-adapting to part-2-understanding-llms in the block
        ch18_block = ch18_block.replace("part-4-training-adapting", "part-2-understanding-llms")

        # Find the end of Part II / start of Part III banner
        part3_banner = '    <div style="margin: 2rem 0 1rem 0; padding: 0.8rem 1.5rem; background: linear-gradient(135deg, var(--primary), var(--accent)); color: white; border-radius: 10px; font-size: 1rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;">Part III: Working with LLMs</div>'

        if part3_banner in content:
            content = content.replace(part3_banner, ch18_block + "\n\n" + "    " + part3_banner.strip())
            log("  Moved Ch 18 block from Part IV to Part II in toc.html")
        else:
            log("  WARNING: Could not find Part III banner in toc.html to insert Ch 18 before")
    else:
        log("  WARNING: Could not find Ch 18 block in toc.html")

    write_file(toc_path, content)
    log("  Updated toc.html with all title and structural changes")


# ============================================================
# Also update introduction.html references
# ============================================================
def update_introduction():
    log("\n=== Updating introduction.html references ===")
    intro = os.path.join(BASE, "introduction.html")
    if os.path.isfile(intro):
        content = read_file(intro)
        changed = False

        if "Modern LLM Landscape &amp; Model Internals" in content:
            content = content.replace("Modern LLM Landscape &amp; Model Internals", "The Modern LLM Landscape")
            changed = True
        if "Modern LLM Landscape and Model Internals" in content:
            content = content.replace("Modern LLM Landscape and Model Internals", "The Modern LLM Landscape")
            changed = True

        if changed:
            write_file(intro, content)
            log("  Updated chapter titles in introduction.html")


# ============================================================
# Update the root index.html TOC references
# ============================================================
def update_root_index():
    log("\n=== Updating root index.html ===")
    idx = os.path.join(BASE, "index.html")
    content = read_file(idx)
    changed = False

    if "Modern LLM Landscape &amp; Model Internals" in content:
        content = content.replace("Modern LLM Landscape &amp; Model Internals", "The Modern LLM Landscape")
        changed = True
    if "Modern LLM Landscape and Model Internals" in content:
        content = content.replace("Modern LLM Landscape and Model Internals", "The Modern LLM Landscape")
        changed = True

    if changed:
        write_file(idx, content)
        log("  Updated root index.html")


# ============================================================
# Run all tasks
# ============================================================
def main():
    log("Book Restructuring Script")
    log("=" * 60)

    move_interpretability()    # Task 1
    fix_section_73()           # Task 2
    rename_part7()             # Task 3
    rename_ch25()              # Task 4
    rename_ch7()               # Task 5
    delete_orphans()           # Task 6
    # Task 7: Do NOT merge Parts 9 and 10 (keep separate)
    update_toc()               # Task 8
    update_introduction()
    update_root_index()

    log("\n" + "=" * 60)
    log("DONE. All restructuring tasks completed.")
    log(f"Total operations logged: {len(LOG)}")


if __name__ == "__main__":
    main()
