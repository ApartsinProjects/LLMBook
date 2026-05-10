# Diagram Regeneration — Subagent Brief

You are designing technical diagrams as part of a larger book-redesign sweep. The main agent will pass you 5 specific figures to design. Read each .mmd source, design a high-quality SVG, save to disk. The main agent handles wiring after you finish.

## Tools you must use

- **Read**: read each .mmd source file before designing
- **Write**: emit SVG files
- **Bash**: optional, for running `verify_svg.py` to self-check

## Skill location

`C:/Users/apart/.claude/skills/technical-diagram-designer/` (v1.4)

Read these BEFORE designing:
- `SKILL.md` — workflow + rules R1-R10
- `PATTERNS.md` — 21 named patterns with reference SVGs
- `HELPERS.md` — SVG snippets (markers, callouts, pills, tonal echo)
- `chart_helpers.py` — Python codegen for heatmaps, bars, log axes (USE THIS for charts)

## Design conventions (non-negotiable)

### Canonical color palette (semantic)
- **data / input**: `#1a4078` border on `#eef4fa` fill
- **model / inference**: `#1f7a3a` border on `#ecf6ee` fill
- **orchestration / control**: `#722f8a` border on `#f4ecf7` fill
- **store / data store**: `#7a5e1a` border on `#fef3e0` fill (also for callouts: `#d4b96a` on `#fff5dc`)
- **warning / error**: `#b3401b` border on `#fdeee8` fill
- **frozen / muted**: `#5a4a3a` border on `#f0f0f0` fill
- **text dark**: `#1a1a2e`
- **text muted**: `#5a4a3a`

### Typography
- Title: `font-size="22"` to `"28"`, font-weight=600
- Subtitle: 13, italic
- Section labels: 14-18, weight=700
- Box labels: 12-14
- Body / annotations: 11-12 (NEVER smaller than 11)
- Use `font-family="Helvetica, Arial, sans-serif"` on root `<svg>`

### Canvas
- Default viewBox: `0 0 1300 700` for landscape, `0 0 1200 800` for portrait
- Always include `<defs>` with `<marker id="arr">` for arrowheads

### Standard `<defs>` block
```xml
<defs>
  <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#1a1a2e"/>
  </marker>
</defs>
```

### Mandatory components per diagram
1. **Title** at top: `<text font-size="24" font-weight="600" text-anchor="middle">...`
2. **Subtitle** under title: 13px, gray (`#5a4a3a`), one-sentence summary
3. **Bottom takeaway** strip: rounded rect with "Key idea" header + 1-2 sentence explanation
4. Use **callout boxes** (yellow `#fff5dc` / `#d4b96a`) for "Why?" / "Diagnose" / "Use when" sidebars

### Forbidden
- Font sizes below 11px
- 3-digit hex shortcuts (`#fff` → use `#ffffff`)
- Pure black strokes (`#000000` → use `#1a1a2e`)
- Em dashes (—) — use commas, semicolons, parentheses, or "—" written as "--"

## Per-figure workflow

For each of the 5 figures assigned:

### Step 1 — Read source
```python
# main agent will give you a path like:
# part-1-foundations/module-XX-...../images/fig-A.B.C-name.mmd
# Always read it first to understand intent
```

### Step 2 — Decide diagram type
Use the decision tree from `SKILL.md`:
- Sequential process → pipeline (Pattern 1)
- Comparison → two-lane (Pattern 4)
- Hierarchy → tree (Pattern 3)
- Cycle → lifecycle/cycle (Pattern 5)
- Annotated artifact → side callouts (Pattern 20)
- Fallback chain → cascading staircase (Pattern 21)
- Numerical chart → use `chart_helpers.py`

### Step 3 — Output structured plan (R9)
Before writing SVG, output this template (concise — 5 lines max):
```
## Diagram Plan: <figure-name>
- Decision branch: <type>
- Pattern: <number + name>
- Aspect: landscape 1300×700 (or other)
- Key message: <one sentence>
- Why this beats the original Mermaid: <reason>
```

### Step 4 — Write SVG
Save to: `E:/Projects/BookBlogsHome/LLMBook/KDP/diagrams/svg/<basename>.svg`

Where `<basename>` = the .mmd filename without `.mmd` extension AND truncated to remove the long auto-generated tail (e.g., `fig-0.1.2-gradient-descent-follows-the-slope-downhill-step-by-step-t` → `fig-0.1.2-gradient-descent`).

### Step 5 — Self-verify (optional but recommended)
```bash
/c/Python314/python "C:/Users/apart/.claude/skills/technical-diagram-designer/verify_svg.py" "E:/Projects/BookBlogsHome/LLMBook/KDP/diagrams/svg/<basename>.svg"
```

Should report 0 errors. Warnings about color cardinality on heatmaps are OK.

## Reference example

A well-designed figure shipped in batch 8:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1300 700" font-family="Helvetica, Arial, sans-serif">
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#1a1a2e"/>
    </marker>
  </defs>
  <text x="650" y="40" font-size="24" font-weight="600" text-anchor="middle" fill="#1a1a2e">[Figure title]</text>
  <text x="650" y="66" font-size="13" text-anchor="middle" fill="#5a4a3a">[One-sentence subtitle]</text>

  <!-- Main content here using palette + patterns -->

  <!-- Bottom takeaway -->
  <g transform="translate(80, 620)">
    <rect x="0" y="0" width="1180" height="60" rx="6" fill="#ecf6ee" stroke="#1f7a3a" stroke-width="1.5"/>
    <text x="20" y="25" font-size="13" font-weight="700" fill="#1f7a3a">Key idea</text>
    <text x="20" y="46" font-size="12" fill="#1a1a2e">[1-2 sentence takeaway]</text>
  </g>
</svg>
```

For 50+ shipped reference figures see `KDP/diagrams/svg/*.svg` (each one passes verify_svg.py with 0 errors).

## Return format

When finished with all 5 figures, return a single message:

```
DONE: 5 figures designed, all in KDP/diagrams/svg/
- fig-X.Y.Z-name1.svg (Pattern N: ...)
- fig-X.Y.Z-name2.svg (Pattern N: ...)
- ...
Verify status: <0 errors / N warnings>
```

The main agent will run auto_fix_svg.py + rasterizer + HTML wiring.
