"""Fix SECTION_ORDER bugs: reorganize epigraph + big-picture + prerequisites.

Pattern detected in the broken sections:
  Line A: <blockquote class="epigraph">
  Line A+1: <p>QUOTE + INTRO_PROSE</p>     # inflated: epigraph paragraph contains both
  Line A+2: </div>                          # wrong closing tag (should be </blockquote>)
  Line A+3: <div class="prerequisites">...
  ...
  Line B: ...content... </div>
  Line B+1: <span class="agent-avatar-inline">...<cite>...</cite>
  Line B+2: </blockquote>                   # orphan blockquote close that should belong to epigraph
  Line B+3: <div class="callout big-picture">
  Line B+4: <div class="callout-title">Big Picture</div>
  Line B+5: <details class="bibliography-collapsible">  # bibliography inside big-picture; big-picture is empty

Fix:
  - Split epigraph paragraph: extract quote + introductory prose
  - Move avatar/cite from orphan location to immediately after the quote
  - Properly close </blockquote> for the epigraph
  - Insert filled big-picture callout BEFORE prerequisites using the extracted intro prose
  - Convert the empty big-picture+bibliography wrapper into a proper bibliography section

For 47.1b which has 3 issues (Prereq before BP + orphan h2 + orphan callout after whats-next),
we handle similarly: detect that the orphan content goes AFTER whats-next (but should be before).
"""
import re
import sys
from pathlib import Path

# Paths relative to project root
TARGETS = [
    "part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7a.html",
    "part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.1.html",
    "part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.2.html",
    "part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.3.html",
    "part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.4.html",
    "part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.5.html",
    "part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.1.html",
    "part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.2.html",
    "part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.3.html",
    "part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.10.html",
    "part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.6.html",
    "part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.8.html",
    "part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.9.html",
    "part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.5.html",
    "part-5-multimodal-llms/module-24-vla-models/section-24.1.html",
    "part-5-multimodal-llms/module-24-vla-models/section-24.10.html",
    "part-5-multimodal-llms/module-24-vla-models/section-24.11.html",
    "part-5-multimodal-llms/module-24-vla-models/section-24.12.html",
    "part-5-multimodal-llms/module-24-vla-models/section-24.13.html",
    "part-5-multimodal-llms/module-24-vla-models/section-24.2.html",
    "part-5-multimodal-llms/module-24-vla-models/section-24.3.html",
    "part-5-multimodal-llms/module-24-vla-models/section-24.4.html",
    "part-5-multimodal-llms/module-24-vla-models/section-24.5.html",
    "part-5-multimodal-llms/module-24-vla-models/section-24.7.html",
    "part-5-multimodal-llms/module-24-vla-models/section-24.8.html",
    "part-5-multimodal-llms/module-24-vla-models/section-24.9.html",
    "part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.5.html",
]


def split_epigraph_paragraph(p_text):
    """Split an inflated epigraph paragraph into (quote, intro_prose).

    Heuristic:
      - If it starts with a quote (" or "), the quote ends at the closing ".
      - Otherwise, the first sentence (up to first period followed by space + capital) is the quote.
      - Everything else is intro prose.
    """
    # Strip outer whitespace and newlines
    t = p_text.strip()
    # Case 1: Quoted opening
    m = re.match(r'^(["“])([^"”]+?)(["”])\s*(.*)$', t, re.DOTALL)
    if m:
        quote = m.group(1) + m.group(2) + m.group(3)
        rest = m.group(4).strip()
        return quote, rest
    # Case 2: First sentence (ends with . followed by space + capital letter or word)
    m = re.match(r'^(.+?[.!?])\s+([A-Z].*)$', t, re.DOTALL)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    # Fallback: split on first period
    if '.' in t:
        idx = t.index('.') + 1
        return t[:idx].strip(), t[idx:].strip()
    return t, ""


