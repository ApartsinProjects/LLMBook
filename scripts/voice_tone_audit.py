#!/usr/bin/env python
"""Voice and tone consistency audit for LLMBook.

Read-only scan. Produces voice-tone-audit.md.
"""
import os
import re
import sys
import html
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
OUT = ROOT / "voice-tone-audit.md"

EXCLUDE_DIRS = {
    "node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
    "source_fix_backups", "pagefind", "templates", ".claude", ".book-update",
    "vendor", "tmp_whats_next", "agents", "_concept-figs", "downloads",
    "images", "styles", "scripts",
}

# Banned hype words (case-insensitive). Pattern -> display.
HYPE_PATTERNS = [
    (r"\brevolutionary\b", "revolutionary"),
    (r"\bgroundbreaking\b", "groundbreaking"),
    (r"\bdefinitive\b", "definitive"),
    (r"\bmust[- ]read\b", "must-read"),
    (r"\bworld[- ]class\b", "world-class"),
    (r"\bcutting[- ]edge\b", "cutting-edge"),
    (r"\bparadigm shift\b", "paradigm shift"),
    (r"\bgame[- ]changer\b", "game-changer"),
    (r"\bbleeding[- ]edge\b", "bleeding-edge"),
]
# 'essential' and 'state-of-the-art' handled contextually below.

HEDGING_WORDS = ["might", "may", "could", "arguably", "it seems", "perhaps", "possibly"]

# Code-fence / element heuristics: strip <pre>...</pre>, <code>...</code>,
# <script>, <style>, HTML comments, math blocks.
RE_PRE = re.compile(r"<pre\b[^>]*>.*?</pre>", re.IGNORECASE | re.DOTALL)
RE_CODE = re.compile(r"<code\b[^>]*>.*?</code>", re.IGNORECASE | re.DOTALL)
RE_SCRIPT = re.compile(r"<script\b[^>]*>.*?</script>", re.IGNORECASE | re.DOTALL)
RE_STYLE = re.compile(r"<style\b[^>]*>.*?</style>", re.IGNORECASE | re.DOTALL)
RE_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
RE_KATEX = re.compile(r"\$\$.*?\$\$|\\\(.*?\\\)|\\\[.*?\\\]", re.DOTALL)
RE_TAG = re.compile(r"<[^>]+>")


def strip_code_and_tags(content):
    """Remove code blocks and HTML tags; return prose text."""
    c = RE_COMMENT.sub(" ", content)
    c = RE_SCRIPT.sub(" ", c)
    c = RE_STYLE.sub(" ", c)
    c = RE_PRE.sub(" ", c)
    c = RE_CODE.sub(" ", c)
    c = RE_KATEX.sub(" ", c)
    c = RE_TAG.sub(" ", c)
    c = html.unescape(c)
    return c


def keep_code_only(content):
    """Return only what is inside <pre> / <code> / <script> blocks (used to
    check if a match was inside code)."""
    blocks = []
    for m in RE_PRE.finditer(content):
        blocks.append(m.group(0))
    for m in RE_CODE.finditer(content):
        blocks.append(m.group(0))
    for m in RE_SCRIPT.finditer(content):
        blocks.append(m.group(0))
    return "\n".join(blocks)


def walk_html_files():
    """Yield absolute paths to HTML files outside excluded dirs."""
    for root, dirs, files in os.walk(ROOT):
        # Filter out excluded directory names in-place
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if f.endswith(".html"):
                yield Path(root) / f


def is_chapter_index(path):
    name = path.name.lower()
    if name == "index.html":
        return True
    return False


def line_of(content, idx):
    """Return 1-based line number of byte index idx in content."""
    return content.count("\n", 0, idx) + 1


def is_inside_block(content, idx, block_regex):
    for m in block_regex.finditer(content):
        if m.start() <= idx < m.end():
            return True
    return False


def is_inside_code(content, idx):
    return (
        is_inside_block(content, idx, RE_PRE)
        or is_inside_block(content, idx, RE_CODE)
        or is_inside_block(content, idx, RE_SCRIPT)
        or is_inside_block(content, idx, RE_STYLE)
        or is_inside_block(content, idx, RE_COMMENT)
    )


