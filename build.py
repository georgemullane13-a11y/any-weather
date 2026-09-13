#!/usr/bin/env python3
"""
Static site generator for Any Weather Roofing Ltd.

Everything the site needs lives in this file: content, SEO metadata, structured
data and the HTML templates. Run `python3 build.py` to regenerate the site into
the repository root (the generated files are committed so the site can be served
straight from GitHub Pages / any static host with no build step).
"""

import os
import re
import html
import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()

# --------------------------------------------------------------------------- #
#  Business details
# --------------------------------------------------------------------------- #

SITE = {
    "name": "Any Weather Roofing Ltd",
    "short": "Any Weather Roofing",
    "tagline": "Quality roofing. Any weather.",
    "origin": "https://anyweatherroofingltd.co.uk",
    "phone_display": "07745 364 538",
    "phone_tel": "+447745364538",
    "whatsapp": "447745364538",
    "city": "Plymouth",
    "county": "Devon",
    "region": "Plymouth and the surrounding areas",
    "company_no": "15905071",
    "checkatrade": "https://www.checkatrade.com/trades/anyweatherroofingltd",
    "facebook": "https://www.facebook.com/people/Any-Weather-Roofing-LTD/",
    "recommend_pct": "100",
    "review_count": "27",
    "hours": "Free quote booked within 12 hours",
    "founded": "2024",
}

# Named on the original site.
PRIMARY_AREAS = [
    "Plymouth", "Plympton", "Plymstock", "Devonport",
    "Mutley", "Mannamead", "Stoke", "Eggbuckland",
]

# Further Plymouth neighbourhoods covered by "and surrounding areas".
WIDER_AREAS = [
    "Crownhill", "Derriford", "Peverell", "St Budeaux", "Honicknowle",
    "Southway", "Ernesettle", "Efford", "Laira", "Hooe", "Turnchapel",
    "Elburton", "Roborough", "Milehouse", "Keyham", "Ford",
    "Stonehouse", "Barbican", "Cattedown", "Whitleigh",
]

# --------------------------------------------------------------------------- #
#  Icons (24x24, stroke = currentColor)
# --------------------------------------------------------------------------- #

def _i(body, fill=False):
    attrs = 'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
    if fill:
        attrs = 'fill="currentColor" stroke="none"'
    return ('<svg viewBox="0 0 24 24" %s aria-hidden="true" focusable="false">%s</svg>' % (attrs, body))

ICONS = {
    "roof": _i('<path data-draw d="M2 11.2 12 3.4l10 7.8"/><path data-draw d="M4.6 10.2V20h14.8v-9.8"/><path data-draw d="M9.4 20v-5.2h5.2V20"/>'),
    "wrench": _i('<path data-draw d="M20.3 5.1a4.9 4.9 0 0 1-6.4 6.4L5.6 19.8a2 2 0 0 1-2.8-2.8l8.3-8.3a4.9 4.9 0 0 1 6.4-6.4L14.6 5.6l.9 2.9 2.9.9Z"/>'),
    "layers": _i('<path data-draw d="M12 3.2 21 8l-9 4.8L3 8Z"/><path data-draw d="M3 12.4 12 17.2 21 12.4"/><path data-draw d="M3 16.6 12 21.4 21 16.6"/>'),
    "gutter": _i('<path data-draw d="M3 6.5h18"/><path data-draw d="M3 6.5v3.6a2.4 2.4 0 0 0 2.4 2.4h13.2a2.4 2.4 0 0 0 2.4-2.4V6.5"/><path data-draw d="M8 15.4v2"/><path data-draw d="M12 15.4v3.4"/><path data-draw d="M16 15.4v2"/>'),
    "chimney": _i('<path data-draw d="M3 13 12 5.6 21 13"/><path data-draw d="M16.2 8.4V4.2h3.2v6.8"/><path data-draw d="M5.6 12.2V20h12.8v-7.8"/>'),
    "shield": _i('<path data-draw d="M12 2.8 20 6v6c0 4.6-3.3 7.6-8 9.2-4.7-1.6-8-4.6-8-9.2V6Z"/><path data-draw d="m8.8 11.9 2.2 2.2 4.2-4.4"/>'),
    "leaf": _i('<path data-draw d="M4 20c-1.4-7.6 3-13.4 16-13.4C20 16 14.6 21 4 20Z"/><path data-draw d="M4.8 19.2C8 14.6 11.6 11.8 16 10"/>'),
    "bolt": _i('<path data-draw d="M13.4 2.6 4.8 13.4h6l-1.2 8 8.6-10.8h-6Z"/>'),
    "phone": _i('<path data-draw d="M21 16.4v2.7a1.8 1.8 0 0 1-2 1.8 17.8 17.8 0 0 1-7.8-2.8 17.5 17.5 0 0 1-5.4-5.4A17.8 17.8 0 0 1 3 4.9a1.8 1.8 0 0 1 1.8-2h2.7a1.8 1.8 0 0 1 1.8 1.5c.1.9.3 1.7.6 2.5a1.8 1.8 0 0 1-.4 1.9L8.4 9.9a14.4 14.4 0 0 0 5.4 5.4l1.1-1.1a1.8 1.8 0 0 1 1.9-.4c.8.3 1.6.5 2.5.6A1.8 1.8 0 0 1 21 16.4Z"/>'),
    "check": _i('<circle data-draw cx="12" cy="12" r="9.2"/><path data-draw d="m8 12.3 2.7 2.7L16.3 9"/>'),
    "star": _i('<path d="m12 2.6 2.9 5.9 6.5.9-4.7 4.6 1.1 6.4-5.8-3-5.8 3 1.1-6.4L2.6 9.4l6.5-.9Z"/>', fill=True),
    "arrow": _i('<path d="M4 12h15"/><path d="m13 6 6 6-6 6"/>'),
    "arrow-left": _i('<path d="M20 12H5"/><path d="m11 6-6 6 6 6"/>'),
    "drag": _i('<path d="M9 6 3.6 12 9 18"/><path d="m15 6 5.4 6L15 18"/><path d="M12 3.6v16.8"/>'),
    "pin": _i('<path data-draw d="M12 21.4s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z"/><circle data-draw cx="12" cy="10.2" r="2.6"/>'),
    "clock": _i('<circle data-draw cx="12" cy="12" r="9.2"/><path data-draw d="M12 6.8V12l3.4 2"/>'),
    "mail": _i('<rect data-draw x="2.8" y="4.8" width="18.4" height="14.4" rx="2.4"/><path data-draw d="m3.4 6.6 8.6 6 8.6-6"/>'),
    "badge": _i('<circle data-draw cx="12" cy="9" r="6.2"/><path data-draw d="m8.4 14.4-1.2 7 4.8-2.6 4.8 2.6-1.2-7"/>'),
    "pound": _i('<path data-draw d="M14.8 5.6a3.6 3.6 0 0 0-6.2 2.5v3.3H6.4"/><path data-draw d="M8.6 11.4v3a3.4 3.4 0 0 1-1.6 3h10.4"/><path data-draw d="M7 11.4h6"/>'),
    "calendar": _i('<rect data-draw x="3.2" y="5" width="17.6" height="16" rx="2.4"/><path data-draw d="M3.2 10h17.6"/><path data-draw d="M8.4 3v4"/><path data-draw d="M15.6 3v4"/>'),
    "ruler": _i('<path data-draw d="m14.6 2.8 6.6 6.6L9.4 21.2 2.8 14.6Z"/><path data-draw d="m8.4 9 2 2"/><path data-draw d="m11.4 6 2 2"/><path data-draw d="m5.4 12 2 2"/>'),
    "sparkle": _i('<path data-draw d="M12 3.2 13.8 9l5.8 1.8-5.8 1.8L12 18.4l-1.8-5.8L4.4 10.8 10.2 9Z"/><path data-draw d="M18.6 4v2.6"/><path data-draw d="M19.9 5.3h-2.6"/>'),
    "users": _i('<path data-draw d="M16 20.4v-1.8a3.6 3.6 0 0 0-3.6-3.6H6.6A3.6 3.6 0 0 0 3 18.6v1.8"/><circle data-draw cx="9.5" cy="7.8" r="3.6"/><path data-draw d="M21 20.4v-1.8a3.6 3.6 0 0 0-2.7-3.5"/><path data-draw d="M15.6 4.4a3.6 3.6 0 0 1 0 6.9"/>'),
    "whatsapp": _i('<path d="M12 2.2A9.7 9.7 0 0 0 3.6 16.8L2.4 21.6l4.9-1.3A9.7 9.7 0 1 0 12 2.2Zm5.6 13.7c-.2.7-1.4 1.3-2 1.4-.5.1-1.2.1-1.9-.1a15 15 0 0 1-6.4-5.5c-.5-.8-.8-1.6-.8-2.4 0-.9.4-1.6.9-2.1.2-.2.4-.3.6-.3h.5c.2 0 .4 0 .6.4l.8 2c.1.2 0 .4-.1.5l-.4.5c-.1.2-.3.3-.1.6a9.4 9.4 0 0 0 3.7 3.2c.3.1.5.1.6-.1l.8-1c.2-.2.3-.2.6-.1l2 .9c.3.1.4.2.4.4.1.2.1.8-.1 1.2Z"/>', fill=True),
}

def icon(name, cls=""):
    svg = ICONS[name]
    if cls:
        svg = svg.replace("<svg ", '<svg class="%s" ' % cls, 1)
    return svg


# --------------------------------------------------------------------------- #
#  Services
# --------------------------------------------------------------------------- #

