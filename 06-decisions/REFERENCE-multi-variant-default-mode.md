# REFERENCE - the multi-variant default output mode

Owner: this is a reference / pattern document, not a brand-specific decision. Status: **canonical pattern**, do not delete.

This file documents the default output format for any customer-facing copy generation request. The pattern is captured here so future Claude sessions, the Brain CLI, and contributors emit the same shape of output without needing to re-invent it per surface.

## The rule

For any customer-facing copy generation slot (hero, PDP h1, ad headline, email subject + preview, microcopy, captions, push, SMS, founder essay opener, press boilerplate, About openers, welcome-flow openings), the default output is **N variants (4-6) per slot**, each:

- Cited to a specific canon principle (Layer 0 / BE / Voss-NSTD / Cialdini-Sutherland / DTC / Pricing / LLM SEO)
- Tagged with Wall-1 and Wall-2 hygiene status (OK or Risk)
- Star-weighted on a 1-5 scale based on lens-fit + Misha-veto risk + load-bearing principles served
- One variant marked PREFERRED with a one-sentence rationale

Single-variant mode is reserved. The trigger list below is bounded; do not multi-variant on every micro-decision.

## Why this is the default

A single-variant output ("here is my best draft") asks the decider to either accept or reject blind. Three problems follow:

1. **Decision invisibility**. The decider does not see the option space. Whether the draft is good is a question they cannot answer without seeing what was rejected.
2. **No canon citation**. A single draft is hard to argue with because the rationale is implicit. Multi-variant forces every option to declare its canon source, which makes the rationale legible (and rejection legible).
3. **No A/B ladder**. The same content is going to need testing anyway. Generating the test slate during the draft step is cheaper than retroactively building it after the chosen draft fails.

Multi-variant mode does three jobs at once with the same effort.

## Output format (canonical table)

| # | Variant copy | Lens / canon principle | Wall-1 | Wall-2 | Stars | Notes |
|---|---|---|---|---|---|---|
| A | _line A_ | _e.g. Layer 0 ICP vector V1_ | OK / Risk | OK / Risk | ★★★★ | _why this might win_ |
| B | _line B_ | _e.g. BE - loss aversion_ | OK / Risk | OK / Risk | ★★★ | _why this might win_ |
| C | _line C_ | _e.g. Voss - calibrated label_ | OK / Risk | OK / Risk | ★★★★★ | PREFERRED. _why._ |
| D | _line D_ | _e.g. Cialdini Unity (community identity close)_ | OK / Risk | OK / Risk | ★★ | _why this might lose_ |
| E | _line E_ | _e.g. Sutherland verb-not-noun_ | OK / Risk | OK / Risk | ★★★ | _why this is the safe fallback_ |

Optional 6th variant if the surface has a hard split (cold vs warm audience, mobile vs desktop hero, EU vs US copy). Skip a slot if the lens does not apply to the surface (e.g. Pricing lens skipped on identity-close microcopy).

## Star calibration

- ★ (1 star) - include for completeness, expected to underperform; useful as the floor of the test range
- ★★ (2 stars) - solid, might surprise
- ★★★ (3 stars) - strong default, no obvious risk
- ★★★★ (4 stars) - strong + carries one extra load-bearing principle the surface needs
- ★★★★★ (5 stars) - PREFERRED, all load-bearing principles for the surface satisfied + lowest decider-veto risk

## When multi-variant mode fires (default ON)

- Hero copy / brand mark headline
- PDP h1 + first sub-line
- Ad headline (paid social, paid search)
- Email subject line + preview text
- Microcopy (CTA button, form labels, error messages where tone matters)
- IG / TikTok captions
- Push notifications + SMS body
- Founder essay opening (the first 1-3 sentences set the register)
- Press boilerplate
- About page section openers
- Welcome-flow email openings

## When single-variant mode applies (multi-variant OFF)

- Locked canon (manifesto, mission statement V1, hero 3-line, "What we believe" 5-line block, "What we are not" negation lines, identity close, founder sign-off)
- Single-word labels (community name, founder first name, brand name, pillar words)
- Time-sensitive ops (a SLA-bounded reply, a hot CS response, a within-the-hour social post)
- Surfaces where the brand owner has already specified the exact wording
- Legal / regulatory copy (ingredient panel, allergen declaration, VAT footer, refund policy)
- Schema.org structured-data text (uses the locked product name + locked description)

