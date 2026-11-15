(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var root = document.documentElement;

  /* header state */
  var header = document.querySelector('.site-header');
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 20); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* mobile menu */
  var btn = document.querySelector('.menu-btn');
  if (btn) {
    btn.addEventListener('click', function () {
      var open = !root.classList.contains('menu-open');
      root.classList.toggle('menu-open', open);
      btn.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && root.classList.contains('menu-open')) btn.click();
    });
  }

  /* cursor glow */
  var glow = document.querySelector('.glow');
  if (glow && !reduce) {
    var gx = innerWidth / 2, gy = innerHeight / 3, tx = gx, ty = gy;
    addEventListener('pointermove', function (e) { tx = e.clientX; ty = e.clientY; });
    (function loop() { gx += (tx - gx) * .08; gy += (ty - gy) * .08; glow.style.transform = 'translate(' + gx + 'px,' + gy + 'px)'; requestAnimationFrame(loop); })();
  }

  /* magnetic buttons */
  if (!reduce && matchMedia('(hover:hover)').matches) {
    document.querySelectorAll('.btn').forEach(function (b) {
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.setProperty('--x', ((e.clientX - r.left - r.width / 2) * .2) + 'px');
        b.style.setProperty('--y', ((e.clientY - r.top - r.height / 2) * .3) + 'px');
      });
      b.addEventListener('pointerleave', function () { b.style.setProperty('--x', '0px'); b.style.setProperty('--y', '0px'); });
    });
  }

  /* reveal on scroll */
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: .12, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });

  /* route path lengths */
  document.querySelectorAll('.route-path').forEach(function (p) {
    p.style.setProperty('--len', Math.ceil(p.getTotalLength()));
  });

  /* runner dot on hero route */
  var hp = document.querySelector('.hero .route-path'), runner = document.querySelector('.hero .runner');
  if (hp && runner && !reduce) {
    var L = hp.getTotalLength(), t0 = null;
    (function run(ts) {
      if (t0 === null) t0 = ts;
      var t = ((ts - t0 - 3700) / 9000);
      if (t > 0) { var pt = hp.getPointAtLength((t % 1) * L); runner.setAttribute('cx', pt.x); runner.setAttribute('cy', pt.y); runner.style.opacity = 1; }
      requestAnimationFrame(run);
    })(performance.now());
  }

  /* scroll-driven route story */
  var story = document.querySelector('.story');
  if (story) {
    var sp = story.querySelector('.route-path'), sr = story.querySelector('.runner'), steps = story.querySelectorAll('.step');
    var SL = sp.getTotalLength();
    function upd() {
      var r = story.getBoundingClientRect(), h = innerHeight;
      var p = Math.min(1, Math.max(0, (h * .55 - r.top) / (r.height - h * .3)));
      sp.style.setProperty('--p', p);
      var pt = sp.getPointAtLength(p * SL); sr.setAttribute('cx', pt.x); sr.setAttribute('cy', pt.y);
      steps.forEach(function (s) { var b = s.getBoundingClientRect(); s.classList.toggle('on', b.top < h * .7 && b.bottom > h * .2); });
    }
    addEventListener('scroll', upd, { passive: true }); addEventListener('resize', upd); upd();
  }

  /* countdown */
  var cd = document.querySelector('.countdown');
  if (cd) {
    var target = new Date(cd.dataset.date).getTime();
    var els = cd.querySelectorAll('b');
    function tick() {
      var d = Math.max(0, target - Date.now());
      var v = [Math.floor(d / 864e5), Math.floor(d / 36e5) % 24, Math.floor(d / 6e4) % 60, Math.floor(d / 1e3) % 60];
      v.forEach(function (n, i) { els[i].textContent = i ? String(n).padStart(2, '0') : n; });
    }
    tick(); setInterval(tick, 1000);
  }

  /* counters */
  var co = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return; co.unobserve(e.target);
      var el = e.target, end = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length, t0 = null;
      if (reduce) { el.textContent = end.toFixed(dec).replace('.', ','); return; }
      (function f(ts) { if (t0 === null) t0 = ts; var k = Math.min(1, (ts - t0) / 1600); k = 1 - Math.pow(1 - k, 3);
        el.textContent = (end * k).toFixed(dec).replace('.', ','); if (k < 1) requestAnimationFrame(f); })(performance.now());
    });
  }, { threshold: .5 });
  document.querySelectorAll('[data-count]').forEach(function (el) { co.observe(el); });
})();