SERVICES = [
    {
        "slug": "new-roofs",
        "nav": "New Roofs",
        "card": "New Roofs & Re-roofing",
        "icon": "roof",
        "h1": "New Roofs & Full Re-roofing in Plymouth",
        "title": "New Roofs Plymouth | Full Re-roofing & Roof Replacement",
        "meta": "Complete new roofs and full re-roofing across Plymouth. Slate and tile coverings fitted properly, with free no-obligation quotes. Call 07745 364 538.",
        "blurb": "Complete roof replacements built to shrug off everything the South West throws at them — stripped, re-felted, re-battened and finished properly.",
        "intro": [
            "When a roof has reached the end of its working life, patching it stops being economical. A full re-roof strips the covering back to the rafters so every layer underneath can be inspected, replaced and rebuilt to current standards — not just the tiles you can see from the pavement.",
            "We re-roof Victorian terraces, post-war semis and new-build extensions right across Plymouth. Every job starts with a proper look in the loft and finishes with a tidy site, so you know exactly what you are paying for before a single tile is lifted.",
        ],
        "included_title": "What a full re-roof includes",
        "included": [
            "Strip of the existing covering, with responsible removal and disposal of all waste",
            "Inspection of rafters, purlins and wall plates, with timber replaced where it has rotted",
            "New breathable roofing membrane and treated battens set to the correct gauge",
            "Natural slate, fibre cement slate or concrete and clay tiles to match your property",
            "New lead flashings, valleys, ridge and hip finishes — dry-fixed where appropriate",
            "Fresh eaves protection, ventilation and, if needed, new fascias, soffits and guttering",
        ],
        "signs_title": "Signs your roof needs replacing rather than repairing",
        "signs": [
            "Repeated leaks in different places, or repairs that stop holding after a season",
            "Widespread slipped, cracked or delaminating slates and tiles",
            "Sagging between the rafters, or daylight visible through the roof from inside the loft",
            "Nail fatigue — slates sliding off in sound condition because the fixings have corroded",
            "Damp, staining or crumbling plaster on upstairs ceilings after heavy rain",
        ],
        "extra_title": "Built for Plymouth weather",
        "extra": [
            "Plymouth roofs work hard. Salt-laden air off the Sound corrodes fixings faster than inland, and Atlantic south-westerlies drive rain horizontally into details that would stay dry elsewhere. We specify materials and fixings with that in mind — stainless or copper nails where corrosion is a risk, mechanically fixed ridges instead of mortar alone on exposed elevations, and generous laps at the verges.",
            "You will get a clear written quotation setting out the covering, the underlay, the flashing details and the timescale. No vague figures, no surprises halfway through the job.",
        ],
        "faqs": [
            ("How long does a full re-roof take?",
             "Most standard Plymouth terraces and semis take between three days and a week, depending on the size of the roof, the access and the weather. We will give you a realistic timescale with your quote and let you know straight away if rain is going to push it back — a roof is never left open overnight."),
            ("How much does a new roof cost?",
             "It depends on the size and pitch of the roof, the covering you choose, the access, and what we find once the old covering is off. Natural slate costs more than concrete tile; a three-storey terrace with no rear access costs more than a bungalow. That is why we survey every roof in person and quote a fixed price in writing, free and with no obligation."),
            ("Will you need scaffolding?",
             "Yes — any full re-roof is scaffolded for safety and to protect your property. Scaffolding is included and coordinated by us, so you have one point of contact for the whole job."),
        ],
    },
    {
        "slug": "roof-repairs",
        "nav": "Roof Repairs",
        "card": "Roof Repairs & Maintenance",
        "icon": "wrench",
        "h1": "Roof Repairs & Maintenance in Plymouth",
        "title": "Roof Repairs Plymouth | Leaks, Slipped Slates & Maintenance",
        "meta": "Fast, honest roof repairs across Plymouth — leaks traced and fixed, slipped slates replaced, flashings renewed. Free quotes. Call 07745 364 538.",
        "blurb": "Leaks traced to their real source and fixed properly, from a single slipped slate to failed flashings and worn verge details.",
        "intro": [
            "Most roof leaks are not where the stain appears on the ceiling. Water travels along battens, rafters and felt before it drops, so the fix starts with finding the actual entry point rather than guessing at the nearest damaged tile.",
            "We handle everything from one-off repairs to planned maintenance on roofs that still have years left in them. If a repair is the right answer, we will say so — and if it is not, we will tell you that too.",
        ],
        "included_title": "Repairs we carry out",
        "included": [
            "Slipped, cracked and missing slates and tiles replaced to match",
            "Leak tracing and targeted repairs, including in-loft inspection",
            "Ridge and hip tiles re-bedded, re-pointed or dry-fixed",
            "Failed lead flashings, soakers and valleys renewed",
            "Verge and eaves repairs, including re-pointing and dry verge systems",
            "Felt, batten and timber repairs where water has already got in",
        ],
        "signs_title": "Worth getting looked at",
        "signs": [
            "Damp patches, staining or a musty smell in upstairs rooms",
            "Slates or fragments of mortar in the garden after a windy night",
            "Daylight through the roof, or wet felt and timber visible in the loft",
            "Sagging or blistered plaster around chimney breasts",
            "Gutters overflowing on one side of the house only",
        ],
        "extra_title": "Honest advice, either way",
        "extra": [
            "A repair should buy you real time, not just get you through until the next downpour. Where a roof genuinely has life left in it, we will make a sound repair and explain how long you can reasonably expect it to hold. Where the covering is beyond saving, we will show you why rather than sell you a patch that fails in six months.",
            "Small problems stay small if they are caught early. A single slipped slate costs very little to put back; the same slate left over a winter can cost you a ceiling.",
        ],
        "faqs": [
            ("How quickly can you come out?",
             "We aim to respond to repair enquiries quickly, and we run a 24-hour call-out for urgent leaks and storm damage. Call 07745 364 538 and we will tell you honestly when we can get to you."),
            ("Can you repair my roof if it is only one slate?",
             "Yes. No job is too small — replacing one slipped slate now is far cheaper than dealing with a rotten batten and a damaged ceiling later."),
            ("Do you charge for a quote?",
             "No. Quotes and estimates are free and carry no obligation. We will look at the roof, explain what we have found and put a price in writing."),
        ],
    },
    {
        "slug": "flat-roofing",
        "nav": "Flat Roofing",
        "card": "Flat Roofing",
        "icon": "layers",
        "h1": "Flat Roofing in Plymouth",
        "title": "Flat Roofing Plymouth | EPDM, GRP & Felt Flat Roofs",
        "meta": "Flat roof replacement and repair across Plymouth — extensions, dormers, garages and porches. Long-life membrane systems. Free quotes: 07745 364 538.",
        "blurb": "Warm, watertight flat roofs for extensions, dormers, garages and porches, laid with proper falls and detailed edges.",
        "intro": [
            "A flat roof only fails for a handful of reasons: standing water where the falls are wrong, split seams, tired upstands, or an edge detail that lets water track underneath. Get those right and a modern flat roof will outlast the felt roofs most people remember.",
            "We install and repair flat roofs on extensions, dormers, garages, porches and bay windows throughout Plymouth, matching the system to the job rather than fitting the same thing everywhere.",
        ],
        "included_title": "Flat roofing work we take on",
        "included": [
            "Full flat roof replacement, stripped back and re-decked where the boards have gone",
            "Single-ply and rubber membrane systems laid in one seamless piece",
            "Fibreglass (GRP) roofs with bonded trims for balconies and walk-on areas",
            "High-performance torch-on felt systems for larger and commercial roofs",
            "Correct falls built in, with new outlets, drips and edge trims",
            "Repairs to splits, blisters, ponding and failed upstands",
        ],
        "signs_title": "Telltale signs a flat roof is failing",
        "signs": [
            "Puddles still sitting on the roof days after the rain stopped",
            "Blisters, bubbles or splits across the surface",
            "Felt pulling away from the upstands or the wall abutment",
            "Damp appearing where the flat roof meets the main building",
            "Soft or springy spots underfoot, which usually means the decking is wet",
        ],
        "extra_title": "Choosing the right system",
        "extra": [
            "There is no single best flat roof — there is the right one for your roof. Rubber membranes suit simple rectangular extensions and go down in a single sheet with no seams to fail. Fibreglass is the better call for balconies and anywhere that gets walked on. Torch-on felt still earns its place on larger roofs and where budget matters.",
            "Whichever we recommend, the detailing is what decides how long it lasts: proper falls to the outlet, upstands taken high enough, and edges trimmed so wind cannot get under the membrane.",
        ],
        "faqs": [
            ("How long does a modern flat roof last?",
             "Far longer than the felt roofs of the 1970s. Quality membrane and fibreglass systems, correctly installed with the right falls and detailing, are designed to give decades of service. The installation matters as much as the material — ask about the guarantee offered on your quote."),
            ("Can you repair my flat roof instead of replacing it?",
             "Often, yes. Localised splits, failed seams and tired upstands can be repaired. If the decking underneath is already wet and soft, replacement is the honest answer — we will tell you which you are looking at."),
            ("Do you fit flat roofs on garages and porches?",
             "Yes. Garages, porches, dormers, bay windows and single-storey extensions are everyday work for us across Plymouth."),
        ],
    },
    {
        "slug": "roofline-fascias-soffits-guttering",
        "nav": "Roofline & Guttering",
        "card": "Roofline, Fascias & Guttering",
        "icon": "gutter",
        "h1": "Roofline, Fascias, Soffits & Guttering in Plymouth",
        "title": "Fascias, Soffits & Guttering Plymouth | Roofline Replacement",
        "meta": "UPVC fascias, soffits, bargeboards and guttering fitted across Plymouth. Stop overflowing gutters and rotten timber for good. Call 07745 364 538.",
        "blurb": "Fascias, soffits, bargeboards and guttering renewed so rainwater goes where it should and your timbers stay dry.",
        "intro": [
            "The roofline is the strip of your house that does the least glamorous job and takes the most punishment. Rotten fascias let water into the rafter feet; blocked or sagging gutters send it straight down the wall instead of into the drain.",
            "We replace tired timber and failing plastic roofline with low-maintenance UPVC systems, and we fit, repair and clear guttering across Plymouth, Plympton and Plymstock.",
        ],
        "included_title": "Roofline and rainwater work",
        "included": [
            "Full UPVC fascia, soffit and bargeboard replacement in white, black, grey or woodgrain",
            "New guttering, downpipes, hoppers and outlets correctly set to fall",
            "Over-cladding or full strip-off and replacement, depending on the condition of the timber",
            "Gutter clearing, re-fixing, re-aligning and leak repairs",
            "Dry verge systems to replace cracked mortar verges",
            "Eaves ventilation added where the loft needs airflow",
        ],
        "signs_title": "Signs your roofline needs attention",
        "signs": [
            "Water pouring over the gutter edge in heavy rain",
            "Green algae streaks or damp patches running down an external wall",
            "Flaking paint, soft timber or visible rot along the fascia board",
            "Gutter sections sagging, joints dripping, or brackets pulling away",
            "Birds or wasps getting in where the soffit has opened up",
        ],
        "extra_title": "Why it is worth doing properly",
        "extra": [
            "Guttering is cheap compared with the damage it prevents. Water running down a wall for a winter will find its way through the pointing, and once it is in the wall you are dealing with damp plaster and cold rooms rather than a leaking joint.",
            "We fit roofline as a complete system, so the fascia, the soffit, the ventilation and the gutter all work together rather than being three separate patch jobs from three different decades.",
        ],
        "faqs": [
            ("Do I need scaffolding for new fascias and guttering?",
             "For most two-storey properties, yes — it is safer and produces a much better finish than working off ladders. We will include any access equipment in your written quote."),
            ("Can you just clear my gutters?",
             "Yes. Gutter clearing and re-fixing is a common job for us, particularly after autumn leaf fall and after storms. We will let you know if we spot anything else that needs attention while we are up there."),
            ("How long does UPVC roofline last?",
             "Good-quality UPVC roofline needs no painting and typically lasts for decades — an occasional wash is all the maintenance it wants, which is why so many Plymouth homeowners move away from timber."),
        ],
    },
    {
        "slug": "chimney-repairs",
        "nav": "Chimney Work",
        "card": "Chimney Repairs & Repointing",
        "icon": "chimney",
        "h1": "Chimney Repairs, Repointing & Flashing in Plymouth",
        "title": "Chimney Repairs Plymouth | Repointing, Flashing & Rebuilds",
        "meta": "Chimney repointing, flashing renewal, flaunching and rebuilds across Plymouth. Stop chimney leaks and damp for good. Call 07745 364 538.",
        "blurb": "Repointing, flaunching, flashing renewal and partial rebuilds — the most common source of leaks on an otherwise sound roof.",
        "intro": [
            "Chimneys take weather from every side and have no roof of their own. On older Plymouth housing they are very often the real cause of a leak that looks like a roof problem — washed-out pointing, cracked flaunching at the top, or a flashing that gave up years ago.",
            "We repair, repoint, re-flash and where necessary rebuild chimney stacks, and we can remove a redundant stack and make good the roof if you would rather be rid of it.",
        ],
        "included_title": "Chimney work we carry out",
        "included": [
            "Repointing stacks in a suitable mortar mix, raked out properly first",
            "New flaunching to the top of the stack to shed water off the pots",
            "Lead flashings, soakers, back gutters and aprons renewed",
            "Partial and full stack rebuilds using matching or reclaimed brick",
            "Capping and venting disused flues to keep them dry and ventilated",
            "Chimney removal above or below roof level, with the roof made good",
        ],
        "signs_title": "Signs of a failing chimney",
        "signs": [
            "Damp staining on the chimney breast in a bedroom or loft",
            "Crumbling mortar joints, or sand collecting on the roof below the stack",
            "Cracked or missing flaunching around the base of the pots",
            "Lead flashing lifted, split, or held down with tar and hope",
            "The stack leaning noticeably out of upright",
        ],
        "extra_title": "Lead done properly",
        "extra": [
            "Most chimney leaks we are called to trace back to the flashing rather than the brickwork. Mortar fillets crack, cement 'repairs' shrink away from the stack, and lead that was never chased into the joints simply lifts in the wind.",
            "We use lead of the correct code, dressed to shape and wedged and pointed into raked-out joints, with soakers and a proper back gutter where the roof pitch needs one. Done once, it should outlast the covering around it.",
        ],
        "faqs": [
            ("My chimney is not used any more — should I remove it or keep it?",
             "Either is a valid answer. Keeping it preserves the look of the house and the option of a fire later, but it still needs maintaining. Removing it above roof level takes away the maintenance and the leak risk. We are happy to price both so you can decide."),
            ("Why does my chimney breast get damp in winter only?",
             "It usually points to water entering through the stack or the flashing and tracking down the flue, or to a disused flue with no ventilation. Both are fixable — the first step is a look at the stack itself."),
            ("Do you need scaffolding to work on a chimney?",
             "Almost always, yes. Chimney work needs safe, stable access to be done well, and we will include it in your quote rather than adding it later."),
        ],
    },
    {
        "slug": "lead-work",
        "nav": "Lead Work",
        "card": "Lead Work & Weatherproofing",
        "icon": "shield",
        "h1": "Lead Flashing, Valleys & Weatherproofing in Plymouth",
        "title": "Lead Work Plymouth | Flashing, Valleys & Weatherproofing",
        "meta": "Professional lead flashing, valleys, soakers and weatherproofing across Plymouth. Traditional leadwork, correctly detailed. Call 07745 364 538.",
        "blurb": "Traditional leadwork done to code — flashings, valleys, soakers and abutments detailed so junctions stay dry for decades.",
        "intro": [
            "Lead is what keeps the awkward parts of a roof dry: where it meets a wall, where two slopes meet, around a chimney, or over a bay window. It is also the first thing a cut-price job skimps on, which is why cracked mortar fillets and smeared-on sealant are such a common sight.",
            "We carry out proper leadwork across Plymouth — the right code of lead, correct bay lengths, dressed to shape and fixed so it can move without splitting.",
        ],
        "included_title": "Leadwork and weatherproofing",
        "included": [
            "Stepped and apron flashings to chimneys, parapets and abutments",
            "Open and secret lead valleys, re-lined or newly formed",
            "Soakers and cover flashings to side abutments",
            "Lead and fibreglass bay window and porch roofs",
            "Box gutters, back gutters and parapet gutter linings",
            "Replacement of failed cement fillets and previous sealant repairs",
        ],
        "signs_title": "Where lead usually lets go",
        "signs": [
            "Cracked cement fillets where lead should have been used in the first place",
            "Splits running across a flashing — usually lead laid in bays that were too long",
            "Lead lifting away from the wall because it was never chased into the joint",
            "Valleys blocked with debris, or lined lead that has thinned and holed",
            "Repeated damp at a single junction, no matter how many times it is sealed",
        ],
        "extra_title": "Why detail beats sealant",
        "extra": [
            "Sealant and flashing tape have their place as a genuine emergency measure. As a permanent fix they fail, because they rely on adhesion to a surface that is moving, wet and exposed to UV.",
            "Correctly formed lead relies on geometry instead: overlaps that shed water, clips that hold it down, and bay lengths that let the metal expand and contract without tearing. That is why lead flashings on well-built roofs are still doing their job a hundred years on.",
        ],
        "faqs": [
            ("Is lead still the best material for flashing?",
             "For most domestic roofs, yes — it is durable, malleable enough to dress to any shape, and fully recyclable. On some projects a lead substitute makes sense, particularly where theft is a concern, and we can talk you through the options."),
            ("Can you repair a lead valley without replacing the whole roof?",
             "Usually. Valleys can often be re-lined with the surrounding slates or tiles carefully lifted and re-laid, which is far less disruptive and far cheaper than a full re-roof."),
            ("Someone sealed my flashing with black mastic — can it be fixed properly?",
             "Yes. We remove the old repair, rake out the joints and fit new lead as it should have been done. It is one of the most common jobs we are called out to."),
        ],
    },
    {
        "slug": "moss-removal-roof-cleaning",
        "nav": "Moss & Cleaning",
        "card": "Moss Removal & Roof Cleaning",
        "icon": "leaf",
        "h1": "Moss Removal & Roof Cleaning in Plymouth",
        "title": "Roof Moss Removal & Cleaning Plymouth | Gutter Clearing",
        "meta": "Professional roof moss removal, roof cleaning and gutter clearing across Plymouth. Protect your tiles and clear your gutters. Call 07745 364 538.",
        "blurb": "Moss cleared, gutters flushed and the roof left clean — protecting the covering rather than blasting it to pieces.",
        "intro": [
            "Plymouth's damp, mild winters are ideal for moss. Left alone it holds water against the tiles, lifts the laps so wind-driven rain gets underneath, and eventually washes down into the gutters and blocks them.",
            "We clear moss and clean roofs carefully, using methods that suit the covering. A high-pressure lance can strip the protective surface from a concrete tile and force water under the laps, so it is not our default answer.",
        ],
        "included_title": "What roof cleaning covers",
        "included": [
            "Careful manual moss removal from tiles, slates and ridges",
            "Softwash treatment to kill remaining spores and slow regrowth",
            "Full gutter, hopper and downpipe clearing and flush",
            "All moss and debris bagged and removed from site",
            "Roof condition check while we are up there, reported back to you honestly",
            "Optional moss-inhibiting treatment to extend the clean",
        ],
        "signs_title": "Why moss is worth removing",
        "signs": [
            "Thick moss holds moisture against tiles through every frost cycle",
            "Debris washes into gutters and blocks downpipes, so water runs down walls",
            "Lifted laps let wind-driven rain travel under the covering",
            "Heavy growth adds weight and traps leaf litter in valleys",
            "A mossy roof makes an otherwise well-kept house look neglected",
        ],
        "extra_title": "Clean, not damaged",
        "extra": [
            "The aim of a roof clean is a roof that looks cared for and sheds water properly — not a roof that has had years taken off its life in an afternoon. We assess the covering first and choose the gentlest method that will do the job.",
            "We will also tell you what we find. If we spot a slipped slate, a cracked ridge or a failing flashing while the roof is clear, you will hear about it with a price to put it right — or a straight 'that can wait' if it can.",
        ],
        "faqs": [
            ("Does moss actually damage a roof?",
             "Indirectly, yes. The moss itself does not eat the tile, but it holds water against the covering, blocks gutters and valleys, and lifts the laps so rain can get underneath. On older or porous tiles the freeze-thaw cycle it encourages does cause real damage."),
            ("Will you jet wash my roof?",
             "Only where the covering can take it. High pressure can strip the surface off concrete tiles and drive water under the laps. Most roofs are better cleared by hand and then treated, which lasts longer and does no harm."),
            ("How often should a roof be cleaned?",
             "It depends on how shaded and sheltered your roof is. A north-facing roof under trees in a damp Plymouth valley will need attention far more often than an exposed south-facing one. Every few years is typical."),
        ],
    },
    {
        "slug": "emergency-roofing",
        "nav": "Emergency Call-out",
        "card": "Emergency & Storm Damage",
        "icon": "bolt",
        "h1": "Emergency Roofing & Storm Damage Repairs in Plymouth",
        "title": "Emergency Roofer Plymouth | 24 Hour Storm Damage Call-out",
        "meta": "24-hour emergency roofing call-out across Plymouth. Storm damage, urgent leaks and make-safe, with insurance work undertaken. Call 07745 364 538.",
        "blurb": "24-hour call-out for storm damage and urgent leaks — made safe and watertight first, repaired properly after.",
        "intro": [
            "When a south-westerly takes slates off in the middle of the night, the priority is stopping water getting into the house. We run a 24-hour call-out for exactly that: get there, make it safe, get it watertight, then sort the permanent repair in daylight.",
            "We also handle insurance work, so if you are claiming for storm damage we can document what we find and quote in the format your insurer needs.",
        ],
        "included_title": "Emergency response",
        "included": [
            "24-hour call-out for urgent leaks and storm damage",
            "Temporary make-safe — sheeting, tarping and securing loose material",
            "Removal of dangerous slates, tiles, ridges and debris",
            "Photographic record of the damage for your insurance claim",
            "Full written quote for the permanent repair, free of charge",
            "Insurance work undertaken, domestic and commercial",
        ],
        "signs_title": "Call straight away if",
        "signs": [
            "Water is actively coming through a ceiling or light fitting",
            "Slates, tiles or ridge sections have come off in a storm",
            "A chimney pot, stack or section of roofline looks unstable",
            "A flat roof has lifted or torn in high wind",
            "Debris has fallen and there is a risk to people below",
        ],
        "extra_title": "Stay safe while you wait",
        "extra": [
            "Keep everyone clear of the area below the damage and do not go up on the roof yourself — wet slate in wind is exactly as dangerous as it sounds. Inside, move what you can out of the way and put a container under the drip; if a ceiling is bulging with trapped water, keep out of the room and tell us when you call.",
            "If water is anywhere near light fittings or wiring, turn that circuit off at the consumer unit and leave it off until it has been checked.",
        ],
        "faqs": [
            ("Do you really answer out of hours?",
             "Yes — we operate a 24-hour call-out for genuine emergencies. Call 07745 364 538 and we will tell you honestly how quickly we can reach you."),
            ("Will my insurance cover storm damage?",
             "Most buildings policies cover storm damage, though excesses and conditions vary. We undertake insurance work and will photograph and document what we find so you have the evidence your insurer asks for."),
            ("What does a make-safe involve?",
             "Whatever it takes to stop further water getting in and to remove anything that could fall — usually sheeting over the damaged area, securing loose slates or ridge, and clearing debris. It is a temporary measure, followed by a proper repair once conditions allow."),
        ],
    },
]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}