## Slate composition recommendation

For most customer-facing copy slots, the 4-6 variants should span:

- 1 variant from **Layer 0** (ICP / content vector / Wall hygiene)
- 1 variant from **Behavioral Economics** (anchoring / loss aversion / mental accounting / endowment)
- 1 variant from **Voss / NSTD** (calibrated question / label / no-oriented / accusation audit)
- 1 variant from **Cialdini-Sutherland** (Unity / Pratfall / verb-not-noun / costly signal)
- 1 variant from **DTC mechanics or Subscription mechanics** (founder-voice / day-7 review / pause-not-cancel / anti-discount)
- 0-1 variant from **Pricing or LLM SEO mechanics** (if the surface has price or entity-citation exposure)

Skip lenses where they do not apply. Lean into 2 variants of the same lens where one lens clearly dominates the surface.

## How to mark a variant PREFERRED

The PREFERRED variant is the one where ALL of the following are true:

1. It satisfies every load-bearing principle for the surface (e.g. for a manifesto hero, all five load-bearing positioning elements; for a price block, the protocol-stack comparator; for a testimonial, the 5-beat formula).
2. It has the lowest decider-veto risk (no policy violations, no Wall-1/Wall-2 issues, no jargon flags, no risk of being misread).
3. It is internally consistent with the other surfaces in the same campaign (no conflict with the hero, the manifesto, the founder essay).

If no variant clears all three, the draft is not ready. Iterate before marking any variant PREFERRED.

## What this pattern does NOT do

- Does not replace locked-canon surfaces. Manifesto, mission, hero 3-line, identity close, founder sign-off all stay single-variant by design.
- Does not waste effort on locked-canon surfaces. The trigger list is bounded; do not generate 4-6 variants of "-misha" or "[Brand Name]".
- Does not generate variants without canon-citation. Every variant must trace to a specific principle or it does not count.
- Does not require all 4-6 variants to be useable. Including a 1-star variant is fine and informative; the slate is the deliverable, not just the PREFERRED.

## Relationship to other canon

| Sibling file | What it owns | Relationship to this pattern |
|---|---|---|
| `01-canon/cocktail-recipes.md` | Cocktail "Multi-variant decision-support cocktail" | The cocktail is this pattern operationalised. |
| `00-foundations/positioning.md` | Mission + walls + content vectors | The slate composition uses the Layer 0 anchors as the first slot. |
| `00-foundations/brand-voice.md` | Hard rules + two voice registers | Every variant passes the same hard-rule scan; multi-variant does not bypass voice rules. |
| `01-canon/behavioral-economics.md` + `nstd-tactics.md` + `cialdini-sutherland.md` + `dtc-mechanics.md` + `subscription-mechanics.md` + `pricing-mechanics.md` + `llm-seo-canon.md` | The 88 canon principles | Each variant cites a principle from one of these schools. |
| Brain CLI `search` / `tactic` / `for-stage` / `for-vector` outputs | Surface-to-canon retrieval | The Brain returns a recommended slate (lens combination) that becomes the input to the multi-variant draft. |

## How to extend the pattern

If your brand later adds a new canon school (e.g. category-specific science, brand-tone evidence, regulatory schools), include it in the slate composition recommendation for the surfaces where it applies. Update the slate-composition table in this file in the same PR.

If your brand later changes its voice register (e.g. a previously serious brand softens to playful), the variant slate can carry the register shift across surfaces by adding a register-tagged variant per slot. The shift becomes legible across the test slate before locking into canon.

## Sources

- Ariely _Predictably Irrational_ ch. 1 + Williams-Sonoma 1992 - decoy effect proves the slate effect (the option set shapes the choice as much as the option content)
- Sutherland _Alchemy_ ch. 4 - satisficing-at-acquisition (4-6 options is the cognitive sweet spot for human deciders)
- Sutherland _Alchemy_ ch. 8 - sweat-the-small-stuff (multi-variant on microcopy demonstrates care)
- Bohner-Einwiller-Erb-Siebler 2003 _JCP_ 13(4) - Pratfall (showing weaker variants alongside the strong one increases trust in the chosen variant)
- Iyengar-Lepper 2000 _JPSP_ - jam-shop (24 options reduce conversion; 4-6 is the optimal range)
