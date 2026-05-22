# REFERENCE - context exclusion pattern (targeting rule, not gatekeeping rule)

Owner: this is a reference / pattern document, not a brand-specific decision. Status: **canonical pattern**, do not delete.

This file documents the rule that scopes target-market exclusions based on customer-baseline reality, while keeping the brand welcoming to anyone who finds it and chooses to buy. The pattern is captured here so future Claude sessions and contributors apply it without conflating an exclusion with a gatekeeping mechanism.

## The rule

**Not all target markets share the pain your product solves. Exclude markets where the pain does not land from your acquisition targeting (paid social geo, creator partnerships, IG / TikTok briefs, PR pitches). Welcome anyone who finds the brand organically and chooses to buy. The exclusion is a targeting rule, not a gatekeeping rule.**

The exclusion criterion can be:
- **Palate / culinary tradition** (food brand whose pain is "bland disciplined eating" - excluded markets are high-spice-tradition palates)
- **Climate** (winter-coat brand - excluded markets are tropical year-round)
- **Life stage** (newborn-baby gear - excluded segments are non-parents)
- **Income tier** (premium brand - excluded segments cannot afford the price tier regardless of fit)
- **Existing-solution density** (productivity tool whose pain is "no calendar exists" - excluded markets already saturate on Outlook / Google Calendar)
- **Cultural / regulatory** (alcohol brand in dry-country markets, gambling product in restricted jurisdictions)

The exclusion is honest: the brand acknowledges it cannot solve the pain for that audience as a daily reality. The brand stays welcoming: anyone in that audience who wants the brand for reasons outside the canonical pain-fit is a customer regardless.

## When to use this pattern

Apply this pattern when ALL of the following are true:

1. Your product solves a specific pain.
2. That pain has clear preconditions (a customer baseline state that must be true for the pain to land).
3. Some demographics / geographies / segments do not meet those preconditions through no fault of their own.
4. Targeting those audiences in acquisition copy would waste budget on people for whom the pain does not exist as a daily condition.

Without those four, the exclusion is just demographic targeting and the gatekeeping confusion does not arise.

## Why "targeting, not gatekeeping" matters

The wording is load-bearing. Here is why.

**Gatekeeping mechanism** = "we will not sell to X audience". This reads as exclusion-as-judgement and creates legal exposure under anti-discrimination law in many jurisdictions. It also alienates X audience members who would have been customers regardless of the brand's targeting choice.

**Targeting rule** = "we will not target X audience in our acquisition channels because the pain we solve does not land for them as a daily condition; we welcome anyone from X who finds us and wants to buy". This reads as honest product-pain-fit and creates no legal exposure - it is a marketing-spend allocation decision, not a sale-of-goods restriction.

Always frame the exclusion as targeting. The "anyone who finds us and chooses to buy is welcomed" clause is part of the rule, not an afterthought.

## What the exclusion affects

1. **Paid social geo + interest targeting** - excluded markets / interests are off the targeting list. Lookalike audiences exclude them.
2. **Creator / influencer partnerships** - excluded-audience creators are not Phase 1 acquisition partners.
3. **Content briefs** (IG / TikTok / YouTube) - the implied reader is not from the excluded segment.
4. **PR pitches** - excluded-audience publications are not Phase 1 outreach priority.
5. **Email subject lines + cold copy** - the implied reader is not from the excluded segment.

## What the exclusion does NOT affect

1. **Customer acquisition through organic search / direct / referral** - anyone who searches for the brand and lands on the site is treated identically regardless of segment.
2. **Customer service** - any customer is supported, no segment-based escalation.
3. **Returns / refunds** - same policy for all customers.
4. **Welcome flow + retention** - customer journey is identical regardless of segment.
5. **Phase 2+ expansion** - the exclusion is a Phase 1 acquisition-targeting rule. Phase 2 may revisit if data justifies.

## How to apply the rule cleanly

1. **Identify the pain preconditions explicitly**. What does the customer baseline need to be for your pain to land? Write this down.

2. **Map pain preconditions to demographic / geographic / segment markers**. Which audiences fail those preconditions through their baseline reality?

