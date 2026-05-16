#!/usr/bin/env python3
"""Test the standardize_bib functions on sample files in /tmp/bibtest."""
import sys
from pathlib import Path

sys.path.insert(0, "E:/Projects/BookBlogsHome/LLMBook/.book-update")
sys.stdout.reconfigure(encoding="utf-8")

# Monkey-patch ROOT and run on test files
import standardize_bib as sb

sb.ROOT = Path("C:/Users/apart/AppData/Local/Temp/bibtest")
sb.SKIP_DIRS = set()

testdir = Path("C:/Users/apart/AppData/Local/Temp/bibtest")
if not testdir.exists():
    testdir = Path("/tmp/bibtest")

for p in testdir.glob("*.html"):
    print("\n" + "="*80)
    print("PROCESSING:", p.name)
    print("="*80)
    orig = p.read_text(encoding="utf-8")
    edited = sb.process_file(p)
    if edited:
        new = p.read_text(encoding="utf-8")
        # Print only the diff around bibliography
        # Find the new callout bibliography
        s = new.find('<div class="callout bibliography">')
        if s >= 0:
            e = sb.find_balanced_div(new, s)
            if e:
                print(new[s:e][:3000])
        else:
            print("(no callout bibliography in output)")
    else:
        print("(file not changed)")

print("\nStats:", dict(sb.stats["variants"]))
print("Entries preserved:", sb.stats["entries_preserved"])
print("rel/target added:", sb.stats["rel_attrs_added"])
