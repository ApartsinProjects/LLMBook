// Validate every $...$ and $$...$$ math block in shipped HTML using KaTeX.
// Output: file:line  [kind] error  expr  for each defect.
// Exit code 1 if any defect found.
//
// Usage: node KDP/build/_v654_validate_math.cjs

const fs = require('fs');
const path = require('path');

const KATEX_PATH = 'C:/Users/apart/AppData/Roaming/npm/node_modules/@mermaid-js/mermaid-cli/node_modules/katex';
const katex = require(KATEX_PATH);

const ROOT = path.resolve(__dirname, '..', '..');
const SKIP_FRAGMENTS = ['node_modules', '.git/', 'pagefind/', 'KDP/build/',
  'KDP/output/', 'templates/', '_archive/', 'temp_epub/'];

function* walkHtml(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    const rel = path.relative(ROOT, full).replace(/\\/g, '/');
    if (SKIP_FRAGMENTS.some(s => rel.includes(s))) continue;
    if (entry.isDirectory()) yield* walkHtml(full);
    else if (entry.name.endsWith('.html')) yield full;
  }
}

function lineOf(text, idx) {
  return text.slice(0, idx).split('\n').length;
}

function decodeEntities(s) {
  return s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ');
}

function isLikelyMath(s) {
  if (s.includes('\\')) return true;
  if (/[_^{}]/.test(s)) return true;
  return false;
}

function tryRender(expr, displayMode) {
  try {
    katex.renderToString(decodeEntities(expr), { displayMode, throwOnError: true, strict: 'error' });
    return null;
  } catch (e) {
    return String(e.message || e).split('\n')[0].slice(0, 200);
  }
}

const DISPLAY_RE = /\$\$([\s\S]+?)\$\$/g;
const INLINE_RE = /(?<!\$)\$([^$\n]{2,200}?)\$(?!\$)/g;

let totalBlocks = 0;
let totalErrors = 0;
const errorFiles = new Set();

// Strip <pre>...</pre> and <code>...</code> blocks (KaTeX auto-render skips these
// per the standard ignoredTags config), and strip any backslash-escaped \$
// (treated as literal dollar by KaTeX, not a delimiter).
function stripIgnored(text) {
  return text
    .replace(/<pre[\s\S]*?<\/pre>/g, m => ' '.repeat(m.length))
    .replace(/<code[\s\S]*?<\/code>/g, m => ' '.repeat(m.length))
    .replace(/\\\$/g, '  ');  // \$ becomes two spaces (preserves offsets)
}

for (const file of walkHtml(ROOT)) {
  const rawText = fs.readFileSync(file, 'utf8');
  const text = stripIgnored(rawText);
  const rel = path.relative(ROOT, file).replace(/\\/g, '/');
  const local = [];

  // Display blocks
  let m;
  DISPLAY_RE.lastIndex = 0;
  while ((m = DISPLAY_RE.exec(text)) !== null) {
    const expr = m[1].trim();
    if (!isLikelyMath(expr)) continue;
    totalBlocks++;
    const err = tryRender(expr, true);
    if (err) local.push([lineOf(text, m.index), 'display', err, expr.slice(0, 100)]);
  }

  // Strip display blocks then scan inline
  const noDisplay = text.replace(DISPLAY_RE, m => ' '.repeat(m.length));
  INLINE_RE.lastIndex = 0;
  while ((m = INLINE_RE.exec(noDisplay)) !== null) {
    const expr = m[1].trim();
    if (!isLikelyMath(expr)) continue;
    totalBlocks++;
    const err = tryRender(expr, false);
    if (err) local.push([lineOf(text, m.index), 'inline', err, expr.slice(0, 100)]);
  }

  if (local.length) {
    errorFiles.add(rel);
    local.sort((a, b) => a[0] - b[0]);
    for (const [line, kind, err, snip] of local) {
      const safeSnip = snip.replace(/[^\x20-\x7e]/g, '?');
      console.log(`${rel}:${line}  [${kind}] ${err}`);
      console.log(`    expr: ${safeSnip}`);
      totalErrors++;
    }
  }
}

console.log();
console.log(`Validated ${totalBlocks} math blocks. Errors: ${totalErrors} across ${errorFiles.size} file(s).`);
process.exit(totalErrors ? 1 : 0);
