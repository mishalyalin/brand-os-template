# Cocktail recipes

Owner: {{ YOUR_NAME }}. Status: TEMPLATE - add your first cocktail when a real use case demands it. Version: 0.1.0.

A "cocktail" is a pre-vetted stack of behavioral, negotiation, and influence tactics applied to a specific funnel moment, with the Wall-1 and Wall-2 hygiene checks already applied. The Brain treats cocktails as **Layer 1** - pre-curated answers that should be tried before generating a fresh stack from raw tactics.

The Brain parses this file at index-build time. Each `### <Name>` block becomes one cocktail in the index. After editing this file, run:

```bash
python3 tools/marketing_brain.py rebuild-index
```

## How to write a cocktail

Each cocktail entry should contain:

1. **Funnel stage** - where it fires (hero, cart abandon, welcome flow, PDP, founder section, retention email, etc.)
2. **Tactic stack** - which behavioral principles are layered (Anchoring + Loss Aversion + Identity Priming, etc.)
3. **Verbatim copy or template** - the actual sentence-level draft, ready to ship or fill-in
4. **Primary citations** - the canonical source for each principle (Kahneman, Voss, Cialdini, etc.)
5. **Wall-1 / Wall-2 hygiene confirmation** - explicit "this respects Wall 1 because..." sentences
6. **Notes on when NOT to use** - the situations where this cocktail fails

## Example cocktail (placeholder - replace with yours)

### {{ EXAMPLE_COCKTAIL_NAME }}

**Funnel stage:** {{ FUNNEL_STAGE }}.

**Tactic stack:** {{ TACTIC_1 }} + {{ TACTIC_2 }} + {{ TACTIC_3 }}.

**Verbatim copy:**

> {{ VERBATIM_COPY }}

**Why this cocktail fits the brand:**

{{ FIT_RATIONALE }}

**Primary citations:**

- {{ TACTIC_1 }}: {{ CITATION_1 }}
- {{ TACTIC_2 }}: {{ CITATION_2 }}
- {{ TACTIC_3 }}: {{ CITATION_3 }}

**Hygiene confirmation:**

- Wall 1: {{ WALL_1_NOTE }}
- Wall 2: {{ WALL_2_NOTE }}

**When NOT to use:** {{ WHEN_NOT_TO_USE }}.

---

### The honest-attribution testimonial cocktail (5-beat formula)

This is a CANON cocktail. It is not a brand-specific example - it is the cross-brand pattern for every customer testimonial across every surface. Keep this entry; do not delete or replace.

**Funnel stage:** review collection + every social-proof surface (PDP review widget, IG testimonial captions, day-7 post-purchase email, affiliate creator scripts, founder-section pull-out quotes).

**Tactic stack:** Cialdini Social Proof + Voss "That's Right" elicitation + Sutherland Costly-Signal disclaimer + Cialdini Unity (community close, optional).

**Verbatim template:**

> Beat 1 (discipline + goal, customer-owned): "I have been {{ DISCIPLINE_VERB }} for {{ TIMEFRAME }} to {{ GOAL }}."
>
> Beat 2 (honest disclaimer): "The {{ MEASURABLE_RESULT }} came from {{ DISCIPLINE }}, not from {{ BRAND_NAME }}. {{ ATTRIBUTION_DETAIL }}."
>
> Beat 3 (specific failure mode the product prevented): "What I would have failed on was {{ SPECIFIC_FAILURE_MODE }} - {{ CONCRETE_DETAIL }}. That is what {{ BRAND_NAME }} caught."
>
> Beat 4 (optional treat-within-the-frame): "Now {{ TREAT }} is part of the routine instead of a cheat."
>
> Beat 5 (optional community close): "I am {{ COMMUNITY_NAME_SINGULAR }} now."

**Why this cocktail fits any brand following the customer-owns-outcome positioning:**

The 5-beat structure separates OUTCOME (owned by customer discipline) from MECHANISM (owned by the product). Wall-1 safe by construction - Beat 2 explicitly denies product-as-cause for the outcome, which earns the brand the right to take credit for the adherence-rescue moment in Beat 3.

**Primary citations:**

- Cialdini "Influence" - Social Proof (Chapter 4): testimonials work because they are not the brand speaking
- Voss "Never Split the Difference" - That's Right elicitation: the 5-beat formula gives the customer a structure they can fill with their own truth, which produces more authentic testimonials than open-ended prompts
- Sutherland "Alchemy" - Costly-Signal Theory: the honest disclaimer in Beat 2 signals confidence - the brand could overclaim and chose not to. Customers pattern-match honesty as trustworthiness.

**Hygiene confirmation:**

- Wall 1: PASS by construction. Beat 2 forces customer-ownership of the outcome.
- Wall 2: PASS by construction. No category comparison required for the testimonial to land.

