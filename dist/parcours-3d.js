(function () {
  var el = document.getElementById('map3d');
  if (!el || !window.maplibregl) return;
  var VIEWS = {
    '5km': { center: [1.4378, 43.6010], zoom: 14.6, pitch: 60, bearing: -25 },
    '10km': { center: [1.4372, 43.5950], zoom: 14.3, pitch: 58, bearing: -20 }
  };
  Promise.all(['5km', '10km'].map(function (k) { return fetch('assets/parcours-' + k + '.geojson').then(function (r) { return r.json(); }); })).then(function (fs) {
    var ROUTES = { '5km': fs[0], '10km': fs[1] }, cur = '5km', line, cum, total, start, markers = [];
    var map = new maplibregl.Map({ container: el, style: 'https://tiles.openfreemap.org/styles/liberty', center: VIEWS[cur].center, zoom: VIEWS[cur].zoom, pitch: VIEWS[cur].pitch, bearing: VIEWS[cur].bearing, maxPitch: 80, attributionControl: { compact: true }, cooperativeGestures: true });
    map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'top-right');

    function dist(a, b) { var x = (b[0] - a[0]) * Math.PI / 180 * Math.cos(a[1] * Math.PI / 180), y = (b[1] - a[1]) * Math.PI / 180; return 6371000 * Math.sqrt(x * x + y * y); }
    function at(s) { s = Math.max(0, Math.min(total, s)); var i = 1; while (i < cum.length - 1 && cum[i] < s) i++; var t = (s - cum[i - 1]) / Math.max(cum[i] - cum[i - 1], 1e-9); return [line[i - 1][0] + (line[i][0] - line[i - 1][0]) * t, line[i - 1][1] + (line[i][1] - line[i - 1][1]) * t]; }
    function bearing(a, b) { var r = Math.PI / 180, y = Math.sin((b[0] - a[0]) * r) * Math.cos(b[1] * r), x = Math.cos(a[1] * r) * Math.sin(b[1] * r) - Math.sin(a[1] * r) * Math.cos(b[1] * r) * Math.cos((b[0] - a[0]) * r); return (Math.atan2(y, x) / r + 360) % 360; }
    function prep(k) {
      line = ROUTES[k].geometry.coordinates; start = line[0]; cum = [0];
      for (var i = 1; i < line.length; i++) cum.push(cum[i - 1] + dist(line[i - 1], line[i]));
      total = cum[cum.length - 1];
    }
    prep(cur);

    function drawMarkers() {
      markers.forEach(function (m) { m.remove(); }); markers = [];
      for (var k = 1; k * 1000 < total - 300; k++) { var d = document.createElement('div'); d.className = 'km-marker'; d.textContent = k + ' km'; markers.push(new maplibregl.Marker({ element: d }).setLngLat(at(k * 1000)).addTo(map)); }
      var s = document.createElement('div'); s.className = 'start-marker'; s.textContent = 'Départ · Arrivée';
      markers.push(new maplibregl.Marker({ element: s, anchor: 'bottom', offset: [0, -6] }).setLngLat(start).addTo(map));
    }

    map.on('load', function () {
      // teinte rose sur les bâtiments 3D du style
      map.getStyle().layers.forEach(function (l) {
        if (l.type === 'fill-extrusion') { map.setPaintProperty(l.id, 'fill-extrusion-color', '#f4d3e2'); map.setPaintProperty(l.id, 'fill-extrusion-opacity', .85); }
      });
      map.addSource('route', { type: 'geojson', data: ROUTES[cur], lineMetrics: true });
      map.addSource('done', { type: 'geojson', data: { type: 'Feature', geometry: { type: 'LineString', coordinates: [start, start] } } });
      map.addLayer({ id: 'route-glow', type: 'line', source: 'route', layout: { 'line-join': 'round', 'line-cap': 'round' }, paint: { 'line-color': '#ff3d97', 'line-width': 22, 'line-blur': 14, 'line-opacity': .55 } });
      map.addLayer({ id: 'route-halo', type: 'line', source: 'route', layout: { 'line-join': 'round', 'line-cap': 'round' }, paint: { 'line-color': '#fff', 'line-width': 10 } });
      map.addLayer({ id: 'route-line', type: 'line', source: 'route', layout: { 'line-join': 'round', 'line-cap': 'round' }, paint: { 'line-width': 6, 'line-gradient': ['interpolate', ['linear'], ['line-progress'], 0, '#ff3d97', .5, '#b0115f', 1, '#ff3d97'] } });
      map.addLayer({ id: 'route-done', type: 'line', source: 'done', layout: { 'line-join': 'round', 'line-cap': 'round' }, paint: { 'line-color': '#14040c', 'line-width': 4 } });
      drawMarkers();
    });

    var anim = null, btn = document.getElementById('fly-btn'), bar = document.querySelector('.map-progress i'), kmEl = document.querySelector('.map-km');
    function setDone(s) {
      var c = [line[0]]; for (var i = 1; i < line.length && cum[i] < s; i++) c.push(line[i]); c.push(at(s));
      var src = map.getSource('done'); if (src) src.setData({ type: 'Feature', geometry: { type: 'LineString', coordinates: c } });
      bar.style.width = (s / total * 100) + '%'; kmEl.textContent = (s / 1000).toFixed(2).replace('.', ',') + ' km';
    }
    function stop() { if (anim) { cancelAnimationFrame(anim); anim = null; } btn.innerHTML = '▶&nbsp; Survoler le parcours'; }
    btn.addEventListener('click', function () {
      if (anim) { stop(); return; }
      btn.innerHTML = '❚❚&nbsp; Pause';
      var t0 = null, dur = cur === '10km' ? 90000 : 55000, lastB = null;
      function step(ts) {
        if (t0 === null) t0 = ts; var p = (ts - t0) / dur;
        if (p >= 1) { setDone(total); stop(); map.flyTo(Object.assign({ duration: 2500 }, VIEWS[cur])); return; }
        var s = p * total, c = at(s), b = bearing(c, at(s + 150));
        lastB = lastB === null ? b : lastB + ((((b - lastB) % 360) + 540) % 360 - 180) * .05;
        map.jumpTo({ center: c, bearing: lastB, pitch: 70, zoom: 16.6 }); setDone(s);
        anim = requestAnimationFrame(step);
      }
      map.flyTo({ center: start, zoom: 16.6, pitch: 70, bearing: bearing(start, at(150)), duration: 1500 });
      setTimeout(function () { anim = requestAnimationFrame(step); }, 1500);
    });
    ['mousedown', 'wheel', 'touchstart'].forEach(function (e) { el.addEventListener(e, function () { if (anim) stop(); }, { passive: true }); });
    document.getElementById('reset-btn').addEventListener('click', function () { stop(); setDone(0); map.flyTo(Object.assign({ duration: 1800 }, VIEWS[cur])); });

    var tabs = document.querySelectorAll('.route-tab');
    Array.prototype.forEach.call(tabs, function (t) {
      t.addEventListener('click', function () {
        var k = t.getAttribute('data-route'); if (k === cur) return;
        stop(); cur = k; prep(k);
        Array.prototype.forEach.call(tabs, function (o) { var on = o === t; o.classList.toggle('on', on); o.classList.toggle('ghost', !on); o.setAttribute('aria-pressed', on ? 'true' : 'false'); });
        var src = map.getSource('route'); if (src) src.setData(ROUTES[k]);
        setDone(0); drawMarkers(); map.flyTo(Object.assign({ duration: 1800 }, VIEWS[k]));
      });
    });
  });
})();
