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
| Areas: Stockport, Cheadle, Cheadle Hulme, Gatley, Bramhall, Hazel Grove, Wythenshawe, Sale, Hale, Bowdon, Wilmslow, Alderley Edge, Prestbury ("and all areas of Manchester & Cheshire") | "Areas we cover" and contact graphics |
| Founder story ("started as an idea… a busy mum with big dreams", "Built around mum life. Built by me."), pet friendly, eco-conscious, Airbnb turnovers, 2–3 hour cleans, "New client enquiries welcome", @kjpristine.cleaning | Recent Facebook posts |
| Phone 07368 420872, kjpristinecleaning@gmail.com | Existing site and business card |
| Photos: kitchen, child's bedroom, wardrobe, bedroom reset, and the "5 hours, one home" bathroom, living room and oven | Cropped from screenshots of their posts. The AI-generated images of Kerri were deliberately **not** used |

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
5. **Quote form:** connected to Formspree (`https://formspree.io/f/mppwnykd`),
   so enquiries arrive by email at the address on that Formspree account. The
   first real submission may ask you to confirm the form in Formspree; after
   that it's automatic. If Formspree can't be reached, the visitor gets
   one-tap buttons to send the same enquiry by WhatsApp (07368 420872) or
   email. To use a different form, change `data-endpoint` and `action` on
   `<form id="quote-form">`.
6. **Logo:** `assets/img/logo.svg` is a vector redraw of the logo. If Kerri has
   the original artwork file, drop it in with the same name.
7. **Checks:** confirm with Kerri the "weekly or fortnightly" wording for
   regular cleans, the owner quote, and that the TikTok/Instagram links (taken
   from the links provided) match the `@kjpristine.cleaning` handle on her
   graphics.
8. **Photo of Kerri:** a real photo of her (not AI-generated) would suit the
   About section well.

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
