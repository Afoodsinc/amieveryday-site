#!/usr/bin/env python3
"""Deterministic structural checks for the committed static site."""
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

from build_site import PRODUCTS

ROOT = Path(__file__).resolve().parents[1]
PAGES = ["index.html", "products.html", "product-tomato-paste.html", "recipes.html", "about.html", "where-to-buy.html", "partners.html", "contact.html"]

class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.h1=0; self.lang=""; self.refs=[]; self.images=[]; self.videos=[]; self.cinema_sources=[]; self.cinema_toggles=[]; self.films=[]; self.json_blocks=[]; self._json=False; self._buffer=[]; self.canonical=0; self.hreflangs=set()
    def handle_starttag(self, tag, attrs):
        data=dict(attrs)
        if tag=="html": self.lang=data.get("lang","")
        if tag=="h1": self.h1+=1
        if tag in {"a","link","script","img","source","video"}:
            for key in ("href","src","srcset","data-src","poster"):
                if data.get(key): self.refs.append(data[key].split()[0])
        if tag=="img": self.images.append(data)
        if tag=="video": self.videos.append(data)
        if tag=="source" and data.get("data-src"): self.cinema_sources.append(data)
        if tag=="button" and "data-cinema-toggle" in data: self.cinema_toggles.append(data)
        if tag=="section" and data.get("data-film"): self.films.append(data)
        if tag=="link" and data.get("rel")=="canonical": self.canonical+=1
        if tag=="link" and data.get("rel")=="alternate" and data.get("hreflang"): self.hreflangs.add(data["hreflang"])
        if tag=="script" and data.get("type")=="application/ld+json": self._json=True; self._buffer=[]
    def handle_data(self,data):
        if self._json: self._buffer.append(data)
    def handle_endtag(self,tag):
        if tag=="script" and self._json: self.json_blocks.append("".join(self._buffer)); self._json=False

def local_target(page: Path, ref: str):
    parsed=urlsplit(ref)
    if parsed.scheme or ref.startswith("//") or ref.startswith("#"): return None
    target=(page.parent/parsed.path).resolve()
    if parsed.path.endswith("/"): target/= "index.html"
    return target

