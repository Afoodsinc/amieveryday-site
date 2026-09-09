#!/usr/bin/env python3
"""ami anytime site generator — EN at /, ES at /es/. Output: site/"""
import json, os, re, html
SC = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(SC, "site")
os.makedirs(os.path.join(SITE, "es"), exist_ok=True)

# ---------- CSS: reuse the mockup's style + additions ----------
base_css = re.search(r"<style>(.*?)</style>", open(os.path.join(SC, "template.html")).read(), re.S).group(1)
base_css = base_css.replace(".boardwrap{max-width:1360px;margin:0 auto;padding:40px 24px 80px;display:flex;flex-direction:column;gap:64px}", ".boardwrap{max-width:1360px;margin:0 auto;padding:0;display:flex;flex-direction:column}")
base_css = base_css.replace("body{background:var(--board);", "body{background:var(--paper);")
base_css = base_css.replace(".frame{background:var(--paper);border-radius:18px;box-shadow:0 1px 0 rgba(22,34,63,.06),var(--sh-photo);overflow:hidden;border:1px solid rgba(22,34,63,.06)}", ".frame{background:var(--paper);overflow:hidden}")
extra_css = """
  a.wm{text-decoration:none}
  .lang a{color:#fff} .lang a.on{color:var(--navy)}
  .burger{display:none}
  .page-head{padding:44px var(--pad) 8px} .page-head h1{font-family:var(--display);font-weight:900;font-size:44px;letter-spacing:-.03em;color:var(--navy);margin:10px 0 4px;text-wrap:balance} .page-head .es{color:var(--ink-3);font-size:17px} .page-head p{color:var(--ink-2);max-width:64ch;margin:14px 0 0;font-size:16.5px}
  .catalog{padding:24px var(--pad) 56px;display:flex;flex-direction:column;gap:40px}
  .dept{scroll-margin-top:90px} .dept-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px;border-bottom:1px solid var(--line-2);padding-bottom:10px;margin-bottom:16px}
  .dept-head h3{font-family:var(--display);font-weight:900;font-size:26px;letter-spacing:-.02em;color:var(--navy);margin:0;display:flex;align-items:center;gap:12px} .dept-head h3 i{width:14px;height:14px;border-radius:50%;background:var(--c);display:inline-block}
  .dept-head span{color:var(--ink-3);font-size:14px;font-variant-numeric:tabular-nums}
  .items{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
  .item{border:1px solid var(--line);border-radius:var(--r-s);padding:12px 14px;display:flex;gap:12px;align-items:center;background:#fff;min-height:64px}
  .item i{flex:none;width:34px;height:34px;border-radius:9px;background:var(--c);opacity:.9;display:inline-flex;align-items:center;justify-content:center}
  .item i svg{width:18px;height:18px;color:#fff}
  .item b{display:block;font-weight:700;font-size:14.5px;color:var(--ink);line-height:1.2} .item small{color:var(--ink-3);font-size:12.5px;font-variant-numeric:tabular-nums}
  .item.soon b::after{content:" · " attr(data-soon);color:var(--green-ink);font-weight:700;font-size:11px;letter-spacing:.06em;text-transform:uppercase}
  .deptnav{display:flex;gap:8px;flex-wrap:wrap;padding:18px var(--pad) 0}
  .deptnav a{border:1px solid var(--line);border-radius:var(--pill);padding:8px 13px;font-size:13px;font-weight:600;color:var(--ink-2);display:inline-flex;align-items:center;gap:8px;background:#fff} .deptnav a i{width:9px;height:9px;border-radius:50%;background:var(--c);display:inline-block}
  .rgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;padding:24px var(--pad) 56px}
  .rc{border:1px solid var(--line);border-radius:var(--r);overflow:hidden;background:#fff;display:flex;flex-direction:column}
  .rc img{width:100%;aspect-ratio:3/2;object-fit:cover}
  .rc .b{padding:16px 18px 18px;display:flex;flex-direction:column;gap:6px}
  .rc .with{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--green-ink);font-weight:700}
  .rc h3{font-family:var(--display);font-weight:800;font-size:20px;color:var(--navy);margin:0;line-height:1.15}
  .rc .meta{color:var(--ink-3);font-size:13px;display:flex;gap:12px}
  .recipe{padding:8px var(--pad) 56px;display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:40px;align-items:start;scroll-margin-top:90px}
  .recipe img{width:100%;aspect-ratio:3/2;object-fit:cover;border-radius:var(--r);box-shadow:var(--sh-photo)}
  .recipe h2{font-family:var(--display);font-weight:900;font-size:34px;letter-spacing:-.025em;color:var(--navy);margin:0 0 4px;text-wrap:balance}
  .recipe .meta{color:var(--ink-3);font-size:14px;display:flex;gap:14px;margin-bottom:14px}
  .recipe h4{font-family:var(--display);font-weight:800;font-size:14px;letter-spacing:.08em;text-transform:uppercase;color:var(--green-ink);margin:18px 0 8px}
  .recipe ul,.recipe ol{margin:0;padding-left:20px;color:var(--ink);display:flex;flex-direction:column;gap:6px;font-size:15px}
  .recipe .uses{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px} .recipe .uses span{border:1px solid var(--line);border-radius:var(--pill);padding:6px 12px;font-size:12.5px;font-weight:600;color:var(--navy);background:var(--paper-warm)}
  .rsep{height:1px;background:var(--line-2);margin:0 var(--pad) 40px}
  #map{height:520px;border-radius:var(--r);border:1px solid var(--line);margin:24px var(--pad) 0;overflow:hidden;background:var(--paper-warm)}
  .markets{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;padding:24px var(--pad) 8px}
  .mk{border:1px solid var(--line);border-radius:var(--r);padding:18px 20px;background:#fff}
  .mk b{display:block;font-family:var(--display);font-weight:800;font-size:18px;color:var(--navy)} .mk .st{display:inline-block;margin:6px 0 8px;font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;border-radius:var(--pill);padding:4px 9px;background:var(--green-soft);color:var(--green-ink)} .mk .st.next{background:#EEF0F3;color:var(--ink-3)} .mk p{margin:0;color:var(--ink-2);font-size:14.5px}
  .two{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:40px;padding:24px var(--pad) 56px;align-items:start}
  .prose{color:var(--ink);font-size:16.5px;max-width:62ch} .prose p{margin:0 0 16px} .prose h3{font-family:var(--display);font-weight:900;font-size:24px;letter-spacing:-.02em;color:var(--navy);margin:26px 0 8px}
  .vals{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:8px} .vals div{border:1px solid var(--line);border-radius:var(--r-s);padding:14px 16px;background:#fff} .vals b{display:block;font-family:var(--display);font-weight:800;color:var(--navy);font-size:16px;margin-bottom:4px} .vals span{color:var(--ink-2);font-size:14px}
  .stack{display:flex;flex-direction:column;gap:18px} .stack img{width:100%;border-radius:var(--r);box-shadow:var(--sh-photo);object-fit:cover}
  .card{border:1px solid var(--line);border-radius:var(--r);padding:22px 24px;background:#fff}
  .card h3{font-family:var(--display);font-weight:800;font-size:18px;color:var(--navy);margin:0 0 10px}
  .card ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px;font-size:15px;color:var(--ink)}
  .card li{display:flex;gap:10px;align-items:flex-start} .card li svg{flex:none;color:var(--green-ink);margin-top:3px}
  .form{display:flex;flex-direction:column;gap:12px} .form label{font-size:13px;font-weight:700;color:var(--ink-2);display:flex;flex-direction:column;gap:6px}
  .form input,.form textarea,.form select{font:inherit;font-size:15px;padding:12px 14px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)} .form textarea{min-height:120px;resize:vertical}
  .form input:focus,.form textarea:focus,.form select:focus{outline:3px solid var(--green);outline-offset:1px;border-color:var(--navy)}
  .steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;padding:8px var(--pad) 40px}
  .step{border:1px solid var(--line);border-radius:var(--r);padding:20px;background:#fff} .step b{display:block;font-family:var(--display);font-weight:900;font-size:28px;color:var(--green-ink);margin-bottom:6px} .step h4{margin:0 0 6px;font-family:var(--display);font-weight:800;font-size:17px;color:var(--navy)} .step p{margin:0;color:var(--ink-2);font-size:14.5px}
  .banner{margin:0 var(--pad);border-radius:var(--r);overflow:hidden} .banner img{width:100%;aspect-ratio:16/7;object-fit:cover;display:block}
  @media (max-width:1100px){ :root{--pad:24px} .hero{grid-template-columns:1fr;gap:28px;padding-top:36px} .hero h2{font-size:44px} .pillars{grid-template-columns:1fr 1fr} .pillars > div + div{border-left:0;padding-left:0} .aisles,.grid4,.items{grid-template-columns:repeat(2,minmax(0,1fr))} .recipes,.rgrid,.markets,.steps{grid-template-columns:1fr 1fr} .life{grid-template-columns:1fr} .life figure.big{grid-row:auto} .partners{grid-template-columns:1fr;padding:32px 24px 0} .where,.two,.recipe{grid-template-columns:1fr} .fgrid{grid-template-columns:1fr 1fr} .plp{grid-template-columns:1fr} .rail{display:none} .grid3{grid-template-columns:repeat(2,minmax(0,1fr))} .pdp{grid-template-columns:1fr} .tabs .tb{grid-template-columns:1fr} .range{flex-direction:column;align-items:flex-start} .page-head h1{font-size:36px} }
  @media (max-width:700px){ .util .l{display:none} .hero h2{font-size:36px} .aisles,.grid4,.grid3,.recipes,.rgrid,.markets,.steps,.fgrid,.pillars,.items,.vals{grid-template-columns:1fr} .pdp .stage{height:380px} #map{height:380px}
    .nav{flex-wrap:wrap;gap:12px} .menu{display:none;width:100%;flex-direction:column;gap:4px;padding:8px 0 4px;border-top:1px solid var(--line-2)} .menu a{padding:10px 0} .nav.open .menu{display:flex}
    .burger{display:inline-flex;width:44px;height:44px;border-radius:50%;border:1px solid var(--line);align-items:center;justify-content:center;background:#fff;color:var(--navy);cursor:pointer;margin-left:auto} .nav-actions .btn{display:none} }
"""
CSS = base_css + extra_css

