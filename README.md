# amianytime.com — ami anytime brand website

Static bilingual site (HTML/CSS/JS, no publish-time build step). Published with GitHub Pages; custom domain via `CNAME`.

Owner: American Foods International Inc. Content and artwork © American Foods International Inc.

Eight English pages live at the root and eight Spanish twins live in `es/`. Images are in `img/` (WebP), the shared visual system is `site.css`, and `tools/build_site.py` regenerates every committed page.

The site includes a bilingual retailer/distributor story, an 18-market privacy-safe Americas partnership explorer, interactive product quick views, a food-led recipe experience, the ami brand ambition, an American Foods ownership section, and consistent trademark treatment. The roadmap SVG is the public-domain `America map.svg` by xZise from Wikimedia Commons. The global private-label section uses the CC0 `Blank world map.svg` by Nitesh003 from Wikimedia Commons, delivered as an optimized local PNG. The American Foods marks come from the approved 2026 Retail Partner Presentation source deck; current ami product art and lockups come from the September 11, 2026 catalogue.

Local checks:

```sh
python3 tools/build_site.py
python3 tools/check_site.py
```
