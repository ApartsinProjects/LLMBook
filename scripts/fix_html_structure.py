#!/usr/bin/env python3
"""
Fix HTML structural issues found by audit_html_wellformed.py.

Patterns fixed:
1. Missing </main> before </body> (insert before footer nav or </body>)
2. Extra </div> in chapters 32/33 (stray </div> after epigraph, extra near end)
3. Unclosed <div class="lab"> in sections 32.1 and 33.3
4. Unclosed <ul>/<li> in section 30.1
5. Mismatched </strong> closing <em> in section 10.4
6. <div class="answer"> with bare text ending in </p> (missing opening <p>)
7. <div class="diagram-caption"> ending with </p> instead of nothing
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXES_APPLIED = []


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def count_div_balance(content):
    opens = len(re.findall(r"<div[\s>]", content))
    closes = len(re.findall(r"</div>", content))
    return opens, closes


def log_fix(filepath, description):
    rel = os.path.relpath(filepath, ROOT)
    FIXES_APPLIED.append((rel, description))
    print(f"  FIXED: {rel}: {description}")


# ---------------------------------------------------------------------------
# Pattern 1: Missing </main> before </body>
# Files that have <main class="content"> but no </main>.
# Insert </main> before <nav class="chapter-nav"> or before </body>.
# ---------------------------------------------------------------------------
def fix_missing_main_close(filepath):
    content = read_file(filepath)

    # Check if file has <main> open but no </main>
    has_main_open = bool(re.search(r"<main\s+class=\"content\">", content))
    has_main_close = "</main>" in content

    if not has_main_open:
        return False
    if has_main_close:
        return False

    # Strategy: insert </main> before <nav class="chapter-nav">
    nav_match = re.search(r"^(<nav\s+class=\"chapter-nav\">)", content, re.MULTILINE)
    if nav_match:
        pos = nav_match.start()
        content = content[:pos] + "</main>\n" + content[pos:]
        write_file(filepath, content)
        log_fix(filepath, "Inserted </main> before <nav class='chapter-nav'>")
        return True

    # Fallback: insert before </body>
    body_match = re.search(r"</body>", content)
    if body_match:
        pos = body_match.start()
        content = content[:pos] + "</main>\n" + content[pos:]
        write_file(filepath, content)
        log_fix(filepath, "Inserted </main> before </body>")
        return True

    return False


# ---------------------------------------------------------------------------
# Pattern 2: Extra </div> in chapters 32 and 33 after epigraph
# The pattern is: </blockquote> ... </div> ... </div> (stray) before content
# Also extra </div> near the end before <nav class="chapter-nav">
# ---------------------------------------------------------------------------
def fix_stray_div_after_epigraph(filepath):
    """Remove the stray </div> that appears after prerequisites div closes."""
    content = read_file(filepath)
    lines = content.split("\n")
    changed = False

    # The pattern: the prerequisites div ends with </div> on one line,
    # then there's a blank </div> on the next line (the stray one),
    # then a <figure> or <h2> or content follows.
    # From examining the files, the stray </div> appears right after
    # the prerequisites closing </div>, separated by a blank line.
    # Specifically: line N = "</div>", line N+1 = "", line N+2 = "</div>"
    # where the </div> on N+2 is stray.

    # Actually from the files: the prerequisites block ends with:
    #   <p>...</p></div>
    #
    #   </div>      <-- this is the stray one
    #
    #   <figure ...

    # Look for the pattern: </div>\n\n</div>\n\n<figure
    # or </div>\n\n</div>\n\n<h2
    # right after the prerequisites section

    new_content = re.sub(
        r"(</p></div>\s*\n)\s*\n</div>(\s*\n\s*\n?\s*<(?:figure|h2))",
        r"\1\2",
        content,
    )

    if new_content != content:
        changed = True
        content = new_content
        log_fix(filepath, "Removed stray </div> after prerequisites/epigraph block")

    # Also fix extra </div> near end: pattern is </div>\n</div>\n\n before content
    # These files also have an extra </div> near the end, before exercises or
    # before <nav class="chapter-nav">
    # Pattern: </div>\n</div>\n\n<section class="bibliography"> or similar

    # Count div balance to see if still imbalanced
    opens, closes = count_div_balance(content)
    if closes > opens:
        # Try to find and remove extra </div> near the end
        # Pattern: </div>\n</div>\n\n<section or </div>\n</div>\n\n\n\n<h2
        # The extra </div> is typically the one right before bibliography or exercises

        # Look for </div>\n</div>\n\n (two consecutive close divs before a gap)
        # near the end of the file (last 30% of content)
        cutoff = int(len(content) * 0.6)
        tail = content[cutoff:]

        # Pattern: whats-next div closes, then extra </div> follows
        fixed_tail = re.sub(
            r"(</div>\n)</div>\n(\n+<(?:section class=\"bibliography\"|h2>Exercises))",
            r"\1\2",
            tail,
            count=1,
        )

        if fixed_tail != tail:
            content = content[:cutoff] + fixed_tail
            changed = True
            log_fix(filepath, "Removed extra </div> near end of file")

    if changed:
        write_file(filepath, content)
    return changed


# ---------------------------------------------------------------------------
# Pattern 3: Unclosed <div class="lab"> before </section>
# In sections 32.1 and 33.3, the <div class="lab"> is never closed.
# Insert </div> before the </section> that force-closes it.
# ---------------------------------------------------------------------------
def fix_unclosed_lab_div(filepath):
    content = read_file(filepath)

    # Find <section class="lab" ...> followed by <div class="lab">
    # The </section> closes the section but not the div.
    # Insert </div> before </section> inside lab sections.

    # Pattern: we need to add </div> just before the </details>\n </section>
    # that closes the lab section.
    # From the files: the lab content has a <details> with solution code,
    # then </details>\n </section>

    # More specifically: find </section> that comes after a lab div
    # and add </div> before it if needed.

    # Strategy: find each <div class="lab"> and check if it's closed
    # before the next </section>

    pattern = r'(<div class="lab">)(.*?)(</section>)'
    matches = list(re.finditer(pattern, content, re.DOTALL))

    if not matches:
        return False

    changed = False
    for m in reversed(matches):
        inner = m.group(2)
        # Count div opens and closes within this span
        inner_opens = len(re.findall(r"<div[\s>]", inner))
        inner_closes = len(re.findall(r"</div>", inner))

        if inner_opens >= inner_closes:
            # Need to add (inner_opens - inner_closes) </div> before </section>
            deficit = inner_opens - inner_closes
            # But we also need +1 for the <div class="lab"> itself
            # Actually the lab div open is in group(1), so we need deficit+1
            # Wait: the regex captures <div class="lab"> in group(1),
            # inner content in group(2). inner_opens counts divs INSIDE the lab div.
            # The lab div itself needs one </div>.
            # So total needed = inner_opens - inner_closes + 1

            # Hmm, let's be more precise. The <div class="lab"> is the outer div.
            # inner contains nested <div> ... </div> pairs.
            # If inner has N opens and M closes, and N == M, then we just need
            # one </div> for the lab div itself.
            # If inner has N opens and M closes where N > M, we need (N-M+1) closes.

            needed = inner_opens - inner_closes + 1
            insert = "</div>\n" * needed
            end_pos = m.start(3)
            content = content[:end_pos] + insert + content[end_pos:]
            changed = True
            log_fix(filepath, f"Closed unclosed <div class='lab'> (added {needed} </div>)")

    if changed:
        write_file(filepath, content)
    return changed


# ---------------------------------------------------------------------------
# Pattern 4: Unclosed <ul>/<li> in section 30.1 (lines 582-588)
# The </div> appears inside a <li> prematurely.
# ---------------------------------------------------------------------------
def fix_section_30_1(filepath):
    content = read_file(filepath)

    # The problem: around line 582-585:
    #  <ul>
    #  <li><strong>OpenTelemetry for LLMs:</strong> ...text...
    #
    # </div> </li>
    # The </div> is stray, closing the parent callout div prematurely.
    # Fix: remove the stray </div> from inside the <li>.

    old = "\n</div> </li>"
    new = "\n </li>"

    if old in content:
        content = content.replace(old, new, 1)
        write_file(filepath, content)
        log_fix(filepath, "Removed stray </div> inside <li> in research frontier callout")
        return True
    return False


# ---------------------------------------------------------------------------
# Pattern 5: </strong> closing where </em> expected (section 10.4)
# Line 633: <em>adaptive reasoning</em> would allow... </strong>
# The </strong> has no matching <strong>.
# ---------------------------------------------------------------------------
def fix_stray_strong_close(filepath):
    """Fix stray </strong> that appears in research frontier paragraphs.

    Pattern A: <em>text</em> ... sentence end.</strong> Next sentence.
    Pattern B: <a>text</a> ... sentence end.</strong> Next sentence.
    In both cases, the </strong> has no matching <strong> open tag.
    """
    content = read_file(filepath)
    changed = False

    # Pattern A: </em> ... .</strong> with no <strong> in between
    new_content = re.sub(
        r'</em>((?:(?!</em>|<strong>|</p>).)*?)\.</strong>',
        r'</em>\1.',
        content,
    )
    if new_content != content:
        content = new_content
        changed = True

    # Pattern B: </a> ... .</strong> with no <strong> in between
    new_content = re.sub(
        r'</a>((?:(?!</a>|<strong>|</p>|</em>).)*?)\.</strong>',
        r'</a>\1.',
        content,
    )
    if new_content != content:
        content = new_content
        changed = True

    if changed:
        write_file(filepath, content)
        log_fix(filepath, "Removed stray </strong> (no matching <strong>)")
    return changed


# ---------------------------------------------------------------------------
# Pattern 6: <div class="answer"> with bare text ending </p>
# These divs contain text without an opening <p> but with a closing </p>.
# Fix: add <p> after the <div class="answer"> opening.
# ---------------------------------------------------------------------------
def fix_answer_div_missing_p(filepath):
    content = read_file(filepath)
    lines = content.split("\n")
    changed = False

    # Fix answer divs that have orphan </p> (no matching <p> open).
    # Two variants:
    # Variant A (single-line): <div class="answer">text.</p>
    #   Next line is </details> or similar (no </div> for this div).
    #   Fix: <div class="answer"><p>text.</p></div>
    #
    # Variant B (multi-line): <div class="answer">text.</p>\n</div>
    #   Fix: <div class="answer"><p>text.</p>\n</div>

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Check if this line has <div class="answer"> with content
        if '<div class="answer">' not in stripped:
            continue

        # Extract after the div tag
        idx = stripped.index('<div class="answer">')
        after = stripped[idx + len('<div class="answer">'):]

        # Skip if already has <p> tag
        if after.lstrip().startswith("<p>"):
            continue

        # Variant A: line ends with </p> (no </div>)
        if after.rstrip().endswith("</p>") and not after.rstrip().endswith("</div>"):
            # Add <p> after <div class="answer"> and </div> after </p>
            lines[i] = line.replace(
                '<div class="answer">' + after,
                '<div class="answer"><p>' + after.rstrip()[:-4] + '</p></div>'
            )
            changed = True
            continue

        # Variant B: line ends with </p> then next line is </div>
        # or line has content ending with </p> and </div> is after
        if after.rstrip().endswith("</div>"):
            # Check if there's </p> just before </div>
            before_div = after.rstrip()[:-len("</div>")].rstrip()
            if before_div.endswith("</p>") and "<p>" not in after:
                lines[i] = line.replace(
                    '<div class="answer">' + after,
                    '<div class="answer"><p>' + after
                )
                changed = True
                continue

        # Variant B multi-line: line has <div class="answer">text
        # and next non-blank lines end with </p>\n</div>
        if i + 1 < len(lines) and lines[i + 1].strip() == "</div>":
            # The content ends on this line, next is </div>
            if after.rstrip().endswith("</p>") and "<p>" not in after:
                lines[i] = line.replace(
                    '<div class="answer">' + after,
                    '<div class="answer"><p>' + after
                )
                changed = True

    if changed:
        content = "\n".join(lines)
        write_file(filepath, content)
        log_fix(filepath, "Fixed <div class='answer'> with orphan </p>")
    return changed


# ---------------------------------------------------------------------------
# Pattern 7: <div class="diagram-caption"> ending with </p> instead of </div>
# Fix: replace the </p> with nothing (the </div> on next line handles closing)
# ---------------------------------------------------------------------------
def fix_diagram_caption_p(filepath):
    content = read_file(filepath)
    changed = False

    # Pattern: <div class="diagram-caption"><strong>Figure...</strong> text.</p>
    # The </p> is wrong since there's no <p> opening.
    # Fix: remove the </p>.
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if '<div class="diagram-caption">' in line and line.rstrip().endswith("</p>"):
            # Check there's no <p> in this line
            if "<p>" not in line:
                lines[i] = line.rstrip()[:-4]  # remove </p>
                changed = True
    new_content = "\n".join(lines)

    if new_content != content:
        content = new_content
        changed = True
        write_file(filepath, content)
        log_fix(filepath, "Removed stray </p> from diagram-caption div")
    return changed


# ---------------------------------------------------------------------------
# Pattern 2b: Extra </div> for files in module-32/33 that have imbalance of 2
# More targeted: find files with +2 div imbalance and remove the two extra </div>
# ---------------------------------------------------------------------------
def fix_remaining_div_imbalance(filepath):
    """Second pass: handle any remaining div imbalance by finding extra </div>."""
    content = read_file(filepath)
    opens, closes = count_div_balance(content)

    if closes <= opens:
        return False

    excess = closes - opens
    lines = content.split("\n")
    changed = False

    # Strategy: find standalone </div> lines in suspicious locations.
    # Score each candidate by how "suspicious" it looks, then remove
    # the top N candidates where N = excess.

    candidates = []  # (score, line_index)

    for i in range(len(lines)):
        stripped = lines[i].strip()
        if stripped != "</div>":
            continue

        # Get context
        next_content = ""
        for j in range(i + 1, min(i + 5, len(lines))):
            if lines[j].strip():
                next_content = lines[j].strip()
                break

        prev_content = ""
        for j in range(i - 1, max(i - 5, -1), -1):
            if lines[j].strip():
                prev_content = lines[j].strip()
                break

        score = 0

        # High score: between </div> (or closing tag) and <div class="callout
        # or <div class="whats-next" or <h2> or <section
        if next_content.startswith('<div class="callout'):
            score += 5
        if next_content.startswith('<div class="whats-next'):
            score += 4
        if next_content.startswith("<h2"):
            score += 4
        if next_content.startswith("<figure"):
            score += 3
        if next_content.startswith("<section"):
            score += 3
        if next_content.startswith("<h2>Exercises") or next_content.startswith("<h2>Exercise"):
            score += 5
        if prev_content == "</div>":
            score += 2
        if prev_content.endswith("</div>"):
            score += 1

        # Penalty: if this is likely closing a real div
        # (e.g., prev is content, next is </details>)
        if next_content.startswith("</details"):
            score -= 3
        if next_content.startswith("</section"):
            score -= 2

        if score > 0:
            candidates.append((score, i))

    # Sort by score descending, take the top `excess` candidates
    candidates.sort(key=lambda x: -x[0])
    removal_indices = [idx for _, idx in candidates[:excess]]

    if removal_indices:
        for idx in sorted(removal_indices, reverse=True):
            lines.pop(idx)
        content = "\n".join(lines)
        write_file(filepath, content)
        changed = True
        log_fix(filepath, f"Removed {len(removal_indices)} extra </div> (div imbalance fix)")

    return changed


# ---------------------------------------------------------------------------
# Pattern 8: Unclosed <div class="whats-next"> before <section class="bibliography">
# The whats-next div starts but is never closed. Insert </div> before the next
# <section> tag (bibliography).
# ---------------------------------------------------------------------------
def fix_unclosed_whats_next(filepath):
    content = read_file(filepath)
    lines = content.split("\n")
    changed = False

    in_whats_next = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if '<div class="whats-next">' in stripped:
            in_whats_next = True
            continue
        if in_whats_next and stripped.startswith("<section"):
            # Insert </div> before this <section> to close the whats-next div
            indent = len(line) - len(line.lstrip())
            lines.insert(i, " " * indent + "</div>")
            changed = True
            break

    if changed:
        content = "\n".join(lines)
        write_file(filepath, content)
        log_fix(filepath, "Closed unclosed <div class='whats-next'>")
    return changed


# ---------------------------------------------------------------------------
# Pattern 9: Unclosed last <div class="bib-entry-card"> before </section>
# The final bib-entry-card is missing </div>.
# ---------------------------------------------------------------------------
def fix_unclosed_bib_entry_card(filepath):
    content = read_file(filepath)

    # Find the last <div class="bib-entry-card"> and check if it's closed
    # before </section>
    pattern = r'(<div class="bib-entry-card">)((?:(?!<div class="bib-entry-card">).)*?)(</section>)'
    matches = list(re.finditer(pattern, content, re.DOTALL))

    if not matches:
        return False

    # Check the LAST match: count divs inside
    m = matches[-1]
    inner = m.group(2)
    inner_opens = len(re.findall(r"<div[\s>]", inner))
    inner_closes = len(re.findall(r"</div>", inner))

    if inner_opens <= inner_closes:
        # The bib-entry-card div itself is unclosed
        end_pos = m.start(3)
        content = content[:end_pos] + "</div>\n" + content[end_pos:]
        write_file(filepath, content)
        log_fix(filepath, "Closed unclosed <div class='bib-entry-card'>")
        return True

    return False


# ---------------------------------------------------------------------------
# Main: collect files and apply fixes
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("HTML Structure Fix Script")
    print("=" * 70)
    print()

    # Collect all HTML files from the audit report
    # We'll process all HTML files in content directories
    content_dirs = [
        "front-matter", "part-1-foundations", "part-2-understanding-llms",
        "part-3-working-with-llms", "part-4-training-adapting",
        "part-5-retrieval-conversation", "part-6-agentic-ai",
        "part-7-multimodal-applications", "part-8-evaluation-production",
        "part-9-safety-strategy", "part-10-frontiers", "part-11-idea-to-product",
        "appendices",
    ]

    html_files = []
    for cdir in content_dirs:
        full_dir = ROOT / cdir
        if not full_dir.is_dir():
            continue
        for fpath in full_dir.rglob("*.html"):
            html_files.append(fpath)
    html_files.sort()

    print(f"Found {len(html_files)} HTML files.\n")

    # -----------------------------------------------------------------------
    # Phase 1: Specific targeted fixes
    # -----------------------------------------------------------------------
    print("--- Phase 1: Targeted fixes for specific files ---\n")

    # Section 30.1: stray </div> inside <li>
    p = ROOT / "part-8-evaluation-production/module-30-observability-monitoring/section-30.1.html"
    if p.exists():
        fix_section_30_1(p)

    # Stray </strong> with no matching <strong> (multiple files)
    stray_strong_files = [
        "part-3-working-with-llms/module-10-llm-apis/section-10.4.html",
        "part-4-training-adapting/module-13-synthetic-data/section-13.1.html",
        "part-4-training-adapting/module-13-synthetic-data/section-13.2.html",
        "part-4-training-adapting/module-13-synthetic-data/section-13.3.html",
        "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.1.html",
        "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.3.html",
        "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.4.html",
        "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.6.html",
        "part-4-training-adapting/module-16-distillation-merging/section-16.3.html",
        "part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.3.html",
    ]
    # The stray_strong_close function handles the </em>...</strong> pattern.
    # For files where </strong> appears without </em> preceding, use a
    # broader approach below.
    for rel in stray_strong_files:
        p = ROOT / rel
        if p.exists():
            fix_stray_strong_close(p)

    # Section 14.1: broken tag </div>div class=...> (missing < before div)
    p = ROOT / "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.1.html"
    if p.exists():
        content = read_file(p)
        old = '</div>div class="callout research-frontier">'
        new = '</div>\n<div class="callout research-frontier">'
        if old in content:
            content = content.replace(old, new, 1)
            write_file(p, content)
            log_fix(p, "Fixed broken tag: </div>div -> </div>\\n<div")

    # -----------------------------------------------------------------------
    # Phase 2: Fix stray </div> after epigraph in chapters 32 and 33
    # -----------------------------------------------------------------------
    print("\n--- Phase 2: Fix stray </div> after epigraph (ch32/33) ---\n")

    ch32_dir = ROOT / "part-9-safety-strategy/module-32-safety-ethics-regulation"
    ch33_dir = ROOT / "part-9-safety-strategy/module-33-strategy-product-roi"

    for d in [ch32_dir, ch33_dir]:
        if not d.is_dir():
            continue
        for fpath in sorted(d.glob("section-*.html")):
            fix_stray_div_after_epigraph(fpath)

    # -----------------------------------------------------------------------
    # Phase 3: Fix unclosed <div class="lab">
    # -----------------------------------------------------------------------
    print("\n--- Phase 3: Fix unclosed <div class='lab'> ---\n")

    for fname in ["section-32.1.html", "section-33.3.html"]:
        if "32" in fname:
            p = ch32_dir / fname
        else:
            p = ch33_dir / fname
        if p.exists():
            fix_unclosed_lab_div(p)

    # -----------------------------------------------------------------------
    # Phase 4: Fix <div class="answer"> missing <p>
    # -----------------------------------------------------------------------
    print("\n--- Phase 4: Fix <div class='answer'> missing <p> ---\n")

    for fpath in html_files:
        fix_answer_div_missing_p(fpath)

    # -----------------------------------------------------------------------
    # Phase 5: Fix diagram-caption ending with </p>
    # -----------------------------------------------------------------------
    print("\n--- Phase 5: Fix diagram-caption stray </p> ---\n")

    for fpath in html_files:
        fix_diagram_caption_p(fpath)

    # -----------------------------------------------------------------------
    # Phase 5b: Fix unclosed last <div class="bib-entry-card"> before </section>
    # -----------------------------------------------------------------------
    print("\n--- Phase 5b: Fix unclosed <div class='bib-entry-card'> ---\n")

    bib_entry_files = [
        "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.1.html",
        "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html",
        "part-1-foundations/module-02-tokenization-subword-models/section-2.1.html",
        "part-1-foundations/module-02-tokenization-subword-models/section-2.2.html",
        "part-1-foundations/module-02-tokenization-subword-models/section-2.3.html",
    ]
    for rel in bib_entry_files:
        p = ROOT / rel
        if p.exists():
            fix_unclosed_bib_entry_card(p)

    # -----------------------------------------------------------------------
    # Phase 6: Insert missing </main> (broadest fix, most files)
    # -----------------------------------------------------------------------
    print("\n--- Phase 6: Insert missing </main> ---\n")

    for fpath in html_files:
        fix_missing_main_close(fpath)

    # -----------------------------------------------------------------------
    # Phase 7: Final pass to fix remaining div imbalances
    # -----------------------------------------------------------------------
    print("\n--- Phase 7: Fix remaining div imbalances ---\n")

    for d in [ch32_dir, ch33_dir]:
        if not d.is_dir():
            continue
        for fpath in sorted(d.glob("section-*.html")):
            content = read_file(fpath)
            opens, closes = count_div_balance(content)
            if closes > opens:
                fix_remaining_div_imbalance(fpath)

    # Also check other files flagged in the report
    imbalanced_files = [
        "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html",
        "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html",
        "part-1-foundations/module-04-transformer-architecture/section-4.1.html",
        "part-1-foundations/module-04-transformer-architecture/section-4.2.html",
        "part-1-foundations/module-04-transformer-architecture/section-4.3.html",
        "part-1-foundations/module-04-transformer-architecture/section-4.4.html",
        "part-1-foundations/module-04-transformer-architecture/section-4.5.html",
        "part-2-understanding-llms/module-18-interpretability/section-18.2.html",
        "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.1.html",
        "part-8-evaluation-production/module-29-evaluation-observability/section-29.11.html",
        "part-8-evaluation-production/module-30-observability-monitoring/section-30.1.html",
        "part-8-evaluation-production/module-31-production-engineering/section-31.1.html",
        "part-8-evaluation-production/module-31-production-engineering/section-31.2.html",
        "part-8-evaluation-production/module-31-production-engineering/section-31.3.html",
        "part-8-evaluation-production/module-31-production-engineering/section-31.4.html",
    ]

    for rel in imbalanced_files:
        fpath = ROOT / rel
        if fpath.exists():
            content = read_file(fpath)
            opens, closes = count_div_balance(content)
            if closes > opens:
                fix_remaining_div_imbalance(fpath)

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("\n" + "=" * 70)
    print(f"SUMMARY: {len(FIXES_APPLIED)} fixes applied across {len(set(r for r, _ in FIXES_APPLIED))} files")
    print("=" * 70)

    # Verify div balance on all previously-imbalanced files
    print("\n--- Verification: div balance check ---\n")
    all_imbalanced_files = imbalanced_files + [
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.1.html",
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.2.html",
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.3.html",
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.4.html",
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.5.html",
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.6.html",
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.7.html",
        "part-9-safety-strategy/module-33-strategy-product-roi/section-33.1.html",
        "part-9-safety-strategy/module-33-strategy-product-roi/section-33.2.html",
        "part-9-safety-strategy/module-33-strategy-product-roi/section-33.3.html",
        "part-9-safety-strategy/module-33-strategy-product-roi/section-33.4.html",
        "part-9-safety-strategy/module-33-strategy-product-roi/section-33.5.html",
    ]

    still_imbalanced = 0
    for rel in all_imbalanced_files:
        fpath = ROOT / rel
        if fpath.exists():
            content = read_file(fpath)
            opens, closes = count_div_balance(content)
            status = "OK" if opens == closes else f"STILL IMBALANCED ({opens} opens, {closes} closes)"
            if opens != closes:
                still_imbalanced += 1
                print(f"  {rel}: {status}")

    if still_imbalanced == 0:
        print("  All previously-imbalanced files now have balanced divs.")
    else:
        print(f"\n  {still_imbalanced} files still have div imbalance.")


if __name__ == "__main__":
    main()
