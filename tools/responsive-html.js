// Gives every <img> that has WebP derivatives (public/assets/img/r/, made by
// tools/make-derivatives.js) a srcset and sizes, so phones download a 480 px WebP instead
// of a 1,400 px JPEG. The original src stays as the fallback. Used by build.js on every
// page, and runnable on its own over public/ after the derivatives change:
//   node tools/responsive-html.js
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..', 'public');
const R = path.join(ROOT, 'assets', 'img', 'r');
let cache = null;
function derivatives() {
  if (cache) return cache;
  cache = {};
  if (!fs.existsSync(R)) return cache;
  for (const f of fs.readdirSync(R)) {
    const m = f.match(/^(.+)-(\d+)\.webp$/); if (!m) continue;
    (cache[m[1]] = cache[m[1]] || []).push(+m[2]);
  }
  for (const k in cache) cache[k].sort((a, b) => a - b);
  return cache;
}
function responsiveImages(html) {
  const d = derivatives();
  return html.replace(/<img\b([^>]*?)\bsrc="(\/assets\/(?:img\/)?([^"\/?]+)\.(?:jpe?g|png))(\?[^"]*)?"([^>]*)>/gi, (m, pre, src, stem, q, post) => {
    if (/\bsrcset=/.test(pre + post)) return m;
    const ws = d[stem]; if (!ws || !ws.length) return m;
    const isLogo = /^logo-/.test(stem);
    const srcset = ws.map(w => `/assets/img/r/${stem}-${w}.webp ${w}w`).join(', ');
    const sizes = isLogo ? '(max-width: 900px) 52vw, 240px' : '(max-width: 760px) 100vw, (max-width: 1100px) 50vw, 640px';
    return `<img${pre}src="${src}${q || ''}" srcset="${srcset}" sizes="${sizes}"${post}>`;
  });
}
module.exports = { responsiveImages };
if (require.main === module) {
  const walk = dir => fs.readdirSync(dir, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(dir, e.name)) : e.name.endsWith('.html') ? [path.join(dir, e.name)] : []);
  let n = 0;
  for (const f of walk(ROOT)) { const s = fs.readFileSync(f, 'utf8'); const t = responsiveImages(s); if (t !== s) { fs.writeFileSync(f, t); n++; } }
  console.log('responsive images: ' + n + ' pages updated');
}
