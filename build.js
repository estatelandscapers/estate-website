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
const STAMP = new Date().toISOString().slice(0, 16) + 'Z';
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
  html = html.replace('</html>', '<!-- estate build ' + STAMP + ' · ' + c.path + ' -->\n</html>');
  if (!global.__built) global.__built = new Set();
  if (global.__built.has(c.path)) throw new Error('DUPLICATE PAGE PATH: ' + c.path + ' built twice (second source: ' + f + ')');
  global.__built.add(c.path);
  const out = c.path.endsWith('.html')
    ? path.join(OUT, c.path.replace(/^\//, ''))
    : path.join(OUT, c.path.replace(/^\//, ''), 'index.html');
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, html);
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
  '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
  SITEMAP_PATHS.map(p => '  <url><loc>https://www.estatelandscapers.com.au' + p + '</loc><lastmod>' + today + '</lastmod></url>').join('\n') +
  '\n</urlset>\n');
console.log(n + ' pages built into public/ · sitemap.xml: ' + SITEMAP_PATHS.length + ' URLs');
