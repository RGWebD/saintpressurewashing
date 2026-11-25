# Saint Pressure Washing LLC — build notes (RGWebD demo, 2026-11-25)
Live: https://rgwebd.github.io/saintpressurewashing/  ·  Generator: build.py → docs/

## Sources
- Facebook https://www.facebook.com/SaintPressureWashingLLC — intro, phone, IG, 2 verbatim recommendations, post captions + tagged places (see notes_fb.md)
- Their site https://saintpressurewashing.com (GoDaddy) — service descriptions, FAQ (pricing, soft washing, why a pro), slogan "you make the mess, we'll do the rest", logo PNG (transparent, 2560px), 4 job photos at 2560px
- Nextdoor https://nextdoor.com/pages/saint-pressure-washing-llc-cypress-tx/ — "Based out of Cypress", serves suburbs around Houston, email saintpressurewashing@gmail.com, neighbor rec by "C. S."
- Cylex directory — hours Mon–Fri 7:30–5:30, Sat 8:30–6:30, Sun 9:30–3:30 (matches Google AI summary) → shown as "hours as listed", flagged
- TX comptroller (via exa): LLC formed 2021-05-10, mailing address = 15103 Shady Gate Ct, Cypress 77429 (home address → NOT published)
- LinkedIn (Tony Beffer, Business Owner) says "fully insured" → NOT used (unconfirmed claim)

## Not verified / left out
- Google rating & review count (5.0/15 only in AI summary) → no aggregateRating, no stars
- Owner surname → not used (Tony appears only inside quoted reviews)
- Street address → not published (service-area business)

## Photo plan
- hero-lot = their site GENB1789 (2560) cropped to remove corner watermark — home hero full-bleed
- ada-stripes (site blob.png), residential-drive (RUBI8550), warehouse-midwash (IMG_1206) — services + gallery
- sweep-lot = f11→f12 (same lot before/after), sweep-annex = f13→f14; ECC-aligned, cropped left of watermark (tools/sweep.py)
- rig-night = FB cover; f01–f10, f16–f19 framed/cards/gallery; f18 business sign blurred
- dropped: f15 (weak, van + flag), FB logo.jpg (site PNG is better), site partner logos (list page)
