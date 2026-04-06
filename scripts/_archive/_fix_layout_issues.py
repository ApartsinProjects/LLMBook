"""
Fix layout issues across the LLM textbook.
Issue 1: Missing/non-standard chapter-nav footers
Issue 2: Element ordering (prerequisites after big-picture) in Part 2
Issue 3: Missing epigraphs in Module 30
Issue 4: Missing big-picture callouts in specific files
"""

import re
import os
import glob
from html import unescape

BASE = r"E:\Projects\LLMCourse"

counters = {
    "issue1_nav_converted": 0,
    "issue1_nav_added": 0,
    "issue2_reordered": 0,
    "issue3_epigraphs": 0,
    "issue4_big_picture": 0,
}


def read_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def get_section_title(filepath):
    """Extract the short title from the <title> tag, stripping the 'Section X.Y: ' prefix."""
    content = read_file(filepath)
    m = re.search(r"<title>(?:Section\s+[\d.]+:\s*)?(.*?)</title>", content)
    if m:
        return unescape(m.group(1).strip())
    return None


def get_section_number(filepath):
    """Extract section number like '6.1' from filename."""
    basename = os.path.basename(filepath)
    m = re.match(r"section-(\d+\.\d+)\.html", basename)
    return m.group(1) if m else None


def get_module_sections(module_dir):
    """Get sorted list of section files in a module directory."""
    pattern = os.path.join(module_dir, "section-*.html")
    files = sorted(glob.glob(pattern))
    return files


# ============================================================
# ISSUE 1: Fix chapter-nav footers
# ============================================================

def fix_chapter_nav(filepath, sections_in_module):
    """Convert existing nav or add chapter-nav footer."""
    content = read_file(filepath)

    # Already has chapter-nav? Skip.
    if 'class="chapter-nav"' in content:
        return False

    section_num = get_section_number(filepath)
    if not section_num:
        return False

    # Find position in module
    idx = None
    for i, s in enumerate(sections_in_module):
        if os.path.basename(s) == os.path.basename(filepath):
            idx = i
            break
    if idx is None:
        return False

    # Build prev/next links
    prev_link = ""
    next_link = ""

    if idx > 0:
        prev_file = os.path.basename(sections_in_module[idx - 1])
        prev_num = get_section_number(sections_in_module[idx - 1])
        prev_title = get_section_title(sections_in_module[idx - 1])
        if prev_title and prev_num:
            prev_link = f'    <a href="{prev_file}" class="prev">&#8592; Previous: {prev_num} {prev_title}</a>'
        elif prev_num:
            prev_link = f'    <a href="{prev_file}" class="prev">&#8592; Previous: Section {prev_num}</a>'

    if idx < len(sections_in_module) - 1:
        next_file = os.path.basename(sections_in_module[idx + 1])
        next_num = get_section_number(sections_in_module[idx + 1])
        next_title = get_section_title(sections_in_module[idx + 1])
        if next_title and next_num:
            next_link = f'    <a href="{next_file}" class="next">Next: {next_num} {next_title} &#8594;</a>'
        elif next_num:
            next_link = f'    <a href="{next_file}" class="next">Next: Section {next_num} &#8594;</a>'

    # Build the new nav block
    nav_lines = ['<nav class="chapter-nav">']
    if prev_link:
        nav_lines.append(prev_link)
    if next_link:
        nav_lines.append(next_link)
    nav_lines.append('</nav>')
    new_nav = "\n".join(nav_lines)

    original = content

    # Pattern 1: <nav style="..."> ... </nav>
    inline_nav_pattern = r'<nav\s+style="[^"]*"[^>]*>.*?</nav>'
    m = re.search(inline_nav_pattern, content, re.DOTALL)
    if m:
        content = content[:m.start()] + new_nav + content[m.end():]
        write_file(filepath, content)
        counters["issue1_nav_converted"] += 1
        return True

    # Pattern 2: <nav class="nav-footer"> ... </nav>
    nav_footer_pattern = r'<nav\s+class="nav-footer"[^>]*>.*?</nav>'
    m = re.search(nav_footer_pattern, content, re.DOTALL)
    if m:
        content = content[:m.start()] + new_nav + content[m.end():]
        write_file(filepath, content)
        counters["issue1_nav_converted"] += 1
        return True

    # Pattern 3: any other <nav> ... </nav>
    generic_nav_pattern = r'<nav[^>]*>.*?</nav>'
    m = re.search(generic_nav_pattern, content, re.DOTALL)
    if m:
        content = content[:m.start()] + new_nav + content[m.end():]
        write_file(filepath, content)
        counters["issue1_nav_converted"] += 1
        return True

    # No nav at all: insert before </body>
    body_close = content.rfind("</body>")
    if body_close >= 0:
        content = content[:body_close] + "\n" + new_nav + "\n\n" + content[body_close:]
        write_file(filepath, content)
        counters["issue1_nav_added"] += 1
        return True

    return False


