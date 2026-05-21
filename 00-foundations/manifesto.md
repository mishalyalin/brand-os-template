# {{ BRAND_NAME }} Manifesto

Owner: {{ YOUR_NAME }}. Status: canonical (locked {{ DATE }}). Version: manifesto-v1.0.0. Last updated: {{ DATE }}.

This is the public-facing brand manifesto. It is the first thing a visitor sees on the Brand OS web (`/` route). It is the canonical source for the brand mission, vision, and purpose - rendered in the founder narrative voice register, locked together, no consultancy jargon.

Mission, vision, and purpose are aligned with `00-foundations/positioning.md` and `00-foundations/founder-stories.md`. If any line below conflicts with those source files, those source files win and this file gets fixed inline.

---

# {{ HERO_LINE_1 }}
# {{ HERO_LINE_2 }}
# {{ HERO_LINE_3 }}

---

## Why we exist

{{ WHY_PARAGRAPH_1 }}

{{ WHY_PARAGRAPH_2_FOUNDER_BROUGHT_OTHERS_IN }}

{{ WHY_PARAGRAPH_3_NOT_WILLPOWER_BUT_X }}

{{ WHY_PARAGRAPH_4_OPTIONAL_CONCRETE_IMAGERY }}

{{ WHY_PARAGRAPH_5_BUILT_THE_TOOL }}

{{ WHY_PUNCH_LINE }}

## What we do

{{ MISSION_PARAGRAPH }}

{{ WHAT_WE_DO_OPTIONAL_LOCATIVE_SCENES }}

{{ WHAT_WE_DO_OPTIONAL_TRANSFORMATIONAL_REFRAME }}

## Where we are going

{{ VISION_PARAGRAPH_1 }}

{{ VISION_PARAGRAPH_2 }}

{{ VISION_PARAGRAPH_3 }}

## What we believe

- {{ BELIEF_1 }}
- {{ BELIEF_2 }}
- {{ BELIEF_3 }}
- {{ BELIEF_4 }}
- {{ BELIEF_5 }}

## What we are not

{{ NEGATION_TRIPLE }}

{{ NEGATION_PARAGRAPH_WE_DO_NOT_PROMISE_OUTCOMES }}

## You

{{ YOU_OPENING_PARAGRAPH }}

{{ YOU_OPTIONAL_CONCRETE_REASON_LIST }}

{{ YOU_CLOSING_QUESTION }}

If yes, you are {{ COMMUNITY_NAME_SINGULAR }}.

-{{ FOUNDER_SHORTNAME }}

---

## Structure (load-bearing elements)

The manifesto is organised in seven sections, each carrying a specific function. Drop any one and the manifesto loses its load.

| Section | Function | Source canon |
|---|---|---|
| 3-line hero | Compressed mission, period-terminated, each line a separate breath | `00-foundations/positioning.md` Mission V2 |
| Why we exist | Founder origin in narrative form - the "purpose in life" question answered | `00-foundations/founder-stories.md` founder arc |
| What we do (mission) | Operational mission verbatim | `00-foundations/positioning.md` Mission V1 |
| Where we are going (vision) | Future-state language - the world we are building | New canon - locked at first manifesto write |
| What we believe | 5 belief statements (Cialdini Commitment-Consistency anchor) | New canon - locked at first manifesto write |
| What we are not | 3-line negation block (Wall-1 protection by explicit denial) | `00-foundations/positioning.md` "What this positioning forbids" |
| You / identity close | Reader-as-protagonist + community identity close (Cialdini Unity) | `00-foundations/positioning.md` POS-LICENSES community name |

## Five load-bearing positioning elements (verify all 5 are present)

1. Customer owns the input ("the {{ CUSTOMER_INPUT_NOUN }} you chose")
2. Customer owns the goal ("the goals you set")
3. Universalism ("wherever you are" / "whatever your reason")
4. Goal-agnostic disclaimer ("whatever they are" / "we do not ask which one")
5. Factual product attributes (the three pillars from positioning.md)

