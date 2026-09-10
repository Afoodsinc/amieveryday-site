#!/usr/bin/env python3
"""Build the static ami anytime website from one bilingual source."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://amianytime.com"
SEARCH = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"></circle><path d="m20 20-4-4"></path></svg>'
ARROW = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'
MENU = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"></path></svg>'

PRODUCTS = [
    ("new-drink-orange-200.webp", "Orange Fruit Drink", "Bebida de naranja", "200 ml", "drinks"),
    ("new-drink-mango-200.webp", "Mango Fruit Drink", "Bebida de mango", "200 ml", "drinks"),
    ("new-drink-tropical-200.webp", "Tropical Fruit Drink", "Bebida tropical", "200 ml", "drinks"),
    ("new-drink-apple-200.webp", "Apple Fruit Drink", "Bebida de manzana", "200 ml", "drinks"),
    ("new-drink-orange-1l.webp", "Orange Fruit Drink", "Bebida de naranja", "1 L", "drinks"),
    ("new-drink-mango-1l.webp", "Mango Fruit Drink", "Bebida de mango", "1 L", "drinks"),
    ("new-drink-pineapple-1l.webp", "Pineapple Fruit Drink", "Bebida de piña", "1 L", "drinks"),
    ("new-drink-apple-1l.webp", "Apple Fruit Drink", "Bebida de manzana", "1 L", "drinks"),
    ("new-drink-tropical-1l.webp", "Tropical Fruit Drink", "Bebida tropical", "1 L", "drinks"),
    ("new-whole-peeled-tomatoes.webp", "Whole Peeled Tomatoes", "Tomates enteros pelados", "400 g", "tomato"),
    ("new-chopped-tomatoes.webp", "Chopped Tomatoes", "Tomates picados", "400 g", "tomato"),
    ("tomato-paste.webp", "Tomato Paste", "Pasta de tomate", "400 g", "tomato"),
    ("new-ketchup.webp", "Tomato Ketchup", "Kétchup de tomate", "340 g", "tomato"),
    ("new-mix-veg.webp", "Mixed Vegetables", "Vegetales mixtos", "400 g", "veg"),
    ("new-sweet-corn.webp", "Sweet Corn", "Maíz dulce", "340 g", "veg"),
    ("baby-corn.webp", "Baby Corn", "Maíz baby", "425 g", "veg"),
    ("mushrooms-whole.webp", "Whole Button Mushrooms", "Champiñones enteros", "284 g", "veg"),
    ("mushrooms-sliced.webp", "Sliced Mushrooms", "Champiñones en láminas", "284 g", "veg"),
    ("new-pinto.webp", "Pinto Beans", "Frijoles pintos", "400 g", "beans"),
    ("new-black-beans.webp", "Black Beans", "Frijoles negros", "400 g", "beans"),
    ("new-red-kidney.webp", "Red Kidney Beans", "Frijoles rojos", "400 g", "beans"),
    ("new-tuna-flakes-oil.webp", "Tuna Flakes in Oil", "Atún desmenuzado en aceite", "140 g", "tuna"),
    ("new-tuna-chunks-water.webp", "Tuna Chunks in Water", "Atún en trozos en agua", "140 g", "tuna"),
    ("new-tuna-chunks-oil.webp", "Tuna Chunks in Oil", "Atún en trozos en aceite", "140 g", "tuna"),
    ("peach.webp", "Sliced Peaches in Syrup", "Duraznos en rebanadas en almíbar", "425 g", "pantry"),
    ("new-soy-light.webp", "Light Soy Sauce", "Salsa de soya clara", "500 ml", "pantry"),
    ("new-soy-dark.webp", "Dark Soy Sauce", "Salsa de soya oscura", "500 ml", "pantry"),
    ("new-noodles-chicken.webp", "Instant Noodles, Chicken", "Fideos instantáneos sabor pollo", "85 g", "pantry"),
    ("new-noodles-beef.webp", "Instant Noodles, Beef", "Fideos instantáneos sabor res", "85 g", "pantry"),
]
CATEGORIES = {
    "drinks": ("Fruit drinks", "Bebidas de fruta", "var(--fruit)"),
    "tomato": ("Tomato", "Tomate", "var(--tomato)"),
    "veg": ("Vegetables & corn", "Vegetales y maíz", "var(--corn)"),
    "beans": ("Beans", "Frijoles", "var(--beans)"),
    "tuna": ("Products of the sea", "Productos del mar", "var(--sea)"),
    "pantry": ("Pantry", "Despensa", "var(--pantry)"),
}
IMAGE_SIZES = {
    "recipe-arroz.webp": (1300, 872), "new-life-cooking.webp": (1163, 1237),
    "recipe-ensalada.webp": (1300, 872), "recipe-batido.webp": (1300, 872),
    "recipe-sopa.webp": (1300, 872), "mushrooms-whole.webp": (859, 859),
}

def page_path(slug, lang):
    file = "index.html" if slug == "home" else f"{slug}.html"
    return file if lang == "en" else f"es/{file}"

def href(slug, lang, fragment=""):
    return ("index.html" if slug == "home" else f"{slug}.html") + fragment

def asset(name, lang):
    return ("../" if lang == "es" else "") + name

def alternate(slug, lang):
    file = "index.html" if slug == "home" else f"{slug}.html"
    return f"es/{file}" if lang == "en" else f"../{file}"

def esc(value):
    return html.escape(value, quote=True)

def head(slug, lang, title, description, schema=None):
    en = f"{SITE}/{page_path(slug, 'en')}".replace("/index.html", "/")
    es = f"{SITE}/{page_path(slug, 'es')}".replace("/index.html", "/")
    current = en if lang == "en" else es
    structured = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    preload = f'<link rel="preload" as="image" href="{asset("img/lineup-800.webp",lang)}" media="(max-width:700px)"><link rel="preload" as="image" href="{asset("img/lineup.webp",lang)}" media="(min-width:701px)">' if slug=="home" else ""
    return f'''<!doctype html><html lang="{lang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}"><meta name="theme-color" content="#21366b">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{current}"><meta property="og:image" content="{SITE}/img/lineup.webp"><meta property="og:locale" content="{'en_US' if lang=='en' else 'es_419'}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{SITE}/img/lineup.webp">
<link rel="canonical" href="{current}"><link rel="alternate" hreflang="en" href="{en}"><link rel="alternate" hreflang="es" href="{es}"><link rel="alternate" hreflang="x-default" href="{en}">
<link rel="icon" href="{asset('favicon.svg', lang)}" type="image/svg+xml">{preload}<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<script>document.documentElement.classList.add("js")</script><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&amp;family=Nunito:wght@800;900&amp;display=swap" rel="stylesheet"><link rel="stylesheet" href="{asset('site.css', lang)}">{structured}</head>'''

def header(slug, lang):
    t = ({"products":"Products","recipes":"Recipes","where-to-buy":"Where to buy","about":"Our brand","partners":"For retailers","skip":"Skip to content","menu":"Open menu","search":"Search products","nav":"Main navigation"} if lang == "en" else {"products":"Productos","recipes":"Recetas","where-to-buy":"Dónde comprar","about":"Nuestra marca","partners":"Para supermercados","skip":"Saltar al contenido","menu":"Abrir menú","search":"Buscar productos","nav":"Navegación principal"})
    nav = "".join(f'<a href="{href(key,lang)}"'+(' aria-current="page"' if slug == key else '')+f'>{t[key]}</a>' for key in ("products","recipes","where-to-buy","about","partners"))
    en_link=href(slug,lang) if lang=="en" else alternate(slug,lang); es_link=alternate(slug,lang) if lang=="en" else href(slug,lang)
    return f'''<body><a class="skip-link" href="#main">{t['skip']}</a><header class="site-header"><div class="header-inner">
<a class="brand-mark" href="{href('home',lang)}" aria-label="ami anytime home"><img src="{asset('img/new-lockup.webp',lang)}" width="860" height="612" alt="ami anytime"></a>
<nav class="primary-nav" id="primary-nav" aria-label="{t['nav']}">{nav}</nav><div class="header-tools"><div class="language-switch" aria-label="Language"><a href="{en_link}"{' aria-current="page"' if lang=='en' else ''} lang="en">EN</a><a href="{es_link}"{' aria-current="page"' if lang=='es' else ''} lang="es">ES</a></div><a class="search-link" href="{href('products',lang)}#catalog" aria-label="{t['search']}">{SEARCH}</a><button class="menu-toggle" type="button" aria-controls="primary-nav" aria-expanded="false" aria-label="{t['menu']}">{MENU}</button></div></div></header>'''

def footer(lang):
    if lang == "en":
        line="Everyday products. One familiar brand. Always with you."
        cols=[("Explore",[("Products","products",""),("Recipes","recipes",""),("Where to buy","where-to-buy","")]),("About ami",[("Our brand","about",""),("For retailers","partners","")]),("Help",[("Product support","about","#product-support"),("Contact us","contact","")])]
        legal="Privacy and legal information available through American Foods International."
    else:
        line="Productos de todos los días. Una marca fácil de reconocer. Siempre contigo."
        cols=[("Explora",[("Productos","products",""),("Recetas","recipes",""),("Dónde comprar","where-to-buy","")]),("Sobre ami",[("Nuestra marca","about",""),("Para supermercados","partners","")]),("Ayuda",[("Ayuda con un producto","about","#product-support"),("Contáctanos","contact","")])]
        legal="Información legal y de privacidad disponible a través de American Foods International."
    blocks="".join(f'<div><h2>{heading}</h2><ul class="footer-links">'+"".join(f'<li><a href="{href(slug,lang,fragment)}">{label}</a></li>' for label,slug,fragment in items)+"</ul></div>" for heading,items in cols)
    return f'''<footer class="site-footer"><div class="footer-inner"><div class="footer-grid"><div class="footer-brand"><div class="footer-wordmark">ami<span>.</span></div><p>{line}</p></div>{blocks}</div><div class="footer-bottom"><span>© 2026 American Foods International</span><span>{legal}</span></div></div></footer><script src="{asset('site.js',lang)}" defer></script></body></html>'''

def product_card(product, lang, linked=False):
    image,en,es,size,category=product; name=en if lang=="en" else es; cat=CATEGORIES[category][0 if lang=="en" else 1]
    tag="a" if linked and en=="Tomato Paste" else "article"; link=f' href="{href("product-tomato-paste",lang)}"' if tag=="a" else ""
    return f'''<{tag} class="product-card"{link} data-product="{esc(en+' '+es+' '+size)}" data-category="{category}" style="--category:{CATEGORIES[category][2]}"><div class="product-visual"><img src="{asset('img/'+image,lang)}" width="900" height="900" alt="{esc('ami '+name+', '+size)}" loading="lazy"></div><div class="product-meta"><span class="product-category">{cat}</span><strong class="product-name">{name}</strong><span class="product-size">{size}</span></div></{tag}>'''

def recipe_card(image,name,time,uses,anchor,lang):
    prep="Prep" if lang=="en" else "Preparación"; serves="Serves 4" if lang=="en" else "Rinde 4 porciones"
    width,height=IMAGE_SIZES[image]
    return f'''<a class="recipe-card" href="{href('recipes',lang)}#{anchor}"><img src="{asset('img/'+image,lang)}" width="{width}" height="{height}" alt="{esc(name)}" loading="lazy"><div class="recipe-card-body"><span class="eyebrow">{prep}: {time}</span><h3>{name}</h3><div class="recipe-meta"><span>{serves}</span></div><div class="uses">{"".join(f'<span>{esc(x)}</span>' for x in uses)}</div></div></a>'''

def frame(slug,lang,title,description,main,schema=None):
    return "\n".join((head(slug,lang,title,description,schema),header(slug,lang),main,footer(lang)))

def organization(lang):
    return {"@context":"https://schema.org","@type":"Organization","name":"ami anytime","url":SITE+("/" if lang=="en" else "/es/"),"logo":f"{SITE}/img/new-lockup.webp","parentOrganization":{"@type":"Organization","name":"American Foods International","url":"https://americanfoods.com"}}

def build_home(lang):
    en=lang=="en"
    c={
      "eyebrow":"Everyday essentials" if en else "Productos esenciales para cada día",
      "h1":"Everyday food,<br><em>ready for real meals.</em>" if en else "Alimentos de todos los días,<br><em>para comidas de verdad.</em>",
      "lead":"From tomatoes and beans to tuna, corn, noodles and fruit drinks, ami brings familiar essentials together under one clear brand." if en else "De tomates y frijoles a atún, maíz, fideos y bebidas de fruta, ami reúne productos conocidos bajo una marca clara.",
      "products":"Browse products" if en else "Ver productos", "cook":"Cook with ami" if en else "Cocinar con ami",
      "stage":"The ami launch range" if en else "El surtido de lanzamiento ami",
      "proof":["Easy to recognize","Organized by aisle","English and Spanish"] if en else ["Fácil de reconocer","Organizado por pasillo","En español e inglés"],
      "findeyebrow":"Find your next staple" if en else "Encuentra tu próximo favorito", "findh":"What are you looking for?" if en else "¿Qué estás buscando?",
      "placeholder":"Try tomato, beans, tuna…" if en else "Prueba tomate, frijoles, atún…", "search":"Search" if en else "Buscar",
      "start":"Start with the essentials" if en else "Empieza por lo esencial", "startp":"Explore the launch range by category, pack size and flavor." if en else "Explora el surtido de lanzamiento por categoría, tamaño y sabor.",
      "all":"See the launch range" if en else "Ver el surtido de lanzamiento", "range":"Launch range" if en else "Surtido de lanzamiento",
      "featured":"Made for the pantry" if en else "Hechos para la despensa", "featuredp":"A focused range of familiar foods for meals, lunches and everyday moments." if en else "Un surtido enfocado de alimentos conocidos para comidas, almuerzos y momentos de todos los días.",
      "system":"One band. Easy to recognize." if en else "Una banda. Fácil de reconocer.", "systemp":"The navy ami band keeps the family together. Category colors make products easier to spot and organize across the aisle." if en else "La banda azul de ami mantiene unida a la familia. Los colores por categoría ayudan a encontrar y organizar los productos en el pasillo.",
      "real":"Built around real meals and everyday moments." if en else "Pensado para comidas de verdad y momentos cotidianos.", "real2":"Familiar staples, one clear family." if en else "Productos conocidos, una familia clara.",
      "tonight":"Turn pantry staples into dinner" if en else "Convierte la despensa en una comida", "tonightp":"Simple recipes with ami products and ingredients you probably already have." if en else "Recetas sencillas con productos ami e ingredientes que probablemente ya tienes.",
      "recipes":"Explore recipes" if en else "Ver recetas", "retailh":"Bring ami to your market" if en else "Lleva ami a tu mercado", "retailp":"Explore the retail program and talk with American Foods International." if en else "Conoce el programa comercial y conversa con American Foods International.", "retailcta":"For retailers" if en else "Para supermercados"
    }
    cats=[("tomato","new-whole-peeled-tomatoes.webp"),("beans","new-black-beans.webp"),("tuna","new-tuna-chunks-water.webp"),("drinks","new-drink-orange-1l.webp")]
    cat_html="".join(f'<a class="category-card" href="{href("products",lang)}?category={key}#catalog" style="--cat:{CATEGORIES[key][2]}"><span>{c["range"]}</span><strong>{CATEGORIES[key][0 if en else 1]}</strong><img src="{asset("img/"+image,lang)}" width="900" height="900" alt="" loading="lazy"></a>' for key,image in cats)
    featured="".join(product_card(PRODUCTS[i],lang,True) for i in (9,18,21,14,25,27))
    recipes="".join([
      recipe_card("recipe-arroz.webp","Black bean rice" if en else "Arroz con frijoles negros","15 min",["ami Black Beans"] if en else ["ami Frijoles negros"],"black-bean-rice",lang),
      recipe_card("new-life-cooking.webp","Pantry tomato pasta" if en else "Pasta de tomate de la despensa","25 min",["ami Tomato Paste"] if en else ["ami Pasta de tomate"],"tomato-pasta",lang),
      recipe_card("recipe-ensalada.webp","Three-bean corn salad" if en else "Ensalada de frijoles y maíz","15 min",["ami Sweet Corn","ami Pinto Beans"] if en else ["ami Maíz dulce","ami Frijoles pintos"],"bean-corn-salad",lang)
    ])
    main=f'''<main id="main" class="page-shell">
<section class="hero"><div class="hero-copy"><span class="eyebrow light">{c['eyebrow']}</span><h1>{c['h1']}</h1><p>{c['lead']}</p><div class="actions"><a class="button primary" href="{href('products',lang)}">{c['products']} {ARROW}</a><a class="button outline" href="{href('recipes',lang)}">{c['cook']}</a></div></div><div class="hero-stage"><div class="stage-label"><span>{c['stage']}</span><span>ami anytime</span></div><picture><source media="(max-width:700px)" srcset="{asset('img/lineup-800.webp',lang)}"><img src="{asset('img/lineup.webp',lang)}" width="1600" height="1063" alt="{c['stage']}"></picture></div></section>
<div class="proof-strip" aria-label="Brand highlights">{"".join(f'<div><i></i><span>{x}</span></div>' for x in c['proof'])}</div>
<section class="finder" aria-labelledby="finder-heading"><div><span class="eyebrow">{c['findeyebrow']}</span><h2 id="finder-heading">{c['findh']}</h2></div><form class="search-form" action="{href('products',lang)}" method="get">{SEARCH}<label class="visually-hidden" for="home-search">{c['placeholder']}</label><input id="home-search" name="q" placeholder="{c['placeholder']}"><button class="button navy" type="submit">{c['search']}</button></form></section>
<section class="section" data-reveal><div class="section-heading"><div><span class="eyebrow">{c['eyebrow']}</span><h2>{c['start']}</h2><p>{c['startp']}</p></div><a class="text-link" href="{href('products',lang)}">{c['all']} {ARROW}</a></div><div class="category-grid">{cat_html}</div></section>
<section class="section" data-reveal><div class="section-heading"><div><span class="eyebrow">{c['range']}</span><h2>{c['featured']}</h2><p>{c['featuredp']}</p></div></div><div class="product-grid">{featured}</div></section>
<section class="section" data-reveal><div class="identity-panel"><div><span class="eyebrow">ami anytime</span><h2>{c['system']}</h2><p>{c['systemp']}</p><div class="color-key"><span style="--swatch:var(--tomato)"><i></i>{CATEGORIES['tomato'][0 if en else 1]}</span><span style="--swatch:var(--beans)"><i></i>{CATEGORIES['beans'][0 if en else 1]}</span><span style="--swatch:var(--corn)"><i></i>{CATEGORIES['veg'][0 if en else 1]}</span><span style="--swatch:var(--sea)"><i></i>{CATEGORIES['tuna'][0 if en else 1]}</span></div></div><div class="identity-product"><img src="{asset('img/tomato-paste.webp',lang)}" width="860" height="860" alt="ami {('Tomato Paste' if en else 'Pasta de tomate')}"></div></div></section>
<section class="section" data-reveal><div class="story-grid"><figure class="story-card"><picture><source media="(max-width:700px)" srcset="{asset('img/new-life-cooking-582.webp',lang)}"><img src="{asset('img/new-life-cooking.webp',lang)}" width="1163" height="1237" alt="{c['real']}" loading="lazy"></picture><figcaption>{c['real']}</figcaption></figure><figure class="story-card"><picture><source media="(max-width:700px)" srcset="{asset('img/new-life-kid-720.webp',lang)}"><img src="{asset('img/new-life-kid.webp',lang)}" width="1439" height="1071" alt="{c['real2']}" loading="lazy"></picture><figcaption>{c['real2']}</figcaption></figure></div></section>
<section class="section" data-reveal><div class="section-heading"><div><span class="eyebrow">{c['cook']}</span><h2>{c['tonight']}</h2><p>{c['tonightp']}</p></div><a class="text-link" href="{href('recipes',lang)}">{c['recipes']} {ARROW}</a></div><div class="recipe-grid">{recipes}</div></section>
<section class="section" data-reveal><div class="retailer-panel"><div><span class="eyebrow light">{c['retailcta']}</span><h2>{c['retailh']}</h2><p>{c['retailp']}</p></div><a class="button light" href="{href('partners',lang)}">{c['retailcta']} {ARROW}</a></div></section></main>'''
    title="ami anytime | Everyday food, ready for real meals" if en else "ami anytime | Alimentos de todos los días para comidas de verdad"
    description="Explore ami everyday pantry products, simple recipes, and confirmed market availability." if en else "Explora productos ami para la despensa, recetas sencillas y disponibilidad confirmada por mercado."
    return frame("home",lang,title,description,main,organization(lang))

def page_hero(lang,eyebrow,title,body,crumb):
    home="Home" if lang=="en" else "Inicio"
    return f'''<section class="page-hero"><span class="eyebrow">{eyebrow}</span><h1>{title}</h1><p>{body}</p></section><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{href('home',lang)}">{home}</a><span aria-hidden="true">/</span><span>{crumb}</span></nav>'''

def build_products(lang):
    en=lang=="en"
    title="Products | ami anytime" if en else "Productos | ami anytime"
    description="Browse the 29-product ami launch range by category, pack size and flavor." if en else "Explora el surtido de lanzamiento de 29 productos ami por categoría, tamaño y sabor."
    labels={
      "eyebrow":"Products" if en else "Productos", "h1":"Everyday essentials, organized by aisle" if en else "Productos esenciales, organizados por pasillo",
      "lead":"Browse the ami launch range by category and pack size. Availability may vary by market." if en else "Explora el surtido de lanzamiento de ami por categoría y tamaño. La disponibilidad puede variar según el mercado.",
      "search":"Search products" if en else "Buscar productos", "clear":"Clear" if en else "Borrar", "all":"All" if en else "Todos",
      "count":"29 products in the launch range" if en else "29 productos en el surtido de lanzamiento", "badge":"Launch range" if en else "Surtido de lanzamiento", "heading":"The ami launch range" if en else "El surtido de lanzamiento ami",
      "empty":"No products match that search." if en else "Ningún producto coincide con esa búsqueda.",
      "more":"More from ami" if en else "Más de ami",
      "morep":"The broader program is planned across pantry, beverages, dairy, frozen, household and personal care. Final assortment and timing are set market by market." if en else "El programa ampliado contempla productos de despensa, bebidas, lácteos, congelados, hogar y cuidado personal. El surtido final y las fechas se definen mercado por mercado.",
      "cta":"Explore the retail program" if en else "Conocer el programa para supermercados"
    }
    buttons=[("all",labels["all"])]+[(key,CATEGORIES[key][0 if en else 1]) for key in ("drinks","tomato","veg","beans","tuna","pantry")]
    main=f'''<main id="main" class="page-shell">{page_hero(lang,labels['eyebrow'],labels['h1'],labels['lead'],labels['eyebrow'])}
<section class="catalog-tools" id="catalog" aria-label="{labels['search']}"><div class="catalog-search">{SEARCH}<label class="visually-hidden" for="catalog-search">{labels['search']}</label><input id="catalog-search" type="search" placeholder="{labels['search']}" autocomplete="off"><button id="catalog-clear" type="button">{labels['clear']}</button></div><div class="filter-row" aria-label="{'Categories' if en else 'Categorías'}">{"".join(f'<button type="button" data-filter="{key}" aria-pressed="{"true" if key=="all" else "false"}">{label}</button>' for key,label in buttons)}</div><p class="catalog-status" id="catalog-status" aria-live="polite" data-template-en="products shown" data-template-es="productos visibles">{labels['count']}</p></section>
<section class="catalog-section"><div class="section-heading"><div><span class="eyebrow">{labels['badge']}</span><h2>{labels['heading']}</h2></div></div><div class="product-grid" id="product-grid">{"".join(product_card(p,lang,True) for p in PRODUCTS)}</div><div class="catalog-empty" id="catalog-empty" hidden>{labels['empty']}</div></section>
<section class="program-preview" data-reveal><span class="eyebrow light">ami anytime</span><h2>{labels['more']}</h2><p>{labels['morep']}</p><div class="program-categories"><span>{'Pantry' if en else 'Despensa'}</span><span>{'Beverages' if en else 'Bebidas'}</span><span>{'Dairy' if en else 'Lácteos'}</span><span>{'Frozen' if en else 'Congelados'}</span><span>{'Household' if en else 'Hogar'}</span><span>{'Personal care' if en else 'Cuidado personal'}</span></div><a class="button light" href="{href('partners',lang)}">{labels['cta']} {ARROW}</a></section></main>'''
    items={"@context":"https://schema.org","@type":"ItemList","name":"ami launch range" if en else "Surtido de lanzamiento ami","numberOfItems":len(PRODUCTS),"itemListElement":[{"@type":"ListItem","position":i+1,"name":p[1 if en else 2]} for i,p in enumerate(PRODUCTS)]}
    return frame("products",lang,title,description,main,items)

RECIPES = [
  {"id":"black-bean-rice","image":"recipe-arroz.webp","time":"35 min","en":("Black bean rice",["2 cups cooked rice","1 can ami Black Beans","1 small onion, chopped","Lime and cilantro to serve"],["Warm the beans with the onion in a saucepan.","Fold in the cooked rice and heat through.","Finish with lime and cilantro."]),"es":("Arroz con frijoles negros",["2 tazas de arroz cocido","1 lata de ami Frijoles negros","1 cebolla pequeña picada","Limón y cilantro para servir"],["Calienta los frijoles con la cebolla en una olla.","Incorpora el arroz cocido y calienta bien.","Termina con limón y cilantro."]),"uses_en":["ami Black Beans"],"uses_es":["ami Frijoles negros"]},
  {"id":"tomato-pasta","image":"new-life-cooking.webp","time":"25 min","en":("Pantry tomato pasta",["400 g pasta","2 tbsp ami Tomato Paste","1 can ami Whole Peeled Tomatoes","1 can ami Tuna Chunks in Oil","Garlic and herbs"],["Cook the pasta until al dente.","Cook the tomato paste and garlic for one minute, then add the tomatoes.","Simmer for 10 minutes, fold in the tuna and toss with the pasta."]),"es":("Pasta de tomate de la despensa",["400 g de pasta","2 cucharadas de ami Pasta de tomate","1 lata de ami Tomates enteros pelados","1 lata de ami Atún en trozos en aceite","Ajo y hierbas"],["Cocina la pasta hasta que esté al dente.","Cocina la pasta de tomate y el ajo por un minuto; luego agrega los tomates.","Cocina 10 minutos, incorpora el atún y mezcla con la pasta."]),"uses_en":["ami Tomato Paste","ami Whole Peeled Tomatoes","ami Tuna"],"uses_es":["ami Pasta de tomate","ami Tomates enteros pelados","ami Atún"]},
  {"id":"bean-corn-salad","image":"recipe-ensalada.webp","time":"15 min","en":("Three-bean corn salad",["1 can ami Sweet Corn","1 can ami Pinto Beans","1 can ami Red Kidney Beans","Bell pepper, lime and cilantro"],["Drain and rinse the beans and corn.","Combine with the chopped pepper.","Dress with lime, season and finish with cilantro."]),"es":("Ensalada de frijoles y maíz",["1 lata de ami Maíz dulce","1 lata de ami Frijoles pintos","1 lata de ami Frijoles rojos","Pimiento, limón y cilantro"],["Escurre y enjuaga los frijoles y el maíz.","Combina con el pimiento picado.","Adereza con limón, sazona y termina con cilantro."]),"uses_en":["ami Sweet Corn","ami Pinto Beans","ami Red Kidney Beans"],"uses_es":["ami Maíz dulce","ami Frijoles pintos","ami Frijoles rojos"]},
  {"id":"mango-peach-smoothie","image":"recipe-batido.webp","time":"5 min","en":("Mango and peach smoothie",["1 cup ami Mango Fruit Drink","½ can ami Sliced Peaches, drained","½ cup plain yogurt","1 cup ice"],["Add everything to a blender.","Blend until smooth and thick.","Serve right away."]),"es":("Batido de mango y durazno",["1 taza de ami Bebida de mango","½ lata de ami Duraznos en rebanadas, escurridos","½ taza de yogur natural","1 taza de hielo"],["Pon todo en la licuadora.","Licúa hasta que quede suave y espeso.","Sirve de inmediato."]),"uses_en":["ami Mango Fruit Drink","ami Sliced Peaches"],"uses_es":["ami Bebida de mango","ami Duraznos en rebanadas"]},
  {"id":"vegetable-noodle-soup","image":"recipe-sopa.webp","time":"30 min","en":("Vegetable noodle soup",["1 can ami Mixed Vegetables","1 can ami Chopped Tomatoes","1 pack ami Instant Noodles, Chicken","Onion, garlic and water"],["Soften the onion and garlic in a pot.","Add the tomatoes and water; simmer for 10 minutes.","Add the vegetables and noodles, then cook until the noodles are tender."]),"es":("Sopa de vegetales con fideos",["1 lata de ami Vegetales mixtos","1 lata de ami Tomates picados","1 paquete de ami Fideos instantáneos sabor pollo","Cebolla, ajo y agua"],["Sofríe la cebolla y el ajo en una olla.","Agrega los tomates y el agua; cocina 10 minutos.","Añade los vegetales y los fideos; cocina hasta que los fideos estén tiernos."]),"uses_en":["ami Mixed Vegetables","ami Chopped Tomatoes","ami Instant Noodles"],"uses_es":["ami Vegetales mixtos","ami Tomates picados","ami Fideos instantáneos"]},
  {"id":"garlic-soy-mushrooms","image":"mushrooms-whole.webp","time":"15 min","packshot":True,"en":("Garlic-soy mushrooms",["2 cans ami Whole Button Mushrooms, drained","1 tbsp ami Dark Soy Sauce","3 garlic cloves, sliced","Scallions and black pepper"],["Pat the mushrooms dry and sear them in a hot pan.","Add the garlic and cook for one minute.","Add the soy sauce, toss until glossy and finish with scallions."]),"es":("Champiñones al ajo y soya",["2 latas de ami Champiñones enteros, escurridos","1 cucharada de ami Salsa de soya oscura","3 dientes de ajo en láminas","Cebollín y pimienta negra"],["Seca los champiñones y dóralos en una sartén caliente.","Agrega el ajo y cocina por un minuto.","Añade la salsa de soya, mezcla hasta que brillen y termina con cebollín."]),"uses_en":["ami Whole Button Mushrooms","ami Dark Soy Sauce"],"uses_es":["ami Champiñones enteros","ami Salsa de soya oscura"]},
]

def build_recipes(lang):
    en=lang=="en"; title="Recipes | ami anytime" if en else "Recetas | ami anytime"; intro="Six simple recipes made with ami products and everyday staples." if en else "Seis recetas sencillas con productos ami e ingredientes de todos los días."
    cards="".join(recipe_card(r["image"],r[lang][0],r["time"],r["uses_en" if en else "uses_es"],r["id"],lang) for r in RECIPES)
    articles=[]
    for r in RECIPES:
        name,ingredients,steps=r[lang]; uses=r["uses_en" if en else "uses_es"]
        width,height=IMAGE_SIZES[r["image"]]
        articles.append(f'''<article class="recipe-article" id="{r['id']}"><div class="recipe-media{' packshot' if r.get('packshot') else ''}"><img src="{asset('img/'+r['image'],lang)}" width="{width}" height="{height}" alt="{esc(name)}" loading="lazy"></div><div class="recipe-body"><span class="eyebrow">{('Prep' if en else 'Preparación')}: {r['time']} · {('Serves 4' if en else 'Rinde 4 porciones')}</span><h2>{name}</h2><h3>{'ami products in this recipe' if en else 'Productos ami en esta receta'}</h3><div class="uses">{"".join(f'<span>{esc(x)}</span>' for x in uses)}</div><h3>{'Ingredients' if en else 'Ingredientes'}</h3><ul>{"".join(f'<li>{esc(x)}</li>' for x in ingredients)}</ul><h3>{'Method' if en else 'Preparación'}</h3><ol>{"".join(f'<li>{esc(x)}</li>' for x in steps)}</ol></div></article>''')
    main=f'''<main id="main" class="page-shell">{page_hero(lang,'Recipes' if en else 'Recetas','Easy meals from the pantry' if en else 'Comidas fáciles con lo que hay en la despensa',intro,'Recipes' if en else 'Recetas')}<section class="recipe-index"><div class="recipe-grid">{cards}</div></section>{''.join(articles)}<section class="retailer-panel"><div><span class="eyebrow light">ami anytime</span><h2>{'Find the products for your next meal' if en else 'Encuentra los productos para tu próxima comida'}</h2><p>{'Browse the launch range by category and pack size.' if en else 'Explora el surtido de lanzamiento por categoría y tamaño.'}</p></div><a class="button light" href="{href('products',lang)}">{'Browse products' if en else 'Ver productos'} {ARROW}</a></section></main>'''
    schema={"@context":"https://schema.org","@graph":[{"@type":"Recipe","name":r[lang][0],"image":f"{SITE}/img/{r['image']}","prepTime":"PT"+r["time"].replace(" min","M"),"recipeYield":"4 servings" if en else "4 porciones"} for r in RECIPES]}
    return frame("recipes",lang,title,intro,main,schema)

def build_pdp(lang):
    en=lang=="en"; name="Tomato Paste" if en else "Pasta de tomate"; lead="Concentrated tomato for sauces, rice, soups and stews." if en else "Tomate concentrado para salsas, arroz, sopas y guisos."
    facts=[("What it is","Concentrated tomato paste for everyday cooking."),("How to use it","Add it to sofrito, sauces, rice, soups and stews for deeper tomato flavor."),("Package information","See the package for ingredients, nutrition and storage instructions.")] if en else [("Qué es","Pasta de tomate concentrada para cocinar todos los días."),("Cómo usarla","Agrégala al sofrito, las salsas, el arroz, las sopas y los guisos para intensificar el sabor a tomate."),("Información del empaque","Consulta en el empaque los ingredientes, la información nutricional y las instrucciones de conservación.")]
    main=f'''<main id="main" class="page-shell"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{href('home',lang)}">{'Home' if en else 'Inicio'}</a><span>/</span><a href="{href('products',lang)}">{'Products' if en else 'Productos'}</a><span>/</span><span>{name}</span></nav><section class="pdp"><div class="pdp-stage"><img src="{asset('img/tomato-paste.webp',lang)}" width="860" height="860" alt="ami {name}, 400 g"></div><div class="pdp-copy"><span class="eyebrow">{'Tomato' if en else 'Tomate'}</span><h1>{name}</h1><p class="pdp-lead">{lead}</p><span class="pack-size">400 g</span><ul class="fact-list">{"".join(f'<li><strong>{h}</strong><span>{p}</span></li>' for h,p in facts)}</ul><div class="actions"><a class="button navy" href="{href('where-to-buy',lang)}">{'Where to buy' if en else 'Dónde comprar'}</a><a class="button ghost" href="{href('contact',lang)}">{'Request product information' if en else 'Solicitar información del producto'}</a></div></div></section><section class="recipe-callout"><img src="{asset('img/new-life-cooking-582.webp',lang)}" width="582" height="619" alt="{'Pantry tomato pasta' if en else 'Pasta de tomate de la despensa'}" loading="lazy"><div><span class="eyebrow">{'Cook with ami' if en else 'Cocinar con ami'}</span><h2>{'Pantry tomato pasta' if en else 'Pasta de tomate de la despensa'}</h2><p>{'A simple weeknight meal built around tomatoes, tuna and pantry staples.' if en else 'Una comida sencilla para la semana con tomates, atún y productos de la despensa.'}</p></div><a class="button navy" href="{href('recipes',lang)}#tomato-pasta">{'View recipe' if en else 'Ver receta'}</a></section></main>'''
    schema={"@context":"https://schema.org","@type":"Product","name":f"ami {name}","image":f"{SITE}/img/tomato-paste.webp","description":lead,"brand":{"@type":"Brand","name":"ami anytime"},"size":"400 g"}
    return frame("product-tomato-paste",lang,f"{name} | ami anytime",lead,main,schema)

def build_about(lang):
    en=lang=="en"; intro="ami anytime is the own-brand program of American Foods International. It brings everyday grocery staples together under one clear, consistent brand." if en else "ami anytime es el programa de marca propia de American Foods International. Reúne productos básicos de todos los días bajo una marca clara y consistente."
    values=[("Easy to recognize","A consistent navy band connects the range across categories."),("Practical by design","Familiar foods and clear pack information support everyday choices."),("Built market by market","Products, packs and labels are defined for each market.")] if en else [("Fácil de reconocer","Una banda azul consistente conecta el surtido entre categorías."),("Práctica por diseño","Alimentos conocidos e información clara en el empaque apoyan las decisiones diarias."),("Desarrollada mercado por mercado","Los productos, empaques y etiquetas se definen para cada mercado.")]
    support="Keep the package and contact the store where you bought it or write to us. Include the product name, lot code and best-before date so we can review it." if en else "Conserva el empaque y comunícate con la tienda donde lo compraste o escríbenos. Incluye el nombre del producto, el código de lote y la fecha de consumo preferente para que podamos revisarlo."
    main=f'''<main id="main" class="page-shell">{page_hero(lang,'Our brand' if en else 'Nuestra marca','Everyday products, chosen with care' if en else 'Productos cotidianos, elegidos con cuidado',intro,'Our brand' if en else 'Nuestra marca')}<section class="split-section"><div class="split-copy"><span class="eyebrow">ami anytime</span><h2>{'Made to make everyday shopping clearer' if en else 'Creada para hacer más clara la compra diaria'}</h2><p>{'ami was created to make everyday groceries easier to recognize, choose and use. The range focuses on familiar foods, practical packs and a consistent look across categories.' if en else 'ami nació para que los productos de todos los días sean más fáciles de reconocer, elegir y usar. El surtido se enfoca en alimentos conocidos, tamaños prácticos y una imagen consistente entre categorías.'}</p><div class="value-list">{"".join(f'<div><strong>{h}</strong><span>{p}</span></div>' for h,p in values)}</div></div><div class="split-media"><img src="{asset('img/new-life-kid.webp',lang)}" width="1439" height="1071" alt="{'ami in an everyday family moment' if en else 'ami en un momento familiar cotidiano'}" loading="lazy"></div></section><section class="identity-panel"><div><span class="eyebrow">{'Recognizing ami' if en else 'Cómo reconocer ami'}</span><h2>{'Find the navy band' if en else 'Busca la banda azul'}</h2><p>{'Look for the navy ami band and green line. Aisle colors help distinguish beans and vegetables, tomato products, corn, fruit and products of the sea at a glance.' if en else 'Busca la banda azul de ami y la línea verde. Los colores por pasillo ayudan a distinguir de inmediato los frijoles y vegetales, productos de tomate, maíz, frutas y productos del mar.'}</p></div><div class="identity-product"><img src="{asset('img/new-whole-peeled-tomatoes.webp',lang)}" width="860" height="860" alt="ami {'Whole Peeled Tomatoes' if en else 'Tomates enteros pelados'}"></div></section><section class="empty-state" id="product-support"><span class="eyebrow light">{'Product support' if en else 'Ayuda con un producto'}</span><h2>{'Questions about a product?' if en else '¿Tienes alguna pregunta sobre un producto?'}</h2><p>{support}</p><div class="actions"><a class="button light" href="{href('contact',lang)}">{'Contact us' if en else 'Contáctanos'}</a></div></section></main>'''
    return frame("about",lang,"Our brand | ami anytime" if en else "Nuestra marca | ami anytime",intro,main)

def build_where(lang):
    en=lang=="en"; intro="Choose a country to see confirmed retailers and store locations." if en else "Elige un país para consultar cadenas y tiendas confirmadas."
    main=f'''<main id="main" class="page-shell">{page_hero(lang,'Where to buy' if en else 'Dónde comprar','Find ami in your market' if en else 'Encuentra ami en tu mercado',intro,'Where to buy' if en else 'Dónde comprar')}<section class="empty-state"><span class="eyebrow light">{'Availability' if en else 'Disponibilidad'}</span><h2>{'No confirmed stores are published yet.' if en else 'Aún no hay tiendas confirmadas publicadas.'}</h2><p>{'We will add retailers and store locations here once they are confirmed for publication. For now, contact us with your market or visit the retailer program.' if en else 'Agregaremos aquí cadenas y tiendas cuando estén confirmadas para publicación. Por ahora, contáctanos indicando tu mercado o conoce el programa para supermercados.'}</p><div class="actions"><a class="button light" href="{href('contact',lang)}">{'Contact us' if en else 'Contáctanos'}</a><a class="button outline" href="{href('partners',lang)}">{'For retailers' if en else 'Para supermercados'}</a></div></section></main>'''
    return frame("where-to-buy",lang,"Where to buy | ami anytime" if en else "Dónde comprar | ami anytime",intro,main)

def build_partners(lang):
    en=lang=="en"; intro="ami combines a coordinated consumer brand, category-based assortment planning and launch support from American Foods International." if en else "ami combina una marca de consumo coordinada, planificación de surtido por categoría y apoyo de lanzamiento de American Foods International."
    steps=[("Tell us about your market","Share your company, country and retail format."),("Review categories and requirements","Explore the categories that fit your market and operating needs."),("Build the launch plan together","Define the approved assortment, information and launch materials.")] if en else [("Cuéntanos sobre tu mercado","Comparte tu empresa, país y formato comercial."),("Revisemos las categorías y los requisitos","Exploremos las categorías que se ajustan a tu mercado y operación."),("Construyamos juntos el plan de lanzamiento","Definamos el surtido aprobado, la información y los materiales de lanzamiento.")]
    components=["A coordinated English-and-Spanish consumer brand","Assortment planning by category","Packaging and merchandising guidelines","Approved product information and specifications","Launch materials and recipe content","A dedicated commercial point of contact"] if en else ["Una marca de consumo coordinada en español e inglés","Planificación de surtido por categoría","Lineamientos de empaque y exhibición","Información y especificaciones de producto aprobadas","Materiales de lanzamiento y contenido de recetas","Un contacto comercial dedicado"]
    subject="ami retailer inquiry" if en else "Consulta comercial ami"
    main=f'''<main id="main" class="page-shell">{page_hero(lang,'For retailers' if en else 'Para supermercados','Build a recognizable own-brand range for your market' if en else 'Desarrolla un surtido de marca propia reconocible para tu mercado',intro,'For retailers' if en else 'Para supermercados')}<section class="route-grid">{"".join(f'<article class="route-card"><span class="route-number">{i}</span><h2>{h}</h2><p>{p}</p></article>' for i,(h,p) in enumerate(steps,1))}</section><section class="split-section"><div class="split-copy"><span class="eyebrow">{'The program' if en else 'El programa'}</span><h2>{'A clear system from pack to shelf' if en else 'Un sistema claro del empaque al anaquel'}</h2><div class="value-list">{"".join(f'<div><strong>{x}</strong></div>' for x in components)}</div></div><div class="split-media"><img src="{asset('img/lineup.webp',lang)}" width="1600" height="1063" alt="{'ami launch range' if en else 'Surtido de lanzamiento ami'}" loading="lazy"></div></section><section class="retailer-panel"><div><span class="eyebrow light">{'Start a conversation' if en else 'Inicia una conversación'}</span><h2>{'Tell us about your market' if en else 'Cuéntanos sobre tu mercado'}</h2><p>{'Tell us about your company, market and the categories you are exploring.' if en else 'Cuéntanos sobre tu empresa, tu mercado y las categorías que estás evaluando.'}</p></div><a class="button light" href="mailto:info@afoodsinc.com?subject={subject.replace(' ','%20')}">{'Contact the ami team' if en else 'Contactar al equipo de ami'} {ARROW}</a></section></main>'''
    return frame("partners",lang,"For retailers | ami anytime" if en else "Para supermercados | ami anytime",intro,main)

def build_contact(lang):
    en=lang=="en"; intro="Choose a topic so your message reaches the right team." if en else "Elige un tema para que tu mensaje llegue al equipo indicado."
    topics=[("Product question","Include the product name, lot code and best-before date.","ami product question"),("Retail inquiry","Tell us about your company, market and categories.","ami retailer inquiry"),("Supplier proposal","Share the company and products you represent.","ami supplier proposal"),("Media or other","Send the context needed to route your message.","ami general inquiry")] if en else [("Consulta sobre un producto","Incluye el nombre del producto, el código de lote y la fecha de consumo preferente.","Consulta sobre un producto ami"),("Consulta comercial","Cuéntanos sobre tu empresa, mercado y categorías.","Consulta comercial ami"),("Propuesta de proveedor","Comparte la empresa y los productos que representas.","Propuesta de proveedor ami"),("Prensa u otro","Envía el contexto necesario para dirigir tu mensaje.","Consulta general ami")]
    cards="".join(f'<article class="route-card"><span class="route-number">{i}</span><h2>{h}</h2><p>{p}</p><a class="text-link" href="mailto:info@afoodsinc.com?subject={s.replace(" ","%20")}">{"Write to us" if en else "Escríbenos"} {ARROW}</a></article>' for i,(h,p,s) in enumerate(topics,1))
    main=f'''<main id="main" class="page-shell">{page_hero(lang,'Contact' if en else 'Contacto','How can we help?' if en else '¿Cómo podemos ayudarte?',intro,'Contact' if en else 'Contacto')}<section class="route-grid contact-routes">{cards}</section><section class="office-grid"><article class="office"><h2>{'United States office and warehouse' if en else 'Oficina y bodega en Estados Unidos'}</h2><address>2300 NW 92nd Ave<br>Doral, FL 33172, USA<br><a class="text-link" href="tel:+18778947675">+1 877 894 7675</a></address></article><article class="office"><h2>{'Panama office' if en else 'Oficina de Panamá'}</h2><address>PH Plaza del Este, Torre A, Piso 13<br>Costa del Este, Panamá<br><a class="text-link" href="tel:+5073107576">+507 310 7576</a></address></article></section></main>'''
    return frame("contact",lang,"Contact | ami anytime" if en else "Contacto | ami anytime",intro,main)

def build_404():
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | ami anytime</title><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&amp;family=Nunito:wght@800;900&amp;display=swap" rel="stylesheet"><link rel="stylesheet" href="site.css"></head><body><a class="skip-link" href="#main">Skip to content</a><main id="main" class="page-shell"><section class="page-hero error-hero"><span class="eyebrow">Wrong aisle? · ¿Pasillo equivocado?</span><h1>404</h1></section><section class="error-panels"><article class="route-card"><h2>This page isn’t here.</h2><p>We couldn’t find that page. Choose where to go next.</p><div class="actions"><a class="button navy" href="index.html">Home</a><a class="button ghost" href="products.html">Products</a><a class="button ghost" href="recipes.html">Recipes</a></div></article><article class="route-card" lang="es"><h2>Esta página no está aquí.</h2><p>No encontramos esa página. Elige cómo continuar.</p><div class="actions"><a class="button navy" href="es/index.html">Inicio</a><a class="button ghost" href="es/products.html">Productos</a><a class="button ghost" href="es/recipes.html">Recetas</a></div></article></section></main></body></html>'''

def write(slug,lang,content):
    target=ROOT/page_path(slug,lang); target.parent.mkdir(parents=True,exist_ok=True); target.write_text(content.strip()+"\n",encoding="utf-8")

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--home-only",action="store_true"); args=parser.parse_args()
    builders={"home":build_home}
    if not args.home_only:
        builders.update({"products":build_products,"product-tomato-paste":build_pdp,"recipes":build_recipes,"about":build_about,"where-to-buy":build_where,"partners":build_partners,"contact":build_contact})
    for lang in ("en","es"):
        for slug,builder in builders.items(): write(slug,lang,builder(lang))
    if not args.home_only:
        (ROOT/"404.html").write_text(build_404().strip()+"\n",encoding="utf-8")

if __name__ == "__main__": main()