# ============================================================
# ISSUE 2: Fix element ordering in Part 2 (modules 06, 07, 08)
# ============================================================

def fix_element_ordering(filepath):
    """Move prerequisites block before big-picture callout if it appears after."""
    content = read_file(filepath)

    # Find big-picture and prerequisites positions
    bp_match = re.search(r'<div class="callout big-picture">.*?</div>\s*</div>', content, re.DOTALL)
    # Alternative: big-picture may end with just </div>
    if not bp_match:
        bp_match = re.search(r'<div class="callout big-picture">.*?</div>', content, re.DOTALL)

    prereq_match = re.search(r'<div class="prerequisites">.*?</div>', content, re.DOTALL)

    if not bp_match or not prereq_match:
        return False

    bp_start = bp_match.start()
    prereq_start = prereq_match.start()

    # Only fix if prerequisites appears AFTER big-picture
    if prereq_start <= bp_start:
        return False

    # Extract both blocks
    prereq_block = prereq_match.group(0)

    # Remove the prerequisites block from its current position
    content_without_prereq = content[:prereq_match.start()] + content[prereq_match.end():]

    # Clean up whitespace where prereq was removed
    content_without_prereq = re.sub(r'\n\s*\n\s*\n', '\n\n', content_without_prereq)

    # Re-find big-picture position in modified content
    bp_match2 = re.search(r'<div class="callout big-picture">', content_without_prereq)
    if not bp_match2:
        return False

    # Insert prerequisites before big-picture
    insert_pos = bp_match2.start()
    content_fixed = (
        content_without_prereq[:insert_pos]
        + prereq_block + "\n\n    "
        + content_without_prereq[insert_pos:]
    )

    write_file(filepath, content_fixed)
    counters["issue2_reordered"] += 1
    return True


# ============================================================
# ISSUE 3: Add epigraphs to Module 30
# ============================================================

MODULE_30_EPIGRAPHS = {
    "section-30.1.html": (
        "They said emergent abilities were like magic. Turns out, most magic is just a measurement trick with better lighting.",
        "A Skeptical AI Researcher"
    ),
    "section-30.2.html": (
        "We keep scaling until the electricity bill becomes the research contribution.",
        "A Budget-Conscious AI Lab Director"
    ),
    "section-30.3.html": (
        "The future of AI safety is a lot like the future of weather forecasting: everyone agrees it matters, nobody agrees on the model.",
        "A Cautiously Optimistic AI Agent"
    ),
    "section-30.4.html": (
        "Multimodal models see, hear, and read. They still cannot fold laundry, but give them time.",
        "A Pragmatic Vision-Language Model"
    ),
    "section-30.5.html": (
        "The hardest part of predicting the future of AI is that the future keeps arriving ahead of schedule.",
        "A Perpetually Surprised Forecaster"
    ),
}


def add_epigraph_module30(filepath):
    """Add epigraph to Module 30 section files if missing."""
    content = read_file(filepath)
    basename = os.path.basename(filepath)

    if basename not in MODULE_30_EPIGRAPHS:
        return False

    # Already has epigraph?
    if 'class="epigraph"' in content:
        return False

    quote, cite = MODULE_30_EPIGRAPHS[basename]

    epigraph_block = f'''<blockquote class="epigraph">
    <p>"{quote}"</p>
    <cite>{cite}</cite>
</blockquote>'''

    # Insert after <main class="content"> or after </header>
    # Try <main class="content"> first
    m = re.search(r'(<main\s+class="content">\s*\n)', content)
    if m:
        insert_pos = m.end()
        content = content[:insert_pos] + "\n    " + epigraph_block + "\n\n" + content[insert_pos:]
        write_file(filepath, content)
        counters["issue3_epigraphs"] += 1
        return True

    # Try </header>
    m = re.search(r'(</header>\s*\n)', content)
    if m:
        insert_pos = m.end()
        content = content[:insert_pos] + "\n" + epigraph_block + "\n\n" + content[insert_pos:]
        write_file(filepath, content)
        counters["issue3_epigraphs"] += 1
        return True

    return False


# ============================================================
# ISSUE 4: Add big-picture callouts to specific files
# ============================================================