# ---------- i18n ----------
T = {
 "en": dict(
  lang="en", other="es", other_label="ES", self_label="EN", dir="",
  util="A brand of American Foods International · Miami, FL", find="Find a store",
  nav=[("about.html","About"),("products.html","Products"),("recipes.html","Recipes"),("where-to-buy.html","Where to Buy"),("partners.html","Partners"),("contact.html","Contact")],
  hero_eyebrow="Low cost · True value", hero_h="Global flavors.<br><em>Honest</em> prices.<br>Every day.", hero_sub="Más sabor, más valor — todos los días.",
  hero_p="ami brings the quality of the world’s best-known brands to your table, at a price that respects your budget. 149 products, one trusted label, down every aisle of the store.",
  cta1="Explore products", cta2="Where to buy", tag="The basket that stretches further",
  range_b="One label you can trust, in every color of the aisle.", range_p="Green for vegetables and beans, red for tomato, yellow for corn, orange for fruit, blue for seafood — so you find what you need at a glance, and the navy ami band tells you it’s ours.",
  pillars=[("Low cost, true value","Benchmarked against the value shelf every week. The lowest price on the shelf — without the compromise."),("Global brands and flavors","Sourced from the world’s best producers — the flavors families already love, at a fraction of the brand price."),("Exclusive by design","ami is licensed to a select few retail partners in each market. If it’s on your shelf, it isn’t on your competitor’s."),("Quality guaranteed","Every product carries our guarantee. If it isn’t right, bring it back — it’s on us.")],
  aisle_eyebrow="Shop by aisle", aisle_h="Down every aisle of the store", aisle_sub="En cada pasillo de tu supermercado", all149="All 149 products",
  new_eyebrow="What’s new", new_h="New this season", new_sub="Fruit drinks · 1 L and 200 ml", new_link="See all beverages", new="New",
  core_eyebrow="On shelf now", core_h="Start with the pantry core", core_sub="The basics already on the shelf", core_link="See canned goods",
  life_eyebrow="Real life", life_h="Made for the way you actually shop", life_sub="For everyday shopping",
  life_caps=["Find the navy band, find the value","Same quality, smarter price","In every kitchen"],
  rec_eyebrow="Recipes", rec_h="Dinner from the pantry", rec_sub="Quick ideas with ami products", rec_link="All recipes", rom="Recipe of the month", see="See recipe",
  part_eyebrow="For retailers · Partners", part_h="A brand built for a few select partners", part_p="ami isn’t sold everywhere — by design. In each market we license the full 149-product program to one retail partner, country by country, with true exclusivity and launch support. Global sourcing, one mixed container, one purchase order.",
  part_list=["Country-level exclusivity, category by category","Price shielding written into every license","Launch plans, displays and in-store activation","Registrations, specs and certifications handled"], part_cta="Become a partner", part_cta2="Talk to us",
  wtb_eyebrow="Where to buy", wtb_h="Coming to shelves across Central America, the Caribbean and South Florida", wtb_p="Ask for ami anytime at your supermarket — and tell us where you shop, so we bring it closer to you.", wtb_cta="Find a store near you",
  news_eyebrow="Stay close", news_h="New products, recipes and offers — once a month", news_p="No noise. One email a month with what’s new on the shelf and what to cook with it.", news_ph="Your email", news_btn="Sign up",
  f_tag="Present at every breakfast, every celebration, every stage of life.", f_products="Products", f_brand="Brand", f_partners="Partners", f_contact="Contact",
  f_links_p=[("products.html#canned","Canned Goods"),("products.html#pantry","Pantry"),("products.html#beverages","Beverages"),("products.html#household","Household"),("products.html","All products")],
  f_links_b=[("about.html","About ami"),("about.html#guarantee","Our guarantee"),("recipes.html","Recipes"),("where-to-buy.html","Where to buy")],
  f_links_t=[("partners.html","Become a partner"),("partners.html#program","Country licensing"),("contact.html","Spec sheets"),("contact.html","Contact sales")],
  dist="Distributed by American Foods International Inc", seal="Quality guaranteed", legal="© 2026 American Foods International Inc. ami anytime™ is a trademark of American Foods International Inc.", privacy="Privacy", terms="Terms", access="Accessibility",
  # products page
  prod_title="All products · ami anytime", prod_h="All 149 products", prod_sub="Todos los productos", prod_p="The full ami anytime program, department by department. Items marked “coming soon” are in development and arrive in waves; everything else is on shelf or launching now.", soon="coming soon", existing="on shelf",
  # recipes page
  rec_title="Recipes · ami anytime", recp_h="Recipes from the pantry", recp_sub="Recetas", recp_p="Simple, honest dishes built around ami products — the kind you can cook on a weeknight with what’s already in the cupboard.", serves="Serves", mins="min", ingredients="Ingredients", method="Method", uses="Made with",
  # where to buy page
  wtb_title="Where to buy · ami anytime", wtbp_h="Where to find ami", wtbp_sub="Dónde comprar", wtbp_p="ami anytime launches market by market through one exclusive retail partner in each country. Here is where we are heading first — ask for ami at your supermarket, and tell us where you shop.", launching="Launching", next="Coming next", tell="Tell us where you shop",
  # about
  about_title="About · ami anytime", about_h="A brand that redefines the word “value”", about_sub="Nuestra historia", about_p="ami anytime is the own-brand program of American Foods International — a Miami-based food company that has spent years bringing trusted American and global brands to supermarkets across Central America and the Caribbean. We built ami for the shopper who is price-conscious but never quality-blind.",
  about_body=[("Why ami exists","Families in our markets pay some of the highest prices in the hemisphere for everyday groceries, and the “value” options on the shelf too often mean a compromise. We thought there was a better way: source each product from the world’s best producer for that category, put it under one honest label, and price it against the value shelf — every week."),("How we work","We don’t make everything ourselves. We choose. Every ami product comes from a qualified producer — tomatoes from where tomatoes are best, tuna from where tuna is best — and is packed to our specification, registered in each market, and guaranteed by us."),("One brand, one look","The navy ami band with the green line is the same on every pack. The color of the label tells you the aisle: green for vegetables and beans, red for tomato, yellow for corn, orange for fruit, blue for seafood. Find the band, find the value.")],
  values_h="What ami is", values=[("Smart","Ahorro inteligente — saving that never feels like going without."),("Practical","Everyday products in the sizes families actually use."),("Honest","Real claims, real quality, one guarantee."),("Modern","A clean, confident brand you are glad to have on the table."),("Accessible","Priced for every budget, available where you already shop.")],
  guar_h="Our guarantee", guar_p="Every ami product carries the American Foods quality guarantee. If a product isn’t right, take it back to the store where you bought it, or write to us — we make it right, no questions.",
  # partners
  partn_title="Partners · ami anytime", partn_h="One market. One partner. One program.", partn_sub="Para retailers", partn_p="ami anytime is licensed to a single retail partner per country: a complete 149-product own-brand program, with true category-by-category exclusivity, price shielding, and a launch plan — sourced globally and delivered in one mixed container against one purchase order.",
  steps=[("1","Country license","Exclusive rights to the ami program in your market, category by category, for the term of the agreement."),("2","Launch plan","Assortment, planogram, pricing ladder, displays and in-store activation — built with your team before the first container lands."),("3","Ongoing supply","Global sourcing, registrations and certifications handled by us; replenishment on one PO, one mixed container, weekly price benchmarks.")],
  partn_form_h="Talk to us about your market", partn_form_p="Tell us who you are and where you operate. A member of the American Foods commercial team will come back within two business days.", company="Company", country="Country / market", name="Your name", email="Email", message="Message", send="Send",
  # contact
  contact_title="Contact · ami anytime", contact_h="Get in touch", contact_sub="Contáctanos", contact_p="For shoppers, retailers and suppliers — we read everything.",
  us_office="US office & warehouse", pa_office="Panama office", phone="Phone", mail="Email", hours="Office hours", hours_v="Monday–Friday, 8:30–17:30 ET", social="Follow",
  form_h="Send us a message", topic="Topic", topics=["I’m a shopper","I’m a retailer","I’m a supplier","Press / other"],
  pdp_crumb=["Home","Products","Canned Goods","Tomato Paste"],
 ),
 "es": dict(
  lang="es", other="", other_label="EN", self_label="ES", dir="es/",
  util="Una marca de American Foods International · Miami, FL", find="Buscar tienda",
  nav=[("about.html","Nosotros"),("products.html","Productos"),("recipes.html","Recetas"),("where-to-buy.html","Dónde comprar"),("partners.html","Socios"),("contact.html","Contacto")],
  hero_eyebrow="Bajo costo · Valor real", hero_h="Sabores del mundo.<br>Precios <em>honestos</em>.<br>Todos los días.", hero_sub="Más sabor, más valor.",
  hero_p="ami lleva a tu mesa la calidad de las marcas más reconocidas del mundo, a un precio que respeta tu presupuesto. 149 productos, una sola marca de confianza, en cada pasillo del supermercado.",
  cta1="Ver productos", cta2="Dónde comprar", tag="La canasta que rinde más",
  range_b="Una marca en la que confías, en cada color del pasillo.", range_p="Verde para vegetales y frijoles, rojo para tomate, amarillo para maíz, naranja para frutas, azul para pescados — encuentras lo que buscas de un vistazo, y la banda azul de ami te dice que es nuestro.",
  pillars=[("Bajo costo, valor real","Comparado cada semana contra el anaquel de valor. El precio más bajo del anaquel — sin sacrificar calidad."),("Marcas y sabores del mundo","De los mejores productores del mundo — los sabores que las familias ya conocen, a una fracción del precio de marca."),("Exclusivo por diseño","ami se licencia a unos pocos socios comerciales en cada mercado. Si está en tu anaquel, no está en el de tu competencia."),("Calidad garantizada","Cada producto lleva nuestra garantía. Si algo no está bien, devuélvelo — nosotros respondemos.")],
  aisle_eyebrow="Compra por pasillo", aisle_h="En cada pasillo del supermercado", aisle_sub="Down every aisle of the store", all149="Los 149 productos",
  new_eyebrow="Novedades", new_h="Nuevo esta temporada", new_sub="Bebidas de fruta · 1 L y 200 ml", new_link="Ver todas las bebidas", new="Nuevo",
  core_eyebrow="Ya en anaquel", core_h="Empieza por la despensa básica", core_sub="Los básicos que ya están en el anaquel", core_link="Ver enlatados",
  life_eyebrow="Vida real", life_h="Hecho para la compra de todos los días", life_sub="Made for the way you shop",
  life_caps=["Busca la banda azul, encuentra el valor","La misma calidad, mejor precio","En cada cocina"],
  rec_eyebrow="Recetas", rec_h="La cena sale de la despensa", rec_sub="Ideas rápidas con productos ami", rec_link="Todas las recetas", rom="Receta del mes", see="Ver receta",
  part_eyebrow="Para retailers · Socios", part_h="Una marca hecha para unos pocos socios", part_p="ami no se vende en todas partes — a propósito. En cada mercado licenciamos el programa completo de 149 productos a un solo socio comercial, país por país, con exclusividad real y apoyo de lanzamiento. Abastecimiento global, un contenedor mixto, una orden de compra.",
  part_list=["Exclusividad por país, categoría por categoría","Protección de precio escrita en cada licencia","Planes de lanzamiento, exhibiciones y activación en tienda","Registros, fichas técnicas y certificaciones resueltas"], part_cta="Quiero ser socio", part_cta2="Hablemos",
  wtb_eyebrow="Dónde comprar", wtb_h="Llegando a los anaqueles de Centroamérica, el Caribe y el sur de Florida", wtb_p="Pide ami anytime en tu supermercado — y cuéntanos dónde compras, para llevarlo más cerca de ti.", wtb_cta="Buscar tienda",
  news_eyebrow="Mantente cerca", news_h="Productos nuevos, recetas y ofertas — una vez al mes", news_p="Sin ruido. Un correo al mes con lo nuevo en el anaquel y qué cocinar con ello.", news_ph="Tu correo", news_btn="Suscribirme",
  f_tag="Presentes en cada desayuno, en cada celebración y en cada etapa de la vida.", f_products="Productos", f_brand="Marca", f_partners="Socios", f_contact="Contacto",
  f_links_p=[("products.html#canned","Enlatados"),("products.html#pantry","Despensa"),("products.html#beverages","Bebidas"),("products.html#household","Hogar"),("products.html","Todos los productos")],
  f_links_b=[("about.html","Sobre ami"),("about.html#guarantee","Nuestra garantía"),("recipes.html","Recetas"),("where-to-buy.html","Dónde comprar")],
  f_links_t=[("partners.html","Ser socio"),("partners.html#program","Licencia por país"),("contact.html","Fichas técnicas"),("contact.html","Contactar ventas")],
  dist="Distribuido por American Foods International Inc", seal="Calidad garantizada", legal="© 2026 American Foods International Inc. ami anytime™ es una marca registrada de American Foods International Inc.", privacy="Privacidad", terms="Términos", access="Accesibilidad",
  prod_title="Todos los productos · ami anytime", prod_h="Los 149 productos", prod_sub="All products", prod_p="El programa completo de ami anytime, departamento por departamento. Los productos marcados “próximamente” están en desarrollo y llegan por etapas; el resto ya está en anaquel o en lanzamiento.", soon="próximamente", existing="en anaquel",
  rec_title="Recetas · ami anytime", recp_h="Recetas de la despensa", recp_sub="Recipes", recp_p="Platos sencillos y honestos con productos ami — de los que se cocinan entre semana con lo que ya hay en la alacena.", serves="Porciones", mins="min", ingredients="Ingredientes", method="Preparación", uses="Hecho con",
  wtb_title="Dónde comprar · ami anytime", wtbp_h="Dónde encontrar ami", wtbp_sub="Where to buy", wtbp_p="ami anytime se lanza mercado por mercado a través de un socio comercial exclusivo en cada país. Aquí es donde vamos primero — pide ami en tu supermercado y cuéntanos dónde compras.", launching="Lanzamiento", next="Próximamente", tell="Cuéntanos dónde compras",
  about_title="Nosotros · ami anytime", about_h="La marca que redefine la palabra “valor”", about_sub="Our story", about_p="ami anytime es el programa de marca propia de American Foods International — una empresa de alimentos con sede en Miami que lleva años acercando marcas americanas y globales de confianza a los supermercados de Centroamérica y el Caribe. Creamos ami para el consumidor que cuida su bolsillo pero nunca cierra los ojos ante la calidad.",
  about_body=[("Por qué existe ami","Las familias de nuestros mercados pagan algunos de los precios más altos del hemisferio por la compra diaria, y las opciones de “valor” del anaquel demasiadas veces significan renunciar a algo. Pensamos que había un camino mejor: buscar cada producto en el mejor productor del mundo para esa categoría, ponerlo bajo una marca honesta y fijar su precio contra el anaquel de valor — cada semana."),("Cómo trabajamos","No fabricamos todo nosotros. Elegimos. Cada producto ami viene de un productor calificado — tomates de donde son mejores los tomates, atún de donde es mejor el atún — envasado bajo nuestra especificación, registrado en cada mercado y garantizado por nosotros."),("Una marca, una imagen","La banda azul de ami con la línea verde es la misma en cada empaque. El color de la etiqueta te dice el pasillo: verde para vegetales y frijoles, rojo para tomate, amarillo para maíz, naranja para frutas, azul para pescados. Busca la banda, encuentra el valor.")],
  values_h="Cómo es ami", values=[("Inteligente","Ahorro inteligente — nunca se siente como privarse."),("Práctica","Productos de todos los días en los tamaños que las familias realmente usan."),("Honesta","Claims reales, calidad real, una garantía."),("Moderna","Una marca limpia y segura que da gusto tener en la mesa."),("Accesible","Con precio para cada presupuesto, donde ya haces tu compra.")],
  guar_h="Nuestra garantía", guar_p="Cada producto ami lleva la garantía de calidad de American Foods. Si un producto no está bien, devuélvelo a la tienda donde lo compraste o escríbenos — lo resolvemos, sin preguntas.",
  partn_title="Socios · ami anytime", partn_h="Un mercado. Un socio. Un programa.", partn_sub="For retailers", partn_p="ami anytime se licencia a un único socio comercial por país: un programa completo de marca propia de 149 productos, con exclusividad real categoría por categoría, protección de precio y un plan de lanzamiento — abastecido globalmente y entregado en un contenedor mixto contra una sola orden de compra.",
  steps=[("1","Licencia por país","Derechos exclusivos del programa ami en tu mercado, categoría por categoría, por la vigencia del acuerdo."),("2","Plan de lanzamiento","Surtido, planograma, escalera de precios, exhibiciones y activación en tienda — construido con tu equipo antes de que llegue el primer contenedor."),("3","Suministro continuo","Abastecimiento global, registros y certificaciones a nuestro cargo; reposición con una OC, un contenedor mixto, comparativos de precio semanales.")],
  partn_form_h="Hablemos de tu mercado", partn_form_p="Cuéntanos quién eres y dónde operas. Un miembro del equipo comercial de American Foods te responderá en dos días hábiles.", company="Empresa", country="País / mercado", name="Tu nombre", email="Correo", message="Mensaje", send="Enviar",
  contact_title="Contacto · ami anytime", contact_h="Contáctanos", contact_sub="Get in touch", contact_p="Consumidores, retailers y proveedores — leemos todo.",
  us_office="Oficina y bodega en EE. UU.", pa_office="Oficina en Panamá", phone="Teléfono", mail="Correo", hours="Horario", hours_v="Lunes a viernes, 8:30–17:30 ET", social="Síguenos",
  form_h="Envíanos un mensaje", topic="Tema", topics=["Soy consumidor","Soy retailer","Soy proveedor","Prensa / otro"],
  pdp_crumb=["Inicio","Productos","Enlatados","Pasta de tomate"],
 )
}

