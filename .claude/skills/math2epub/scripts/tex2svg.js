// Batch convert LaTeX math expressions to SVG via MathJax (Node).
//
// Reads JSON from stdin: [{"id": "0", "tex": "x^2", "display": false}, ...]
// Writes JSON to stdout : [{"id": "0", "svg": "<svg>...</svg>"}, ...]
//
// On parse error: {"id": "0", "svg": "", "error": "..."}
//
// Owned by the math2epub skill. The canonical copy lives at
//   .claude/skills/math2epub/scripts/tex2svg.js
// in the LLMBook repo, mirrored via NTFS junction to
//   C:/Users/apart/.claude/skills/math2epub/scripts/tex2svg.js
//
// Module resolution: requires `mathjax-full` reachable via NODE_PATH or
// via standard node_modules lookup. The default install location used by
// render_svg.py is `E:/Tools/mathjax/node_modules`. Override by setting
// the MATH2EPUB_MATHJAX env var to a directory that contains node_modules.

require('mathjax-full/js/util/asyncLoad/node.js');
const {mathjax} = require('mathjax-full/js/mathjax.js');
const {TeX} = require('mathjax-full/js/input/tex.js');
const {SVG} = require('mathjax-full/js/output/svg.js');
const {liteAdaptor} = require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('mathjax-full/js/handlers/html.js');
const {AllPackages} = require('mathjax-full/js/input/tex/AllPackages.js');

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);

const tex = new TeX({packages: AllPackages});
const svg = new SVG({
    // fontCache:'none' = each glyph's <path d="..."> is drawn directly,
    // no <defs>/<use xlink:href="..."/> indirection. Kindle Previewer 3
    // strips <defs> but keeps the <use> references, which then resolve
    // to nothing. See LESSONS.md L2 in the math2epub skill for details.
    fontCache: 'none',
    // scale 1.8 makes the intrinsic SVG dimensions match body-font
    // height. The user-visible result is that an inline math fragment
    // like `y_i` reads at the same height as the surrounding text,
    // instead of looking like a tiny subscript image.
    scale: 1.8,
    exFactor: 0.5,
    mtextInheritFont: false,
    displayAlign: 'center',
    displayIndent: '0',
});
const doc = mathjax.document('', {InputJax: tex, OutputJax: svg});

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
    let items;
    try {
        items = JSON.parse(input);
    } catch (e) {
        console.error('JSON parse error:', e.message);
        process.exit(1);
    }
    const out = items.map(item => {
        try {
            // em: base font size in pixels for layout calculations.
            // 24 instead of the default 16 produces larger SVG width/
            // height attributes (which Kindle interprets as physical
            // pixel sizes). The 1ex=12px conversion in render_svg.py
            // relies on this em:24, ex:12 pairing.
            const node = doc.convert(item.tex, {
                display: !!item.display,
                em: 24,
                ex: 12,
                containerWidth: 80 * 24,
            });
            const svgOutput = adaptor.innerHTML(node);
            return {id: item.id, svg: svgOutput};
        } catch (e) {
            return {id: item.id, svg: '', error: e.message};
        }
    });
    process.stdout.write(JSON.stringify(out));
});
