# Any Weather Roofing Ltd — website

A fast, SEO-optimised static website for **Any Weather Roofing Ltd**, Plymouth.
No frameworks, no build tooling, no runtime dependencies — plain HTML, one
stylesheet, one small JavaScript file, and hand-built inline SVG artwork.

Content is carried over from the previous site at `anyweatherroofingltd.co.uk`
(services, coverage area, phone number, positioning) and expanded into a full
page-per-service structure.

---

## Structure

```
index.html                      Home
services/index.html             Service overview
services/<slug>/index.html      8 individual service pages
areas-we-cover/index.html       Local coverage page
about/index.html                About
contact/index.html              Contact + enquiry form
privacy/index.html              Privacy policy
404.html                        Not-found page
robots.txt  sitemap.xml  site.webmanifest
assets/css/styles.css           Design system + all page styles
assets/js/main.js               Reveals, nav, FAQ, counters, rain
assets/img/                     favicon, OG card, touch icon
build.py                        Generates every HTML page (content lives here)
tools/make_images.py            Regenerates the PNG assets (needs Pillow)
```

## Editing the site

**All copy, metadata and structured data live in `build.py`.** Edit there and
regenerate:

```bash
python3 build.py          # rewrites every HTML page + sitemap.xml
```

Common edits:

| I want to…                        | Edit in `build.py`              |
| --------------------------------- | ------------------------------- |
| Change the phone number / details  | `SITE`                          |
| Add or reword a service            | `SERVICES`                      |
| Add a town or neighbourhood        | `PRIMARY_AREAS` / `WIDER_AREAS` |
| Change the areas copy              | `AREA_NOTES`                    |
| Add an FAQ (home page)             | `HOME_FAQS`                     |
| Add a review                       | `TESTIMONIALS`                  |
| Point the contact form somewhere   | `FORM_ACTION`                   |

Styling is hand-written CSS in `assets/css/styles.css`, driven by custom
properties at the top of the file (`--ember`, `--slate-900`, spacing, radii).

## Before it goes live — checklist

1. **Contact form back-end.** `FORM_ACTION` in `build.py` is a placeholder.
   Point it at Formspree / Netlify Forms / Basin / your own handler, then
   re-run `python3 build.py`. Until then the form posts nowhere — the phone
   and WhatsApp links are the live routes.
2. **Add an email address** if you want one shown (there was none on the old
   site). Add it to `SITE` and to the footer/contact blocks.
3. **Confirm the business details** used on the About and Contact pages:
   company number `15905071`, founding year, VAT registration, Checkatrade
   membership.
4. **Guarantee wording.** No warranty terms were stated on the old site, so
   none are claimed here. If you offer one (e.g. a 10-year workmanship
   guarantee), add it — it converts well.
5. **Review `privacy/index.html`** and add a registered address.
6. **Google Business Profile.** The structured data on the site declares
   Plymouth, Devon with no street address. If the business has a verifiable
   address, add it to `business_jsonld()` so it matches the GBP listing.
7. **Verify in Google Search Console** and submit `/sitemap.xml`.

## Hosting

Every path is root-relative (`/assets/...`), so serve the repository root at
the domain apex:

- **GitHub Pages** — enable Pages on this branch and add a `CNAME` file
  containing `anyweatherroofingltd.co.uk`, then point DNS at GitHub.
- **Netlify / Cloudflare Pages / Vercel** — no build command, publish
  directory `/`.
- **Any shared host** — upload the repository contents as-is.

Local preview:

```bash
python3 -m http.server 8000    # then open http://127.0.0.1:8000
```

## What makes it SEO-optimised

- Unique `<title>`, meta description and canonical URL on every page
- One `<h1>` per page, logical heading order, descriptive internal links
- **Structured data** on every page: `RoofingContractor` / `LocalBusiness` with
  `areaServed`, `geo`, opening hours and an offer catalogue; plus `WebSite`,
  `BreadcrumbList`, `Service` and `FAQPage` where relevant
- A page per service and a dedicated local-coverage page, each with genuinely
  distinct copy rather than swapped town names
- Open Graph and Twitter card metadata with a 1200×630 image
- `sitemap.xml`, `robots.txt`, web manifest, SVG favicon, Apple touch icon
- Fast by construction: no framework, no JS libraries, no photographic assets
  (all illustration is inline SVG), fonts preconnected and `display=swap`
- Accessible: skip link, visible focus rings, `aria-current`, labelled form
  fields, `aria-expanded` accordions, and a full `prefers-reduced-motion` path

## Animation

Everything is CSS-driven and degrades cleanly:

- Hero roof tiles "lay themselves in" on load, sun rays rotate, clouds drift
- Falling rain generated in JS (skipped entirely for reduced motion)
- Scroll-triggered reveals with per-item stagger via `IntersectionObserver`
- SVG icons draw themselves in with `stroke-dashoffset`
- Animated process timeline, counting stats, marquee trust bar, hover lifts

`prefers-reduced-motion: reduce` disables all of it, and the `.reveal` opacity
is only applied once JavaScript has run, so content is never hidden from a
crawler or a no-JS visitor.