3. **Build the include / exclude lists**. Be specific - not "Asia" but "high-spice-tradition home-cooking palates such as India, Pakistan, Bangladesh, Thailand, Korea, Vietnam". Specificity protects you from over-inclusion.

4. **Document the rule**. Save to `06-decisions/<date>-context-exclusion-<criterion>.md`. Capture: what is excluded, why preconditions do not land, that this is targeting-not-gatekeeping, what Phase 2 reconsideration looks like.

5. **Wire into operational surfaces**. Paid social settings, creator briefs, content brief templates, PR pitch lists.

6. **Refresh quarterly**. Targeting decisions get re-audited as data lands. Exclusion is not a permanent strategic-segment decision.

## Banned framings (do not use these in customer copy)

| Anti-pattern (reads as gatekeeping) | Safe (reads as honest targeting) |
|---|---|
| "Pranasalt is not for [excluded audience]" | "Pranasalt is built for [pain-fit audience]" |
| "We do not sell to [excluded audience]" | "We do not target [excluded audience] in our acquisition channels because the pain we solve does not land there as a daily condition" |
| "X audience cannot benefit from our product" | "X audience already has a solution to this pain through their daily baseline; we welcome them if they choose us regardless" |
| "Our brand is exclusively for [included audience]" | "Our brand is built around [included audience's pain]; anyone who finds us and wants to buy is welcomed" |

## How to verify the rule is working

Three checks at 60 / 90 days post-implementation:

1. **Wasted-spend audit on paid social**. Paid social spend should not be reaching excluded audiences. If it is, the targeting setup is leaking.
2. **Customer mix audit**. The percentage of customers from excluded segments should be small (low single digits) and primarily organic-discovery. If it is large, either the exclusion is wrong (Phase 2 expansion data) or the targeting is leaking (operational fix).
3. **Legal / PR exposure check**. No customer service ticket / complaint / press inquiry framing the brand as discriminatory should land. If one does, audit the customer-copy framings for accidental gatekeeping language.

## Relationship to other canon

| Sibling file | What it owns | Relationship to this pattern |
|---|---|---|
| `00-foundations/positioning.md` | ICP + content vectors + walls | The ICP definition gets the exclusion clause appended. |
| `00-foundations/voice-anti-patterns.md` | Anti-pattern list | The customer-copy framings are captured as an anti-pattern with banned / safe before-after tables. |
| `06-decisions/REFERENCE-pmf-sequencing-phase1-narrow-phase2-expand.md` | Phase 1 / Phase 2 sequencing | The exclusion rule + sequencing rule work together; both protect the Phase 1 brand mental category. |
| `04-content-rules/<roadmap>.md` | Phase 1 launch markets list | The exclusion is operationalised as an include / exclude geography table in the product roadmap or launch plan. |

## How to extend the rule

If your brand later launches in a previously-excluded market (Phase 2+ expansion data justifies it), capture the data + reasoning in a new decision record and update the include / exclude tables. Do not silently lift the exclusion - leave a record so the rationale is auditable.

If your brand observes high organic-discovery conversion from an excluded audience (people are finding you and buying regardless), that is informative. Either the exclusion is wrong (pain DOES land for them) or the segment self-selects on a non-canonical pain-fit (they want your product for reasons outside your canonical pain-fit). Investigate before changing the exclusion.

## Sources

- Cialdini _Influence_ ch. 5 (Liking) - liking-based heuristics include matching pain to audience; mismatched pain reads as inauthentic
- Sutherland _Alchemy_ ch. 2 (verb-not-noun) - the product is defined by what it does for someone; defining who it doesn't do that for is part of the same clarity
- Bohner-Einwiller-Erb-Siebler 2003 _JCP_ 13(4) (Pratfall) - acknowledging where the brand cannot solve the problem builds trust with audiences where the brand can
- Crossing the Chasm (Geoffrey Moore, 1991) - early-market focus on a single beachhead vertical is the canonical exclusion pattern at scale
- UK Equality Act 2010 + EU GDPR + US Civil Rights Act - the legal frame for why targeting rules and gatekeeping mechanisms are different
