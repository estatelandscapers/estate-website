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
  var nav = document.querySelector('.nav');
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

// Hero band scroll-reveal: as the band approaches the top of the viewport it
// inflates toward full height — the scroll "feeds" the image — then releases
// and scrolls past. Reversible; disabled for reduced-motion.
(function () {
  var band = document.querySelector('.fdh-band');
  if (!band) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var ticking = false;
  function minH(vh) {
    var m = Math.min(vh * 0.48, 540);
    if (window.innerWidth <= 700) m = vh * 0.38;
    return Math.max(m, 260);
  }
  function frame() {
    ticking = false;
    var vh = window.innerHeight;
    var r = band.getBoundingClientRect();
    var start = vh, end = vh * 0.10;               // grow while the band's top travels this zone
    var p = (start - r.top) / (start - end);
    p = Math.max(0, Math.min(1, p));
    p = p * p * (3 - 2 * p);                        // smoothstep
    var h = minH(vh) + (vh - minH(vh)) * p;
    band.style.setProperty('--bandh', h.toFixed(1) + 'px');
    band.style.height = 'var(--bandh)';
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  frame();
})();
