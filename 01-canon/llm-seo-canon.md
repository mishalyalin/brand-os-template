# LLM SEO and Content Engineering Canon for the brand

Owner: Brand voice panel. Status: canonical reference. Version: llm-seo-canon-v1.0.0. Last updated: 2026-05-20.

Compressed reference for the four LLM-era SEO pillars that survived the April 2026 Google core update, the content-engineering operating pattern that the top-10% of SaaS / DTC sites use to scale evidence-backed copy, and the ranking-collapse anti-patterns that died in the same update window. Each principle covers the canon reference, a one-line definition, the funnel stages where it lands hardest for the brand, and the places where it should NOT be used.

## The thesis in one paragraph

April 2026 Google reshaped the SERP - 38.8% of Top-10 pages fell out of the index entirely, 90.7% of URLs in the Top-10 changed positions, and SaaS / tech blogs that combined proprietary data + documentation + free tools with behavioural signals grew 22% while skyscraper rewrites and pure aggregator plays collapsed. The brands that survived shared one operating pattern - content engineering - the discipline of building systems that produce, refresh, and distribute content at scale without losing voice. the brand's Brand OS is content engineering by construction (the Brain is the retrieval layer, this canon is the spec, the Wall-1 / Wall-2 hygiene checks are the constraint layer). The four pillars below are the strategic moves that pour traffic into that system; the content-engineering pattern is the factory that processes it.

### 1. Topical Authority (Semantic SEO)

**Canon reference:** ESA Digital _How to Get Cited by AI in 2026_ (Dennis Lazard, May 2026); RASK AI case study (50% of sign-ups from AI search, 12,100 AI LLM traffic per month); AITHOR case study (50,000 AI LLM traffic per month, 5,000 AI citations per month); Eugene Schwartz _Breakthrough Advertising_ (1966) - awareness-stages framework underneath the topical-authority mechanic.

**One-line definition:** Win the LLM's mental map of a single topic cluster by being the source of breadth + depth across every adjacent question the customer might ask.