def fix_file(filepath: Path) -> tuple[str, bool]:
    """Returns (description, success)."""
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")

    # 1. Find the epigraph block
    epi_start = None
    for i, line in enumerate(lines):
        if 'class="epigraph"' in line and '<blockquote' in line:
            epi_start = i
            break

    if epi_start is None:
        return ("No <blockquote class=epigraph> found", False)

    # 2. Detect inflated epigraph: look for <p>...</p> followed by </div> (wrong close)
    # The epigraph paragraph typically spans 1 or more lines.
    p_start = None
    p_end = None
    blockquote_end = None
    for j in range(epi_start + 1, min(epi_start + 30, len(lines))):
        line = lines[j]
        if p_start is None and '<p>' in line:
            p_start = j
        if p_start is not None and ('</p>' in line):
            p_end = j
            # next non-empty line should be </blockquote> or </div>
            for k in range(j + 1, min(j + 5, len(lines))):
                if '</blockquote>' in lines[k] or '</div>' in lines[k]:
                    blockquote_end = k
                    break
            break

    if p_start is None or p_end is None or blockquote_end is None:
        return ("Could not parse epigraph paragraph", False)

    # 3. Extract paragraph text (between <p> and </p>, possibly across lines)
    if p_start == p_end:
        # Single line
        m = re.search(r'<p>(.*?)</p>', lines[p_start], re.DOTALL)
        p_text = m.group(1) if m else ""
    else:
        p_text_parts = []
        for k in range(p_start, p_end + 1):
            line = lines[k]
            if k == p_start:
                m = re.search(r'<p>(.*)$', line)
                p_text_parts.append(m.group(1) if m else "")
            elif k == p_end:
                m = re.search(r'^(.*?)</p>', line)
                p_text_parts.append(m.group(1) if m else "")
            else:
                p_text_parts.append(line)
        p_text = "\n".join(p_text_parts)

    quote, intro_prose = split_epigraph_paragraph(p_text)

    # 4. Find the orphan avatar+cite+</blockquote> later in file.
    # Pattern A: <span class="agent-avatar-inline">...<cite>...</cite></blockquote>
    # Pattern B: <cite>...</cite> on one line, </blockquote> on the next (no avatar)
    orphan_avatar_line = None
    orphan_blockquote_line = None
    orphan_cite_line = None
    for k in range(blockquote_end + 1, len(lines)):
        if 'class="agent-avatar-inline"' in lines[k]:
            orphan_avatar_line = k
        if orphan_avatar_line is not None and '</blockquote>' in lines[k]:
            orphan_blockquote_line = k
            break

    # Fallback: bare <cite> followed by </blockquote>
    if orphan_blockquote_line is None:
        for k in range(blockquote_end + 1, len(lines)):
            if '<cite>' in lines[k] and 'agent-avatar-inline' not in lines[k]:
                # Check that next line(s) contain </blockquote> within 3 lines
                for m in range(k, min(k + 3, len(lines))):
                    if '</blockquote>' in lines[m]:
                        orphan_cite_line = k
                        orphan_blockquote_line = m
                        break
                if orphan_blockquote_line is not None:
                    break

    # 5. Find empty big-picture callout (right after orphan </blockquote>).
    bp_start = None
    bp_title_end = None
    details_start = None
    details_end = None
    search_from = (orphan_blockquote_line + 1) if orphan_blockquote_line is not None else (blockquote_end + 1)
    for k in range(search_from, len(lines)):
        if 'class="callout big-picture"' in lines[k]:
            bp_start = k
            # Next line(s) should have callout-title
            for m in range(k + 1, k + 4):
                if m < len(lines) and 'callout-title' in lines[m]:
                    bp_title_end = m
                    break
            # Then <details class="bibliography-collapsible">
            for m in range((bp_title_end or k) + 1, (bp_title_end or k) + 5):
                if m < len(lines) and 'bibliography-collapsible' in lines[m]:
                    details_start = m
                    break
            break

    # 6. Find </details> closing for the bibliography
    if details_start is not None:
        for k in range(details_start, len(lines)):
            if '</details>' in lines[k]:
                details_end = k
                break

    # 7. Extract avatar+cite content (without trailing </blockquote>)
    avatar_cite_block = []
    first_orphan_line = orphan_avatar_line if orphan_avatar_line is not None else orphan_cite_line
    if first_orphan_line is not None and orphan_blockquote_line is not None:
        for k in range(first_orphan_line, orphan_blockquote_line + 1):
            line = lines[k]
            # Strip trailing </blockquote> if present
            line = line.replace('</blockquote>', '')
            if line.strip():
                avatar_cite_block.append(line)

    # 8. Build the new structure
    avatar_cite_text = "\n".join(avatar_cite_block) if avatar_cite_block else ""

    # New epigraph block
    new_epigraph = []
    new_epigraph.append('<blockquote class="epigraph">')
    new_epigraph.append(f'<p>{quote}</p>')
    if avatar_cite_text:
        new_epigraph.append(avatar_cite_text)
    new_epigraph.append('</blockquote>')

    # New big-picture block
    new_big_picture = []
    if intro_prose:
        new_big_picture.append('<div class="callout big-picture">')
        new_big_picture.append('<div class="callout-title">Big Picture</div>')
        new_big_picture.append(f'<p>{intro_prose}</p>')
        new_big_picture.append('</div>')

    # 9. Rebuild the file
    # Replace [epi_start ... blockquote_end] with new_epigraph + new_big_picture
    # Remove [orphan_avatar_line ... orphan_blockquote_line]
    # Replace [bp_start ... details_start - 1] with nothing (we'll keep <details> ... </details> but unwrap)
    # Actually we want to unwrap: remove the big-picture-callout-div wrapper but keep its bibliography content
    new_lines = []
    skip_until = -1
    first_orphan_line = orphan_avatar_line if orphan_avatar_line is not None else orphan_cite_line
    for i, line in enumerate(lines):
        if i <= skip_until:
            continue
        if i == epi_start:
            new_lines.extend(new_epigraph)
            new_lines.extend(new_big_picture)
            skip_until = blockquote_end
            continue
        if first_orphan_line is not None and i == first_orphan_line:
            # Skip avatar/cite lines (already merged into epigraph)
            skip_until = orphan_blockquote_line
            continue
        if bp_start is not None and i == bp_start:
            # Skip the empty big-picture wrapper opening lines (up to details_start - 1)
            skip_until = (details_start or i) - 1
            continue
        if details_end is not None and i == details_end:
            # Append details and skip the trailing </div> that closed big-picture
            new_lines.append(line)
            # Next line is </div> closing big-picture wrapper - skip it
            for k in range(i + 1, min(i + 5, len(lines))):
                if lines[k].strip() == '</div>' or lines[k].strip() == '':
                    if lines[k].strip() == '</div>':
                        skip_until = k
                        break
                else:
                    break
            continue
        new_lines.append(line)

    new_text = "\n".join(new_lines)
    filepath.write_text(new_text, encoding="utf-8")
    return (
        f"epi_start={epi_start+1}, p=[{p_start+1}-{p_end+1}], bq_end={blockquote_end+1}, "
        f"orphan_avatar={orphan_avatar_line+1 if orphan_avatar_line else 'None'}, "
        f"orphan_bq={orphan_blockquote_line+1 if orphan_blockquote_line else 'None'}, "
        f"bp_start={bp_start+1 if bp_start else 'None'}, "
        f"details_end={details_end+1 if details_end else 'None'}, "
        f"intro_len={len(intro_prose)}",
        True,
    )


def main():
    root = Path(".")
    results = []
    for target in TARGETS:
        fpath = root / target
        if not fpath.exists():
            results.append((target, "MISSING", False))
            continue
        try:
            desc, ok = fix_file(fpath)
        except Exception as e:
            desc = f"EXCEPTION: {e}"
            ok = False
        results.append((target, desc, ok))

    for target, desc, ok in results:
        marker = "OK" if ok else "FAIL"
        print(f"[{marker}] {target}: {desc}")
    print(f"\n{sum(1 for _, _, ok in results if ok)}/{len(results)} fixed.")


if __name__ == "__main__":
    main()
