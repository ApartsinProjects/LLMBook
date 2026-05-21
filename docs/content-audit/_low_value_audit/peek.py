"""Inspect a few code blocks for tuning the classifier."""
import json, sys
from pathlib import Path

JSONL = Path(__file__).parent / "code_blocks_classified.jsonl"

mode = sys.argv[1] if len(sys.argv) > 1 else "summary"

blocks = [json.loads(l) for l in JSONL.open(encoding="utf-8")]

if mode == "summary":
    # Show lang_class breakdown
    from collections import Counter
    c = Counter(b["lang_class"] for b in blocks)
    for lc, n in c.most_common(30):
        print(f"  {n:5d}  {lc!r}")
elif mode == "kept_with_print_ratio":
    # blocks classified as KEEP but with high print_ratio
    kept = [b for b in blocks if b["category"] == "KEEP"]
    kept.sort(key=lambda b: -b["print_ratio"])
    for b in kept[:30]:
        print(f"{b['file']}:{b['line_no']}  pr={b['print_ratio']:.2f} n_lines={b['n_lines']} imports={b['imports']}")
        print("    " + (b["code"][:200].replace("\n", "\n    ")))
        print("---")
elif mode == "kept_short":
    # short blocks that might be toy demos
    kept = [b for b in blocks if b["category"] == "KEEP" and b["n_lines"] <= 6]
    kept.sort(key=lambda b: b["n_lines"])
    for b in kept[:30]:
        print(f"{b['file']}:{b['line_no']}  n_lines={b['n_lines']} imports={b['imports']}")
        print("    " + (b["code"][:300].replace("\n", "\n    ")))
        print("---")
elif mode == "kept_no_lib":
    # KEEP but no real library and no defs — likely toy
    kept = [b for b in blocks if b["category"] == "KEEP" and not b["imports"] and not b["has_def"]]
    for b in kept[:30]:
        print(f"{b['file']}:{b['line_no']}  n_lines={b['n_lines']}")
        print("    " + (b["code"][:300].replace("\n", "\n    ")))
        print("---")
elif mode == "kept_pseudo":
    # KEEP but contains "pseudocode" markers
    import re
    kept = [b for b in blocks if b["category"] == "KEEP"]
    pseudo = []
    for b in kept:
        if re.search(r"\b(pseudocode|pseudo-code|sketch|conceptually)\b", b.get("ctx_before_tail", "") + " " + b.get("ctx_after_head", ""), re.IGNORECASE):
            pseudo.append(b)
    for b in pseudo[:20]:
        print(f"{b['file']}:{b['line_no']}  n_lines={b['n_lines']} imports={b['imports']}")
        print("    " + (b["code"][:300].replace("\n", "\n    ")))
        print("---")
elif mode == "top_drop":
    drops = [b for b in blocks if b["category"] == "DROP"]
    drops.sort(key=lambda b: -b["severity"])
    for b in drops[:30]:
        print(f"sev={b['severity']:.1f}  {b['file']}:{b['line_no']}")
        print(f"  {b['reason']}")
        print("  " + (b["code"][:200].replace("\n", "\n  ")))
        print("---")
elif mode == "dataclass_kept":
    # KEEP blocks that are actually @dataclass with no methods
    kept = [b for b in blocks if b["category"] == "KEEP" and "@dataclass" in b.get("code", "") and not b["has_def"]]
    for b in kept[:30]:
        print(f"{b['file']}:{b['line_no']}  n_lines={b['n_lines']} kv_ratio={b['kv_ratio']:.2f}")
        print("  " + (b["code"][:300].replace("\n", "\n  ")))
        print("---")
elif mode == "many_classes":
    # blocks with multiple class defs
    blks = [b for b in blocks if b["category"] in ("KEEP", "DROP")]
    import re
    for b in blks:
        n_class = len(re.findall(r"^\s*class\s+", b["code"], re.MULTILINE))
        if n_class >= 3:
            print(f"{b['file']}:{b['line_no']} classes={n_class} cat={b['category']}")
            print("  " + (b["code"][:300].replace("\n", "\n  ")))
            print("---")
