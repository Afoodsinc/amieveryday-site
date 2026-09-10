# amianytime.com — ami anytime brand website

Static bilingual site (HTML/CSS/JS, no publish-time build step). Published with GitHub Pages; custom domain via `CNAME`.

Owner: American Foods International Inc. Content and artwork © American Foods International Inc.

Eight English pages live at the root and eight Spanish twins live in `es/`. Images are in `img/` (WebP), the shared visual system is `site.css`, and `tools/build_site.py` regenerates every committed page.

Local checks:

```sh
python3 tools/build_site.py
python3 tools/check_site.py
```
