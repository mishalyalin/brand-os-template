# Brand voice

Owner: {{ YOUR_NAME }}. Status: TEMPLATE - fill in via `python3 tools/onboard.py` or edit directly. Version: 0.1.0.

## The five-sentence voice

{{ FIVE_SENTENCE_VOICE }}

Five sentences each doing one job: who is the voice / what they sound like / what they assume about the reader / what they reject in the category / what they swap in.

## Two voice registers (do not mix them)

The brand speaks in TWO registers depending on who is speaking. They are not interchangeable.

### Register A: founder narrative

Who speaks: the founder, or content authored in the founder's voice (manifesto, About page, welcome flow E3, podcast appearances).

What it sounds like: first-person or third-person narrative. Can carry the founder's discipline arc, the failure modes the founder watched, the inventor's frame ("I built the tool I did not have"). Can use long-form. Can carry conviction.

Wall-1 verdict: less strict because the founder is describing the founder's OWN experience, not making product claims. But still no medicinal vocabulary about what the product does.

### Register B: customer testimonial

Who speaks: a customer, or content authored as if a customer is speaking (review widgets, IG testimonial copy, affiliate scripts, day-7 post-purchase email solicit).

What it sounds like: first-person from the customer. Must follow the **5-beat honest-attribution formula** (see `01-canon/cocktail-recipes.md` "The honest-attribution testimonial cocktail"). The customer's discipline + goal own the outcome. The product owns the adherence-rescue mechanism, not the outcome.

Wall-1 verdict: very strict. The customer cannot say the product caused the outcome. The customer can only say the product made the discipline livable, made the meal repeatable, made the routine sustainable - never that it caused weight loss / muscle gain / longevity / energy / immunity / [specific body claim].

### Why this matters

Mixing registers is the most common voice failure. A founder who sounds like a customer ("I lost {{ N }} kg with our product") is a Wall-1 violation. A customer who sounds like a founder ("Our product is what got me through") is creepy. Each register stays in its lane.

Pin every touchpoint copy file in `03-touchpoint-copy/` to one register at the top of the file. CI does not yet enforce the register pin - the reviewer enforces it.

## The seven hard rules (CI-enforced)

1. **{{ HARD_RULE_1 }}** ({{ HARD_RULE_1_RATIONALE }})
2. **{{ HARD_RULE_2 }}** ({{ HARD_RULE_2_RATIONALE }})
3. **{{ HARD_RULE_3 }}** ({{ HARD_RULE_3_RATIONALE }})
4. **{{ HARD_RULE_4 }}** ({{ HARD_RULE_4_RATIONALE }})
5. **{{ HARD_RULE_5 }}** ({{ HARD_RULE_5_RATIONALE }})
6. **{{ HARD_RULE_6 }}** ({{ HARD_RULE_6_RATIONALE }})
7. **{{ HARD_RULE_7 }}** ({{ HARD_RULE_7_RATIONALE }})

## Banned vocabulary

- {{ BANNED_PHRASE_1 }}
- {{ BANNED_PHRASE_2 }}

## Before / after examples

| Off-brand | On-brand |
|---|---|
| {{ OFF_BRAND_EXAMPLE_1 }} | {{ ON_BRAND_EXAMPLE_1 }} |
| {{ OFF_BRAND_EXAMPLE_2 }} | {{ ON_BRAND_EXAMPLE_2 }} |

## How to use this file

Every touchpoint copy file pins to a brand voice version in its front matter.
