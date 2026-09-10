# ami anytime top-standard redesign — 2026-09-09

## Outcome

The site was rebuilt as a shopper-first modern pantry system. It now answers five questions in order: what ami is, which real products are shown, what to cook, whether confirmed stores are published, and where a retailer should go.

## Review team

- Commercial and brand: audience hierarchy, proposition, benchmark transfer, and conversion flow.
- Bilingual content: evidence-safe English and neutral Latin American Spanish, one language per page, and routed customer intent.
- Technical and UX QA: image/source truth, responsive behavior, accessibility, progressive enhancement, metadata, and publishing checks.

## Benchmark lessons applied

- Essential Everyday and Goya: connect products, recipes, and location instead of presenting separate content silos.
- ALDI and Trader Joe's: curate the useful range before exposing breadth.
- Graza and Fishwife: show the product and its use before telling a long corporate story.
- UNFI: keep the retailer decision path distinct from the shopper journey.

The visual language remains original to ami: navy masterbrand, green utility line, aisle colors, exact packshots on clean stages, and warm meal photography.

## Problems removed

- Obsolete AI renders with old green/red/yellow packages.
- A 178-card catalogue containing 139 placeholders and contradictory sizes.
- Repeated homepage sections that made the same product and retailer points.
- Unsupported price, quality, availability, guarantee, exclusivity, certification, and response-time claims.
- Empty map, newsletter capture, placeholder legal links, and forms without an approved backend.
- Mixed-language helper copy inside English and Spanish pages.

## New architecture

Shopper: Home → Products → Product detail or Recipe → Where to buy.

Retailer: Home → For retailers → market/category conversation.

Global navigation: Products, Recipes, Where to buy, Our brand, For retailers, EN/ES. Contact and product support live in the footer.

## Product truth

The public catalogue is limited to 29 current-art products. Individual packshots govern the size displayed next to each image. A remaining owner reconciliation is recorded in `HANDOFF.md`: current tuna artwork shows 140 g while an older catalogue summary said 170 g. The website shows 140 g so the on-page text and art do not contradict one another.

## Acceptance standard

- One clear H1 and one language per page.
- Exact referenced images, with dimensions; no obsolete `gen-*` packaging art.
- Product search and category filters work in both languages and ignore accents.
- Mobile navigation is keyboard operable and Escape returns focus.
- Content is visible when JavaScript fails or motion is reduced.
- Every bilingual page has canonical and EN/ES/x-default hreflang metadata.
- JSON-LD parses, all local links and images resolve, and the custom-domain `CNAME` is unchanged.
- No horizontal overflow at 360, 700, 1100, or 1360 CSS pixels.