CONTACT = dict(us_addr="2300 NW 92nd Ave, Doral, FL 33172, USA", pa_addr="PH Plaza del Este, Torre A, Piso 13, Costa del Este, Panamá", phone="+1 877 894 7675", pa_phone="+507 310 7576", email="info@afoodsinc.com", linkedin="https://www.linkedin.com/company/americanfoods")

# ---------- catalog data ----------
SKUS = json.load(open(os.path.join(SC, "skus.json")))
DEPTS = [  # (id, EN, ES, color var, depts in xlsx)
 ("canned","Canned Goods","Enlatados","--c-veg",["Canned Protein","Canned Beans","Canned Vegetables","Tomato","Canned Fruit"]),
 ("pantry","Pantry","Despensa","--c-pantry",["Rice & Grains","Pasta","Oils","Baking","Condiments","Seasonings"]),
 ("breakfast","Breakfast & Snacks","Desayuno y snacks","--c-corn",["Cereal & Breakfast","Cookies & Crackers","Snacks"]),
 ("beverages","Beverages","Bebidas","--c-fruit",["Beverages"]),
 ("dairy","Dairy","Lácteos","--c-dairy",["Shelf-Stable Dairy"]),
 ("frozen","Frozen","Congelados","--c-frozen",["Frozen"]),
 ("household","Household","Hogar y limpieza","--c-house",["Household"]),
 ("care","Personal Care & Wellness","Cuidado personal","--c-care",["Personal Care","OTC & Wellness","Baby"]),
]
SUB_ES = {"Canned Protein":"Proteínas en lata","Canned Beans":"Frijoles","Canned Vegetables":"Vegetales","Tomato":"Tomate","Canned Fruit":"Frutas en lata","Rice & Grains":"Arroz y granos","Pasta":"Pasta","Oils":"Aceites","Baking":"Repostería","Condiments":"Condimentos","Seasonings":"Sazonadores","Cereal & Breakfast":"Cereales y desayuno","Cookies & Crackers":"Galletas","Snacks":"Snacks","Beverages":"Bebidas","Shelf-Stable Dairy":"Lácteos de larga vida","Frozen":"Congelados","Household":"Hogar","Personal Care":"Cuidado personal","OTC & Wellness":"Bienestar","Baby":"Bebé"}
# real-art images for some items (name substring -> file)
ITEM_IMG = {"Tomato Paste":"tomato-paste","Whole Peeled Tomatoes":"new-whole-peeled-tomatoes","Diced Tomatoes":"new-diced-tomatoes","Black Beans":"new-black-beans","Red Kidney":"new-red-kidney","Pinto":"new-pinto","Mixed Vegetables":"new-mix-veg","Whole Kernel Corn":"new-sweet-corn","Peach Slices":"peach","Chunk Light Tuna in Oil":"tuna","Chunk Light Tuna in Water":"tuna","Mushroom":"mushrooms-whole","Baby Corn":"baby-corn"}

