// Google Analytics 4 — loader is in the page head; config fires on the live
// domain only, so staging traffic never pollutes the property. gtag is defined
// globally either way so form events can call it safely.
window.dataLayer = window.dataLayer || [];
window.gtag = function () { dataLayer.push(arguments); };
if (/estatelandscapers\.com\.au$/.test(location.hostname)) {
  gtag('js', new Date());
  gtag('config', 'G-NWQPY0NXEF');
}

// Mobile navigation toggle
(function () {
  var btn = document.querySelector('.nav-toggle');
  var links = document.getElementById('nav-links');
  if (!btn || !links) return;
  function setOpen(open) {
    links.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.style.overflow = open ? 'hidden' : '';
  }
  btn.addEventListener('click', function () { setOpen(!links.classList.contains('open')); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && links.classList.contains('open')) { setOpen(false); btn.focus(); }
  });
  document.addEventListener('click', function (e) {
    if (links.classList.contains('open') && !links.contains(e.target) && !btn.contains(e.target)) setOpen(false);
  });
  links.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
})();

// Navigation highlighting.
// Plain page links: marked when you're ON that page. Anchor links (Services,
// Process): scrollspy — lit only while their section is actually in view.
(function () {
  var here = location.pathname.replace(/\/+$/, '/') || '/';
  if (!here.endsWith('/')) here += '/';
  var links = [].slice.call(document.querySelectorAll('.nav-links a'));

  // 1. Same-page anchor links become spies; other links get page marking.
  var spies = [];
  links.forEach(function (a) {
    var href = a.getAttribute('href') || '';
    var path = href.split('#')[0];
    var hash = href.indexOf('#') > -1 ? href.split('#')[1] : '';
    if (hash && (path === here || path === '')) {
      var t = document.getElementById(hash);
      if (t) spies.push({ a: a, t: t });
    } else if (!hash && path === here) {
      a.setAttribute('aria-current', 'page');
    }
  });

  // 2. Scrollspy: a section is "current" while it occupies the reading band
  //    near the top of the viewport; leaving it clears the highlight.
  if (spies.length && 'IntersectionObserver' in window) {
    function clear() { spies.forEach(function (s) { s.a.removeAttribute('aria-current'); }); }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var m = spies.filter(function (s) { return s.t === e.target; })[0];
        if (!m) return;
        if (e.isIntersecting) { clear(); m.a.setAttribute('aria-current', 'location'); }
        else if (m.a.hasAttribute('aria-current')) { m.a.removeAttribute('aria-current'); }
      });
    }, { rootMargin: '-15% 0px -65% 0px' });
    spies.forEach(function (s) { io.observe(s.t); });
  }
})();

// Current year in the footer
(function () {
  var y = document.getElementById('yr');
  if (y) y.textContent = new Date().getFullYear();
})();

// GA4 — only on the live domain, so staging never pollutes the data
(function () {
  var h = location.hostname;
  if (h !== 'www.estatelandscapers.com.au' && h !== 'estatelandscapers.com.au') return;
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=G-NWQPY0NXEF';
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', 'G-NWQPY0NXEF');
})();

// Precise anchor offset: measure the sticky nav so jumped-to headings land exactly
// below it — no sliver of the section above showing through.
(function () {
  var nav = document.querySelector('.hd') || document.querySelector('.nav');
  if (!nav) return;
  function set() { document.documentElement.style.setProperty('--navh', nav.offsetHeight + 'px'); }
  set();
  window.addEventListener('resize', set);
})();

// Back to top — appears after a screen and a half of scroll.
(function () {
  var b = document.createElement('button');
  b.className = 'totop'; b.type = 'button'; b.setAttribute('aria-label', 'Back to top');
  b.innerHTML = '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M7 12V2M2.5 6.5 7 2l4.5 4.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  b.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  document.body.appendChild(b);
  window.addEventListener('scroll', function () {
    b.classList.toggle('show', window.scrollY > window.innerHeight * 1.5);
  }, { passive: true });
})();

