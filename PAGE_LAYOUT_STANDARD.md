# Page Layout Standard

Every content page in the book follows the SAME outer skeleton. This document
is the canonical reference; deviations break user experience (broken
navigation, content stranded after the footer, inconsistent appendix vs
chapter pages).

## Canonical structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>...</title>
  <link rel="stylesheet" href="…/styles/book.css">
  …KaTeX, Prism, Pagefind links…
</head>
<body>

<header class="chapter-header">
  <nav class="header-nav">…book title link, contents link…</nav>
  <div class="header-search"><div id="search"></div></div>
  <div class="part-label" data-pagefind-meta="part">Part X: …</div>
  <div class="chapter-label" data-pagefind-meta="chapter">Chapter NN: …</div>
  <h1>Page Title</h1>
</header>

<main class="content">
  <span hidden data-pagefind-meta="part:Part X: …"></span>
  <span hidden data-pagefind-meta="chapter:Chapter NN: …"></span>

  <!-- prose, callouts, code, figures, etc -->

  <!-- For chapter / appendix INDEX pages only: section grid -->
  <div class="section-grid">
    <a class="section-card" href="…">…</a>
    …
  </div>

  <!-- Bottom nav: prev / up / next, all three are <a> links -->
  <nav class="chapter-nav">
    <a class="prev" href="…">Prev label</a>
    <a class="up"   href="…">Up label</a>
    <a class="next" href="…">Next label</a>
  </nav>

  <footer><p>Fifth Edition, 2026 &middot; <a href="…/toc.html">Contents</a></p></footer>
</main>

<script>…PagefindUI init…</script>
</body>
</html>
```

## Hard rules

1. **Order inside `<main>` is FROZEN**: prose → optional section-grid → `<nav class="chapter-nav">` → `<footer>` → `</main>`. Nothing else after `<footer>` except whitespace and the `</main>` close tag.

2. **`<nav class="chapter-nav">` MUST contain exactly three `<a>` elements**, in this order:
   - `<a class="prev" href="…">…</a>` — last section of previous chapter, or last section of this chapter for section pages
   - `<a class="up" href="…">…</a>` — link to the parent chapter index, or to the part landing page for chapter index pages
   - `<a class="next" href="…">…</a>` — first section of next chapter / next section of this chapter

   **No plain text in nav.** Every visible word must be wrapped in an anchor.

3. **Section-grid appears INSIDE `<main>` and BEFORE the chapter-nav.** Never after `</footer>`. Chapter index pages have one; section pages have none.

4. **Every page has a `<footer>`** with edition + Contents link.

5. **Pagefind meta spans** (`<span hidden data-pagefind-meta="…">`) sit at the very top of `<main>` so they get indexed even though the visible header is in `exclude_selectors`.

## Page-type variants

| Page type           | `prev` link target                 | `up` link target          | `next` link target            |
|---------------------|------------------------------------|---------------------------|-------------------------------|
| Front matter        | previous FM page                   | toc.html                  | next FM page or first chapter |
| Part landing        | last section of previous part      | toc.html                  | first chapter of this part    |
| Chapter index       | last section of previous chapter   | parent part landing       | first section of this chapter |
| Chapter section     | previous section (same chapter)    | this chapter index        | next section (same chapter)   |
| Appendix index      | last section of previous appendix  | appendices/index.html     | first section of this appendix |
| Appendix section    | previous section (same appendix)   | this appendix index       | next section (same appendix)  |
| toc.html            | (front matter index)               | index.html (book home)    | first chapter                 |

## Common layout mistakes (all auto-detected by `_v628_audit_layout.py`)

| Code | Symptom                                | Auto-fix                       |
|------|----------------------------------------|--------------------------------|
| A    | Nav contains plain text (no anchor)    | wrap in proper `<a>` tags      |
| B    | Nav appears AFTER `<footer>`           | move nav before footer         |
| C    | `<div class="section-grid">` after footer | move grid before nav        |
| C2   | Other stray content after footer       | move inside main, above nav    |
| E    | Page has no `<nav class="chapter-nav">`| insert canonical 3-link nav    |
| F    | Page has no `<footer>`                 | insert canonical footer        |

`_v629_normalize_layout.py` applies all six fixes idempotently.
