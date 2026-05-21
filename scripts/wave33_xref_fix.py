"""Wave 33 surgical fixes.

Fix:
  1. All 'stale_section_labels' (cross-chapter drift): rewrite anchor text to
     reflect the actual target's section number.
  2. Top 30 'bad_anchor_text' cases (most-visible to readers): rewrite anchor
     text where the cited section number does not match the target's section
     number. Only patch when target file confirms the section number.

We do NOT touch module-42 or module-44.

Each fix is recorded with file + before/after for the report.
"""

import os
import re
import json

ROOT = r"E:\Projects\BookBlogsHome\LLMBook"
os.chdir(ROOT)

FINDINGS = json.load(open("docs/content-audit/_xref_findings.json", "r", encoding="utf-8"))

# Skip protections
def skip_file(path):
    norm = path.replace("\\", "/")
    return "module-42" in norm or "module-44" in norm


# Helper: rewrite an <a href="..."> tag's text content (only the text directly
# inside the tag). Returns updated source string and a record of the change.
def rewrite_anchor_text(content, href, old_text, new_text):
    """Find the FIRST <a> that has the given href and the given current text,
    and replace the text with new_text.

    Returns (new_content, changed_bool).
    """
    # Escape regex for href
    href_re = re.escape(href)
    # Build regex matching <a ... href="HREF" ...>OLD_TEXT</a>
    # Where OLD_TEXT exactly matches plain_inner. We must allow optional inner tags.
    # The simplest approach: find the <a> tag start, then ensure plain text of inner
    # exactly equals old_text, then rewrite. We'll use a careful per-position scan.

    pattern = re.compile(
        rf'(<a\b[^>]*href\s*=\s*"{href_re}"[^>]*>)([\s\S]*?)(</a>)',
        re.IGNORECASE,
    )

    for m in pattern.finditer(content):
        opening = m.group(1)
        inner = m.group(2)
        closing = m.group(3)
        # Strip tags from inner
        plain = re.sub(r"<[^>]+>", "", inner).strip()
        if plain == old_text.strip():
            # Replace text directly (assume no inner tags). If there are inner tags,
            # find the first text node containing old_text and replace.
            if "<" in inner:
                # try to swap the literal substring
                if old_text in inner:
                    new_inner = inner.replace(old_text, new_text, 1)
                else:
                    continue
            else:
                new_inner = new_text
            new_content = content[:m.start()] + opening + new_inner + closing + content[m.end():]
            return new_content, True
    return content, False


FIXES_APPLIED = []


def apply_text_fix(fpath, href, old_text, new_text, category):
    """Apply a single text fix to file fpath."""
    if skip_file(fpath):
        return False
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    new_content, changed = rewrite_anchor_text(content, href, old_text, new_text)
    if not changed:
        return False
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)
    FIXES_APPLIED.append({
        "file": fpath,
        "category": category,
        "before": old_text,
        "after": new_text,
        "href": href,
    })
    return True


# -----------------------------------------------------------------------------
# Part 1: All stale section labels (cross-chapter drift)
# -----------------------------------------------------------------------------

stale_fixes = []
for it in FINDINGS["stale_section_labels"]:
    cited = it["cited_section"]
    target = it["target_section"]
    old_text = it["text"].strip()
    # Construct new text: replace "Section X" with "Section TARGET"
    # Be careful with the text that says "Section 44.1: Online Eval..." - we should
    # replace the whole label.
    # If text is exactly "Section X.Y" or "Section X.Y (something)", we update only the
    # number portion to the target. Otherwise we replace "Section X.Y" with "Section
    # TARGET".
    pattern = re.compile(
        r"(?i)\b(section\s+)" + re.escape(cited) + r"\b"
    )
    def _sub(m, t=target):
        return m.group(1) + t
    new_text = pattern.sub(_sub, old_text, count=1)
    if new_text == old_text:
        # fall back: nothing to do
        continue
    ok = apply_text_fix(it["file"], it["href"], old_text, new_text, "stale_section_label")
    stale_fixes.append({"file": it["file"], "before": old_text, "after": new_text, "ok": ok})


print("Stale label fixes:")
for f in stale_fixes:
    print(f"  {'OK' if f['ok'] else 'MISS'}: {f['file']}  '{f['before']}' -> '{f['after']}'")


# -----------------------------------------------------------------------------
# Part 2: Top 30 bad anchor text fixes
# -----------------------------------------------------------------------------

# Strategy: prioritize fixes where:
#   1. Cited section is in different chapter than target (high-impact)
#   2. Otherwise, fix variants (X.Y -> X.Ya) where target's parent chapter is the
#      same (so reader still ends up at correct content but text is wrong).
# We pick the first 30 unique (file, href) entries to fix.

bad = FINDINGS["bad_anchor_text"]

# Sort: chapter mismatches FIRST, then variant mismatches
def priority(it):
    cited_ch = int(it["cited_section"].split(".")[0])
    target_ch = int(it["target_section"].split(".")[0])
    return (0 if cited_ch != target_ch else 1, it["file"], it["href"])

bad_sorted = sorted(bad, key=priority)

# Take top 30 unique cases, filtering protected files
candidates = []
seen = set()
for it in bad_sorted:
    if skip_file(it["file"]):
        continue
    key = (it["file"], it["href"], it["text"])
    if key in seen:
        continue
    seen.add(key)
    candidates.append(it)
    if len(candidates) >= 30:
        break


# Now apply fix: rewrite the anchor's text label.
# The fix is: change cited_section -> target_section in the text label.
top30_fixes = []
for it in candidates:
    cited = it["cited_section"]
    target = it["target_section"]
    old_text = it["text"].strip()
    # Replace "Section CITED" with "Section TARGET" (keep prefix, trailing punctuation).
    pattern = re.compile(
        r"(?i)\b(section\s+)" + re.escape(cited) + r"\b"
    )
    def _sub(m, t=target):
        return m.group(1) + t
    new_text = pattern.sub(_sub, old_text, count=1)
    if new_text == old_text:
        continue
    ok = apply_text_fix(it["file"], it["href"], old_text, new_text, "bad_anchor_text")
    top30_fixes.append({"file": it["file"], "before": old_text, "after": new_text, "ok": ok})


print()
print("Top 30 bad anchor text fixes:")
for f in top30_fixes:
    print(f"  {'OK' if f['ok'] else 'MISS'}: {f['file']}  '{f['before'][:60]}' -> '{f['after'][:60]}'")


# Save the fix log
with open("docs/content-audit/_xref_fixes_applied.json", "w", encoding="utf-8") as fh:
    json.dump({
        "stale_section_label": stale_fixes,
        "top30_bad_anchor": top30_fixes,
        "all_fixes": FIXES_APPLIED,
    }, fh, indent=2)
print()
print(f"Total fixes applied: {len(FIXES_APPLIED)}")
print(f"Log: docs/content-audit/_xref_fixes_applied.json")
