// Render SVG to PNG using puppeteer (bundled with @mermaid-js/mermaid-cli).
// Usage: node svg_to_png.cjs <input.svg> <output.png> [width]
const path = require('path');
const fs = require('fs');

const MERMAID_NM = 'C:/Users/apart/AppData/Roaming/npm/node_modules/@mermaid-js/mermaid-cli/node_modules';
const puppeteer = require(path.join(MERMAID_NM, 'puppeteer'));

(async () => {
  const [, , svgPath, pngPath, widthStr] = process.argv;
  if (!svgPath || !pngPath) {
    console.error('Usage: node svg_to_png.cjs <input.svg> <output.png> [width]');
    process.exit(1);
  }
  const width = parseInt(widthStr || '1400', 10);

  const svg = fs.readFileSync(svgPath, 'utf8');
  // Wrap SVG in HTML so puppeteer can render with proper dimensions
  const html = `<!doctype html><html><head><style>
    body { margin: 0; padding: 0; background: white; }
    svg { display: block; width: ${width}px; height: auto; background: white; }
  </style></head><body>${svg}</body></html>`;

  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: width + 20, height: 1200, deviceScaleFactor: 2 });
  await page.setContent(html, { waitUntil: 'networkidle0' });
  const svgEl = await page.$('svg');
  const box = await svgEl.boundingBox();
  await svgEl.screenshot({ path: pngPath, omitBackground: false, clip: { x: box.x, y: box.y, width: box.width, height: box.height } });
  await browser.close();
  console.log(`wrote ${pngPath}`);
})();
