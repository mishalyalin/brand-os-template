# Positioning

Owner: {{ YOUR_NAME }}. Status: TEMPLATE - fill in via `python3 tools/onboard.py` or edit directly. Version: 0.1.0. Last updated: {{ DATE }}.

This file is the strategic frame for every customer-facing decision. The Marketing Brain treats it as **Layer 0** - the gate every tactic must pass before it can ship. If a creative idea does not fit the ICP, the 6 content vectors, or respect Wall 1 and Wall 2, the answer is no.

## The positioning line

> **"{{ YOUR_POSITIONING_LINE }}"**

The single source of truth for every brand decision. Not a tagline - the lens through which every creative choice is evaluated.

## ICP - ideal customer profile

- ICP: {{ ICP_DESCRIPTION }}

## Content vectors

Every customer-facing creative must fit one of the vectors below. Up to six total.

1. **{{ VECTOR_1_NAME }}.** {{ VECTOR_1_DESCRIPTION }}
2. **{{ VECTOR_2_NAME }}.** {{ VECTOR_2_DESCRIPTION }}

The vector key + aliases for the Brain parser live in `08-templates/vocab/content-vectors.json`.

## Walls - where we do not play

| Wall | What we do not say |
|---|---|
| **Wall 1 - {{ WALL_1_NAME }}** | {{ WALL_1_FORBIDDEN_REGISTER }} |
| **Wall 2 - {{ WALL_2_NAME }}** | {{ WALL_2_FORBIDDEN_REGISTER }} |

The Brain auto-flags retrieved rows for Wall-1 and Wall-2 trigger words. Edit `08-templates/vocab/hygiene-vocab.json` to tune trigger lists.

## What this positioning forbids in copy

- {{ FORBID_1 }}
- {{ FORBID_2 }}

## What this positioning licenses

- {{ LICENSE_1 }}
- {{ LICENSE_2 }}

## Founder credential

{{ FOUNDER_CREDENTIAL_PARAGRAPH }}

The founder credential is the authority anchor. State the credential factually. Avoid hype.

## Mission surface architecture (V1 / V2 / V3)

The positioning line is one half of the brand story. The mission is the other half - it answers "what do we DO for the customer." Express it across three surface lengths so the same idea can ride a hero, a paragraph, and a tagline without rewriting.

| Surface | Length | Pattern |
|---|---|---|
| **V1 - paragraph** | 2-4 sentences | `{{ MISSION_PARAGRAPH }}` - the operational mission, used on About page and welcome flow E3 |
| **V2 - 3-line hero** | 3 short lines, period-terminated, one breath each | `{{ HERO_LINE_1 }}` / `{{ HERO_LINE_2 }}` / `{{ HERO_LINE_3 }}` - the compressed mission, used on hero, deck cover, manifesto |
| **V3 - tagline** | 1-3 words | `{{ TAGLINE }}` - the brand mark adjunct, used in footer, sign-off, business card |

All three surfaces compress the same mission. If V1 says one thing and V3 says another, V1 wins and V3 gets fixed.

## Five load-bearing positioning elements

Every customer-facing surface (hero, manifesto, paragraph, PDP block) must visibly carry these five elements. Drop one and the positioning loses its load.

1. **Customer owns the input.** The diet / habit / discipline / routine belongs to the customer, not the brand. Pattern: `{{ CUSTOMER_INPUT_NOUN }} you chose` - not `our {{ CUSTOMER_INPUT_NOUN }}` and not `the right {{ CUSTOMER_INPUT_NOUN }}`.
2. **Customer owns the goal.** The outcome belongs to the customer. Pattern: `the goal you set` - not `your goal with us` and not `our promise`.
3. **Universalism.** The product works for any version of the customer profile, not one segment. Pattern: `wherever you are` / `whoever you are` / `whatever your reason` - not `for [specific identity]` and not `the perfect fit for [specific user]`.
4. **Goal-agnostic disclaimer.** Explicit refusal to define why the customer is doing what they are doing. Pattern: `whatever they are` / `we do not ask which one` - not `to help you [specific outcome]`.
5. **Factual product attributes.** The product description is factual - what it is and what it does at the physical/sensory level. Not vague-benefit claims. Pattern: `{{ PILLAR_1 }}, {{ PILLAR_2 }}, {{ PILLAR_3 }}` - measurable nouns the customer can verify.

## Three pillars architecture

Express the product through exactly three pillars. More dilutes attention; fewer fails to differentiate. Each pillar must be a single word or short phrase the customer can see, hold, or measure.

| Pillar | Engineering basis | Wall 1 verdict |
|---|---|---|
| **{{ PILLAR_1 }}** | {{ PILLAR_1_EVIDENCE }} | {{ PILLAR_1_WALL_1 }} |
| **{{ PILLAR_2 }}** | {{ PILLAR_2_EVIDENCE }} | {{ PILLAR_2_WALL_1 }} |
| **{{ PILLAR_3 }}** | {{ PILLAR_3_EVIDENCE }} | {{ PILLAR_3_WALL_1 }} |

The three pillars repeat in this exact order across hero, PDP, manifesto, and pack copy. If you ever say four pillars, you have lost the architecture.

## Qualifier discipline rule (CI-enforced)

Any reference in customer copy to the customer's INPUT or GOAL must pair with a customer-ownership qualifier within 200 characters. Triggers and matching qualifiers are configurable in `.github/workflows/brand-voice-check.yml` and `08-templates/vocab/hygiene-vocab.json`.

Example trigger phrases (replace with yours during onboarding):

- "stick with your {{ CUSTOMER_INPUT_NOUN }}" / "stick with the {{ CUSTOMER_INPUT_NOUN }}"
- "reach your goal" / "reach the goals"
- "achieve your goal" / "achieve the goals"

Example matching qualifiers (must be within 200 chars of the trigger):

- "the {{ CUSTOMER_INPUT_NOUN }} you chose"
- "the goals you set"
- "whatever they are"
- "whatever your goal is"
- "you chose" / "you set"
- third-person variants: "the {{ CUSTOMER_INPUT_NOUN }} they chose" / "they chose" / "their {{ CUSTOMER_INPUT_NOUN }}"

This rule exists to protect Wall 1 (no medicinal / vague-benefit register). Without the customer-ownership qualifier, "stick with your diet to reach your goal" reads as a benefit claim by the brand. With it, the construction reframes as the customer's own commitment which the brand supports - regulatorily safer and emotionally more accurate.

## Voice register references

{{ VOICE_REGISTER_REFS }}

Cadence references only - not category competitors.

## Reference brands we do NOT name in customer copy

{{ NEVER_NAME_BRANDS }}

## How this file connects to the Marketing Brain

```bash
python3 tools/marketing_brain.py rebuild-index
python3 tools/marketing_brain.py icp
```

## Pending decisions

- (open positioning questions awaiting decision)

## Source materials

- Onboarding interview run on {{ DATE }} via `tools/onboard.py`
