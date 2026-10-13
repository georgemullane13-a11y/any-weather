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

  /* ----------------------------------------------------- enquiry form */
  (function enquiryForm() {
    var OK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9.5" stroke-width="1.6"/><path d="m8 12.3 2.7 2.7L16.3 9"/></svg>';
    var BAD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9.5"/><path d="M12 7.5v6"/><path d="M12 16.6v.2"/></svg>';

    var form = document.querySelector("[data-ajax-form], [data-wa-form]");
    if (!form) return;
    var sent = form.querySelector(".form-sent");
    var icon = sent && sent.querySelector(".form-sent__icon");
    var text = sent && sent.querySelector(".form-sent__text");
    var button = form.querySelector("button[type=submit]");

    function show(ok, message) {
      if (!sent) return;
      sent.hidden = false;
      sent.classList.toggle("is-error", !ok);
      if (icon) icon.innerHTML = ok ? OK : BAD;
      if (text) text.innerHTML = message;
      sent.scrollIntoView({ block: "nearest", behavior: reduced ? "auto" : "smooth" });
    }

    function field(name) {
      var el = form.elements[name];
      return el && el.value ? el.value.trim() : "";
    }

    /* WhatsApp transport — used only when no back-end is configured. */
    if (form.hasAttribute("data-wa-form")) {
      form.addEventListener("submit", function (e) {
        if (!form.checkValidity()) return;
        e.preventDefault();
        var lines = ["Roofing enquiry from the website", ""];
        [["Name", "name"], ["Phone", "phone"], ["Email", "email"],
         ["Postcode", "postcode"], ["Service", "service"]].forEach(function (pair) {
          if (field(pair[1])) lines.push(pair[0] + ": " + field(pair[1]));
        });
        if (field("message")) lines.push("", field("message"));
        window.open("https://wa.me/" + form.getAttribute("data-wa-form") +
                    "?text=" + encodeURIComponent(lines.join("\n")), "_blank", "noopener");
        show(true, "Your enquiry is ready to send in WhatsApp. If it did not open, call " +
                   '<a href="tel:+447745364538">07745 364 538</a>.');
      });
      return;
    }

    /* Back-end transport — post in the background so the visitor stays put.
       Without JavaScript the browser posts the form normally instead. */
    if (!window.fetch || !window.FormData) return;

    form.addEventListener("submit", function (e) {
      if (!form.checkValidity()) return;
      e.preventDefault();
      form.classList.add("is-sending");
      if (button) button.disabled = true;

      fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" }
      }).then(function (res) {
        if (res.ok) {
          form.reset();
          show(true, "Thanks — your enquiry is on its way. We will come back to you shortly. " +
                     "If it is urgent, call <a href=\"tel:+447745364538\">07745 364 538</a>.");
          return;
        }
        return res.json().catch(function () { return {}; }).then(function (data) {
          var why = data && data.errors && data.errors.length
            ? data.errors.map(function (x) { return x.message; }).join(". ")
            : "That did not send.";
          show(false, why + ' Please call <a href="tel:+447745364538">07745 364 538</a> ' +
                      'or message us on <a href="https://wa.me/447745364538" rel="noopener">WhatsApp</a>.');
        });
      }).catch(function () {
        show(false, 'That did not send — you may be offline. Please call ' +
                    '<a href="tel:+447745364538">07745 364 538</a> or message us on ' +
                    '<a href="https://wa.me/447745364538" rel="noopener">WhatsApp</a>.');
      }).then(function () {
        form.classList.remove("is-sending");
        if (button) button.disabled = false;
      });
    });
  })();


  /* ======================================================================
     The Any Weather test — a canvas weather engine driving one scene.
     Runs only while on screen and the tab is visible; particle count
     scales to the canvas area; reduced motion gets the copy, not the storm.
     ====================================================================== */
  (function weatherTest() {
    var stage = document.querySelector("[data-weather-stage]");
    if (!stage) return;

    var canvas  = stage.querySelector(".weather__canvas");
    var flash   = stage.querySelector(".weather__flash");
    var skies   = {};
    var nameEl  = stage.querySelector("[data-weather-name]");
    var claimEl = stage.querySelector("[data-weather-claim]");
    var liveEl  = stage.querySelector("[data-weather-live]");
    var stateEl = stage.querySelector(".weather__state");
    var buttons = all(".weather__btn", stage);

    all(".weather__sky", stage).forEach(function (el) {
      skies[el.getAttribute("data-sky")] = el;
    });

    var COPY = {};
    all("[data-weather-copy]", stage).forEach(function (tag) {
      try { COPY[tag.getAttribute("data-weather-copy")] = JSON.parse(tag.textContent); }
      catch (e) { /* ignore a malformed block rather than break the page */ }
    });

    // density = particles per 10k css px²; wind in px/s; gravity in px/s
    var MODES = {
      sun:   { density: 0.10, wind:  14, gravity:  26, kind: "mote",  lightning: 0 },
      rain:  { density: 1.55, wind: 150, gravity: 980, kind: "drop",  lightning: 0 },
      storm: { density: 2.45, wind: 420, gravity: 1180, kind: "drop", lightning: 0.012 },
      hail:  { density: 0.95, wind: 110, gravity: 900, kind: "hail",  lightning: 0.002 },
      snow:  { density: 1.05, wind:  52, gravity: 110, kind: "flake", lightning: 0 }
    };

    var mode = "rain", cfg = MODES[mode], particles = [], raf = null;
    var w = 0, h = 0, dpr = 1, last = 0, onScreen = false;
    var ctx = canvas && canvas.getContext ? canvas.getContext("2d") : null;

    /* ---------------------------------------------------------- sizing */
    function resize() {
      if (!ctx) return;
      var r = stage.getBoundingClientRect();
      w = Math.max(1, Math.round(r.width));
      h = Math.max(1, Math.round(r.height));
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      seed();
    }

    function target() {
      var area = (w * h) / 10000;
      return Math.min(Math.round(area * cfg.density), w < 700 ? 190 : 460);
    }

    function spawn(above) {
      return {
        x: Math.random() * (w + 300) - 150,
        y: above ? -Math.random() * h * 0.4 : Math.random() * h,
        z: 0.45 + Math.random() * 0.75,          // depth: size, speed and alpha
        sway: Math.random() * Math.PI * 2,
        spin: 0.4 + Math.random() * 1.6
      };
    }

    function seed() {
      var n = target();
      particles.length = 0;
      for (var i = 0; i < n; i++) particles.push(spawn(false));
    }

    function retarget() {
      var n = target();
      while (particles.length < n) particles.push(spawn(true));
      if (particles.length > n) particles.length = n;
    }

    /* ----------------------------------------------------------- frame */
    function step(now) {
      raf = null;
      if (!ctx) return;
      var dt = Math.min((now - (last || now)) / 1000, 0.05);
      last = now;
      ctx.clearRect(0, 0, w, h);

      for (var i = 0; i < particles.length; i++) {
        var p = particles[i];
        var vy = cfg.gravity * p.z;
        var vx = cfg.wind * p.z;

        if (cfg.kind === "flake" || cfg.kind === "mote") {
          p.sway += dt * p.spin;
          vx += Math.sin(p.sway) * (cfg.kind === "flake" ? 34 : 16);
          vy *= cfg.kind === "mote" ? -0.35 : 1;      // motes drift upward
        }
        p.x += vx * dt;
        p.y += vy * dt;

        if (p.y > h + 24 || p.y < -60 || p.x > w + 160 || p.x < -220) {
          particles[i] = spawn(vy > 0);
          continue;
        }

        if (cfg.kind === "drop") {
          var len = (cfg.gravity / 95) * p.z * 5;
          ctx.strokeStyle = "rgba(196,226,250," + (0.18 + p.z * 0.4).toFixed(2) + ")";
          ctx.lineWidth = Math.max(0.7, p.z * 1.25);
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p.x - (vx / vy) * len, p.y - len);
          ctx.stroke();
        } else if (cfg.kind === "hail") {
          ctx.fillStyle = "rgba(232,245,255," + (0.4 + p.z * 0.5).toFixed(2) + ")";
          ctx.beginPath();
          ctx.arc(p.x, p.y, 1.1 + p.z * 1.9, 0, 6.2832);
          ctx.fill();
        } else if (cfg.kind === "flake") {
          ctx.fillStyle = "rgba(255,255,255," + (0.35 + p.z * 0.5).toFixed(2) + ")";
          ctx.beginPath();
          ctx.arc(p.x, p.y, 1 + p.z * 2.1, 0, 6.2832);
          ctx.fill();
        } else {
          ctx.fillStyle = "rgba(255,226,170," + (0.1 + p.z * 0.26).toFixed(2) + ")";
          ctx.beginPath();
          ctx.arc(p.x, p.y, 0.8 + p.z * 1.5, 0, 6.2832);
          ctx.fill();
        }
      }

      if (cfg.lightning && Math.random() < cfg.lightning && flash) {
        flash.classList.remove("is-lit");
        void flash.offsetWidth;
        flash.classList.add("is-lit");
      }
      if (onScreen && !document.hidden) raf = requestAnimationFrame(step);
    }

    function play() {
      if (raf || reduced || !ctx) return;
      last = 0;
      raf = requestAnimationFrame(step);
    }
    function pause() {
      if (raf) { cancelAnimationFrame(raf); raf = null; }
    }

    /* ----------------------------------------------------------- state */
    var autoTimer = null;
    function setMode(next, fromUser) {
      if (!MODES[next]) return;
      mode = next;
      cfg = MODES[next];
      stage.setAttribute("data-mode", next);

      Object.keys(skies).forEach(function (k) {
        skies[k].classList.toggle("is-on", k === next);
      });
      buttons.forEach(function (b) {
        b.setAttribute("aria-pressed", String(b.getAttribute("data-weather") === next));
      });

      var copy = COPY[next];
      if (copy && stateEl) {
        stateEl.classList.add("is-swapping");
        setTimeout(function () {
          if (nameEl) nameEl.textContent = copy.name;
          if (claimEl) claimEl.textContent = copy.claim;
          stateEl.classList.remove("is-swapping");
        }, reduced ? 0 : 240);
        if (liveEl) liveEl.textContent = copy.name + ". " + copy.claim;
      }

      retarget();
      if (fromUser && autoTimer) { clearInterval(autoTimer); autoTimer = null; }
    }

    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        setMode(b.getAttribute("data-weather"), true);
      });
    });

    /* Cycle gently until someone takes over, so the band is never static. */
    function startAuto() {
      if (autoTimer || reduced) return;
      var order = ["rain", "storm", "hail", "snow", "sun"], i = 0;
      autoTimer = setInterval(function () {
        i = (i + 1) % order.length;
        setMode(order[i], false);
      }, 7000);
    }

    /* ------------------------------------------------- lifecycle hooks */
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          onScreen = e.isIntersecting;
          if (onScreen) { play(); startAuto(); }
          else { pause(); if (autoTimer) { clearInterval(autoTimer); autoTimer = null; } }
        });
      }, { threshold: 0.12 }).observe(stage);
    } else {
      onScreen = true; play(); startAuto();
    }

    document.addEventListener("visibilitychange", function () {
      if (document.hidden) pause(); else if (onScreen) play();
    });

    if ("ResizeObserver" in window) new ResizeObserver(resize).observe(stage);
    else window.addEventListener("resize", resize, { passive: true });

    resize();
    setMode("rain", false);
  })();

  /* ---------------------------------------------------------- the year */
  all("[data-year]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
