/*
 * render_math.js — batch KaTeX server-side renderer
 *
 * Reads a JSON array of math expressions from stdin:
 *   [{"id": "0", "tex": "x^2", "display": false}, ...]
 *
 * Writes a JSON array of rendered HTML to stdout:
 *   [{"id": "0", "html": "<span class=\"katex\">...</span>"}, ...]
 *
 * On parse error: {"id": "0", "html": "<original tex>", "error": "..."}
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
            const html = katex.renderToString(item.tex, {
                displayMode: !!item.display,
                throwOnError: false,
                /* v15.13 (final): output: 'mathml' is the documented
                 * Kindle path. Per KDP "Enhanced Typesetting" support page
                 * (https://kdp.amazon.com/en_US/help/topic/G202087570) and
                 * the Kindle Publishing Guidelines, Kindle's KFX converter
                 * applies its OWN typesetter to MathML elements. Custom
                 * CSS on MathML is largely ignored.
                 *
                 * `htmlAndMathml` causes Kindle's converter to consume the
                 * MathML AND keep the KaTeX HTML, leading to duplicated
                 * visual rendering (math appears twice). Use `mathml` only. */
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
