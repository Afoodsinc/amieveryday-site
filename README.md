# amianytime.com — ami anytime brand website

Static bilingual site (HTML/CSS/JS, no publish-time build step). Published with GitHub Pages; custom domain via `CNAME`.

Owner: American Foods International Inc. Content and artwork © American Foods International Inc.

Eight English pages live at the root and eight Spanish twins live in `es/`. Images are in `img/` (WebP), the shared visual system is `site.css`, and `tools/build_site.py` regenerates every committed page.

The site now includes a bilingual retailer/distributor story, a privacy-safe local Americas roadmap, the ami brand ambition, an American Foods ownership section, and restrained `™` treatment for the pending trademark. The roadmap SVG is the public-domain `America map.svg` by xZise from Wikimedia Commons; the American Foods marks come from the approved 2026 Retail Partner Presentation source deck.

Local checks:

```sh
python3 tools/build_site.py
python3 tools/check_site.py
```
