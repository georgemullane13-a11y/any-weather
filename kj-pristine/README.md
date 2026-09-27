# KJ Pristine: website mockup

A one-page, mobile-first, SEO-optimised site for **KJ Pristine**, Kerri Jackson's
owner-operated premium domestic cleaning and housekeeping business in South
Manchester and Cheshire.

It's plain HTML, CSS and JavaScript: no frameworks and no build step. Open
`index.html`, or serve the folder:

```bash
cd kj-pristine && python3 -m http.server 8000
# → http://localhost:8000
```

## Where the content came from

Everything is taken from KJ Pristine's own social posts, flyers and existing site:

| Used on the site | Source |
| --- | --- |
| Logo, colours (sage, forest, terracotta, dusty rose, cream), serif + script type | Logo post, "Areas we cover" and flyer graphics |
| "Clean spaces. Brighter places.", "Exceptional care for exceptional homes", "You look after them, I'll look after your home" | Social graphics |
| KJ Signature Clean, KJ Deep Clean, KJ Home Reset, regular cleans, add-ons, bespoke quotes | Printed service flyer |
| Declutter & Organisation **from £35/hour** (add-on or standalone) | "Autumn reset" post |
| Fully insured, DBS checked, Level 5 British Cleaning qualified, owner operated, eco-friendly | Post footers and existing site |
| Payment terms (25% deposit on deep cleans/resets) and 24-hour satisfaction promise | Payment info and checklist sheets |
| Areas: Stockport, Cheadle, Cheadle Hulme, Gatley, Bramhall, Hazel Grove, Wythenshawe, Sale, Hale, Wilmslow | "Areas we cover" post |
| Phone 07368 420872, kjpristinecleaning@gmail.com | Existing site and business card |
| Before/after photos (kitchen, bedroom, wardrobe) | Cropped from screenshots of their posts |

## Before going live

1. **Photos:** the images in `assets/img/` are cropped from phone screenshots,
   so they are low resolution. Ask Kerri for the original photos and replace
   them, keeping the same filenames. The kitchen pair drives the drag slider,
   so both photos need to be framed the same way.
2. **Reviews:** the three review cards are clearly marked *Sample review:
   replace*. Swap in real Facebook or Google reviews, with the customer's
   permission. Never publish invented reviews.
3. **Domain:** replace `https://www.kjpristine.co.uk/` in `index.html`
   (canonical, Open Graph and schema) with the real domain.
4. **WhatsApp:** the buttons use `wa.me/447368420872`. Confirm that number is on WhatsApp.
5. **Quote form:** set `data-endpoint` on `<form id="quote-form">` to a
   Formspree, Netlify Forms or similar URL. While it's empty the form runs in
   demo mode: it validates the fields and shows the thank-you message, but
   sends nothing.
6. **Logo:** `assets/img/logo.svg` is a vector redraw of the logo. If Kerri has
   the original artwork file, drop it in with the same name.
7. **Checks:** confirm the "weekly or fortnightly" wording for regular cleans
   and the owner quote attribution with Kerri.

## SEO included

- Title, meta description, canonical, Open Graph, `en-GB`, geo meta
- A single H1, with H2s per section and H3s per card
- JSON-LD `HouseCleaning` (LocalBusiness) with the areas served, services, the
  £35/hr price, founder and social links, plus `FAQPage` schema
- A local-search section written naturally around "cleaning services near
  me", "local cleaning company", domestic and deep cleaning, and each town
- Descriptive alt text on every image; lazy loading below the fold; no framework JavaScript

## Animation and interaction

Staggered hero entrance, twinkling sparkles, scroll reveals, card hover glow,
a drag before/after slider with an automatic "peek" when it first comes into
view, tap-to-reveal photo pairs, scrolling brand taglines, map pins that drop
in, a swipeable reviews carousel on mobile, a floating-label form with
validation and a success state, and a sticky Call / WhatsApp / Quote bar on
mobile. It all honours `prefers-reduced-motion`.
