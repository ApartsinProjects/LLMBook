"""Auto-fix redundant figures flagged with AUTO-FIX by the audit script.

Reads `docs/content-audit/REDUNDANT_FIGURES.json` and for every pair tagged
`autofix_candidate: true`, removes the DROP figure's `<figure>` or
`<div class="diagram-container">` block (with its caption), updates any
prose references to the dropped figure to point at the kept figure, and
renumbers subsequent figures in the same section to preserve monotonic
numbering when the dropped figure was not the last one.

Stdlib only. Idempotent: runs successfully even if a target figure was
already removed in a previous run.

Usage:
    /c/Python314/python scripts/fix_redundant_figures.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "docs" / "content-audit" / "REDUNDANT_FIGURES.json"

# Caption patterns (must match what the detector recognizes)
FIGCAPTION_LABEL_RE = re.compile(
    r'<figcaption[^>]*>\s*<strong>\s*Figure\s+'
    r'(?P<num>\d+\.\d+\.\d+)\s*</strong>',
    re.IGNORECASE,
)
DIAGRAM_CAPTION_LABEL_RE = re.compile(
    r'<div\s+class="diagram-caption"[^>]*>\s*<strong>\s*Figure\s+'
    r'(?P<num>\d+\.\d+\.\d+)\s*</strong>',
    re.IGNORECASE,
)
FIGURE_CAPTION_DIV_LABEL_RE = re.compile(
    r'<div\s+class="figure-caption"[^>]*>\s*<strong>\s*Figure\s+'
    r'(?P<num>\d+\.\d+\.\d+)\s*</strong>',
    re.IGNORECASE,
)

# Prose reference patterns (match "Figure X.Y.Z" anywhere in body text)
PROSE_REF_RE = re.compile(
    r'(?<![\w.])Figure\s+(?P<num>\d+\.\d+\.\d+)(?!\d)',
    re.IGNORECASE,
)


def find_block_spans(html: str) -> list[dict]:
    """Find every figure-containing block in the file, in document order.

    Returns list of dicts with: label, container_kind, block_start,
    block_end (offsets into html).
    """
    blocks: list[dict] = []

    # <figure>...</figure> with a figcaption that has Figure X.Y.Z
    fig_re = re.compile(r"<figure\b[^>]*>", re.IGNORECASE)
    for fm in fig_re.finditer(html):
        # Find matching </figure>
        depth = 1
        i = fm.end()
        # Linear scan: walk forward, track nested <figure>
        while i < len(html):
            m = re.search(
                r"<(/?)figure\b[^>]*>", html[i:], re.IGNORECASE
            )
            if not m:
                break
            absolute = i + m.start()
            if m.group(1) == "/":
                depth -= 1
                if depth == 0:
                    inner = html[fm.start():absolute + m.end() - m.start()]
                    label_m = FIGCAPTION_LABEL_RE.search(inner)
                    if label_m:
                        blocks.append({
                            "label": f"Figure {label_m.group('num')}",
                            "num": label_m.group("num"),
                            "container_kind": "figure",
                            "block_start": fm.start(),
                            "block_end": absolute + m.end() - m.start(),
                        })
                    i = absolute + m.end() - m.start()
                    break
            else:
                depth += 1
            i = absolute + m.end() - m.start()

    # <div class="diagram-container">...closing </div></div>
    # Match minimum-greedy: outer div ends when nesting balances
    dc_re = re.compile(
        r'<div\s+class="diagram-container"[^>]*>', re.IGNORECASE
    )
    for fm in dc_re.finditer(html):
        # Walk forward tracking <div> depth
        depth = 1
        i = fm.end()
        while i < len(html):
            m = re.search(r"<(/?)div\b[^>]*>", html[i:], re.IGNORECASE)
            if not m:
                break
            absolute = i + m.start()
            if m.group(1) == "/":
                depth -= 1
                if depth == 0:
                    inner = html[fm.start():absolute + m.end() - m.start()]
                    label_m = DIAGRAM_CAPTION_LABEL_RE.search(inner)
                    if label_m:
                        blocks.append({
                            "label": f"Figure {label_m.group('num')}",
                            "num": label_m.group("num"),
                            "container_kind": "diagram-container",
                            "block_start": fm.start(),
                            "block_end": absolute + m.end() - m.start(),
                        })
                    i = absolute + m.end() - m.start()
                    break
            else:
                depth += 1
            i = absolute + m.end() - m.start()

    # Sort blocks by start position, dedupe by start
    blocks.sort(key=lambda b: b["block_start"])
    # Remove overlapping (defensive: prefer the outer one)
    deduped: list[dict] = []
    for b in blocks:
        if any(
            d["block_start"] <= b["block_start"]
            < d["block_end"] for d in deduped
        ):
            continue
        deduped.append(b)
    return deduped


def trim_surrounding_blank_lines(text: str, start: int, end: int) -> tuple[int, int]:
    """Expand (start, end) to swallow a trailing newline (and a leading
    blank line if present)."""
    # Trailing newline
    if end < len(text) and text[end] == "\n":
        end += 1
    # If now we leave two adjacent blank lines, drop one
    while end < len(text) and text[end] == "\n" and start > 0 and text[start - 1] == "\n":
        end += 1
    return start, end


def apply_autofix(html: str, drop_num: str, keep_num: str) -> tuple[str, dict]:
    """Remove the figure block labelled `drop_num`, redirect prose refs to
    `keep_num`, and renumber subsequent figures so numbering stays
    monotonic.

    Returns (new_html, stats).
    """
    blocks = find_block_spans(html)
    drop_blocks = [b for b in blocks if b["num"] == drop_num]
    if not drop_blocks:
        return html, {"status": "already-removed", "drop_num": drop_num}

    # If multiple blocks share the same number (shouldn't, but defensive),
    # remove ALL of them.
    drop_block = drop_blocks[0]

    # Parse numbers as tuples for comparison
    def parse(n: str) -> tuple[int, int, int]:
        a, b, c = n.split(".")
        return int(a), int(b), int(c)

    drop_t = parse(drop_num)
    keep_t = parse(keep_num)
    # Sanity: same section (same X.Y prefix)
    if drop_t[:2] != keep_t[:2]:
        return html, {
            "status": "different-section-skipped",
            "drop_num": drop_num,
            "keep_num": keep_num,
        }

    # Figures that need renumbering: those with the same (X, Y) prefix
    # and Z > drop_t[2], EXCEPT keep_num itself (its number stays).
    same_section_blocks = [
        b for b in blocks
        if parse(b["num"])[:2] == drop_t[:2]
    ]
    # Build old -> new map. drop_num is removed; anything > drop_num
    # shifts down by 1. keep_num is also subject to this rule.
    renumber: dict[str, str] = {}
    for b in same_section_blocks:
        t = parse(b["num"])
        if t == drop_t:
            continue
        if t[2] > drop_t[2]:
            new_z = t[2] - 1
            new_num = f"{t[0]}.{t[1]}.{new_z}"
            renumber[b["num"]] = new_num
    # If keep_num was renumbered, the prose-redirect target also shifts.
    final_keep_num = renumber.get(keep_num, keep_num)

    # 1) Remove the drop block (with surrounding whitespace cleanup)
    start, end = drop_block["block_start"], drop_block["block_end"]
    start, end = trim_surrounding_blank_lines(html, start, end)
    new_html = html[:start] + html[end:]
    stats: dict = {
        "status": "ok",
        "drop_num": drop_num,
        "keep_num": keep_num,
        "final_keep_num": final_keep_num,
        "renumber_map": renumber,
        "removed_chars": end - start,
    }

    # 2) Redirect prose references to drop_num -> final_keep_num. Do this
    #    BEFORE renumbering so that the renumber pass doesn't accidentally
    #    re-shift the redirected refs.
    redirect_count = 0

    def _redirect(m: re.Match) -> str:
        nonlocal redirect_count
        num = m.group("num")
        if num == drop_num:
            redirect_count += 1
            return f"Figure {final_keep_num}"
        return m.group(0)

    new_html = PROSE_REF_RE.sub(_redirect, new_html)
    stats["prose_refs_redirected"] = redirect_count

    # 3) Renumber subsequent figures. We rebuild captions AND every prose
    #    reference, using the renumber map. We do this with placeholders to
    #    avoid the keep_num <-> drop_num swap problem.
    if renumber:
        # Sort by old number so we don't double-replace
        token_map = {
            old: f"\x00FIG_{i}\x00"
            for i, old in enumerate(renumber.keys())
        }
        # Replace every Figure {old} with the placeholder
        for old, token in token_map.items():
            # Match in captions
            new_html = re.sub(
                r'(<strong>\s*)Figure\s+' + re.escape(old)
                + r'(\s*</strong>)',
                r'\1Figure ' + token + r'\2',
                new_html,
                flags=re.IGNORECASE,
            )
            # Match in prose references (Figure X.Y.Z not followed by digit)
            new_html = re.sub(
                r'(?<![\w.])Figure\s+' + re.escape(old) + r'(?!\d)',
                "Figure " + token,
                new_html,
                flags=re.IGNORECASE,
            )
        # Now swap placeholders for new numbers
        for old, token in token_map.items():
            new_num = renumber[old]
            new_html = new_html.replace(token, new_num)

    return new_html, stats


def main():
    parser = argparse.ArgumentParser(
        description="Apply auto-fixes from REDUNDANT_FIGURES.json"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would change without writing files.",
    )
    parser.add_argument(
        "--report",
        default=str(REPORT_JSON),
        help="Path to REDUNDANT_FIGURES.json",
    )
    args = parser.parse_args()

    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    report_path = Path(args.report)
    if not report_path.exists():
        print(
            f"ERROR: report not found at {report_path}. "
            "Run `audit_redundant_figures.py` first.",
            file=sys.stderr,
        )
        sys.exit(1)

    data = json.loads(report_path.read_text(encoding="utf-8"))
    autofix_pairs = [p for p in data if p.get("autofix_candidate")]
    if not autofix_pairs:
        print("No AUTO-FIX pairs in report. Nothing to do.")
        return

    print(f"Found {len(autofix_pairs)} auto-fix pair(s).")

    # Group by file (each file may have multiple drops). We handle them
    # sequentially in document order; first drop must be largest Z so
    # earlier drops don't invalidate later block offsets.
    by_file: dict[str, list[dict]] = defaultdict(list)
    for p in autofix_pairs:
        by_file[p["file"]].append(p)

    total_files = 0
    total_fixes = 0
    for relfile, pairs in by_file.items():
        path = ROOT.joinpath(*relfile.split("/"))
        if not path.exists():
            print(f"  SKIP {relfile}: not found")
            continue
        original = path.read_text(encoding="utf-8")
        html = original

        # Determine keep/drop for each pair using the SAME heuristic the
        # report exposed (KEEP/DROP captured in the audit). The JSON does
        # not have keep/drop columns yet, so we re-derive from the same
        # heuristic in audit_redundant_figures.suggest_keep_drop.
        for p in pairs:
            p["_keep"], p["_drop"] = _derive_keep_drop(p)

        # Sort drops by figure number descending so we delete from the
        # bottom up; that way each later deletion's block offsets are
        # still valid when we process it.
        def _drop_num_tuple(p: dict) -> tuple[int, int, int]:
            # _drop is "Figure X.Y.Z"
            return tuple(int(x) for x in p["_drop"].split()[-1].split("."))

        pairs.sort(key=_drop_num_tuple, reverse=True)

        file_stats = []
        for p in pairs:
            keep_label = p["_keep"]  # "Figure X.Y.Z"
            drop_label = p["_drop"]
            keep_num = keep_label.split()[-1]
            drop_num = drop_label.split()[-1]
            html, stats = apply_autofix(html, drop_num, keep_num)
            file_stats.append({"pair": p, "stats": stats})
            print(
                f"  {relfile}: DROP {drop_label} (KEEP {keep_label}) -> "
                f"{stats['status']}"
            )
            if stats["status"] == "ok":
                print(
                    f"    removed {stats['removed_chars']} chars, "
                    f"redirected {stats['prose_refs_redirected']} prose ref(s), "
                    f"renumber={stats['renumber_map']}"
                )
                total_fixes += 1

        if html != original:
            if args.dry_run:
                print(f"  [dry-run] would write {relfile} ({len(html)} chars)")
            else:
                path.write_text(html, encoding="utf-8")
                total_files += 1

    print(f"\nFixed {total_fixes} pair(s) across {total_files} file(s).")


def _derive_keep_drop(pair_record: dict) -> tuple[str, str]:
    """Replicate the audit's KEEP/DROP heuristic so we don't have to
    pass extra columns through the JSON report.

    Uses the substantive caption-token sets to score "specificity",
    falling back to keep-first on ties.
    """
    # Defensive: caption_shared_words may include the shared overlap
    shared = set(pair_record.get("caption_shared_words", []))

    def sub_tokens(text: str) -> list[str]:
        STOPWORDS = _STOPWORDS_CACHED
        lower = text.lower()
        words = re.findall(r"[a-z]+", lower)
        return [w for w in words if w not in STOPWORDS and len(w) >= 4]

    a_sub = sub_tokens(pair_record["fig_a_caption"])
    b_sub = sub_tokens(pair_record["fig_b_caption"])
    a_unique = [t for t in a_sub if t not in shared]
    b_unique = [t for t in b_sub if t not in shared]
    a_score = len(set(a_unique)) + 0.02 * len(pair_record["fig_a_caption"])
    b_score = len(set(b_unique)) + 0.02 * len(pair_record["fig_b_caption"])
    if a_score >= b_score:
        return pair_record["fig_a_label"], pair_record["fig_b_label"]
    return pair_record["fig_b_label"], pair_record["fig_a_label"]


# Cached stopword set (matches detector exactly)
_STOPWORDS_CACHED = set("""
a about above across after again against all almost alone along already also
although always am among amongst an and another any anybody anyone anything
anywhere are aren around as at back be became because become becomes been
before being below between beyond both but by came can cannot could did do
does doing done down during each either else enough etc even ever every
everybody everyone everything everywhere except few first for found four from
further get gets give given gives go goes got had has have having he her hers
herself him himself his how however i if in into is it its itself just keep
know last least less let like little look made make many may me might more
most much must my myself never new next no nobody non none nor not now of off
often on once one only or other others ought our ours ourselves out over own
per perhaps please put rather really said same say see seem seems seen self
several shall she should since so some somebody someone something somewhere
still such take than that the their theirs them themselves then there these
they thing things this those though three through thus to together too toward
towards two under until up upon us use used uses using very via was way we
well were what whatever when where whether which while who whom whose why
will with within without would yet you your yours yourself yourselves figure
figures shows showing show shown image illustration diagram caption panel
panels box boxes arrow arrows top bottom left right above below visual which
where these those this that them they them their there here was been being
also although still however just only even very while when then while now
this also been been very thing things one ones two three four five six seven
eight nine ten 's
""".split())


if __name__ == "__main__":
    main()
