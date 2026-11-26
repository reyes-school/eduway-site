/* EduWay — small progressive enhancements. Site works without JS. */
(function () {
  var d = document, root = d.documentElement;
  root.classList.remove("no-js");

  // sticky header border
  var hdr = d.querySelector(".hdr");
  var onScroll = function () { if (hdr) hdr.classList.toggle("scrolled", window.scrollY > 8); };
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // full-screen mobile menu
  var burger = d.querySelector(".burger"), mnav = d.getElementById("mnav");
  function closeMenu() {
    if (!mnav || mnav.hidden) return;
    mnav.classList.remove("open"); burger.setAttribute("aria-expanded", "false"); d.body.classList.remove("noscroll");
    setTimeout(function () { mnav.hidden = true; }, 250);
  }
  if (burger && mnav) {
    burger.addEventListener("click", function () {
      if (mnav.hidden) {
        mnav.hidden = false; d.body.classList.add("noscroll"); burger.setAttribute("aria-expanded", "true");
        requestAnimationFrame(function () { mnav.classList.add("open"); });
      } else closeMenu();
    });
    mnav.addEventListener("click", function (e) { if (e.target.closest("a")) closeMenu(); });
    d.addEventListener("keydown", function (e) { if (e.key === "Escape") closeMenu(); });
  }

  // "Become a partner" buttons preselect the request type in the lead form
  d.querySelectorAll("[data-type]").forEach(function (a) {
    a.addEventListener("click", function () {
      var r = d.querySelector('#leadForm input[name=type][value="' + a.dataset.type + '"]');
      if (r) r.checked = true;
    });
  });

  // sticky mobile CTA hides while the lead form is on screen
  var mcta = d.querySelector(".mcta"), lead = d.getElementById("leadForm");
  if (mcta && "IntersectionObserver" in window) {
    if (!lead) mcta.classList.add("hide");
    else new IntersectionObserver(function (es) { mcta.classList.toggle("hide", es[0].isIntersecting); }).observe(lead);
  }

  // role tabs (WAI-ARIA tabs)
  d.querySelectorAll("[role=tablist]").forEach(function (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll("[role=tab]"));
    function select(t) {
      tabs.forEach(function (x) {
        var on = x === t;
        x.setAttribute("aria-selected", on ? "true" : "false");
        x.tabIndex = on ? 0 : -1;
        var p = d.getElementById(x.getAttribute("aria-controls"));
        if (p) p.hidden = !on;
      });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (e) {
        var k = e.key, n = null;
        if (k === "ArrowRight") n = tabs[(i + 1) % tabs.length];
        if (k === "ArrowLeft") n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (n) { e.preventDefault(); n.focus(); select(n); }
      });
    });
  });

  // white-label builder
  var mock = d.getElementById("mock");
  if (mock) {
    var nameIn = d.getElementById("schoolName"), nameOut = d.getElementById("mockName"), init = d.getElementById("mockInit");
    var fallback = nameOut ? nameOut.textContent : "";
    if (nameIn) nameIn.addEventListener("input", function () {
      var v = nameIn.value.trim() || fallback;
      nameOut.textContent = v.slice(0, 28);
      init.textContent = v.charAt(0).toUpperCase();
    });
    d.querySelectorAll(".swatches button").forEach(function (b) {
      b.addEventListener("click", function () {
        d.querySelectorAll(".swatches button").forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true");
        mock.style.setProperty("--b", b.dataset.c);
        mock.style.setProperty("--bs", b.dataset.s);
      });
    });
  }

  // lead form → /api/lead (Vercel function → Telegram)
  var form = d.getElementById("leadForm");
  if (form) {
    var ok = d.getElementById("formOk"), err = d.getElementById("formErr"), btn = form.querySelector("button[type=submit]");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      ok.classList.remove("show"); err.classList.remove("show");
      var bad = null;
      form.querySelectorAll("input[required],select[required]").forEach(function (i) { i.classList.add("touched"); if (!bad && !i.checkValidity()) bad = i; });
      if (bad) { bad.focus(); bad.reportValidity && bad.reportValidity(); return; }
      var data = {}; new FormData(form).forEach(function (v, k) { data[k] = String(v).trim(); });
      data.page = location.pathname;
      var label = btn.innerHTML; btn.disabled = true; btn.textContent = form.dataset.sending || "…";
      fetch(form.action, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function () {
          var t = form.querySelector("input[name=type]:checked"); form.reset(); if (t) t.checked = true; form.querySelectorAll(".touched").forEach(function (i) { i.classList.remove("touched"); });
          ok.classList.add("show"); ok.focus();
          if (window.gtag) window.gtag("event", "generate_lead");
        })
        .catch(function () { err.classList.add("show"); })
        .finally(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  }

  // ---------- motion ----------
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var rvs = [];
  if ("IntersectionObserver" in window && !reduce) {
    // word-by-word headlines (hero h1 + section h2)
    d.querySelectorAll(".hero h1, .head h2, .case-txt h2, .lead-sec h2").forEach(function (h) {
      var n = 0;
      (function split(el) {
        Array.prototype.slice.call(el.childNodes).forEach(function (c) {
          if (c.nodeType === 3) {
            var frag = d.createDocumentFragment();
            c.textContent.split(/(\s+)/).forEach(function (w) {
              if (!w) return;
              if (/^\s+$/.test(w)) { frag.appendChild(d.createTextNode(w)); return; }
              var s = d.createElement("span"); s.className = "mw"; s.style.setProperty("--w", n++); s.textContent = w; frag.appendChild(s);
            });
            el.replaceChild(frag, c);
          } else if (c.nodeType === 1 && c.tagName !== "BR") {
            if (c.classList.contains("grad")) { c.classList.add("mwi"); c.style.setProperty("--w", n++); }
            else split(c);
          }
        });
      })(h);
      h.classList.add("mh", "rv");
    });
    // stagger siblings inside grids
    d.querySelectorAll(".val-grid,.bento,.sec-grid,.steps,.partners,.facts,.faq,.stats,.compare,.checks").forEach(function (g) {
      var i = 0;
      Array.prototype.forEach.call(g.children, function (c) {
        if (!c.classList.contains("rv")) c.classList.add("rv");
        c.style.setProperty("--d", (Math.min(i++, 8) * 0.08) + "s");
      });
    });
    rvs = Array.prototype.slice.call(d.querySelectorAll(".rv"));
    var vh = window.innerHeight || 800;
    var show = function (el) {
      el.classList.add("in");
      // drop the stagger delay once revealed so hover feels instant
      setTimeout(function () { el.style.removeProperty("--d"); }, 1400);
      if (el.classList.contains("stat")) countUp(el.querySelector("b"));
    };
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { show(en.target); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -6% 0px" });
    root.classList.add("rv-on");
    rvs.forEach(function (el) { if (el.getBoundingClientRect().top < vh * 0.94) requestAnimationFrame(function () { show(el); }); else io.observe(el); });
    var all = function () { rvs.forEach(function (el) { el.classList.add("in"); }); };
    window.addEventListener("hashchange", all); window.addEventListener("beforeprint", all);
  }

  // count-up for plain integer stats
  function countUp(b) {
    if (!b || b.dataset.done) return; b.dataset.done = 1;
    var t = b.textContent.trim(); if (!/^\d+$/.test(t)) return;
    var end = +t, t0 = null, dur = 1200;
    (function step(ts) {
      if (!t0) t0 = ts; var k = Math.min(1, (ts - t0) / dur), e2 = 1 - Math.pow(1 - k, 3);
      b.textContent = Math.round(end * e2); if (k < 1) requestAnimationFrame(step); else b.textContent = t;
    })(performance.now());
  }

  // scroll-linked: progress bar, hero tilt, parallax phones
  if (!reduce) {
    var bar = d.createElement("div"); bar.className = "sprog"; bar.setAttribute("aria-hidden", "true"); d.body.appendChild(bar);
    var stage = d.querySelector(".stage"), heroWrap = d.querySelector(".hero .wrap");
    var par = [];
    d.querySelectorAll(".stage .p1").forEach(function (el) { par.push([el, -0.12]); });
    d.querySelectorAll(".stage .p2").forEach(function (el) { par.push([el, -0.22]); });
    d.querySelectorAll(".case-phones .p1").forEach(function (el) { par.push([el, 0.08]); });
    d.querySelectorAll(".case-phones .p2").forEach(function (el) { par.push([el, -0.1]); });
    d.querySelectorAll(".builder .mock").forEach(function (el) { par.push([el, -0.06]); });
    root.classList.add("js-motion");
    var ticking = false;
    var frame = function () {
      ticking = false;
      var y = window.scrollY, H = window.innerHeight, max = d.documentElement.scrollHeight - H;
      bar.style.transform = "scaleX(" + (max > 0 ? Math.min(1, y / max) : 0) + ")";
      if (stage) {
        var r = stage.getBoundingClientRect();
        var p = Math.max(0, Math.min(1, (H - r.top) / (H * 0.55)));
        stage.style.setProperty("--p", p.toFixed(3));
      }
      if (heroWrap && y < H * 1.2) {
        heroWrap.style.setProperty("--ho", Math.max(0, 1 - y / (H * 0.75)).toFixed(3));
        heroWrap.style.setProperty("--hy", (y * 0.25).toFixed(1) + "px");
      }
      par.forEach(function (it) {
        var r2 = it[0].getBoundingClientRect(); if (r2.bottom < -200 || r2.top > H + 200) return;
        var c = (r2.top + r2.height / 2) - H / 2;
        it[0].style.setProperty("--py", (c * it[1]).toFixed(1) + "px");
      });
    };
    var onS = function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } };
    window.addEventListener("scroll", onS, { passive: true }); window.addEventListener("resize", onS); frame();
  }

  var y = d.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
})();
