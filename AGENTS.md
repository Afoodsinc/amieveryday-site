# AGENTS.md — ami anytime website (amianytime.com)

Instructions for any coding agent (Codex, Claude, human) working in this repo. Read `HANDOFF.md` next for the full state of the project.

## What this is
The consumer + retail-partner website of **ami anytime**, the own-brand grocery program of American Foods International (AFI, Miami / Panamá). Static HTML/CSS, bilingual (EN at `/`, ES at `/es/`), hosted on **GitHub Pages** from branch `main`, root folder. Live: https://amianytime.com · https://amianytime.com/es/

## Hard rules
1. **Static site only.** No build step is required to publish: whatever is in `main` is live within ~1 minute. If you add a generator, its output must be committed flat HTML in this layout (see "Layout").
2. **Never delete or change `CNAME`** (`amianytime.com`). It binds the custom domain. Removing it drops HTTPS and the domain.
3. **Every page exists twice** (EN + ES). Any content change ships in both languages, with `hreflang` + `canonical` kept in sync. Spanish is LatAm-neutral (no Spain-only forms).
4. **Brand name is lowercase**: `ami`, `ami anytime`. Tagline: "always with you" / "siempre contigo".
5. **Pricing doctrine**: never quote or compare against US national-brand prices on the site. Claims must be supportable ("lowest price" needs a qualifier or gets removed; that is a brand decision for Frank/Fredy, not the agent).
6. **Do not touch** DNS, GoDaddy, GitHub Pages settings, or any domain. `frankstanzione.com` is personal and unrelated. These require the owner (Frank) with SMS codes.
7. **No credentials in the repo**, no third-party scripts beyond the current allow-list (Google Fonts, cdnjs Leaflet with SRI, CARTO tiles). Adding a form backend or analytics: propose the vendor + exact snippet; Frank opens the account.
8. **Keep the original design.** Frank explicitly asked to keep the existing look (navy/green, aisle colour system, card layouts). Improve within it; do not redesign without a request.
9. **Images**: real packshots first (in `img/`, sourced from the designer's deck). Never reuse a packshot for a different product. AI lifestyle renders (`gen-*.webp`) are placeholders until real photography exists.
10. Commit messages: plain English, one line, what changed and why. Always `git pull --rebase origin main` before pushing (GitHub sometimes commits `CNAME` from the settings UI).

## Layout
```
/                 EN pages: index.html about.html products.html product-tomato-paste.html recipes.html where-to-buy.html partners.html contact.html
/es/              ES twins, same filenames
/img/             WebP assets (packshots new-*.webp, lifestyle new-life-*.webp, AI renders gen-*.webp, recipes recipe-*.webp, lineup.webp, new-lockup.webp, new-tagline.webp, new-badge-bestseller.webp)
CNAME robots.txt sitemap.xml favicon.svg .nojekyll
docs/reviews/     CTO + UX review reports (2026-09-09) — the ranked backlog
tools/legacy/     the ORIGINAL Python generator + CSS template (superseded; later patches were lost). Reference only.
```
CSS lives inline in each page's `<style>` (identical across pages). Design tokens: navy `#253768`, navy-deep `#1B2A52`, green `#8FB944`, green-ink `#4E7A1F`, ink `#1C2430`, ink-3 `#66707D`; aisle colours veg `#5E9C3B`, tomato `#D8352C`, fruit `#F28C00`, corn `#F2B705`, sea `#2C7FB8`, dairy `#E9D9B5`, pantry `#C98A3B`, house `#7C8FA6`, care `#C77BA6`, frozen `#6FB8D8`. Fonts: Nunito 700–900 (display), DM Sans 400–700 (body), via Google Fonts.

## Definition of done for any change
- Both languages updated; every `img/` reference resolves; images carry `width`/`height`, below-fold ones `loading="lazy"`.
- One `<h1>` per page; JSON-LD still valid (`python3 -c` json.loads over every `ld+json` block).
- `curl -I https://amianytime.com/<page>` returns 200 after push; no horizontal scroll at 360 px.
- Note the change in `HANDOFF.md` → "Change log".