def check(page: Path):
    text=page.read_text(encoding="utf-8"); parser=AuditParser(); parser.feed(text)
    expected="es" if page.parent.name=="es" else "en"
    assert parser.lang==expected, f"{page}: expected lang {expected}"
    assert parser.h1==1, f"{page}: expected one h1, got {parser.h1}"
    assert parser.canonical==1, f"{page}: expected one canonical"
    assert {"en","es","x-default"} <= parser.hreflangs, f"{page}: incomplete hreflang"
    assert 'href="#"' not in text, f"{page}: placeholder link"
    assert "https://americanfoods.com" not in text, f"{page}: incorrect American Foods organization URL"
    assert "americanfoodsllc.com" not in text.lower(), f"{page}: obsolete American Foods organization URL"
    assert "widely available" not in text.lower() and "amplia disponibilidad" not in text.lower(), f"{page}: unsupported availability claim"
    assert "essential" not in text.lower() and "esencial" not in text.lower(), f"{page}: competitor-adjacent essential language remains"
    assert "®" not in text, f"{page}: registered mark used without registration approval"
    assert "no launch announced" not in text.lower() and "lanzamiento no anunciado" not in text.lower(), f"{page}: stale no-launch language"
    assert "site-refresh.css" not in text, f"{page}: legacy stylesheet"
    assert "gen-basket" not in text and "gen-shopper" not in text and "gen-aisle" not in text, f"{page}: obsolete art"
    assert "img/new-lockup.webp" not in text, f"{page}: obsolete opaque ami logo"
    assert "favicon.svg" not in text, f"{page}: obsolete favicon"
    assert "lineup.webp" not in text, f"{page}: stale social image"
    assert "range-seal" not in text, f"{page}: obsolete product-count seal"
    assert "numberOfItems" not in text and '"position"' not in text, f"{page}: public product counts remain in schema"
    assert "29 products" not in text and "29 productos" not in text, f"{page}: public fixed catalogue count remains"
    assert "170 g" not in text, f"{page}: stale tuna weight"
    for phrase in ("first ami", "first range", "primer surtido", "focused range", "surtido enfocado", "focused start", "inicio enfocado", "next chapter", "próximo capítulo"):
        assert phrase not in text.lower(), f"{page}: small-or-new brand language remains: {phrase}"
    assert " AFI " not in text, f"{page}: public American Foods abbreviation remains"
    assert "info@afoodsinc.com" not in text.lower(), f"{page}: old contact mailbox"
    assert "trademark applications" not in text.lower() and "solicitudes de registro" not in text.lower(), f"{page}: stale pending-trademark wording"
    assert "site.css?v=20260920-2" in text, f"{page}: stale shared CSS version"
    assert "site.js?v=20260920-2" in text, f"{page}: stale shared JavaScript version"
    assert "img/ami-social-card.webp" in text, f"{page}: missing current social image"
    expected_social_alt = "ami anytime everyday product range" if expected == "en" else "Gama de productos cotidianos ami anytime"
    assert text.count(f'<meta property="og:image:alt" content="{expected_social_alt}">') == 1, f"{page}: incorrect Open Graph image alt"
    assert text.count(f'<meta name="twitter:image:alt" content="{expected_social_alt}">') == 1, f"{page}: incorrect Twitter image alt"
    assert "img/ami-logo-navy.png" in text, f"{page}: missing canonical ami header logo"
    assert "img/ami-logo-white.png" in text, f"{page}: missing canonical ami footer logo"
    expected_film={
        "index.html":"table", "products.html":"ingredients", "product-tomato-paste.html":"product",
        "recipes.html":"kitchen", "about.html":"about", "where-to-buy.html":"markets",
        "partners.html":"partners", "contact.html":"contact",
    }[page.name]
    assert len(parser.films)==1 and parser.films[0].get("data-film")==expected_film, f"{page}: missing or incorrect cinematic module"
    assert len(parser.videos)==1, f"{page}: expected exactly one cinematic video"
    video=parser.videos[0]
    for attr in ("muted","loop","playsinline"):
        assert attr in video, f"{page}: cinematic video missing {attr}"
    assert video.get("preload")=="none", f"{page}: cinematic video must use preload=none"
    assert video.get("width")=="1280" and video.get("height")=="720", f"{page}: cinematic video missing stable dimensions"
    assert video.get("poster"), f"{page}: cinematic video missing poster"
    assert "autoplay" not in video, f"{page}: raw video autoplay is not allowed"
    assert len(parser.cinema_sources)==2, f"{page}: expected mobile and desktop film sources"
    assert len(parser.cinema_toggles)==1, f"{page}: expected one accessible play/pause control"
    toggle=parser.cinema_toggles[0]
    assert toggle.get("data-play-label") and toggle.get("data-pause-label"), f"{page}: film control labels missing"
    assert toggle.get("aria-pressed")=="false", f"{page}: film control initial state incorrect"
    marks=[image for image in parser.images if "brand-film__mark" in image.get("class","").split()]
    assert len(marks)==1 and marks[0].get("src","").endswith("img/ami-logo-white.png"), f"{page}: exact ami film logo missing"
    for block in parser.json_blocks: json.loads(block)
    for image in parser.images:
        assert image.get("width") and image.get("height"), f"{page}: image missing dimensions: {image.get('src')}"
    for ref in parser.refs:
        target=local_target(page,ref)
        if target is not None: assert target.exists(), f"{page}: broken local reference {ref}"
    if page.name=="where-to-buy.html":
        marker_ids=[part.split('"',1)[0] for part in text.split('data-market="')[1:]]
        card_ids=[part.split('"',1)[0] for part in text.split('data-market-card="')[1:]]
        assert len(marker_ids)==18 and len(card_ids)==18, f"{page}: expected 18 market markers and cards"
        assert len(set(marker_ids))==18 and set(marker_ids)==set(card_ids), f"{page}: market IDs must be unique and paired"
        assert "cartocdn" not in text and "leaflet" not in text.lower(), f"{page}: map must not make third-party tile requests"
        assert text.count('data-market-filter=')==4, f"{page}: expected four market filters"
        assert "Partner applications open" in text or "Postulaciones de socios abiertas" in text, f"{page}: missing partnership status"
        expected_market_label="Markets" if expected=="en" else "Mercados"
        expected_retail_state="No verified retail locations have been published yet." if expected=="en" else "Todavía no se han publicado puntos de venta verificados."
        assert f"<title>{expected_market_label} | ami anytime</title>" in text, f"{page}: incorrect market page label"
        assert expected_retail_state in text, f"{page}: missing explicit unpublished retail-location state"
        assert 'id="partner-opportunities"' in text, f"{page}: shopper and partner market states are not separated"
        assert (
            ('href="products.html"' in text and 'href="recipes.html"' in text)
            or ('href="../products.html"' in text and 'href="../recipes.html"' in text)
        ), f"{page}: missing shopper paths"
        assert "Sales@Afoodsinc.com" in text and (
            "opens your email application" in text or "abre tu aplicación de correo" in text
        ), f"{page}: missing availability email fallback or disclosure"
    if page.name=="partners.html":
        assert 'id="retailers"' in text and 'id="distributors"' in text, f"{page}: missing partner audience journey"
        assert "2009" in text and "2024" in text and "world-map.png" in text, f"{page}: missing long-term global evidence"
    if page.name=="products.html":
        assert text.count("data-quick-product") == len(PRODUCTS), f"{page}: every product must open a quick view"
        assert 'id="product-dialog"' in text, f"{page}: missing product quick view"
        assert 'data-filter="pasta"' in text, f"{page}: missing pasta filter"
        assert "data-template-en" not in text, f"{page}: numeric result-count template remains"
        assert all(product[1 if expected=="en" else 2] in text for product in PRODUCTS), f"{page}: incomplete product range"
        assert text.count("140 g") >= 3, f"{page}: tuna products must use the owner-confirmed 140 g size"
    if page.name=="contact.html":
        assert text.count("mailto:Sales@Afoodsinc.com?subject=") == 4, f"{page}: expected four approved inquiry routes"
        assert text.count("mailto:Sales@Afoodsinc.com") == 5, f"{page}: expected four inquiry routes plus readable email fallback"
        assert "Sales@Afoodsinc.com" in text and ("opens your email application" in text or "abre tu aplicación de correo" in text), f"{page}: missing email-app disclosure"
        assert "media-other" not in text and "Media or other" not in text and "Prensa u otra" not in text, f"{page}: obsolete fifth route"
        expected_heading="To route your inquiry" if expected=="en" else "Para dirigir tu consulta"
        assert expected_heading in text, f"{page}: incorrect contact heading"