**When NOT to use:**

- The 5-beat formula is for CUSTOMER voice (Register B in `00-foundations/brand-voice.md`). The FOUNDER does not speak in this register. Founder content uses the chronological-correctness rule from `00-foundations/founder-stories.md` instead.
- Anonymous press quotes or aggregated review-count claims ("4.9 stars from 1,200 reviews") sit beside the testimonial, not inside it.
- One-line star-ratings without body text do not get the 5-beat treatment - they are a separate surface.

**Day-7 review-request email template:** `03-touchpoint-copy/emails/review-request.md` (three variants A/B/C).

**Wall-1 reject patterns and safe rewrites:** see `08-templates/testimonial-template.md` for the full table.

---

### The category-anchor reframe cocktail (Sutherland verb-not-noun)

**Where it fires:** Hero copy. PDP h1 + first body paragraph. IG bio. Founder essay opening. Press boilerplate. About page. Any surface where the reader's first mental category-lookup happens.

**Why this is canon:**

Every product has two category anchors: the legal one (what regulators classify it as) and the customer mental one (what the customer's brain files it under at first contact). Most early brands assume these must be the same. They do not. The legal classification stays locked; the customer mental category is a marketing decision that lives in the hero copy.

When a brand's customer mental anchor is set at the wrong reference class, the price will feel wrong no matter how good the copy is. The hero copy is where this is fixed. The Sutherland _Alchemy_ verb-not-noun lesson applied to product reveal: lead with what the product DOES in the customer's life, not with what it IS in the cupboard.

Full pattern documented in `06-decisions/REFERENCE-category-anchor-reframe.md`.

**Recipe (lead with verb / function, hold the noun):**

- Open with what the product DOES in the customer's life, never with what the product IS
- Anchor against the peer set in the NEW customer category (whatever your reframed peer set is), not against the peer set in the legal category
- The product noun appears later in the page (PDP technical block, ingredient panel, mission statement) - never in hero h1
- Wall-2 hygiene throughout - no category-comparison against the OLD category peers
- Wall-1 hygiene throughout - the reframe does not unlock new claims

**Hero-line variant template (multi-variant default mode applies):**

| # | Hero line construction | Anchor type | Notes |
|---|---|---|---|
| A | "The [function] in your [budget category]." | Direct category placement | Most explicit; reads as definition. Use on About / founder essay where reader has context. |
| B | "The [tool] that fixes the worst part of [the problem your customer has]." | Verb-led, problem-named | Best for paid social cold audience; surfaces the pain before product. |
| C | "The [unit] between [success state] and [failure state]." | Failure-mode anchor | Best for retention email + creator brief opener (loss aversion lens). |
| D | "The [recursive reframe] that makes [the goal] work." | Recursive reframe | Best for IG bio + 7-word headline slots. |
| E | "Next to your [peer 1]. Next to your [peer 2]. The [thing] in your stack that [verb-led action]." | Peer placement + mechanism | Best for PDP price block + founder essay. Names peer-set; needs owner per-surface OK. |
| F | "What you take when you take your [discipline / commitment] seriously and you still want to [enjoy the thing]." | Identity + permission | Best for paid social warm audience; identity-led + permission-led. |

Each row leads with a verb or a function. Each row reveals the product implicitly without naming the old category noun.

**Stacked principles:**

1. **Sutherland verb-not-noun** (_Alchemy_, ch. 2) - the function is named before the form. Product reveal is delayed.
2. **Mental categorisation** (Lakoff / Sutherland) - the first noun the customer mentally tags determines reference class for everything they read after. Get the first noun right.
3. **Anchoring** (Kahneman / Ariely) - the reference class anchors the price tolerance. Anchoring at the right peer set is half the price work.
4. **Pratfall reframe** (Sutherland 2.7 + Bohner et al. 2003) - surfacing the pain (the problem the discipline solves) before the offer increases credibility.
5. **Wall-2 hygiene by construction** - the cocktail forbids the customer-side noun for the OLD category from appearing in primary copy. The cocktail itself enforces the wall.

**Hygiene confirmation:**

- Wall 1: PASS by construction - the reframe never introduces medicinal claims.
- Wall 2: PASS by construction - the cocktail bans the old-category product noun from primary copy.

**When NOT to use:**

- Ingredient panels, regulatory blocks, legal pages, VAT documentation - these use the legal noun because they live in the legal classification surface.
- Surfaces where you have not done the upstream category-reframe work (see `REFERENCE-category-anchor-reframe.md`). Without the upstream work, this cocktail just confuses.
- Surfaces where the category reframe is contested by the customer (e.g. when retail buyer expectations or platform classification force the old category). In those cases the legal-and-customer category collapse back together by external pressure.

**Pairs well with:**

- "Multi-variant decision-support cocktail" below - this cocktail emits 6 hero-line variants by default; the multi-variant cocktail explains how to read them.
- Any pricing cocktail in your `01-canon/pricing-mechanics.md` - the price anchor must match the category anchor or both fail.
- Any testimonial cocktail in this file - testimonials on the same page must reinforce the new category, not undercut it by accidentally using the old-category noun.

### The multi-variant decision-support cocktail

**Where it fires:** Default output format for any customer-facing copy generation request - hero copy, PDP h1, ad headline, subject line, sub-line, microcopy, CTA, captions, push notifications, SMS, email body openings, founder essay openings.

Single-variant mode is reserved. Trigger list and exclusion list documented in `06-decisions/REFERENCE-multi-variant-default-mode.md`.

**Why this is canon:**

A single-variant output ("here is my best draft") asks the decider to either accept or reject blind. Multi-variant output surfaces the option space, forces each variant to declare its canon source, and creates a tested ladder for free. Three jobs at once for the same effort.

**Recipe (output format):**

| # | Variant copy | Lens / canon principle | Wall-1 | Wall-2 | Stars | Notes |
|---|---|---|---|---|---|---|
| A | _line A_ | _e.g. Layer 0 ICP vector_ | OK / Risk | OK / Risk | ★★★★ | _why this might win_ |
| B | _line B_ | _e.g. BE - loss aversion_ | OK / Risk | OK / Risk | ★★★ | _why this might win_ |
| C | _line C_ | _e.g. Voss - calibrated label_ | OK / Risk | OK / Risk | ★★★★★ | PREFERRED. _why._ |
| D | _line D_ | _e.g. Cialdini Unity_ | OK / Risk | OK / Risk | ★★ | _why this might lose_ |
| E | _line E_ | _e.g. Sutherland verb-not-noun_ | OK / Risk | OK / Risk | ★★★ | _why this is the safe fallback_ |

Optional 6th variant if the surface has a hard split (cold vs warm, mobile vs desktop, EU vs US).

**Star calibration:**

- ★ - underperform-expected floor
- ★★ - solid, might surprise
- ★★★ - strong default
- ★★★★ - strong + carries extra load-bearing principle
- ★★★★★ - PREFERRED, all load-bearing principles + lowest decider-veto risk

**Slate composition recommendation:**

- 1 variant from Layer 0 (ICP / content vector)
- 1 variant from Behavioral Economics
- 1 variant from Voss / NSTD
- 1 variant from Cialdini-Sutherland
- 1 variant from DTC mechanics or Subscription mechanics
- 0-1 variant from Pricing or LLM SEO mechanics

Skip lenses that do not apply. Lean into 2 variants of the same lens when one lens clearly dominates the surface.

**Stacked principles:**

1. **Decoy effect** (Ariely / Williams-Sonoma 1992) - the slate creates a reference class for the PREFERRED. Without the slate, PREFERRED has nothing to be measured against.
2. **Satisficing** (Sutherland _Alchemy_ ch. 4) - 4-6 options lets the decider satisfice; preserves agency; speeds decision.
3. **Process honesty** (Cialdini Authority + Bohner Pratfall) - showing the weak variants signals the brand is not hiding trade-offs.
4. **Sweat-the-small-stuff** (Sutherland 2.11) - 4-6 variants on microcopy demonstrates care.
5. **Iyengar-Lepper bound** (jam-shop 2000) - 24 options reduce conversion; 4-6 is the cognitive sweet spot.

**Hygiene confirmation:**

- Wall 1: PASS by construction - every variant passes the same hard-rule scan; multi-variant does not bypass voice rules.
- Wall 2: PASS by construction - same scan applies to every variant.

**When NOT to use:**

- Locked canon (manifesto, mission V1, hero 3-line, "What we believe" 5-line block, "What we are not" negation lines, identity close, founder sign-off)
- Single-word labels (community name, founder name, brand name, pillar words)
- Time-sensitive ops (SLA-bounded reply, hot CS response, within-the-hour social post)
- Surfaces where the brand owner has already specified the exact wording
- Legal / regulatory copy (ingredient panel, allergen declaration, VAT footer, refund policy)
- Schema.org structured-data text (locked product name + locked description)

**Pairs well with:**

- The category-anchor reframe cocktail above - the hero-line variants A-F there demonstrate the multi-variant pattern in action.
- Any pricing cocktail in your `01-canon/pricing-mechanics.md` - price-block variants benefit from multi-variant testing because pricing copy is one of the highest-leverage surfaces.
- The honest-attribution testimonial cocktail above - testimonial coaching may emit 4-5 candidate rewrites for a single source review.

---

Add additional cocktails below as the brand develops them. Cocktails are the most valuable layer of the Brain because each one represents a battle-tested combination - not theory, applied practice.
