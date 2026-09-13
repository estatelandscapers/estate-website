#!/usr/bin/env node
/* Estate Landscapers — zero-dependency static build.
   src/pages/**  +  src/partials/**  +  src/layout.html  →  public/**
   Run: node build.js
   Shared chrome (nav, footer, utility bar) lives in ONE partial each — edit once,
   every page changes. Pages carry only their own content and a CONFIG header. */
const fs = require('fs'), path = require('path');
const SRC = path.join(__dirname, 'src');
const OUT = path.join(__dirname, 'public');

const read = f => fs.readFileSync(f, 'utf8');
const partial = n => read(path.join(SRC, 'partials', n + '.html'));

function render(tpl, vars) {
  let prev = null, cur = tpl, guard = 0;
  while (cur !== prev) {
    if (++guard > 12) throw new Error('include loop on ' + vars.PATH);
    prev = cur;
    cur = cur.replace(/\{\{include ([\w-]+)\}\}/g, (_, n) => partial(n));
    cur = cur.replace(/\{\{([A-Z_]+)\}\}/g, (_, k) => {
      if (!(k in vars)) throw new Error('missing {{' + k + '}} on ' + vars.PATH);
      return vars[k];
    });
  }
  return cur;
}

const walk = d => fs.readdirSync(d, { withFileTypes: true })
  .flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);

const layout = read(path.join(SRC, 'layout.html'));
const PHOTOS = [];
const IMAGES = [];
function pageSlug(p) { return p === '/' ? 'home' : p.replace(/^\/|\/$/g, '').replace(/\//g, '-').replace(/\.html$/, ''); }
// Visible breadcrumb trail on pages two or more levels deep. The JSON-LD
// BreadcrumbList already exists on most; this is the human-readable half.
const CRUMB_LABEL = { residential: 'Residential', commercial: 'Commercial', projects: 'Projects',
  insights: 'Insights', areas: 'Service areas', 'retaining-walls': 'Retaining walls' };
function titleise(seg) {
  return CRUMB_LABEL[seg] || seg.replace(/-/g, ' ').replace(/^\w/, ch => ch.toUpperCase());
}
function addCrumbs(html, cpath) {
  const segs = cpath.split('/').filter(Boolean);
  if (segs.length < 2) return html;
  let href = '', items = ['<a href="/">Home</a>'];
  segs.forEach((s, i) => {
    href += '/' + s;
    items.push(i === segs.length - 1
      ? '<span aria-current="page">' + titleise(s) + '</span>'
      : '<a href="' + href + '/">' + titleise(s) + '</a>');
  });
  const nav = '<nav class="crumbs" aria-label="Breadcrumb"><div class="shell">' +
    items.join('<span class="sep" aria-hidden="true">›</span>') + '</div></nav>\n';
  return html.replace('<main id="main">', '<main id="main">\n' + nav);
}

// A card that links to another page shows THAT page's hero photo, so the image
// a visitor clicks is the image they land on. One file, many places, no copies.
// The dark hero plays a silent looping clip when hero-bg.mp4 exists; the still
// stays underneath as the poster and as the fallback for anyone who shouldn't
// or can't have motion.
function heroVideo(html) {
  const dir = path.join(OUT, 'assets', 'img');
  const files = fs.existsSync(dir) ? fs.readdirSync(dir) : [];
  const vid = files.find(f => /^hero-bg\.(mp4|webm)$/i.test(f));
  if (!vid) return html;
  const still = files.find(f => /^hero-bg\.(jpe?g|png|webp)$/i.test(f));
  const tag = '<video class="herovid" muted loop playsinline preload="none" aria-hidden="true"' +
    (still ? ' poster="/assets/img/' + still + '"' : '') + '>' +
    '<source src="/assets/img/' + vid + '" type="video/' + (/webm$/i.test(vid) ? 'webm' : 'mp4') +
    '"></video>';
  return html.replace('<div class="bg" aria-hidden="true"></div>',
    '<div class="bg" aria-hidden="true"></div>' + tag);
}

function heroFileFor(target) {
  const dir = path.join(OUT, 'assets', 'img');
  const all = fs.existsSync(dir) ? fs.readdirSync(dir) : [];
  const slug = pageSlug(target);
  const names = [slug + '-hero', slug + '-1'];
  if (target.startsWith('/projects/')) names.unshift('project-' + slug.replace(/^projects-/, '') + '-hero');
  for (const n of names) {
    const f = all.find(f => { const m = f.match(/^(.+?)(?:--.+)?\.(webp|jpe?g|png)$/i); return m && m[1] === n; });
    if (f) return f;
    if (PHOTO_MAP[n]) {
      const t = PHOTO_MAP[n].replace(/^\/?(assets\/img\/)?/, '');
      if (fs.existsSync(path.join(dir, t))) return t;
    }
  }
  return null;
}
function heroImg(file, fallbackAlt) {
  const words = (file.match(/--(.+)\.\w+$/) || [])[1];
  const alt = words ? words.replace(/-/g, ' ').replace(/^\w/, c => c.toUpperCase()) : (fallbackAlt || '');
  return '<img src="/assets/img/' + file + '" alt="' + alt.replace(/"/g, '&quot;') + '" loading="lazy" decoding="async">';
}
function cardHeroes(html) {
  const heroOf = heroFileFor;
  // explicit: <div class="plate" data-hero="/projects/x/"></div>
  html = html.replace(/<div class="plate" data-hero="(\/[^"]+)"[^>]*>[\s\S]*?<\/div>/g, (m, href) => {
    const file = heroOf(href);
    return file ? '<div class="plate">' + heroImg(file) + '</div>' : m;
  });
  // cards with no plate at all: give project cards one
  html = html.replace(/<a class="card" href="(\/projects\/[^"#]+)"([^>]*)>(\s*<div class="in">)/g, (m, href, attrs, inner) => {
    const file = heroOf(href);
    return file ? '<a class="card" href="' + href + '"' + attrs + '><div class="plate">' + heroImg(file) + '</div>' + inner : m;
  });
  return html.replace(/<a class="card" href="(\/[^"#]+)"([^>]*)>([\s\S]*?)<\/a>/g, (m, href, attrs, inner) => {
    if (!/<div class="slot">/.test(inner)) return m;
    const file = heroOf(href);
    if (!file) return m;
    return '<a class="card" href="' + href + '"' + attrs + '>' +
      inner.replace(/<div class="slot"[^>]*>[\s\S]*?<\/div>/, heroImg(file)) + '</a>';
  });
}

