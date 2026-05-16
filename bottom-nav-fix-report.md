# Bottom Nav Correctness Report

## Summary
- Files scanned: 503
- Files with correct nav (no edit): 157
- Files fixed: 234
- Files with no nav block (created): 5
- Files skipped (in flight, mtime < 10 min): 107

## Per-bucket findings
- Sections: 92 fixed, 145 correct, 0 created
- Chapter indexes: 52 fixed, 9 correct, 0 created
- Part indexes: 12 fixed, 0 correct, 0 created
- Appendix sections: 59 fixed, 3 correct, 0 created
- Appendix indexes: 16 fixed, 0 correct, 5 created
- Appendix root: 0 fixed, 0 correct, 0 created (skipped, in-flight)
- Front matter: 3 fixed, 0 correct, 0 created (4 of 7 skipped, in-flight)

## Issue type breakdown
- Wrong href target: 149
- Wrong nav-num text: 151
- Wrong nav-title text: 234
- Wrong nav-label text: 0
- Missing nav block (created): 5
- Duplicate nav blocks (cleaned): 0
- Broken hrefs stripped: 0

## Notes

Source of truth: discovery walks the filesystem (parts, modules, sections, appendices, front-matter) in canonical reading order. Section ordering uses natural numeric sort on `section-N.M.html`; appendix sections use `section-X.M.html`. Mixed-numbering chapters (e.g., module-61 contains section-33.4 + section-33.11 + section-61.1-.4) are sorted into a single chain; the last section transitions to the next chapter's first section, and the chapter index itself points to the next chapter.

Contract decisions made:
- Part 1 prev points at the last front-matter page (copyright.html) when FM is present.
- Last part's "next" points at appendices/index.html.
- Appendices root: prev = last part index (Part XII Frontiers), up = toc.html, next = Appendix A.
- Last appendix (U War Stories) next = toc.html.
- Last appendix section in a non-final appendix transitions to the next appendix's first section.
- Front matter "up" points at toc.html (the user noted FM index.html is being dropped).
- Front matter reading order: foreword > look-inside-preview > fm-what-this-book-covers > fm-who-should-read > fm-how-to-use > about-authors > copyright > Part I.

Empty-section chapters in Part 11 (chapters 54, 56, 57) have no section files on disk; their index page's next points at the next chapter's index. Chapters 51-53, 55, 58-60 have section files on disk that book_structure.yaml does not enumerate fully; the filesystem is the ground truth and the chain was built from disk.

Edge-case handling:
- One `<a>` is omitted if its target doesn't exist on disk (broken href stripped). No broken hrefs were detected on the 396 non-skipped pages.
- Duplicate nav blocks: keep first, delete rest. None found (the earlier dup-nav fix script covered these).
- Missing block: 5 appendix indexes (e.g., appendix-r-reading-pathways, appendix-g-problem-solution-key) had no nav-block at all and were created.

The 107 skipped files were modified within the past 10 minutes (multiple authoring / enrichment agents still in flight on Parts 1-12 sections, the appendices root, and 4 front-matter pages including foreword.html and look-inside-preview.html). They will need a follow-up pass after those agents land.

## Skipped files (count by area)
- Front matter: 4 (foreword, look-inside-preview, fm-who-should-read, about-authors)
- Part 1 Foundations: 5 sections
- Part 2 Understanding LLMs: 18 sections
- Part 3 Working with LLMs: 4 sections
- Part 4 Training and Adapting: 13 sections
- Part 5 Retrieval and Conversation: 8 sections
- Part 6 Agentic AI: 8 sections
- Part 7 Multimodal Generation: 4 sections
- Part 8 Evaluation and Production: 7 sections
- Part 9 Safety, Security and Ethics: 5 sections
- Part 10 Idea to Product: 1 section
- Part 11 Applications: 13 sections + 2 chapter indexes (52, 53)
- Part 12 Frontiers: 4 (1 section + 3 chapter indexes 63/64/65)
- Appendices: 8 sections (e.2, e.3, f.2, f.3, i.7, n.1, o.2) + appendices/index.html
