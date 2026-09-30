/* KJ Pristine: interactions. No dependencies. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Header: shadow on scroll + mobile bar ---------- */
  var header = document.querySelector('.site-header');
  var mobileBar = document.querySelector('.mobile-bar');
  var quote = document.getElementById('quote');
  function onScroll() {
    var y = window.scrollY;
    header.classList.toggle('scrolled', y > 10);
    if (mobileBar) {
      var qTop = quote ? quote.getBoundingClientRect().top : Infinity;
      mobileBar.classList.toggle('show', y > 500 && qTop > window.innerHeight * 0.6);
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile nav ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  function closeNav() {
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
  }
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });
  nav.addEventListener('click', function (e) { if (e.target.closest('a')) closeNav(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeNav(); });

  /* ---------- Active nav link ---------- */
  var navLinks = Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]:not(.btn)'));
  if ('IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        navLinks.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === '#' + en.target.id); });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    navLinks.forEach(function (a) { var s = document.querySelector(a.getAttribute('href')); if (s) spy.observe(s); });
  }

  /* ---------- Hero floating elements start after entrance ---------- */
  setTimeout(function () {
    document.querySelectorAll('.badge-round, .float-card').forEach(function (el) {
      el.style.opacity = 1; el.style.animation = 'none'; void el.offsetWidth; el.style.animation = ''; el.classList.add('is-in');
    });
  }, reduceMotion ? 0 : 1600);

  /* ---------- Scroll reveal with sibling stagger ---------- */
  var reveals = document.querySelectorAll('.reveal, .map');
  if ('IntersectionObserver' in window && !reduceMotion) {
    // stagger siblings that share a parent
    var groups = new Map();
    document.querySelectorAll('.reveal').forEach(function (el) {
      var p = el.parentElement, i = groups.get(p) || 0;
      el.style.setProperty('--delay', Math.min(i * 0.08, 0.5) + 's');
      groups.set(p, i + 1);
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- Service card cursor glow ---------- */
  document.querySelectorAll('.service-card').forEach(function (card) {
    card.addEventListener('pointermove', function (e) {
      var r = card.getBoundingClientRect();
      card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      card.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  /* ---------- Before / after slider ---------- */
  document.querySelectorAll('[data-ba]').forEach(function (ba) {
    var stage = ba.querySelector('.ba-stage');
    var range = ba.querySelector('.ba-range');
    function set(v) { stage.style.setProperty('--pos', v + '%'); }
    range.addEventListener('input', function () { set(range.value); });

    // one-time "peek" animation when first seen
    if ('IntersectionObserver' in window && !reduceMotion) {
      var played = false;
      var peek = new IntersectionObserver(function (entries) {
        if (!entries[0].isIntersecting || played) return;
        played = true; peek.disconnect();
        var start = null, dur = 2200;
        function step(t) {
          if (!start) start = t;
          var p = Math.min((t - start) / dur, 1);
          var v = 50 + Math.sin(p * Math.PI * 2) * 32 * (1 - p);
          set(v); range.value = v;
          if (p < 1 && !range.matches(':active')) requestAnimationFrame(step); else { set(range.value); }
        }
        setTimeout(function () { requestAnimationFrame(step); }, 500);
      }, { threshold: 0.6 });
      peek.observe(stage);
    }
  });

  /* ---------- Tap-to-reveal pairs ---------- */
  document.querySelectorAll('[data-flip]').forEach(function (el) {
    function flip() {
      var on = el.classList.toggle('revealed');
      el.setAttribute('aria-pressed', String(on));
    }
    el.addEventListener('click', flip);
    el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); flip(); } });
    if (window.matchMedia('(hover: hover)').matches) {
      el.addEventListener('mouseenter', function () { el.classList.add('revealed'); el.setAttribute('aria-pressed', 'true'); });
      el.addEventListener('mouseleave', function () { el.classList.remove('revealed'); el.setAttribute('aria-pressed', 'false'); });
    }
  });

  /* ---------- Reviews carousel dots (mobile) ---------- */
  var track = document.querySelector('[data-reviews]');
  var dotsWrap = document.querySelector('.review-dots');
  if (track && dotsWrap) {
    var cards = track.children;
    for (var i = 0; i < cards.length; i++) {
      (function (idx) {
        var b = document.createElement('button');
        b.type = 'button'; b.tabIndex = -1;
        b.addEventListener('click', function () { cards[idx].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' }); });
        dotsWrap.appendChild(b);
      })(i);
    }
    function updateDots() {
      var mid = track.scrollLeft + track.clientWidth / 2, best = 0, bestD = Infinity;
      for (var j = 0; j < cards.length; j++) {
        var c = cards[j], d = Math.abs(c.offsetLeft + c.offsetWidth / 2 - mid);
        if (d < bestD) { bestD = d; best = j; }
      }
      Array.prototype.forEach.call(dotsWrap.children, function (b, k) { b.classList.toggle('active', k === best); });
    }
    track.addEventListener('scroll', updateDots, { passive: true });
    updateDots();
  }

  /* ---------- Service links preselect the form ---------- */
  document.querySelectorAll('[data-service]').forEach(function (a) {
    a.addEventListener('click', function () {
      var v = a.getAttribute('data-service');
      var input = document.querySelector('.pick-grid input[value="' + v.replace(/"/g, '\\"') + '"]');
      if (input) input.checked = true;
    });
  });

  /* ---------- Quote form ---------- */
  var form = document.getElementById('quote-form');
  if (form) {
    var dateInput = form.querySelector('input[type="date"]');
    if (dateInput) dateInput.min = new Date().toISOString().split('T')[0];

    function validate() {
      var ok = true;
      form.querySelectorAll('.field input[required]').forEach(function (inp) {
        var f = inp.closest('.field');
        var valid = inp.checkValidity() && inp.value.trim() !== '';
        f.classList.toggle('invalid', !valid);
        if (!valid) ok = false;
      });
      var pick = form.querySelector('.service-pick');
      var chosen = form.querySelector('input[name="service"]:checked');
      pick.classList.toggle('invalid', !chosen);
      if (!chosen) ok = false;
      return ok;
    }
    form.addEventListener('input', function (e) {
      var f = e.target.closest('.field');
      if (f && f.classList.contains('invalid') && e.target.checkValidity()) f.classList.remove('invalid');
    });
    form.addEventListener('change', function (e) {
      if (e.target.name === 'service') form.querySelector('.service-pick').classList.remove('invalid');
    });

    function field(name) {
      var el = form.querySelector('[name="' + name + '"]:checked') || form.querySelector('[name="' + name + '"]:not([type="radio"])');
      return el ? el.value.trim() : '';
    }
    function buildMessage() {
      var date = field('date');
      if (date) {
        var d = new Date(date + 'T12:00:00');
        date = d.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'long' });
      }
      var lines = [
        'Hi Kerri, I’d love a free quote from KJ Pristine.',
        '',
        'Name: ' + field('name'),
        'Phone: ' + field('phone'),
        'Email: ' + field('email'),
        'Service: ' + field('service'),
        'Preferred date: ' + (date || 'Flexible')
      ];
      if (field('message')) lines.push('', field('message'));
      return lines.join('\n');
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validate()) {
        var first = form.querySelector('.invalid input, .invalid');
        if (first && first.focus) first.focus();
        return;
      }
      var btn = form.querySelector('button[type="submit"]');
      var endpoint = form.getAttribute('data-endpoint');
      var success = form.querySelector('.form-success');
      var msg = buildMessage();
      var waUrl = 'https://wa.me/' + form.getAttribute('data-whatsapp') + '?text=' + encodeURIComponent(msg);
      var mailUrl = 'mailto:' + form.getAttribute('data-email') +
        '?subject=' + encodeURIComponent('Free quote request: ' + field('service')) +
        '&body=' + encodeURIComponent(msg);
      success.querySelector('[data-success-wa]').href = waUrl;
      success.querySelector('[data-success-mail]').href = mailUrl;

      function show(title, lead, withActions) {
        btn.classList.remove('loading');
        success.querySelector('h3').textContent = title;
        success.querySelector('.success-lead').innerHTML = lead;
        success.querySelector('.success-actions').hidden = !withActions;
        success.hidden = false;
      }
      function fallback(opened) {
        show(opened ? 'Nearly there!' : 'Let’s try another way',
          opened ? 'Your enquiry is ready in WhatsApp. Just press <strong>send</strong> and I’ll be in touch as soon as possible.'
                 : 'Sorry, the form couldn’t send just now. Tap below to send the same enquiry by WhatsApp or email.',
          true);
      }

      if (endpoint) {
        btn.classList.add('loading');
        fetch(endpoint, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
          .then(function (r) { if (!r.ok) throw new Error(r.status); })
          .then(function () {
            show('Thank you!', 'Your enquiry is in. I’ll be in touch as soon as possible to arrange your free walk-through.', false);
            form.reset();
          })
          .catch(function () { fallback(false); });
        return;
      }

      // No endpoint set: hand the enquiry to WhatsApp (email as a fallback)
      window.open(waUrl, '_blank', 'noopener');
      fallback(true);
    });
  }

  /* ---------- Year ---------- */
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();
})();
