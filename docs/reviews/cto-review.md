# amianytime.com — CTO technical review (2026-09-09)

Numbers are from the live site (= repo HEAD `35898e0`); the clone's `img/` holds 35 uncommitted changes from another workstream and was ignored.

## Executive summary (for Frank)

1. The site starts fast: no JavaScript on 15 of 16 pages, 11 KB compressed HTML — leaner than Aldi (1,023 KB, 182 scripts) and Essential Everyday (36 scripts).
2. But Home pushes 1.2 MB of photos at once (18 images, none deferred): 6-8 s on a phone. A one-line change per image cuts first load to ~200 KB.
3. Google sees no product data: 0 structured-data blocks, no H1 on Home/Products/Product pages, and 165 of 178 catalog cards have no photo.
4. Forms do not work for most visitors: all 5 open the visitor's email app (`mailto:`), nothing is captured, and `info@afoodsinc.com` is exposed to spam bots 20 times.
5. Trust gaps: Privacy, Terms, Instagram, Facebook links go nowhere (`#`); the map sends visitor IPs to CARTO with no privacy notice; 404 page is GitHub's generic one.
6. All fixable in ~2 working days on the same free host; Frank only needs to open two free accounts (forms, monitoring).

## Findings (ranked by impact)

| # | Finding | Evidence | Fix | Effort | Who |
|---|---------|----------|-----|--------|-----|
| 1 | Images: no lazy-load, no width/height, no srcset, hero not preloaded | Home 1,207 KB (18 imgs eager); Recipes 587; Products 525; PDP 479; 0/20 lazy or sized → layout shift, LCP ~2.5 s mobile | `loading="lazy"` below fold, add dimensions, preload hero `gen-basket.webp` (88 KB), 2-size srcset for 1300 px photos | S | Claude now |
| 2 | Forms are `mailto:` — silent failure, address scraped | 5 forms × EN/ES `action="mailto:info@afoodsinc.com"`; 20 plain mailto links | Formspree free tier (GitHub-Pages compatible, spam filter); obfuscate address | S | Frank opens account (5 min) → Claude wires |
| 3 | Zero structured data; no Twitter card; PDP description 23 chars | 0 `ld+json` on 16 pages (benchmarks also 0); `twitter:*` 0 | JSON-LD (Organization, Product, BreadcrumbList, ItemList); `summary_large_image`; 140-char descriptions | S | Claude now |
| 4 | No H1 on key pages; heading levels skip | `index`, `products`, `product-tomato-paste` (EN+ES) h1=0; Home h2→h5, PDP uses h6 | Hero h2→h1; renumber | S | Claude now |
| 5 | Dead legal/social links; no privacy policy despite third-party map | `href="#"` Privacy/Terms/Instagram/Facebook every page; `basemaps.cartocdn.com` tiles | Privacy + Terms pages EN/ES naming CARTO/OSM/Google Fonts; fix or drop social links | M | Claude drafts, Frank approves |
| 6 | 149-SKU catalog, 13 photos | products.html: 178 `.pcard`, 13 `<img>` | Shoot/render range in batches | L | Frank (photo budget) |
| 7 | No HSTS/CSP; Leaflet CDN without SRI | Only `cache-control: max-age=600` header; cdnjs `leaflet.min.js/.css` no `integrity=` | SRI now; HSTS/CSP via free Cloudflare in front | S / M | Claude / Frank (DNS) |
| 8 | Small-text contrast fails AA | `#5F8F2A` on white 3.85:1 (12 px eyebrows); `#7C8592` 3.73:1 (11.5-13 px labels); NEW badge 3.45:1 | `#4F7A22` and `#5F6977` (≥4.5:1) | S | Claude now |
| 9 | Generator lost; 16 hand-copied pages | 29.7 KB `<style>` + nav/footer duplicated ×16 | Stdlib Python 3.9 generator in repo (see Architecture) | M | Claude now |
| 10 | Generic 404, no `favicon.ico`/manifest | `/nope` → "Page not found · GitHub Pages"; `/favicon.ico` 404 | Branded `404.html` (EN/ES), ico + manifest | S | Claude now |
| 11 | No skip link; burger lacks `aria-expanded`; lang toggle 22 px tall | `<button class="burger" aria-label="Menu" onclick=…>`; `.lang a{padding:2px 10px}` | Skip link, ARIA + Escape, 44 px toggle | S | Claude now |
| 12 | Render-blocking Google Fonts, no preconnect to `fonts.gstatic` | 9 KB CSS + 76 KB woff2 from 2 extra origins | Self-host 2 files, preload | S | Claude now |
| 13 | No analytics or uptime check | none | Plausible/GoatCounter (cookieless, no banner); UptimeRobot; Search Console | S | Frank accounts → Claude snippet |

**Working well:** HTTPS/www redirects, canonical + hreflang correct on all 16 pages, valid sitemap/robots, OG tags, viewport, focus/reduced-motion styles, alt on every image, no overflow risk (no tables, `minmax(0,1fr)` grids), 44 px burger.

## Benchmark

| Site | HTML | Scripts | HSTS/CSP | JSON-LD | Skip link | Alt gaps |
|------|------|---------|----------|---------|-----------|----------|
| amianytime.com | 50 KB | 0 | no/no | 0 | no | 0/20 |
| essentialeveryday.com | 50 KB | 36 | yes/yes | 0 | yes | 7/14 |
| aldi.us | 1,023 KB | 182 | yes/yes | 0 | yes | 0/29 |
| Walmart GV / Trader Joe's / Costco | bot-shielded | – | yes | – | – | – |

Closing #1-5 and #7-8 puts AMI ahead of all three on every measurable check.

## Architecture

Keep GitHub Pages. Rebuild the generator as a stdlib-only Python 3.9 `build.py` in the repo emitting the same flat HTML (Frank edits `content/*.json`, Claude builds and commits). Forms → Formspree; analytics → Plausible/GoatCounter; monitoring → UptimeRobot; Cloudflare free tier later for HSTS/CSP/caching.

## Do now (top 5)

1. Image pass (#1): lazy-load, dimensions, hero preload, srcset — Home 1.2 MB → ~200 KB first paint.
2. Replace the 5 `mailto:` forms with Formspree and hide the address (#2).
3. JSON-LD, H1s, Twitter cards (#3, #4) — SEO layer competitors lack.
4. Contrast colours, skip link, hamburger ARIA, Leaflet SRI (#7, #8, #11).
5. Rebuild the generator (#9), then 404, privacy/terms, self-hosted fonts (#5, #10, #12).