def main():
    pages=[ROOT/name for name in PAGES]+[ROOT/"es"/name for name in PAGES]
    for page in pages: check(page)
    error_page=(ROOT/"404.html").read_text(encoding="utf-8").lower()
    assert "essential" not in error_page and "esencial" not in error_page, "404.html: competitor-adjacent essential language remains"
    assert "site.css?v=20260920-2" in error_page, "404.html: stale shared CSS version"
    css=(ROOT/"site.css").read_text(encoding="utf-8")
    focus_treatment=""":focus-visible {
  outline: 3px solid #fff;
  outline-offset: 2px;
  box-shadow: 0 0 0 6px var(--navy) !important;
}"""
    forced_colors="""@media (forced-colors: active) {
  :focus-visible { outline-color: CanvasText; box-shadow: none !important; }
}"""
    assert focus_treatment in css, "global focus treatment must retain white and navy contrast rings"
    assert forced_colors in css, "global focus treatment must retain forced-colors support"
    assert (ROOT/"CNAME").read_text(encoding="utf-8").strip()=="amianytime.com"
    for required in ("america-map.svg","world-map.png","afi-logo-white.png","afi-logo-navy.png","ami-logo-navy.png","ami-logo-white.png","ami-social-card.webp"):
        assert (ROOT/"img"/required).exists(), f"missing required brand asset: {required}"
    film_keys=("table","ingredients","product","kitchen","about","markets","partners","contact")
    media=[]
    for key in film_keys:
        poster=ROOT/"img"/f"film-{key}-poster.webp"
        desktop=ROOT/"video"/"website"/f"ami-{key}-desktop.mp4"
        mobile=ROOT/"video"/"website"/f"ami-{key}-mobile.mp4"
        assert poster.exists() and poster.stat().st_size <= 180*1024, f"{poster}: missing or over 180 KB"
        assert desktop.exists() and desktop.stat().st_size <= 2500*1024, f"{desktop}: missing or over 2.5 MB"
        assert mobile.exists() and mobile.stat().st_size <= 1200*1024, f"{mobile}: missing or over 1.2 MB"
        media.extend((poster,desktop,mobile))
    assert sum(path.stat().st_size for path in media) <= 30*1024*1024, "website film package exceeds 30 MB"
    for name in PAGES:
        en=AuditParser(); en.feed((ROOT/name).read_text(encoding="utf-8"))
        es=AuditParser(); es.feed((ROOT/"es"/name).read_text(encoding="utf-8"))
        en_sources=[Path(source["data-src"]).name for source in en.cinema_sources]
        es_sources=[Path(source["data-src"]).name for source in es.cinema_sources]
        assert en_sources==es_sources, f"{name}: English and Spanish must share the same approved films"
    en_film_keys=[]
    for name in PAGES:
        parser=AuditParser(); parser.feed((ROOT/name).read_text(encoding="utf-8"))
        en_film_keys.append(parser.films[0]["data-film"])
    assert len(set(en_film_keys))==len(PAGES), "every English page type must have a distinct approved film"
    product_page=(ROOT/"product-tomato-paste.html").read_text(encoding="utf-8")
    assert 'class="brand-film__product"' in product_page and 'src="img/tomato-paste.webp"' in product_page, "product film must preserve the exact packshot as an HTML overlay"
    assert (ROOT/"favicon.png").exists(), "missing canonical browser icon"
    assert len(list(ROOT.glob("*.html")))==9
    print(f"OK: {len(pages)} bilingual pages, local references, metadata, images, and JSON-LD")

if __name__=="__main__": main()
