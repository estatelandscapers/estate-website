// Estate Landscapers: the online estimator.
//
// The questions, the number and the booking all come from the quote tool. This file is
// the screens: one question at a time, big targets, answers saved as they go, and a
// heartbeat so the tool knows how long the client spent where. No framework, no build.
(function () {
  'use strict';
  var root = document.getElementById('estimator'); if (!root) return;
  var app = document.getElementById('estApp');
  var API = root.dataset.endpoint;
  var qs = new URLSearchParams(location.search);

  // ---- state --------------------------------------------------------------------------
  var S = { token: null, vk: null, first: '', steps: [], sizes: [], answers: {}, reactions: [], expires: null,
    completed: false, booked: false, i: 0, screen: 'gate', result: null, slots: null, email: qs.get('e') || '' };
  try { S.vk = localStorage.getItem('el_vk'); if (!S.vk) { S.vk = 'v' + Date.now().toString(36) + Math.random().toString(36).slice(2, 10); localStorage.setItem('el_vk', S.vk); } } catch (e) { S.vk = 'v' + Date.now().toString(36); }
  try { S.token = sessionStorage.getItem('el_est_token'); } catch (e) {}

  function api(path, body, method) {
    var h = { 'Content-Type': 'application/json', 'X-Est-Visitor': S.vk };
    if (S.token) h['X-Est-Token'] = S.token;
    return fetch(API + path, { method: method || (body ? 'POST' : 'GET'), headers: h, body: body ? JSON.stringify(body) : undefined })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok) { var e = new Error(j.error || 'Something went wrong'); e.status = r.status; e.paused = !!j.paused; if (e.paused) paused(j.error); throw e; } return j; }); });
  }
  // The tool can switch the estimator off from Settings. Every call then answers 503 with
  // paused:true; the page shows one honest screen and points at the quote form.
  function paused(msg) {
    setScreen('paused');
    h(frame({ body: '<p class="eyebrow">Free online estimate</p><h1>The estimator is taking a short break.</h1>' +
      '<p class="est-hint">' + esc(msg || 'It will be back shortly.') + '</p>' +
      '<div class="btn-row"><a class="btn" href="/residential/quote/">Get a quote</a><a class="btn btn-o" href="/contact/">Contact us</a></div>' }));
  }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function ga(name, p) { try { if (window.gtag) window.gtag('event', name, p || {}); } catch (e) {} }

  // ---- heartbeat: seconds on each screen, every 15 s while the page is in front of them ----
  var hb = { screen: 'gate', since: Date.now(), acc: {} };
  function tick() {
    if (document.visibilityState !== 'visible') { hb.since = Date.now(); return; }
    var now = Date.now(), sec = Math.round((now - hb.since) / 1000); hb.since = now;
    if (sec > 0) hb.acc[hb.screen] = (hb.acc[hb.screen] || 0) + sec;
  }
  function flush() {
    tick();
    var keys = Object.keys(hb.acc); if (!keys.length || !S.token) return;
    var total = 0; keys.forEach(function (k) { total += hb.acc[k]; });
    var payload = { seconds: total, screens: hb.acc }; hb.acc = {};
    api('/event', { type: 'heartbeat', payload: payload }).catch(function () {});
  }
  setInterval(flush, 15000);
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') flush(); else hb.since = Date.now(); });
  window.addEventListener('pagehide', flush);
  function setScreen(name) { tick(); hb.screen = name; S.screen = name; }

  // ---- which questions apply ------------------------------------------------------------
  function applicable() {
    return S.steps.filter(function (s) {
      if (!s.showIf) return true;
      return Object.keys(s.showIf).every(function (k) { return s.showIf[k].indexOf(S.answers[k]) >= 0; });
    });
  }
  function answered(s) {
    var v = S.answers[s.key];
    if (s.type === 'sizes') return Object.keys(S.answers.sizes || {}).length > 0;
    if (s.type === 'multi') return Array.isArray(v) && v.length > 0;
    return v !== undefined && v !== null && v !== '';
  }

  // ---- render ---------------------------------------------------------------------------
  function h(html) { app.innerHTML = html; window.scrollTo({ top: Math.max(0, app.getBoundingClientRect().top + window.scrollY - 90), behavior: 'smooth' }); }
  function frame(opts) {
    var pct = opts.pct == null ? null : Math.round(opts.pct);
    return '<div class="est-card">' +
      '<div class="est-top"><span class="est-brand">ESTATE <em>·</em></span><span class="est-count">' + esc(opts.count || '') + '</span></div>' +
      (pct == null ? '' : '<div class="est-prog"><i style="width:' + pct + '%"></i></div>') +
      '<div class="est-body">' + opts.body + '</div>' +
      (opts.foot ? '<div class="est-foot">' + opts.foot + '</div>' : '') + '</div>';
  }
  var BTN = function (id, label, outline) { return '<button type="button" class="btn' + (outline ? ' btn-o' : '') + '" id="' + id + '">' + label + '</button>'; };

  // ---- the gate -------------------------------------------------------------------------
  function gate(msg, mode) {
    setScreen('gate');
    mode = mode || (S.email ? 'code' : 'code');
    var codeForm = '<p class="eyebrow">Free online estimate</p><h1>Enter your 4-digit code</h1>' +
      '<p class="est-hint">It is in the email we sent you. Your answers are saved, so you can come back any time.</p>' +
      (msg ? '<p class="est-err">' + esc(msg) + '</p>' : '') +
      '<div class="field"><label for="gEmail">Email the code was sent to</label><input id="gEmail" type="email" inputmode="email" autocomplete="email" value="' + esc(S.email) + '" placeholder="you@example.com"></div>' +
      '<div class="field"><label for="gCode">Access code</label><input id="gCode" type="text" inputmode="numeric" pattern="[0-9]*" maxlength="4" autocomplete="one-time-code" class="est-code" placeholder="0000"></div>' +
      '<div class="btn-row"><button type="button" class="btn" id="gGo">Continue</button></div>' +
      '<p class="est-links"><a href="#" id="gNo">I don\'t have a code yet</a> · <a href="#" id="gResend">Resend my code</a></p>';
    var getForm = '<p class="eyebrow">Free online estimate</p><h1>Get your code</h1>' +
      '<p class="est-hint">We email you a 4-digit code straight away. It opens the estimator, and your answers are saved as you go.</p>' +
      (msg ? '<p class="est-err">' + esc(msg) + '</p>' : '') +
      '<div class="field"><label for="sName">Your name</label><input id="sName" autocomplete="name"></div>' +
      '<div class="field"><label for="sEmail">Email</label><input id="sEmail" type="email" inputmode="email" autocomplete="email" value="' + esc(S.email) + '"></div>' +
      '<div class="field"><label for="sPhone">Mobile <span class="opt">optional</span></label><input id="sPhone" type="tel" inputmode="tel" autocomplete="tel"></div>' +
      '<div class="field"><label for="sSuburb">Suburb</label><input id="sSuburb" autocomplete="address-level2"></div>' +
      '<input type="text" name="website" id="sWeb" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">' +
      '<div class="btn-row"><button type="button" class="btn" id="sGo">Email me the code</button></div>' +
      '<p class="est-links"><a href="#" id="sHave">I already have a code</a></p>';
    h(frame({ body: mode === 'get' ? getForm : codeForm }));
    if (mode === 'get') {
      document.getElementById('sHave').addEventListener('click', function (e) { e.preventDefault(); gate(null, 'code'); });
      document.getElementById('sGo').addEventListener('click', function () {
        var b = { name: document.getElementById('sName').value.trim(), email: document.getElementById('sEmail').value.trim(), phone: document.getElementById('sPhone').value.trim(), suburb: document.getElementById('sSuburb').value.trim(), website: document.getElementById('sWeb').value };
        if (!b.name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(b.email)) return gate('Your name and a valid email are needed: the code is emailed to you.', 'get');
        this.disabled = true; this.textContent = 'Sending…';
        api('/start', b).then(function (r) { S.email = b.email; ga('estimate_code_requested'); sent(r.email); })
          .catch(function (e) { if (!e.paused) gate(e.message, 'get'); });
      });
    } else {
      document.getElementById('gNo').addEventListener('click', function (e) { e.preventDefault(); gate(null, 'get'); });
      document.getElementById('gResend').addEventListener('click', function (e) {
        e.preventDefault(); var em = document.getElementById('gEmail').value.trim();
        if (!em) return gate('Enter your email first, then tap Resend.');
        api('/resend', { email: em }).then(function () { S.email = em; sent(em); }).catch(function () { sent(em); });
      });
      var go = function () {
        var em = document.getElementById('gEmail').value.trim(), code = document.getElementById('gCode').value.replace(/\D/g, '');
        if (!em || code.length !== 4) return gate('Enter the email and the 4-digit code from it.');
        document.getElementById('gGo').disabled = true;
        api('/auth', { code: code, email: em, vk: S.vk, touch: 'ontouchstart' in window }).then(function (r) {
          S.token = r.token; try { sessionStorage.setItem('el_est_token', r.token); } catch (x) {}
          S.email = em; S.first = r.first || ''; S.steps = r.steps; S.sizes = r.sizes; S.answers = r.answers || {}; S.reactions = r.reactions; S.expires = r.expires;
          S.completed = !!r.completed; S.booked = !!r.booked; S.saved = r.saved || 0;
          ga('estimate_opened');
          welcome();
        }).catch(function (e) { if (!e.paused) gate(e.message); });
      };
      document.getElementById('gGo').addEventListener('click', go);
      document.getElementById('gCode').addEventListener('keydown', function (e) { if (e.key === 'Enter') go(); });
      (S.email ? document.getElementById('gCode') : document.getElementById('gEmail')).focus();
    }
  }
  function sent(masked) {
    setScreen('gate');
    h(frame({ body: '<p class="eyebrow">Check your email</p><h1>Your code is on its way</h1>' +
      '<p class="est-hint">We sent a 4-digit code to <b>' + esc(masked || S.email) + '</b>. It can take a minute. Check junk if it is not there.</p>' +
      '<div class="btn-row"><button type="button" class="btn" id="sBack">I have the code</button></div>' }));
    document.getElementById('sBack').addEventListener('click', function () { gate(null, 'code'); });
  }

  // ---- welcome / resume -----------------------------------------------------------------
  function welcome() {
    setScreen('welcome');
    var list = applicable(), done = list.filter(answered).length;
    var resume = S.saved > 0 && done > 0 && !S.completed;
    var body = '<p class="eyebrow">' + (S.first ? 'Hi ' + esc(S.first) : 'Welcome') + '</p>' +
      (S.booked ? '<h1>Your site visit is booked.</h1><p class="est-hint">You can still change your answers or look at your ballpark again. We will confirm the visit the day before, with an ETA.</p>'
        : S.completed ? '<h1>Welcome back.</h1><p class="est-hint">You have already seen your ballpark. Change any answer and it updates, or pick a Friday for the site visit.</p>'
        : resume ? '<h1>Pick up where you left off.</h1><p class="est-hint">You have answered ' + done + ' of ' + list.length + ' questions. The rest takes a few minutes.</p>'
        : '<h1>About 8 minutes, one question at a time.</h1><p class="est-hint">Rough answers are fine, and "Not sure" is always an option: anything you are not sure of, we measure on the site visit. You get a ballpark range at the end.</p>') +
      '<div class="btn-row">' +
      (S.completed ? BTN('wBall', 'See my ballpark') + BTN('wReview', 'Change my answers', true) + (S.booked ? '' : BTN('wBook', 'Pick a Friday', true))
        : BTN('wStart', resume ? 'Continue' : 'Start')) + '</div>';
    h(frame({ body: body }));
    var on = function (id, fn) { var el = document.getElementById(id); if (el) el.addEventListener('click', fn); };
    on('wStart', function () { S.i = resume ? firstUnanswered() : 0; question(); });
    on('wBall', function () { complete(); });
    on('wReview', function () { review(); });
    on('wBook', function () { book(); });
  }
  function firstUnanswered() { var list = applicable(); for (var i = 0; i < list.length; i++) if (!answered(list[i]) && !list[i].optional) return i; return 0; }

  // ---- questions --------------------------------------------------------------------------
  function question() {
    var list = applicable();
    if (S.i >= list.length) return review();
    if (S.i < 0) S.i = 0;
    var s = list[S.i]; setScreen(s.id);
    var body = '<p class="est-sec">' + esc(s.section) + '</p><h2 class="est-q">' + esc(s.title) + '</h2>' + (s.hint ? '<p class="est-hint">' + esc(s.hint) + '</p>' : '');
    var v = S.answers[s.key];
    if (s.type === 'text') {
      body += '<div class="field"><input id="qText" value="' + esc(v || '') + '" placeholder="e.g. 23 Frederick Street, Miranda"></div>';
    } else if (s.type === 'single') {
      body += '<div class="est-opts">' + s.options.map(function (o) { return '<button type="button" class="est-opt" data-v="' + esc(o.v) + '" aria-pressed="' + (v === o.v) + '">' + esc(o.label) + '</button>'; }).join('') +
        (s.other ? '<button type="button" class="est-opt" data-other="1" aria-pressed="' + (v && !s.options.some(function (o) { return o.v === v; })) + '">Someone else…</button><div class="field" id="qOtherWrap" style="' + (v && !s.options.some(function (o) { return o.v === v; }) ? '' : 'display:none') + '"><input id="qOther" value="' + esc(v && !s.options.some(function (o) { return o.v === v; }) ? v : '') + '" placeholder="Type the name"></div>' : '') + '</div>';
    } else if (s.type === 'multi') {
      var arr = Array.isArray(v) ? v : [];
      body += '<div class="chips est-chips">' + s.options.map(function (o) { return '<button type="button" class="chip" data-v="' + esc(o.v) + '" aria-pressed="' + (arr.indexOf(o.v) >= 0) + '">' + esc(o.label) + '</button>'; }).join('') + '</div>';
    } else if (s.type === 'sizes') {
      var scope = (S.answers.scope || []).filter(function (id) { return S.sizes.some(function (z) { return z.id === id; }); });
      if (!scope.length) { S.answers.sizes = S.answers.sizes || {}; S.i++; return question(); }
      var sz = S.answers.sizes || {};
      body += scope.map(function (id) {
        var z = S.sizes.find(function (x) { return x.id === id; });
        var cur = sz[id], unk = cur === 'unknown', val = unk || cur == null ? Math.round(z.max / 4 / z.step) * z.step : cur;
        return '<div class="est-size" data-id="' + id + '"><h3>' + esc(z.ask) + '</h3>' + (z.typical ? '<p class="est-hint">' + esc(z.typical) + '</p>' : '') +
          '<div class="est-slider' + (unk ? ' is-unk' : '') + '"><div class="est-val"><b>' + val + '</b> ' + esc(z.unit) + '</div>' +
          '<input type="range" min="' + z.step + '" max="' + z.max + '" step="' + z.step + '" value="' + val + '" aria-label="' + esc(z.label) + '">' +
          '<div class="est-ends"><span>' + z.step + '</span><span>' + z.max + ' ' + esc(z.unit) + '</span></div></div>' +
          '<button type="button" class="est-unk" aria-pressed="' + unk + '">Not sure</button></div>';
      }).join('');
    } else if (s.type === 'slider') {
      var unk2 = v === 'unknown', val2 = unk2 || v == null ? s.def : v;
      body += '<div class="est-slider' + (unk2 ? ' is-unk' : '') + '" id="qSlider"><div class="est-val"><b>' + val2 + '</b> ' + esc(s.unit) + (s.id === 'access' ? ' <span class="est-bin">' + binHint(val2) + '</span>' : '') + '</div>' +
        '<input type="range" min="' + s.min + '" max="' + s.max + '" step="' + s.step + '" value="' + val2 + '"><div class="est-ends"><span>' + s.min + '</span><span>' + s.max + ' ' + esc(s.unit) + '</span></div></div>' +
        (s.unknown ? '<button type="button" class="est-unk" id="qUnk" aria-pressed="' + unk2 + '">Not sure</button>' : '');
    } else if (s.type === 'scale') {
      var dir = S.answers.fallDir || '';
      body += '<div class="est-scale">' + s.scale.map(function (o) { return '<button type="button" class="est-opt est-opt-sm" data-v="' + o.v + '" aria-pressed="' + (v === o.v) + '">' + esc(o.label) + '</button>'; }).join('') + '</div>' +
        '<div class="est-dir" id="qDir" style="' + (v > 0 ? '' : 'display:none') + '"><p class="est-hint">And is the back fence higher or lower than where you are standing?</p>' +
        '<div class="est-opts est-two"><button type="button" class="est-opt" data-dir="higher" aria-pressed="' + (dir === 'higher') + '">Higher</button><button type="button" class="est-opt" data-dir="lower" aria-pressed="' + (dir === 'lower') + '">Lower</button></div></div>' +
        '<button type="button" class="est-unk" id="qUnk" aria-pressed="' + (v === 'unknown') + '">Not sure</button>';
    }
    var foot = BTN('qBack', 'Back', true) + BTN('qNext', s.optional && !answered(s) ? 'Skip' : 'Next');
    h(frame({ count: (S.i + 1) + ' of ' + list.length, pct: 100 * S.i / list.length, body: body, foot: foot }));
    wire(s);
  }
  function binHint(mm) { mm = +mm; return mm < 600 ? 'narrower than a wheelie bin' : mm < 700 ? 'about a wheelie bin' : mm < 1000 ? 'a bin and a bit' : mm < 1500 ? 'a wheelbarrow passes easily' : 'a small machine fits'; }
  function wire(s) {
    var next = document.getElementById('qNext'), unknownTapped = false;
    document.getElementById('qBack').addEventListener('click', function () { if (S.i === 0) return welcome(); S.i--; question(); });
    if (s.type === 'text') {
      var t = document.getElementById('qText'); t.focus();
      t.addEventListener('keydown', function (e) { if (e.key === 'Enter') next.click(); });
    }
    if (s.type === 'single') {
      app.querySelectorAll('.est-opt').forEach(function (b) {
        b.addEventListener('click', function () {
          app.querySelectorAll('.est-opt').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
          b.setAttribute('aria-pressed', 'true');
          var ow = document.getElementById('qOtherWrap');
          if (b.dataset.other) { if (ow) { ow.style.display = ''; document.getElementById('qOther').focus(); } }
          else { if (ow) ow.style.display = 'none'; S.answers[s.key] = b.dataset.v; setTimeout(function () { next.click(); }, 180); }
        });
      });
    }
    if (s.type === 'multi') {
      app.querySelectorAll('.chip').forEach(function (b) {
        b.addEventListener('click', function () {
          var on = b.getAttribute('aria-pressed') === 'true';
          var exclusive = ['none', 'nothing', 'unknown', 'unsure'];
          if (!on && exclusive.indexOf(b.dataset.v) >= 0) app.querySelectorAll('.chip').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
          if (!on && exclusive.indexOf(b.dataset.v) < 0) app.querySelectorAll('.chip').forEach(function (x) { if (exclusive.indexOf(x.dataset.v) >= 0) x.setAttribute('aria-pressed', 'false'); });
          b.setAttribute('aria-pressed', on ? 'false' : 'true');
        });
      });
    }
    if (s.type === 'sizes' || s.type === 'slider') {
      app.querySelectorAll('input[type=range]').forEach(function (r) {
        r.addEventListener('input', function () {
          var wrap = r.closest('.est-slider'); wrap.classList.remove('is-unk');
          wrap.querySelector('.est-val b').textContent = r.value;
          var bin = wrap.querySelector('.est-bin'); if (bin) bin.textContent = binHint(r.value);
          var u = wrap.parentElement.querySelector('.est-unk'); if (u) u.setAttribute('aria-pressed', 'false');
        });
      });
      app.querySelectorAll('.est-unk').forEach(function (u) {
        u.addEventListener('click', function () {
          var on = u.getAttribute('aria-pressed') === 'true';
          u.setAttribute('aria-pressed', on ? 'false' : 'true');
          var wrap = u.parentElement.querySelector('.est-slider'); if (wrap) wrap.classList.toggle('is-unk', !on);
          unknownTapped = !on;
        });
      });
    }
    if (s.type === 'scale') {
      app.querySelectorAll('.est-scale .est-opt').forEach(function (b) {
        b.addEventListener('click', function () {
          app.querySelectorAll('.est-scale .est-opt').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
          b.setAttribute('aria-pressed', 'true'); document.getElementById('qUnk').setAttribute('aria-pressed', 'false');
          S.answers.fallMm = +b.dataset.v;
          var d = document.getElementById('qDir'); d.style.display = S.answers.fallMm > 0 ? '' : 'none';
          if (S.answers.fallMm === 0) { S.answers.fallDir = ''; setTimeout(function () { next.click(); }, 180); }
        });
      });
      app.querySelectorAll('[data-dir]').forEach(function (b) {
        b.addEventListener('click', function () {
          app.querySelectorAll('[data-dir]').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
          b.setAttribute('aria-pressed', 'true'); S.answers.fallDir = b.dataset.dir; setTimeout(function () { next.click(); }, 180);
        });
      });
      document.getElementById('qUnk').addEventListener('click', function () {
        app.querySelectorAll('.est-scale .est-opt').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        this.setAttribute('aria-pressed', 'true'); S.answers.fallMm = 'unknown'; S.answers.fallDir = ''; unknownTapped = true;
        document.getElementById('qDir').style.display = 'none';
      });
    }
    next.addEventListener('click', function () {
      // Collect the answer from the screen.
      var patch = {};
      if (s.type === 'text') { var tv = document.getElementById('qText').value.trim(); if (!tv) return shake(); patch[s.key] = tv; }
      if (s.type === 'single') {
        var o = document.getElementById('qOther');
        if (o && o.closest('#qOtherWrap').style.display !== 'none') { if (!o.value.trim()) return shake(); patch[s.key] = o.value.trim(); }
        else if (S.answers[s.key] == null) { if (s.optional) { S.i++; return question(); } return shake(); }
        else patch[s.key] = S.answers[s.key];
      }
      if (s.type === 'multi') {
        var sel = [].map.call(app.querySelectorAll('.chip[aria-pressed="true"]'), function (b) { return b.dataset.v; });
        if (!sel.length) { if (s.optional) { S.i++; return question(); } return shake(); }
        patch[s.key] = sel;
      }
      if (s.type === 'sizes') {
        var sz = {};
        app.querySelectorAll('.est-size').forEach(function (d) { var unk = d.querySelector('.est-unk').getAttribute('aria-pressed') === 'true'; sz[d.dataset.id] = unk ? 'unknown' : +d.querySelector('input[type=range]').value; });
        patch.sizes = sz;
      }
      if (s.type === 'slider') { var unk3 = document.getElementById('qUnk') && document.getElementById('qUnk').getAttribute('aria-pressed') === 'true'; patch[s.key] = unk3 ? 'unknown' : +document.querySelector('#qSlider input').value; }
      if (s.type === 'scale') {
        if (S.answers.fallMm == null) return shake();
        if (S.answers.fallMm > 0 && !S.answers.fallDir) { document.getElementById('qDir').style.display = ''; return shake(); }
        patch.fallMm = S.answers.fallMm; patch.fallDir = S.answers.fallDir || '';
      }
      Object.keys(patch).forEach(function (k) { S.answers[k] = patch[k]; });
      api('/answers', { step: s.id, answers: patch, unknown: unknownTapped || Object.keys(patch).some(function (k) { return patch[k] === 'unknown'; }) }).catch(function (e) { if (e.status === 401) return expired(); });
      S.i++; question();
    });
  }
  function shake() { var c = app.querySelector('.est-card'); c.classList.remove('est-shake'); void c.offsetWidth; c.classList.add('est-shake'); }
  function expired() { S.token = null; try { sessionStorage.removeItem('el_est_token'); } catch (e) {} gate('Your session timed out. Enter your code again and your answers will be there.'); }

  // ---- review: everything editable ----------------------------------------------------------
  var LABEL = {};
  function labelFor(s, v) {
    if (v == null || v === '') return '';
    if (v === 'unknown') return 'Not sure';
    if (s.type === 'sizes') { var sz = S.answers.sizes || {}; return Object.keys(sz).map(function (id) { var z = S.sizes.find(function (x) { return x.id === id; }) || { label: id, unit: '' }; return z.label + ': ' + (sz[id] === 'unknown' ? 'not sure' : sz[id] + ' ' + z.unit); }).join(', '); }
    if (s.type === 'scale') { var o = s.scale.find(function (x) { return x.v === v; }); return (o ? o.label : v + ' mm') + (S.answers.fallDir ? ', ' + S.answers.fallDir : ''); }
    if (s.type === 'slider') return v + ' ' + s.unit;
    var opts = s.options || [];
    if (Array.isArray(v)) return v.map(function (x) { var o2 = opts.find(function (y) { return y.v === x; }); return o2 ? o2.label : x; }).join(', ');
    var o3 = opts.find(function (y) { return y.v === v; }); return o3 ? o3.label : String(v);
  }
  function review() {
    setScreen('review');
    var list = applicable();
    var rows = list.map(function (s, i) {
      var val = s.type === 'sizes' ? labelFor(s, S.answers.sizes) : labelFor(s, S.answers[s.key]);
      return '<div class="est-row"><div><div class="est-rk">' + esc(s.title) + '</div><div class="est-rv">' + (val ? esc(val) : '<span class="est-miss">' + (s.optional ? 'Skipped' : 'Not answered') + '</span>') + '</div></div><button type="button" class="est-edit" data-i="' + i + '">Change</button></div>';
    }).join('');
    var body = '<p class="est-sec">Check your answers</p><h2 class="est-q">Everything we will price from.</h2><p class="est-hint">Tap Change on anything, or add detail below. More detail means a tighter number.</p>' +
      '<div class="est-rows">' + rows + '</div>' +
      '<div class="field"><label for="rNotes">Anything else we should know? <span class="opt">optional</span></label><textarea id="rNotes" rows="3" placeholder="Finishes you like, a plan you have, a deadline, what the neighbours did…">' + esc(S.answers.notes || '') + '</textarea></div>';
    h(frame({ count: 'Review', pct: 100, body: body, foot: BTN('rBack', 'Back', true) + BTN('rGo', 'See my ballpark') }));
    app.querySelectorAll('.est-edit').forEach(function (b) { b.addEventListener('click', function () { S.i = +b.dataset.i; question(); }); });
    document.getElementById('rBack').addEventListener('click', function () { S.i = list.length - 1; question(); });
    document.getElementById('rGo').addEventListener('click', function () {
      var notes = document.getElementById('rNotes').value.trim(); S.answers.notes = notes;
      api('/answers', { step: 'review', answers: { notes: notes } }).catch(function () {});
      complete();
    });
  }

  // ---- the ballpark -------------------------------------------------------------------------
  function complete() {
    setScreen('ballpark');
    h(frame({ count: 'Your ballpark', body: '<p class="est-hint">Working it out…</p>' }));
    api('/complete', {}).then(function (r) {
      S.result = r; S.completed = true; ga('estimate_ballpark', { lo: r.lo, hi: r.hi });
      var range = (!r.decline && !r.tooUnknown) ? '<div class="est-range"><div class="l">Based on your answers</div><div class="n">$' + fmt(r.lo) + ' <em>to</em> $' + fmt(r.hi) + '</div><p>Including GST. Basic finishes on the low side, Premium on the high side. Subject to the site visit, final measurements and the finishes you choose.</p></div>' : '';
      var inc = r.included.map(function (i) { return '<li class="i"><span>' + esc(i.name) + ', ' + esc(i.qty) + '</span><span>included</span></li>'; }).join('') +
        r.allowed.map(function (a) { return '<li class="i"><span>' + esc(a) + '</span><span>allowed for</span></li>'; }).join('') +
        r.excluded.map(function (x) { return '<li class="x"><span>' + esc(x.name) + '</span><span>' + esc(x.why) + '</span></li>'; }).join('');
      var body = '<p class="est-sec">' + (r.decline ? 'A note on access' : r.tooUnknown ? 'Nearly there' : 'Your ballpark') + '</p>' + range +
        '<h2 class="est-q" style="font-size:1.05rem">' + esc(r.headline) + '</h2>' + r.body.split('\n\n').map(function (p) { return '<p class="est-hint">' + esc(p) + '</p>'; }).join('') +
        (inc ? '<ul class="est-inc">' + inc + '</ul>' : '') +
        '<p class="est-fine">A copy of this is on its way to ' + esc(S.email) + '.</p>';
      h(frame({ count: 'Your ballpark', body: body, foot: BTN('bEdit', 'Change answers', true) + BTN('bNext', r.decline ? 'Book a visit anyway' : 'Next') }));
      document.getElementById('bEdit').addEventListener('click', review);
      document.getElementById('bNext').addEventListener('click', function () { if (r.decline || r.tooUnknown) return book(); reaction(); });
    }).catch(function (e) { if (e.paused) return; if (e.status === 401) return expired(); h(frame({ body: '<p class="est-err">' + esc(e.message) + '</p><div class="btn-row">' + BTN('bRetry', 'Try again') + '</div>' })); document.getElementById('bRetry').addEventListener('click', complete); });
  }
  function fmt(n) { return (n || 0).toLocaleString('en-AU'); }
  function reaction() {
    setScreen('reaction');
    var body = '<p class="est-sec">One quick question</p><h2 class="est-q">Does that sound about right for you?</h2><p class="est-hint">Optional, and it helps us pitch the quote at the right level.</p>' +
      '<div class="est-opts">' + S.reactions.map(function (o) { return '<button type="button" class="est-opt" data-v="' + esc(o.v) + '" aria-pressed="' + (S.answers.priceReaction === o.v) + '">' + esc(o.label) + '</button>'; }).join('') + '</div>';
    h(frame({ count: 'Your ballpark', body: body, foot: BTN('xBack', 'Back', true) + BTN('xSkip', 'Skip') }));
    app.querySelectorAll('.est-opt').forEach(function (b) { b.addEventListener('click', function () { S.answers.priceReaction = b.dataset.v; api('/reaction', { v: b.dataset.v }).catch(function () {}); ga('estimate_reaction', { v: b.dataset.v }); book(); }); });
    document.getElementById('xBack').addEventListener('click', complete);
    document.getElementById('xSkip').addEventListener('click', book);
  }

  // ---- Friday booking -------------------------------------------------------------------------
  function book() {
    setScreen('book');
    h(frame({ count: 'Site visit', body: '<p class="est-hint">Checking Fridays…</p>' }));
    api('/slots').then(function (r) {
      var opts = r.slots.map(function (s) {
        return '<div class="est-day"><div class="est-dayl">' + esc(s.label) + '</div><div class="est-two">' +
          '<button type="button" class="est-opt" data-date="' + s.date + '" data-half="AM"' + (s.am ? '' : ' disabled') + '>Morning' + (s.am ? '' : ' <small>full</small>') + '</button>' +
          '<button type="button" class="est-opt" data-date="' + s.date + '" data-half="PM"' + (s.pm ? '' : ' disabled') + '>Afternoon' + (s.pm ? '' : ' <small>full</small>') + '</button></div></div>';
      }).join('');
      var body = '<p class="est-sec">Site visit</p><h2 class="est-q">Pick a Friday</h2><p class="est-hint">We measure, check the access and falls, and photograph the site. Your itemised quote follows within 48 hours. We have a high number of enquiries at the moment and will do our best to accommodate your pick; we confirm the day before, with an ETA.</p>' +
        opts + '<div class="est-opts" style="margin-top:14px"><button type="button" class="est-opt est-opt-grey" id="kNoFri">Fridays don\'t work for me</button><button type="button" class="est-opt est-opt-grey" id="kLater">Not ready yet, I\'ll come back</button></div>';
      h(frame({ count: 'Site visit', body: body, foot: BTN('kBack', 'Back', true) }));
      document.getElementById('kBack').addEventListener('click', complete);
      app.querySelectorAll('[data-date]').forEach(function (b) {
        b.addEventListener('click', function () {
          b.disabled = true; b.textContent = 'Booking…';
          api('/book', { date: b.dataset.date, half: b.dataset.half }).then(function (res) { S.booked = true; ga('estimate_visit_booked'); files(res); })
            .catch(function (e) { if (e.paused) return; if (e.status === 401) return expired(); alert(e.message); book(); });
        });
      });
      document.getElementById('kNoFri').addEventListener('click', function () { api('/not-ready', { reason: 'fridays' }).catch(function () {}); files(null, 'nofri'); });
      document.getElementById('kLater').addEventListener('click', function () { api('/not-ready', { reason: 'later' }).catch(function () {}); files(null, 'later'); });
    }).catch(function (e) { if (e.paused) return; if (e.status === 401) return expired(); files(null, 'error'); });
  }

  // ---- photos and drawings (optional) ----------------------------------------------------------
  var CHUNK = 5 * 1024 * 1024;
  function putFile(f, url, onBytes) {
    var pos = 0;
    function chunk(retried) {
      var end = Math.min(pos + CHUNK, f.size);
      return fetch(url, { method: 'PUT', headers: { 'Content-Range': 'bytes ' + pos + '-' + (end - 1) + '/' + f.size }, body: f.slice(pos, end) })
        .then(function (r) { if (!r.ok && r.status !== 202) throw new Error('upload ' + r.status); onBytes(end - pos); pos = end; return step(); },
          function (err) { if (retried) throw err; return new Promise(function (res) { setTimeout(res, 800); }).then(function () { return chunk(true); }); });
    }
    function step() { return pos >= f.size ? Promise.resolve() : chunk(false); }
    return step();
  }
  function files(booking, why) {
    setScreen('files');
    var lead = booking ? '<p class="est-sec">Booked</p><h2 class="est-q">' + esc(booking.label) + ', ' + (booking.half === 'AM' ? 'morning' : 'afternoon') + '.</h2><p class="est-hint">We will confirm the day before with an ETA. A confirmation is on its way to your email.</p>'
      : why === 'nofri' ? '<p class="est-sec">No problem</p><h2 class="est-q">We will call to find a day that works.</h2>'
      : '<p class="est-sec">Whenever you are ready</p><h2 class="est-q">Your code keeps working, so come back any time.</h2>';
    var body = lead + '<h3 class="est-h3">Add photos or drawings <span class="opt">optional</span></h3><p class="est-hint">Front, back and the side access help most. Builder drawings or a landscape plan mean a tighter number on the day.</p>' +
      '<label class="est-drop"><input type="file" id="fIn" multiple accept=".pdf,.jpg,.jpeg,.png,.heic,.heif,.webp,.dwg,.doc,.docx,.xls,.xlsx,.zip"><span>+ Choose files</span></label><div id="fList" class="est-flist"></div><div id="fMsg" class="est-hint"></div>';
    h(frame({ count: 'Last step', body: body, foot: BTN('fSkip', 'Finish', true) + BTN('fUp', 'Upload and finish') }));
    var picked = [];
    document.getElementById('fIn').addEventListener('change', function () { picked = [].slice.call(this.files, 0, 20); document.getElementById('fList').innerHTML = picked.map(function (f) { return '<div>' + esc(f.name) + ' <span class="est-fine">' + (f.size / 1e6).toFixed(1) + ' MB</span></div>'; }).join(''); });
    document.getElementById('fSkip').addEventListener('click', function () { done(booking); });
    document.getElementById('fUp').addEventListener('click', function () {
      if (!picked.length) return done(booking);
      var btn = this; btn.disabled = true; btn.textContent = 'Uploading…'; var msg = document.getElementById('fMsg');
      api('/files', { files: picked.map(function (f) { return { name: f.name, size: f.size }; }) }).then(function (r) {
        var ok = [], bad = [], total = picked.reduce(function (a, f) { return a + f.size; }, 0), sent = 0;
        return picked.reduce(function (p, f, i) {
          return p.then(function () {
            var u = r.uploads[i]; if (!u || !u.uploadUrl) { bad.push(f.name); return; }
            return putFile(f, u.uploadUrl, function (n) { sent += n; msg.textContent = 'Uploading… ' + Math.round(100 * sent / total) + '%'; }).then(function () { ok.push(u.name || f.name); }, function () { bad.push(f.name); });
          });
        }, Promise.resolve()).then(function () {
          return api('/files/complete', { uploaded: ok }).catch(function () {}).then(function () { ga('estimate_files', { n: ok.length }); done(booking, ok, bad); });
        });
      }).catch(function (e) { msg.innerHTML = '<span class="est-err">' + esc(e.message) + '</span>'; btn.disabled = false; btn.textContent = 'Try again'; });
    });
  }
  function done(booking, ok, bad) {
    setScreen('done'); flush();
    var body = '<p class="est-sec">All done</p><h2 class="est-q">Thanks' + (S.first ? ', ' + esc(S.first) : '') + '.</h2>' +
      (booking ? '<p class="est-hint">Your site visit is pencilled in for <b>' + esc(booking.label) + ', ' + (booking.half === 'AM' ? 'morning' : 'afternoon') + '</b>. We confirm the day before with an ETA.</p>' : '<p class="est-hint">Your answers and your ballpark are saved. We will give you a call to confirm the details.</p>') +
      (ok && ok.length ? '<p class="est-hint">Files received: ' + esc(ok.join(', ')) + '.</p>' : '') +
      (bad && bad.length ? '<p class="est-err">These did not upload: ' + esc(bad.join(', ')) + '. Email them to enquiry@estatelandscapers.com.au.</p>' : '') +
      '<p class="est-hint">Your code keeps working until ' + esc(String(S.expires || '').slice(0, 10)) + ', so you can change answers any time.</p>' +
      '<div class="btn-row">' + BTN('dBall', 'See my ballpark again', true) + '<a class="btn" href="/projects/">See our projects</a></div>';
    h(frame({ count: 'Done', body: body }));
    document.getElementById('dBall').addEventListener('click', complete);
  }

  // ---- boot ----------------------------------------------------------------------------------
  if (S.token) {
    // A token from this browser session: try to resume without the code screen.
    api('/auth-resume', {}).then(function (r) { S.first = r.first || ''; S.steps = r.steps; S.sizes = r.sizes; S.answers = r.answers || {}; S.reactions = r.reactions; S.expires = r.expires; S.completed = !!r.completed; S.booked = !!r.booked; S.saved = r.saved || 0; S.email = r.email || S.email; welcome(); })
      .catch(function (e) { S.token = null; if (!e.paused) gate(null, qs.get('get') ? 'get' : 'code'); });
  } else gate(null, qs.get('get') ? 'get' : 'code');
})();