BIG_PICTURE_CALLOUTS = {
    # Module 01 sections
    os.path.join("part-1-foundations", "module-01-foundations-nlp-text-representation", "section-1.1.html"):
        "This entire book is a journey through one central question: <strong>How do we represent language in a form that machines can work with?</strong> Every breakthrough in NLP, from bag-of-words to transformers to ChatGPT, is fundamentally an answer to this question. The better our representation, the more capable our systems become.",

    os.path.join("part-1-foundations", "module-01-foundations-nlp-text-representation", "section-1.2.html"):
        "Text preprocessing is where raw human language meets machine computation. The choices you make here (lowercasing, stemming, stopword removal) propagate through every downstream model. Understanding these classical techniques is essential because modern tokenizers (covered in <a href=\"../module-02-tokenization-subword-models/section-2.1.html\">Chapter 2</a>) evolved to solve the limitations you will discover in this section.",

    os.path.join("part-1-foundations", "module-01-foundations-nlp-text-representation", "section-1.3.html"):
        "Word embeddings were the first technique to capture <em>meaning</em> in numbers. They showed that mathematical operations on vectors could mirror semantic relationships: king minus man plus woman equals queen. This idea, that geometry can encode semantics, is the conceptual foundation for every embedding model in this book, from sentence embeddings (<a href=\"../../part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.1.html\">Chapter 18</a>) to the hidden states inside transformers (<a href=\"../module-04-transformer-architecture/section-4.1.html\">Chapter 4</a>).",

    os.path.join("part-1-foundations", "module-01-foundations-nlp-text-representation", "section-1.4.html"):
        "Contextual embeddings represent the critical bridge between static word vectors and modern transformers. ELMo demonstrated that the same word should have <em>different</em> representations depending on its context, an insight that directly inspired BERT and GPT. Understanding this transition prepares you for the full Transformer architecture in <a href=\"../module-04-transformer-architecture/section-4.1.html\">Chapter 4</a>.",

    # Module 04 sections
    os.path.join("part-1-foundations", "module-04-transformer-architecture", "section-4.2.html"):
        "Building a Transformer from scratch is the single most effective way to internalize the architecture. By writing each component yourself (embeddings, multi-head attention, feed-forward layers, residual connections), you develop the intuition needed to debug, modify, and optimize Transformer-based models throughout the rest of this book.",

    os.path.join("part-1-foundations", "module-04-transformer-architecture", "section-4.5.html"):
        "Understanding what Transformers <em>can</em> and <em>cannot</em> compute in theory helps explain their practical strengths and weaknesses. This section connects the architectural choices from <a href=\"section-4.1.html\">Section 4.1</a> to formal results about expressiveness, giving you a principled framework for understanding why certain tasks remain challenging even for very large models.",
}

# Check for the Issue 4 files mentioned in the task that may have different paths
# "part-3-working-with-llms/module-10-llm-apis/section-10.4.html" (listed as 9.4)
# "part-3-working-with-llms/module-11-prompt-engineering/section-11.5.html" (listed as 10.5)
BIG_PICTURE_CALLOUTS[os.path.join("part-3-working-with-llms", "module-10-llm-apis", "section-10.4.html")] = \
    "Reasoning models and multimodal APIs represent the cutting edge of the LLM API landscape. Understanding how to work with these specialized endpoints prepares you for the advanced prompting techniques in <a href=\"../module-11-prompt-engineering/section-11.1.html\">Chapter 11</a> and the multimodal applications in <a href=\"../../part-6-agents-applications/module-23-multimodal/section-23.1.html\">Chapter 23</a>."

BIG_PICTURE_CALLOUTS[os.path.join("part-3-working-with-llms", "module-11-prompt-engineering", "section-11.5.html")] = \
    "Prompting reasoning and multimodal models requires fundamentally different strategies than prompting standard chat models. This section bridges the prompting foundations from earlier sections with the specialized capabilities of reasoning models (<a href=\"../../part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html\">Section 7.3</a>) and multimodal systems (<a href=\"../../part-6-agents-applications/module-23-multimodal/section-23.1.html\">Chapter 23</a>)."


