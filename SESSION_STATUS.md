# Session Status: 2026-05-11

Snapshot of major work-in-progress on the LLMBook EPUB pipeline and book restructure.

## Repo state

| Item | Value |
|---|---|
| Repo | https://github.com/ApartsinProjects/LLMBook |
| Branch | `main` |
| Last committed work | `9d11ef0 fix(epub): switch math to MathML, fix silent hook failures` |
| Tag for safe rollback | `v3-pre-restructure` (pushed) |
| In-progress (uncommitted) | Restructure file deletes + Steps 1-5 helper scripts under `KDP/build/_step*.py` |
| Latest EPUB | `KDP/output/building-conversational-ai-llms-agents.epub` |

## Word counts

| Metric | Before this session | After Steps 1-5 |
|---|---|---|
| Sections (parts only) | 245 | 226 |
| Sections (appendices) | 108 | 83 |
| **Total sections** | **353** | **309** (-12%) |
| Word count | 1,284,573 | 1,311,654 (note: still high; cuts so far were duplicates, no large prose-trimming yet) |
| Appendices | 22 (A-V) | 17 (M, N, O, P, Q removed) |

## Completed work this session (chronological)

### A. EPUB math + validation fixes (committed)
1. **Switched math rendering from KaTeX HTML to MathML** (`KDP/html2pub/src/html2pub/render_math.js`). Eliminated the ~400 empty structural spans per chapter that Kindle painted as black-box tofu (`???`).
2. **Fixed silent plugin failure**: `python -m html2pub` couldn't import `_html2pub_hooks` because `KDP/build/` was not on PYTHONPATH. The "[warn] No module named '_html2pub_hooks'" was swallowed in batch output. Across many builds the project hooks (Pygments highlighting, wisdom-council slim, math cleanup) were silently doing nothing.
   - Fix in `KDP/build/publish.py`: sets `PYTHONPATH=KDP/build` before invoking html2pub.
   - Fix in `KDP/html2pub/src/html2pub/builder.py`: `post_process` plugin loading now hard-fails with a clear error, never silently no-ops.
3. **OPF-014 (71 epubcheck errors)**: chapters with `<math>` now declare `properties="mathml"` in the OPF manifest (`builder.py`).
4. **TeX rewrite**: `\text{XYZ}` -> `\mathrm{XYZ}` for alphanumeric content, applied in `math_render.py` before sending to KaTeX. Avoids a KaTeX MathML schema bug.
5. **Strip invisible-operator `<mo>`** from `<msub>`/`<msup>` children, fixing remaining schema violations from `\max`, `\min`, `\sup` in subscripts.

Result: **epubcheck passes 0 errors / 0 warnings.** Math is centered, sits on text baseline, no tofu.

### B. CSS adjustments (committed)
- `KDP/html2pub/src/html2pub/default_overrides.css`: MathML-specific alignment rules added.
  - `math { vertical-align: -0.25em }` for inline math (Kindle puts inline `<math>` at top of line by default).
  - `.math-block { text-align: center }` plus inline-block centering for display math.

### C. Book restructure (uncommitted)
Tagged v3-pre-restructure baseline first. Then executed five planned cuts via one-shot scripts under `KDP/build/_step*.py`:

| Step | Script | Action | Outcome |
|---|---|---|---|
| 1 | `_redirect_rewrites.py` | Deleted 5 duplicate sections (29.5, 29.7 stubs + 22.2, 29.8, 35.7 dups) | 59 cross-refs rewritten, 5 files removed |
| 2 | `_move_35_to_26.py` | Moved 35.5/35.6/35.8 (agent reliability content misplaced in "AI & Society") into Module 26 as 26.8/26.9/26.10 | 3 files moved, inbound refs updated |
| 3 | `_step3_slim_eval.py` | Slimmed evaluation: removed 13.3, 21.7, 22.8, 25.6, 29.3, 29.9, 29.12, 30.4 | 8 files removed, 86 refs rewritten |
| 4 | `_step4_consolidate.py` | Consolidated reasoning + agents: removed 11.5, 24.3, 24.4, 25.3, 25.5, 25.8 | 6 files removed, 44 refs rewritten |
| 5 | `_step5_appendix_cut.py` | Dropped appendices M (LangGraph), N (CrewAI), O (LlamaIndex), P (Semantic Kernel), Q (DSPy) | 5 directories / 25 sections removed, 90 refs rewritten |

**Total: 24 source-section files deleted, 5 appendix directories removed, ~280 cross-references rewritten across ~130 files.**

## Pending / not committed

1. **Verify final EPUB build** - rebuild was triggered (background task `bvq6nrmpt`) but I have not yet confirmed:
   - `epubcheck` still passes 0 errors after restructure
   - All inbound cross-references resolve (no broken `<a href>`)
   - Actual EPUB file size + chapter count match `spine_manifest.json` (309)

2. **Commit the restructure**. Pending message:
   ```
   restructure(v3.1): drop 24 sections + 5 framework appendices for adoption

   - Step 1: 5 duplicate sections removed
   - Step 2: 35.5/35.6/35.8 moved into Module 26 (correct home)
   - Step 3: evaluation slimmed 13->5 sections
   - Step 4: 6 small/duplicate sections removed (11.5, 24.3-4, 25.3/5/8)
   - Step 5: appendices M/N/O/P/Q dropped (kept K HuggingFace + L LangChain)
   - 280+ cross-references rewritten to point to surviving canonical sections
   - Spine: 353 -> 309 sections (-12%)
   ```