// First-touch attribution: remember the landing page and any campaign tags, so the
// enquiry that happens three pages later still knows where the visit came from.
(function () {
  try {
    var q = new URLSearchParams(location.search), utm = {}, has = false;
    ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid'].forEach(function (k) {
      if (q.get(k)) { utm[k] = q.get(k); has = true; }
    });
    if (has && !sessionStorage.getItem('el_utm')) sessionStorage.setItem('el_utm', JSON.stringify(utm));
    if (!sessionStorage.getItem('el_landing')) sessionStorage.setItem('el_landing', location.pathname + location.search);
  } catch (e) {}
})();


// Cursor: dot glued to the mouse, ring chasing with easing, both blend-inverted
// so they read over any background; grows over interactive elements. Fine
// pointers only, and only when the boot script allowed motion (html.js).
(function () {
  if (!/\bjs\b/.test(document.documentElement.className)) return;
  if (!window.matchMedia('(pointer: fine)').matches) return;
  var dot = document.createElement('div'); dot.id = 'cur';
  var ring = document.createElement('div'); ring.id = 'cuf';
  document.body.appendChild(dot); document.body.appendChild(ring);
  document.documentElement.classList.add('cur-on');
  var mx = -40, my = -40, fx = -40, fy = -40;
  document.addEventListener('mousemove', function (e) {
    mx = e.clientX; my = e.clientY;
    dot.style.left = mx + 'px'; dot.style.top = my + 'px';
  }, { passive: true });
  (function chase() {
    fx += (mx - fx) * 0.13; fy += (my - fy) * 0.13;
    ring.style.left = fx + 'px'; ring.style.top = fy + 'px';
    requestAnimationFrame(chase);
  })();
  document.addEventListener('mouseover', function (e) {
    if (e.target.closest('a, button, .chip, .card, .fd-door, input, select, textarea, .filebox'))
      document.documentElement.classList.add('cur-hover');
  }, { passive: true });
  document.addEventListener('mouseout', function (e) {
    if (e.target.closest('a, button, .chip, .card, .fd-door, input, select, textarea, .filebox'))
      document.documentElement.classList.remove('cur-hover');
  }, { passive: true });
})();

// Reveal on scroll: content blocks below the fold rise in as they enter view,
// staggered within their group. Above-the-fold content is never touched, so
// nothing flashes; without JS or with reduced motion, everything is static.
(function () {
  if (!/\bjs\b/.test(document.documentElement.className)) return;
  if (!('IntersectionObserver' in window)) return;
  var els = document.querySelectorAll('.card, .steps li, .faq li, .fd-row .tx, .fd-door, .g2 > div, .plate');
  var vh = window.innerHeight, list = [];
  els.forEach(function (el) {
    if (el.getBoundingClientRect().top > vh * 0.88) { el.classList.add('rv'); list.push(el); }
  });
  if (!list.length) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var el = en.target, sibs = el.parentElement ? [].slice.call(el.parentElement.children) : [];
      var i = Math.max(0, sibs.indexOf(el));
      el.style.transitionDelay = Math.min(i * 70, 350) + 'ms';
      el.classList.add('v');
      io.unobserve(el);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  list.forEach(function (el) { io.observe(el); });
})();

// Front-door mega menu: hamburger opens the full sitemap panel; closes on X,
// Escape, or choosing a link. Focus moves in on open and back on close.
(function () {
  var btn = document.getElementById('megabtn');
  var mega = document.getElementById('mega');
  var close = document.getElementById('megaclose');
  if (!btn || !mega || !close) return;
  function setOpen(open) {
    mega.classList.toggle('on', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) close.focus(); else btn.focus();
  }
  btn.addEventListener('click', function () { setOpen(true); });
  close.addEventListener('click', function () { setOpen(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && mega.classList.contains('on')) setOpen(false);
  });
  mega.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
})();

// Hero project slider: fades between slides every 5s when there's more than one,
// with arrows and dots. One slide today; each future project adds a div.fdh-slide.
(function () {
  var band = document.getElementById('heroslides');
  if (!band) return;
  var slides = [].slice.call(band.querySelectorAll('.fdh-slide'));
  if (slides.length < 2) return;
  band.classList.add('multi');
  var dots = band.querySelector('.fdh-dots'), cur = 0, timer;
  slides.forEach(function (_, i) {
    var b = document.createElement('button');
    b.setAttribute('aria-label', 'Go to project ' + (i + 1));
    b.addEventListener('click', function () { go(i, true); });
    dots.appendChild(b);
  });
  function paint() {
    slides.forEach(function (s, i) { s.classList.toggle('on', i === cur); });
    [].slice.call(dots.children).forEach(function (d, i) { d.classList.toggle('on', i === cur); });
  }
  function go(i, manual) {
    cur = (i + slides.length) % slides.length; paint();
    if (manual) { clearInterval(timer); arm(); }
  }
  function arm() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    timer = setInterval(function () { go(cur + 1); }, 5000);
  }
  band.querySelector('.fdh-arr.prev').addEventListener('click', function () { go(cur - 1, true); });
  band.querySelector('.fdh-arr.next').addEventListener('click', function () { go(cur + 1, true); });
  paint(); arm();
})();