**Where to use in the brand funnel:** Build the "Make healthy food taste good" cluster as a content cathedral. Pillar page (the homepage) anchors the cluster. Sub-pillar pages cover the six content vectors (bodybuilder plate, bland-plate rescue, sweet pairing, avocado moment, salad-bar fix, chicken-and-rice rescue) as deep sub-clusters. Recipe pages stack underneath - one recipe per typical meal occasion, each anchored to one content vector, each citing primary sources (Eurofins ICP-MS panel, the founder's lived Ayurvedic-eating period). Multilingual: UK English at launch, then DE / FR / NL as EU shipping lane spins up. Editorial register throughout (Aesop / Le Labo cadence). Founder credential (the founder + a prior venture + a prior product) cited on About page + cross-linked from every cluster anchor.

**Where NOT to use:** Skyscraper-style "everything you need to know about salt" listicles - April 2026 Gemini 4.0 flags semantically perfect rewrites as derivative and demotes them out of the Top-100. Anything that competes on word count instead of substance. Generic recipe pages that could come from any food site without the brand's per-meal anchor.

### 2. Programmatic SEO

**Canon reference:** ESA Digital case studies - RASK AI tools matrix (language × voice clone, document × translator, video / audio × translator: 12,100 traffic per month per page family); Lovable Templates; Webflow Integration pages; Augment Code Tools.

**One-line definition:** Generate pages by formula - one templated page per cell of an `<input> × <output>` matrix - so the LLM can match a long-tail query directly to a destination page that answers it precisely.

**Where to use in the brand funnel:** The the brand matrices are constrained by Wall 2 (no competitor comparison pages, no category-vs-category pages). What survives Wall 2: (a) protein × meal-occasion recipe matrix - "the brand for grilled chicken thigh dinner", "the brand on poached eggs at breakfast", "the brand on smashed avocado at brunch"; (b) diet × use-case pages - "the brand for bodybuilder cutting protocol", "the brand for Ayurvedic limited-set vegan plate"; (c) free-tool pages with behavioural signals - per-meal sodium tracker, flavour-balance score calculator, salt-on-fruit pairing recommender. The free-tool pages double as the proprietary-data layer the LLMs reward.

**Where NOT to use:** Anything that violates Wall 2 - "the brand vs Maldon" pages, "the brand vs Tabasco" pages, "best salt brand" listicles seeded from our domain. We accept being placed in third-party best-of lists via Pillar 3 but never publish category comparison from our own domain. Per-product cost comparison pages also banned per the positioning lock - we anchor against per-meal cost only.

### 3. Brand SEO

**Canon reference:** ESA Digital case studies - Marketplace UGC Music Marketplace (400 AI citations per month, 250,000 AI traffic per month); Enterprise CRM case (500 AI citations per month, 80% AI traffic share US). Per the same source: sites with high direct / brand traffic share lost 1.5x less visibility in the April 2026 update than sites without.

**One-line definition:** Get the brand name to appear in third-party top / best lists, guest posts, AI Overview citations, podcast transcripts, and structured data so the LLM treats the brand as a known entity with a defined position when answering customer queries.

**Where to use in the brand funnel:** Build inbound brand mentions in three layers: (a) editorial mentions in cooking blogs, fitness blogs, nutrition newsletters, behavioural-economics newsletters - the founder can appear as a guest writer leveraging the a prior venture credential; (b) AI Overview citations - publish structured-data PDP + structured-data founder credential + structured-data quality-report PDF so LLMs have crawlable facts; (c) podcast appearances and editorial profiles for the founder. Founder credential is the authority anchor - amortise it across as many media surfaces as schedule allows. When the customer asks ChatGPT "what's a good seasoning blend for high-protein meal prep that isn't loaded with junk?", the brand needs to be in the answer.

**Where NOT to use:** Paid placements that look like editorial without disclosure (Wall-1 adjacent regulatory issue). Sponsorship of category-comparison content from our side (Wall-2 violation even if the publisher writes it). Vanity mentions in publications outside the ICP register - if the target reader of the publication is not 30-55 active urban UK / EU / US strength-trained adult, the mention has zero ICP value and dilutes the brand-mention signal.

### 4. Regular Page Refresh

**Canon reference:** ESA Digital RASK AI + Enterprise CRM case studies - both flagged "regular page refresh: regular updates and maintenance of the main conversion pages" as one of four winning strategies. Per the March 2026 SE Ranking analysis, 80% of content in the Top-3 was changed during the update period - the brands that maintained Top-10 were the ones already refreshing on rolling cadence.

**One-line definition:** Conversion pages, pillar pages, and high-value programmatic pages are refreshed on a calendarized cadence - the LLM treats freshness + active maintenance as a quality signal.

**Where to use in the brand funnel:** Quarterly refresh of the four high-stakes surfaces - homepage hero, PDP main, About / founder section, welcome-flow email sequence. Monthly refresh of programmatic pages (Pillar 2 matrices) as new recipes / new use cases / new evidence emerge. Annual refresh of the canonical foundation files (positioning.md, brand-voice.md) only when the founder makes a positioning-level decision documented in `06-decisions/`. Maintenance log in `06-decisions/refreshes/YYYY-MM-DD-<surface>.md` so the refresh history itself becomes a freshness signal for LLM crawlers.

**Where NOT to use:** Cosmetic-only refreshes that do not change substance - LLMs are getting better at detecting this and treat it as a negative signal. Refreshing immediately after a the founder-level positioning lock - let the positioning rest for 6+ weeks before the next refresh to avoid the "uncertain brand" signal.

### 5. Content Engineering

**Canon reference:** AirOps blog _Content Engineering_ (2026); GrowthX overview deck (2026); n8n node-based workflow patterns; ESA Digital observation that the top-10% of surviving sites all use this operating pattern.

**One-line definition:** Content engineering is the practice of building systems that help teams create, update, reuse, and distribute content at scale without losing accuracy, consistency, or voice.

**Where to use in the brand funnel:** The Brand OS itself IS the content engineering platform - the Brain CLI is the retrieval layer (RAG over positioning + cocktails + canon + Vault rows); the canon files are the spec; the hygiene vocab + Wall-1 / Wall-2 scan + the seven hard rules are the constraint layer; the GitHub Actions (brand-voice-check, claims-trace) are the CI quality gate; the decision records in `06-decisions/` are the institutional memory; when a Claude session loads the repo, CLAUDE.md is the plug-in contract; the Brain answers any tactic query in one call. For new content sprints - (a) define the spec in plain English in a Google Doc, (b) analyse where person-hours go now (research, brief, writing, refresh), (c) ask Claude or ChatGPT to draft the workflow spec, (d) implement as either a Brain-prompted Claude session for low-volume / high-stakes work, or as a node-based n8n / Make workflow for programmatic-SEO scale. The Brand OS is the constraint contract every workflow passes through before publication.

**Where NOT to use:** Full automation without human review on high-stakes surfaces (hero, PDP, founder section, regulatory copy). Generative-AI-only content without proprietary data - collapses in the April 2026 ranking model. Workflows that bypass the Brain query step - any copy generated without first checking the Brain is by construction not content engineering, it is just AI rewriting.

### 6. April 2026 anti-patterns (ranking-collapse triggers)

**Canon reference:** SE Ranking March 2026 core update analysis via SearchEngineLand; Originality.ai _AI Content in Google Search Results_ (September 2025); Graphite _Five Percent: More Articles are Created by AI than Humans_.

**One-line definition:** The four documented failure modes from the April 2026 Google core update window - approaches that lost between 28% and 100% of visibility and which the Brain auto-flags when surfaced by any retrieved row.

**Where to use in the brand funnel:** Apply as a hygiene scan on every content production decision, the same way Wall-1 and Wall-2 hygiene scans run on every cocktail and Vault row. (a) Skyscraper rewrites - "make it longer and better than competitors" is dead, Gemini 4.0 flags semantically perfect rewrites as derivative and demotes them out of the Top-100. (b) Pure aggregation / scraping - job aggregators dropped 28% in coverage, dictionary sites dropped 35%. (c) Brand-agnostic traffic plays - sites with low direct / brand traffic share lost 1.5x more visibility than sites with strong brand signals. (d) Generative AI content without proprietary data + human review - 17.31% of the Top is now 100% AI content, but only the slice combined with proprietary data and behavioural signals stayed in the Top-10.

**Where NOT to use:** This principle is the negative space of the other four pillars - it is itself the anti-pattern list. Do not interpret it as "do not use AI content" - the case studies are explicit that AI content + proprietary data + human review + Wall hygiene is the winning combination. Interpret as the things to avoid while applying Pillars 1-5.

---

## KPIs that matter in the LLM era

Track these per quarter alongside conventional SEO KPIs. The benchmarks below come from the ESA Digital case studies; the brand targets should scale to category and stage.

| KPI | What it means | RASK AI benchmark | AITHOR benchmark | the brand Y1 target |
|---|---|---|---|---|
| AI LLM traffic per month | Visits to the brand domain originating from ChatGPT / Claude / Perplexity / Gemini / Copilot etc. | 12,100 | 50,000 | (set after launch baseline) |
| AI citations per month | Distinct times the brand name appears in an LLM answer | (not disclosed) | 5,000 | (set after launch) |
| Sign-up share from AI | % of new subscribers whose attribution touchpoint is an LLM | 50% | (not disclosed) | 20% by Y1 end |
| AI Overview presence | % of target queries where the brand appears in the AI Overview answer | (not disclosed) | (not disclosed) | (measure post-launch) |
| Direct + brand traffic share | % of total traffic that is direct or brand-search (April 2026 protection signal) | (not disclosed) | (not disclosed) | > 30% by Y1 end |

The April 2026 update specifically rewarded sites with high direct + brand traffic share - the 1.5x visibility differential. the brand's brand-mention investment (Pillar 3) directly feeds this KPI.

## Connection to other Brain layers

The six principles above do not replace the Behavioural Economics / NSTD / Cialdini-Sutherland canon - they sit alongside it. A typical query is answered by stacking:

- **Pillar from this canon** (e.g. Programmatic SEO) for the distribution / volume mechanic
- **Cialdini-Sutherland principle** (e.g. Costly Signaling) for the trust / persuasion mechanic inside each page
- **Behavioural Economics principle** (e.g. Anchoring, Specific Numbers) for the per-page conversion mechanic
- **NSTD tactic** (e.g. Labelling, Calibrated Question) for any conversational surface (founder DMs, cart-abandon SMS)

The Brain returns all four schools in one search and the caller picks the right stack.

## Pending decisions

- Which free tools / micro-apps to build first as Pillar 2 + proprietary-data anchors? Candidate list: per-meal sodium budget calculator, flavour-balance score, salt-on-fruit pairing recommender, weekly-meal-prep flavour planner. the founder to pick one or two for Y1.
- Brand-mention partnership budget for Y1 (Pillar 3). Case studies imply 6-12 months of consistent guest-posting + podcast appearances before the AI citation flywheel turns. Allocate before launch.
- Page-refresh cadence (Pillar 4) - confirm quarterly for high-stakes surfaces vs monthly for programmatic. Default in this canon = quarterly hero / PDP / About / welcome, monthly programmatic, annual foundations. Adjust based on Q1 launch data.
- Multilingual roll-out timing for Pillar 1 - UK English at launch is locked. DE / FR / NL depend on EU shipping lane confirmation (Active Ants / Huboo NL / SEKO referral pipeline outcome).

## Source materials

- Dennis Lazard / ESA Digital _How to Get Cited by AI in 2026_ presentation, 12 May 2026 (evidence file at `05-evidence/seo-research/2026-05-12-esa-digital-ai-citation-playbook.md`)
- SE Ranking March 2026 core update analysis via SearchEngineLand
- AirOps _Content Engineering_ definition
- GrowthX overview deck (Figma)
- RASK AI + AITHOR + Marketplace UGC + Marketplace B2C + Enterprise CRM case studies (all by ESA Digital, evidence file above)
- Originality.ai _AI Content in Google Search Results_ (September 2025)
- Graphite _Five Percent: More Articles are Created by AI than Humans_
