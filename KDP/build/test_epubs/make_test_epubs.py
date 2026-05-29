"""Generate small test EPUBs to isolate KPV behaviors quickly.

Each test EPUB exercises ONE category of layout/rendering. Running these
through `kindlepreviewer -convert -qualitychecks` takes seconds vs minutes
for the full book, letting us iterate on CSS/source fixes fast.

Categories:
  test_math.epub      - inline math, display math, math-in-table, math-in-callout
  test_tables.epub    - wide tables, tables-in-callout, tables-with-math, tables-with-code
  test_code.epub      - code with leading blank, over-indent, wide lines, multi-language
  test_author.epub    - author cards: photo + bio + links
  test_callouts.epub  - all callout types: note, warning, tip, big-picture, etc.
  test_navigation.epub - section cards, chapter-nav, table of contents
  test_combined.epub  - everything combined (sanity check)

Each EPUB uses the same epub_overrides.css and book.css as the real book,
so any fix applied there gets validated by the test cycle.

Run:
    python make_test_epubs.py [test_name|all]
"""
from pathlib import Path
import zipfile
import shutil
import re
import sys

BUILD = Path(__file__).resolve().parent
ROOT = BUILD.parents[1].parent  # E:/Projects/BookBlogsHome/LLMBook
STYLES = ROOT / 'styles'
OVERRIDES = BUILD.parent / 'epub_overrides.css'
OUT = BUILD / 'output'
OUT.mkdir(parents=True, exist_ok=True)

# ----- Common EPUB chrome -----
MIMETYPE = b'application/epub+zip'

CONTAINER_XML = b'''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="EPUB/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>
'''

CONTENT_OPF_TPL = '''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="en">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{uuid}</dc:identifier>
    <dc:title>Test: {title}</dc:title>
    <dc:language>en</dc:language>
    <dc:creator>epub2kpf test harness</dc:creator>
    <meta property="dcterms:modified">2026-05-15T00:00:00Z</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="css1" href="styles/test.css" media-type="text/css"/>
    <item id="ch1" href="chapter1.xhtml" media-type="application/xhtml+xml" {props}/>
  </manifest>
  <spine>
    <itemref idref="ch1"/>
  </spine>
</package>
'''

