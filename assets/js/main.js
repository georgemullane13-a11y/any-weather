/* Any Weather Roofing Ltd — interaction layer.
   No dependencies. Every component degrades to a usable static page. */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var all = function (sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  };

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
    var stick = function () { header.classList.toggle("is-stuck", window.scrollY > 8); };
    stick();
    window.addEventListener("scroll", stick, { passive: true });
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
  var revealables = all(".reveal, .steps, .icon-square");
  if (!("IntersectionObserver" in window) || reduced) {
    revealables.forEach(function (el) { el.classList.add("is-visible"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add("is-visible");
        io.unobserve(e.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    revealables.forEach(function (el) { io.observe(el); });
  }

  all("[data-stagger]").forEach(function (group) {
    var step = parseInt(group.getAttribute("data-stagger"), 10) || 90;
    Array.prototype.forEach.call(group.children, function (child, i) {
      child.style.setProperty("--delay", i * step + "ms");
    });
  });

  all("[data-draw]").forEach(function (path) {
    if (typeof path.getTotalLength !== "function") return;
    try { path.style.setProperty("--len", Math.ceil(path.getTotalLength()) + 2); }
    catch (err) { /* not a geometry node */ }
  });

  /* --------------------------------------------------- counting numbers */
  var counters = all("[data-count]");
  function runCount(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    if (isNaN(target)) return;
    if (reduced) { el.textContent = String(target); return; }
    var dur = 1300, start = null;
    (function tick(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      el.textContent = String(Math.round(target * (1 - Math.pow(1 - p, 3))));
      if (p < 1) requestAnimationFrame(tick);
    })(performance.now());
  }
  if (counters.length && "IntersectionObserver" in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        runCount(e.target);
        cio.unobserve(e.target);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { cio.observe(el); });
  } else {
    counters.forEach(runCount);
  }

  /* -------------------------------------------------------------- FAQ */
  all(".faq__q").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!open));
      btn.closest(".faq__item").classList.toggle("is-open", !open);
    });
  });

  /* ------------------------------------------------------ hero slideshow */
  (function heroSlideshow() {
    var stage = document.querySelector("[data-slideshow]");
    if (!stage) return;
    var slides = all(".hero__slide", stage);
    var dots = all(".hero__dot");
    if (slides.length < 2) return;

    var DURATION = parseInt(stage.getAttribute("data-interval"), 10) || 6000;
    var index = 0, timer = null;
    dots.forEach(function (d) { d.style.setProperty("--dur", DURATION + "ms"); });

    function show(next) {
      slides[index].classList.remove("is-active");
      if (dots[index]) dots[index].setAttribute("aria-current", "false");
      index = (next + slides.length) % slides.length;
      slides[index].classList.add("is-active");
      if (dots[index]) {
        // restart the progress fill
        var fill = dots[index].querySelector("i");
        if (fill) { fill.style.animation = "none"; void fill.offsetWidth; fill.style.animation = ""; }
        dots[index].setAttribute("aria-current", "true");
      }
    }
    function play() {
      if (reduced) return;
      stop();
      timer = setInterval(function () { show(index + 1); }, DURATION);
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }

    dots.forEach(function (dot, i) {
      dot.addEventListener("click", function () { show(i); play(); });
    });
    stage.addEventListener("pointerenter", stop);
    stage.addEventListener("pointerleave", play);
    document.addEventListener("visibilitychange", function () {
      document.hidden ? stop() : play();
    });
    play();
  })();

  /* --------------------------------------------- before / after sliders */
  all("[data-ba]").forEach(function (slider) {
    var grip = slider.querySelector(".ba-slider__grip");
    var dragging = false;
    var swept = false;

    function set(pct) {
      pct = Math.max(0, Math.min(100, pct));
      slider.style.setProperty("--pos", pct.toFixed(2) + "%");
      if (grip) grip.setAttribute("aria-valuenow", Math.round(pct));
    }
    function fromEvent(e) {
      var r = slider.getBoundingClientRect();
      set(((e.clientX - r.left) / r.width) * 100);
    }

    slider.addEventListener("pointerdown", function (e) {
      dragging = true;
      slider.setPointerCapture(e.pointerId);
      fromEvent(e);
    });
    slider.addEventListener("pointermove", function (e) { if (dragging) fromEvent(e); });
    slider.addEventListener("pointerup", function () { dragging = false; });
    slider.addEventListener("pointercancel", function () { dragging = false; });

    if (grip) {
      grip.addEventListener("keydown", function (e) {
        var now = parseFloat(grip.getAttribute("aria-valuenow")) || 50;
        var step = e.shiftKey ? 10 : 3;
        if (e.key === "ArrowLeft") { set(now - step); e.preventDefault(); }
        if (e.key === "ArrowRight") { set(now + step); e.preventDefault(); }
        if (e.key === "Home") { set(0); e.preventDefault(); }
        if (e.key === "End") { set(100); e.preventDefault(); }
      });
      grip.addEventListener("click", function (e) { e.stopPropagation(); });
    }

    /* One automatic sweep the first time it scrolls into view, so the
       control explains itself without anyone having to touch it. */
    function sweep() {
      if (swept || reduced) return;
      swept = true;
      var t0 = performance.now(), dur = 2400;
      (function frame(t) {
        var p = Math.min((t - t0) / dur, 1);
        var eased = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
        set(50 + Math.sin(eased * Math.PI * 2) * 28);
        if (p < 1 && !dragging) requestAnimationFrame(frame);
        else if (!dragging) set(50);
      })(t0);
    }
    if ("IntersectionObserver" in window) {
      var bio = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          setTimeout(sweep, 350);
          bio.unobserve(e.target);
        });
      }, { threshold: 0.45 });
      bio.observe(slider);
    }
    set(50);
  });

  /* ------------------------------------------------------- work gallery */
  all("[data-gallery]").forEach(function (gallery) {
    var track = gallery.querySelector(".gallery__track");
    if (!track) return;
    gallery.querySelectorAll("[data-gallery-prev], [data-gallery-next]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var first = track.firstElementChild;
        var step = first ? first.getBoundingClientRect().width + 24 : 320;
        track.scrollBy({ left: btn.hasAttribute("data-gallery-next") ? step : -step,
                         behavior: reduced ? "auto" : "smooth" });
      });
    });
  });

  /* ---------------------------------------------------------- the year */
  all("[data-year]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
