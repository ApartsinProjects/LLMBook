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
            // v13.11: Reverted to 'mathml' (from htmlAndMathml in v13.9).
            // The htmlAndMathml output grew XHTML payload from ~14 MB
            // to ~21 MB, which triggered an opaque "Kindle conversion
            // has encountered an internal error" during MOBI generation
            // in KPV3 -convert. Math typography improvement deferred
            // until either (a) Amazon fixes KFX MOBI builder for large
            // HTML payloads, or (b) we pre-render math to inline SVG.
            //
            // v802 source-side selective conversion (in fix_math_alignment
            // -> simplify_inline_mathml) still converts ~700 simple
            // inline math expressions to plain HTML <sub>/<sup>, which
            // preserves inline flow without MathML rendering quirks.
            const html = katex.renderToString(item.tex, {
                displayMode: !!item.display,
                throwOnError: false,
                output: 'mathml',
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
