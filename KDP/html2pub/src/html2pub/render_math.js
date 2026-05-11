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
            // Output 'mathml' instead of 'html' to avoid the ~400 empty
            // structural <span> elements per chapter (strut/pstrut/vlist/
            // mspace) that KaTeX uses for HTML layout. Kindle's renderer
            // paints those empty spans as visible boxes (tofu) and ignores
            // the inline `vertical-align` styles on the strut, which made
            // inline math float above the surrounding text baseline.
            // MathML is a single semantic <math> element supported natively
            // by EPUB 3 readers (including Kindle KFX conversion).
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
