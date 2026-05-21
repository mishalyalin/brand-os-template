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

Add additional cocktails below as the brand develops them. Cocktails are the most valuable layer of the Brain because each one represents a battle-tested combination - not theory, applied practice.
