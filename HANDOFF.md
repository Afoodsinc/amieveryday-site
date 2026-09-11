# HANDOFF — ami anytime website · state as of 2026-09-11

Written by Claude (Frank Stanzione's chief-of-staff agent) for the next builder (Codex). Everything needed to continue is in this repo, plus the two Dropbox folders named below for source art. Read `AGENTS.md` first for the rules.

## 1. Where things are

| Thing | Address |
|---|---|
| Live site | https://amianytime.com (EN) · https://amianytime.com/es/ (ES) — 8 pages each |
| Repo (source of truth) | github.com/Afoodsinc/amieveryday-site — branch `main`, root, public. Repo name is legacy; the domain is amianytime.com. Owner org: `Afoodsinc` (American Foods-owned; Frank's GitHub). |
| Hosting | GitHub Pages, custom domain via the `CNAME` file, Enforce HTTPS ON, certificate issued. Cache header `max-age=600`. No HSTS/CSP (GitHub Pages limitation; Cloudflare free tier would add them — owner decision). |
| DNS (GoDaddy, Frank's account) | amianytime.com: A @ → 185.199.108/109/110/111.153, CNAME www → afoodsinc.github.io. 11 other domains 301-forward to https://amianytime.com: amieveryday.com, amianytime.co, ami-brands.com, amilabel.com, theamibrand.com, theamibrands.net/.info/.shop/.store/.xyz, theamistore.com. Every GoDaddy save needs Frank's SMS code. **Do not touch.** |
| Backlog | `docs/reviews/cto-review.md` and `docs/reviews/ux-review.md` (ranked, with evidence and paste-ready copy). Current benchmark direction: `docs/reviews/benchmark-refresh-2026-09-09.md`. |
| Source art (designer packshots) | `/Users/Frank/Downloads/AMI Catalogue English.pdf` (17-page catalogue downloaded 2026-09-11) is the current web-art source. Its approved embedded product art, transparent ami lockups and lifestyle scenes have been extracted into `img/`. The older Dropbox website-source deck remains historical reference only. |
| AI lifestyle renders | Dropbox: `…/06 Brand & Marketing/_web-lifestyle-renders/` (Higgsfield nano-banana-pro; `gen-*.webp`, `recipe-*.webp`) |
| SKU list | Dropbox: `Frank Claude AI/Knowledge/source-files/AMI_Own_Brand_Program_149_SKUs.xlsx` (the 149-product program). ⚠️ It disagrees with the deck (see §4). |
| Project record (decisions, history) | Dropbox: `Frank Claude AI/Projects/ami-website.md` |
| Company contact facts used on the site | 2300 NW 92nd Ave, Doral, FL 33172 · PH Plaza del Este, Torre A, Piso 13, Costa del Este, Panamá · +1 877 894 7675 · +507 310 7576 · Sales@Afoodsinc.com (confirmed by Frank for current website inquiries) |

## 2. What is built (2026-09-09 redesign)
- 16 bilingual pages: Home, Products, tomato-paste detail, Recipes (6), Our brand, Where to buy, For partners, and Contact.
- Shopper-first flow: product-led Home → searchable food portfolio → product/recipe → honest availability roadmap. The multi-category platform is presented at brand scale without overstating current catalogue or retail availability.
- Partner flow is separate and executive-ready: global private-label context → retailer/distributor role choice → distinct value stories → depth-before-breadth operating model → American Foods credibility → inquiry.
- Where to buy now uses a local, privacy-safe Americas map and 18 accessible, clickable market cards covering every Central American country plus priority North American and Caribbean markets. Applications are open, qualified partners are described as under review, and every future partner and verified store profile has a defined home.
- Home and Products use a centered 3×2 composition built from six current packshots. Fixed public product-count claims have been removed; every catalogue card has an accessible quick view with the pack size in its accessible name.
- Recipes now opens with a food-led visual story, all recipe imagery uses controlled proportions, the copy and structured data agree, and Garlic-soy mushrooms has a prepared-dish image instead of a raw packshot.
- The partner page tells the 15-year global private-label story with sourced NIQ, PLMA, Circana, and FMI evidence: private label's share of global CPG spending grew from 15% in 2009 to 22% in 2024; 2025 European and U.S. sales data and 2026 shopper evidence provide the current executive proof points.
- Homepage and Our Brand now tell the ami origin, international everyday-value ambition, disciplined market-by-market growth model, and American Foods ownership story.
- `ami anytime™` is used consistently as the trademark treatment; `®` is prohibited until registration is confirmed.
- The obsolete `gen-basket`, `gen-aisle`, and `gen-shopper` art is no longer referenced. Exact individual packshots are used for catalogue truth; current-art lifestyle images are limited to supporting story and recipe moments.
- Empty map, newsletter capture, fake forms, placeholder legal links, unverified availability, commercial terms, guarantees, and superlative price/quality claims were removed.
- Product search and aisle filters work in English and Spanish. Mobile navigation closes on link selection, Escape, and desktop resize. Content remains visible if JavaScript fails.
- Shared source: `site.css`, `site.js`, and stdlib-only `tools/build_site.py`. Structural QA is automated in `tools/check_site.py`; publish output remains flat static HTML.

## 3. How the site is produced
`tools/build_site.py` is the maintained bilingual source and regenerates all 16 pages plus the 404 page with Python 3.9 standard-library code. The generated HTML is committed, so GitHub Pages still publishes directly without a build service. `tools/legacy/` is historical reference only and must not be used to publish.

## 4. Open decisions (Frank / Fredy — do not decide for them)
1. **Forms backend.** Public calls to action use directed `mailto:` links. A real form requires an approved destination, owner, privacy/consent copy, and success state.
2. **Legal pages.** No placeholder legal links are exposed. Privacy/terms pages still require owner/legal approval before publication.
3. **Retail availability.** The site publishes roadmap markets but no retailer or store availability. Add names, locations, partner ownership, or launch status only after confirmation and display approval.
4. **Commercial terms.** Exclusivity, price protection, licensing, sourcing, registrations, certifications, mixed containers, and response-time promises remain owner/legal gated and are not public claims.

## 5. Backlog that needs no decision (ranked, from the reviews)
- [x] Branded 404 page (`404.html` at root; GitHub Pages serves it).
- [x] ES catalogue: translate the 149 program names on `/es/products.html`.
- [x] Recipes: rewrite all six around the current food portfolio.
- [x] Add two-size `srcset` delivery for large lifestyle photos; keep Google Fonts with preconnect for now.
- [x] Make the canned-goods filters work and remove the fake sort.
- [x] Add an in-page aisle jump menu for tablet and phone.
- [x] Give every wordmark the accessible name "ami anytime".
- [ ] Analytics (Plausible or GoatCounter, cookieless), UptimeRobot, Google Search Console — Frank opens accounts.
- [x] Consolidate ad-hoc font sizes into the eight-step type scale.

## 6. Scores to beat (2026-09-09)
UX 6/10. Benchmark /30: Aldi 20 · Trader Joe's 20 · Essential Everyday 18 · Great Value 17 · **ami 17** (wins bilingual 4/5 and B2B path 4/5; loses product browse 2/5 and where-to-buy 1/5). Technical: lighter than all benchmarks; gaps were structured data, forms, legal pages, HSTS/CSP.

## 7. People
Frank Stanzione (CEO, owner, non-technical — wants numbers and decisions, not options) · Jorge (American Foods IT: DNS, mailboxes, accounts) · Fredy (AMI brand decisions) · Anyela (marketing execution) · Jhonathan (designer; source of all packshots).

## Change log
- 2026-09-03 — site v1 published (EN/ES, 16 pages), domain amianytime.com bound, HTTPS enforced, 11 domains forwarded.
- 2026-09-09 — new deck art (29-item launch range, real packshots site-wide, new lineup/lifestyle) · CTO + UX reviews · same-day fixes (see §2) · this handoff.
- 2026-09-09 — added a branded bilingual 404 page with clear EN/ES routes back to Home and Products.
- 2026-09-09 — translated all 149 full-program product names on the Spanish catalogue and normalized launch terminology to neutral Latin American Spanish.
- 2026-09-09 — rewrote all six recipes in English and Spanish around the 29 launch products, corrected metric pack sizes, and removed non-launch ami ingredient claims.
- 2026-09-09 — added responsive two-size WebP delivery for large lifestyle, recipe, banner, and lineup images across both languages, including responsive preloads.
- 2026-09-09 — made the canned-goods filters keyboard-accessible and functional in English and Spanish, added live result counts, and removed the fake one-option sort.
- 2026-09-09 — added a localized, horizontally scrollable aisle jump menu for tablet and phone catalog browsing while preserving the desktop aisle rail.
- 2026-09-09 — gave every header and footer wordmark the accessible name “ami anytime” while keeping the stylized dotless mark visual-only.
- 2026-09-09 — consolidated the site into an eight-step responsive type scale and corrected stale heading selectors so the real H1s render at the intended hierarchy.
- 2026-09-09 — applied a benchmark-led “modern pantry” visual refinement and added distinct shopper and retailer pathways on both homepages without changing the gated hero copy.
- 2026-09-09 — added real bilingual catalogue search by name, category and size; wired every header search icon to it; preserved the existing canned filters.
- 2026-09-09 — replaced unsupported About and return-guarantee language with evidence-safe brand facts and product-support instructions in English and Spanish.
- 2026-09-09 — made the language switch and active navigation explicit to assistive technology and added Escape-to-close mobile navigation behavior.
- 2026-09-09 — connected the tomato-paste detail page to its real recipe and removed false PDP tabs, dead social links and placeholder legal links as clickable controls.
- 2026-09-09 — recorded the official food-brand benchmark, adopted patterns, exclusions and acceptance standard in `docs/reviews/benchmark-refresh-2026-09-09.md`.
- 2026-09-09 — completed a full top-standard redesign with commercial/brand, bilingual-content, and technical-QA agent reviews; rebuilt the shopper and retailer flows, removed obsolete AI packaging art and unverified experiences, and consolidated all pages into one deterministic bilingual source.
- 2026-09-09 — optically centered the homepage product stage by removing the decorative tilt and centering both the white panel and product lineup across desktop and mobile layouts.
- 2026-09-09 — expanded the site for CEO, investor, retailer, and distributor conversations: added the global private-label growth story with NIQ evidence, separate retailer and distributor propositions, a local interactive Americas roadmap with 11 target markets, the fuller ami ambition and brand story, American Foods ownership and operating credibility, corrected American Foods organization links/schema, and trademark treatment in English and Spanish.
- 2026-09-11 — adopted the current catalogue art, added pasta and Bolognese products, standardized the exact transparent ami anytime lockup and browser icon, removed fixed product counts and the fifth contact route, changed inquiries to Sales@Afoodsinc.com, corrected bilingual trademark/company/contact copy, confirmed tuna at 140 g, and added a current representative social card.
- 2026-09-11 — removed “first range,” “focused start,” and related small-or-new brand language across English and Spanish; repositioned Home, Products, Our Brand, Partners, Recipes, and Where to Buy around the established ami food portfolio and scalable multi-category platform.
- 2026-09-09 — completed the CEO/CTO final pass: replaced the single-year private-label statistic with a sourced 15-year global movement, rebuilt Products and Recipes as image-led interactive experiences, expanded the partnership map to 18 markets including all of Central America and major Caribbean islands, made market cards and filters interactive, and added partner-application and future-profile states throughout.
- 2026-09-09 — completed a second commercial, bilingual, and technical release gate: removed the distorted/stale lineup from Home and Products, rebuilt both product stages with exact current packshots, corrected all responsive image geometry, placed map pins on a true-ratio canvas, updated partner evidence through 2026, strengthened first-screen CTAs and measurable ambition language, aligned all six recipes and schema, added a prepared mushroom dish image, and preserved selected product/market context through Contact.
