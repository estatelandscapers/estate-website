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
    FOOTER: c.footer ? '{{include footer-' + c.footer + '}}' : '',
    BODY: body
  };
  const html = c.raw ? render(body, vars) : render(layout, vars);
  const out = c.path.endsWith('.html')
    ? path.join(OUT, c.path.replace(/^\//, ''))
    : path.join(OUT, c.path.replace(/^\//, ''), 'index.html');
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, html);
  console.log('built ' + c.path);
  n++;
}
console.log(n + ' pages built into public/');
