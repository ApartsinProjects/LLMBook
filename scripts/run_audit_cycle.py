"""Audit Cycle: snapshot current plugin audit state, compare to previous, identify
highest-impact unaddressed issues, and propose the next fix wave.

Usage:
    /c/Python314/python scripts/run_audit_cycle.py

Output:
- docs/content-audit/cycle_snapshots/cycle_<N>.json
- prints delta vs previous cycle (newly-introduced / newly-resolved per check_id)
- prints top-10 categories by count, with "MECHANICAL" / "AUTHORING" / "DECISION" tag
"""
import json
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOTS_DIR = ROOT / "docs" / "content-audit" / "cycle_snapshots"
SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Categorize each plugin's findings by remediation type
REMEDIATION_TYPE = {
    # Mechanical (single-pass regex/Python sweep)
    "BROKEN_XREF": "MECHANICAL",
    "DUP_FIGURE_NUM": "MECHANICAL",
    "SVG_TITLE_TEXT": "PER-FILE",  # heuristic-flagged, needs case-by-case
    "BARE_CODE_AFTER_HEADING": "MECHANICAL",
    "BROKEN_FIGURE_REF": "MECHANICAL",
    "CAPTION_MISALIGN": "MECHANICAL",
    "CHAPTER_LABEL_NO_TITLE": "MECHANICAL",
    "CHAPTER_LABEL_ON_ANCHOR": "MECHANICAL",
    "CODE_NO_LANGUAGE": "MECHANICAL",
    "CONSECUTIVE_HEADINGS": "MECHANICAL",
    "DUP_BIB_BLOCK": "MECHANICAL",
    "EMPTY_SECTION": "AUTHORING",
    "EXCESSIVE_BLANKS": "MECHANICAL",
    "EXT_LINK_ATTRS": "MECHANICAL",
    "FIGURE_SEQUENCE": "PER-FILE",
    "FM4_PROMISE": "AUTHORING",
    "FOOTER_PLACEMENT": "MECHANICAL",
    "GENERIC_SVG_LABEL": "AUTHORING",
    "GIANT_SECTION": "DECISION",
    "GRAPHQL": "MECHANICAL",
    "HARDCODED_STYLE": "MECHANICAL",
    "HEADING_HIERARCHY": "MECHANICAL",
    "HEADING_NUM_MIX": "MECHANICAL",
    "INDEX_ORDER": "MECHANICAL",
    "INLINE_STYLE_IN_CODE": "MECHANICAL",
    "LAB_COVERAGE": "AUTHORING",
    "LATEX_SYNTAX": "MECHANICAL",
    "LEGACY_BIBLIOGRAPHY": "MECHANICAL",
    "MANUAL_HIGHLIGHT_SPANS": "MECHANICAL",
    "MATH_PROSE_MIXING": "MECHANICAL",
    "MATH_RENDERING": "MECHANICAL",
    "MISSING_IMG_DIMS": "MECHANICAL",
    "MISSING_META_DESC": "MECHANICAL",
    "MISSING_OUTPUT": "AUTHORING",
    "MISSING_SKIP_LINK": "MECHANICAL",
    "MISSING_TH_SCOPE": "MECHANICAL",
    "MIXED_CAPTION_STYLE": "MECHANICAL",
    "ORPHAN_CONTENT": "MECHANICAL",
    "ORPHAN_TAG_BEFORE_MAIN": "MECHANICAL",
    "PART_INDEX": "AUTHORING",
    "PART_LABEL_FORMAT": "MECHANICAL",
    "PART_INDEX_LAYOUT": "AUTHORING",
    "CHAPTER_INDEX_LAYOUT": "AUTHORING",
    "SECTION_PAGE_LAYOUT": "AUTHORING",
    "PLACEHOLDER_CONTENT": "MECHANICAL",
    "PSEUDO_CALLOUT": "MECHANICAL",
    "SECTION_CALLOUT": "AUTHORING",
    "SECTION_ORDER": "MECHANICAL",
    "SECTION_STRUCTURE": "AUTHORING",
    "SELFCHECK_NON_CANONICAL": "AUTHORING",
    "SVG_ARIA_TRUNCATED": "MECHANICAL",
    "SVG_OVERLAP": "PER-FILE",
    "SVG_PANEL_ASYM": "PER-FILE",
    "SVG_TEXT_CLIPPING": "PER-FILE",
    "SVG_TEXT_OVERFLOW": "PER-FILE",
    "SVG_TEXT_RIGHT_CLIP": "PER-FILE",
    "TABLE_NO_THEAD": "MECHANICAL",
    "TH_SCOPE_MISMATCH": "MECHANICAL",
    "TITLE_FORMAT": "MECHANICAL",
    "TOC_LINK_TARGET": "MECHANICAL",
    "TRIPLE_DOLLAR_MATH": "MECHANICAL",
    "TRUNCATED_NAV": "MECHANICAL",
    "UNCLOSED_PREREQ_P": "MECHANICAL",
    "UNCLOSED_P_IN_DIV": "MECHANICAL",
    "UNCLOSED_P_TAG": "MECHANICAL",
    "UNESCAPED_AMPERSAND_TITLE": "MECHANICAL",
    "UNEXPLAINED_IMPORT": "AUTHORING",
    "UNUSED_VENDOR": "MECHANICAL",
    "VAGUE_HEADING": "AUTHORING",
    "VENDOR_PATH_PREFIX": "MECHANICAL",
    "WRONG_TH_SCOPE": "MECHANICAL",
    "DECORATIVE_CODE": "AUTHORING",
    "DECISION_FRAMEWORK_EARLY": "AUTHORING",
    "CODE_FRAG_NUM": "PER-FILE",
    "CALLOUT_TYPE_MISMATCH": "MECHANICAL",
    "CHAPTER_STARTER": "AUTHORING",
    "CALLOUT_NON_CANONICAL": "MECHANICAL",
    "CALLOUT_TITLE_PREFIX": "MECHANICAL",
    "CHAPTER_NAV_INCOMPLETE": "MECHANICAL",
    "BIG_PICTURE_EXCESS_BOLD": "MECHANICAL",
    "OFFTOPIC_NO_LLM_CONTEXT": "AUTHORING",
    "WHATS_NEXT_NO_LINK": "MECHANICAL",
    "IMAGE_OPPORTUNITY": "AUTHORING",
    "STRUCTURAL_VIOLATION": "MECHANICAL",
}


