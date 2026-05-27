"""
Aggregate the 8 gap-audit JSON files (A..H) into a single compact summary.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
families = ["A", "B", "C", "D", "E", "F", "G", "H"]

print("# Gap Audit — Consolidated Summary\n")
totals_all = {"total_items": 0, "present": 0, "partial": 0, "missing": 0}
must_add_all = []

for fam in families:
    p = ROOT / f"_gap_audit_{fam}.json"
    if not p.exists():
        print(f"## Family {fam}: MISSING\n")
        continue
    data = json.loads(p.read_text(encoding="utf-8"))
    s = data.get("summary", {})
    chapters = data.get("chapters", [])
    print(f"## Family {fam} (chapters {', '.join(map(str, chapters))})")
    print(f"- Items: {s.get('total_items')} | Present: {s.get('present')} | Partial: {s.get('partial')} | Missing: {s.get('missing')}")
    for k in totals_all:
        totals_all[k] += s.get(k, 0)
    top = data.get("top_5_must_add") or data.get("top_10_must_add") or []
    if top:
        print("- Top must-add items:")
        for i, item in enumerate(top, 1):
            print(f"  {i}. {item}")
    # Also list ALL missing items (concise)
    missing_items = [it for it in data.get("items", []) if it.get("status") == "missing"]
    if missing_items:
        print(f"- ALL missing items ({len(missing_items)}):")
        for it in missing_items:
            target = it.get("best_target_section", "?")
            src = it.get("slide_deck", "?")
            typ = it.get("item_type", "?")
            desc = it.get("item", "?")
            notes = it.get("notes", "")
            print(f"  * [{target}] ({typ}, slide {src}) {desc}")
            if notes:
                print(f"    -> {notes[:200]}")
    print()

print(f"\n## OVERALL\n")
print(f"- Total items: {totals_all['total_items']}")
print(f"- Present: {totals_all['present']} ({100*totals_all['present']/max(1,totals_all['total_items']):.1f}%)")
print(f"- Partial: {totals_all['partial']} ({100*totals_all['partial']/max(1,totals_all['total_items']):.1f}%)")
print(f"- Missing: {totals_all['missing']} ({100*totals_all['missing']/max(1,totals_all['total_items']):.1f}%)")
