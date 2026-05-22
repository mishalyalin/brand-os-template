# REFERENCE - the category-anchor reframe pattern

Owner: this is a reference / pattern document, not a brand-specific decision. Status: **canonical pattern**, do not delete.

This file documents WHY and HOW to shift the customer-side category your product sits in, without changing the legal classification of the product. The pattern is captured here so future Claude sessions and contributors can apply it to a brand before they edit anything else.

## When to use this pattern

Apply this pattern when all of the following are true:

1. Your product's **legal classification** (food / supplement / cosmetic / device) is locked and you do not want to change it.
2. Your product's **default customer-side category** (the one the customer's brain reaches for first when they see the price) is set at the wrong reference class.
3. The mismatch shows up as a pricing problem: the price feels "too expensive" against the customer's mental reference class, even though it is competitive against the actual peer set in the customer's life.

Classic shape: a premium food product priced like a supplement, but anchored in the customer's head against grocery-aisle peers, so the price feels wrong. Or: a productivity tool priced like a SaaS, but anchored against free apps, so the price feels wrong. Or: a piece of furniture priced like a long-life investment, but anchored against IKEA, so the price feels wrong.

If the customer is comparing your product to the wrong reference class, the price will always feel wrong, no matter how good the copy is. Fix the reference class first.

## The two-axis model

Every product has **two** category anchors:

- **Legal anchor** - what regulators / tax authorities / customs / VAT rules classify the product as. This is generally fixed by formulation, claim set, and packaging. You cannot move this without changing the product itself or its claim set.
- **Customer mental anchor** - what the customer's brain files the product under at first contact. This is set by copy, packaging visuals, retail context, pricing, and comparator brands named in the hero. This is fully under marketing control.

Most brand work assumes the two anchors must be the same. They do not. A food product can legally be classified as food (zero-rate VAT, food channels, food safety regulation) while customer-side living in the "discipline tool" category alongside non-food peers (training accessories, supplements, gym memberships).

The category-anchor reframe is the move that separates the two axes intentionally.

## How to do it

1. **Audit your current customer-side anchor**. Read your hero copy as a stranger. What is the first noun the customer's brain tags your product as? "Salt"? "Spice"? "Supplement"? "Drink"? Write it down.

2. **Audit your reference class against your price**. List the 5-7 brands the customer would compare you to if they accepted the current anchor. If your price is more than ~30% above the typical price in that reference class, your current anchor is wrong for your price.

3. **Pick the new customer-side category**. The new category should:
   - Have a typical price the customer is already paying happily (or aspiring to)
   - Solve a problem your product also solves
   - Sit in a budget your customer already has (mental account: "things I spend on for my goal")
   - NOT be a category your product cannot legally claim to be in
   - NOT be a category-fight you cannot win (do not pick a category dominated by a brand with 10x your budget)

4. **Pick the new peer set**. 4-6 brands your customer ALREADY pays for monthly that sit in the new category. Name them in internal canon documents. Decide per-surface whether to name them in customer copy or use abstractions ("less than your monthly gym").

5. **Rewrite the hero and PDP h1**. The hero copy must NOT use the old category noun as its primary product noun. Replace with a verb-led construction (Sutherland _Alchemy_ verb-not-noun) or a function-led construction or a problem-led construction. The product noun stays in the ingredient panel, the legal block, the regulatory documentation - never in the hero.

6. **Rewrite the price block**. Anchor against peers in the new category, not peers in the old category. Use mental-accounting language ("the line item in your X budget") rather than per-unit comparisons.

7. **Add Wall-2 hygiene to your CI**. Any future copy that uses the old category noun as a primary product noun fails the brand voice check.

8. **Document the decision**. Save a `YYYY-MM-DD-category-anchor-<your-new-anchor>.md` file in `06-decisions/` capturing the old anchor, the new anchor, the trigger event (usually a pricing problem), the alternatives considered, and the migration plan for existing surfaces.

## What this pattern does NOT do

- It does not change your product's legal classification. Your VAT treatment, food-safety rules, customs codes, ingredient panel, allergen declaration, regulatory claims set, all stay locked. The reframe is purely customer mental model.
- It does not give you license to make claims you could not make under the old anchor. Wall 1 (medicinal vocabulary) still applies. The new category does not unlock new claims.
- It does not work if your product is fundamentally in the old category and the price was always wrong for that reason. The reframe rescues a price that is right against the new peer set; it does not rescue a price that is wrong against any peer set.
- It does not work without commitment. Half-reframed brands (hero uses new category, PDP uses old category, paid social uses old category) confuse the customer worse than either anchor alone.

## How to verify a reframe held

Three checks at 30 / 60 / 90 days post-reframe:

1. **Customer reviews + UGC**. Do customers now describe the product in the new category language, or do they still default to the old? Search for the old category noun in reviews; if it shows up more than 20% of the time, the reframe has not taken.
2. **Price objection rate**. Compare the rate of "too expensive" complaints / cart abandons / refund-with-price-reason before and after the reframe. The reframe is working if the rate drops by 30%+ within 60 days.
3. **Repeat purchase / subscription retention**. Customers anchored in the right category renew. Customers anchored in the wrong category churn at the renewal moment, when the price hits the mental account again. Track 60-day retention against pre-reframe baseline.

If all three fail to move, the reframe is wrong for the brand. Either the peer set was wrong, or the price is wrong, or the product is genuinely not in the new category.

## Relationship to other canon

| Sibling file | What it owns | Relationship to this pattern |
|---|---|---|
| `00-foundations/positioning.md` | Mission + walls + content vectors | The Wall 2 (category-fight ban) is the wall this pattern routes around. |
| `00-foundations/manifesto.md` | 7-section brand manifesto | The "What we are not" block is the place where the old category noun appears, in negation form. |
| `01-canon/cocktail-recipes.md` | Cocktail "Category-anchor reframe (verb-not-noun)" | The cocktail is this pattern operationalised for hero copy. |
| `01-canon/cialdini-sutherland.md` | Sutherland verb-not-noun principle | The theoretical source for the verb-led construction. |
| `01-canon/pricing-mechanics.md` | Ramanujam pricing-by-reference-class | The theoretical source for "price is anchored by category, not by absolute number." |

## How to extend the pattern

If your brand later spans multiple customer-side categories (e.g. a product line targeting two distinct ICP segments living in different mental categories), capture each anchor separately as a labeled positioning anchor in the Brain (Layer 0), and route content vectors to the appropriate anchor per surface. The Brain's `for-vector` retrieval supports multiple anchors.

If your brand later changes its legal classification (e.g. food product moves to supplement classification, or vice versa), the customer-side anchor may need to change with it. Re-run the audit; do not assume the prior reframe survives a legal-classification change.

## Sources

- Sutherland _Alchemy_ ch. 2 - verb-not-noun product reveal
- Ramanujam-Tacke _Monetizing Innovation_ ch. 4 - reference-class price-anchoring
- Lakoff _Women, Fire, and Dangerous Things_ - mental categorisation under stress
- Ariely _Predictably Irrational_ ch. 1 - anchoring