def run_audit():
    """Run the plugin audit and return the JSON."""
    runner = ROOT / "scripts" / "run_book_audit.py"
    result = subprocess.run(
        [sys.executable, str(runner), "--json"],
        capture_output=True,
        text=True,
        timeout=600,
    )
    stdout = result.stdout
    # Skip leading WARNING lines until first '{'
    start = stdout.find("{")
    if start < 0:
        raise RuntimeError(f"Audit output had no JSON: {stdout[:500]}")
    return json.loads(stdout[start:])


def next_cycle_num():
    existing = sorted(SNAPSHOTS_DIR.glob("cycle_*.json"))
    if not existing:
        return 1
    nums = []
    for p in existing:
        try:
            nums.append(int(p.stem.split("_")[1]))
        except ValueError:
            pass
    return max(nums) + 1 if nums else 1


def summarize(data, label):
    by_pri = Counter(i["priority"] for i in data["issues"])
    by_check = Counter(i["check_id"] for i in data["issues"])
    print(f"\n{label}: {data['issue_count']} issues across {data['file_count']} files")
    print(f"  By priority: P0={by_pri.get('P0',0)} P1={by_pri.get('P1',0)} P2={by_pri.get('P2',0)} P3={by_pri.get('P3',0)}")
    print(f"  Top 15 check IDs:")
    for cid, n in by_check.most_common(15):
        tag = REMEDIATION_TYPE.get(cid, "?")
        pri = next(i["priority"] for i in data["issues"] if i["check_id"] == cid)
        print(f"    {pri}  {cid:<32} {n:5}  [{tag}]")


def diff_against(prev, curr):
    prev_by = Counter(i["check_id"] for i in prev["issues"])
    curr_by = Counter(i["check_id"] for i in curr["issues"])
    all_keys = set(prev_by) | set(curr_by)
    deltas = []
    for k in all_keys:
        delta = curr_by[k] - prev_by[k]
        if delta != 0:
            deltas.append((delta, k))
    deltas.sort()
    print("\nDeltas vs previous snapshot:")
    if not deltas:
        print("  (no change)")
    for delta, k in deltas[:20]:
        sign = "+" if delta > 0 else ""
        print(f"  {sign}{delta:4}  {k}")


def propose_next_fixes(curr):
    """Group remaining issues by remediation type."""
    by_type = Counter()
    for i in curr["issues"]:
        t = REMEDIATION_TYPE.get(i["check_id"], "?")
        by_type[t] += 1
    print("\nBy remediation type:")
    for t, n in by_type.most_common():
        print(f"  {n:5}  {t}")

    # Suggest top mechanical sweep candidates (>=10 issues per check)
    print("\nNext fix candidates (>= 10 issues, MECHANICAL only):")
    by_check = Counter(i["check_id"] for i in curr["issues"])
    for cid, n in by_check.most_common():
        if n < 10:
            break
        t = REMEDIATION_TYPE.get(cid, "?")
        if t == "MECHANICAL":
            print(f"  {n:5}  {cid}  -> write sweep")


def main():
    print(f"=== Audit cycle {next_cycle_num()} ===")
    start = time.time()
    data = run_audit()
    elapsed = time.time() - start
    print(f"Audit took {elapsed:.1f}s")

    cycle = next_cycle_num()
    out = SNAPSHOTS_DIR / f"cycle_{cycle:02d}.json"
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")

    summarize(data, f"Cycle {cycle}")

    # Diff against previous
    prev_path = SNAPSHOTS_DIR / f"cycle_{cycle-1:02d}.json"
    if prev_path.exists():
        prev = json.loads(prev_path.read_text(encoding="utf-8"))
        diff_against(prev, data)

    propose_next_fixes(data)

    print(f"\nSnapshot saved: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
