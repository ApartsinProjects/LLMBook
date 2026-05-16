# What Comes Next Trim Report

## Scope
- **Files scanned**: 76 (all `index.html` files with `<div class="whats-next">` blocks, plus 4 front-matter pages; skip-dirs excluded)
- **Block variants**: `<h2>What Comes Next</h2>` and `<h3>What's Next?</h3>` both detected

## Edits
- **Files edited**: 8
- **Net sentences cut**: ~10 (block-internal; estimated by parser counting end-of-sentence punctuation)
- **Character reduction in edited blocks**: ~3,490 chars before -> ~1,780 chars after (~49% trimmed)

## Edited files
1. `part-7-multimodal-generation/index.html` (3->3 sentences, 642->430 chars; the canonical BEFORE example in the spec)
2. `part-7-multimodal-generation/module-32-embodied-world-models/index.html` (4->2)
3. `part-11-applications-across-industries/module-58-creative-industries/index.html` (4->2)
4. `part-11-applications-across-industries/index.html` (3->2; also FIXED a broken self-link `<a href="index.html">Part XII</a>` that pointed to itself; now links to `../part-12-frontiers/index.html`)
5. `part-11-applications-across-industries/module-59-recommendation-search/index.html` (3->2)
6. `part-12-frontiers/module-62-frontier-theory/index.html` (3->1; ADDED missing hyperlink to Chapter 63)
7. `part-12-frontiers/module-64-agi-trajectories/index.html` (3->1; ADDED hyperlinks to Chapter 65 and capstone)
8. `part-9-safety-security-ethics/module-38-agent-safety-security/index.html` (3->2)

## Sentence-count histogram

| Sentences | Before | After |
|-----------|--------|-------|
| 1         | 36     | 37    |
| 2         | 30     | 36    |
| 3         | 8      | 3     |
| 4         | 2      | 0     |
| Total     | 76     | 76    |

## Link integrity
- **Links dropped**: 0
- **Links added** (during compression, to address missing or broken hyperlinks): 6
  - Part XI index: broken self-link replaced with valid Part XII / appendices / capstone links
  - module-62: text-only "Chapter 63" upgraded to hyperlink
  - module-64: text-only "Chapter 65" + capstone upgraded to hyperlinks
- **All 28 link targets in edited blocks resolve** (verified by `validate_links.py`)

## Not edited (intentional)
- 36 blocks with 1 sentence (already minimal; many are `TODO author this` placeholders in Part X)
- 30 blocks with 2 sentences (already on target)
- 3 remaining 3-sentence blocks judged already-focused: `part-12-frontiers/module-65-tools-of-the-trade/index.html` (150 chars), `part-4-training-adapting/index.html` (275 chars), `part-7-multimodal-generation/index.html` (compressed but still 3 sentences by design, matching the spec's AFTER example)

## Notes
- No file appeared mid-shift from another agent.
- Helper scripts and the file index were temporary; cleaned up after run.