// Instagram squares on the residential page. Two sources, in order:
//   1. the quote tool's /api/public/instagram endpoint (live, daily) if it exists
//   2. /instagram.json in this repo — update it weekly, no backend needed
// If neither yields posts, the labelled photo slots stay exactly as they are.
(function () {
  var grid = document.getElementById('igfeed');
  if (!grid) return;
  function render(posts) {
    if (!posts || !posts.length) return false;
    var plates = grid.querySelectorAll('.plate');
    posts.slice(0, plates.length).forEach(function (p, i) {
      if (!p.image || !p.permalink) return;
      var a = document.createElement('a');
      a.href = p.permalink; a.target = '_blank'; a.rel = 'noopener';
      a.style.cssText = 'position:absolute;inset:0;display:block';
      var img = document.createElement('img');
      img.src = p.image; img.alt = (p.caption || 'Estate Landscapers on Instagram').slice(0, 120);
      img.loading = 'lazy'; img.style.cssText = 'width:100%;height:100%;object-fit:cover';
      a.appendChild(img); plates[i].innerHTML = ''; plates[i].appendChild(a);
    });
    return true;
  }
  fetch('/api/instagram')
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (d) { if (!render(d && d.posts)) throw 0; })
    .catch(function () {
      fetch('/instagram.json').then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) { render(d && d.posts); }).catch(function () {});
    });
})();

// Reading progress bar (mobile): fills as the reader moves down the page.
(function () {
  var bar = document.querySelector('.prog i');
  if (!bar) return;
  function upd() {
    var max = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.height = (max > 0 ? Math.min(100, window.scrollY / max * 100) : 0).toFixed(1) + '%';
  }
  window.addEventListener('scroll', upd, { passive: true }); window.addEventListener('resize', upd); upd();
})();

// Projects index: sector filter chips.
(function () {
  var grid = document.getElementById('pgrid'); if (!grid) return;
  var chips = document.querySelectorAll('[data-f]');
  chips.forEach(function (b) { b.addEventListener('click', function () {
    var f = b.dataset.f;
    chips.forEach(function (x) { x.classList.toggle('b', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    grid.querySelectorAll('.card').forEach(function (c) { c.classList.toggle('hide', f !== 'all' && c.dataset.sector !== f); });
  }); });
})();

// ---------------------------------------------------------------- prefetch --
// Predictive loading: the page a visitor is about to open is fetched before
// they click. Two signals, both cheap: links that scroll into view get a
// low-priority speculative fetch, and hovering or touching one promotes it.
// Only same-origin document links, never forms or downloads, and skipped
// entirely on slow connections or when the browser asks us to save data.
(function () {
  var nav = navigator.connection || {};
  if (nav.saveData) return;
  if (/2g/.test(nav.effectiveType || '')) return;
  var done = {};
  function prefetch(href, priority) {
    if (!href || done[href]) return;
    var u;
    try { u = new URL(href, location.href); } catch (e) { return; }
    if (u.origin !== location.origin) return;
    if (u.pathname === location.pathname) return;
    if (/\.(zip|pdf|jpe?g|png|webp|svg)$/i.test(u.pathname)) return;
    done[href] = 1;
    var l = document.createElement('link');
    l.rel = 'prefetch'; l.href = u.href; l.as = 'document';
    if (priority) l.fetchPriority = 'high';
    document.head.appendChild(l);
  }
  // hover / touch = strong intent
  ['mouseover', 'touchstart', 'focusin'].forEach(function (ev) {
    document.addEventListener(ev, function (e) {
      var a = e.target.closest && e.target.closest('a[href]');
      if (a) prefetch(a.getAttribute('href'), true);
    }, { passive: true, capture: true });
  });
  // visible links = weak intent, throttled to the first dozen
  if ('IntersectionObserver' in window) {
    var budget = 12;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting || budget <= 0) return;
        budget--; prefetch(en.target.getAttribute('href'), false); io.unobserve(en.target);
      });
    }, { rootMargin: '200px' });
    setTimeout(function () {
      document.querySelectorAll('main a[href^="/"]').forEach(function (a) { io.observe(a); });
    }, 1200);
  }
})();