3. **Update `BOOK_CONFIG.md`** to reflect the new spine: section gaps in Module 22 (no 22.2), Module 24 (no 24.3, 24.4), Module 25 (no 25.3, 25.5, 25.8), Module 29 (no 29.3, 29.5, 29.7, 29.8, 29.9, 29.12), Module 30 (no 30.4), Module 35 (no 35.5, 35.6, 35.7, 35.8). Module 26 grew (now has 26.8, 26.9, 26.10).

4. **Tag v3.1** after the restructure commit lands and EPUB verifies clean.

## Pending follow-ups (not started)

These were discussed but not executed:

- **Renumber to remove gaps**: Currently chapters have gaps like 22.1, 22.3, 22.4, 22.5, 22.6, 22.7. Renumbering to 22.1-6 would be cleaner but breaks every cross-reference + reader bookmarks. Defer until v4.
- **Slim H2/H3 in over-headed chapters**: 32.1 (14 H2 / 18 H3), 4.1 (14/19), 4.3 (12/26), 27.7 (8/39), 12.5 (12/21). Hard cap at 6 H2 / 12 H3 was suggested. Not done yet, requires per-chapter manual editing.
- **Module 18 (Interpretability)**: suggested move from Part 2 to Part 10 (Frontiers). Not done.
- **Module 16 (Distillation & Merging)**: suggested merge into Module 15 (PEFT). Not done.
- **Module 35 (AI & Society)**: now half-empty after Step 2. Suggest merging the remaining 4 sections (35.1-35.4 + 35.9) into Module 32 (Safety & Ethics) and deleting Module 35 entirely. Not done.
- **Module 36/37/38** (product strategy): suggested compression to 1 chapter "From Prototype to Production". Not done.
- **Module 29 + 30 merger**: highly redundant after evaluation slim. One unified chapter would drop ~40K words. Not done.
- **Index pages**: 38 module-index files repeat what part-level intro covers (~30K words of "in this chapter you will learn..."). Replace each with 100-word abstract + section list. Not done.

## Useful commands for next session

```bash
# Repo
cd /e/Projects/BookBlogsHome/LLMBook
git status
git log --oneline -5

# Build EPUB (uses PYTHONPATH=KDP/build for hook loading)
/c/Python314/python KDP/build/publish.py

# Direct html2pub build (faster, no optimization)
PYTHONPATH=/e/Projects/BookBlogsHome/LLMBook/KDP/build /c/Python314/python -m html2pub build .

# Spot check EPUB content
/c/Python314/python -c "
import zipfile, re
z = zipfile.ZipFile('KDP/output/building-conversational-ai-llms-agents.epub')
h = z.read('EPUB/chapters/ch_0029_part-1-foundations-module-03-sequence-models-attention-section-3-1.xhtml').decode('utf-8')
print(h[:2000])
"

# Word count audit
/c/Python314/python -c "
import re
from pathlib import Path
total = sum(len(re.sub(r'<[^>]+>',' ',p.read_text('utf-8','replace')).split())
            for p in Path('.').glob('part-*/module-*/section-*.html'))
print(f'{total:,} words')
"

# Regenerate spine after deletions
/c/Python314/python KDP/build/generate_spine.py

# Validate
java -jar /e/Tools/epubcheck/epubcheck-5.1.0/epubcheck.jar KDP/output/building-conversational-ai-llms-agents.epub
```

## Key files (orientation for future work)

| Path | Purpose |
|---|---|
| `BOOK_CONFIG.md` | Canonical chapter map. **Stale after restructure - needs update.** |
| `KDP/html2pub/src/html2pub/builder.py` | Main EPUB assembly. Hard-fails on missing plugin (new). |
| `KDP/html2pub/src/html2pub/math_render.py` | TeX -> MathML via Node bridge. Pre-rewrites `\text` -> `\mathrm`. |
| `KDP/html2pub/src/html2pub/render_math.js` | KaTeX renderToString with `output: 'mathml'`. |
| `KDP/html2pub/src/html2pub/default_overrides.css` | EPUB CSS overrides (math, code, captions, KaTeX legacy). |
| `KDP/build/_html2pub_hooks.py` | Project post_process hook. Strips invisible `<mo>` from `<msub>/<msup>`. |
| `KDP/build/publish.py` | Pipeline orchestrator. Sets `PYTHONPATH=KDP/build` before html2pub. |
| `KDP/build/spine_manifest.json` | Generated by `generate_spine.py` from disk walk. |
| `KDP/build/_redirect_rewrites.py` | Step 1 (one-shot, can re-run safely if needed). |
| `KDP/build/_move_35_to_26.py` | Step 2 (idempotent file moves + path fixups). |
| `KDP/build/_step3_slim_eval.py` | Step 3. |
| `KDP/build/_step4_consolidate.py` | Step 4. |
| `KDP/build/_step5_appendix_cut.py` | Step 5. |
| `~/.claude/skills/html2pub/SKILL.md` | html2pub Claude skill v1.2.1 with 16 production lessons. **Update to v1.3 with Lesson 17 (MathML over HTML for Kindle) and Lesson 18 (PYTHONPATH for project plugins) is pending.** |

## Open questions for next session

- Confirm the restructured EPUB still passes `epubcheck` clean. If new errors surface (broken cross-refs, invalid OPF after deletions), fix before committing.
- Decide whether to renumber to remove section-number gaps now (clean) vs later (avoids cross-ref churn twice).
- Decide whether to proceed with the deferred follow-ups (Module 35 merger, Module 36-38 compression, index-page slim, H2/H3 cap enforcement).
