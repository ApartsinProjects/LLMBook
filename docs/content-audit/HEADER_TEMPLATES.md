# Canonical Header Templates

The book has 3 page types with distinct canonical header structures.

## Template A: Part Index Page

Path pattern: `part-N-*/index.html`

```html
<header class="chapter-header">
  <nav class="header-nav">
    <a class="book-title-link" href="../index.html">Building Conversational AI with LLMs and Agents</a>
    <a class="toc-link" href="../toc.html" title="Table of Contents">
      <span class="toc-icon">&#9776;</span> Contents
    </a>
  </nav>
  <div class="part-label" data-pagefind-meta="part">Part {ROMAN}</div>
  <h1 class="part-title">Part {ROMAN}: {PART_TITLE}</h1>
</header>
```

Notes:
- NO `<div class="header-search">` block — part-level pages don't need their own search box
- `<div class="part-label">` is a single-element label (NOT a multi-level breadcrumb), since part pages ARE the top-level navigation node and don't need to point back to book root
- `<h1 class="part-title">` repeats "Part X: ..." (matches the part-label)
- `data-pagefind-meta="part"` on the part-label so Pagefind indexes "Part XX" as the part name
- Alternative: `<div class="page-breadcrumb" data-pagefind-meta="part">` with breadcrumb chain (older pages). Both forms accepted by the audit plugin.

## Template B: Chapter (Module) Index Page

Path pattern: `part-N-*/module-NN-*/index.html`

```html
<header class="chapter-header">
  <nav class="header-nav">
    <a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>
    <a class="toc-link" href="../../toc.html" title="Table of Contents">
      <span class="toc-icon">&#9776;</span> Contents
    </a>
  </nav>
  <div class="header-search">
    <div id="search"></div>
  </div>
  <div class="page-breadcrumb" data-pagefind-meta="chapter">
    <a href="../index.html">Part {ROMAN}: {PART_TITLE}</a>
    <span class="bc-sep">&rsaquo;</span>
    <span class="bc-current">Chapter {NN}: {CHAPTER_TITLE}</span>
  </div>
  <h1>{CHAPTER_TITLE}</h1>
</header>
```

Notes:
- HAS `<div class="header-search">` (chapter-level pages get the search box)
- Breadcrumb has 2 levels: part → chapter (current)
- `<h1>` is the chapter title alone (no "Chapter NN:" prefix — the breadcrumb carries that)
- `data-pagefind-meta="chapter"` on the breadcrumb

## Template C: Section Page

Path pattern: `part-N-*/module-NN-*/section-NN.M.html`

```html
<header class="chapter-header">
  <nav class="header-nav">
    <a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>
    <a class="toc-link" href="../../toc.html" title="Table of Contents">
      <span class="toc-icon">&#9776;</span> Contents
    </a>
  </nav>
  <div class="header-search">
    <div id="search"></div>
  </div>
  <div class="page-breadcrumb" data-pagefind-meta="chapter">
    <a href="../index.html">Part {ROMAN}: {PART_TITLE}</a>
    <span class="bc-sep">&rsaquo;</span>
    <a href="index.html">Chapter {NN}: {CHAPTER_TITLE}</a>
  </div>
  <h1>{SECTION_TITLE}</h1>
  <div class="page-current">Section {NN.M}</div>
</header>
```

Notes:
- HAS `<div class="header-search">`
- Breadcrumb has 2 anchor LEVELS: part (link) → chapter (link). Chapter is NOT bc-current because the section is the current page.
- `<h1>` = section title (no "Section NN.M:" prefix — `page-current` div carries that)
- `<div class="page-current">Section NN.M</div>` AFTER the h1
- `data-pagefind-meta="chapter"` on breadcrumb (sections index under their chapter, not separately)

## Canonical class names (DO NOT vary)

- Wrapper: `<header class="chapter-header">` (NOT `section-header`, NOT `part-header`)
- Nav: `<nav class="header-nav">`
- Title link: `<a class="book-title-link">`
- TOC link: `<a class="toc-link">` with `<span class="toc-icon">` inside
- Search box: `<div class="header-search"><div id="search"></div></div>`
- Breadcrumb: `<div class="page-breadcrumb" data-pagefind-meta="{part|chapter}">`
- Breadcrumb separator: `<span class="bc-sep">&rsaquo;</span>` (right-angle-quote, not arrow)
- Breadcrumb current: `<span class="bc-current">...</span>`
- Section number: `<div class="page-current">Section NN.M</div>`

## Audit plugin

`agents/book-skills/scripts/audit/checks/p2_header_template.py` enforces:
- All section pages have all 3 of: header-nav, header-search, page-breadcrumb, h1, page-current
- All chapter index pages have all of: header-nav, header-search, page-breadcrumb, h1 (no page-current)
- All part index pages have header-nav, page-breadcrumb, h1 (NO header-search, NO page-current)
- No page uses `<header class="section-header">` or `<header class="part-header">` — must be `chapter-header`
