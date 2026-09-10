#!/usr/bin/env python3
"""Deterministic structural checks for the committed static site."""
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = ["index.html", "products.html", "product-tomato-paste.html", "recipes.html", "about.html", "where-to-buy.html", "partners.html", "contact.html"]

class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.h1=0; self.lang=""; self.refs=[]; self.images=[]; self.json_blocks=[]; self._json=False; self._buffer=[]; self.canonical=0; self.hreflangs=set()
    def handle_starttag(self, tag, attrs):
        data=dict(attrs)
        if tag=="html": self.lang=data.get("lang","")
        if tag=="h1": self.h1+=1
        if tag in {"a","link","script","img","source"}:
            for key in ("href","src","srcset"):
                if data.get(key): self.refs.append(data[key].split()[0])
        if tag=="img": self.images.append(data)
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
    assert "https://americanfoods.com" not in text, f"{page}: incorrect AFI organization URL"
    assert "®" not in text, f"{page}: registered mark used without registration approval"
    assert "site-refresh.css" not in text, f"{page}: legacy stylesheet"
    assert "gen-basket" not in text and "gen-shopper" not in text and "gen-aisle" not in text, f"{page}: obsolete art"
    for block in parser.json_blocks: json.loads(block)
    for image in parser.images:
        assert image.get("width") and image.get("height"), f"{page}: image missing dimensions: {image.get('src')}"
    for ref in parser.refs:
        target=local_target(page,ref)
        if target is not None: assert target.exists(), f"{page}: broken local reference {ref}"
    if page.name=="where-to-buy.html":
        marker_ids=[part.split('"',1)[0] for part in text.split('data-market="')[1:]]
        card_ids=[part.split('"',1)[0] for part in text.split('data-market-card="')[1:]]
        assert len(marker_ids)==11 and len(card_ids)==11, f"{page}: expected 11 market markers and cards"
        assert len(set(marker_ids))==11 and set(marker_ids)==set(card_ids), f"{page}: market IDs must be unique and paired"
        assert "cartocdn" not in text and "leaflet" not in text.lower(), f"{page}: map must not make third-party tile requests"
    if page.name=="partners.html":
        assert 'id="retailers"' in text and 'id="distributors"' in text, f"{page}: missing partner audience journey"

def main():
    pages=[ROOT/name for name in PAGES]+[ROOT/"es"/name for name in PAGES]
    for page in pages: check(page)
    assert (ROOT/"CNAME").read_text(encoding="utf-8").strip()=="amianytime.com"
    for required in ("america-map.svg","afi-logo-white.png","afi-logo-navy.png"):
        assert (ROOT/"img"/required).exists(), f"missing required brand asset: {required}"
    assert len(list(ROOT.glob("*.html")))==9
    print(f"OK: {len(pages)} bilingual pages, local references, metadata, images, and JSON-LD")

if __name__=="__main__": main()