def count_words(text):
    return len(re.findall(r"\b[a-zA-Z][a-zA-Z'\-]*\b", text))


def analyze_file(path):
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return None
    prose = strip_code_and_tags(content)
    word_count = count_words(prose)

    rec = {
        "path": path,
        "rel": str(path.relative_to(ROOT)).replace("\\", "/"),
        "word_count": word_count,
        "is_index": is_chapter_index(path),
        "em_dash_hits": [],  # list of (line, snippet)
        "double_dash_hits": [],
        "hype_hits": Counter(),  # word -> count
        "hype_examples": defaultdict(list),  # word -> [snippets]
        "pronoun_you": 0,
        "pronoun_we": 0,
        "pronoun_reader": 0,
        "hedge_counts": Counter(),
        "hedge_total": 0,
        "oxford_yes": 0,  # `, and X` (Oxford)
        "oxford_no": 0,  # `X and Y` after two-item enumeration without comma
        "past_tense_hits": [],  # for index pages
        "essential_marketing": 0,
        "sota_adj": 0,
    }

    # 1. Em-dashes (literal char). Search in raw content but exclude inside code
    # blocks and HTML comments. Inside attribute? Treat as flagged because rare.
    for m in re.finditer("—", content):
        if is_inside_code(content, m.start()):
            continue
        # exclude inside HTML tags themselves
        # Find nearest preceding < and >. If < is closer than >, we're in a tag.
        lt = content.rfind("<", 0, m.start())
        gt = content.rfind(">", 0, m.start())
        if lt > gt:
            continue
        line = line_of(content, m.start())
        # capture 60-char window
        start = max(0, m.start() - 40)
        end = min(len(content), m.end() + 40)
        snippet = content[start:end].replace("\n", " ").strip()
        rec["em_dash_hits"].append((line, snippet))

    # 2. Double-dash drift `--` in prose. Skip inside code/tags. Skip
    # numeric/CSS contexts. Require word boundaries on each side OR space.
    for m in re.finditer(r"(?<!-)--(?!-)", content):
        if is_inside_code(content, m.start()):
            continue
        lt = content.rfind("<", 0, m.start())
        gt = content.rfind(">", 0, m.start())
        if lt > gt:
            continue  # inside a tag
        # Skip if surrounded by non-prose chars like CSS, command-line flags.
        before = content[max(0, m.start() - 1):m.start()]
        after = content[m.end():m.end() + 1]
        # CLI flag pattern: `--word` (no leading space-word-space) or trailing
        # letter -> likely a CLI flag. Skip those.
        if after and after.isalpha():
            continue
        # Require space-bordered or punctuation-bordered context.
        if not (before in (" ", "\xa0", ")", "]", "\"", "'", ",", ".", ";", ":", "?", "!", "}", ">") or before == ""):
            continue
        line = line_of(content, m.start())
        start = max(0, m.start() - 40)
        end = min(len(content), m.end() + 40)
        snippet = content[start:end].replace("\n", " ").strip()
        rec["double_dash_hits"].append((line, snippet))

    # 3. Hype words (case-insensitive) in prose only.
    for pat, label in HYPE_PATTERNS:
        for m in re.finditer(pat, prose, re.IGNORECASE):
            rec["hype_hits"][label] += 1
            if len(rec["hype_examples"][label]) < 2:
                start = max(0, m.start() - 30)
                end = min(len(prose), m.end() + 30)
                rec["hype_examples"][label].append(prose[start:end].strip())

    # essential (marketing sense) — exclude technical uses like "essential
    # property", "essential singularity". Flag occurrences of "essential
    # reading", "essential guide", "essential tool", "essential resource",
    # "essential book", "essential skills".
    for m in re.finditer(
        r"\bessential\s+(reading|guide|tool|resource|book|skills?|knowledge|reference)\b",
        prose,
        re.IGNORECASE,
    ):
        rec["essential_marketing"] += 1
        rec["hype_hits"]["essential (marketing)"] += 1
        if len(rec["hype_examples"]["essential (marketing)"]) < 2:
            start = max(0, m.start() - 30)
            end = min(len(prose), m.end() + 30)
            rec["hype_examples"]["essential (marketing)"].append(prose[start:end].strip())

    # state-of-the-art as adjective: pattern `state-of-the-art <noun>`. Flag
    # if followed by a word that looks like a noun (rough heuristic: any
    # subsequent word).
    for m in re.finditer(r"\bstate[- ]of[- ]the[- ]art\b\s+\w+", prose, re.IGNORECASE):
        rec["sota_adj"] += 1
        rec["hype_hits"]["state-of-the-art (adj)"] += 1
        if len(rec["hype_examples"]["state-of-the-art (adj)"]) < 2:
            start = max(0, m.start() - 30)
            end = min(len(prose), m.end() + 30)
            rec["hype_examples"]["state-of-the-art (adj)"].append(prose[start:end].strip())

    # 4. Pronoun consistency.
    rec["pronoun_you"] = len(re.findall(r"\byou\b", prose, re.IGNORECASE))
    rec["pronoun_we"] = len(re.findall(r"\bwe\b", prose, re.IGNORECASE))
    rec["pronoun_reader"] = len(
        re.findall(r"\bthe reader(s)?\b|\breaders\b", prose, re.IGNORECASE)
    )

    # 5. Hedging.
    for hw in HEDGING_WORDS:
        # multi-word phrases need exact (case-insensitive)
        if " " in hw:
            cnt = len(re.findall(rf"\b{re.escape(hw)}\b", prose, re.IGNORECASE))
        else:
            cnt = len(re.findall(rf"\b{hw}\b", prose, re.IGNORECASE))
        rec["hedge_counts"][hw] = cnt
        rec["hedge_total"] += cnt

    # 6. Oxford comma. Pattern: `A, B, and C` (Oxford) vs `A, B and C` (no
    # Oxford). Require at least one preceding comma in same sentence-chunk.
    # Oxford: comma directly before " and " preceded by another word and a
    # comma earlier in the run.
    # Quick heuristic: regex `, \w+,? and \w+` vs `\w+, \w+ and \w+`.
    rec["oxford_yes"] = len(re.findall(r",\s+\w[\w\-]*,\s+(?:and|or)\s+\w", prose))
    rec["oxford_no"] = len(re.findall(r"\w,\s+\w[\w\-]*\s+(?:and|or)\s+\w[\w\-]*\b(?!\s*,)", prose))

    # 7. Past tense in chapter index pages. Look for "Chapter X covered",
    # "Chapter X discussed", "we covered", "we discussed", "this chapter
    # explored", etc.
    if rec["is_index"]:
        past_patterns = [
            r"Chapter \d+\s+covered\b",
            r"Chapter \d+\s+discussed\b",
            r"Chapter \d+\s+explored\b",
            r"Chapter \d+\s+presented\b",
            r"Chapter \d+\s+introduced\b",
            r"This chapter (covered|discussed|explored|presented|introduced)\b",
            r"\bwe (covered|discussed|explored|presented|introduced)\b",
            r"\b(was|were) (covered|discussed|explored|presented|introduced)\b",
        ]
        for pat in past_patterns:
            for m in re.finditer(pat, prose, re.IGNORECASE):
                rec["past_tense_hits"].append(prose[m.start():m.end()])

    return rec


