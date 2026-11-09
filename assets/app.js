/* ATS Trockenbau – Interaktionen */
(function () {
  var d = document, root = d.documentElement;
  root.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var header = d.querySelector('.site-header');

  /* Jahr */
  var y = d.getElementById('year');
  if (y) y.textContent = String(new Date().getFullYear());

  /* Mobiles Menü */
  var menuBtn = d.querySelector('.menu-btn');
  var menu = d.getElementById('menu');
  function setMenu(open) {
    if (!menu) return;
    root.toggleAttribute('data-menu', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü');
    menu.inert = !open;
  }
  if (menuBtn && menu) {
    menuBtn.addEventListener('click', function () { setMenu(!root.hasAttribute('data-menu')); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
    window.matchMedia('(min-width: 64rem)').addEventListener('change', function (e) { if (e.matches) setMenu(false); });
  }

  /* Aktiver Menüpunkt mit gleitender Markierung */
  var links = Array.prototype.slice.call(d.querySelectorAll('.nav-links a[href^="#"]'));
  var indicator = d.querySelector('.nav-indicator');
  function mark(id) {
    var active = null;
    links.forEach(function (a) {
      var on = a.getAttribute('href') === '#' + id;
      if (on) { a.setAttribute('aria-current', 'true'); active = a; } else a.removeAttribute('aria-current');
    });
    if (!indicator) return;
    if (!active) { indicator.style.opacity = '0'; return; }
    indicator.style.opacity = '1';
    indicator.style.width = active.offsetWidth + 'px';
    indicator.style.transform = 'translateX(' + active.offsetLeft + 'px)';
  }
  if ('IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) mark(e.target.id); });
    }, { rootMargin: '-45% 0px -54% 0px' });
    d.querySelectorAll('main > section[id]').forEach(function (s) { spy.observe(s); });
  }

  /* Wand-Geschichte: Schritt aus Scrollposition */
  var build = d.querySelector('.build');
  var stage = d.querySelector('.build-stage');
  var wall = d.querySelector('.wall');
  var items = Array.prototype.slice.call(d.querySelectorAll('.story-item'));
  var last = -1;
  function setStep(n) {
    if (n === last) return;
    last = n;
    for (var i = 1; i <= 5; i++) wall.classList.toggle('s' + i, i <= n);
    var act = Math.max(n, 1) - 1;
    items.forEach(function (it, i) { it.classList.toggle('is-active', i === act); });
  }
  if (build && stage && wall) {
    if (reduce) {
      setStep(5);
      items.forEach(function (it) { it.classList.add('is-active'); });
    } else {
      var ticking = false;
      var update = function () {
        ticking = false;
        var r = build.getBoundingClientRect();
        var top = header ? header.getBoundingClientRect().bottom : 0;
        var total = Math.max(1, build.offsetHeight - stage.offsetHeight);
        var p = Math.min(1, Math.max(0, (top - r.top) / total));
        build.style.setProperty('--p', p.toFixed(4));
        var n = r.top < window.innerHeight * 0.55 ? Math.min(5, Math.floor(p * 5) + 1) : 0;
        if (r.bottom < 0) n = 5;
        setStep(n);
      };
      window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
      window.addEventListener('resize', update);
      update();
    }
  }

  /* Leistungs-Schiene: Pfeile */
  d.querySelectorAll('[data-rail]').forEach(function (wrap) {
    var rail = wrap.querySelector('.rail');
    var prev = wrap.querySelector('[data-prev]');
    var next = wrap.querySelector('[data-next]');
    var stepW = function () { var c = rail.querySelector('.card'); return (c ? c.offsetWidth : 300) + 16; };
    var upd = function () {
      prev.disabled = rail.scrollLeft < 8;
      next.disabled = rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 8;
    };
    prev.addEventListener('click', function () { rail.scrollBy({ left: -stepW(), behavior: reduce ? 'auto' : 'smooth' }); });
    next.addEventListener('click', function () { rail.scrollBy({ left: stepW(), behavior: reduce ? 'auto' : 'smooth' }); });
    rail.addEventListener('scroll', upd, { passive: true });
    window.addEventListener('resize', upd);
    upd();
  });

  /* Q-Stufen */
  var seg = d.querySelector('.seg');
  if (seg) {
    var tabs = Array.prototype.slice.call(seg.querySelectorAll('[role="tab"]'));
    var panes = Array.prototype.slice.call(d.querySelectorAll('.q-pane'));
    var svgs = Array.prototype.slice.call(d.querySelectorAll('.q-svg'));
    var select = function (i, focus) {
      seg.style.setProperty('--q', i);
      tabs.forEach(function (t, j) { t.setAttribute('aria-selected', String(j === i)); t.tabIndex = j === i ? 0 : -1; });
      panes.forEach(function (p, j) { p.classList.toggle('is-active', j === i); });
      svgs.forEach(function (s, j) { s.classList.toggle('is-active', j === i); });
      if (focus) tabs[i].focus();
    };
    tabs.forEach(function (t, i) { t.addEventListener('click', function () { select(i); }); });
    seg.addEventListener('keydown', function (e) {
      var cur = tabs.findIndex(function (t) { return t.getAttribute('aria-selected') === 'true'; });
      if (e.key === 'ArrowRight') { e.preventDefault(); select((cur + 1) % 4, true); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); select((cur + 3) % 4, true); }
    });
    select(1);
  }

  /* Mobile Aktionsleiste: sichtbar zwischen Hero und Kontakt */
  var dock = d.querySelector('.dock');
  var hero = d.querySelector('.hero');
  var contact = d.getElementById('kontakt');
  if (dock && hero && contact && 'IntersectionObserver' in window) {
    var heroVis = true, contactVis = false;
    var sync = function () { dock.classList.toggle('is-visible', !heroVis && !contactVis); };
    new IntersectionObserver(function (e) { heroVis = e[0].isIntersecting; sync(); }).observe(hero);
    new IntersectionObserver(function (e) { contactVis = e[0].isIntersecting; sync(); }).observe(contact);
  }

  /* Projekt-Galerie: Vollbild */
  var lb = d.getElementById('lightbox');
  var shots = Array.prototype.slice.call(d.querySelectorAll('.shot-btn'));
  if (lb && shots.length && typeof lb.showModal === 'function') {
    var lbImg = lb.querySelector('img'), lbCap = lb.querySelector('figcaption'), cur = 0, startX = null;
    var show = function (i) {
      cur = (i + shots.length) % shots.length;
      lbImg.src = shots[cur].getAttribute('data-full');
      lbImg.alt = shots[cur].getAttribute('data-cap');
      lbCap.textContent = shots[cur].getAttribute('data-cap') + '  ·  ' + (cur + 1) + ' / ' + shots.length;
    };
    shots.forEach(function (b, i) { b.addEventListener('click', function () { show(i); lb.showModal(); }); });
    lb.querySelector('.lb-close').addEventListener('click', function () { lb.close(); });
    lb.querySelector('.lb-prev').addEventListener('click', function () { show(cur - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
    lb.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') show(cur + 1);
      if (e.key === 'ArrowLeft') show(cur - 1);
    });
    lb.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (startX === null) return;
      var dx = e.changedTouches[0].clientX - startX; startX = null;
      if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1));
    });
  }

  /* Anfrageformular */
  var form = d.getElementById('anfrage');
  var status = d.getElementById('form-status');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var missing = [];
      if (!form.name.value.trim()) missing.push('Name');
      if (!/^\S+@\S+\.\S+$/.test(form.email.value.trim())) missing.push('gültige E-Mail');
      if (!form.nachricht.value.trim()) missing.push('Vorhaben');
      if (!form.datenschutz.checked) missing.push('Einverständnis zum Datenschutz');
      if (missing.length) { status.textContent = 'Bitte ergänzen: ' + missing.join(', ') + '.'; return; }
      var to = form.getAttribute('data-mail');
      var projekt = (form.querySelector('input[name="projekt"]:checked') || {}).value || 'Anfrage';
      var body = 'Projekt: ' + projekt + '\nName: ' + form.name.value + '\nTelefon: ' + form.telefon.value +
        '\nE-Mail: ' + form.email.value + '\nOrt: ' + form.ort.value + '\n\n' + form.nachricht.value;
      window.location.href = 'mailto:' + to + '?subject=' + encodeURIComponent('Anfrage: ' + projekt) + '&body=' + encodeURIComponent(body);
      status.textContent = 'Ihr E-Mail-Programm öffnet sich mit der fertigen Anfrage. Bitte dort auf Senden tippen.';
    });
  }
})();
