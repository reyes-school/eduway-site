/* EduWay shelf hero — endless 3D shelf of role boxes. Vanilla JS, one rAF loop + Web Animations API. */
(function () {
  var d = document, hero = d.getElementById("shf");
  if (!hero) return;
  var DATA = JSON.parse(d.getElementById("shf-data").textContent);
  var R = DATA.roles, N = R.length, COPIES = 6, TOT = N * COPIES;
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var EASE = "cubic-bezier(.2,.8,.2,1)", SHEET_EASE = "cubic-bezier(.76,0,.18,1)";
  var shelf = hero.querySelector(".shf-shelf"), stage = hero.querySelector(".shf-stage");
  var play = hero.querySelector(".shf-play"), detail = d.querySelector(".shf-detail");
  var cur = d.querySelector(".shf-cursor");
  var tabs = [].slice.call(hero.querySelectorAll(".shf-tab")), ind = hero.querySelector(".shf-ind");
  var capT = hero.querySelector(".shf-t"), capS = hero.querySelector(".shf-s"), capY = hero.querySelector(".shf-y");
  var pad = function (n) { return (n < 10 ? "0" : "") + n; };

  // ---- build tapes
  var tapes = [];
  for (var v = 0; v < TOT; v++) {
    var i = v % N, id = R[i].id, el = d.createElement("div");
    el.className = "shf-tape";
    el.setAttribute("aria-hidden", "true");
    el.innerHTML = '<div class="shf-sp"><svg viewBox="0 0 142 840" preserveAspectRatio="none"><use href="#shf-sp-' + id + '" width="142" height="840"/></svg></div>' +
      '<div class="shf-cv"><svg viewBox="0 0 474 900" preserveAspectRatio="none"><use href="#shf-cv-' + id + '" width="474" height="900"/></svg></div>';
    stage.appendChild(el);
    var t = { v: v, i: i, el: el, sp: el.firstChild, cv: el.lastChild, lift: 0, liftT: 0, vis: true, shS: -1, shC: -1 };
    (function (t) {
      el.addEventListener("pointerenter", function () { hover = t.v; t.liftT = 1; });
      el.addEventListener("pointerleave", function () { if (hover === t.v) hover = -1; t.liftT = 0; });
      el.addEventListener("click", function () {
        if (dragged) return;
        var r = rel(t.v);
        if (Math.abs(r) < .5) openDetail(); else T = Math.round(T + r);
      });
    })(t);
    tapes.push(t);
  }

  // ---- geometry
  var H, ws, dd, gap, W;
  var probe = d.createElement("div");
  probe.style.cssText = "position:absolute;visibility:hidden;height:var(--H);width:1px;left:-9px;top:0";
  hero.appendChild(probe);
  function measure() {
    H = probe.getBoundingClientRect().height || 360;
    ws = H * 142 / 840; dd = H * 474 / 900; gap = H * .03; W = shelf.clientWidth;
    stage.style.setProperty("--ws", ws + "px"); stage.style.setProperty("--d", dd + "px");
    moveInd();
  }

  // ---- state
  var start = N * Math.floor(COPIES / 2); // middle copy, role 0
  var s = start, T = start, hover = -1, active = -1, dragging = false, dragged = false;
  var mx = innerWidth / 2, my = innerHeight / 2, cx = mx, cy = my, tiltX = 0, tiltY = 0, onCover = false, isOpen = false;
  var inZone = false, shelfCY = 0, shelfCX = 0;

  function wrap(x) { x = ((x % TOT) + TOT) % TOT; return x >= TOT / 2 ? x - TOT : x; }
  function rel(v) { return wrap(v - s); }
  function B(r) { return Math.abs(r) < 1 ? (r + Math.sin(Math.PI * r) / Math.PI) / 2 : (r > 0 ? .5 : -.5); }
  function F(r) { return r * (ws + gap) + (dd - ws + 1.6 * gap) * B(r); }
  function sst(x) { return x * x * (3 - 2 * x); }
  function mod(n) { return ((n % N) + N) % N; }

  // ---- caption swap through masks
  function swap(mask, text, dir) {
    var old = [].slice.call(mask.children);
    var sp = d.createElement("span"); sp.textContent = text;
    mask.appendChild(sp);
    if (reduce) { old.forEach(function (o) { o.remove(); }); return; }
    sp.animate([{ transform: "translateY(" + dir * 105 + "%)" }, { transform: "translateY(0)" }], { duration: 650, easing: EASE, fill: "both" });
    old.forEach(function (o) {
      if (o._leaving) return;
      o._leaving = true;
      var from = getComputedStyle(o).transform; if (from === "none") from = "translateY(0)";
      var a = o.animate([{ transform: from }, { transform: "translateY(" + -dir * 105 + "%)" }], { duration: 650, easing: EASE, fill: "both" });
      a.onfinish = function () { o.remove(); };
    });
  }
  function setActive(i, dir) {
    if (i === active) return;
    var first = active < 0; active = i;
    var r = R[i];
    if (!first) {
      swap(capT, r.name, dir); swap(capS, r.sub, dir);
      swap(capY, DATA.role + " " + pad(i + 1) + " / " + pad(N), dir);
    }
    moveInd();
  }
  function moveInd() {
    if (active < 0) return;
    var g = R[active].g, on = null;
    tabs.forEach(function (b) { var x = b.dataset.g === g; b.classList.toggle("on", x); if (x) on = b; });
    if (on) { ind.style.width = on.offsetWidth + "px"; ind.style.transform = "translateX(" + on.offsetLeft + "px)"; }
  }
  tabs.forEach(function (b) {
    b.addEventListener("click", function () {
      var g = b.dataset.g, target = 0;
      if (g !== "all") for (var k = 0; k < N; k++) if (R[k].g === g) { target = k; break; }
      var base = Math.round(T), diff = mod(target - mod(base));
      if (diff > N / 2) diff -= N;
      T = base + diff;
    });
  });

  // ---- inputs
  hero.querySelector(".shf-prev").addEventListener("click", function () { T = Math.round(T) - 1; });
  hero.querySelector(".shf-next").addEventListener("click", function () { T = Math.round(T) + 1; });
  play.addEventListener("click", function () { openDetail(); });

  function heroVisible() { var r = hero.getBoundingClientRect(); return r.bottom > innerHeight * .4 && r.top < innerHeight * .5; }
  d.addEventListener("keydown", function (e) {
    if (isOpen) { if (e.key === "Escape") closeDetail(); return; }
    var a = d.activeElement, free = !a || a === d.body || hero.contains(a);
    if (!free || !heroVisible()) return;
    if (e.key === "ArrowLeft") { T = Math.round(T) - 1; e.preventDefault(); }
    else if (e.key === "ArrowRight") { T = Math.round(T) + 1; e.preventDefault(); }
    else if (e.key === "Enter" && (!a || a === d.body)) { openDetail(); e.preventDefault(); }
  });

  var wheelTimer = 0;
  shelf.addEventListener("wheel", function (e) {
    if (isOpen) return;
    var dx = e.deltaX, dy = e.deltaY;
    var horiz = Math.abs(dx) > Math.abs(dy) || e.shiftKey;
    if (!horiz) return; // vertical wheel keeps scrolling the page
    e.preventDefault();
    var delta = Math.abs(dx) > Math.abs(dy) ? dx : dy;
    T += delta / (ws + gap) * .5;
    clearTimeout(wheelTimer);
    wheelTimer = setTimeout(function () { T = Math.round(T); }, 160);
  }, { passive: false });

  var x0 = 0, T0 = 0, down = false;
  shelf.addEventListener("pointerdown", function (e) {
    if (e.button !== 0 || e.target.closest(".shf-play")) return;
    down = true; dragged = false; x0 = e.clientX; T0 = T;
  });
  addEventListener("pointermove", function (e) {
    mx = e.clientX; my = e.clientY;
    var t = e.target;
    inZone = !!(t && t.closest && (t.closest(".shf") || t.closest(".shf-detail")));
    if (!down) return;
    var dx = e.clientX - x0;
    if (!dragging && Math.abs(dx) > 5) { dragging = true; dragged = true; }
    if (dragging) T = T0 - dx / (ws + gap);
  }, { passive: true });
  function up() {
    if (!down) return;
    down = false;
    if (dragging) { dragging = false; T = Math.round(T); setTimeout(function () { dragged = false; }, 0); }
  }
  addEventListener("pointerup", up); addEventListener("pointercancel", up);
  d.addEventListener("pointerleave", function () { inZone = false; });

  // ---- detail sheet
  var dS = detail.querySelector(".shf-ds"), dH = detail.querySelector(".shf-dh"), dM = detail.querySelector(".shf-dmeta");
  var dSum = detail.querySelector(".shf-dsum"), dList = detail.querySelector(".shf-dlist"), puse = detail.querySelector(".shf-puse");
  var blobs = [].slice.call(detail.querySelectorAll("mask circle")), DEL = [0, 120, 220, 300, 360, 420, 180];
  var sheetAnim = null, inkRaf = 0, lastFocus = null;

  function coverRect() {
    var t = tapes.filter(function (t) { return Math.abs(rel(t.v)) < .5; })[0];
    return (t ? t.cv : shelf).getBoundingClientRect();
  }
  function insetFrom(r) {
    var vw = innerWidth, vh = innerHeight;
    return "inset(" + Math.max(0, r.top) + "px " + Math.max(0, vw - r.right) + "px " + Math.max(0, vh - r.bottom) + "px " + Math.max(0, r.left) + "px round 3px)";
  }
  function openDetail() {
    if (isOpen) return;
    isOpen = true; T = Math.round(T);
    var r = R[active];
    dS.textContent = r.sub;
    dH.textContent = r.name;
    dM.textContent = DATA.role + " " + pad(active + 1) + " / " + pad(N) + " · WEB · iOS · ANDROID · " + r.list.length + " " + DATA.items;
    dSum.textContent = r.sum;
    dList.innerHTML = "";
    r.list.forEach(function (x) { var li = d.createElement("li"); li.className = "shf-m"; var sp = d.createElement("span"); sp.textContent = x; li.appendChild(sp); dList.appendChild(li); });
    puse.setAttribute("href", "#shf-cv-" + r.id);
    blobs.forEach(function (b) { b.setAttribute("r", 0); });
    var rc = coverRect();
    lastFocus = d.activeElement;
    detail.classList.add("open");
    detail.scrollTop = 0;
    d.body.classList.add("noscroll");
    detail.style.transformOrigin = (rc.left + rc.width / 2) + "px " + (rc.top + rc.height / 2) + "px";
    var dur = reduce ? 1 : 1050;
    if (sheetAnim) sheetAnim.cancel();
    sheetAnim = detail.animate([
      { clipPath: insetFrom(rc), transform: "rotate(-4.5deg)" },
      { clipPath: "inset(0px 0px 0px 0px round 0px)", transform: "rotate(0deg)" }
    ], { duration: dur, easing: SHEET_EASE, fill: "both" });
    [].slice.call(detail.querySelectorAll(".shf-m > *")).forEach(function (el, k) {
      el.animate([{ transform: "translateY(110%)" }, { transform: "translateY(0)" }],
        { duration: reduce ? 1 : 900, delay: reduce ? 0 : 620 + k * 75, easing: EASE, fill: "both" });
    });
    var t0 = performance.now() + (reduce ? -5000 : 520);
    cancelAnimationFrame(inkRaf);
    (function ink(now) {
      var el = now - t0;
      blobs.forEach(function (b, k) {
        var p = Math.min(1, Math.max(0, (el - DEL[k]) / 1250));
        b.setAttribute("r", (720 * (1 - Math.pow(1 - p, 3))).toFixed(1));
      });
      if (el < 2400) inkRaf = requestAnimationFrame(ink);
    })(performance.now());
    setTimeout(function () { detail.querySelector(".shf-close").focus({ preventScroll: true }); }, reduce ? 0 : 700);
  }
  function closeDetail(after) {
    if (!isOpen) return;
    var rc = coverRect();
    var a = detail.animate([
      { clipPath: "inset(0px 0px 0px 0px round 0px)", transform: "rotate(0deg)" },
      { clipPath: insetFrom(rc), transform: "rotate(-4.5deg)" }
    ], { duration: reduce ? 1 : 850, easing: SHEET_EASE, fill: "both" });
    if (sheetAnim) sheetAnim.cancel();
    a.onfinish = function () {
      detail.classList.remove("open");
      detail.getAnimations({ subtree: true }).forEach(function (x) { x.cancel(); });
      isOpen = false;
      d.body.classList.remove("noscroll");
      if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
      if (typeof after === "function") after();
    };
  }
  detail.querySelector(".shf-close").addEventListener("click", function () { closeDetail(); });
  detail.querySelector(".shf-dbtn").addEventListener("click", function (e) {
    e.preventDefault();
    var href = this.getAttribute("href");
    closeDetail(function () { var t = d.querySelector(href); if (t) t.scrollIntoView({ behavior: reduce ? "auto" : "smooth" }); });
  });

  // ---- frame loop
  var last = performance.now();
  function frame(now) {
    var dt = Math.min(.05, (now - last) / 1000); last = now;
    var k = reduce ? 1 : 1 - Math.exp(-(dragging ? 18 : 5.2) * dt);
    s += (T - s) * k;
    if (Math.abs(T - s) < 1e-4) s = T;
    var loop = TOT;
    if (Math.abs(s - start) > loop * 4) { var sh = Math.round((s - start) / loop) * loop; s -= sh; T -= sh; }

    var ai = mod(Math.round(s));
    if (ai !== active) setActive(ai, T - s >= 0 ? 1 : -1);

    var sr = shelf.getBoundingClientRect();
    shelfCX = sr.left + sr.width / 2; shelfCY = sr.top + sr.height / 2;
    var settled = Math.abs(T - s) < .3;
    onCover = !isOpen && inZone && settled && Math.abs(mx - shelfCX) < .55 * dd && Math.abs(my - shelfCY) < .55 * H;
    var tY, tX;
    if (onCover) { tY = (mx - shelfCX) / (.55 * dd) * 9; tX = -(my - shelfCY) / (H / 2) * 6; }
    else { tY = (mx - shelfCX) / W * 5; tX = 0; }
    var kt = reduce ? 1 : 1 - Math.exp(-7 * dt);
    tiltY += (tY - tiltY) * kt; tiltX += (tX - tiltX) * kt;

    var kl = reduce ? 1 : 1 - Math.exp(-12 * dt), lim = W / 2 + 1.5 * dd;
    for (var n = 0; n < TOT; n++) {
      var t = tapes[n], r = rel(t.v), x = F(r);
      if (Math.abs(x) > lim) { if (t.vis) { t.el.style.visibility = "hidden"; t.vis = false; } continue; }
      if (!t.vis) { t.el.style.visibility = ""; t.vis = true; }
      t.lift += ((Math.abs(r) > .5 ? t.liftT : 0) - t.lift) * kl;
      var o = sst(Math.max(0, 1 - Math.abs(r)));
      var ry = -90 * o + tiltY * o, rx = tiltX * o, rz = -4.5 * o;
      var z = o * .2 * H, y = -o * .025 * H - t.lift * .045 * H;
      t.el.style.transform = "translate3d(" + x.toFixed(2) + "px," + y.toFixed(2) + "px," + z.toFixed(2) + "px) rotateZ(" + rz.toFixed(3) + "deg) rotateX(" + rx.toFixed(3) + "deg) rotateY(" + ry.toFixed(3) + "deg)";
      t.el.style.zIndex = Math.round(100 - Math.abs(r) * 4);
      var shS = Math.round(o * .55 * 100) / 100, shC = Math.round((1 - o) * .5 * 100) / 100;
      if (shS !== t.shS) { t.sp.style.setProperty("--shade", shS); t.shS = shS; }
      if (shC !== t.shC) { t.cv.style.setProperty("--shade", shC); t.shC = shC; }
    }

    var ps = isOpen ? 0 : sst(Math.max(0, 1 - Math.abs(T - s) * 3));
    play.style.transform = "translate(" + (W / 2 - .5 * dd - 6) + "px," + (sr.height / 2 + .36 * H) + "px) scale(" + ps.toFixed(3) + ")";

    // cursor
    if (cur) {
      var kc = 1 - Math.exp(-16 * dt);
      cx += (mx - cx) * kc; cy += (my - cy) * kc;
      cur.style.transform = "translate3d(" + cx.toFixed(1) + "px," + cy.toFixed(1) + "px,0)";
      cur.classList.toggle("in", inZone);
      var el = inZone ? d.elementFromPoint(mx, my) : null;
      var overTape = el && el.closest && el.closest(".shf-tape");
      var overBtn = el && el.closest && el.closest("button, a");
      cur.classList.toggle("open", onCover);
      cur.classList.toggle("spine", !onCover && !isOpen && !!overTape);
      cur.classList.toggle("btn", !onCover && !overTape && !!overBtn);
    }
    requestAnimationFrame(frame);
  }

  // keep the sticky mobile CTA out of the way while the hero (which has its own CTA) is on screen
  var mcta = d.querySelector(".mcta");
  if (mcta && "IntersectionObserver" in window) new IntersectionObserver(function (es) { mcta.classList.toggle("shf-hide", es[0].isIntersecting); }, { threshold: .25 }).observe(hero);

  measure();
  addEventListener("resize", measure);
  if (d.fonts && d.fonts.ready) d.fonts.ready.then(measure);
  setActive(mod(start), 1);
  requestAnimationFrame(function (t) { last = t; frame(t); });
})();
