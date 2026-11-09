// Generates responsive WebP derivatives for every photo and logo under public/assets/
// into public/assets/img/r/<stem>-<width>.webp. Run after adding or replacing photos:
//   node tools/make-derivatives.js
// Widths never exceed the original. Existing derivatives are skipped unless the source is newer.
// build.js (and tools/responsive-html.js) rewrite <img> tags to use these when they exist.
const fs = require('fs'), path = require('path');
const sharp = require(process.env.SHARP_PATH || 'sharp');
const IMG = path.join(__dirname, '..', 'public', 'assets', 'img');
const OUT = path.join(IMG, 'r');
const LOGOS = path.join(__dirname, '..', 'public', 'assets');
const WIDTHS = [480, 800, 1200];          // photos: largest display is ~700 CSS px, 1200 covers 2x
const HERO_WIDTHS = [800, 1200, 1600, 1920]; // the full-bleed home background only
fs.mkdirSync(OUT, { recursive: true });
async function run() {
  const srcs = fs.readdirSync(IMG).filter(f => /\.(jpe?g|png)$/i.test(f)).map(f => path.join(IMG, f))
    .concat(fs.readdirSync(LOGOS).filter(f => /^logo-.*\.png$/i.test(f)).map(f => path.join(LOGOS, f)));
  let made = 0, kept = 0;
  for (const src of srcs) {
    const stem = path.basename(src).replace(/\.(jpe?g|png)$/i, '');
    const meta = await sharp(src).metadata();
    const want = /^hero-bg$/.test(stem) ? HERO_WIDTHS : /^logo-/.test(stem) ? [480] : WIDTHS;
    const widths = want.filter(w => w <= meta.width);
    if (!widths.length) widths.push(meta.width);
    for (const w of widths) {
      const out = path.join(OUT, `${stem}-${w}.webp`);
      if (fs.existsSync(out) && fs.statSync(out).mtimeMs >= fs.statSync(src).mtimeMs) { kept++; continue; }
      await sharp(src).resize({ width: w, withoutEnlargement: true }).webp({ quality: /^logo-/.test(stem) ? 90 : 72, effort: 5 }).toFile(out);
      made++;
    }
  }
  console.log(`derivatives: ${made} written, ${kept} up to date, in public/assets/img/r/`);
}
run().catch(e => { console.error(e); process.exit(1); });