# One photograph per service page (files live in assets/img/photos/).
SERVICE_PHOTO = {
    "new-roofs": ("work-1.jpg", "Completed new tiled roof on a Plymouth home"),
    "roof-repairs": ("work-2.jpg", "Roof stripped back to the battens during a repair"),
    "flat-roofing": ("ba-flat-after.jpg", "New seamless membrane flat roof with trimmed edges"),
    "roofline-fascias-soffits-guttering": ("work-6.jpg", "New fascias, soffits and guttering fitted"),
    "chimney-repairs": ("work-3.jpg", "Rebuilt chimney stack with new lead flashing"),
    "lead-work": ("work-4.jpg", "Dry-fixed ridge and new leadwork on a finished roof"),
    "moss-removal-roof-cleaning": ("work-5.jpg", "Roof cleared of moss and debris"),
    "emergency-roofing": ("hero-2.jpg", "Storm damaged roof made safe with scaffolding in place"),
}


# --------------------------------------------------------------------------- #
#  Shared chrome
# --------------------------------------------------------------------------- #

E = html.escape

NAV = [
    ("/", "Home"),
    ("/services/", "Services"),
    ("/areas-we-cover/", "Areas We Cover"),
    ("/about/", "About"),
    ("/contact/", "Contact"),
]

TEL = "tel:" + SITE["phone_tel"]
WA = "https://wa.me/" + SITE["whatsapp"]


def business_jsonld():
    return {
        "@type": ["RoofingContractor", "LocalBusiness"],
        "@id": SITE["origin"] + "/#business",
        "name": SITE["name"],
        "description": ("Roofing contractor in Plymouth, Devon, providing new roofs, roof repairs, "
                        "flat roofing, roofline and guttering, chimney work, leadwork, moss removal "
                        "and 24-hour emergency call-out."),
        "url": SITE["origin"] + "/",
        "telephone": SITE["phone_display"],
        "image": SITE["origin"] + "/assets/img/og-image.png",
        "logo": SITE["origin"] + "/assets/img/logo.svg",
        "priceRange": "££",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Plymouth",
            "addressRegion": "Devon",
            "addressCountry": "GB",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 50.3755, "longitude": -4.1427},
        "areaServed": [{"@type": "City", "name": a} for a in PRIMARY_AREAS],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday",
                          "Friday", "Saturday", "Sunday"],
            "opens": "00:00", "closes": "23:59",
        }],
        "sameAs": [SITE["checkatrade"]],
        "knowsAbout": [s["card"] for s in SERVICES],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Roofing services",
            "itemListElement": [{
                "@type": "Offer",
                "itemOffered": {"@type": "Service", "name": s["card"],
                                "url": SITE["origin"] + "/services/" + s["slug"] + "/"},
            } for s in SERVICES],
        },
    }


