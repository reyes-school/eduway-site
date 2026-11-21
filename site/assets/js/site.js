/* EduWay — small progressive enhancements. Site works without JS. */
(function () {
  var d = document, root = d.documentElement;
  root.classList.remove("no-js");

  // sticky header border
  var hdr = d.querySelector(".hdr");
  var onScroll = function () { if (hdr) hdr.classList.toggle("scrolled", window.scrollY > 8); };
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // mobile nav
  var burger = d.querySelector(".burger"), nav = d.getElementById("nav");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a") && nav.classList.contains("open")) {
        nav.classList.remove("open"); burger.setAttribute("aria-expanded", "false");
      }
    });
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
      form.querySelectorAll("input[required]").forEach(function (i) { i.classList.add("touched"); if (!bad && !i.checkValidity()) bad = i; });
      if (bad) { bad.focus(); bad.reportValidity && bad.reportValidity(); return; }
      var data = {}; new FormData(form).forEach(function (v, k) { data[k] = String(v).trim(); });
      data.page = location.pathname;
      var label = btn.innerHTML; btn.disabled = true; btn.textContent = form.dataset.sending || "…";
      fetch(form.action, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function () {
          form.reset(); form.querySelectorAll(".touched").forEach(function (i) { i.classList.remove("touched"); });
          ok.classList.add("show"); ok.focus();
          if (window.gtag) window.gtag("event", "generate_lead");
        })
        .catch(function () { err.classList.add("show"); })
        .finally(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  }

  // reveal on scroll
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    d.querySelectorAll(".rv").forEach(function (el) { io.observe(el); });
  } else {
    d.querySelectorAll(".rv").forEach(function (el) { el.classList.add("in"); });
  }

  var y = d.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
})();