# ---------- recipes ----------
RECIPES = [
 dict(id="arroz", img="recipe-arroz", serves=4, mins=35, uses=["Black Beans","Long Grain White Rice","Chicken Bouillon"],
  en=dict(t="Arroz con frijoles negros", with_="Black beans · rice", ing=["2 cups ami long grain white rice","1 can ami black beans (15 oz), with liquid","1 small onion, finely chopped","2 cloves garlic, minced","1 ami chicken bouillon cube","2 tbsp ami vegetable oil","1 bay leaf · salt to taste","Lime wedges and chopped cilantro to serve"],
   steps=["Rinse the rice until the water runs clear and drain.","Heat the oil in a pot; cook the onion until soft (4 min), add the garlic for 1 min.","Add the rice and stir 2 min to coat. Add the beans with their liquid, the bouillon dissolved in 2½ cups hot water, and the bay leaf.","Bring to a boil, cover, lower the heat and cook 18 min until the liquid is absorbed.","Rest 5 min off the heat, fluff with a fork, and serve with lime and cilantro."]),
  es=dict(t="Arroz con frijoles negros", with_="Frijoles negros · arroz", ing=["2 tazas de arroz blanco ami","1 lata de frijoles negros ami (425 g), con su líquido","1 cebolla pequeña, picada fina","2 dientes de ajo, picados","1 cubito de caldo de pollo ami","2 cdas de aceite vegetal ami","1 hoja de laurel · sal al gusto","Limón y cilantro picado para servir"],
   steps=["Lava el arroz hasta que el agua salga clara y escúrrelo.","Calienta el aceite en una olla; sofríe la cebolla hasta que esté suave (4 min) y agrega el ajo 1 min.","Añade el arroz y revuelve 2 min. Agrega los frijoles con su líquido, el caldo disuelto en 2½ tazas de agua caliente y el laurel.","Lleva a hervor, tapa, baja el fuego y cocina 18 min hasta que absorba el líquido.","Deja reposar 5 min fuera del fuego, suelta con un tenedor y sirve con limón y cilantro."])),
 dict(id="pomodoro", img="new-life-cooking", serves=4, mins=25, uses=["Tomato Paste","Whole Peeled Tomatoes","Chunk Light Tuna in Oil","Spaghetti"],
  en=dict(t="Pasta al pomodoro with tuna", with_="Tomato paste · tuna · spaghetti", ing=["400 g ami spaghetti","2 tbsp ami tomato paste","1 can ami whole peeled tomatoes (400 g), crushed by hand","1 can ami chunk light tuna in oil (5 oz), drained","2 cloves garlic, sliced · 3 tbsp ami vegetable oil","Pinch of chili flakes · salt · fresh basil or parsley"],
   steps=["Cook the spaghetti in salted boiling water until al dente; save a cup of the water.","Warm the oil and garlic gently until fragrant; stir in the tomato paste and cook 1 min.","Add the crushed tomatoes and chili; simmer 10 min until thick. Season.","Fold in the tuna, then the drained pasta with a splash of pasta water.","Toss over the heat 1 min and finish with the herbs."]),
  es=dict(t="Pasta al pomodoro con atún", with_="Pasta de tomate · atún · espagueti", ing=["400 g de espagueti ami","2 cdas de pasta de tomate ami","1 lata de tomates pelados ami (400 g), triturados a mano","1 lata de atún en aceite ami (142 g), escurrido","2 dientes de ajo en láminas · 3 cdas de aceite vegetal ami","Una pizca de chile en hojuelas · sal · albahaca o perejil fresco"],
   steps=["Cocina el espagueti en agua hirviendo con sal hasta que esté al dente; reserva una taza del agua.","Calienta el aceite con el ajo a fuego suave hasta que aromatice; agrega la pasta de tomate y cocina 1 min.","Añade los tomates triturados y el chile; cocina 10 min hasta espesar. Sazona.","Incorpora el atún y luego la pasta escurrida con un chorrito del agua de cocción.","Saltea 1 min sobre el fuego y termina con las hierbas."])),
 dict(id="ensalada", img="recipe-ensalada", serves=6, mins=15, uses=["Whole Kernel Corn","Pinto Beans","Red Kidney Beans","Mayonnaise"],
  en=dict(t="Corn and bean salad", with_="Sweet corn · pinto beans · red kidney beans", ing=["1 can ami whole kernel corn (15 oz), drained","1 can ami pinto beans (15 oz), rinsed","1 can ami red kidney beans (15 oz), rinsed","1 red bell pepper and ½ red onion, diced","Juice of 2 limes · 3 tbsp ami vegetable oil","1 tsp cumin · salt · a handful of chopped cilantro"],
   steps=["Combine the corn, both beans, pepper and onion in a large bowl.","Whisk the lime juice, oil, cumin and salt; pour over and toss.","Rest 10 minutes so the flavors meet; add the cilantro just before serving.","Keeps 3 days in the fridge — better on day two."]),
  es=dict(t="Ensalada de maíz y frijoles", with_="Maíz dulce · frijoles pintos · frijoles rojos", ing=["1 lata de maíz dulce ami (425 g), escurrido","1 lata de frijoles pintos ami (425 g), enjuagados","1 lata de frijoles rojos ami (425 g), enjuagados","1 pimiento rojo y ½ cebolla morada, en cubos","Jugo de 2 limones · 3 cdas de aceite vegetal ami","1 cdta de comino · sal · un puñado de cilantro picado"],
   steps=["Mezcla el maíz, los dos frijoles, el pimiento y la cebolla en un bol grande.","Bate el jugo de limón, el aceite, el comino y la sal; vierte y revuelve.","Deja reposar 10 minutos para que se junten los sabores; agrega el cilantro justo antes de servir.","Dura 3 días en la nevera — al día siguiente está mejor."])),
 dict(id="batido", img="recipe-batido", serves=2, mins=5, uses=["Mango Nectar","Peach Slices","Evaporated Milk"],
  en=dict(t="Mango and peach smoothie", with_="Mango nectar · sliced peach", ing=["1 cup ami mango nectar, cold","½ can ami peach slices in syrup, drained","½ cup ami evaporated milk","1 cup ice · a squeeze of lime"],
   steps=["Put everything in a blender.","Blend until smooth and thick, about 40 seconds.","Pour over ice; add more nectar if you like it thinner."]),
  es=dict(t="Batido de mango y durazno", with_="Néctar de mango · duraznos", ing=["1 taza de néctar de mango ami, frío","½ lata de duraznos en almíbar ami, escurridos","½ taza de leche evaporada ami","1 taza de hielo · un chorrito de limón"],
   steps=["Pon todo en la licuadora.","Licúa hasta que quede espeso y suave, unos 40 segundos.","Sirve sobre hielo; agrega más néctar si lo prefieres más ligero."])),
 dict(id="sopa", img="recipe-sopa", serves=4, mins=30, uses=["Mixed Vegetables","Whole Peeled Tomatoes","Chicken Bouillon","Elbow Macaroni"],
  en=dict(t="Hearty vegetable soup", with_="Mixed vegetables · whole peeled tomatoes", ing=["1 can ami mixed vegetables (15 oz), with liquid","1 can ami whole peeled tomatoes (400 g), crushed","2 ami chicken bouillon cubes in 5 cups hot water","1 onion and 2 cloves garlic, chopped · 2 tbsp ami vegetable oil","½ cup ami elbow macaroni · salt, pepper, parsley"],
   steps=["Soften the onion and garlic in the oil, 5 min.","Add the tomatoes and the broth; bring to a simmer.","Add the macaroni and cook 8 min; add the mixed vegetables with their liquid and heat through 5 min.","Season, and serve with parsley and crusty bread."]),
  es=dict(t="Sopa de vegetales", with_="Mezcla de vegetales · tomates pelados", ing=["1 lata de mezcla de vegetales ami (425 g), con su líquido","1 lata de tomates pelados ami (400 g), triturados","2 cubitos de caldo de pollo ami en 5 tazas de agua caliente","1 cebolla y 2 dientes de ajo picados · 2 cdas de aceite vegetal ami","½ taza de coditos ami · sal, pimienta, perejil"],
   steps=["Sofríe la cebolla y el ajo en el aceite, 5 min.","Agrega los tomates y el caldo; lleva a hervor suave.","Añade los coditos y cocina 8 min; agrega los vegetales con su líquido y calienta 5 min más.","Sazona y sirve con perejil y pan."])),
 dict(id="champinones", img="gen-basket", serves=4, mins=15, uses=["Whole Button Mushrooms","Dark Soy Sauce"],
  en=dict(t="Garlic-soy button mushrooms", with_="Button mushrooms · soy sauce", ing=["2 cans ami whole button mushrooms (10 oz), drained","3 cloves garlic, sliced · 2 tbsp ami vegetable oil","1 tbsp ami dark soy sauce · 1 tsp sugar","Black pepper · chopped scallions"],
   steps=["Pat the mushrooms dry so they brown instead of steam.","Sear in hot oil 4 min without moving them; add the garlic 1 min.","Add the soy sauce and sugar; toss 1 min until glossy.","Finish with pepper and scallions. Great over rice or as a side."]),
  es=dict(t="Champiñones al ajo y soya", with_="Champiñones · salsa de soya", ing=["2 latas de champiñones enteros ami (284 g), escurridos","3 dientes de ajo en láminas · 2 cdas de aceite vegetal ami","1 cda de salsa de soya oscura ami · 1 cdta de azúcar","Pimienta negra · cebollín picado"],
   steps=["Seca bien los champiñones para que se doren en vez de hervir.","Séllalos en aceite caliente 4 min sin moverlos; agrega el ajo 1 min.","Añade la soya y el azúcar; saltea 1 min hasta que brillen.","Termina con pimienta y cebollín. Buenísimos sobre arroz o como acompañamiento."])),
]

