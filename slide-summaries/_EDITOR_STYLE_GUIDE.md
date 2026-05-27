# Editor Style Guide (read by every chapter-family editing subagent)

## HARD style rules
- **No em dashes (—) or `--`** in prose. Use commas, semicolons, parens, or sentence breaks.
- Third-person voice ("The model learns" not "We learn").
- Book vocabulary: "book / part / chapter / section / appendix / reader". Never "course / module / lecture / student".
- Preserve domain terms exactly (BPE, RoPE, ResNet, DPR, MoE, etc.).
- KaTeX math: `$inline$` and `$$display$$`.
- Code blocks: `<pre><code class="language-python">...</code></pre>`. Captions BELOW with `<p class="figure-caption">Caption text</p>` or similar.

## Callout classes (use the matching one for the situation)
```
callout big-picture   - high-level framing at the top of a major section
callout cross-ref     - "see Section X.Y for ..."
callout exercise      - reader practice
callout fun-note      - light humor / anecdote
callout key-insight   - aha moment
callout key-takeaway  - end-of-section recap
callout library-shortcut - HF transformers / langchain / etc. code snippet
callout note          - tangential clarification
callout practical-example - working code / worked numerical example
callout research-frontier - cutting-edge open question
callout self-check    - reader prompt to verify understanding
callout tip           - production gotcha advice
callout warning       - footgun / common mistake
```

Each callout HTML:
```html
<div class="callout key-takeaway">
  <div class="callout-title">Key takeaway</div>
  <p>The actual content.</p>
</div>
```

## Bibliography entry (use the exact pattern)
```html
<div class="bib-entry-card">
  <div class="bib-ref">
    <a href="https://arxiv.org/abs/XXXX.YYYYY" rel="noopener" target="_blank">
      Author, A. et al. (YEAR). "Title." <em>Venue</em>.
    </a>
    Brief one-sentence summary of what the paper contributes and why a reader of this section should care.
  </div>
</div>
```

## In-place editing protocol
- Use the `Edit` tool with old_string + new_string. Find a stable anchor (an existing `<h2>`, `<h3>`, or unique paragraph) and insert content next to it.
- Preserve all existing whitespace and indentation.
- Never delete existing content unless the gap audit explicitly says to.
- For adding a NEW sub-section, insert a complete `<section>` or `<h3>...</h3>...` block at the appropriate location.
- For adding a single callout, insert just the `<div class="callout ...">...</div>` block.
- For adding bibliography entries, find the existing bib block and append new `<div class="bib-entry-card">...</div>` entries inside it.

## Cross-reference HREF patterns
- Same module: `section-N.M.html`
- Sibling module in same part: `../module-XX-name/section-N.M.html`
- Different part: `../../part-N-name/module-XX-name/section-N.M.html`
- Appendix: `../../appendices/appendix-X-name/section-x.y.html`

## What goes into each edit
Each "missing" item from the gap audit JSON typically becomes:
- A new `<h3>` sub-section (if substantive enough), OR
- A new `<p>` paragraph (if just a name / brief mention), OR
- A new callout (if it's a footgun or practical example), OR
- A new code block + caption (if it's a code recipe), OR
- A new bibliography entry (if it's just adding a missing citation).

Each "partial" item typically becomes:
- An expansion to an existing paragraph (deeper explanation), OR
- A new callout that clarifies the slide's specific angle, OR
- A new bibliography entry to add the canonical reference.

## Forbidden
- Do NOT touch any chapter, section, or file outside your assigned scope.
- Do NOT update `toc.html` or any central navigation. The orchestrator handles that.
- Do NOT renumber existing sections.
- Do NOT change existing prose unless deepening it per the gap audit.
