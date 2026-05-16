"""Validate the migration-map.json for the Part 8 restructure.

Checks:
1. Every 'from' path in section_moves exists on disk.
2. Every 'to' path is unique across all section_moves (no two sources targeting one destination).
3. Every modules_to_delete actually exists.
4. Every module_renames source exists and destination doesn't already exist.
5. modules_to_create destinations don't already exist.
6. anchor_prefix_renames don't chain (no rename whose target is another rename's source).
7. chapter_num_renames don't chain.

Exits 0 on clean validation, 1 with errors otherwise.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MAP = HERE / "migration-map.json"


def main() -> int:
    data = json.loads(MAP.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []

    # 1. section_moves source paths exist
    seen_destinations: dict[str, str] = {}
    for entry in data["section_moves"]:
        src = ROOT / entry["from"]
        if not src.exists():
            errors.append(f"section_moves source missing: {entry['from']}")
        dst = entry["to"]
        is_merge = "merge" in entry.get("action", "")
        if dst in seen_destinations and not is_merge:
            errors.append(
                f"section_moves destination collision: {dst} (sources: "
                f"{seen_destinations[dst]} AND {entry['from']})"
            )
        elif dst in seen_destinations and is_merge:
            # Track merges separately
            warnings.append(
                f"section_moves MERGE planned at {dst}: {seen_destinations[dst]} + {entry['from']}"
            )
        seen_destinations[dst] = entry["from"]

    # 2. sections_from_scratch destinations
    for entry in data["sections_from_scratch"]:
        dst = entry["to"]
        if dst in seen_destinations:
            errors.append(
                f"sections_from_scratch destination collision: {dst} (also a section_move target)"
            )
        seen_destinations[dst] = entry.get("from", "<scratch>")

    # 3. modules_to_delete exist
    for mod in data["modules_to_delete"]:
        p = ROOT / mod
        if not p.exists():
            warnings.append(f"modules_to_delete missing on disk (already deleted?): {mod}")

    # 4. module_renames
    for src, dst in data["module_renames"].items():
        src_p = ROOT / src
        dst_p = ROOT / dst
        if not src_p.exists():
            errors.append(f"module_renames source missing: {src}")
        if dst_p.exists():
            errors.append(f"module_renames destination already exists: {dst}")

    # 5. modules_to_create destinations
    for entry in data["modules_to_create"]:
        dst_p = ROOT / entry["path"]
        if dst_p.exists():
            errors.append(f"modules_to_create path already exists: {entry['path']}")

    # 6. anchor_prefix_renames: no chains (target of one is source of another)
    keys = set(data["anchor_prefix_renames"].keys())
    vals = set(data["anchor_prefix_renames"].values())
    # A value-being-a-key indicates a chain: A->B and B->C
    chain_keys = keys & vals
    if chain_keys:
        warnings.append(
            f"anchor_prefix_renames has values that are also keys (potential chain): {chain_keys}"
        )

    # 7. chapter_num_renames: same chain check
    keys = set(data["chapter_num_renames"].keys()) - {"_note"}
    vals = set(str(v) for v in data["chapter_num_renames"].values() if not str(v).startswith("_"))
    chain_keys = keys & vals
    if chain_keys:
        warnings.append(
            f"chapter_num_renames has chain risk: {chain_keys}. "
            f"Apply renames sorted by destination descending to avoid clobbering."
        )

    # Reporting
    print(f"=== VALIDATION ===")
    print(f"section_moves: {len(data['section_moves'])}")
    print(f"sections_from_scratch: {len(data['sections_from_scratch'])}")
    print(f"module_renames: {len(data['module_renames'])}")
    print(f"modules_to_create: {len(data['modules_to_create'])}")
    print(f"modules_to_delete: {len(data['modules_to_delete'])}")
    print(f"anchor_prefix_renames: {len(data['anchor_prefix_renames'])}")
    print(f"chapter_num_renames: {len(data['chapter_num_renames']) - 1}")  # minus _note
    print()
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  X {e}")
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  ! {w}")
    if not errors and not warnings:
        print("CLEAN. Map is valid.")
        return 0
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
