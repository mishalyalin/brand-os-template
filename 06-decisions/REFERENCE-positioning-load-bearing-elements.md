# REFERENCE - five load-bearing positioning elements pattern

Owner: this is a reference / pattern document, not a brand-specific decision. Status: **canonical pattern**, do not delete.

This file documents the architecture that lives in `00-foundations/positioning.md` "Five load-bearing positioning elements" + "Three pillars architecture" + "Qualifier discipline rule" sections. It is here for future Claude sessions and contributors who need to understand WHY the pattern exists before they edit it.

## What the pattern is

Every customer-facing surface (hero, manifesto, About paragraph, PDP block, paid-ad creative) must visibly carry these five elements. Drop any one and the positioning loses its load.

1. **Customer owns the input.** The diet / habit / routine / discipline belongs to the customer.
2. **Customer owns the goal.** The outcome belongs to the customer.
3. **Universalism.** The product works for any version of the customer profile, not one segment.
4. **Goal-agnostic disclaimer.** Explicit refusal to define why the customer is doing what they are doing.
5. **Factual product attributes.** The three pillars from positioning.md, named factually.

## Why each element is load-bearing

### Element 1 + 2: customer ownership of input and goal

Without these, the brand is implicitly claiming to cause the input or the goal. That is a Wall-1 violation (medicinal / outcome-promising register) under most food / supplement / DTC regulatory regimes. With these, the construction reframes as customer commitment + brand support - regulatorily safer and emotionally more accurate.

### Element 3: universalism

Without it, the positioning narrows to a specific identity / lifestyle / demographic. That limits LTV at scale AND polarizes the founder if their specific identity is used to define the universe of customers. With it, the brand can grow horizontally across identities without rewriting positioning.

### Element 4: goal-agnostic disclaimer

The explicit refusal phrase ("whatever they are" / "we do not ask which one") is the clearest signal to a stranger that the brand is not converting them to a specific philosophy. Without it, even universalist positioning can read as evangelism.

### Element 5: factual product attributes (three pillars)

The brand grounds itself in measurable claims about the product's physical properties. This is the load-bearing structure that lets the brand make claims at all - because every claim resolves to a verifiable property of the product, not a promise about the customer's body or future.

## Why exactly three pillars

Four pillars dilute attention. Two pillars fail to differentiate (every brand has two virtues to claim). Three is the cognitive sweet spot - the customer can hold three after one read.

Express the three pillars in a single short phrase each (one word ideally; two if needed). The pillars repeat in this exact order across hero, PDP, manifesto, pack copy, deck cover. If you ever say four, you have lost the architecture.

## Why the qualifier discipline rule (CI-enforced)

Any reference to the customer's INPUT or GOAL in customer copy must pair with a customer-ownership qualifier within 200 characters. Without this rule, copy drifts toward "stick with your diet to reach your goal" - which is a benefit claim by the brand. With the rule, every drift gets caught at PR review.

The 200-character window is empirical. Shorter windows fail catch cases where the qualifier sits in a previous sentence. Longer windows let benefit claims sneak through with the qualifier far away in the copy.

## How to verify a surface carries all five elements

Open the surface (the actual copy that ships). Read it as a stranger would. Ask:

1. Does the copy state that the discipline / habit / input is THEIR choice, not ours?
2. Does the copy state that the outcome / goal is THEIR achievement, not ours to promise?
3. Does the copy work for someone whose identity, demographic, or lifestyle is different from the founder's?
4. Does the copy explicitly refuse to define WHY the customer is doing the thing?
5. Does the copy name the three pillars (product attributes) factually, not promissorily?

If any answer is no, the surface fails. Send back for rewrite before publishing.

## Relationship to other canon

| Sibling file | What it owns | Relationship to this pattern |
|---|---|---|
| `00-foundations/positioning.md` | The five elements + three pillars + qualifier rule, fillable via onboarding | The home of the pattern. Edit there, not here. |
| `00-foundations/manifesto.md` | The 7-section manifesto | The manifesto structure uses the five elements as a verification gate. |
| `00-foundations/brand-voice.md` | Hard rules + two voice registers | Register B (customer testimonial) implements element 1 + 2 explicitly via the 5-beat formula. |
| `01-canon/cocktail-recipes.md` | The honest-attribution testimonial cocktail | The 5-beat formula is element 1 + 2 + 4 applied to the testimonial surface. |
| `.github/workflows/brand-voice-check.yml` | Qualifier-guard CI step | Enforces element 1 + 2 with the 200-char window. |

## How to extend the pattern

If you add a sixth load-bearing element, document it here (append-only) and update `00-foundations/positioning.md` in the same PR. Five is not magic; it is the current best architecture. Future iterations may add a Wall-3 element (e.g. regulatory geography), or a customer-segment element if the brand splits into multiple lines.

Do not remove an element. If the brand outgrows it, document the supersession and add a follow-on REFERENCE doc.
