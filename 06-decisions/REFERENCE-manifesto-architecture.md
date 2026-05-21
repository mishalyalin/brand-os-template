# REFERENCE - 7-section manifesto architecture pattern

Owner: this is a reference / pattern document, not a brand-specific decision. Status: **canonical pattern**, do not delete.

This file documents the architecture that lives in `00-foundations/manifesto.md` + `web/templates/manifesto.html` + manifesto CSS in `web/static/style.css`. It is here for future Claude sessions and contributors who need to understand WHY the structure exists before they edit it.

## What the pattern is

The brand manifesto is the public-facing statement of mission, vision, and purpose. It is deployed as the home page of the Brand OS web (`/` route) and lifted to other surfaces (About page, investor deck cover, welcome flow E3 email, office wall print).

It has exactly seven sections in this order. Each section carries a specific function. Drop any one and the manifesto loses its load.

1. **3-line hero** - compressed mission, V2 from positioning.md (one breath per line, period-terminated)
2. **Why we exist** - founder origin in narrative form, the "purpose in life" answered
3. **What we do** - operational mission V1 from positioning.md
4. **Where we are going** - vision, future-state language
5. **What we believe** - 5 belief statements (Cialdini Commitment-Consistency anchor)
6. **What we are not** - 3-line negation block (Wall-1 protection by explicit denial)
7. **You** - reader-as-protagonist + community identity close (Cialdini Unity)

## Why each section is load-bearing

### 3-line hero

The customer encounters the brand in 2-3 seconds across most surfaces (Instagram, Google search snippet, About page first viewport, deck cover). The 3-line hero is what they see. Without it, the manifesto opens with paragraph text that does not register inside 2-3 seconds.

Each line is one breath. Each line is period-terminated. The line breaks are part of the design.

### Why we exist (purpose)

The founder origin section answers the existential question. It is the only place the manifesto refers to the founder by name (and even then, third-person narrative, not first-person). Without it, the manifesto is a list of claims without a person behind them.

Construction rules: chronological correctness (founder transformed WITHOUT the product) + ICP-defensiveness (no specific lifestyle label). Both rules documented in `00-foundations/founder-stories.md`.

### What we do (mission)

Verbatim mission paragraph from positioning.md V1. This is the operational statement - what the brand does for the customer. Lifts directly. Do not rewrite in the manifesto; if the mission needs to change, change it in positioning.md and let the manifesto inherit.

### Where we are going (vision)

The future-state language. Three short paragraphs painting the world the brand is building. This is the only section that does not lift verbatim from another canon file - it is locked at first manifesto write and lives here as canonical.

Without this section, the manifesto is past-tense (founder origin) and present-tense (mission) only. The vision section makes the manifesto forward-looking.

### What we believe (5 beliefs)

Five short belief statements. They function as a Cialdini Commitment-Consistency anchor: the reader who agrees with the beliefs has implicitly committed to the brand's frame. Five is the cognitive sweet spot - more dilutes, fewer fails.

These beliefs are NOT brand promises. They are stances. "Discipline is not the problem. Flavour is." is a stance. "We will help you lose 5 kg" is a promise. Promises are banned (Wall-1).

### What we are not (negation)

Three-line negation block. Names the categories the brand explicitly refuses to be ("not a wellness brand", "not a weight-loss brand", "not a supplement"). This is Wall-1 protection by explicit denial - it inoculates the brand against being read as those categories by a stranger.

The single time medicinal-register words are allowed to appear in the manifesto is in this negation block. CI has manifesto.md in its medicinal-vocab skip list specifically for this reason.

### You / identity close (Unity)

The final section addresses the reader directly. It opens the door, asks the calibrated question ("are you in for the long run?"), and closes with the community identity statement ("If yes, you are {{ COMMUNITY_NAME_SINGULAR }}.").

The Cialdini Unity mechanism: people who self-identify with a community are dramatically more likely to commit. The community name itself comes from positioning.md POS-LICENSES list.

Sign-off is the founder's short name (lowercase, short hyphen, e.g. `-{{ FOUNDER_SHORTNAME }}`). On its own line. The sign-off is what carries the personal voice.

## How to iterate the manifesto