# Minimal self-contained CSS for test EPUBs (no external icon refs, no fonts)
TEST_CSS = '''
body { font-family: Georgia, serif; line-height: 1.6; margin: 1em; }
h1 { font-size: 1.6em; margin: 0.5em 0; }
h2 { font-size: 1.3em; margin: 1em 0 0.4em; border-bottom: 1px solid #ddd; padding-bottom: 0.2em; }
h3 { font-size: 1.1em; margin: 0.8em 0 0.3em; }
.chapter-header { background: #1a1f3a; color: white; padding: 1em; margin-bottom: 1em; }
.chapter-header h1 { color: white; }
.chapter-label { color: #f5b942; font-size: 0.85em; text-transform: uppercase; }
.content { padding: 0; }

/* Callouts */
.callout { background: #f5f7fb; border-left: 4px solid #1a4078; padding: 0.8em 1em; margin: 1em 0; page-break-inside: auto; break-inside: auto; }
.callout.note { border-left-color: #3b82f6; background: #eff6ff; }
.callout.warning { border-left-color: #f59e0b; background: #fef3c7; }
.callout.tip { border-left-color: #10b981; background: #ecfdf5; }
.callout.big-picture { border-left-color: #8b5cf6; background: #faf5ff; }
.callout.practical-example { border-left-color: #06b6d4; background: #ecfeff; }
.callout.key-takeaway { border-left-color: #ef4444; background: #fef2f2; page-break-inside: avoid; break-inside: avoid; }
.callout-title { font-weight: bold; margin-bottom: 0.3em; color: #1a1f3a; }

/* Tables */
table { border-collapse: collapse; width: 100%; margin: 1em 0; }
th, td { border: 1px solid #ccc; padding: 0.4em 0.6em; text-align: left; }
th { background: #f5f7fb; }
.comparison-table { display: block; page-break-inside: auto; break-inside: auto; margin: 1em 0; }
.comparison-table-title { background: #1a4078; color: white; padding: 0.5em 0.8em; font-weight: bold; }
.comparison-table > table { display: table; width: 100%; }
table { page-break-inside: auto; break-inside: auto; }
tr { page-break-inside: avoid; }

/* Code */
pre { background: #f6f8fa; border: 1px solid #ddd; padding: 0.8em; overflow-x: auto; font-family: "Courier New", monospace; font-size: 0.9em; page-break-inside: auto; break-inside: auto; }
code { font-family: "Courier New", monospace; }

/* Author cards (v13.15 no-box layout) */
.author-card { display: block; margin: 0.6em 0 1.5em; page-break-inside: auto; break-inside: auto; }
.author-card::after { content: ""; display: block; clear: both; height: 0; }
.author-photo { float: left; width: 120px; max-width: 30%; margin: 0.2em 1em 0.4em 0; border: 1px solid #ccc; border-radius: 4px; }
.author-info { display: block; }
.author-card h3 { margin: 0 0 0.2em; font-size: 1.15em; line-height: 1.25; page-break-after: avoid; }
.author-card p { margin: 0 0 0.6em; line-height: 1.5; text-align: justify; }
.author-links { display: block; margin: 0.4em 0; }
.author-links a { color: #1a4078; text-decoration: underline; margin-right: 0.5em; }

/* Section cards (v13.15 narrow min-width) */
.sections-list { list-style: none; padding: 0; margin: 1em 0; }
.sections-list li { margin: 0.3em 0; }
.section-card { display: flex; flex-wrap: wrap; align-items: flex-start; gap: 0.6em; padding: 0.7em 0.9em; background: white; border: 1px solid #d0d7de; border-left: 4px solid #1a4078; text-decoration: none; color: inherit; page-break-inside: avoid; }
.section-num { display: inline-block; font-weight: bold; color: white; background: #1a4078; padding: 0.25em 0.55em; border-radius: 4px; min-width: 2em; text-align: center; flex-shrink: 0; }
.section-title { font-weight: bold; color: #1a4078; flex: 1 1 0; min-width: 4em; line-height: 1.3; }

/* Chapter nav */
.chapter-nav { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5em; margin: 1.5em 0; }
.chapter-nav a { background: #f5f7fb; border: 1px solid #d0d7de; padding: 0.5em 0.8em; text-decoration: none; color: #1a4078; }

/* Math */
.math-block { text-align: center; padding: 0.5em 0.8em; margin: 0.6em 0; page-break-inside: auto; break-inside: auto; }
.math-block > math { display: inline-block; margin: 0 auto; }
math[display="block"] { display: inline-block; margin: 0 auto; vertical-align: middle; }
'''

NAV_XHTML = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
<title>Navigation</title>
<meta charset="UTF-8"/>
</head>
<body>
<nav epub:type="toc" id="toc">
<h1>Contents</h1>
<ol>
<li><a href="chapter1.xhtml">Test Chapter</a></li>
</ol>
</nav>
</body>
</html>
'''

CHAPTER_TPL = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
<meta charset="UTF-8"/>
<title>{title}</title>
<link rel="stylesheet" type="text/css" href="styles/test.css"/>
</head>
<body>
<header class="chapter-header">
  <div class="chapter-label">Test {slug}</div>
  <h1>{title}</h1>
</header>
<main class="content">
{body}
</main>
</body>
</html>
'''


