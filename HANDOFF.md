# HANDOFF — ami anytime website · state as of 2026-09-09 13:00 ET

Written by Claude (Frank Stanzione's chief-of-staff agent) for the next builder (Codex). Everything needed to continue is in this repo, plus the two Dropbox folders named below for source art. Read `AGENTS.md` first for the rules.

## 1. Where things are

| Thing | Address |
|---|---|
| Live site | https://amianytime.com (EN) · https://amianytime.com/es/ (ES) — 8 pages each |
| Repo (source of truth) | github.com/Afoodsinc/amieveryday-site — branch `main`, root, public. Repo name is legacy; the domain is amianytime.com. Owner org: `Afoodsinc` (AFI-owned; Frank's GitHub). |
| Hosting | GitHub Pages, custom domain via the `CNAME` file, Enforce HTTPS ON, certificate issued. Cache header `max-age=600`. No HSTS/CSP (GitHub Pages limitation; Cloudflare free tier would add them — owner decision). |
| DNS (GoDaddy, Frank's account) | amianytime.com: A @ → 185.199.108/109/110/111.153, CNAME www → afoodsinc.github.io. 11 other domains 301-forward to https://amianytime.com: amieveryday.com, amianytime.co, ami-brands.com, amilabel.com, theamibrand.com, theamibrands.net/.info/.shop/.store/.xyz, theamistore.com. Every GoDaddy save needs Frank's SMS code. **Do not touch.** |
| Backlog | `docs/reviews/cto-review.md` and `docs/reviews/ux-review.md` (ranked, with evidence and paste-ready copy) |
| Source art (designer packshots) | Dropbox: `Frank Claude AI/Ami Own Brand proyect/06 Brand & Marketing/_website-source/` → `Deck English2 (2026-09-08).pdf` (17-page catalogue, latest art), `deck-2026-09-08-extracted-art/` (35 PNGs pulled from the PDF: 3-view can renders 1536×1024, drink rows, tuna trio, ketchup, soy, noodles, lineup 3010×2000, lifestyle, badge, lockup, tagline) and `_web-assets-QA-sheet.png`. Web-ready WebP versions are already in `img/`. |
| AI lifestyle renders | Dropbox: `…/06 Brand & Marketing/_web-lifestyle-renders/` (Higgsfield nano-banana-pro; `gen-*.webp`, `recipe-*.webp`) |
| SKU list | Dropbox: `Frank Claude AI/Knowledge/source-files/AMI_Own_Brand_Program_149_SKUs.xlsx` (the 149-product program). ⚠️ It disagrees with the deck (see §4). |
| Project record (decisions, history) | Dropbox: `Frank Claude AI/Projects/ami-website.md` |
| Company contact facts used on the site | 2300 NW 92nd Ave, Doral, FL 33172 · PH Plaza del Este, Torre A, Piso 13, Costa del Este, Panamá · +1 877 894 7675 · +507 310 7576 · info@afoodsinc.com (**mailbox unverified** — confirm with Jorge, AFI IT) |

## 2. What is built (all live)
- 16 pages: Home, About, Products, Product detail (tomato paste), Recipes (6 EN/ES), Where to buy (Leaflet map, 11 markets: launching Miami/S. Florida, Panamá, Dominican Republic; next GT, SV, HN, PR, Bahamas, Jamaica, Aruba, T&T), Partners (program, inquiry form), Contact.
- Products page: **"Launch range 2026" section** (`#launch`, 29 items with final art and metric sizes) followed by the full 149-product program by 8 aisles (most items "coming soon", placeholder icons).
- Done 2026-09-09 from the CTO/UX reviews: lazy-loaded images with dimensions, hero preload, H1s, JSON-LD (Organization, BreadcrumbList, ItemList of 29, Product), twitter card, AA contrast, skip link + `#main`, `aria-expanded` on the hamburger, SRI on Leaflet, mismatched art removed, PDP language toggle fixed. Home first-load images 1,207 KB → 88 KB.
- EN/ES toggle in the top bar on every page; hamburger menu on mobile (inline JS on the button).

## 3. How the site was produced, and why there is no build
A Python generator (`gen.py` + `template.html` + `skus.json`) produced the pages; the working copy lived in a temporary folder that was wiped. `tools/legacy/` holds the ORIGINAL versions recovered from the session log — later patches (Home nav, launch section, image swaps, CTO fixes) are NOT in them. **The HTML in this repo is the truth.** Recommended next step (CTO review #5): rebuild a stdlib-only Python 3.9 `build.py` with `templates/` + `content/*.json` that regenerates exactly the current HTML, commit its output, keep the flat layout. No Node on Frank's Mac; Codex cloud may use whatever it likes as long as committed output stays flat HTML.

## 4. Open decisions (Frank / Fredy — do not decide for them)
1. **Hero copy.** UX proposal: EN "Always with you. Never over budget." + one line on what ami is; ES "Siempre contigo. Nunca fuera de presupuesto." CTAs "See what's on shelf" / "For retailers". Current: "Global flavors. Honest prices. Every day."
2. **Products page structure.** UX proposal: "On shelf now — 29" + the 149 program as a department index (aisle, count, 3 examples) instead of ~100 grey cards. Frank previously asked to keep the original design → needs his yes.
3. **Forms backend.** All forms are `mailto:` (fail silently on many phones). Options: Formspree free tier (Frank opens account) or an n8n webhook (AFI has n8n Cloud, unproven). Add success state + consent line + Privacy page.
4. **Legal pages.** Privacy/Terms links are `#`. Draft EN/ES naming CARTO/OSM map tiles, Google Fonts, form vendor; Frank approves.
5. **Catalogue truth.** Deck = 29 launch items in metric sizes (400 g cans, 170 g tuna, 340/425 g corn, 284 g mushrooms, 425 g peach, 340 g ketchup, 500 ml soy, 85 g noodles, 200 ml / 1 L drinks). Workbook = 149 SKUs in US sizes, missing whole-peeled/chopped tomatoes 400 g, baby corn, light/dark soy, pineapple drink. Ask Jorge/Fredy which list is the listing truth before rebuilding the catalogue data.
6. **Where-to-buy pre-launch copy** ("one retail partner per country; store list published the week ami reaches the shelf; leave your email"). Delete "Hispanic supermarkets and independents" (contradicts exclusivity).
7. **One partner sentence** everywhere: "ami is licensed to one retail partner per country, category by category, with price shielding written into the license." Site currently says "select few"/"one"/"single" inconsistently and "21 departments" vs 8 aisles.

## 5. Backlog that needs no decision (ranked, from the reviews)
- Branded 404 page (`404.html` at root; GitHub Pages serves it).
- ES catalogue: the 149 program names are still English on `/es/products.html`.
- Recipes: 5 of 6 use non-launch products → rewrite around the 29 launch items (tomato, beans, tuna, corn, mushrooms, noodles, peach, drinks).
- `srcset` two sizes for the 1300 px lifestyle photos; self-host fonts (or keep Google Fonts + preconnect, already done).
- Filters/sort chips on Products are inert (no JS) → make them work or remove.
- Aisle rail hidden below 1100 px → add an in-page aisle jump menu for tablet/phone.
- Wordmark alt text: use "ami anytime" (a dotless ı in one image alt makes screen readers say "amıanytime").
- Analytics (Plausible or GoatCounter, cookieless), UptimeRobot, Google Search Console — Frank opens accounts.
- Consolidate 30+ ad-hoc font sizes into the type scale.

## 6. Scores to beat (2026-09-09)
UX 6/10. Benchmark /30: Aldi 20 · Trader Joe's 20 · Essential Everyday 18 · Great Value 17 · **ami 17** (wins bilingual 4/5 and B2B path 4/5; loses product browse 2/5 and where-to-buy 1/5). Technical: lighter than all benchmarks; gaps were structured data, forms, legal pages, HSTS/CSP.

## 7. People
Frank Stanzione (CEO, owner, non-technical — wants numbers and decisions, not options) · Jorge (AFI IT: DNS, mailboxes, accounts) · Fredy (AMI brand decisions) · Anyela (marketing execution) · Jhonathan (designer; source of all packshots).

## Change log
- 2026-09-03 — site v1 published (EN/ES, 16 pages), domain amianytime.com bound, HTTPS enforced, 11 domains forwarded.
- 2026-09-09 — new deck art (29-item launch range, real packshots site-wide, new lineup/lifestyle) · CTO + UX reviews · same-day fixes (see §2) · this handoff.
- 2026-09-09 — added a branded bilingual 404 page with clear EN/ES routes back to Home and Products.
- 2026-09-09 — translated all 149 full-program product names on the Spanish catalogue and normalized launch terminology to neutral Latin American Spanish.
- 2026-09-09 — rewrote all six recipes in English and Spanish around the 29 launch products, corrected metric pack sizes, and removed non-launch ami ingredient claims.
- 2026-09-09 — added responsive two-size WebP delivery for large lifestyle, recipe, banner, and lineup images across both languages, including responsive preloads.
- 2026-09-09 — made the canned-goods filters keyboard-accessible and functional in English and Spanish, added live result counts, and removed the fake one-option sort.
