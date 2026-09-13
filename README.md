# Any Weather Roofing Ltd — website

A fast, SEO-optimised static website for **Any Weather Roofing Ltd**, Plymouth.
No frameworks, no build tooling, no runtime dependencies — plain HTML, one
stylesheet, one small JavaScript file.

Brand: deep navy + signal blue on cool white, matching the trading identity
(logo, vehicle livery and social graphics). Tagline: *Quality roofing. Any
weather.*

---

## ⚠️ First job: replace the placeholder photos

Everything in `assets/img/photos/` is a **generated placeholder**, marked with a
small `PLACEHOLDER` badge in the corner. Swap in real photographs — keep the
filenames and roughly the aspect ratios and nothing else needs changing.

| File | Used for | Size / ratio |
| --- | --- | --- |
| `hero-1.jpg` `hero-2.jpg` `hero-3.jpg` | Home page hero slideshow | 1800×1100 (16:10), landscape |
| `ba-pitched-before.jpg` / `ba-pitched-after.jpg` | Pitched re-roof before/after slider | 1400×1000 (7:5) — **must be the same framing** |
| `ba-flat-before.jpg` / `ba-flat-after.jpg` | Flat roof before/after slider | 1400×1000 (7:5) — **same framing** |
| `work-1.jpg` … `work-6.jpg` | "Recent work" gallery + service page photos | 1200×900 (4:3) |

For the before/after sliders, shoot or crop both frames from the **same
position** — the effect only works when the two images line up.

Captions, alt text and the pairing live in `build.py` (`HERO_SLIDES`,
`BEFORE_AFTER`, `GALLERY`, `SERVICE_PHOTO`). Update the alt text when you swap
the photos — it matters for both accessibility and image search.

`tools/make_images.py` regenerates the placeholders and the Open Graph card if
you ever need them again (`pip install pillow`).

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
assets/js/main.js               Slideshow, before/after sliders, gallery, nav, FAQ
assets/img/photos/              Photography (placeholders — see above)
assets/img/                     favicon, OG card, touch icon
build.py                        Generates every HTML page (content lives here)
tools/make_images.py            Regenerates the PNG/JPG assets (needs Pillow)
```

## Editing the site

**All copy, metadata and structured data live in `build.py`.** Edit there and
regenerate:

```bash
python3 build.py          # rewrites every HTML page + sitemap.xml
```

| I want to…                        | Edit in `build.py`              |
| --------------------------------- | ------------------------------- |
| Change the phone number / details  | `SITE`                          |
| Add or reword a service            | `SERVICES`                      |
| Change a service page's photo      | `SERVICE_PHOTO`                 |
| Change the hero slideshow          | `HERO_SLIDES`                   |
| Add a before/after job             | `BEFORE_AFTER`                  |
| Add a gallery photo                | `GALLERY`                       |
| Add a town or neighbourhood        | `PRIMARY_AREAS` / `WIDER_AREAS` |
| Change the areas copy              | `AREA_NOTES`                    |
| Add an FAQ (home page)             | `HOME_FAQS`                     |
| Add a review                       | `TESTIMONIALS`                  |
| Point the contact form somewhere   | `FORM_ACTION`                   |

Styling is hand-written CSS in `assets/css/styles.css`, driven by custom
properties at the top of the file (`--navy-900`, `--blue`, spacing, radii).

## Before it goes live — checklist

1. **Replace the placeholder photos** (see above). Nothing else matters as much.
2. **Contact form back-end.** `FORM_ACTION` in `build.py` is a placeholder.
   Point it at Formspree / Netlify Forms / Basin / your own handler, then
   re-run `python3 build.py`. Until then the form posts nowhere — the phone
   and WhatsApp links are the live routes.
3. **Add an email address** if you want one shown. Add it to `SITE` and to the
   footer and contact blocks.
4. **Confirm the business details** on the About and Contact pages: company
   number `15905071`, founding year, VAT registration, insurance cover.
5. **Check the review figures.** "100% recommended / 27 reviews" comes from the
   Facebook page — update `SITE["recommend_pct"]` and `SITE["review_count"]`,
   the hero stats and the reviews section as those numbers move.
6. **Guarantee wording.** No warranty terms are claimed. If you offer one (a
   10-year workmanship guarantee, say), add it — it converts well.
7. **Review `privacy/index.html`** and add a registered address.
8. **Google Business Profile.** The structured data declares Plymouth, Devon
   with no street address. If there is a verifiable address, add it to
   `business_jsonld()` so it matches the GBP listing.
9. **Verify in Google Search Console** and submit `/sitemap.xml`.

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
- Every photo has real alt text, explicit `width`/`height` (no layout shift)
  and `loading="lazy"` below the fold
- Fast by construction: no framework, no JS libraries, fonts preconnected with
  `display=swap`
- Accessible: skip link, visible focus rings, `aria-current`, labelled form
  fields, `aria-expanded` accordions, and keyboard-operable before/after
  sliders (arrow keys, Home/End)

## Animation

Everything degrades cleanly and `prefers-reduced-motion: reduce` disables it all:

- **Hero slideshow** — crossfade with a slow Ken Burns push, per-slide progress
  bars, click to jump, pauses on hover and when the tab is hidden
- **Before/after sliders** — drag the handle (pointer or touch), or focus it and
  use arrow keys / Home / End. Each one sweeps itself once when it first
  scrolls into view, so the control explains itself
- **Work gallery** — snap-scrolling carousel with prev/next and swipe
- Staggered scroll reveals, self-drawing SVG icons, an animated process
  timeline, counting stats, a marquee trust bar and hover lifts

The `.reveal` opacity is only applied once JavaScript has run, so content is
never hidden from a crawler or a no-JS visitor.
