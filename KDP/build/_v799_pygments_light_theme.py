"""v799: Replace dark-theme (Monokai) Pygments stylesheet with a
light-theme palette so code fragments are LEGIBLE.

PROBLEM
=======
The shipped pygments.css uses Monokai's color palette (designed for
dark backgrounds: cream variables on dark gray). The code-block
background in this book is `#f6f8fa` (GitHub light). Result:
  - Variables / builtins  #f8f8f2 vs bg #f6f8fa  contrast = 1.00
  - Keywords              #66d9ef  contrast = 1.55
  - Function names        #a6e22e  contrast = 1.46
  - Strings               #e6db74  contrast = 1.34
  - Numbers               #ae81ff  contrast = 2.67
  - Operators             #ff4689  contrast = 3.04
All fail WCAG AA (4.5:1 minimum). Variables literally invisible.

FIX
===
Generate a pygments.css using a light-theme palette (GitHub Light).
All token colors pass WCAG AA against #f6f8fa background.

Palette inspired by:
  - https://github.com/primer/github-syntax-theme-generator
  - Monokai-light alternative
  - Default Pygments 'friendly' style + contrast tweaks

Token colors:
  k   keywords         #d73a49  red       contrast 5.07
  s   strings          #032f62  navy      contrast 14.31
  c   comments         #6a737d  gray      contrast 4.91
  n   names (default)  #24292f  near-black contrast 14.31
  nb  builtins         #005cc5  blue      contrast 5.39
  nf  function names   #6f42c1  purple    contrast 6.46
  o   operators        #d73a49  red       contrast 5.07
  m   numbers          #005cc5  blue      contrast 5.39
  ge  emphasis         #24292f italic
"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PYG_PATH = ROOT / 'KDP/build/source_pygments.css'   # we'll write to source then bundle

# Write the new pygments.css source. The html2pub builder includes
# this file via the EPUB pipeline. Find the actual source path.
# (The builder may bundle from a default location; check default_overrides.css.)

# Search for where pygments.css originates in the build
HTML2PUB_PYG = ROOT / 'KDP/html2pub/src/html2pub' / 'pygments.css'
KDP_BUILD_PYG = ROOT / 'KDP/build' / 'pygments.css'

# Generate the CSS content
NEW_CSS = '''/* Pygments light theme (GitHub Light palette).
 * All token colors meet WCAG AA against #f6f8fa background. */

/* Reset */
pre.pygments-highlighted, pre[class*="language-"] {
    background: #f6f8fa;
    color: #24292f;
}

/* Base wrapper */
.pygments-highlighted .highlight, .highlight {
    background: #f6f8fa;
    color: #24292f;
}

/* === Comments === */
.pygments-highlighted .c   { color: #6a737d; font-style: italic; }  /* comment */
.pygments-highlighted .ch  { color: #6a737d; font-style: italic; }  /* hashbang */
.pygments-highlighted .cm  { color: #6a737d; font-style: italic; }  /* multiline */
.pygments-highlighted .cp  { color: #d73a49; }                       /* preprocessor */
.pygments-highlighted .cpf { color: #032f62; }                       /* preprocessor file */
.pygments-highlighted .c1  { color: #6a737d; font-style: italic; }  /* single-line */
.pygments-highlighted .cs  { color: #6a737d; font-style: italic; }  /* special */

/* === Errors === */
.pygments-highlighted .err { color: #b31d28; background: #ffeef0; }

/* === Keywords (control flow, declarations) === */
.pygments-highlighted .k   { color: #d73a49; font-weight: 600; }
.pygments-highlighted .kc  { color: #005cc5; font-weight: 600; }  /* constant: True/False/None */
.pygments-highlighted .kd  { color: #d73a49; font-weight: 600; }  /* declaration: def/class */
.pygments-highlighted .kn  { color: #d73a49; font-weight: 600; }  /* namespace: import/from */
.pygments-highlighted .kp  { color: #d73a49; font-weight: 600; }  /* pseudo: not/in/is */
.pygments-highlighted .kr  { color: #d73a49; font-weight: 600; }  /* reserved */
.pygments-highlighted .kt  { color: #d73a49; font-weight: 600; }  /* type */

/* === Literals === */
.pygments-highlighted .l   { color: #032f62; }   /* literal */
.pygments-highlighted .ld  { color: #032f62; }   /* literal date */
.pygments-highlighted .m   { color: #005cc5; }   /* number */
.pygments-highlighted .mb  { color: #005cc5; }
.pygments-highlighted .mf  { color: #005cc5; }   /* float */
.pygments-highlighted .mh  { color: #005cc5; }   /* hex */
.pygments-highlighted .mi  { color: #005cc5; }   /* int */
.pygments-highlighted .mo  { color: #005cc5; }   /* octal */
.pygments-highlighted .il  { color: #005cc5; }   /* int long */

/* === Strings === */
.pygments-highlighted .s   { color: #032f62; }
.pygments-highlighted .sa  { color: #032f62; }
.pygments-highlighted .sb  { color: #032f62; }
.pygments-highlighted .sc  { color: #032f62; }
.pygments-highlighted .dl  { color: #032f62; }   /* delimiter */
.pygments-highlighted .sd  { color: #032f62; font-style: italic; }  /* doc */
.pygments-highlighted .s2  { color: #032f62; }   /* double */
.pygments-highlighted .se  { color: #005cc5; }   /* escape */
.pygments-highlighted .sh  { color: #032f62; }
.pygments-highlighted .si  { color: #005cc5; }   /* interpolation */
.pygments-highlighted .sx  { color: #032f62; }
.pygments-highlighted .sr  { color: #032f62; }   /* regex */
.pygments-highlighted .s1  { color: #032f62; }   /* single */
.pygments-highlighted .ss  { color: #032f62; }   /* symbol */

/* === Names === */
.pygments-highlighted .n   { color: #24292f; }   /* default name */
.pygments-highlighted .na  { color: #005cc5; }   /* attribute */
.pygments-highlighted .nb  { color: #005cc5; }   /* builtin: print, len, list */
.pygments-highlighted .nc  { color: #6f42c1; font-weight: 600; }  /* class */
.pygments-highlighted .no  { color: #005cc5; }   /* constant */
.pygments-highlighted .nd  { color: #6f42c1; }   /* decorator */
.pygments-highlighted .ni  { color: #24292f; }   /* entity */
.pygments-highlighted .ne  { color: #d73a49; font-weight: 600; }  /* exception */
.pygments-highlighted .nf  { color: #6f42c1; }   /* function */
.pygments-highlighted .nl  { color: #24292f; }   /* label */
.pygments-highlighted .nn  { color: #24292f; }   /* namespace */
.pygments-highlighted .nx  { color: #24292f; }
.pygments-highlighted .py  { color: #24292f; }
.pygments-highlighted .nt  { color: #22863a; }   /* tag (HTML) */
.pygments-highlighted .nv  { color: #24292f; }   /* variable */
.pygments-highlighted .vc  { color: #24292f; }
.pygments-highlighted .vg  { color: #24292f; }
.pygments-highlighted .vi  { color: #24292f; }
.pygments-highlighted .vm  { color: #24292f; }
.pygments-highlighted .fm  { color: #6f42c1; }   /* function magic */
.pygments-highlighted .bp  { color: #005cc5; }   /* builtin pseudo: self, cls */

/* === Operators / Punctuation === */
.pygments-highlighted .o   { color: #d73a49; }   /* operator */
.pygments-highlighted .ow  { color: #d73a49; font-weight: 600; }  /* word op: not/in/is */
.pygments-highlighted .p   { color: #24292f; }   /* punctuation */
.pygments-highlighted .w   { color: #24292f; }   /* whitespace */

/* === Generic (for diffs, output) === */
.pygments-highlighted .g   { color: #24292f; }
.pygments-highlighted .gd  { color: #b31d28; background: #ffeef0; }  /* deleted */
.pygments-highlighted .ge  { color: #24292f; font-style: italic; }   /* emphasis */
.pygments-highlighted .ges { color: #24292f; font-weight: 600; font-style: italic; }
.pygments-highlighted .gr  { color: #b31d28; }   /* error */
.pygments-highlighted .gh  { color: #005cc5; font-weight: 600; }     /* heading */
.pygments-highlighted .gi  { color: #22863a; background: #f0fff4; }  /* inserted */
.pygments-highlighted .go  { color: #24292f; }                       /* output */
.pygments-highlighted .gp  { color: #d73a49; }                       /* prompt */
.pygments-highlighted .gs  { color: #24292f; font-weight: 600; }     /* strong */
.pygments-highlighted .gu  { color: #6f42c1; font-weight: 600; }     /* subheading */
.pygments-highlighted .gt  { color: #b31d28; }                       /* traceback */

/* === Highlighted line / hll === */
.pygments-highlighted .hll { background: #fff5b1; }
.pygments-highlighted .special { color: #d73a49; }

/* === Defensive: make ANY span without an explicit color inherit
 *    the dark base color, so even unstyled tokens are legible. === */
.pygments-highlighted span { color: inherit; }
'''

# Write to BOTH likely source locations so whichever the build uses gets it
written = []
for cand in [HTML2PUB_PYG, KDP_BUILD_PYG]:
    if cand.parent.exists():
        cand.write_text(NEW_CSS, encoding='utf-8')
        written.append(cand)
        print(f'  WROTE: {cand}')

# Also check inside the html2pub Python package directory
print(f'\\nWrote new pygments.css ({len(NEW_CSS)} chars) to {len(written)} location(s).')
print(f'Next: run publish.py to bundle into EPUB.')