// A slot file ending .mp4/.webm renders as a silent looping video with the
// matching still (same name, image extension) as its poster. Autoplay only
// happens muted and inline, which every browser allows, and the whole thing is
// skipped for reduced-motion or data-saver visitors by site.js.
function videoTag(file, alt) {
  const stem = file.replace(/\.(mp4|webm)$/i, '');
  const dir = path.join(OUT, 'assets', 'img');
  const poster = ['jpg', 'jpeg', 'webp', 'png']
    .map(e => stem + '.' + e).find(f => fs.existsSync(path.join(dir, f)));
  return '<video class="slotvid" muted loop playsinline preload="metadata" ' +
    (poster ? 'poster="/assets/img/' + poster + '" ' : '') +
    'aria-label="' + alt.replace(/"/g, '&quot;') + '">' +
    '<source src="/assets/img/' + file + '" type="video/' +
    (/\.webm$/i.test(file) ? 'webm' : 'mp4') + '"></video>';
}

function swapPhotos(html, cpath) {
  html = cardHeroes(html);
  const slug = pageSlug(cpath);
  let i = 0;
  return html.replace(/<div class="slot"(?:\s+data-key="([^"]+)")?>([\s\S]*?)<\/div>/g, (m, key, inner) => {
    i++;
    const legacy = slug + '-' + i;
    const name = key || (i === 1 ? slug + '-hero' : legacy);
    const desc = ((inner.match(/<span>([\s\S]*?)<\/span>/) || [,''])[1] || '')
      .replace(/<br\s*\/?\s*>/g, ' ').replace(/\s+/g, ' ').trim();
    const dir = path.join(OUT, 'assets', 'img');
    const all = fs.existsSync(dir) ? fs.readdirSync(dir) : [];
    // 1. a file named for the slot itself
    const candidates = [name, name.replace(/-hero$/, '-1'), legacy];
    const byName = n => all.find(f => {
      const m2 = f.match(/^(.+?)(?:--.+)?\.(webp|jpe?g|png|mp4|webm)$/i);
      return m2 && m2[1] === n;
    });
    let file = null;
    for (const n of candidates) { file = byName(n); if (file) break; }
    // REUSE: data/photo-map.json maps a key to any existing file — one photo, many places.
    if (!file) for (const n of candidates) {
      if (!PHOTO_MAP[n]) continue;
      const target = PHOTO_MAP[n].replace(/^\/?(assets\/img\/)?/, '');
      if (fs.existsSync(path.join(dir, target))) { file = target; break; }
      console.warn('  photo-map: ' + n + ' → ' + target + ' (file not found)');
    }
    PHOTOS.push({ page: cpath, name: name, desc: desc, done: !!file, file: file || null });
    if (!file) return m;
    const words = (file.match(/--(.+)\.\w+$/) || [])[1];
    const alt = words ? words.replace(/-/g, ' ').replace(/^\w/, c => c.toUpperCase()) : desc;
    if (/\.(mp4|webm)$/i.test(file)) return videoTag(file, alt);
    IMAGES.push({ page: cpath, src: '/assets/img/' + file, alt: alt });
    const load = i === 1 ? ' fetchpriority="high"' : ' loading="lazy"';
    return '<img src="/assets/img/' + file + '" alt="' + alt.replace(/"/g, '&quot;') + '"' + load + '>';
  });
}
const BUILT = [];
const STAMP = new Date().toISOString().slice(0, 16) + 'Z';
const MAP_PATH = path.join(__dirname, 'data', 'photo-map.json');
const PHOTO_MAP = fs.existsSync(MAP_PATH) ? JSON.parse(fs.readFileSync(MAP_PATH, 'utf8')) : {};
const SITEMAP_PATHS = [];
let n = 0;
for (const f of walk(path.join(SRC, 'pages'))) {
  const s = read(f);
  const m = s.match(/^<!--CONFIG\s*([\s\S]*?)-->\s*/);
  if (!m) throw new Error('no CONFIG header in ' + f);
  const c = JSON.parse(m[1]);
  const body = s.slice(m[0].length);
  const vars = {
    TITLE: c.title || '', DESC: c.description || '', PATH: c.path,
    PAGE_URL: 'https://www.estatelandscapers.com.au' + c.path,
    NAV: c.nav ? '{{include nav-' + c.nav + '}}' : '',
    ROBOTS: c.noindex ? '<meta name="robots" content="noindex">' : '',
    FOOTER: c.footer ? '{{include footer-' + c.footer + '}}' : '',
    BODY: body
  };
  let html = c.raw ? render(body, vars) : render(layout, vars);
  if (['/residential/quote/', '/commercial/tender/', '/contact/'].includes(c.path))
    html = html.replace('<body', '<body class="noform"');
  if (c.path.startsWith('/projects/'))
    html = html.replace(/\s*<a class="hd-switch hd-portfolio"[\s\S]*?<\/a>/, '');
  if (c.path === '/') html = heroVideo(html);
  html = addCrumbs(html, c.path);
  html = swapPhotos(html, c.path);
  html = html.replace(/<span class="ctile" data-logo="([^"]+)">([^<]+)<\/span>/g, (m, slug, name) => {
    const ext = ['svg', 'png', 'webp'].find(e => fs.existsSync(path.join(OUT, 'assets', 'img', 'councils', slug + '.' + e)));
    return ext ? '<span class="ctile"><img src="/assets/img/councils/' + slug + '.' + ext + '" alt="' + name + '" loading="lazy"></span>' : m;
  });
  // Cache-busting: assets carry the build stamp, so a deploy is visible instantly
  // even though assets themselves are cached for speed.
  html = html.replace(/\/assets\/(site\.css|site\.js|enquiry\.js)(?!\?)/g,
    '/assets/$1?v=' + STAMP.replace(/[^0-9]/g, ''));
  html = html.replace('</html>', '<!-- estate build ' + STAMP + ' · ' + c.path + ' -->\n</html>');
  if (!global.__built) global.__built = new Set();
  if (global.__built.has(c.path)) throw new Error('DUPLICATE PAGE PATH: ' + c.path + ' built twice (second source: ' + f + ')');
  global.__built.add(c.path);
  const out = c.path.endsWith('.html')
    ? path.join(OUT, c.path.replace(/^\//, ''))
    : path.join(OUT, c.path.replace(/^\//, ''), 'index.html');
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, html);
  BUILT.push(out.replace(OUT, ''));
  console.log('built ' + c.path);
  if (!c.path.endsWith('.html') && !c.noindex) SITEMAP_PATHS.push(c.path);
  n++;
}
// ---- sanity: the build must contain a homepage, and no two pages may share a path
if (!fs.existsSync(path.join(OUT, 'index.html')))
  throw new Error('BUILD FAILED SANITY CHECK: public/index.html was not produced — the homepage is missing.');
SITEMAP_PATHS.sort();
const today = new Date().toISOString().slice(0, 10);
fs.writeFileSync(path.join(OUT, 'sitemap.xml'),
  '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' +
  SITEMAP_PATHS.map(p => {
    const imgs = IMAGES.filter(x => x.page === p).map(x =>
      '    <image:image><image:loc>https://www.estatelandscapers.com.au' + x.src + '</image:loc></image:image>').join('\n');
    return '  <url><loc>https://www.estatelandscapers.com.au' + p + '</loc><lastmod>' + today + '</lastmod>' +
      (imgs ? '\n' + imgs + '\n  ' : '') + '</url>';
  }).join('\n') + '\n</urlset>\n');
console.log(n + ' pages built into public/ · sitemap.xml: ' + SITEMAP_PATHS.length + ' URLs');
// PHOTOS.md — the live shot list: regenerated every build, ticks itself off
const byPage = {};
PHOTOS.forEach(p => { (byPage[p.page] = byPage[p.page] || []).push(p); });
let md = '# Photo slots — the shot list\n\n';
md += 'Save an image as `public/assets/img/<name>.jpg` (or .webp/.png), push, and it\n';
md += 'appears in its slot automatically on the next build. This file regenerates on\n';
md += 'every build and ticks itself: ' + PHOTOS.filter(p => p.done).length + ' of ' + PHOTOS.length + ' slots filled.\n\n';
md += 'Best size: 1600px wide, JPG/WebP, under 400 KB (squoosh.app does this in-browser).\n';
md += 'Height is flexible — every slot crops to fit, so keep the subject centred.\n';
md += 'Exact shapes if you want them: heroes and homepage rows ~1600x1200, service\n';
md += 'cards ~1600x1000, the two homepage doors ~1600x900 (subject mid-frame; text\n';
md += 'overlays the bottom), and ONLY the four \"Recent post\" slots are square (1200x1200).\n\n';
md += 'SEO NAMING: keep the slot key, then add real words after a double dash:\n';
md += '  home-2--engineered-retaining-wall-piers-kellyville.jpg\n';
md += 'The words become the alt text and travel into Google Images. Filled slots are\n';
md += 'added to the image sitemap automatically.\n\n';
Object.keys(byPage).sort().forEach(pg => {
  md += '## ' + pg + '\n\n';
  byPage[pg].forEach(p => {
    md += '- [' + (p.done ? 'x' : ' ') + '] `' + p.name + '.jpg` — ' + (p.desc || 'see page') + '\n';
  });
  md += '\n';
});
fs.writeFileSync(path.join(__dirname, 'PHOTOS.md'), md);
console.log('PHOTOS.md: ' + PHOTOS.filter(p => p.done).length + '/' + PHOTOS.length + ' slots filled');

// ---- OVERSIZE ASSET SHIELD ------------------------------------------------
// Cloudflare Workers refuses any single asset over 25 MiB and fails the whole
// deploy. Raw camera files sometimes land in public/assets/img; rather than
// block the site, list anything oversized (or obviously unused and huge) in
// .assetsignore so wrangler skips it. Nothing is deleted from the repo.
(function oversizeShield() {
  const LIMIT = 20 * 1024 * 1024;               // 20 MiB, safely under the 25 MiB ceiling
  const skip = [];
  (function walk(dir, rel) {
    if (!fs.existsSync(dir)) return;
    for (const f of fs.readdirSync(dir)) {
      const full = path.join(dir, f), r = rel ? rel + '/' + f : f;
      const st = fs.statSync(full);
      if (st.isDirectory()) walk(full, r);
      else if (st.size > LIMIT) skip.push({ path: r, mb: (st.size / 1048576).toFixed(1) });
    }
  })(path.join(OUT, 'assets'), 'assets');
  const ignorePath = path.join(OUT, '.assetsignore');
  if (skip.length) {
    fs.writeFileSync(ignorePath, skip.map(s => s.path).join('\n') + '\n');
    console.warn('  WARNING: skipping ' + skip.length + ' oversized asset(s) — over Cloudflare\'s 25 MiB limit:');
    skip.forEach(s => console.warn('    - /' + s.path + '  (' + s.mb + ' MB)'));
    console.warn('  These are excluded from the deploy via .assetsignore. Resize or remove them.');
  } else if (fs.existsSync(ignorePath)) {
    fs.unlinkSync(ignorePath);
  }
})();

// ---- HERO RESOLVER + ASSET WARNINGS ---------------------------------------
// The hero background has repeatedly gone missing or arrived under a slightly
// different name (hero-bg.jpg.jpg, .JPG, .jpeg). Rather than fail the deploy,
// find whatever hero-bg.* actually exists and point the CSS at it. If none
// exists, warn loudly and let the site ship: the hero falls back to its navy
// treatment, which still looks deliberate.
// ---- STALE PAGE CLEANUP ---------------------------------------------------
// public/ is committed, so pages deleted from src/ used to linger and keep
// serving (and duplicating titles). Remove any built page not produced by this
// run. Assets are never touched.
(function stale() {
  const keep = new Set(BUILT.map(p => path.join(OUT, p.replace(/^\//, ''))));
  const removed = [];
  (function walk(dir) {
    for (const f of fs.readdirSync(dir)) {
      const full = path.join(dir, f);
      if (fs.statSync(full).isDirectory()) {
        if (f === 'assets') continue;
        walk(full);
        if (!fs.readdirSync(full).length) fs.rmdirSync(full);
      } else if (/index\.html$/.test(f) && !keep.has(full)) {
        fs.unlinkSync(full); removed.push(full.replace(OUT, ''));
      }
    }
  })(OUT);
  if (removed.length) {
    console.log('removed ' + removed.length + ' stale page(s): ' + removed.slice(0, 6).join(', ') +
      (removed.length > 6 ? ' …' : ''));
  }
})();

(function imageWeights() {
  const dir = path.join(OUT, 'assets', 'img');
  if (!fs.existsSync(dir)) return;
  const heavy = [];
  (function walk(d, rel) {
    for (const f of fs.readdirSync(d)) {
      const full = path.join(d, f);
      const st = fs.statSync(full);
      if (st.isDirectory()) walk(full, rel + f + '/');
      else if (/\.(jpe?g|png|webp)$/i.test(f) && st.size > 500 * 1024)
        heavy.push({ f: rel + f, kb: Math.round(st.size / 1024) });
    }
  })(dir, '');
  if (heavy.length) {
    console.warn('  ' + heavy.length + ' image(s) over 500 KB — these are what make pages feel slow:');
    heavy.sort((a, b2) => b2.kb - a.kb).slice(0, 12)
      .forEach(h => console.warn('    - ' + h.f + '  ' + h.kb + ' KB'));
    console.warn('  Target 1600px wide and under 400 KB (squoosh.app).');
  }
})();

(function heroResolve() {
  const dir = path.join(OUT, 'assets', 'img');
  const cssPath = path.join(OUT, 'assets', 'site.css');
  let css = fs.readFileSync(cssPath, 'utf8');
  const files = fs.existsSync(dir) ? fs.readdirSync(dir) : [];
  const heroVid = files.find(f => /^hero-bg\.(mp4|webm)$/i.test(f));
  const hero = files.find(f => /^hero-bg\.(jpe?g|png|webp)$/i.test(f))
            || files.find(f => /^hero-bg\.(?!mp4|webm)/i.test(f));
  if (heroVid) console.log('hero video present: /assets/img/' + heroVid + (hero ? '' : '  (no still poster — add hero-bg.jpg)'));
  const cur = (css.match(/url\('\/assets\/img\/(hero-bg[^'?]*)/) || [])[1];
  if (hero) {
    if (hero !== cur) {
      css = css.replace(/url\('\/assets\/img\/hero-bg[^']*'\)/g,
        "url('/assets/img/" + hero + "?v=" + STAMP.replace(/[^0-9]/g, '') + "')");
      fs.writeFileSync(cssPath, css);
      console.log('hero image resolved: /assets/img/' + hero + (cur ? '  (CSS had ' + cur + ')' : ''));
    } else {
      console.log('hero image present: /assets/img/' + hero);
    }
  } else {
    console.warn('');
    console.warn('  WARNING: no hero-bg.* in public/assets/img/ — the home page hero will');
    console.warn('  fall back to its navy treatment. Upload the image to fix.');
    console.warn('');
  }
  const refs = new Set();
  for (const m of css.matchAll(/url\('?\/(assets\/[^')?]+)/g)) refs.add(m[1]);
  const missing = [...refs].filter(r => !fs.existsSync(path.join(OUT, r)));
  if (missing.length) {
    console.warn('  WARNING: referenced assets not found (deploy continues):');
    missing.forEach(m => console.warn('    - /' + m));
  }
})();