def make_epub(slug, title, body_html):
    import uuid as uuid_mod
    out_path = OUT / f'test_{slug}.epub'
    # Deterministic UUID per slug
    book_uuid = 'urn:uuid:' + str(uuid_mod.uuid5(uuid_mod.NAMESPACE_OID, f'epub2kpf-test-{slug}'))
    chapter_xhtml = CHAPTER_TPL.format(slug=slug, title=title, body=body_html)
    # Only declare mathml property if chapter has math content
    props = 'properties="mathml"' if '<math' in body_html else ''
    content_opf = CONTENT_OPF_TPL.format(slug=slug, title=title, uuid=book_uuid, props=props)

    # Build ZIP
    if out_path.exists():
        out_path.unlink()
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_STORED) as z:
        # mimetype must be first AND uncompressed
        z.writestr('mimetype', MIMETYPE, compress_type=zipfile.ZIP_STORED)
        # Switch to DEFLATE for rest
        z.writestr('META-INF/container.xml', CONTAINER_XML, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr('EPUB/content.opf', content_opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr('EPUB/nav.xhtml', NAV_XHTML, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr('EPUB/chapter1.xhtml', chapter_xhtml, compress_type=zipfile.ZIP_DEFLATED)
        # Minimal self-contained CSS (no external refs to icons/fonts)
        z.writestr('EPUB/styles/test.css', TEST_CSS,
                   compress_type=zipfile.ZIP_DEFLATED)
    print(f'Built: {out_path} ({out_path.stat().st_size} bytes)')
    return out_path


# ============================================================
# TEST CONTENT
# ============================================================

TEST_MATH = '''
<p>Inline math: the chain rule states
<math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><mi>dL</mi><mi>dx</mi></mfrac><mo>=</mo>
<mfrac><mi>dL</mi><mi>dy</mi></mfrac><mo>&#xD7;</mo><mfrac><mi>dy</mi><mi>dh</mi></mfrac><mo>&#xD7;</mo><mfrac><mi>dh</mi><mi>dx</mi></mfrac></math>
which composes derivatives.</p>

<div class="math-block">
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
<mrow><mfrac><mi>dL</mi><mi>dx</mi></mfrac><mo>=</mo>
<mfrac><mi>dL</mi><mi>dy</mi></mfrac><mo>&#xD7;</mo>
<mfrac><mi>dy</mi><mi>dh</mi></mfrac><mo>&#xD7;</mo>
<mfrac><mi>dh</mi><mi>dx</mi></mfrac></mrow>
</math>
</div>

<p>This is a sentence with inline subscript <math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>x</mi><mi>i</mi></msub></math> and superscript <math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>x</mi><mn>2</mn></msup></math> embedded mid-sentence.</p>

<p>The cdot operator with dots: a&#x22C5;b should render as a&#xD7;b (test the substitution).</p>

<h2>Math inside table</h2>
<div class="comparison-table">
<table>
<thead><tr><th>Expression</th><th>Result</th></tr></thead>
<tbody>
<tr><td>Chain rule</td><td><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>x</mi><mi>i</mi></msub></math></td></tr>
<tr><td>Power</td><td><math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>x</mi><mn>2</mn></msup></math></td></tr>
</tbody>
</table>
</div>

<h2>Math inside callout</h2>
<div class="callout note">
  <div class="callout-title">Note</div>
  <p>Within a callout: <math xmlns="http://www.w3.org/1998/Math/MathML"><mi>a</mi><mo>&#xD7;</mo><mi>b</mi></math> should center properly.</p>
</div>
'''

TEST_TABLES = '''
<h2>Narrow table (2 cols)</h2>
<table>
<thead><tr><th>Key</th><th>Value</th></tr></thead>
<tbody>
<tr><td>foo</td><td>bar</td></tr>
<tr><td>baz</td><td>qux</td></tr>
</tbody>
</table>

<h2>Wide comparison table (6 cols)</h2>
<div class="comparison-table">
<div class="comparison-table-title">Track Overview</div>
<table>
<thead><tr><th>Track</th><th>Level</th><th>Duration</th><th>Prerequisites</th><th>Output</th><th>Cost</th></tr></thead>
<tbody>
<tr><td>Basics</td><td>Beginner</td><td>4 weeks</td><td>None</td><td>Cert</td><td>$0</td></tr>
<tr><td>Intermediate</td><td>Some experience</td><td>8 weeks</td><td>Basics</td><td>Project</td><td>$99</td></tr>
<tr><td>Advanced</td><td>Practitioner</td><td>12 weeks</td><td>Intermediate</td><td>Capstone</td><td>$299</td></tr>
<tr><td>Specialist</td><td>Expert</td><td>16 weeks</td><td>Advanced</td><td>Thesis</td><td>$799</td></tr>
<tr><td>Research</td><td>PhD</td><td>52 weeks</td><td>Specialist</td><td>Paper</td><td>$2999</td></tr>
</tbody>
</table>
</div>

<h2>Wide table inside callout (potential atomic split)</h2>
<div class="callout practical-example">
  <div class="callout-title">Track Comparison</div>
  <div class="comparison-table">
  <table>
  <thead><tr><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th></tr></thead>
  <tbody>
  <tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td></tr>
  <tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td></tr>
  <tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td></tr>
  </tbody>
  </table>
  </div>
</div>

<h2>Tall table (must split across pages)</h2>
<div class="comparison-table">
<table>
<thead><tr><th>Row</th><th>Description</th></tr></thead>
<tbody>
''' + '\n'.join(f'<tr><td>Row {i}</td><td>Some long description of row {i} that fills space and makes the table tall.</td></tr>' for i in range(1, 31)) + '''
</tbody>
</table>
</div>
'''

TEST_CODE = '''
<h2>Basic Python code</h2>
<pre><code class="language-python">import torch
import torch.nn as nn

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 1)

    def forward(self, x):
        return self.fc(x)
</code></pre>

<h2>Code with leading blank (was a bug)</h2>
<pre><code class="language-python">
import re

class PIIRedactor:
    """Redact PII from text."""
    PATTERNS = {"email": r"\\b[\\w.+-]+@\\w+\\.\\w+\\b"}
</code></pre>

<h2>Bash code with long lines</h2>
<pre><code class="language-bash">vllm serve TheBloke/Llama-2-70B-Chat-GPTQ --quantization gptq --tensor-parallel-size 2 --max-model-len 4096
docker run --gpus all --shm-size 1g -p 8080:80 -v /data:/data ghcr.io/huggingface/text-generation-inference:latest
</code></pre>

<h2>Mixed code in callout</h2>
<div class="callout tip">
  <div class="callout-title">Tip</div>
  <p>Use the following pattern:</p>
  <pre><code class="language-python">def hello():
    print("world")</code></pre>
</div>
'''

TEST_AUTHOR = '''
<h2>About the Authors</h2>
<div class="author-card">
  <img class="author-photo" src="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22160%22 height=%22160%22%3E%3Crect width=%22160%22 height=%22160%22 fill=%22%23bbb%22/%3E%3Ctext x=%2280%22 y=%2280%22 text-anchor=%22middle%22 fill=%22white%22%3EPhoto%3C/text%3E%3C/svg%3E" alt="Author 1"/>
  <div class="author-info">
    <h3>Alexander Apartsin, Ph.D.</h3>
    <p>Dr. Apartsin holds a Ph.D. in Computer Science from Tel Aviv University, M.Sc. degrees from the Weizmann Institute of Science and NYU Polytechnic, and a B.Sc. from the Technion.</p>
    <p>Before joining academia, he led data science, AI, and research teams across the technology sector, including automotive AI, telecommunications innovation, and financial services. This industry background shaped his research program in Pragmatic AI: the design of AI methods that remain reliable when real-world conditions depart from clean benchmarks and ideal assumptions.</p>
    <p>His teaching focuses on the practical and scientific foundations of modern AI systems. The undergraduate and graduate courses he designed and taught in large language models, AI agents, generative AI, natural language processing, computer vision, and deep learning provided the foundation for this book.</p>
    <div class="author-links">
      <a href="https://example.com">Homepage</a>
    </div>
  </div>
</div>

<div class="author-card">
  <img class="author-photo" src="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22160%22 height=%22160%22%3E%3Crect width=%22160%22 height=%22160%22 fill=%22%23999%22/%3E%3Ctext x=%2280%22 y=%2280%22 text-anchor=%22middle%22 fill=%22white%22%3EPhoto%3C/text%3E%3C/svg%3E" alt="Author 2"/>
  <div class="author-info">
    <h3>Yehudit Aperstein, Ph.D.</h3>
    <p>Dr. Aperstein holds a Ph.D. in Mathematical Economics from the Weizmann Institute and an M.Sc. in Game Theory from the Technion, with postdoctoral work in Financial Mathematics at Bar-Ilan University.</p>
    <p>She founded and directed the M.Sc. Program in Intelligent Systems at Afeka from 2016 to 2023, and in 2024 founded ICSGen.AI, the Afeka Interdisciplinary Center for Social Good and Generative AI.</p>
  </div>
</div>
'''

TEST_CALLOUTS = '''
<h2>All callout types</h2>

<div class="callout note">
  <div class="callout-title">Note</div>
  <p>This is a note. It should render with a soft blue background and an i-icon.</p>
</div>

<div class="callout warning">
  <div class="callout-title">Warning</div>
  <p>This is a warning. It should have a yellow/orange background.</p>
</div>

<div class="callout tip">
  <div class="callout-title">Tip</div>
  <p>This is a tip. Green background.</p>
</div>

<div class="callout big-picture">
  <div class="callout-title">Big Picture</div>
  <p>This is the big picture callout. It explains the high-level concept and should be visually distinctive enough to be noticed at first glance.</p>
</div>

<div class="callout practical-example">
  <div class="callout-title">Practical Example</div>
  <p>Real-world scenario goes here.</p>
</div>

<div class="callout key-takeaway">
  <div class="callout-title">Key Takeaway</div>
  <p>The single most important point.</p>
</div>

<h2>Long callout that should flow across pages</h2>
<div class="callout note">
  <div class="callout-title">Important Long Note</div>
''' + '\n'.join(f'<p>This is paragraph {i} of a long callout. The callout should split across pages when it does not fit on one. Page-break-inside: auto is the test.</p>' for i in range(1, 11)) + '''
</div>
'''

TEST_NAV = '''
<h2>Section Cards</h2>
<ul class="sections-list">
  <li>
    <a href="#" class="section-card">
      <span class="section-num">S.1</span>
      <span class="section-title">vLLM: PagedAttention, Continuous Batching, and OpenAI-Compatible API</span>
    </a>
  </li>
  <li>
    <a href="#" class="section-card">
      <span class="section-num">S.2</span>
      <span class="section-title">Text Generation Inference (TGI): Deployment and Configuration</span>
    </a>
  </li>
  <li>
    <a href="#" class="section-card">
      <span class="section-num">28.1</span>
      <span class="section-title">A short title</span>
    </a>
  </li>
  <li>
    <a href="#" class="section-card">
      <span class="section-num">AB.5</span>
      <span class="section-title">An appendix section with a moderately long title</span>
    </a>
  </li>
</ul>

<h2>Chapter Nav</h2>
<nav class="chapter-nav">
  <a class="prev" href="#">Previous: Some really long previous section name that might overflow</a>
  <a class="up" href="#">Up: Module Index</a>
  <a class="next" href="#">Next: The next section</a>
</nav>
'''


def all_combined():
    """Combined test EPUB."""
    return f'''
{TEST_MATH}
<hr/>
{TEST_TABLES}
<hr/>
{TEST_CODE}
<hr/>
{TEST_AUTHOR}
<hr/>
{TEST_CALLOUTS}
<hr/>
{TEST_NAV}
'''


TESTS = {
    'math': ('Math Rendering Test', TEST_MATH),
    'tables': ('Table Layout Test', TEST_TABLES),
    'code': ('Code Block Test', TEST_CODE),
    'author': ('Author Card Test', TEST_AUTHOR),
    'callouts': ('Callouts Test', TEST_CALLOUTS),
    'navigation': ('Navigation Test', TEST_NAV),
    'combined': ('Combined Test', all_combined()),
}


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if target == 'all':
        for slug, (title, body) in TESTS.items():
            make_epub(slug, title, body)
    elif target in TESTS:
        title, body = TESTS[target]
        make_epub(target, title, body)
    else:
        print(f'Unknown test: {target}')
        print(f'Available: {", ".join(TESTS.keys())} or all')
        sys.exit(1)