def main():
    records = []
    files = sorted(walk_html_files())
    print(f"[info] scanning {len(files)} files", file=sys.stderr)
    for p in files:
        rec = analyze_file(p)
        if rec is not None:
            records.append(rec)

    # Aggregate
    total_em = sum(len(r["em_dash_hits"]) for r in records)
    total_dd = sum(len(r["double_dash_hits"]) for r in records)
    total_hype = sum(sum(r["hype_hits"].values()) for r in records)

    # Hedging averages per chapter index. We compute per-file rate
    # hedges/1000-words, then take median/mean across files with > 500 words.
    rates = []
    for r in records:
        if r["word_count"] >= 500:
            rates.append((r["hedge_total"] / r["word_count"]) * 1000)
    avg_rate = sum(rates) / len(rates) if rates else 0.0

    # Over-hedged: rate > 1.5x avg, with at least 2k words.
    over_hedged = []
    over_confident = []
    for r in records:
        if r["word_count"] >= 2000:
            rate = (r["hedge_total"] / r["word_count"]) * 1000
            if rate > 1.5 * avg_rate and r["hedge_total"] >= 5:
                over_hedged.append((rate, r))
            if r["hedge_total"] == 0:
                over_confident.append(r)

    # Pronoun drift: file has all three (you, we, reader) with substantial
    # counts in the same file. Threshold: each >= 5 OR mix where smaller is
    # >=20% of largest.
    pronoun_drift = []
    for r in records:
        y, w, rd = r["pronoun_you"], r["pronoun_we"], r["pronoun_reader"]
        if r["word_count"] < 1000:
            continue
        forms = [("you", y), ("we", w), ("reader", rd)]
        active = [(n, c) for n, c in forms if c >= 5]
        if len(active) >= 2 and rd >= 3:
            # All three or two of three including reader.
            if y >= 5 and w >= 5 and rd >= 3:
                pronoun_drift.append((y + w + rd, r))

    # Oxford inconsistency: file has both non-trivial yes and no counts.
    oxford_inconsistent = []
    for r in records:
        if r["oxford_yes"] >= 3 and r["oxford_no"] >= 3:
            ratio = min(r["oxford_yes"], r["oxford_no"]) / max(r["oxford_yes"], r["oxford_no"])
            if ratio >= 0.3:
                oxford_inconsistent.append((ratio, r))

    # Files with past tense in chapter index.
    past_index = [r for r in records if r["is_index"] and r["past_tense_hits"]]

    # Top offenders: weighted sum.
    def score(r):
        return (
            10 * len(r["em_dash_hits"])
            + 8 * len(r["double_dash_hits"])
            + 4 * sum(r["hype_hits"].values())
            + 2 * len(r["past_tense_hits"])
            + (1 if (r["pronoun_you"] >= 5 and r["pronoun_we"] >= 5 and r["pronoun_reader"] >= 3) else 0) * 5
        )
    ranked = sorted(records, key=score, reverse=True)
    top_offenders = [r for r in ranked if score(r) > 0][:30]

    # Build markdown report
    lines = []
    lines.append("# Voice & Tone Consistency Audit")
    lines.append("")
    lines.append(f"Scan root: `{ROOT}`")
    lines.append(f"Excluded dirs: {', '.join(sorted(EXCLUDE_DIRS))}")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- Files scanned: {len(records)}")
    lines.append(f"- Em-dash hits in prose: {total_em} (P0 - user banned)")
    lines.append(f"- Double-dash drift hits in prose: {total_dd} (P0)")
    lines.append(f"- Banned hype-word hits: {total_hype} (P1)")
    lines.append(f"- Files with severe pronoun drift (you+we+reader, each substantial): {len(pronoun_drift)} (P2)")
    lines.append(f"- Files with Oxford-comma inconsistency: {len(oxford_inconsistent)} (P2)")
    lines.append(f"- Chapter-index pages with past-tense drift: {len(past_index)} (P2)")
    lines.append(f"- Book-wide hedging rate: {avg_rate:.2f} hedges per 1000 words")
    lines.append(f"- Over-hedged chapters (>1.5x avg, >=2k words): {len(over_hedged)}")
    lines.append(f"- Over-confident sections (0 hedging, >=2k words): {len(over_confident)}")
    lines.append("")

    # P0 - em-dash
    lines.append("## P0: Em-dash hits in prose (user-banned character)")
    lines.append("")
    if total_em == 0:
        lines.append("_No em-dash characters detected in prose. Pass._")
    else:
        # Sort files by count desc.
        em_files = sorted(
            [r for r in records if r["em_dash_hits"]],
            key=lambda r: -len(r["em_dash_hits"]),
        )
        for r in em_files[:60]:
            lines.append(f"- `{r['rel']}` ({len(r['em_dash_hits'])}x)")
            for line, snip in r["em_dash_hits"][:3]:
                # Trim snippet to ~90 chars.
                if len(snip) > 90:
                    snip = snip[:87] + "..."
                lines.append(f"  - L{line}: `{snip}`")
            if len(r["em_dash_hits"]) > 3:
                lines.append(f"  - ...{len(r['em_dash_hits']) - 3} more")
        if len(em_files) > 60:
            lines.append(f"- ...{len(em_files) - 60} more files with em-dashes")
    lines.append("")

    # P0 - double-dash
    lines.append("## P0: Double-dash drift `--` in prose")
    lines.append("")
    if total_dd == 0:
        lines.append("_No double-dash drift detected in prose. Pass._")
    else:
        dd_files = sorted(
            [r for r in records if r["double_dash_hits"]],
            key=lambda r: -len(r["double_dash_hits"]),
        )
        for r in dd_files[:40]:
            lines.append(f"- `{r['rel']}` ({len(r['double_dash_hits'])}x)")
            for line, snip in r["double_dash_hits"][:2]:
                if len(snip) > 90:
                    snip = snip[:87] + "..."
                lines.append(f"  - L{line}: `{snip}`")
            if len(r["double_dash_hits"]) > 2:
                lines.append(f"  - ...{len(r['double_dash_hits']) - 2} more")
        if len(dd_files) > 40:
            lines.append(f"- ...{len(dd_files) - 40} more files with `--` drift")
    lines.append("")

    # P1 - Hype words
    lines.append("## P1: Banned hype words")
    lines.append("")
    hype_totals = Counter()
    for r in records:
        for w, c in r["hype_hits"].items():
            hype_totals[w] += c
    if not hype_totals:
        lines.append("_No banned hype words detected. Pass._")
    else:
        lines.append("**Book-wide totals:**")
        for w, c in hype_totals.most_common():
            lines.append(f"- `{w}`: {c}")
        lines.append("")
        lines.append("**Top files by hype-word count:**")
        hype_files = sorted(
            [r for r in records if sum(r["hype_hits"].values()) > 0],
            key=lambda r: -sum(r["hype_hits"].values()),
        )
        for r in hype_files[:40]:
            tot = sum(r["hype_hits"].values())
            parts = ", ".join(f"{w}={c}" for w, c in r["hype_hits"].most_common())
            lines.append(f"- `{r['rel']}` (total {tot}): {parts}")
            # one example per top word
            for w in list(r["hype_hits"].keys())[:2]:
                if r["hype_examples"][w]:
                    ex = r["hype_examples"][w][0]
                    if len(ex) > 90:
                        ex = ex[:87] + "..."
                    lines.append(f"  - `{w}`: ...{ex}...")
        if len(hype_files) > 40:
            lines.append(f"- ...{len(hype_files) - 40} more files with hype words")
    lines.append("")

    # P2 - Pronoun drift
    lines.append("## P2: Pronoun consistency (you / we / reader)")
    lines.append("")
    if not pronoun_drift:
        lines.append("_No files mix all three pronoun forms heavily._")
    else:
        lines.append("Files using `you`, `we`, and `the reader`/`readers` heavily in the same file:")
        for _, r in sorted(pronoun_drift, key=lambda x: -x[0])[:30]:
            lines.append(
                f"- `{r['rel']}` -- `you`({r['pronoun_you']}x) + `we`({r['pronoun_we']}x) + `reader(s)`({r['pronoun_reader']}x)"
            )
    lines.append("")

    # P2 - Tense drift in chapter indexes
    lines.append("## P2: Tense drift in chapter-index pages (should be present tense)")
    lines.append("")
    if not past_index:
        lines.append("_No past-tense drift detected in index pages._")
    else:
        for r in sorted(past_index, key=lambda r: -len(r["past_tense_hits"]))[:40]:
            lines.append(f"- `{r['rel']}` ({len(r['past_tense_hits'])} past-tense hits)")
            for ex in r["past_tense_hits"][:2]:
                lines.append(f"  - `{ex}`")
    lines.append("")

    # P2 - Oxford comma inconsistency
    lines.append("## P2: Oxford-comma inconsistency within file")
    lines.append("")
    if not oxford_inconsistent:
        lines.append("_No flagged Oxford-comma inconsistency._")
    else:
        for _, r in sorted(oxford_inconsistent, key=lambda x: -x[0])[:30]:
            lines.append(
                f"- `{r['rel']}` -- Oxford: {r['oxford_yes']}x, non-Oxford: {r['oxford_no']}x"
            )
    lines.append("")

    # Over-hedged / over-confident
    lines.append("## P2: Hedging variance")
    lines.append("")
    lines.append(f"Book-wide hedging rate (files >=500 words): {avg_rate:.2f} hedges per 1000 words.")
    lines.append("")
    lines.append("**Over-hedged chapters (rate > 1.5x book average, >=2k words):**")
    if not over_hedged:
        lines.append("- _none_")
    else:
        for rate, r in sorted(over_hedged, key=lambda x: -x[0])[:30]:
            top_hedges = ", ".join(f"{h}={c}" for h, c in r["hedge_counts"].most_common(3) if c)
            lines.append(
                f"- `{r['rel']}` -- {rate:.2f}/1k ({r['hedge_total']} hedges in {r['word_count']} words). Top: {top_hedges}"
            )
    lines.append("")
    lines.append("**Over-confident sections (0 hedging words in >=2k words):**")
    if not over_confident:
        lines.append("- _none_")
    else:
        for r in sorted(over_confident, key=lambda r: -r["word_count"])[:30]:
            lines.append(f"- `{r['rel']}` -- {r['word_count']} words, 0 hedges")
    lines.append("")

    # Top recurring offenders
    lines.append("## Top recurring offenders (weighted score)")
    lines.append("")
    if not top_offenders:
        lines.append("- _none_")
    else:
        for r in top_offenders:
            issues = []
            if r["em_dash_hits"]:
                issues.append(f"em-dash={len(r['em_dash_hits'])}")
            if r["double_dash_hits"]:
                issues.append(f"--={len(r['double_dash_hits'])}")
            hype_tot = sum(r["hype_hits"].values())
            if hype_tot:
                issues.append(f"hype={hype_tot}")
            if r["past_tense_hits"]:
                issues.append(f"past-tense={len(r['past_tense_hits'])}")
            if r["pronoun_you"] >= 5 and r["pronoun_we"] >= 5 and r["pronoun_reader"] >= 3:
                issues.append("pronoun-drift")
            lines.append(f"- `{r['rel']}` -- {score(r)} pts ({', '.join(issues)})")
    lines.append("")

    # Recommended deterministic fixes
    lines.append("## Recommended deterministic fixes (scriptable)")
    lines.append("")
    if total_em > 0:
        lines.append(f"- Replace `—` -> `, ` book-wide ({total_em} occurrences in prose). Manual review: some may want `;`, `:`, or parens depending on context.")
    if total_dd > 0:
        lines.append(f"- Replace ` -- ` -> `, ` book-wide ({total_dd} occurrences in prose, excluding code/CLI flags).")
    for w, c in hype_totals.most_common():
        lines.append(f"- Audit `{w}` ({c} occurrences) - consider a non-hype substitute or removal.")
    if past_index:
        lines.append(f"- Rewrite past tense in chapter-index pages to present tense in {len(past_index)} files.")
    if oxford_inconsistent:
        lines.append(f"- Pick a single Oxford-comma policy per file in {len(oxford_inconsistent)} files; the dominant style book-wide is detectable per-section.")
    if pronoun_drift:
        lines.append(f"- Normalize pronouns in {len(pronoun_drift)} files; pick one of `you` (instructional) or `we` (collaborative) per section.")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    # Cap at 500 lines.
    text = OUT.read_text(encoding="utf-8")
    line_list = text.splitlines()
    if len(line_list) > 500:
        line_list = line_list[:497] + [
            "",
            f"_...truncated to 500 lines. Full counts retained in summary._",
        ]
        OUT.write_text("\n".join(line_list), encoding="utf-8")
    print(f"[info] wrote {OUT}", file=sys.stderr)
    print(f"[info] {len(records)} files scanned", file=sys.stderr)
    print(f"[info] em-dash total: {total_em}", file=sys.stderr)
    print(f"[info] double-dash total: {total_dd}", file=sys.stderr)
    print(f"[info] hype total: {total_hype}", file=sys.stderr)


if __name__ == "__main__":
    main()