def add_big_picture(filepath, text):
    """Add big-picture callout to a file if missing."""
    full_path = os.path.join(BASE, filepath)
    if not os.path.exists(full_path):
        print(f"  WARNING: File not found: {full_path}")
        return False

    content = read_file(full_path)

    # Check if it already has a big-picture callout
    if 'class="callout big-picture"' in content:
        # Check if it's a key-insight with Big Picture title instead
        pass
    if 'class="callout big-picture"' in content:
        print(f"  SKIP (already has big-picture): {filepath}")
        return False

    # Also check for the key-insight variant that serves as big-picture
    if 'class="callout key-insight"' in content and "Big Picture" in content:
        # Convert key-insight to big-picture
        content = content.replace('class="callout key-insight"', 'class="callout big-picture"', 1)
        write_file(full_path, content)
        counters["issue4_big_picture"] += 1
        print(f"  CONVERTED key-insight to big-picture: {filepath}")
        return True

    big_picture_block = f'''<div class="callout big-picture">
        <div class="callout-title">&#9733; Big Picture</div>
        <p>{text}</p>
    </div>'''

    # Insert after prerequisites if present
    prereq_match = re.search(r'(</div>\s*\n)', content)
    # More specifically, after the prerequisites div
    prereq_match = re.search(r'(<div class="prerequisites">.*?</div>)\s*\n', content, re.DOTALL)
    if prereq_match:
        insert_pos = prereq_match.end()
        content = content[:insert_pos] + "\n    " + big_picture_block + "\n\n" + content[insert_pos:]
        write_file(full_path, content)
        counters["issue4_big_picture"] += 1
        print(f"  ADDED big-picture after prerequisites: {filepath}")
        return True

    # Insert after epigraph if present
    epigraph_match = re.search(r'(</blockquote>)\s*\n', content)
    if epigraph_match:
        insert_pos = epigraph_match.end()
        content = content[:insert_pos] + "\n    " + big_picture_block + "\n\n" + content[insert_pos:]
        write_file(full_path, content)
        counters["issue4_big_picture"] += 1
        print(f"  ADDED big-picture after epigraph: {filepath}")
        return True

    # Insert after <div class="content"> or <main class="content">
    content_div_match = re.search(r'(<(?:div|main)\s+class="content">\s*\n)', content)
    if content_div_match:
        insert_pos = content_div_match.end()
        content = content[:insert_pos] + "\n    " + big_picture_block + "\n\n" + content[insert_pos:]
        write_file(full_path, content)
        counters["issue4_big_picture"] += 1
        print(f"  ADDED big-picture after content div: {filepath}")
        return True

    print(f"  WARNING: Could not find insertion point: {filepath}")
    return False


# ============================================================
# MAIN
# ============================================================

def main():
    os.chdir(BASE)

    # --- ISSUE 1: Fix nav footers ---
    print("=" * 60)
    print("ISSUE 1: Fixing chapter-nav footers")
    print("=" * 60)

    # Process all section files in all modules
    module_dirs = sorted(glob.glob("part-*/module-*/"))
    for mod_dir in module_dirs:
        sections = get_module_sections(mod_dir)
        if not sections:
            continue
        for section_file in sections:
            if 'class="chapter-nav"' not in read_file(section_file):
                result = fix_chapter_nav(section_file, sections)
                if result:
                    print(f"  Fixed: {section_file}")

    # --- ISSUE 2: Fix element ordering ---
    print("\n" + "=" * 60)
    print("ISSUE 2: Fixing element ordering in Part 2")
    print("=" * 60)

    part2_modules = [
        "part-2-understanding-llms/module-06-pretraining-scaling-laws",
        "part-2-understanding-llms/module-07-modern-llm-landscape",
        "part-2-understanding-llms/module-08-inference-optimization",
    ]
    for mod in part2_modules:
        sections = get_module_sections(mod)
        for section_file in sections:
            result = fix_element_ordering(section_file)
            if result:
                print(f"  Reordered: {section_file}")

    # --- ISSUE 3: Add epigraphs to Module 30 ---
    print("\n" + "=" * 60)
    print("ISSUE 3: Adding epigraphs to Module 30")
    print("=" * 60)

    mod30_dir = "part-7-production-strategy/module-30-frontiers"
    for basename in MODULE_30_EPIGRAPHS:
        filepath = os.path.join(mod30_dir, basename)
        result = add_epigraph_module30(filepath)
        if result:
            print(f"  Added epigraph: {filepath}")
        else:
            print(f"  Skipped (already has epigraph or not found): {filepath}")

    # --- ISSUE 4: Add big-picture callouts ---
    print("\n" + "=" * 60)
    print("ISSUE 4: Adding big-picture callouts")
    print("=" * 60)

    for filepath, text in BIG_PICTURE_CALLOUTS.items():
        add_big_picture(filepath, text)

    # --- Summary ---
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Issue 1: Nav converted from other format: {counters['issue1_nav_converted']}")
    print(f"Issue 1: Nav added (no previous nav):     {counters['issue1_nav_added']}")
    print(f"Issue 1: Total nav fixes:                 {counters['issue1_nav_converted'] + counters['issue1_nav_added']}")
    print(f"Issue 2: Element ordering fixed:           {counters['issue2_reordered']}")
    print(f"Issue 3: Epigraphs added:                  {counters['issue3_epigraphs']}")
    print(f"Issue 4: Big-picture callouts added:       {counters['issue4_big_picture']}")
    total = sum(counters.values())
    print(f"TOTAL FIXES:                               {total}")


if __name__ == "__main__":
    main()
