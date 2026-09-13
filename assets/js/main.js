/* Any Weather Roofing Ltd — progressive interaction layer.
   No dependencies. Everything degrades to a fully usable static page. */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------ header + mobile nav */
  var header = document.querySelector(".site-header");
  var nav = document.getElementById("primary-nav");
  var toggle = document.querySelector(".nav-toggle");

  function setHeaderHeight() {
    if (header) document.documentElement.style.setProperty("--header-h", header.offsetHeight + "px");
  }
  setHeaderHeight();
  window.addEventListener("resize", setHeaderHeight, { passive: true });

  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-stuck", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("is-open", !open);
      document.body.style.overflow = !open ? "hidden" : "";
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        toggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("is-open");
        document.body.style.overflow = "";
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) toggle.click();
    });
  }

  /* ------------------------------------------------------ scroll reveal */
  var revealables = document.querySelectorAll(".reveal, .steps, .icon-badge");
  if (!("IntersectionObserver" in window) || reduced) {
    Array.prototype.forEach.call(revealables, function (el) { el.classList.add("is-visible"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        io.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    Array.prototype.forEach.call(revealables, function (el) { io.observe(el); });
  }

  /* Stagger children of any [data-stagger] group. */
  Array.prototype.forEach.call(document.querySelectorAll("[data-stagger]"), function (group) {
    var step = parseInt(group.getAttribute("data-stagger"), 10) || 90;
    Array.prototype.forEach.call(group.children, function (child, i) {
      child.style.setProperty("--delay", i * step + "ms");
    });
  });

  /* --------------------------------------------------- SVG line drawing */
  Array.prototype.forEach.call(document.querySelectorAll("[data-draw]"), function (path) {
    if (typeof path.getTotalLength !== "function") return;
    try {
      var len = Math.ceil(path.getTotalLength()) + 2;
      path.style.setProperty("--len", len);
    } catch (err) { /* non-geometry node — ignore */ }
  });

  /* ------------------------------------------------------------- rain */
  var rain = document.querySelector(".rain");
  if (rain && !reduced) {
    var drops = window.innerWidth < 720 ? 26 : 52;
    var frag = document.createDocumentFragment();
    for (var i = 0; i < drops; i++) {
      var d = document.createElement("span");
      d.style.left = (Math.random() * 100).toFixed(2) + "%";
      d.style.animationDuration = (0.75 + Math.random() * 0.9).toFixed(2) + "s";
      d.style.animationDelay = (Math.random() * 3).toFixed(2) + "s";
      d.style.opacity = (0.25 + Math.random() * 0.6).toFixed(2);
      d.style.height = (46 + Math.random() * 70).toFixed(0) + "px";
      frag.appendChild(d);
    }
    rain.appendChild(frag);
  }

  /* --------------------------------------------------- counting numbers */
  var counters = document.querySelectorAll("[data-count]");
  if (counters.length) {
    var runCount = function (el) {
      var target = parseFloat(el.getAttribute("data-count"));
      if (isNaN(target)) return;
      if (reduced) { el.textContent = String(target); return; }
      var dur = 1400, start = null;
      var tick = function (ts) {
        if (start === null) start = ts;
        var p = Math.min((ts - start) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = String(Math.round(target * eased));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    if ("IntersectionObserver" in window) {
      var cio = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          runCount(e.target);
          cio.unobserve(e.target);
        });
      }, { threshold: 0.5 });
      Array.prototype.forEach.call(counters, function (el) { cio.observe(el); });
    } else {
      Array.prototype.forEach.call(counters, runCount);
    }
  }

  /* -------------------------------------------------------------- FAQ */
  Array.prototype.forEach.call(document.querySelectorAll(".faq__q"), function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".faq__item");
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!open));
      item.classList.toggle("is-open", !open);
    });
  });

  /* ------------------------------------------------------ hero parallax */
  var art = document.querySelector("[data-parallax]");
  if (art && !reduced && window.matchMedia("(min-width: 981px)").matches) {
    var ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = Math.min(window.scrollY, 620);
        art.style.transform = "translate3d(0," + (y * -0.06).toFixed(2) + "px,0)";
        ticking = false;
      });
    }, { passive: true });
  }

  /* ---------------------------------------------------------- the year */
  Array.prototype.forEach.call(document.querySelectorAll("[data-year]"), function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
