# math2epub

A Claude Code skill that renders LaTeX math into Kindle-safe EPUB content.

## TL;DR

```python
import sys
sys.path.insert(0, ".claude/skills/math2epub/scripts")

# Primary pipeline: plain HTML. Compose math from small helpers.
from html_math import HTML_MATH_CSS, var, frac, hat, summation, sup, op, display

mse = display(
    op("MSE") + " = " + frac("1", var("n")) + " "
    + summation(low="i=1", high=var("n")) + " ("
    + hat(var("y")) + "<sub>" + var("i") + "</sub> &#8722; "
    + var("y", sub="i") + ")" + sup("2")
)

# Fallback pipelines for math that HTML cannot do (multi-line align, dense tensor):
from math2epub import render_batch
svgs = render_batch(items, pipeline="svg")   # {id: str}
pngs = render_batch(items, pipeline="png")   # {id: bytes}
```

## Why this exists

Kindle Previewer 3 has multiple silent bugs in MathML rendering, SVG defs/use shadow DOM handling, and KDP's converter strips certain markup. After comparing four pipelines (MathML, SVG, plain HTML, PNG) in real prose layout, **plain HTML proved best** for the LLMBook: it reflows with body text, matches body weight, survives every KDP conversion, and produces ~20-byte inline expressions. SVG and PNG are kept as fallbacks for math that HTML cannot express (multi-line aligned derivations, dense tensor notation).

See `LESSONS.md` for the full debugging history including 15 lessons.

## Files

```
math2epub/
├── SKILL.md                Claude-facing instructions
├── LESSONS.md              Debugging history, by date (L1 through L15)
├── README.md               This file
├── scripts/
│   ├── html_math.py        Plain-HTML helpers (PRIMARY). Atoms: var, frac, hat, bar,
│   │                       vec, sqrt, summation, integral, product, sub, sup.
│   │                       Constants: GREEK, OPS. CSS string: HTML_MATH_CSS.
│   ├── math2epub.py        Unified `render` and `render_batch` for SVG / PNG
│   ├── render_svg.py       MathJax SVG pipeline (Python wrapper around Node)
│   ├── render_png.py       matplotlib mathtext pipeline
│   ├── tex2svg.js          MathJax SVG batch renderer (called via Node)
│   └── validate.py         epubcheck wrapper
└── examples/
    ├── demo.py             SVG + PNG smoke test
    └── html_examples.py    Plain-HTML showcase (prose, display, table,
                            12-formula gallery, Greek+operators reference,
                            typography edge cases). Outputs:
                              demo-output/math-html-examples.html
                              demo-output/math-html-examples.epub
```

## Requirements

- Python 3.11+ with matplotlib
- Node.js with `mathjax-full` installed (default path `E:/Tools/mathjax/`)
- Java + epubcheck for validation (default path `E:/Tools/epubcheck/`)

## Install

The skill lives at two paths simultaneously:

- **Source**: `.claude/skills/math2epub/` inside the LLMBook repo
- **Global**: `C:/Users/apart/.claude/skills/math2epub/` (NTFS junction to source)

Setup script (run once):

```cmd
mklink /J "C:\Users\apart\.claude\skills\math2epub" "E:\Projects\BookBlogsHome\LLMBook\.claude\skills\math2epub"
```

After that, edits to the project copy are immediately visible in the global mirror.