MARKETS = [  # name, lat, lng, status(launching/next), note_en, note_es
 ("Miami · South Florida", 25.77,-80.19,"launching","Hispanic supermarkets and independents across Miami-Dade.","Supermercados hispanos e independientes en Miami-Dade."),
 ("Panamá", 8.98,-79.52,"launching","Our second home: American Foods has an office in Costa del Este.","Nuestra segunda casa: American Foods tiene oficina en Costa del Este."),
 ("República Dominicana", 18.47,-69.90,"launching","The beachhead market for the full program.","El mercado cabeza de playa para el programa completo."),
 ("Guatemala", 14.63,-90.51,"next","","" ),
 ("El Salvador", 13.69,-89.19,"next","",""),
 ("Honduras", 14.07,-87.19,"next","",""),
 ("Puerto Rico", 18.47,-66.11,"next","",""),
 ("Bahamas", 25.05,-77.35,"next","",""),
 ("Jamaica", 17.97,-76.79,"next","",""),
 ("Aruba", 12.52,-70.03,"next","",""),
 ("Trinidad & Tobago", 10.65,-61.52,"next","",""),
]

# ---------- helpers ----------
def esc(s): return html.escape(s, quote=True)
ARROW = '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CHECK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 4 4L19 6"/></svg>'
PIN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>'
SHIELD = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5l-8-3z"/><path d="m9 12 2 2 4-4"/></svg>'
def wm(white=False, root=""):
    return f'<a class="wm{" white" if white else ""}" href="{root}"><span class="word">am<span class="i">ı</span></span><span class="bar"></span><span class="sub">anytime</span></a>'

def head(t, title, desc, page, img="gen-basket"):
    lang=t["lang"]; root="/" if lang=="en" else "/es/"; other_root="/es/" if lang=="en" else "/"
    canon=f"https://amieveryday.com{root}{'' if page=='index.html' else page}"
    alt_en=f"https://amieveryday.com/{'' if page=='index.html' else page}"; alt_es=f"https://amieveryday.com/es/{'' if page=='index.html' else page}"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="en" href="{alt_en}"><link rel="alternate" hreflang="es" href="{alt_es}"><link rel="alternate" hreflang="x-default" href="{alt_en}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="https://amieveryday.com/img/{img}.webp"><meta property="og:type" content="website"><meta property="og:locale" content="{'en_US' if lang=='en' else 'es_419'}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap">
{'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">' if page=='where-to-buy.html' else ''}
<style>{CSS}</style>
</head>
<body><div class="boardwrap"><div class="frame">
"""

def chrome(t, page):
    lang=t["lang"]; root="/" if lang=="en" else "/es/"; other_root="/es/" if lang=="en" else "/"
    p = "" if page=="index.html" else page
    nav="".join(f'<a href="{root}{h}"{" class=\"on\"" if h==page else ""}>{esc(l)}</a>' for h,l in t["nav"])
    return f"""
      <div class="util"><div class="l"><span>{esc(t["util"])}</span></div><div class="r">
        <div class="lang"><a class="on" href="{root}{p}">{t["self_label"]}</a><a href="{other_root}{p}">{t["other_label"]}</a></div>
        <a href="{root}where-to-buy.html">{PIN}{esc(t["find"])}</a></div></div>
      <div class="nav" id="nav">{wm(root=root)}
        <button class="burger" aria-label="Menu" onclick="document.getElementById('nav').classList.toggle('open')"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
        <nav class="menu">{nav}</nav>
        <div class="nav-actions"><a class="icon-btn" href="{root}products.html" aria-label="Search"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg></a><a class="btn primary sm" href="{root}where-to-buy.html">{esc(t["find"])}</a></div>
      </div>
