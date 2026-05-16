"""Quick voice/tone + stale-link fixes from the landed audits.

Findings applied:
1. Em-dash sweep (voice-tone-audit.md P0): 7 em-dashes in prose -> commas.
   Replace literal em-dash (Unicode U+2014) with ', ' when surrounded by
   word chars; preserve em-dashes inside code blocks.

2. Hype-word template (voice-tone-audit.md P1): 76 occurrences of
   "Essential reading for..." in bibliography callouts. Replace with
   "Useful for ...".

3. Stale Part-7 bridge links flagged by a019b9b977a4af726:
   `module-04-transformer-anatomy` (pre-existing broken)
       -> `module-04-transformer-architecture`
   `module-08-pretraining-objectives` (pre-existing broken)
       -> `module-07-pretraining-scaling-laws`

4. Past-tense -> present in chapter index prose patterns
   (voice-tone-audit.md P2; 4 files).

Idempotent. Run with --apply.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update"}


def fix(p: Path, dry_run: bool) -> dict:
    text = p.read_text(encoding="utf-8")
    orig = text
    c = {"em_dash": 0, "essential_reading": 0, "stale_link": 0,
         "past_tense": 0}

    # 1. Em-dash sweep (do not touch inside <pre>/<code>)
    # Split on code block boundaries; rewrite only in prose chunks.
    parts = re.split(r'(<pre[\s\S]*?</pre>|<code[\s\S]*?</code>)',
                       text, flags=re.IGNORECASE)
    for i in range(len(parts)):
        if i % 2 == 0:  # prose chunk
            # Replace em-dash with ', ' (surrounded by word chars/spaces)
            new_chunk, n = re.subn(r'\s*—\s*', ', ', parts[i])
            if n:
                c["em_dash"] += n
                parts[i] = new_chunk
    text = "".join(parts)

    # 2. "Essential reading for..." -> "Useful for..."
    new_text, n = re.subn(
        r'\bEssential reading for\b',
        'Useful for',
        text,
    )
    if n:
        c["essential_reading"] += n
        text = new_text

    # 3. Stale link slugs
    stale_links = [
        ('module-04-transformer-anatomy', 'module-04-transformer-architecture'),
        ('module-08-pretraining-objectives', 'module-07-pretraining-scaling-laws'),
    ]
    for old, new in stale_links:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            c["stale_link"] += n

    # 4. Chapter-index past tense in prose (specific known patterns)
    past_tense_pairs = [
        (r'\bChapter (\d+) covered\b', r'Chapter \1 covers'),
        (r'\bChapter (\d+) introduced\b', r'Chapter \1 introduces'),
        (r'\bChapter (\d+) explored\b', r'Chapter \1 explores'),
        (r'\bChapter (\d+) presented\b', r'Chapter \1 presents'),
    ]
    for pat, repl in past_tense_pairs:
        text, n = re.subn(pat, repl, text)
        if n:
            c["past_tense"] += n

    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return c


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    totals = {"em_dash": 0, "essential_reading": 0, "stale_link": 0,
              "past_tense": 0}
    files_edited = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        c = fix(p, dry_run)
        if any(c.values()):
            files_edited += 1
            for k in totals:
                totals[k] += c[k]

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Files edited:                  {files_edited}")
    print(f"Em-dash -> comma (prose):      {totals['em_dash']}")
    print(f"'Essential reading' -> 'Useful': {totals['essential_reading']}")
    print(f"Stale link slugs:              {totals['stale_link']}")
    print(f"Past-tense -> present-tense:   {totals['past_tense']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
