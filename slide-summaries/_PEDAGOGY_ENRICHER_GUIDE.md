# Pedagogy Enricher Guide

For each technique in your assigned brief JSON, **add the missing pedagogy dimensions** so the section reads like a textbook explanation rather than a survey-paper list.

## The 4 dimensions
For each technique, the audit reports a 4-element vector `[has_figure, has_math, has_code, has_example]`. You must add what is missing:

| Missing | What to add |
|---|---|
| **figure** | An architecture / flow / decision diagram (inline SVG OR a Mermaid PNG + caption). 1 figure is enough. |
| **math** | A KaTeX equation block (`$$...$$`) that captures the core formula. 1-3 equations is enough. |
| **code** | A working `<pre><code class="language-python">...</code></pre>` block, 5-20 lines, with caption BELOW. Prefer real library calls (HF Transformers / PyTorch / LangChain / etc.). |
| **example** | A `<div class="callout practical-example">` or `<div class="callout numeric-example">` with concrete numbers / a worked walkthrough. |

## Style rules (HARD)
- **No em dashes (—) or `--`** in any new prose.
- Third-person voice ("The model learns" not "We learn").
- Book vocabulary: book / part / chapter / section / appendix / reader.
- Preserve domain terms exactly (BPE, RoPE, MoE, LoRA, RLHF, etc.).
- Captions BELOW code blocks, never above.
- Every new figure / code block / callout MUST be referenced in surrounding prose. Add a connecting sentence if needed.
- Use `Edit` tool, not `Write`. Find a stable anchor (existing h3, paragraph end) and insert next to it.
- Idempotent: if the target dimension already exists, skip.

## HTML patterns

### Figure (inline SVG preferred for simple diagrams)
```html
<figure>
  <svg viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">
    <!-- diagram content -->
  </svg>
  <figcaption><strong>Figure X.Y.Z</strong>: <descriptive caption>.</figcaption>
</figure>
```

### Math (KaTeX)
```html
<p>The forward pass computes:</p>
<p>$$ y = \sigma(Wx + b) $$</p>
```

### Code with caption below
```html
<div class="code-block-wrapper">
<pre><code class="language-python">import torch
# minimal working example
...
</code></pre>
<p class="figure-caption"><strong>Code Fragment X.Y.Z</strong>: <descriptive caption>.</p>
</div>
```

### Callout (worked example)
```html
<div class="callout practical-example">
<div class="callout-title">Practical Example: <name></div>
<p>Concrete walkthrough with real numbers...</p>
</div>
```

## Decision tree per technique

1. Read the technique's `canonical_file` and the `canonical_h3` section. Confirm what's missing per the audit's `agg` vector.
2. For each missing dimension, add ONE element:
   - **figure**: prefer inline SVG for simple boxes/arrows; use Mermaid + render to PNG for complex flows.
   - **math**: write the core equation that defines the technique (one line, plus a sentence explaining each symbol).
   - **code**: a minimal HuggingFace / PyTorch / LangChain snippet that runs. If the technique is conceptual (not a library), provide pseudocode in `language-text` style.
   - **example**: a worked example with concrete tensors / numbers OR a real-world scenario, not just prose.
3. Insert each new block adjacent to the most relevant existing prose, with a connecting sentence.
4. Update the `</main>` content; do NOT touch the head, header, footer, or navigation.

## Output format

After processing all techniques in your brief, return a single JSON line:
```
{"bucket": <name>, "status": "ok", "techniques_enriched": <N>, "dimensions_added": {"figure": <a>, "math": <b>, "code": <c>, "example": <d>}, "files_touched": [...]}
```

If a technique cannot be enriched (e.g., section was deleted, file mismatch), note it under `"skipped": [...]`.