"""

def footer(t):
    lang=t["lang"]; root="/" if lang=="en" else "/es/"
    def links(items): return "".join(f'<li><a href="{root}{h}">{esc(l)}</a></li>' for h,l in items)
    return f"""
      <footer>
        <div class="fgrid">
          <div>{wm(True, root)}<p>{esc(t["f_tag"])}</p>
            <div class="social">
              <a href="{CONTACT["linkedin"]}" aria-label="LinkedIn" rel="noopener"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 9h4v12H4zM6 3a2 2 0 1 1 0 4 2 2 0 0 1 0-4zM10 9h4v2c1-1.5 2.5-2.5 4.5-2.5 3 0 4.5 2 4.5 5V21h-4v-6c0-1.5-.5-2.5-2-2.5S14 13.5 14 15v6h-4z"/></svg></a>
              <a href="#" aria-label="Instagram"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg></a>
              <a href="#" aria-label="Facebook"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8z"/></svg></a>
            </div></div>
          <div><h5>{esc(t["f_products"])}</h5><ul>{links(t["f_links_p"])}</ul></div>
          <div><h5>{esc(t["f_brand"])}</h5><ul>{links(t["f_links_b"])}</ul></div>
          <div><h5>{esc(t["f_partners"])}</h5><ul>{links(t["f_links_t"])}</ul></div>
          <div><h5>{esc(t["f_contact"])}</h5><ul><li><a href="mailto:{CONTACT["email"]}">{CONTACT["email"]}</a></li><li><a href="tel:+18778947675">{CONTACT["phone"]}</a></li><li>{esc(t["dist"])}</li><li>{esc(CONTACT["us_addr"])}</li></ul>
            <p><span class="seal">{SHIELD}{esc(t["seal"])}</span></p></div>
        </div>
        <div class="legal"><span>{esc(t["legal"])}</span><div class="links"><a href="#">{esc(t["privacy"])}</a><a href="#">{esc(t["terms"])}</a><a href="#">{esc(t["access"])}</a></div></div>
      </footer>
    </div></div>
    </body></html>"""

def pcard(img, cat, nm, es_line, sz, c, href=None, badge=None, new=None):
    inner=f'{f"<span class=\"new\">{esc(new)}</span>" if new else ""}{f"<img src=\"/img/new-badge-bestseller.webp\" alt=\"Best seller\" style=\"position:absolute;top:10px;right:10px;width:64px;z-index:2\">" if badge else ""}<div class="ph"><img src="/img/{img}.webp" alt="{esc(nm)}"></div><div class="meta"><span class="cat"><i></i>{esc(cat)}</span><span class="nm">{esc(nm)}</span><span class="es">{esc(es_line)}</span><span class="sz">{esc(sz)}</span></div>'
    tag="a" if href else "div"; h=f' href="{href}"' if href else ""
    return f'<{tag} class="pcard"{h} style="--c:var({c});position:relative">{inner}</{tag}>'

def aisle(root, dept_id, count, en, es, c, img=None, svg=None):
    art=f'<img class="art" src="/img/{img}.webp" alt="">' if img else f'<svg class="line" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{svg}</svg>'
    dark=" dark" if c=="--c-dairy" else ""
    return f'<a class="aisle{dark}" href="{root}products.html#{dept_id}" style="--c:var({c})"><span class="ct">{count} items</span>{art}<span class="n">{esc(en)}</span><span class="es">{esc(es)}</span></a>'

SVGS = dict(pantry='<path d="M12 40h24l-2-22H14l-2 22z"/><path d="M17 18v-4a7 7 0 0 1 14 0v4"/><path d="M14 26h20"/>', breakfast='<path d="M8 30c4-10 12-16 24-16 4 0 8 1 8 4 0 8-8 16-20 16-6 0-10-1-12-4z"/><path d="M14 30c6 0 14-4 20-12"/>', dairy='<path d="M17 6h14v7l5 8v19a2 2 0 0 1-2 2H14a2 2 0 0 1-2-2V21l5-8V6z"/><path d="M12 26h24"/>', frozen='<path d="M24 6v36M8 15l32 18M8 33l32-18"/><path d="m24 6-4 4m4-4 4 4M24 42l-4-4m4 4 4-4"/>', household='<path d="M14 20h20l-2 22H16l-2-22z"/><path d="M20 20v-6a4 4 0 0 1 8 0v6"/><path d="M12 20h24"/>', care='<rect x="16" y="14" width="16" height="28" rx="3"/><path d="M20 14v-5h8v5M16 22h16"/>')

def dept_counts():
    from collections import Counter
    c=Counter(i["dept"] for i in SKUS); return {d[0]: sum(c[x] for x in d[4]) for d in DEPTS}

# ---------- pages ----------
def page_index(t):
    lang=t["lang"]; root="/" if lang=="en" else "/es/"; es=lang=="es"; cnt=dept_counts()
    pillars="".join(f'<div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{p}</svg><b>{esc(b)}</b><span>{esc(s)}</span></div>' for (b,s),p in zip(t["pillars"],['<path d="M3 12h4l3-8 4 16 3-8h4"/>','<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>','<path d="M12 3l2.5 5 5.5.8-4 3.9.9 5.5L12 15.6 7.1 18.2l.9-5.5-4-3.9L9.5 8z"/>','<path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5l-8-3z"/><path d="m9 12 2 2 4-4"/>']))
    aisles="".join([
      aisle(root,"canned",cnt["canned"],*(("Canned Goods","Enlatados") if not es else ("Enlatados","Canned goods")),"--c-veg",img="new-mix-veg"),
      aisle(root,"pantry",cnt["pantry"],*(("Pantry","Arroz, pasta, aceites, condimentos") if not es else ("Despensa","Arroz, pasta, aceites, condimentos")),"--c-pantry",svg=SVGS["pantry"]),
      aisle(root,"breakfast",cnt["breakfast"],*(("Breakfast & Snacks","Desayuno y snacks") if not es else ("Desayuno y snacks","Breakfast & snacks")),"--c-corn",svg=SVGS["breakfast"]),
      aisle(root,"beverages",cnt["beverages"],*(("Beverages","Jugos, néctares y bebidas") if not es else ("Bebidas","Jugos, néctares y bebidas")),"--c-fruit",img="new-drink-tropical-1l"),
      aisle(root,"dairy",cnt["dairy"],*(("Dairy","Leche de larga vida") if not es else ("Lácteos","Leche de larga vida")),"--c-dairy",svg=SVGS["dairy"]),
      aisle(root,"frozen",cnt["frozen"],*(("Frozen","Congelados") if not es else ("Congelados","Frozen")),"--c-frozen",svg=SVGS["frozen"]),
      aisle(root,"household",cnt["household"],*(("Household","Hogar y limpieza") if not es else ("Hogar y limpieza","Household")),"--c-house",svg=SVGS["household"]),
      aisle(root,"care",cnt["care"],*(("Personal Care & Wellness","Cuidado personal") if not es else ("Cuidado personal","Personal care & wellness")),"--c-care",svg=SVGS["care"]),
    ])
    N=t["new"]; bev = "Beverages" if not es else "Bebidas"
    new4="".join([pcard("new-drink-tropical-1l",bev,"Tropical Fruit Drink" if not es else "Bebida de frutas tropicales","No added preservatives" if not es else "Sin conservantes añadidos","1 L","--c-fruit",new=N),
                  pcard("new-drink-mango-1l",bev,"Mango Fruit Drink" if not es else "Bebida sabor a mango","Pasteurized" if not es else "Pasteurizada","1 L","--c-fruit",new=N),
                  pcard("new-drink-orange-1l",bev,"Orange Fruit Drink" if not es else "Bebida sabor a naranja","Pasteurized" if not es else "Pasteurizada","1 L","--c-fruit",new=N),
                  pcard("new-drink-apple-200",bev,"Apple Fruit Drink" if not es else "Bebida sabor a manzana","Lunchbox size" if not es else "Tamaño lonchera","200 ml","--c-fruit",new=N)])
    core4="".join([pcard("tomato-paste","Tomato" if not es else "Tomate","Tomato Paste" if not es else "Pasta de tomate","Made with 100% tomatoes" if not es else "Hecha con 100% tomate","15 oz · 425 g","--c-tomato",href=root+"product-tomato-paste.html"),
                   pcard("new-black-beans","Beans" if not es else "Frijoles","Black Beans" if not es else "Frijoles negros","Good source of fiber" if not es else "Buena fuente de fibra","15 oz · 425 g","--c-veg",badge=True),
                   pcard("new-sweet-corn","Vegetables" if not es else "Vegetales","Sweet Corn" if not es else "Maíz dulce","Ready to eat" if not es else "Listo para comer","15.25 oz · 432 g","--c-corn"),
                   pcard("tuna","Seafood" if not es else "Pescados","Tuna Chunks" if not es else "Atún en trozos","In water or in oil" if not es else "En agua o en aceite","5 oz · 142 g","--c-sea")])
    r0,r1,r2,r3 = RECIPES[0],RECIPES[1],RECIPES[2],RECIPES[3]
    def rcard(r):
        L=r[lang]; return f'<a class="rc" href="{root}recipes.html#{r["id"]}"><img src="/img/{r["img"]}.webp" alt="{esc(L["t"])}"><div class="b"><span class="with">{esc(L["with_"])}</span><h3>{esc(L["t"])}</h3><span class="meta"><span>{r["mins"]} {t["mins"]}</span><span>{t["serves"] if "serves" in t else "Serves"} {r["serves"]}</span></span></div></a>'
    parts="".join(f'<li>{CHECK}{esc(x)}</li>' for x in t["part_list"])
    chips="".join(f'<span class="chip{" on" if i==0 else ""}">{esc(m[0])}</span>' for i,m in enumerate(MARKETS[:7]))
    body=f"""
      <div class="hero"><div><span class="eyebrow">{esc(t["hero_eyebrow"])}</span><h2>{t["hero_h"]}</h2><p class="es">{esc(t["hero_sub"])}</p><p>{esc(t["hero_p"])}</p>
        <div class="cta"><a class="btn primary" href="{root}products.html">{esc(t["cta1"])}</a><a class="btn ghost" href="{root}where-to-buy.html">{esc(t["cta2"])}</a></div></div>
        <div class="hero-photo"><img src="/img/gen-basket.webp" alt="A basket of ami anytime canned goods on a sunlit kitchen counter"><span class="tag"><i></i>{esc(t["tag"])}</span></div></div>
      <div class="range"><img src="/img/lineup.webp" alt="The ami anytime canned range"><p><b>{esc(t["range_b"])}</b>{esc(t["range_p"])}</p></div>
      <div class="pillars">{pillars}</div>
      <div class="sec"><div class="sec-head"><div><span class="eyebrow">{esc(t["aisle_eyebrow"])}</span><h3>{esc(t["aisle_h"])}</h3><div class="es">{esc(t["aisle_sub"])}</div></div><a href="{root}products.html">{esc(t["all149"])} {ARROW}</a></div><div class="aisles">{aisles}</div></div>
      <div class="sec"><div class="sec-head"><div><span class="eyebrow">{esc(t["new_eyebrow"])}</span><h3>{esc(t["new_h"])}</h3><div class="es">{esc(t["new_sub"])}</div></div><a href="{root}products.html#beverages">{esc(t["new_link"])} {ARROW}</a></div><div class="grid4">{new4}</div></div>
      <div class="sec"><div class="sec-head"><div><span class="eyebrow">{esc(t["core_eyebrow"])}</span><h3>{esc(t["core_h"])}</h3><div class="es">{esc(t["core_sub"])}</div></div><a href="{root}products.html#canned">{esc(t["core_link"])} {ARROW}</a></div><div class="grid4">{core4}</div></div>
      <div class="sec"><div class="sec-head"><div><span class="eyebrow">{esc(t["life_eyebrow"])}</span><h3>{esc(t["life_h"])}</h3><div class="es">{esc(t["life_sub"])}</div></div></div>
        <div class="life"><figure class="big"><img src="/img/gen-aisle.webp" alt=""><figcaption>{esc(t["life_caps"][0])}</figcaption></figure><figure><img src="/img/gen-shopper.webp" alt=""><figcaption>{esc(t["life_caps"][1])}</figcaption></figure><figure><img src="/img/new-life-cooking.webp" alt=""><figcaption>{esc(t["life_caps"][2])}</figcaption></figure></div></div>
      <div class="sec"><div class="sec-head"><div><span class="eyebrow">{esc(t["rec_eyebrow"])}</span><h3>{esc(t["rec_h"])}</h3><div class="es">{esc(t["rec_sub"])}</div></div><a href="{root}recipes.html">{esc(t["rec_link"])} {ARROW}</a></div>
        <div class="recipes"><div class="rcard month"><span class="eyebrow">{esc(t["rom"])}</span><h4>{esc(r0[lang]["t"])}</h4><p>{esc(r0[lang]["with_"])} · {r0["mins"]} {t["mins"]}</p><a class="btn white sm" href="{root}recipes.html#arroz">{esc(t["see"])}</a></div>{rcard(r1)}{rcard(r2)}{rcard(r3)}</div></div>
      <div class="partners"><div><span class="eyebrow">{esc(t["part_eyebrow"])}</span><h3>{esc(t["part_h"])}</h3><p>{esc(t["part_p"])}</p><ul>{parts}</ul><div class="cta"><a class="btn green" href="{root}partners.html">{esc(t["part_cta"])}</a><a class="btn white" href="{root}contact.html">{esc(t["part_cta2"])}</a></div></div>
        <img src="/img/new-banner-family.webp" alt="ami anytime — always with you" style="max-height:none;border-radius:12px 12px 0 0;object-fit:cover;aspect-ratio:16/8;align-self:end"></div>
      <div class="where"><div><span class="eyebrow">{esc(t["wtb_eyebrow"])}</span><h3>{esc(t["wtb_h"])}</h3><p>{esc(t["wtb_p"])}</p><div class="chips">{chips}</div><div class="cta" style="margin-top:16px"><a class="btn primary" href="{root}where-to-buy.html">{esc(t["wtb_cta"])}</a></div></div>
        <div><span class="eyebrow">{esc(t["news_eyebrow"])}</span><h3>{esc(t["news_h"])}</h3><p>{esc(t["news_p"])}</p><form class="field" action="mailto:{CONTACT["email"]}?subject=ami%20newsletter" method="post" enctype="text/plain"><input name="email" type="email" placeholder="{esc(t["news_ph"])}" required style="flex:1;height:48px;border:1px solid var(--line);border-radius:999px;padding:0 18px;font:inherit;font-size:14.5px;background:var(--paper-warm)"><button class="btn primary" type="submit">{esc(t["news_btn"])}</button></form></div></div>
