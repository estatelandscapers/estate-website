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

// Mark the current page in the navigation
(function () {
  var here = location.pathname.replace(/\/+$/, '/') || '/';
  document.querySelectorAll('.nav-links a').forEach(function (a) {
    var href = a.getAttribute('href') || '';
    if (href.split('#')[0] === here) a.setAttribute('aria-current', 'page');
  });
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
