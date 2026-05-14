/*
 * render_math.js - batch KaTeX server-side renderer
 *
 * Reads JSON from stdin: [{id, tex, display}]
 * Writes JSON to stdout: [{id, html}]
 */
const katex = require('katex');

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
            // v13.9: Switched from 'mathml' to 'htmlAndMathml' — ships
            // BOTH KaTeX HTML (positioned glyphs, high-quality typography)
            // AND MathML (semantic, accessibility). Visual EPUB readers
            // use the HTML rendering (proper italic variables, operator
            // spacing, fraction stacking). Kindle KFX / screen readers
            // can use MathML semantics.
            //
            // Previous concern: the ~400 empty `vlist-s` / strut spans
            // KaTeX HTML emits used to render as visible "tofu" boxes
            // on older Kindles. v789 hook (fix_math_alignment) strips
            // these empty spans before EPUB packaging, so the issue is
            // resolved.
            //
            // File-size impact: +1.1 MB to a 32.8 MB EPUB (3% growth).
            const html = katex.renderToString(item.tex, {
                displayMode: !!item.display,
                throwOnError: false,
                output: 'htmlAndMathml',
                strict: 'ignore',
                trust: false,
            });
            return { id: item.id, html: html };
        } catch (e) {
            return { id: item.id, html: item.tex, error: e.message };
        }
    });
    process.stdout.write(JSON.stringify(out));
});