Manifesto versions follow semantic versioning:

| Version bump | What it covers | Example |
|---|---|---|
| Patch (v1.0.1) | Typo fixes, formatting, broken link | Fix a misspelled belief |
| Minor (v1.1.0) | Surgical edits that add imagery / scenes / reframes WITHOUT changing structure | Add a food-imagery line under "Why we exist", add portability scenes under "What we do" |
| Major (v2.0.0) | Structural rewrites (changing the 7 sections, the 5 load-bearing elements, the founder voice register) | Replace the 7-section model with a 5-section model |

Every iteration ships with a decision record in `06-decisions/` documenting what changed, why, what stays the same, and what stays load-bearing.

## Deployment surfaces

| Surface | Length | Notes |
|---|---|---|
| Brand OS web home (`/` route) | Full manifesto | Renders as hero page; search moves to `/search` |
| Public website About page | Full or sectioned | LLM SEO entity copy; structured-data anchor |
| Investor deck cover slide | 3-line hero only | The compressed mission |
| Press boilerplate | "What we do" + "Where we are going" paragraphs | Standard founder-led press kit |
| Email footer / welcome flow E3 | "Why we exist" + "What we do" | The founder pivot moment |
| Office wall print (one-off) | Full manifesto | Internal team artefact |
| Internal onboarding doc | Full manifesto | First read for any new team member |
| Creator brief opening | "What we believe" + "What we are not" | Helps creators self-locate before scripting |

## Editorial discipline

- Period-terminated declarative cadence throughout. One calibrated question allowed near the close ("are you in for the long run?").
- Short hyphens only.
- No exclamation marks.
- No emojis.
- No medicinal-register words EXCEPT in the explicit "What we are not" negation block.
- No co-founder names unless the on-camera policy in `00-foundations/founder-stories.md` permits it.
- 3-line hero rendered one line per visual breath. Big typography on screen.
- Three pillars rendered bold or in pillar-formatting.
- Sign-off is `-{{ FOUNDER_SHORTNAME }}`, lowercase, short hyphen, own line.

## Banned framings

- "magical" / "magic rescue"
- "religion" / "convert people"
- Specific brand-caused body outcomes ("lose weight" / "burn fat" / "build muscle" / "boost immunity")
- By-equity-only co-founder names
- Celebrity endorsements
- Category comparisons
- Wellness-register vocabulary outside the negation block
- Founder labelled by specific lifestyle / diet / identity (see `00-foundations/founder-stories.md` Rule 2)

## Relationship to other canon

| Sibling file | What it owns | Relationship to this pattern |
|---|---|---|
| `00-foundations/manifesto.md` | The canonical text + load-bearing structure table + banned framings | The home of the manifesto. Edit there, not here. |
| `00-foundations/positioning.md` | Mission V1/V2/V3, three pillars, 5 load-bearing elements | Manifesto inherits from positioning. Conflicts resolve in favour of positioning. |
| `00-foundations/founder-stories.md` | Founder arc rules | Manifesto "Why we exist" applies founder arc Rule 1 + Rule 2. |
| `00-foundations/brand-voice.md` | Two voice registers, hard rules | Manifesto is Register A (founder narrative) throughout. |
| `web/templates/manifesto.html` | The Jinja template for the live web manifesto | Renders the markdown from manifesto.md into the brand visual identity. |
| `web/static/style.css` | The manifesto CSS using CSS variables | Inherits the brand token system. |
| `06-decisions/REFERENCE-positioning-load-bearing-elements.md` | The 5 elements pattern | The manifesto verifies all 5 elements are present before locking. |

## How to write the first manifesto

1. Read `00-foundations/positioning.md` and lock the three pillars first. Without three pillars, "What we do" has nothing to compress into a hero.
2. Read `00-foundations/founder-stories.md` and apply the chronological-correctness rule (Rule 1).
3. Apply ICP-defensiveness (Rule 2).
4. Draft the 3-line hero (V2 mission) first. Then the paragraphs grow from it.
5. Run the five-load-bearing-elements verification before committing.
6. Run brand voice check CI locally before opening the PR.
7. Open PR. Wait for CI green. Merge. Manifesto deploys via the deploy workflow if you have one wired up.