If any of the five is missing, fix it before locking the manifesto version.

## Where this deploys

| Surface | Length | Notes |
|---|---|---|
| Brand OS web home (`/` route) | Full manifesto | Renders as hero page; search moves to `/search` |
| Public website About page | Full or sectioned | LLM SEO entity copy; structured-data anchor |
| Investor deck cover slide | 3-line hero only | The compressed mission |
| Press boilerplate | "What we do" + "Where we are going" paragraphs | Standard founder-led press kit |
| Email footer (long-form on welcome flow E3) | "Why we exist" + "What we do" | The founder pivot moment |
| Office wall print (one-off) | Full manifesto | Internal team artefact |
| Internal onboarding doc (Confluence / Notion) | Full manifesto | First read for any new team member |
| Creator brief opening (`08-templates/creator-brief-template.md`) | "What we believe" + "What we are not" | Helps creators self-locate before scripting |

## Editorial discipline

- Period-terminated declarative cadence throughout. No questions in the manifesto except the single calibrated question near the close.
- Short hyphens only. No em-dashes, no en-dashes.
- No exclamation marks anywhere in the manifesto.
- No emojis.
- No medicinal-register words (the explicit "What we are not" line is the only place those words appear, and they appear in negation form).
- No co-founder names unless the on-camera policy in `00-foundations/founder-stories.md` permits it. Recipe heritage or company history can be acknowledged without naming.
- The 3-line hero is rendered with one line per visual breath. Big typography on screen; the line breaks are part of the design.
- The three pillars are rendered bold or in pillar-formatting to surface the three-pillar architecture.
- Sign-off is `-{{ FOUNDER_SHORTNAME }}` (lowercase, short hyphen). Lives on its own line.

## Banned framings (do not edit these in)

- "magical" / "magic rescue" - vague-benefit-claim trigger, Wall-1 violation
- "religion" / "convert people" - cult-edge framing; manifesto stays goal-agnostic
- "lose weight" / "burn fat" / "build muscle" / [other specific body outcome] as brand-caused outcomes
- By-equity-only co-founder names (see `00-foundations/founder-stories.md` co-founder / on-camera policy)
- Celebrity endorsements - the brand should not chase them; founder credential carries the brand
- Category comparison ("better than {{ COMPETITOR }}" / "vs {{ COMPETITOR }}") - Wall-2 violation
- Wellness-register vocabulary outside the explicit "What we are not" negation line
- Founder labelled by specific lifestyle / diet / identity (see `00-foundations/founder-stories.md` Rule 2 ICP-defensiveness)

## How to write the first manifesto

1. Read `00-foundations/positioning.md` and lock the three pillars first. Without three pillars, "What we do" has nothing to compress into a hero.
2. Read `00-foundations/founder-stories.md` and apply the chronological-correctness rule (Rule 1). Founder succeeded WITHOUT the product. Product is the post-facto rescue for others.
3. Apply ICP-defensiveness (Rule 2). Strip founder-specific lifestyle labels.
4. Draft the 3-line hero (V2 mission) first. Then the paragraphs grow from it.
5. Run the five-load-bearing-elements verification before committing.
6. Run the brand voice check CI locally: em-dash scan + exclamation scan + medicinal vocab scan + qualifier-guard scan.

## How to iterate the manifesto

Manifesto versions follow semantic versioning. v1.0.0 is the first lock. Patch bumps (v1.0.1) for typo fixes. Minor bumps (v1.1.0) for surgical edits that add imagery, scenes, or reframes WITHOUT changing structure. Major bumps (v2.0.0) for structural rewrites (changing the 7 sections or the 5 load-bearing elements).

Every iteration ships with a decision record in `06-decisions/` documenting what changed, why, what stays the same, and what stays load-bearing.
