// Mobile navigation toggle
(function () {
  var btn = document.querySelector('.nav-toggle');
  var links = document.getElementById('nav-links');
  if (!btn || !links) return;
  btn.addEventListener('click', function () {
    var open = links.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
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