"""
    return head(t, "ami anytime — " + ("Global flavors. Honest prices. Every day." if not es else "Sabores del mundo. Precios honestos. Todos los días."), t["hero_p"], "index.html") + chrome(t,"index.html") + body + footer(t)

def page_products(t):
    lang=t["lang"]; root="/" if lang=="en" else "/es/"; es=lang=="es"
    nav="".join(f'<a href="#{d[0]}" style="--c:var({d[3]})"><i></i>{esc(d[2] if es else d[1])}</a>' for d in DEPTS)
    out=[]
    for did,en,esn,c,sub in DEPTS:
        items=[i for i in SKUS if i["dept"] in sub]
        cards=[]
        for i in items:
            img=next((v for k,v in ITEM_IMG.items() if k.lower() in i["name"].lower()), None)
            icon=f'<img src="/img/{img}.webp" alt="" style="width:34px;height:34px;object-fit:contain;border-radius:0">' if img else '<i><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 8h12v11a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2z"/><path d="M8 8V5h8v3"/></svg></i>'
            soon="" if i["existing"] or i["phase"]=="Phase 1" else f' soon" data-soon="{esc(t["soon"])}'
            sub_es = SUB_ES.get(i["dept"], i["dept"])
            cards.append(f'<div class="item{soon}" style="--c:var({c})">{icon}<div><b>{esc(i["name"])}</b><small>{esc(str(i["size"]))} · {esc(sub_es if es else i["dept"])}</small></div></div>')
        out.append(f'<section class="dept" id="{did}"><div class="dept-head"><h3><i style="--c:var({c})"></i>{esc(esn if es else en)}</h3><span>{len(items)} {"productos" if es else "items"}</span></div><div class="items">{"".join(cards)}</div></section>')
    body=f"""
      <div class="page-head"><span class="eyebrow">{esc(t["nav"][1][1])}</span><h1>{esc(t["prod_h"])}</h1><div class="es">{esc(t["prod_sub"])}</div><p>{esc(t["prod_p"])}</p></div>
      <div class="deptnav">{nav}</div>
      <div class="catalog">{"".join(out)}</div>
"""
    return head(t, t["prod_title"], t["prod_p"], "products.html") + chrome(t,"products.html") + body + footer(t)

def page_pdp(t):
    lang=t["lang"]; root="/" if lang=="en" else "/es/"; es=lang=="es"; c=t["pdp_crumb"]
    claims=["Made with 100% tomatoes","No artificial flavors","No preservatives"] if not es else ["Hecha con 100% tomate","Sin sabores artificiales","Sin conservantes"]
    cl="".join(f'<li><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m8 12 3 3 5-6"/></svg>{esc(x)}</li>' for x in claims)
    rel="".join([pcard("new-diced-tomatoes","Tomato" if not es else "Tomate","Diced Tomatoes" if not es else "Tomates en trozos","Easy open","14.5 oz · 411 g","--c-tomato"),pcard("new-black-beans","Beans" if not es else "Frijoles","Black Beans" if not es else "Frijoles negros","","15 oz · 425 g","--c-veg"),pcard("new-pinto","Beans" if not es else "Frijoles","Pinto Beans" if not es else "Frijoles pintos","","15 oz · 425 g","--c-veg"),pcard("tuna","Seafood" if not es else "Pescados","Tuna Chunks" if not es else "Atún en trozos","","5 oz · 142 g","--c-sea")])
    body=f"""
      <div class="crumbs"><a href="{root}">{esc(c[0])}</a><span>/</span><a href="{root}products.html">{esc(c[1])}</a><span>/</span><a href="{root}products.html#canned">{esc(c[2])}</a><span>/</span><b>{esc(c[3])}</b></div>
      <div class="pdp" style="--c:var(--c-tomato)"><div><div class="stage"><img src="/img/tomato-paste.webp" alt="ami anytime tomato paste"></div>
        <div class="thumbs"><div class="on"><img src="/img/tomato-paste.webp" alt=""></div><div><img class="cover" src="/img/gen-basket.webp" alt=""></div><div><img class="cover" src="/img/new-life-cooking.webp" alt=""></div><div><img class="cover" src="/img/recipe-sopa.webp" alt=""></div></div></div>
        <div><span class="cat"><i></i>{"Tomato · Canned Goods" if not es else "Tomate · Enlatados"}</span><h2>{"Tomato Paste" if not es else "Pasta de tomate"}</h2><p class="es">{"Pasta de tomate" if not es else "Tomato paste"}</p>
          <div class="sz"><span class="on">15 oz · 425 g</span><span>6 oz · 170 g</span></div><ul class="claims">{cl}</ul>
          <div class="cta"><a class="btn primary" href="{root}where-to-buy.html">{esc(t["find"])}</a><a class="btn ghost" href="{root}contact.html">{"Spec sheet for buyers" if not es else "Ficha técnica para compradores"}</a></div>
          <div class="guar">{SHIELD.replace('width="22" height="22"','width="30" height="30"')}<div><b>{esc(t["seal"])}</b><span>{esc(t["guar_p"])}</span></div></div></div></div>
      <div class="tabs"><div class="th"><a href="#" class="on">{"Ingredients" if not es else "Ingredientes"}</a><a href="#">{"Nutrition" if not es else "Nutrición"}</a><a href="#">{"How to use" if not es else "Cómo usar"}</a></div>
        <div class="tb"><div><h6>{"Ingredients" if not es else "Ingredientes"}</h6><p>{"Tomatoes. That’s it — concentrated tomato paste with no added flavors or preservatives." if not es else "Tomate. Eso es todo — pasta de tomate concentrada sin sabores ni conservantes añadidos."}</p></div>
          <div><h6>{"Nutrition" if not es else "Nutrición"}</h6><p>{"Per 2 tbsp (33 g): about 30 kcal, 0 g fat, 6 g carbohydrate, 1 g protein. Full panel on pack." if not es else "Por 2 cdas (33 g): aprox. 30 kcal, 0 g grasa, 6 g carbohidratos, 1 g proteína. Tabla completa en el empaque."}</p></div>
          <div><h6>{"How to use" if not es else "Cómo usar"}</h6><p>{"Concentrated tomato for sofrito, stews, rice, sauces and soups. Two tablespoons deepen any tomato base; refrigerate the rest in a covered container." if not es else "Tomate concentrado para sofrito, guisos, arroz, salsas y sopas. Dos cucharadas dan cuerpo a cualquier base de tomate; refrigera el resto tapado."}</p></div></div></div>
      <div class="related"><div class="sec-head"><div><span class="eyebrow">{"Goes well with" if not es else "Combina con"}</span><h3>{"From the same aisle" if not es else "Del mismo pasillo"}</h3></div><a href="{root}products.html#canned">{esc(t["core_link"])} {ARROW}</a></div><div class="grid4">{rel}</div></div>
"""
    return head(t, ("Tomato Paste" if not es else "Pasta de tomate")+" · ami anytime", claims[0], "product-tomato-paste.html", img="tomato-paste") + chrome(t,"products.html") + body + footer(t)

def page_recipes(t):
    lang=t["lang"]; root="/" if lang=="en" else "/es/"
    cards="".join(f'<a class="rc" href="#{r["id"]}"><img src="/img/{r["img"]}.webp" alt="{esc(r[lang]["t"])}"><div class="b"><span class="with">{esc(r[lang]["with_"])}</span><h3>{esc(r[lang]["t"])}</h3><span class="meta"><span>{r["mins"]} {t["mins"]}</span><span>{t["serves"]} {r["serves"]}</span></span></div></a>' for r in RECIPES)
    full=[]
    for r in RECIPES:
        L=r[lang]
        full.append(f'<article class="recipe" id="{r["id"]}"><img src="/img/{r["img"]}.webp" alt="{esc(L["t"])}"><div><span class="eyebrow">{esc(L["with_"])}</span><h2>{esc(L["t"])}</h2><div class="meta"><span>{t["serves"]} {r["serves"]}</span><span>{r["mins"]} {t["mins"]}</span></div>'
                    f'<h4>{esc(t["ingredients"])}</h4><ul>{"".join(f"<li>{esc(x)}</li>" for x in L["ing"])}</ul><h4>{esc(t["method"])}</h4><ol>{"".join(f"<li>{esc(x)}</li>" for x in L["steps"])}</ol>'
                    f'<div class="uses">{"".join(f"<span>ami {esc(u)}</span>" for u in r["uses"])}</div></div></article><div class="rsep"></div>')
    body=f'<div class="page-head"><span class="eyebrow">{esc(t["rec_eyebrow"])}</span><h1>{esc(t["recp_h"])}</h1><div class="es">{esc(t["recp_sub"])}</div><p>{esc(t["recp_p"])}</p></div><div class="rgrid">{cards}</div>{"".join(full)}'
    return head(t, t["rec_title"], t["recp_p"], "recipes.html", img="recipe-arroz") + chrome(t,"recipes.html") + body + footer(t)

def page_wtb(t):
    lang=t["lang"]; root="/" if lang=="en" else "/es/"; es=lang=="es"
    cards="".join(f'<div class="mk"><b>{esc(m[0])}</b><span class="st{"" if m[3]=="launching" else " next"}">{esc(t["launching"] if m[3]=="launching" else t["next"])}</span><p>{esc((m[5] if es else m[4]) or ("Ask for ami anytime at your local supermarket." if not es else "Pide ami anytime en tu supermercado."))}</p></div>' for m in MARKETS)
    markers=json.dumps([[m[0],m[1],m[2],m[3]] for m in MARKETS])
    lab_l=esc(t["launching"]); lab_n=esc(t["next"])
    body=f"""
      <div class="page-head"><span class="eyebrow">{esc(t["wtb_eyebrow"])}</span><h1>{esc(t["wtbp_h"])}</h1><div class="es">{esc(t["wtbp_sub"])}</div><p>{esc(t["wtbp_p"])}</p></div>
      <div id="map" role="img" aria-label="Map of ami anytime markets"></div>
      <div class="markets">{cards}</div>
      <div class="two"><div class="card"><h3>{esc(t["tell"])}</h3><form class="form" action="mailto:{CONTACT["email"]}?subject=Where%20I%20shop" method="post" enctype="text/plain"><label>{esc(t["country"])}<input name="country" required></label><label>{"Supermarket" if not es else "Supermercado"}<input name="store" required></label><label>{esc(t["email"])}<input name="email" type="email"></label><button class="btn primary" type="submit">{esc(t["send"])}</button></form></div>
        <div class="stack"><img src="/img/gen-aisle.webp" alt=""><div class="card"><h3>{esc(t["part_eyebrow"])}</h3><ul><li>{CHECK}{esc(t["part_list"][0])}</li><li>{CHECK}{esc(t["part_list"][1])}</li></ul><p style="margin:14px 0 0"><a class="btn ghost sm" href="{root}partners.html">{esc(t["part_cta"])} </a></p></div></div></div>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
      <script>
      (function(){{
        var map=L.map('map',{{scrollWheelZoom:false}}).setView([16.5,-78],5);
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png',{{attribution:'&copy; OpenStreetMap contributors &copy; CARTO',maxZoom:12}}).addTo(map);
        var M={markers};
        M.forEach(function(m){{
          var launching=m[3]==='launching';
          var mk=L.circleMarker([m[1],m[2]],{{radius:launching?11:8,color:'#fff',weight:2,fillColor:launching?'#8FB944':'#253768',fillOpacity:.95}}).addTo(map);
          mk.bindPopup('<b style="font-family:Nunito,sans-serif;font-size:15px;color:#253768">'+m[0]+'</b><br><span style="font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:'+(launching?'#5F8F2A':'#7C8592')+';font-weight:700">'+(launching?'{lab_l}':'{lab_n}')+'</span>');
        }});
      }})();
      </script>
