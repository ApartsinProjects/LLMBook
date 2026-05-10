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
            const html = katex.renderToString(item.tex, {
                displayMode: !!item.display,
                throwOnError: false,
                output: 'html',
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
