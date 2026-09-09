# amianytime.com — UX & brand review (2026-09-09)

Basis: live HTML/CSS, EN + ES, all 8 pages (live = clone, byte-identical); no screenshots.

## Executive summary

1. It looks like a real brand: clean type, consistent aisle colours, 29 good packshots, full EN/ES, a retailer path most own-brand sites lack.
2. It doesn't yet *work* for a shopper: "Where to buy" has 11 country pins and zero stores; every form is a `mailto:` that fails on most phones.
3. The home page never says what ami is in one line; "always with you" is only image alt text.
4. Products shows 178 cards — 29 real, 100 grey "coming soon" — with packshots reused for the wrong items. Reads unfinished, not big.
5. Privacy/Terms go to `#` while we collect emails; nothing backs "lowest price / best-known brands / no questions".
6. **Score: 6/10.** Movers: (a) real stores + forms that submit; (b) headline and products page built around the 29 real items.

## Benchmark (1–5)

| Criterion | Essential Everyday | Aldi US | Trader Joe's | Great Value | **ami** |
|---|---|---|---|---|---|
| Clarity of promise | 5 | 4 | 3 | 3 | **3** |
| Product browse | 3 | 5 | 5 | 4 | **2** |
| Where-to-buy | 4 | 5 | 5 | 5 | **1** |
| Recipes / content | 3 | 4 | 5 | 2 | **3** |
| Bilingual | 1 | 1 | 1 | 2 | **4** |
| Partner / B2B path | 2 | 1 | 1 | 1 | **4** |
| **Total /30** | 18 | 20 | 20 | 17 | **17** |

## Findings by impact

| # | Finding | Where | Recommendation | Effort |
|---|---|---|---|---|
| 1 | No stores; Miami blurb ("Hispanic supermarkets and independents") contradicts "one partner per country". | where-to-buy, home | Pre-launch block + email capture now; retailer logo + store list when signed. | M |
| 2 | All 5 forms are `mailto:` + `method=post`; silent failure on mobile. | all form pages | Post to n8n webhook (already in stack); success state; route by topic. | S |
| 3 | Hero generic, an H2 (no H1 on home), Spanish subline on EN, AI render (`gen-basket`). | index | New H1/subhead (below); real photo with product in frame. | S |
| 4 | 178 cards, 100 grey; aisle rail hidden ≤1100px; chips/sort inert (no JS); four size formats. | products | **On shelf now** (29, each with a mini detail page) + **Full program** as a department index (aisle, count, 3 examples). One format `425 g · 15 oz`. Working filters or none. | M |
| 5 | Wrong art: Refried Black Beans → whole beans; Frozen Veg/Corn → cans; mushroom recipe → AI basket. | products, recipes | Remove; never substitute. | S |
| 6 | Claims drift: "select few" / "one" / "single" partner; "21 departments" vs 8 aisles; "best-known brands"; "no questions". | home, about, partners | One partner sentence (below); verifiable claims only; guarantee = "replace or refund". | S |
| 7 | Dead ends: Privacy/Terms/Accessibility + 2 social icons = `#`; "Spec sheets" → contact; PDP tabs `#`; PDP EN/ES toggle → /products.html. | footer, PDP | Publish Privacy + Terms; drop dead icons; real spec-sheet PDF; fix toggle. | S |
| 8 | 5 of 6 recipes need products not in the launch range (rice, bouillon, oil, pasta, mayo, milk, nectar). | recipes | Rewrite around launch SKUs + staples. | S |
| 9 | ES: 149 program names untranslated; anglicisms ("Claims reales", "retailers", "cabeza de playa"); regionalisms ("tajados", "Mazorcas baby"); "soja"/"soya"; two drink names. | es/* | Translate all; "Promesas reales", "cadenas", "mercado de entrada", "en láminas", "maíz baby", "soya". | S |
| 10 | Bilingual sublines on both versions. | all | One language per page. | S |
| 11 | No trust signals: certifications, co-packer audits, partner logos, press. | about, partners | "How we qualify a producer" block with real certs. | M |
| 12 | Craft: no image `width/height`, hero not preloaded, lineup.webp 292 KB; 30+ font sizes; wordmark's dotless ı reads "amıanytime" to screen readers. | all | Image dimensions + `fetchpriority`; 8-step type scale; SVG wordmark + `aria-label`. | S |

## Do now (top 5)

**1. Hero (H1; drop the Spanish line on EN).** Pick one:

- EN **Always with you. Never over budget.** / ami anytime is the own brand your supermarket trusts — tomatoes, beans, tuna, corn, drinks — priced for every week of the month.
  ES **Siempre contigo. Nunca fuera de presupuesto.** / ami anytime es la marca propia en la que confía tu supermercado — tomate, frijoles, atún, maíz, bebidas — con precios para todas las semanas del mes.
- EN **Priced to be the lowest on the shelf. Made not to taste like it.** / One navy band on every pack, from the best producer in each category.
  ES **Con el precio más bajo del anaquel. Sin que se note en el sabor.** / Una banda azul en cada empaque, del mejor productor de cada categoría.
- EN **Good food. Fair price. Every aisle.** / From beans to fruit drinks, ami stretches the basket without shrinking dinner. Always with you.
  ES **Buena comida. Precio justo. En cada pasillo.** / De los frijoles a los jugos, ami rinde la canasta sin achicar la cena. Siempre contigo.

CTAs: **See what's on shelf / Ver lo que ya está en anaquel** and **For retailers / Para supermercados**.

**2. Products intro.**
EN: "**On shelf now — 29 products.** What you can find today. **The full program — 149 products, 8 aisles** — arrives in waves; here is what's coming."
ES: "**Ya en anaquel — 29 productos.** Lo que encuentras hoy. **El programa completo — 149 productos, 8 pasillos** — llega por etapas; esto es lo que viene."

**3. Where to buy (pre-launch).**
EN: "We launch with one retail partner per country and publish the store list the week ami reaches the shelf. Leave your email — we'll tell you first."
ES: "Lanzamos con un socio por país y publicamos la lista de tiendas la semana en que ami llega al anaquel. Déjanos tu correo — te avisamos primero."

**4. Forms.** Webhook, not `mailto:`. Success: EN "Thanks — we reply within two business days." ES "Gracias — respondemos en dos días hábiles." Consent: EN "One email a month. Unsubscribe anytime." ES "Un correo al mes. Cancela cuando quieras."

**5. One partner sentence everywhere.**
EN: "ami is licensed to one retail partner per country, category by category, with price shielding written into the license."
ES: "ami se licencia a un solo socio comercial por país, categoría por categoría, con protección de precio escrita en la licencia."
Same day: remove the four mismatched images, fix the PDP toggle, "Claims reales" → "Promesas reales".
