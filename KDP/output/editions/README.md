# Per-Edition EPUB Archive

Each subfolder here holds the canonical EPUB for one numbered edition of
*Building Conversational AI with LLMs and Agents*. The latest build at
`KDP/output/building-conversational-ai-llms-agents.epub` always reflects
the current working tree; the per-edition copies here are immutable
snapshots tied to a git tag.

## Naming convention

```
KDP/output/editions/<N>th-edition/building-conversational-ai-llms-agents-<N>th-edition.epub
```

`N` is the `book.edition_number` field in `KDP/metadata/metadata.yaml`.
The build script reads that field and writes the per-edition copy
automatically; you do not need to do anything beyond bumping the
metadata when starting a new edition.

## How to start a new edition

1. Bump `book.edition` and `book.edition_number` in `KDP/metadata/metadata.yaml`.
2. Update `book.publication_date`.
3. Make all your changes; commit them.
4. Run `python KDP/build/build_epub.py --max-image-side 1200 --jpeg-quality 80`.
5. Run `epubcheck` against the output and verify 0 errors.
6. Tag the commit: `git tag -a "<N>th-edition" -m "..." HEAD` then `git push origin <N>th-edition`.

## Editions on file

| Edition | Date | Git tag | EPUB file |
|---|---|---|---|
| 6th | 2026-05-13 | `6th-edition` | `6th-edition/building-conversational-ai-llms-agents-6th-edition.epub` |

## Why archive locally rather than only in git tags?

Three reasons:

1. **EPUB is binary**: large, slow to diff, slow to checkout. Having a
   copy on disk per edition lets you A/B-compare without `git checkout`
   round-trips.
2. **External tooling**: KDP, EPUBCheck, Calibre, and other readers
   all want a stable file path you can hand them. Each edition's path
   stays valid forever.
3. **Reader-comparison demos**: pointing both EPUBs at the same Kindle
   shows readers what changed between editions.

The archive folder is checked into git; it grows by one EPUB per
edition (≈ 50 MB each). Beyond ~10 editions consider git-LFS.