"""
    return head(t, t["wtb_title"], t["wtbp_p"], "where-to-buy.html", img="gen-aisle") + chrome(t,"where-to-buy.html") + body + footer(t)

def page_about(t):
    lang=t["lang"]; root="/" if lang=="en" else "/es/"
    prose="".join(f'<h3>{esc(h)}</h3><p>{esc(p)}</p>' for h,p in t["about_body"])
    vals="".join(f'<div><b>{esc(b)}</b><span>{esc(s)}</span></div>' for b,s in t["values"])
    body=f"""
      <div class="page-head"><span class="eyebrow">{esc(t["nav"][0][1])}</span><h1>{esc(t["about_h"])}</h1><div class="es">{esc(t["about_sub"])}</div><p>{esc(t["about_p"])}</p></div>
      <div class="banner" style="margin-top:24px"><img src="/img/new-banner-family.webp" alt="ami anytime — always with you"></div>
      <div class="two"><div class="prose">{prose}<h3 id="guarantee">{esc(t["guar_h"])}</h3><p>{esc(t["guar_p"])}</p><p><span class="seal">{SHIELD}{esc(t["seal"])}</span></p></div>
        <div class="stack"><img src="/img/lineup.webp" alt="The ami anytime range"><div class="card"><h3>{esc(t["values_h"])}</h3><div class="vals">{vals}</div></div><div class="card"><h3>American Foods International</h3><ul><li>{CHECK}{esc(CONTACT["us_addr"])}</li><li>{CHECK}{esc(CONTACT["pa_addr"])}</li><li>{CHECK}<a href="{root}contact.html">{esc(t["f_contact"])}</a></li></ul></div></div></div>
"""
    return head(t, t["about_title"], t["about_p"], "about.html", img="new-banner-family") + chrome(t,"about.html") + body + footer(t)

def page_partners(t):
    lang=t["lang"]; root="/" if lang=="en" else "/es/"; es=lang=="es"
    steps="".join(f'<div class="step"><b>{n}</b><h4>{esc(h)}</h4><p>{esc(p)}</p></div>' for n,h,p in t["steps"])
    parts="".join(f'<li>{CHECK}{esc(x)}</li>' for x in t["part_list"])
    body=f"""
      <div class="page-head"><span class="eyebrow">{esc(t["part_eyebrow"])}</span><h1>{esc(t["partn_h"])}</h1><div class="es">{esc(t["partn_sub"])}</div><p>{esc(t["partn_p"])}</p></div>
      <div class="banner" style="margin-top:24px"><img src="/img/gen-aisle.webp" alt=""></div>
      <div class="sec" id="program"><div class="sec-head"><div><span class="eyebrow">{"How it works" if not es else "Cómo funciona"}</span><h3>{"From license to shelf in three steps" if not es else "De la licencia al anaquel en tres pasos"}</h3></div></div></div>
      <div class="steps">{steps}</div>
      <div class="two"><div class="card"><h3>{"What the program includes" if not es else "Qué incluye el programa"}</h3><ul>{parts}<li>{CHECK}{"149 products across 21 departments — canned, pantry, beverages, dairy, frozen, household, personal care" if not es else "149 productos en 21 departamentos — enlatados, despensa, bebidas, lácteos, congelados, hogar, cuidado personal"}</li><li>{CHECK}{"Weekly price benchmarks against the value shelf in your market" if not es else "Comparativos de precio semanales contra el anaquel de valor de tu mercado"}</li></ul></div>
        <div class="card"><h3>{esc(t["partn_form_h"])}</h3><p style="margin:0 0 14px;color:var(--ink-2);font-size:14.5px">{esc(t["partn_form_p"])}</p><form class="form" action="mailto:{CONTACT["email"]}?subject=ami%20partner%20inquiry" method="post" enctype="text/plain"><label>{esc(t["company"])}<input name="company" required></label><label>{esc(t["country"])}<input name="country" required></label><label>{esc(t["name"])}<input name="name" required></label><label>{esc(t["email"])}<input name="email" type="email" required></label><label>{esc(t["message"])}<textarea name="message"></textarea></label><button class="btn green" type="submit">{esc(t["send"])}</button></form></div></div>
"""
    return head(t, t["partn_title"], t["partn_p"], "partners.html", img="gen-aisle") + chrome(t,"partners.html") + body + footer(t)

def page_contact(t):
    lang=t["lang"]; root="/" if lang=="en" else "/es/"; es=lang=="es"
    topics="".join(f'<option>{esc(x)}</option>' for x in t["topics"])
    body=f"""
      <div class="page-head"><span class="eyebrow">{esc(t["nav"][5][1])}</span><h1>{esc(t["contact_h"])}</h1><div class="es">{esc(t["contact_sub"])}</div><p>{esc(t["contact_p"])}</p></div>
      <div class="two"><div class="stack">
          <div class="card"><h3>American Foods International Inc</h3><ul>
            <li>{PIN}<span><b>{esc(t["us_office"])}</b><br>{esc(CONTACT["us_addr"])}</span></li>
            <li>{PIN}<span><b>{esc(t["pa_office"])}</b><br>{esc(CONTACT["pa_addr"])}</span></li>
            <li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg><span><b>{esc(t["phone"])}</b><br><a href="tel:+18778947675">{CONTACT["phone"]}</a> (USA) · <a href="tel:+5073107576">{CONTACT["pa_phone"]}</a> (Panamá)</span></li>
            <li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg><span><b>{esc(t["mail"])}</b><br><a href="mailto:{CONTACT["email"]}">{CONTACT["email"]}</a></span></li>
            <li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg><span><b>{esc(t["hours"])}</b><br>{esc(t["hours_v"])}</span></li>
            <li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 9h4v12H4zM6 3a2 2 0 1 1 0 4 2 2 0 0 1 0-4zM10 9h4v2c1-1.5 2.5-2.5 4.5-2.5 3 0 4.5 2 4.5 5V21h-4v-6c0-1.5-.5-2.5-2-2.5S14 13.5 14 15v6h-4z"/></svg><span><b>{esc(t["social"])}</b><br><a href="{CONTACT["linkedin"]}" rel="noopener">LinkedIn · American Foods</a></span></li></ul></div>
          <img src="/img/new-life-kid.webp" alt="" style="aspect-ratio:3/2"></div>
        <div class="card"><h3>{esc(t["form_h"])}</h3><form class="form" action="mailto:{CONTACT["email"]}?subject=ami%20anytime%20contact" method="post" enctype="text/plain"><label>{esc(t["topic"])}<select name="topic">{topics}</select></label><label>{esc(t["name"])}<input name="name" required></label><label>{esc(t["email"])}<input name="email" type="email" required></label><label>{esc(t["country"])}<input name="country"></label><label>{esc(t["message"])}<textarea name="message" required></textarea></label><button class="btn primary" type="submit">{esc(t["send"])}</button></form></div></div>
"""
    return head(t, t["contact_title"], t["contact_p"], "contact.html", img="new-life-kid") + chrome(t,"contact.html") + body + footer(t)

# ---------- build ----------
PAGES = {"index.html":page_index,"products.html":page_products,"product-tomato-paste.html":page_pdp,"recipes.html":page_recipes,"where-to-buy.html":page_wtb,"about.html":page_about,"partners.html":page_partners,"contact.html":page_contact}
for lang,t in T.items():
    for name,fn in PAGES.items():
        out=os.path.join(SITE, "es" if lang=="es" else "", name)
        open(out,"w").write(fn(t))
# sitemap
urls=[]
for name in PAGES:
    p="" if name=="index.html" else name
    urls.append(f"<url><loc>https://amieveryday.com/{p}</loc></url><url><loc>https://amieveryday.com/es/{p}</loc></url>")
open(os.path.join(SITE,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"\n".join(urls)+"\n</urlset>\n")
print("built", len(PAGES)*2, "pages")