// --------------------------------------------------------------- behaviour --
// What visitors actually do, sent to GA4 as named events. Nothing personal is
// collected: no text they type, no identifiers, only which things get used.
// Read these in GA4 → Reports → Engagement → Events.
(function () {
  if (typeof gtag !== 'function') return;
  var page = location.pathname;
  function ev(name, params) { try { gtag('event', name, params || {}); } catch (e) {} }

  // how far down the page people actually get
  var marks = [25, 50, 75, 100], hit = {};
  function depth() {
    var max = document.documentElement.scrollHeight - window.innerHeight;
    var pct = max > 0 ? (window.scrollY / max) * 100 : 100;
    marks.forEach(function (m) {
      if (pct >= m && !hit[m]) { hit[m] = 1; ev('scroll_depth', { percent: m, page_path: page }); }
    });
  }
  window.addEventListener('scroll', depth, { passive: true }); depth();

  // time actually spent reading, banded so it stays useful in reports
  var start = Date.now(), sent = {};
  [15, 60, 180].forEach(function (s) {
    setTimeout(function () {
      if (document.visibilityState === 'visible' && !sent[s]) {
        sent[s] = 1; ev('time_on_page', { seconds: s, page_path: page });
      }
    }, s * 1000);
  });

  // clicks worth knowing about
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a, button');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    var label = (a.textContent || '').trim().slice(0, 60);
    if (/^tel:/.test(href)) return ev('click_phone', { page_path: page });
    if (/^mailto:/.test(href)) return ev('click_email', { page_path: page });
    if (/\/residential\/quote\//.test(href)) return ev('cta_quote', { page_path: page, label: label });
    if (/\/commercial\/tender\//.test(href)) return ev('cta_tender', { page_path: page, label: label });
    if (/^\/projects\/[a-z]/.test(href)) return ev('open_project', { page_path: page, project: href });
    if (/^\/areas\/[a-z]/.test(href)) return ev('open_area', { page_path: page, area: href });
    if (a.dataset && a.dataset.f) return ev('filter_projects', { filter: a.dataset.f });
    if (a.closest('#mega')) return ev('menu_navigate', { to: href });
    if (/^https?:/.test(href) && href.indexOf(location.host) === -1)
      return ev('click_outbound', { page_path: page, to: href.slice(0, 100) });
  }, { passive: true, capture: true });

  // did the visitor see the photo of the work, or bounce above it?
  if ('IntersectionObserver' in window) {
    var seen = false;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting && !seen) { seen = true; ev('gallery_viewed', { page_path: page }); io.disconnect(); }
      });
    }, { threshold: 0.3 });
    var g = document.querySelector('.g3 .plate img, .fdh-band');
    if (g) io.observe(g);
  }
})();

// ---------------------------------------------------------------- video ----
// Silent looping clips play only when they are worth playing: motion allowed,
// a real connection, and the element actually on screen. Everything else sees
// the poster still, which is why a poster is required.
(function () {
  var vids = document.querySelectorAll('video.herovid, video.slotvid');
  if (!vids.length) return;
  var nav = navigator.connection || {};
  var allow = !window.matchMedia('(prefers-reduced-motion: reduce)').matches &&
              !nav.saveData && !/2g/.test(nav.effectiveType || '');
  if (!allow) return;                      // poster remains, nothing downloads
  if (!('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      var v = en.target;
      if (en.isIntersecting) {
        if (v.preload !== 'auto') { v.preload = 'auto'; v.load(); }
        var p = v.play();
        if (p && p.catch) p.catch(function () {});
        v.classList.add('on');
      } else if (!v.paused) v.pause();
    });
  }, { threshold: 0.25 });
  vids.forEach(function (v) { io.observe(v); });
})();
