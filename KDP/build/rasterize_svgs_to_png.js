/**
 * Bulk SVG-to-PNG rasterizer using sharp.
 *
 * Reads all .svg files in images/svg-rasterized/, produces PNG
 * versions in images/svg-rasterized/png/, and emits a JSON mapping
 * from svg filename to png filename so a follow-on Python script can
 * rewrite <img src=...> references in source HTML.
 *
 * Run from project root:
 *   node KDP/build/rasterize_svgs_to_png.js
 *
 * Requires:
 *   npm install sharp     (locally in project node_modules/)
 */
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const SVG_DIR = 'images/svg-rasterized';
const PNG_DIR = 'images/svg-rasterized/png';
const MAP_OUT = 'images/svg-rasterized/png_map.json';

// Target render width. PNGs render at 2x device pixels for crispness;
// the <img width/height> attrs (computed in the HTML-update step) will
// halve the displayed dims so the visual size matches the original SVG.
const TARGET_WIDTH = 1600;

if (!fs.existsSync(PNG_DIR)) {
  fs.mkdirSync(PNG_DIR, { recursive: true });
}

const svgs = fs.readdirSync(SVG_DIR).filter(f => f.endsWith('.svg'));
console.log(`Found ${svgs.length} SVGs to rasterize`);

const mapping = {};
let ok = 0, failed = 0;

async function rasterize() {
  for (const svg of svgs) {
    const inPath = path.join(SVG_DIR, svg);
    const outName = svg.replace(/\.svg$/, '.png');
    const outPath = path.join(PNG_DIR, outName);

    // Skip if PNG already exists and is newer than source SVG (idempotent)
    if (fs.existsSync(outPath)) {
      const srcMtime = fs.statSync(inPath).mtimeMs;
      const dstMtime = fs.statSync(outPath).mtimeMs;
      if (dstMtime >= srcMtime) {
        mapping[svg] = outName;
        ok++;
        continue;
      }
    }

    try {
      const meta = await sharp(inPath).metadata();
      // Honor SVG natural width if smaller than TARGET_WIDTH (avoid upscaling)
      const targetW = meta.width && meta.width < TARGET_WIDTH ? meta.width * 2 : TARGET_WIDTH;
      const info = await sharp(inPath, { density: 192 })
        .resize({ width: targetW, withoutEnlargement: false })
        .png({ quality: 90, compressionLevel: 9 })
        .toFile(outPath);
      mapping[svg] = outName;
      ok++;
      if (ok % 50 === 0) console.log(`  ${ok}/${svgs.length} rasterized`);
    } catch (e) {
      console.error(`  FAIL ${svg}: ${e.message}`);
      failed++;
    }
  }

  fs.writeFileSync(MAP_OUT, JSON.stringify(mapping, null, 2));
  console.log(`\nDone. ok=${ok} failed=${failed} mapping_file=${MAP_OUT}`);
}

rasterize().catch(e => { console.error(e); process.exit(1); });
