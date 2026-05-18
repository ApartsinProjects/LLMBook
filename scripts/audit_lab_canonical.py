"""Audit Lab callouts against the canonical 8-subdiv structure.

Canonical Lab callout (per task spec):
  <div class="callout lab" id="lab-X-Y">
    <div class="callout-title">Lab: <Title></div>
    <div class="lab-meta">...</div>
    <div class="lab-objective"><h3>Objective</h3>...</div>
    <div class="lab-skills"><h3>What You'll Practice</h3>...</div>
    <div class="lab-prereqs"><h3>Setup</h3>...</div>
    <div class="lab-steps"><h3>Steps</h3>...</div>
    <div class="lab-expected"><h3>Expected Output</h3>...</div>
    <div class="lab-stretch"><h3>Stretch Goals</h3>...</div>
  </div>

Reports per Lab:
  - canonical title?
  - which sub-divs are present?
  - which sub-divs have an inner h3?
  - any inline content immediately under callout-title (orphan)?
"""
import os
import re
import glob

ROOT = r"E:\Projects\BookBlogsHome\LLMBook"

patterns = [
    os.path.join(ROOT, "part-*", "module-*", "section-*.html"),
    os.path.join(ROOT, "appendices", "*", "section-*.html"),
]

files = []
for p in patterns:
    files.extend(sorted(glob.glob(p)))

CANONICAL_SUBDIVS = [
    "lab-meta",
    "lab-objective",
    "lab-skills",
    "lab-prereqs",
    "lab-steps",
    "lab-expected",
    "lab-stretch",
]
# lab-meta has spans, not h3. All others should have an h3.
SUBDIVS_NEED_H3 = {
    "lab-objective", "lab-skills", "lab-prereqs",
    "lab-steps", "lab-expected", "lab-stretch",
}

SKIP_MODULE_NAME = "tools-of-the-trade"


def parse_lab_callout(content, start_idx):
    """Find the matching </div> for the lab callout starting at start_idx,
    returning (end_idx, inner_content)."""
    depth = 1
    i = start_idx
    while i < len(content):
        # Find next <div or </div>
        m_open = re.search(r"<div\b", content[i:])
        m_close = re.search(r"</div>", content[i:])
        if not m_close:
            return -1, ""
        if m_open and m_open.start() < m_close.start():
            depth += 1
            i += m_open.end()
        else:
            depth -= 1
            i += m_close.end()
            if depth == 0:
                return i, content[start_idx:i - len("</div>")]
    return -1, ""


report = []

for fpath in files:
    rel = os.path.relpath(fpath, ROOT).replace("\\", "/")
    if SKIP_MODULE_NAME in rel:
        continue
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Find every <div class="callout lab"> (or with id)
    for m in re.finditer(r'<div\s+class="callout lab"(?:\s+id="([^"]*)")?\s*>', content):
        lab_id = m.group(1) or "(no-id)"
        callout_start_line = content[:m.start()].count("\n") + 1
        # Capture inner content
        end_idx, inner = parse_lab_callout(content, m.end())
        if end_idx == -1:
            report.append({
                "file": rel,
                "line": callout_start_line,
                "id": lab_id,
                "error": "unclosed lab callout",
            })
            continue

        # Find callout-title
        title_m = re.search(r'<div\s+class="callout-title">(.*?)</div>', inner, re.DOTALL)
        title_text = title_m.group(1).strip() if title_m else ""
        canonical_title = title_text.startswith("Lab:") or title_text.startswith("Lab :")

        # Check each canonical sub-div
        present = {}
        h3_present = {}
        for cls in CANONICAL_SUBDIVS:
            cls_re = rf'<div\s+class="{cls}"\s*>'
            sub_m = re.search(cls_re, inner)
            present[cls] = sub_m is not None
            if sub_m:
                # Look ahead to closing </div> for inner h3
                sub_end_idx = sub_m.end()
                # Track depth
                d = 1
                j = sub_end_idx
                while j < len(inner) and d > 0:
                    next_open = re.search(r"<div\b", inner[j:])
                    next_close = re.search(r"</div>", inner[j:])
                    if not next_close:
                        break
                    if next_open and next_open.start() < next_close.start():
                        d += 1
                        j += next_open.end()
                    else:
                        d -= 1
                        j += next_close.end()
                sub_body = inner[sub_end_idx:j - len("</div>")]
                h3_present[cls] = bool(re.search(r"<h3\b", sub_body))
            else:
                h3_present[cls] = False

        missing_subdivs = [c for c in CANONICAL_SUBDIVS if not present[c]]
        missing_h3 = [c for c in SUBDIVS_NEED_H3 if present[c] and not h3_present[c]]

        report.append({
            "file": rel,
            "line": callout_start_line,
            "id": lab_id,
            "title": title_text[:80],
            "canonical_title": canonical_title,
            "missing_subdivs": missing_subdivs,
            "missing_h3": missing_h3,
        })


# Print report
print(f"\n=== LAB CANONICAL AUDIT ({len(report)} labs) ===\n")
canonical_count = 0
non_canonical_count = 0
title_issues = []
subdiv_issues = []
h3_issues = []
for r in report:
    if "error" in r:
        print(f"  ERROR {r['file']}:{r['line']} {r['id']}: {r['error']}")
        continue
    issues = []
    if not r["canonical_title"]:
        issues.append("non-canonical title")
        title_issues.append(r)
    if r["missing_subdivs"]:
        issues.append(f"missing: {', '.join(r['missing_subdivs'])}")
        subdiv_issues.append(r)
    if r["missing_h3"]:
        issues.append(f"missing h3 in: {', '.join(r['missing_h3'])}")
        h3_issues.append(r)
    if issues:
        non_canonical_count += 1
        print(f"  {r['file']}:{r['line']} [{r['id']}] {r['title'][:50]}")
        for iss in issues:
            print(f"    - {iss}")
    else:
        canonical_count += 1

print(f"\nTotals: {canonical_count} canonical, {non_canonical_count} with issues")
print(f"  Title issues: {len(title_issues)}")
print(f"  Sub-div issues: {len(subdiv_issues)}")
print(f"  h3 issues: {len(h3_issues)}")

# Per-subdiv frequency of missing
counts = {c: 0 for c in CANONICAL_SUBDIVS}
for r in report:
    if "error" in r:
        continue
    for c in r.get("missing_subdivs", []):
        counts[c] += 1
print("\nMissing sub-div frequency:")
for c, n in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {c}: {n} labs missing it")