def jsonld(*objects):
    import json
    graph = {"@context": "https://schema.org", "@graph": list(objects)}
    return ('<script type="application/ld+json">%s</script>'
            % json.dumps(graph, ensure_ascii=False, separators=(",", ":")))


def breadcrumb_ld(trail):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [{
            "@type": "ListItem", "position": i + 1, "name": name,
            "item": SITE["origin"] + url,
        } for i, (url, name) in enumerate(trail)],
    }


def faq_ld(faqs):
    return {
        "@type": "FAQPage",
        "mainEntity": [{
            "@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        } for q, a in faqs],
    }


def head(title, desc, path, structured, og_type="website"):
    canonical = SITE["origin"] + path
    return """<!doctype html>
<html lang="en-GB" class="no-js">
<head>
<meta charset="utf-8">
<script>document.documentElement.className="js"</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#0a2035">
<meta name="author" content="{name}">
<meta name="geo.region" content="GB-PLY">
<meta name="geo.placename" content="Plymouth">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{name}">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{origin}/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{name} — roofing across Plymouth">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{origin}/assets/img/og-image.png">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=Source+Sans+3:wght@400;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/styles.css">
{structured}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
""".format(title=E(title), desc=E(desc), canonical=canonical, name=E(SITE["name"]),
           og_type=og_type, origin=SITE["origin"], structured=structured)


def site_header(active):
    links = "".join(
        '<a href="%s"%s>%s</a>' % (url, ' aria-current="page"' if url == active else "", E(label))
        for url, label in NAV
    )
    return """
<div class="topbar">
  <div class="container topbar__inner">
    <ul class="topbar__list">
      <li>{pin} {region}</li>
      <li>{clock} {hours}</li>
      <li>{badge} Checkatrade approved &amp; fully insured</li>
    </ul>
    <ul class="topbar__list">
      <li>{phone} <a href="{tel}"><strong>{phone_display}</strong></a></li>
    </ul>
  </div>
</div>
<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="/" aria-label="{name} — home">
      {logo}
      <span class="brand__text">
        <span class="brand__name">Any Weather</span>
        <span class="brand__tag">Roofing Ltd</span>
      </span>
    </a>
    <nav class="nav" id="primary-nav" aria-label="Primary">
      {links}
      <a class="btn btn--sm" href="/contact/">Get a free quote</a>
    </nav>
    <div class="header-actions">
      <a class="btn btn--sm" href="{tel}">{phone} {phone_display}</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Menu"><span></span></button>
    </div>
  </div>
</header>
""".format(links=links, tel=TEL, phone=icon("phone"), pin=icon("pin"), clock=icon("clock"),
           badge=icon("badge"), region=E(SITE["region"]), hours=E(SITE["hours"]),
           phone_display=SITE["phone_display"], name=E(SITE["name"]), logo=LOGO_SVG,
           founded=SITE["founded"])


def cta_band(heading, text, deep=True):
    return """
<section class="section section--{tone}">
  <div class="container">
    <div class="cta-band reveal">
      {mark}
      <span class="eyebrow">Free, no-obligation quote</span>
      <h2>{heading}</h2>
      <p>{text}</p>
      <div class="btn-row">
        <a class="btn" href="{tel}">{phone} Call {phone_display}</a>
        <a class="btn btn--light" href="{wa}" rel="noopener">{wa_icon} WhatsApp us</a>
        <a class="btn btn--light" href="/contact/">Request a callback</a>
      </div>
    </div>
  </div>
</section>
""".format(tone="mist" if deep else "paper", heading=E(heading), text=E(text), tel=TEL, wa=WA,
           phone=icon("phone"), wa_icon=icon("whatsapp"), phone_display=SITE["phone_display"],
           mark=CTA_MARK_SVG)


def site_footer():
    service_links = "".join('<li><a href="/services/%s/">%s</a></li>' % (s["slug"], E(s["card"]))
                            for s in SERVICES)
    area_links = "".join("<li>%s</li>" % E(a) for a in PRIMARY_AREAS)
    return """
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="/">
          {logo}
          <span class="brand__text">
            <span class="brand__name">Any Weather</span>
            <span class="brand__tag">Roofing Ltd</span>
          </span>
        </a>
        <p>Plymouth's trusted roofing specialists. Quality workmanship, honest advice and long-lasting protection — whatever the weather.</p>
        <p style="margin-top:1rem"><a class="link-arrow" href="{checkatrade}" rel="noopener nofollow">{badge} Checkatrade reviews {arrow}</a></p>
        <p style="margin-top:.5rem"><a class="link-arrow" href="{facebook}" rel="noopener nofollow">{users} Follow us on Facebook {arrow}</a></p>
      </div>
      <div>
        <h4>Services</h4>
        <ul class="footer-links">{service_links}</ul>
      </div>
      <div>
        <h4>Areas covered</h4>
        <ul class="footer-links">{area_links}<li><a href="/areas-we-cover/">See all areas</a></li></ul>
      </div>
      <div>
        <h4>Get in touch</h4>
        <ul class="footer-contact">
          <li>{phone}<span><a href="{tel}">{phone_display}</a><br>24-hour call-out</span></li>
          <li>{wa_icon}<span><a href="{wa}" rel="noopener">Message on WhatsApp</a></span></li>
          <li>{pin}<span>Plymouth, Devon<br>and surrounding areas</span></li>
          <li>{clock}<span>Free quotes, 7 days a week</span></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; <span data-year>2026</span> {name}. Registered in England &amp; Wales, company no. {company_no}.</p>
      <p><a href="/privacy/">Privacy</a> &middot; <a href="/sitemap.xml">Sitemap</a> &middot; <a href="/contact/">Contact</a></p>
    </div>
  </div>
</footer>
<div class="callbar">
  <a class="btn" href="{tel}">{phone} Call now</a>
  <a class="btn btn--light" href="{wa}" rel="noopener">{wa_icon} WhatsApp</a>
</div>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
""".format(logo=LOGO_SVG, service_links=service_links, area_links=area_links, tel=TEL, wa=WA,
           phone=icon("phone"), wa_icon=icon("whatsapp"), pin=icon("pin"), clock=icon("clock"),
           badge=icon("badge"), phone_display=SITE["phone_display"], name=E(SITE["name"]),
           company_no=SITE["company_no"], checkatrade=SITE["checkatrade"],
           facebook=SITE["facebook"], users=icon("users"), arrow=icon("arrow"))


def crumbs(trail):
    items = []
    for i, (url, name) in enumerate(trail):
        last = i == len(trail) - 1
        if last:
            items.append('<li><span aria-current="page">%s</span></li>' % E(name))
        else:
            items.append('<li><a href="%s">%s</a></li>' % (url, E(name)))
    return '<nav aria-label="Breadcrumb"><ol class="crumbs">%s</ol></nav>' % "".join(items)


def faq_section(faqs, heading="Frequently asked questions", intro=None, tone="paper"):
    items = []
    for i, (q, a) in enumerate(faqs):
        items.append("""
      <div class="faq__item">
        <h3 style="margin:0"><button class="faq__q" type="button" aria-expanded="false" aria-controls="faq-{i}"><span>{q}</span><span class="faq__icon" aria-hidden="true"></span></button></h3>
        <div class="faq__a" id="faq-{i}"><div><p>{a}</p></div></div>
      </div>""".format(i=i, q=E(q), a=E(a)))
    return """
<section class="section section--{tone}">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">Good to know</span>
      <h2>{heading}</h2>
      {intro}
    </div>
    <div class="faq reveal">{items}</div>
  </div>
</section>
""".format(tone=tone, heading=E(heading), items="".join(items),
           intro=("<p>%s</p>" % E(intro)) if intro else "")


# --------------------------------------------------------------------------- #
#  Brand marks and diagrams (inline SVG — no image weight)
# --------------------------------------------------------------------------- #

LOGO_SVG = """<svg class="brand__mark" viewBox="0 0 120 96" role="img" aria-label="Any Weather Roofing Ltd logo">
  <g fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
    <path d="M8 54a52 52 0 0 1 104 0"/>
    <path d="M18 78 46 50l17 17"/>
    <path d="M63 67 84 46l19 19v13"/>
    <path d="M18 78h85"/>
  </g>
  <g fill="currentColor">
    <rect x="76" y="56" width="8" height="8"/><rect x="88" y="56" width="8" height="8"/>
    <rect x="76" y="68" width="8" height="8"/><rect x="88" y="68" width="8" height="8"/>
  </g>
</svg>"""

CTA_MARK_SVG = """<svg class="cta-band__mark" viewBox="0 0 120 96" aria-hidden="true" focusable="false">
  <g fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M8 54a52 52 0 0 1 104 0"/><path d="M18 78 46 50l17 17"/>
    <path d="M63 67 84 46l19 19v13"/><path d="M18 78h85"/>
  </g>
</svg>"""


ROOF_SECTION_SVG = """<svg viewBox="0 0 700 400" role="img" aria-labelledby="sec-title">
  <title id="sec-title">Cross-section of a correctly built pitched roof: rafter, breathable membrane, treated batten and slate covering</title>
  <rect width="700" height="400" fill="#0d2942"/>
  <g stroke="#17456e" stroke-width="1" opacity=".5">""" + "".join(
    '<path d="M0 %d h700"/>' % y for y in range(0, 400, 28)
) + """</g>
  <g transform="rotate(-26 300 250)">
    <rect x="80" y="268" width="400" height="22" rx="2" fill="#3d2a1c"/>
    <rect x="80" y="268" width="400" height="22" rx="2" fill="none" stroke="#6b4a31" stroke-width="2"/>
    <path d="M80 262h400" stroke="#1e8bff" stroke-width="7" stroke-linecap="round" data-draw/>""" + "".join(
    '<rect x="%d" y="238" width="18" height="18" fill="#8a6440"/>' % x
    for x in range(96, 470, 62)
) + "".join(
    '<rect x="%d" y="226" width="96" height="12" rx="2" fill="%s"/>'
    % (86 + i * 62, "#2f4b66" if i % 2 else "#22394f") for i in range(6)
) + """
  </g>
  <g font-family="Archivo, sans-serif" font-size="15" font-weight="600" fill="#cfe0ef">
    <g stroke="#1e8bff" stroke-width="1.6" fill="none">
      <path d="M368 96h58"/><path d="M338 168h88"/><path d="M310 238h116"/><path d="M282 308h144"/>
    </g>
    <rect x="364" y="92" width="8" height="8" fill="#1e8bff" stroke="none"/>
    <rect x="334" y="164" width="8" height="8" fill="#1e8bff" stroke="none"/>
    <rect x="306" y="234" width="8" height="8" fill="#1e8bff" stroke="none"/>
    <rect x="278" y="304" width="8" height="8" fill="#1e8bff" stroke="none"/>
    <text x="434" y="101">Slate or tile covering</text>
    <text x="434" y="173">Treated batten</text>
    <text x="434" y="243">Breathable membrane</text>
    <text x="434" y="313">Sound rafter</text>
  </g>
</svg>"""


def coverage_svg():
    pins = [(300, 200, 12), (196, 148, 7), (400, 150, 7), (228, 268, 7),
            (386, 262, 7), (150, 214, 6), (452, 212, 6), (300, 302, 6)]
    dots = "".join(
        '<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
        % (x - r, y - r, r * 2, r * 2, "#1e8bff" if i == 0 else "#57a8ff")
        for i, (x, y, r) in enumerate(pins))
    rings = "".join(
        '<circle cx="300" cy="200" r="%d" fill="none" stroke="#1e8bff" stroke-width="1.4" opacity="%.2f"/>'
        % (60 + i * 52, 0.36 - i * 0.07) for i in range(4))
    spokes = "".join(
        '<path d="M300 200 L%d %d" stroke="#57a8ff" stroke-width="1.2" opacity=".26"/>' % (x, y)
        for x, y, _ in pins[1:])
    return ("""<svg viewBox="0 0 600 400" role="img" aria-label="Diagram showing roofing coverage radiating out from Plymouth">
  <rect width="600" height="400" fill="#0d2942"/>
  <g opacity=".6">%s</g>
  %s %s
  <circle cx="300" cy="200" r="26" fill="none" stroke="#1e8bff" stroke-width="2" opacity=".7" style="animation:pulsering 3s ease-out infinite;transform-origin:300px 200px"/>
  <text x="300" y="250" text-anchor="middle" font-family="Archivo, sans-serif" font-size="15" font-weight="700" letter-spacing="3" fill="#ffffff">PLYMOUTH</text>
</svg>""" % (rings, spokes, dots))


# --------------------------------------------------------------------------- #
#  Photography
#
#  Placeholders live in assets/img/photos/. Swap the files, keep the names.
# --------------------------------------------------------------------------- #

PHOTO_DIR = "/assets/img/photos/"

HERO_SLIDES = [
    ("hero-1.jpg", "Finished slate roof on a Plymouth property"),
    ("hero-2.jpg", "Stripped roof mid re-roof with scaffolding in place"),
    ("hero-3.jpg", "New tiled roof with fresh lead flashing to the chimney"),
]

BEFORE_AFTER = [
    {
        "id": "pitched",
        "title": "Full pitched re-roof",
        "where": "Plymouth",
        "before": "ba-pitched-before.jpg",
        "after": "ba-pitched-after.jpg",
        "alt_before": "Tired pitched roof with worn tiles and heavy moss before work started",
        "alt_after": "The same roof finished with new tiles, ridge and flashing",
        "copy": "Worn tiles, leaks and years of moss stripped back to the rafters, then rebuilt with new membrane, battens, tiles and lead.",
        "points": ["Brand new tiles", "Fully sealed", "Clean modern finish", "Built to last"],
    },
    {
        "id": "flat",
        "title": "Flat roof transformation",
        "where": "Plymouth",
        "before": "ba-flat-before.jpg",
        "after": "ba-flat-after.jpg",
        "alt_before": "Old failing flat roof with ponding and split seams",
        "alt_after": "New single-piece membrane flat roof with clean trimmed edges",
        "copy": "A failed felt roof replaced with a seamless membrane system, proper falls and new edge trims — watertight and walk-on ready.",
        "points": ["Watertight", "Enhanced durability", "Fast & reliable", "Built to last"],
    },
]

GALLERY = [
    ("work-1.jpg", "New tiled roof", "Full re-roof", "Completed pitched roof in new grey tiles"),
    ("work-2.jpg", "Strip and re-felt", "Re-roof in progress", "Roof stripped to the battens during a re-roof"),
    ("work-3.jpg", "Chimney and flashing", "Lead work", "Rebuilt chimney stack with new lead flashing"),
    ("work-4.jpg", "Ridge and hip finish", "New roof", "Dry-fixed ridge and hip tiles on a finished roof"),
    ("work-5.jpg", "Storm damage repair", "Emergency call-out", "Storm damaged roof made safe before repair"),
    ("work-6.jpg", "Roofline renewal", "Fascias and guttering", "New fascias, soffits and guttering fitted"),
]

# --------------------------------------------------------------------------- #
#  Page builders
# --------------------------------------------------------------------------- #

TRUST_POINTS = [
    ("badge", "Checkatrade approved"),
    ("shield", "Fully insured"),
    ("star", "100% recommended on Facebook"),
    ("clock", "24-hour call-out"),
    ("pound", "Free, no-obligation quotes"),
    ("calendar", "Quote booked within 12 hours"),
    ("users", "Domestic &amp; commercial"),
    ("check", "Insurance work undertaken"),
    ("pin", "Plymouth based"),
    ("sparkle", "Site left clean and tidy"),
]

PROCESS = [
    ("Get in touch", "Call, WhatsApp or send the form. Tell us what is happening and we will tell you straight away whether it is urgent."),
    ("Free survey", "We come out and look properly — including in the loft where it matters — so the diagnosis is based on evidence, not guesswork."),
    ("Fixed written quote", "A clear, itemised price with no obligation. You will know the materials, the method and the timescale before you commit."),
    ("Work done, site left tidy", "We turn up when we say, protect your property, and clear every last bit of waste before we leave."),
]

HOME_FAQS = [
    ("Do you charge for a quote?",
     "No. Every quote and estimate is free and carries no obligation. We will come out, look at the roof properly and put a clear written price in front of you."),
    ("Which areas do you cover?",
     "We cover Plymouth and the surrounding areas, including Plympton, Plymstock, Devonport, Mutley, Mannamead, Stoke and Eggbuckland. If you are just outside, call us — we will tell you honestly whether we can get to you."),
    ("Do you offer emergency call-out?",
     "Yes. We run a 24-hour call-out for storm damage and urgent leaks. We will make the roof safe and watertight first, then quote for the permanent repair."),
    ("Do you carry out insurance work?",
     "Yes. We undertake insurance work and will photograph and document storm damage so you have the evidence your insurer needs."),
    ("Do you work on commercial buildings as well as homes?",
     "We do. Alongside domestic roofing we take on commercial work — flat roof systems, maintenance and repairs on shops, offices and industrial units."),
    ("How do I know whether I need a repair or a new roof?",
     "A roof with sound timbers and isolated damage is usually worth repairing. Widespread slipped slates, repeated leaks in different places, failed fixings or sagging between the rafters normally point to a re-roof. We will show you what we have found and let you decide — we do not sell re-roofs to people who do not need one."),
]

TESTIMONIALS = [
    ("Very happy with the chimney work.", "Checkatrade review", "Chimney repairs, Plymouth"),
    ("Friendly, reliable and left everything tidy. Would recommend Any Weather Roofing.",
     "Checkatrade review", "Roofing work, Plymouth"),
    ("Great communication throughout.", "Checkatrade review", "Roof repair, Plymouth"),
]


def hero_slideshow():
    slides = "".join(
        '''<div class="hero__slide{active}"><img src="{dir}{file}" alt="{alt}" width="1800" height="1100"{loading}></div>'''.format(
            active=" is-active" if i == 0 else "", dir=PHOTO_DIR, file=f, alt=E(alt),
            loading='' if i == 0 else ' loading="lazy"')
        for i, (f, alt) in enumerate(HERO_SLIDES))
    dots = "".join(
        '''<button class="hero__dot" type="button" aria-current="{cur}" aria-label="Show photo {n} of {total}"><i></i></button>'''.format(
            cur="true" if i == 0 else "false", n=i + 1, total=len(HERO_SLIDES))
        for i in range(len(HERO_SLIDES)))
    return slides, dots


def ba_cards():
    out = []
    for b in BEFORE_AFTER:
        points = "".join("<li>%s %s</li>" % (icon("check"), E(pt)) for pt in b["points"])
        out.append('''
      <article class="ba-card reveal">
        <div class="ba-slider" data-ba style="--pos:50%">
          <img class="ba-slider__before" src="{dir}{before}" alt="{alt_before}" width="1400" height="1000" loading="lazy">
          <img class="ba-slider__after" src="{dir}{after}" alt="{alt_after}" width="1400" height="1000" loading="lazy">
          <span class="ba-slider__tag ba-slider__tag--before">Before</span>
          <span class="ba-slider__tag ba-slider__tag--after">After</span>
          <span class="ba-slider__line"></span>
          <button class="ba-slider__grip" type="button" role="slider" tabindex="0"
                  aria-label="{title} — drag to compare before and after"
                  aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">{grip}</button>
        </div>
        <div class="ba-card__body">
          <h3>{title}</h3>
          <p>{copy}</p>
          <ul class="ba-points">{points}</ul>
        </div>
      </article>'''.format(dir=PHOTO_DIR, before=b["before"], after=b["after"],
                           alt_before=E(b["alt_before"]), alt_after=E(b["alt_after"]),
                           title=E(b["title"]), copy=E(b["copy"]), points=points,
                           grip=icon("drag")))
    return "".join(out)


def gallery_block():
    items = "".join('''
        <figure class="gallery__item">
          <img src="{dir}{file}" alt="{alt}" width="1200" height="900" loading="lazy">
          <figcaption class="gallery__cap">{title}<span>{kind}</span></figcaption>
        </figure>'''.format(dir=PHOTO_DIR, file=f, alt=E(alt), title=E(title), kind=E(kind))
        for f, title, kind, alt in GALLERY)
    return '''
      <div class="gallery" data-gallery>
        <div class="gallery__track">{items}</div>
        <div class="gallery__nav">
          <button class="gallery__btn" type="button" data-gallery-prev aria-label="Previous photos">{left}</button>
          <button class="gallery__btn" type="button" data-gallery-next aria-label="More photos">{right}</button>
        </div>
      </div>'''.format(items=items, left=icon("arrow-left"), right=icon("arrow"))


def service_cards(limit=None, exclude=None):
    items = [s for s in SERVICES if s["slug"] != exclude]
    if limit:
        items = items[:limit]
    return "".join("""
      <article class="card card--link reveal">
        <span class="icon-square">{icon}</span>
        <h3><a href="/services/{slug}/">{card}</a></h3>
        <p>{blurb}</p>
        <span class="link-arrow">Read more {arrow}</span>
      </article>""".format(icon=icon(s["icon"]), slug=s["slug"], card=E(s["card"]),
                           blurb=E(s["blurb"]), arrow=icon("arrow"))
        for s in items)


def build_home():
    slides, dots = hero_slideshow()
    marquee_group = "".join('<span class="marquee__item">%s %s</span>' % (icon(i), t)
                            for i, t in TRUST_POINTS)
    steps = "".join("""
      <div class="step reveal">
        <div class="step__num">{n}</div>
        <h3>{title}</h3>
        <p>{body}</p>
      </div>""".format(n=i + 1, title=E(t), body=E(b)) for i, (t, b) in enumerate(PROCESS))
    quotes = "".join("""
      <figure class="quote reveal">
        <div class="quote__stars" aria-label="5 out of 5">{stars}</div>
        <blockquote>&ldquo;{text}&rdquo;</blockquote>
        <figcaption><b>{who}</b>{what}</figcaption>
      </figure>""".format(stars=icon("star") * 5, text=E(t), who=E(w), what=E(x))
        for t, w, x in TESTIMONIALS)
    areas = "".join('<li><a class="area-chip" href="/areas-we-cover/">%s</a></li>' % E(a)
                    for a in PRIMARY_AREAS)

    structured = jsonld(
        business_jsonld(),
        {"@type": "WebSite", "@id": SITE["origin"] + "/#website", "url": SITE["origin"] + "/",
         "name": SITE["name"], "inLanguage": "en-GB",
         "publisher": {"@id": SITE["origin"] + "/#business"}},
        faq_ld(HOME_FAQS),
    )

    body = """
<main id="main">
  <section class="hero">
    <div class="hero__stage" data-slideshow data-interval="6000">{slides}</div>
    <div class="hero__scrim"></div>
    <div class="container">
      <div class="hero__inner">
        <div class="hero__rule"></div>
        <h1>
          <span class="hero__kicker">Plymouth</span>
          <span class="hero__line" style="--d:.3s">Roofing done</span>
          <span class="hero__line hero__line--blue" style="--d:.4s">properly.</span>
        </h1>
        <p class="hero__lede">New roofs, roof repairs, flat roofing, guttering and emergency call-out across Plymouth and the surrounding areas. Quality roofing. Any weather.</p>
        <div class="btn-row">
          <a class="btn" href="/contact/">Request a free quote {arrow}</a>
          <a class="btn btn--light" href="{tel}">{phone} {phone_display}</a>
        </div>
        <ul class="hero__chips">
          <li class="chip">{check} Fully insured</li>
          <li class="chip">{calendar} Quote booked within 12hrs</li>
          <li class="chip">{clock} 24-hour call-out</li>
        </ul>
        <div class="hero__dots" role="group" aria-label="Choose a photo">{dots}</div>
      </div>
    </div>
    <div class="hero__stats">
      <div class="container">
        <ul>
          <li><div class="stat"><div class="stat__num"><span data-count="100">100</span><span class="u">%</span></div><div class="stat__label">Recommended</div></div></li>
          <li><div class="stat"><div class="stat__num"><span data-count="27">27</span></div><div class="stat__label">Facebook reviews</div></div></li>
          <li><div class="stat"><div class="stat__num">12<span class="u">hr</span></div><div class="stat__label">Quote booked in</div></div></li>
          <li><div class="stat"><div class="stat__num">24<span class="u">/7</span></div><div class="stat__label">Emergency call-out</div></div></li>
        </ul>
      </div>
    </div>
  </section>

  <div class="trustbar" aria-hidden="true">
    <div class="marquee">
      <div class="marquee__group">{marquee}</div>
      <div class="marquee__group">{marquee}</div>
    </div>
  </div>

  <section class="section section--paper" id="services">
    <div class="container">
      <div class="section-head center reveal">
        <span class="eyebrow">What we do</span>
        <h2>Roofing services across Plymouth</h2>
        <p>From a single slipped slate to a full re-roof, every job gets the same approach: find the real problem, explain it clearly, and fix it properly.</p>
      </div>
      <div class="grid grid--3" data-stagger="80">{cards}</div>
    </div>
  </section>

  <section class="section section--navy" id="before-after">
    <div class="container">
      <div class="section-head center reveal">
        <span class="eyebrow">Before &amp; after</span>
        <h2>Drag the slider. See the difference.</h2>
        <p>Real jobs, start to finish. Pull the handle across to reveal what the same roof looked like before we started.</p>
      </div>
      <div class="ba" data-stagger="120">{ba}</div>
    </div>
  </section>

  <section class="section section--paper" id="our-work">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Recent work</span>
        <h2>Roofs we have finished lately</h2>
        <p>Pitched re-roofs, flat roofs, chimneys, leadwork and roofline — all across Plymouth and the surrounding areas.</p>
      </div>
      <div class="reveal">{gallery}</div>
    </div>
  </section>

  <section class="section section--navy">
    <div class="container">
      <div class="split">
        <div class="reveal">
          <span class="eyebrow">Why homeowners choose us</span>
          <h2>A roof is only as good as the layers you cannot see</h2>
          <p>Anyone can lay tiles. What decides whether a roof still keeps water out in twenty years is the membrane, the battens, the fixings and the flashing detail underneath &mdash; the parts nobody inspects from the pavement.</p>
          <ul class="ticks">
            <li>{check}<div><strong>We diagnose before we quote</strong><span>Including a look in the loft, because the leak is rarely where the stain is.</span></div></li>
            <li>{check}<div><strong>Specified for the South West</strong><span>Salt air and Atlantic south-westerlies punish fixings and details. We allow for that.</span></div></li>
            <li>{check}<div><strong>Clear, fixed written quotes</strong><span>Materials, method and timescale on paper before any work starts. No surprises.</span></div></li>
            <li>{check}<div><strong>Tidy site, every time</strong><span>Property protected, waste removed, and we leave it as we found it.</span></div></li>
          </ul>
          <div class="btn-row" style="margin-top:2rem">
            <a class="btn" href="/about/">More about us {arrow}</a>
          </div>
        </div>
        <div class="frame reveal">{section_art}</div>
      </div>
    </div>
  </section>

  <section class="section section--mist">
    <div class="container">
      <div class="section-head center reveal">
        <span class="eyebrow">How it works</span>
        <h2>Four straightforward steps</h2>
        <p>No pressure, no sales visit dressed up as a survey, and no price that changes once the scaffolding is up.</p>
      </div>
      <div class="steps" data-stagger="110">{steps}</div>
    </div>
  </section>

  <section class="section section--paper">
    <div class="container">
      <div class="split split--reverse">
        <div class="frame reveal">{map_art}</div>
        <div class="reveal">
          <span class="eyebrow">Where we work</span>
          <h2>Covering Plymouth and the surrounding areas</h2>
          <p>We are Plymouth based, so we are local to the roofs we work on &mdash; which means faster call-outs, and we are still around if you need us again.</p>
          <ul class="area-chips">{areas}</ul>
          <div class="btn-row" style="margin-top:2rem">
            <a class="btn btn--ghost" href="/areas-we-cover/">See all areas covered {arrow}</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--mist">
    <div class="container">
      <div class="section-head center reveal">
        <span class="eyebrow">What customers say</span>
        <h2>100% recommended</h2>
        <p>Every one of our <a href="{facebook}" rel="noopener nofollow">27 Facebook reviews</a> recommends us, and our work is verified on <a href="{checkatrade}" rel="noopener nofollow">Checkatrade</a> too.</p>
      </div>
      <div class="grid grid--3" data-stagger="90">{quotes}</div>
    </div>
  </section>

  {faq}
  {cta}
</main>
""".format(slides=slides, dots=dots, tel=TEL, phone=icon("phone"),
           phone_display=SITE["phone_display"], arrow=icon("arrow"), check=icon("check"),
           clock=icon("clock"), calendar=icon("calendar"), marquee=marquee_group,
           cards=service_cards(), ba=ba_cards(), gallery=gallery_block(),
           section_art=ROOF_SECTION_SVG, steps=steps, map_art=coverage_svg(), areas=areas,
           quotes=quotes, checkatrade=SITE["checkatrade"], facebook=SITE["facebook"],
           faq=faq_section(HOME_FAQS, "Roofing questions, answered", tone="paper"),
           cta=cta_band("Get a free roofing quote in Plymouth",
                        "Tell us what is going on with your roof and we will come and look at it properly — free, with no obligation and no pressure."))

    return head(
        "Roofers in Plymouth | New Roofs & Repairs | Any Weather",
        "Trusted roofers in Plymouth. New roofs, repairs, flat roofing, guttering, chimney work and 24-hour emergency call-out. Free quotes — call 07745 364 538.",
        "/", structured) + site_header("/") + body + site_footer()


def build_services_index():
    structured = jsonld(
        business_jsonld(),
        breadcrumb_ld([("/", "Home"), ("/services/", "Services")]),
        {"@type": "CollectionPage", "name": "Roofing services in Plymouth",
         "url": SITE["origin"] + "/services/",
         "about": {"@id": SITE["origin"] + "/#business"}},
    )
    body = """
<main id="main">
  <section class="pagehead">
    <div class="container">
      {crumbs}
      <span class="eyebrow">Our services</span>
      <h1>Roofing services in Plymouth</h1>
      <p>Eight specialist services covering everything a pitched or flat roof in the South West is likely to need &mdash; from urgent leaks at midnight to a full re-roof booked in for the spring.</p>
      <div class="btn-row">
        <a class="btn" href="{tel}">{phone} Call {phone_display}</a>
        <a class="btn btn--light" href="/contact/">Request a free quote {arrow}</a>
      </div>
    </div>
  </section>

  <section class="section section--paper">
    <div class="container">
      <div class="grid grid--3" data-stagger="80">{cards}</div>
    </div>
  </section>

  <section class="section section--navy">
    <div class="container">
      <div class="split">
        <div class="reveal">
          <span class="eyebrow">Not sure what you need?</span>
          <h2>Tell us the symptom &mdash; we will find the cause</h2>
          <p>Most people call us about a damp patch, not a failed flashing. That is fine. Describe what you can see and we will work out what is actually causing it, then tell you what it will take to put right.</p>
          <ul class="ticks">
            <li>{check}<div><strong>Damp on an upstairs ceiling</strong><span>Usually a slipped slate, a failed flashing or a blocked valley &mdash; rarely where the stain appears.</span></div></li>
            <li>{check}<div><strong>Water running down an outside wall</strong><span>Typically guttering: blocked, sagging, or set to the wrong fall.</span></div></li>
            <li>{check}<div><strong>Damp on the chimney breast</strong><span>Nearly always the stack itself &mdash; pointing, flaunching or flashing.</span></div></li>
            <li>{check}<div><strong>Puddles on a flat roof</strong><span>Falls in the wrong place, and a sign the covering is on borrowed time.</span></div></li>
          </ul>
        </div>
        <div class="frame reveal">{art}</div>
      </div>
    </div>
  </section>

  <section class="section section--mist">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Recent work</span>
        <h2>Roofs we have finished lately</h2>
      </div>
      <div class="reveal">{gallery}</div>
    </div>
  </section>

  {cta}
</main>
""".format(gallery=gallery_block(), crumbs=crumbs([("/", "Home"), ("/services/", "Services")]), tel=TEL,
           phone=icon("phone"), phone_display=SITE["phone_display"], arrow=icon("arrow"),
           cards=service_cards(), check=icon("check"), art=ROOF_SECTION_SVG,
           cta=cta_band("Free quotes on every service",
                        "One call gets you an honest opinion and a fixed written price. If a repair will do, we will say so."))
    return head(
        "Roofing Services in Plymouth | Repairs & New Roofs",
        "New roofs, repairs, flat roofing, fascias and guttering, chimney work, leadwork, moss removal and 24-hour emergency call-out across Plymouth.",
        "/services/", structured) + site_header("/services/") + body + site_footer()


def service_photo(slug):
    f, alt = SERVICE_PHOTO[slug]
    return ('<img src="%s%s" alt="%s" width="1200" height="900" loading="lazy">'
            % (PHOTO_DIR, f, E(alt)))


def build_service(s):
    trail = [("/", "Home"), ("/services/", "Services"),
             ("/services/%s/" % s["slug"], s["card"])]
    structured = jsonld(
        business_jsonld(),
        breadcrumb_ld(trail),
        {"@type": "Service", "name": s["card"], "serviceType": s["card"],
         "url": SITE["origin"] + "/services/" + s["slug"] + "/",
         "description": s["meta"],
         "provider": {"@id": SITE["origin"] + "/#business"},
         "areaServed": [{"@type": "City", "name": a} for a in PRIMARY_AREAS]},
        faq_ld(s["faqs"]),
    )
    included = "".join("<li>%s</li>" % E(x) for x in s["included"])
    signs = "".join("<li>%s</li>" % E(x) for x in s["signs"])
    intro = "".join("<p>%s</p>" % E(p) for p in s["intro"])
    extra = "".join("<p>%s</p>" % E(p) for p in s["extra"])

    body = """
<main id="main">
  <section class="pagehead">
    <div class="container">
      {crumbs}
      <span class="eyebrow">{nav}</span>
      <h1>{h1}</h1>
      <p>{blurb}</p>
      <div class="btn-row">
        <a class="btn" href="{tel}">{phone} Call {phone_display}</a>
        <a class="btn btn--light" href="{wa}" rel="noopener">{wa_icon} WhatsApp us</a>
      </div>
    </div>
  </section>

  <section class="section section--paper">
    <div class="container">
      <div class="split">
        <div class="reveal prose">
          <span class="icon-square">{icon}</span>
          <h2 style="margin-top:1.4rem">{included_title}</h2>
          {intro}
          <ul>{included}</ul>
        </div>
        <div class="reveal">
          <div class="card" style="box-shadow:var(--shadow-md)">
            <span class="icon-square icon-square--light">{warn}</span>
            <h3 style="margin-top:1.15rem">{signs_title}</h3>
            <div class="prose" style="margin-top:1rem"><ul>{signs}</ul></div>
          </div>
          <div class="callout" style="margin-top:1.25rem">
            <p><strong>Not sure how serious it is?</strong> Send us a photo on WhatsApp and we will give you an honest opinion before anyone comes out.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--navy">
    <div class="container">
      <div class="split">
        <div class="reveal">
          <span class="eyebrow">The detail that matters</span>
          <h2>{extra_title}</h2>
          {extra}
          <div class="btn-row" style="margin-top:2rem">
            <a class="btn" href="/contact/">Get a free quote {arrow}</a>
          </div>
        </div>
        <div class="frame reveal">{art}</div>
      </div>
    </div>
  </section>

  {faq}

  <section class="section section--mist">
    <div class="container">
      <div class="section-head center reveal">
        <span class="eyebrow">Related</span>
        <h2>Other roofing services</h2>
      </div>
      <div class="grid grid--3" data-stagger="80">{related}</div>
    </div>
  </section>

  {cta}
</main>
""".format(crumbs=crumbs(trail), nav=E(s["nav"]), h1=E(s["h1"]), blurb=E(s["blurb"]),
           tel=TEL, phone=icon("phone"), phone_display=SITE["phone_display"], wa=WA,
           wa_icon=icon("whatsapp"), icon=icon(s["icon"]), included_title=E(s["included_title"]),
           intro=intro, included=included, warn=icon("bolt"), signs_title=E(s["signs_title"]),
           signs=signs, extra_title=E(s["extra_title"]), extra=extra, arrow=icon("arrow"),
           art=service_photo(s["slug"]),
           faq=faq_section(s["faqs"], "%s — your questions" % s["nav"], tone="paper"),
           related=service_cards(limit=3, exclude=s["slug"]),
           cta=cta_band("Free quote for %s in Plymouth" % s["nav"].lower(),
                        "Call, message or send a photo. We will tell you what is wrong, what it takes to fix it, and what it costs — before you commit to anything."))
    return head(s["title"], s["meta"], "/services/%s/" % s["slug"], structured,
                og_type="article") + site_header("/services/") + body + site_footer()


AREA_NOTES = {
    "Plymouth": "From the Victorian terraces of the city centre to the post-war estates that ring it, Plymouth roofs take the full force of Atlantic weather. We work right across the city on everything from single slate replacements to full re-roofs.",
    "Plympton": "Plympton's mix of period cottages around the Ridgeway and large modern estates means very different roofs on the same round. We cover both — tiled estate roofs, slate on the older properties, and plenty of extension flat roofs.",
    "Plymstock": "Exposed, close to the water and regularly on the receiving end of wind-driven rain. Plymstock roofs tend to show their age at the verges and ridges first, which is where a lot of our repair work here starts.",
    "Devonport": "Dense terraced housing with shared party walls, valley gutters and tall chimney stacks. Access and neighbourly care matter as much as the roofing here, and we plan jobs accordingly.",
    "Mutley": "Large Victorian and Edwardian properties, many converted to flats, with steep slate roofs and complex valley and dormer details. Leadwork and valley repairs are our most common call here.",
    "Mannamead": "Substantial period homes with natural slate, decorative ridge and original leadwork worth preserving. We repair sympathetically and match materials wherever we can.",
    "Stoke": "A mix of period terraces and later infill, with plenty of rendered walls where a failing gutter quickly turns into a damp problem inside. Roofline and rainwater work is a regular job here.",
    "Eggbuckland": "Largely post-war housing with concrete tile roofs now reaching the age where fixings fatigue and ridges need re-bedding. Moss growth on the shadier elevations is common too.",
}


def build_areas():
    trail = [("/", "Home"), ("/areas-we-cover/", "Areas We Cover")]
    structured = jsonld(
        business_jsonld(), breadcrumb_ld(trail),
        {"@type": "WebPage", "name": "Areas we cover",
         "url": SITE["origin"] + "/areas-we-cover/",
         "about": {"@id": SITE["origin"] + "/#business"}},
    )
    cards = "".join("""
      <article class="card reveal">
        <span class="icon-square icon-square--light">{pin}</span>
        <h3>Roofers in {area}</h3>
        <p>{note}</p>
        <a class="link-arrow" href="/contact/">Get a quote in {area} {arrow}</a>
      </article>""".format(pin=icon("pin"), area=E(a), note=E(AREA_NOTES[a]), arrow=icon("arrow"))
        for a in PRIMARY_AREAS)
    wider = "".join('<li><span class="area-chip">%s</span></li>' % E(a) for a in WIDER_AREAS)

    body = """
<main id="main">
  <section class="pagehead">
    <div class="container">
      {crumbs}
      <span class="eyebrow">Coverage</span>
      <h1>Roofers covering Plymouth &amp; the surrounding areas</h1>
      <p>We are based in Plymouth and work across the city and the neighbourhoods around it. Being local means we can get to urgent jobs quickly — and that we are still here if you need us again in five years.</p>
      <div class="btn-row">
        <a class="btn" href="{tel}">{phone} Call {phone_display}</a>
        <a class="btn btn--light" href="/contact/">Check your postcode {arrow}</a>
      </div>
    </div>
  </section>

  <section class="section section--paper">
    <div class="container">
      <div class="section-head center reveal">
        <span class="eyebrow">Primary coverage</span>
        <h2>Where we work most</h2>
        <p>Different parts of Plymouth throw up different roofing problems. Here is what we tend to see where.</p>
      </div>
      <div class="grid grid--3" data-stagger="70">{cards}</div>
    </div>
  </section>

  <section class="section section--navy">
    <div class="container">
      <div class="split">
        <div class="frame reveal">{map_art}</div>
        <div class="reveal">
          <span class="eyebrow">And the rest of the city</span>
          <h2>Also working throughout</h2>
          <p>Our round covers the wider Plymouth area too. If your postcode is not on the list, call us anyway — we will give you a straight answer rather than waste your time.</p>
          <ul class="area-chips">{wider}</ul>
        </div>
      </div>
    </div>
  </section>

  {faq}
  {cta}
</main>
""".format(crumbs=crumbs(trail), tel=TEL, phone=icon("phone"),
           phone_display=SITE["phone_display"], arrow=icon("arrow"), cards=cards,
           map_art=coverage_svg(), wider=wider,
           faq=faq_section([
               ("Do you charge extra for travel within Plymouth?",
                "No. Anywhere in Plymouth and the surrounding areas listed here is part of our normal round, and quotes are free wherever you are on that list."),
               ("I am just outside your area — can you still come?",
                "Quite possibly. Call us with your postcode and we will tell you straight away whether we can take it on rather than stringing you along."),
               ("How quickly can you reach an emergency in Plymouth?",
                "We operate a 24-hour call-out and being locally based means we are usually not far away. Call 07745 364 538 and we will give you an honest time."),
           ], "Coverage questions", tone="paper"),
           cta=cta_band("Roofing quotes across Plymouth",
                        "Free, no-obligation and with honest advice attached — wherever you are in the city."))
    return head(
        "Areas We Cover | Roofers in Plymouth & Surrounding Areas",
        "We cover Plymouth, Plympton, Plymstock, Devonport, Mutley, Mannamead, Stoke, Eggbuckland and nearby. Free roofing quotes — call 07745 364 538.",
        "/areas-we-cover/", structured) + site_header("/areas-we-cover/") + body + site_footer()


def build_about():
    trail = [("/", "Home"), ("/about/", "About")]
    structured = jsonld(
        business_jsonld(), breadcrumb_ld(trail),
        {"@type": "AboutPage", "name": "About Any Weather Roofing Ltd",
         "url": SITE["origin"] + "/about/",
         "about": {"@id": SITE["origin"] + "/#business"}},
    )
    values = [
        ("check", "Honest advice", "If a repair will do, we will tell you. We would rather have a customer for twenty years than one oversold job."),
        ("ruler", "Quality workmanship", "The right materials, the right fixings and the right details — including the ones nobody will ever see."),
        ("shield", "Long-lasting protection", "Every decision is made with the next storm in mind, not just the next inspection."),
        ("sparkle", "Respect for your home", "Property protected, waste taken away, and the site left clean before we go."),
    ]
    value_cards = "".join("""
      <article class="card reveal">
        <span class="icon-square">{icon}</span>
        <h3>{title}</h3>
        <p>{body}</p>
      </article>""".format(icon=icon(i), title=E(t), body=E(b)) for i, t, b in values)

    body = """
<main id="main">
  <section class="pagehead">
    <div class="container">
      {crumbs}
      <span class="eyebrow">About us</span>
      <h1>A Plymouth roofing company built on doing it properly</h1>
      <p>Any Weather Roofing Ltd is a Plymouth-based roofing contractor working across the city and the surrounding areas, on everything from urgent leaks to complete re-roofs.</p>
      <div class="btn-row">
        <a class="btn" href="{tel}">{phone} Call {phone_display}</a>
        <a class="btn btn--light" href="{checkatrade}" rel="noopener nofollow">{badge} Our Checkatrade profile</a>
      </div>
    </div>
  </section>

  <section class="section section--paper">
    <div class="container">
      <div class="split">
        <div class="prose reveal">
          <span class="eyebrow">Our approach</span>
          <h2 style="margin-top:.8rem">Fewer shortcuts, fewer callbacks</h2>
          <p>Roofing has a reputation problem, and it is not hard to see why. A roof is the one part of a house most people never see, which makes it the easiest place to cut a corner — a cement fillet instead of lead, a tile laid over a rotten batten, a flat roof with no fall in it.</p>
          <p>We built this company to work the other way round. Every job starts with a proper diagnosis, including a look in the loft where it matters, and every quote sets out what we are actually doing in writing before anyone commits to anything.</p>
          <p>That means we occasionally talk people out of work they were expecting to pay for. It also means most of our work comes from people who have used us before, or who were told about us by someone who did.</p>
          <h3>Local, and staying local</h3>
          <p>We are based in Plymouth and work in Plymouth. There is no call centre, no national franchise and no doorstep sales operation — you speak to the people who will be on your roof, and we are still down the road if anything needs looking at again.</p>
          <p>Being local also shapes the work itself. Roofs here deal with salt-laden air off the Sound and Atlantic south-westerlies that drive rain sideways into details that would stay dry inland. We specify fixings and flashing details with that in mind, because a roof that would be fine in the Midlands is not necessarily fine in Plymstock.</p>
        </div>
        <div class="reveal">
          <div class="frame">{art}</div>
          <div class="card" style="margin-top:1.25rem">
            <h3>Company details</h3>
            <div class="prose" style="margin-top:1rem">
              <ul>
                <li><strong>{name}</strong></li>
                <li>Registered in England &amp; Wales, company no. {company_no}</li>
                <li>Checkatrade approved &middot; VAT registered</li>
                <li>Domestic and commercial work undertaken</li>
                <li>Insurance work undertaken</li>
                <li>24-hour call-out, 7 days a week</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--mist">
    <div class="container">
      <div class="section-head center reveal">
        <span class="eyebrow">What we stand on</span>
        <h2>Four things we do not compromise on</h2>
      </div>
      <div class="grid grid--4" data-stagger="80">{value_cards}</div>
    </div>
  </section>

  {cta}
</main>
""".format(crumbs=crumbs(trail), tel=TEL, phone=icon("phone"),
           phone_display=SITE["phone_display"], checkatrade=SITE["checkatrade"],
           badge=icon("badge"), art=service_photo("new-roofs"), name=E(SITE["name"]),
           company_no=SITE["company_no"], value_cards=value_cards,
           cta=cta_band("Talk to a Plymouth roofer directly",
                        "No sales team, no scripts. Call and you will speak to someone who actually works on roofs."))
    return head(
        "About Us | Plymouth Roofing Contractor | Any Weather Roofing",
        "Plymouth-based roofing contractor offering honest advice, quality workmanship and long-lasting protection across Plymouth and surrounding areas.",
        "/about/", structured) + site_header("/about/") + body + site_footer()


def build_contact():
    trail = [("/", "Home"), ("/contact/", "Contact")]
    structured = jsonld(
        business_jsonld(), breadcrumb_ld(trail),
        {"@type": "ContactPage", "name": "Contact Any Weather Roofing Ltd",
         "url": SITE["origin"] + "/contact/",
         "about": {"@id": SITE["origin"] + "/#business"}},
    )
    options = "".join('<option value="%s">%s</option>' % (E(s["card"]), E(s["card"]))
                      for s in SERVICES)
    body = """
<main id="main">
  <section class="pagehead">
    <div class="container">
      {crumbs}
      <span class="eyebrow">Get in touch</span>
      <h1>Free roofing quotes across Plymouth</h1>
      <p>Call, WhatsApp or send us the details below. Photos help enormously &mdash; if you can safely take one from the ground, send it and we can often tell you what you are dealing with before we come out.</p>
      <div class="btn-row">
        <a class="btn" href="{tel}">{phone} Call {phone_display}</a>
        <a class="btn btn--light" href="{wa}" rel="noopener">{wa_icon} WhatsApp us</a>
      </div>
    </div>
  </section>

  <section class="section section--paper">
    <div class="container">
      <div class="split">
        <div class="reveal">
          <span class="eyebrow">Request a quote</span>
          <h2 style="margin-top:.8rem">Tell us about your roof</h2>
          <p class="lede" style="margin-top:1rem">We will come back to you with an honest first opinion and, if it needs a visit, a time that suits you.</p>
          <ul class="ticks">
            <li>{check}<div><strong>Free and no obligation</strong><span>A quote costs you nothing and commits you to nothing.</span></div></li>
            <li>{clock}<div><strong>24-hour call-out</strong><span>If it is urgent, call rather than fill in a form — we answer out of hours.</span></div></li>
            <li>{shield}<div><strong>Insurance work</strong><span>Storm damage documented and quoted in the format insurers ask for.</span></div></li>
          </ul>
          <div class="card" style="margin-top:2rem">
            <h3>Contact details</h3>
            <ul class="footer-contact" style="margin-top:1.1rem;color:var(--ink-soft)">
              <li>{phone}<span><a href="{tel}" style="color:var(--ember-600)">{phone_display}</a><br>24 hours, 7 days a week</span></li>
              <li>{wa_icon}<span><a href="{wa}" rel="noopener" style="color:var(--ember-600)">Message us on WhatsApp</a></span></li>
              <li>{pin}<span>Plymouth, Devon &mdash; covering Plymouth, Plympton, Plymstock, Devonport, Mutley, Mannamead, Stoke and Eggbuckland</span></li>
              <li>{badge}<span>Company no. {company_no} &middot; Checkatrade approved</span></li>
            </ul>
          </div>
        </div>

        <div class="reveal">
          <form class="form-card" action="{form_action}" method="POST">
            <div class="field-row">
              <div class="field">
                <label for="name">Your name</label>
                <input id="name" name="name" type="text" autocomplete="name" required>
              </div>
              <div class="field">
                <label for="phone">Phone number</label>
                <input id="phone" name="phone" type="tel" autocomplete="tel" required>
              </div>
            </div>
            <div class="field">
              <label for="email">Email address</label>
              <input id="email" name="email" type="email" autocomplete="email">
            </div>
            <div class="field-row">
              <div class="field">
                <label for="postcode">Postcode</label>
                <input id="postcode" name="postcode" type="text" autocomplete="postal-code" placeholder="e.g. PL4 6AB">
              </div>
              <div class="field">
                <label for="service">What do you need?</label>
                <select id="service" name="service">
                  <option value="">Not sure / something else</option>
                  {options}
                </select>
              </div>
            </div>
            <div class="field">
              <label for="message">Tell us what is happening</label>
              <textarea id="message" name="message" placeholder="For example: damp patch on the bedroom ceiling after heavy rain, and a slate came down in the last storm." required></textarea>
            </div>
            <button class="btn" type="submit" style="width:100%">{mail} Send my enquiry</button>
            <p class="form-note">We only use your details to answer your enquiry. Urgent? Call <a href="{tel}" style="color:var(--ember-600);font-weight:600">{phone_display}</a> &mdash; we answer 24 hours.</p>
          </form>
        </div>
      </div>
    </div>
  </section>

  {cta}
</main>
""".format(crumbs=crumbs(trail), tel=TEL, phone=icon("phone"),
           phone_display=SITE["phone_display"], wa=WA, wa_icon=icon("whatsapp"),
           check=icon("check"), clock=icon("clock"), shield=icon("shield"), pin=icon("pin"),
           badge=icon("badge"), company_no=SITE["company_no"], options=options,
           mail=icon("mail"), form_action=FORM_ACTION,
           cta=cta_band("Prefer to talk it through?",
                        "Call and you will get someone who knows roofs, not a call handler reading from a script."))
    return head(
        "Contact Us | Free Roofing Quotes in Plymouth | Any Weather",
        "Get a free, no-obligation roofing quote in Plymouth. Call 07745 364 538, message on WhatsApp or send an enquiry. 24-hour call-out.",
        "/contact/", structured) + site_header("/contact/") + body + site_footer()


# Set this to your form back-end (Formspree, Netlify Forms, Basin, a PHP handler,
# …). Until it is set, the form posts nowhere — the phone and WhatsApp links are
# the live routes. See README.md.
FORM_ACTION = "https://formspree.io/f/REPLACE_WITH_YOUR_FORM_ID"


def build_privacy():
    trail = [("/", "Home"), ("/privacy/", "Privacy")]
    structured = jsonld(business_jsonld(), breadcrumb_ld(trail))
    body = """
<main id="main">
  <section class="pagehead">
    <div class="container">
      {crumbs}
      <span class="eyebrow">Legal</span>
      <h1>Privacy policy</h1>
      <p>How {name} handles the information you give us through this website.</p>
    </div>
  </section>
  <section class="section section--paper">
    <div class="container narrow prose">
      <h2>What we collect</h2>
      <p>If you use the enquiry form on this site we collect the name, phone number, email address, postcode and message you choose to give us. If you call or message us we keep a record of that conversation so we can answer it properly.</p>
      <h2>Why we collect it</h2>
      <p>Only to respond to your enquiry, provide a quotation and carry out any work you go on to instruct. We do not sell your details, and we do not pass them to third parties for marketing.</p>
      <h2>How long we keep it</h2>
      <p>Enquiries that do not lead to work are kept only as long as they are useful, and then deleted. Records relating to work carried out are kept for as long as we are required to keep them for accounting, warranty and insurance purposes.</p>
      <h2>Cookies</h2>
      <p>This website does not set advertising or tracking cookies. Web fonts are loaded from Google Fonts, which means your browser makes a request to Google's servers when the page loads.</p>
      <h2>Your rights</h2>
      <p>Under UK data protection law you can ask us what information we hold about you, ask us to correct it, or ask us to delete it. Call <a href="{tel}">{phone_display}</a> and we will deal with it.</p>
      <h2>Contact</h2>
      <p>{name}, registered in England &amp; Wales, company no. {company_no}. Telephone <a href="{tel}">{phone_display}</a>.</p>
      <div class="callout" style="margin-top:2rem">
        <p><strong>Note for the site owner:</strong> this policy is a starting point written to match how the site currently works. Review it — and add your registered address and a contact email — before relying on it.</p>
      </div>
    </div>
  </section>
</main>
""".format(crumbs=crumbs(trail), name=E(SITE["name"]), tel=TEL,
           phone_display=SITE["phone_display"], company_no=SITE["company_no"])
    return head("Privacy Policy | Any Weather Roofing Ltd",
                "How Any Weather Roofing Ltd collects, uses and protects the information you provide through this website.",
                "/privacy/", structured) + site_header("/privacy/") + body + site_footer()


def build_404():
    page = head("Page not found | Any Weather Roofing Ltd",
                "The page you were looking for could not be found.",
                "/404.html", jsonld(business_jsonld()))
    page = page.replace('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
                        '<meta name="robots" content="noindex, follow">')
    body = """
<main id="main">
  <section class="pagehead">
    <div class="container">
      <span class="eyebrow">Error 404</span>
      <h1>That page has slipped off the roof</h1>
      <p>The page you were after is not here any more. Try one of these instead &mdash; or just call us, which is usually quicker anyway.</p>
      <div class="btn-row">
        <a class="btn" href="{tel}">{phone} Call {phone_display}</a>
        <a class="btn btn--light" href="/">Back to the homepage</a>
      </div>
    </div>
  </section>
  <section class="section section--paper">
    <div class="container">
      <div class="grid grid--3" data-stagger="70">{cards}</div>
    </div>
  </section>
</main>
""".format(tel=TEL, phone=icon("phone"), phone_display=SITE["phone_display"],
           cards=service_cards(limit=6))
    return page + site_header("/") + body + site_footer()


# --------------------------------------------------------------------------- #
#  Non-HTML assets
# --------------------------------------------------------------------------- #

def sitemap(paths):
    urls = "".join(
        "<url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>"
        % (SITE["origin"], p, TODAY, freq, pri) for p, freq, pri in paths)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % urls)


ROBOTS = """User-agent: *
Allow: /

Sitemap: {origin}/sitemap.xml
""".format(origin=SITE["origin"])

WEBMANIFEST = """{{
  "name": "{name}",
  "short_name": "Any Weather Roofing",
  "description": "Roofing across Plymouth — new roofs, repairs, flat roofing and 24-hour emergency call-out.",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0a2035",
  "icons": [
    {{ "src": "/assets/img/favicon.svg", "sizes": "any", "type": "image/svg+xml" }},
    {{ "src": "/assets/img/apple-touch-icon.png", "sizes": "180x180", "type": "image/png" }}
  ]
}}
""".format(name=SITE["name"])

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect width="120" height="120" rx="26" fill="#0a2035"/>
  <g transform="translate(0 14)" fill="none" stroke="#ffffff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
    <path d="M12 52a48 48 0 0 1 96 0"/>
    <path d="M21 76 47 50l16 16"/>
    <path d="M63 66 82 47l18 18v11"/>
    <path d="M21 76h79"/>
  </g>
  <g fill="#1e8bff" transform="translate(0 14)">
    <rect x="75" y="56" width="8" height="8"/><rect x="87" y="56" width="8" height="8"/>
    <rect x="75" y="67" width="8" height="8"/><rect x="87" y="67" width="8" height="8"/>
  </g>
</svg>
"""


# --------------------------------------------------------------------------- #
#  Write everything out
# --------------------------------------------------------------------------- #

def write(rel_path, content):
    full = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)
    return rel_path


def main():
    written = []
    written.append(write("index.html", build_home()))
    written.append(write("services/index.html", build_services_index()))
    for s in SERVICES:
        written.append(write("services/%s/index.html" % s["slug"], build_service(s)))
    written.append(write("areas-we-cover/index.html", build_areas()))
    written.append(write("about/index.html", build_about()))
    written.append(write("contact/index.html", build_contact()))
    written.append(write("privacy/index.html", build_privacy()))
    written.append(write("404.html", build_404()))

    paths = [("/", "weekly", "1.0"), ("/services/", "monthly", "0.9")]
    paths += [("/services/%s/" % s["slug"], "monthly", "0.8") for s in SERVICES]
    paths += [("/areas-we-cover/", "monthly", "0.7"), ("/about/", "yearly", "0.6"),
              ("/contact/", "yearly", "0.8"), ("/privacy/", "yearly", "0.2")]
    written.append(write("sitemap.xml", sitemap(paths)))
    written.append(write("robots.txt", ROBOTS))
    written.append(write("site.webmanifest", WEBMANIFEST))
    written.append(write("assets/img/favicon.svg", FAVICON))

    for path in written:
        print("  wrote", path)
    print("\n%d files written." % len(written))


if __name__ == "__main__":
    main()
