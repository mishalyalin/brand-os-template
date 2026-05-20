# Behavioural Economics Canon

Owner: Brand voice panel. Status: canonical reference. Version: be-canon-v1.0.0. Last updated: 2026-05-19.

Compressed reference for the sixteen behavioural economics principles that govern premium DTC funnel design. Each principle covers the canonical source, a one-line definition, the funnel stages where it lands hardest, and the places where it should NOT be used. The "where to use" guidance is pattern-level - adapt the implementation to your brand's actual touchpoints, product, and regulatory walls.

## The thesis in one paragraph

A premium DTC funnel is not a sales process. It is a sequence of cognitive frames, each engineered to make the next commitment feel smaller than it actually is. Each frame stacks two to three persuasion principles into a single felt state. Compound effect across a six-touchpoint funnel separates a 2 percent conversion from a 6 percent conversion. The funnel is not selling the product. It is constructing the frames that make the product the most rational thing to buy this week.

## The sixteen principles

### 1. Anchoring

**Canonical source:** Kahneman, _Thinking Fast and Slow_ (2011), Chapter 11. Ariely, _Predictably Irrational_ (2008), Chapter 2 wine-and-Social-Security-number experiment.

**One-line definition:** The first number a customer sees on a page recalibrates their sense of what every subsequent number means.

**Where to use:** Lander hero with a category-benchmark anchor below the fold. Pricing tier headers (retail price visible alongside subscription price). Price-objection email with a comparison list. PDP per-use breakdown (cost-per-meal / cost-per-use / cost-per-day anchored against a culturally comparable alternative).

**Where NOT to use:** Avoid putting the absolute price anywhere above the brand promise. The product hooks first; the price reads as obvious after the value frame is set.

### 2. The decoy effect (asymmetric dominance)

**Canonical source:** Ariely's Economist subscription experiment, _Predictably Irrational_ Chapter 1. Joel Huber and Christopher Puto, 1982 formalisation.

**One-line definition:** A third option that is clearly worse than option B but not clearly worse than option A makes option B feel like the obvious choice.

**Where to use:** PDP three-tier visual decoy at single-SKU launch (a worse-cadence subscribe, a recommended-cadence subscribe, a one-time purchase with explicit "no saving" labelling). Later phases with additional SKUs become a true three-tier SKU ladder.

**Where NOT to use:** Do not run a decoy that requires false claims. The one-time tier must genuinely lack the saving the subscription tier carries.

### 3. Loss aversion

**Canonical source:** Kahneman and Tversky's prospect theory, Econometrica 1979. Losses weighted approximately 2.25 times more heavily than equivalent gains.

**One-line definition:** Frame the offer as "what you will lose if you do not act" and the same incentive becomes 2.25x more motivating than "what you will gain if you act".

**Where to use:** Final-day urgency closer (walking-away language, real expiry). Cart abandon SMS with two or three loss axes (financial, time, opportunity). Post-signup "reserved in your name for 48 hours" framing.

**Where NOT to use:** Avoid stacking too many loss frames on the same screen. The reader becomes resistant if loss is mentioned in three consecutive sentences. One loss per touchpoint, well placed.

### 4. Default bias

**Canonical source:** Thaler and Sunstein, _Nudge_ (2008), Chapter 5. Organ-donation opt-in vs opt-out study showing ~70 percentage point difference.

**One-line definition:** Whatever option is pre-selected for the user becomes the option most users actually choose.

**Where to use:** PDP subscription tier as default selection. Email preference centre pre-selecting the sensible defaults rather than asking the user to opt into each stream individually.

**Where NOT to use:** Where local consent law forbids pre-checked opt-in (e.g. UK PECR forbids pre-checked SMS opt-in at checkout). Default must be unchecked where required, then over-merchandised with good copy that earns the active opt-in. Check `00-foundations/regulatory-frames.md` for your jurisdiction.

### 5. Social proof

**Canonical source:** Cialdini, _Influence_ (1984), Chapter 4. Asch conformity studies, 1951. Ariely's tip-jar starter-coins experiments, _Predictably Irrational_ Chapter 1.

**One-line definition:** The customer trusts a number, a name, or a story from a peer more than any claim from the brand itself.

**Where to use:** Structural-proof stack at pre-launch (third-party lab certification, regulatory registrations, transparent ingredient or component declaration). Founder credential transfer (a verifiable prior-industry track record as authority anchor). Review widget from launch onward, including the empty-state.

**Where NOT to use:** Do not fake review counts or customer counts. A real small number beats a fake large number. Numbers without a verifiable source do not ship.

### 6. Scarcity

**Canonical source:** Cialdini, _Influence_, Chapter 7. Brehm reactance theory, 1966. Ariely on honest scarcity in _The (Honest) Truth About Dishonesty_ (2012).

**One-line definition:** Honest scarcity (limited stock, time-bound offer with a real deadline) increases urgency; dishonest scarcity (perpetual "24 hours left" countdowns) destroys trust over the customer lifetime.

**Where to use:** Real production batch scarcity ("First batch: N units. Next batch ships from [supplier] in [month]." - based on actual production cadence). Real time-bound code expiry (signup code with a fixed window that actually expires).

**Where NOT to use:** Banned: hero countdown timers that reset, "only X left" counters that never go to zero, "selling fast" badges with no underlying truth. See `07-anti-patterns/` for the regulatory exposure in your jurisdiction.

### 7. The endowment effect

**Canonical source:** Thaler, Kahneman and Knetsch's mug experiment, Journal of Political Economy 1990. Ariely's "I, Mine" chapter in _Predictably Irrational_.

**One-line definition:** The moment something feels "yours", giving it up feels like losing a possession - even if you never paid for it.

**Where to use:** Possessive framing throughout post-signup ("your code", "your bonus is reserved", "your first box is queued"). Win-state moments that explicitly transfer ownership of a code, bonus, or perk.

**Where NOT to use:** Pre-signup. A bonus is "the bonus" until the customer has earned it through signup; only then does it become "your bonus".

### 8. The free-as-cue effect

**Canonical source:** Ariely, _Predictably Irrational_, Chapter 3 "The Cost of Zero Cost". Lindt Truffle / Hershey's Kiss experiment.

**One-line definition:** The word "free" disproportionately attracts attention and reduces decision friction. A small free gift outperforms a much larger percentage discount.

**Where to use:** Lander hero leading with "Free [bonus] with your first [purchase]" not "Save X% on your first [purchase]". Bonus itemised at retail value with strikethrough.

**Where NOT to use:** Do not lead with free if the free thing is not yet genuinely allocated. Every "free" claim must trace to an actual budgeted line item.

### 9. Mental accounting

**Canonical source:** Thaler, "Mental Accounting Matters", Journal of Behavioral Decision Making, 1999.

**One-line definition:** The customer's perceived cost depends entirely on which mental account they slot the purchase into.

**Where to use:** Three-axis price framing (per-box, per-use, per-week). Explicit mental-account substitution in the price-objection email ("Slot it in your [appropriate budget category], not your [adjacent more-restrictive budget category]").

**Where NOT to use:** Reframing into a mental account that crosses one of your brand's regulatory walls (e.g. a food brand reframing into a "wellness budget" can push the brand toward a medicinal register). Check the reframing against `00-foundations/regulatory-frames.md`.

### 10. The peak-end rule

**Canonical source:** Kahneman et al, "When more pain is preferred to less", Psychological Science 1993. Kahneman, _Thinking Fast and Slow_ Chapter 35.

**One-line definition:** The customer's memory of the funnel will be shaped almost entirely by its emotional peak (the win moment) and its end (the unboxing).

**Where to use:** Peak amplification at the signup win-state. End amplification at unboxing (handwritten note, surprise bonus on top of the box, a tactile artefact designed as an end-experience object).

**Where NOT to use:** Do not design the peak around an exclamation-mark or emoji burst if your voice rules forbid both. The peak in an editorial voice is a quiet, well-chosen line rather than effusive celebration.

### 11. Identity priming

**Canonical source:** Ariely, _The Upside of Irrationality_ (2010), Chapters 1 and 4. Self-signalling theory, Bodner and Prelec 2003.

**One-line definition:** The funnel works better when it gets the customer to identify themselves as a kind of person, not just buy a product.

**Where to use:** Capture popup identity question ("Which of these sounds most like you tonight?" with category-native options). Lander closing line that names the kind of person the brand is for. Founder note framing identity (family, craft, ritual, lifestyle - whatever the brand legitimately occupies).

**Where NOT to use:** Identity priming must NOT cross one of your brand's regulatory walls. For example, a food brand should not prime medicinal identity ("I am someone who supports my immune system"). Keep identity priming inside your category's legitimate register.

### 12. The IKEA effect

**Canonical source:** Norton, Mochon and Ariely, Journal of Consumer Psychology 2012, "The IKEA effect: When labor leads to love".

**One-line definition:** The more the customer does to personalise or build the product, the more they value what they end up with.

**Where to use:** Lander "build your profile" three-question quiz. Personalised onboarding ("Pick the three of these seven that you actually [use / cook / wear / etc.]"). Month-3 retention email asking the customer to shape the next product iteration.

**Where NOT to use:** Avoid making the customer build the product before the first purchase if the build complexity is high. Three questions is the right ceiling; seven questions is the wrong floor.

### 13. Pain of paying

**Canonical source:** Prelec and Loewenstein, "The Red and the Black", Marketing Science 1998. Ariely and Kreisler, _Dollars and Sense_ (2017), Chapter 9.

**One-line definition:** Anything that smooths, hides, or pre-pays the moment of payment increases conversion. Anything that visibly extracts money decreases it.

**Where to use:** One-tap wallet checkout (Apple Pay, Shop Pay, Google Pay) as primary buttons above card-entry. Tax-treatment framing as explicit pain-reduction signal where the brand has a genuine tax advantage to communicate. Subscription as "charged on each shipment, not today".

**Where NOT to use:** Do not hide the price entirely. The pain of paying is reduced by smoothing the moment, not by concealing the cost. Concealment is likely to fall foul of consumer-protection law in your jurisdiction (check `00-foundations/regulatory-frames.md`).

### 14. Reciprocity priming

**Canonical source:** Cialdini, _Influence_, Chapter 2 "Reciprocation". Ariely's gift-economy work, _Predictably Irrational_ Chapter 4.

**One-line definition:** A small unexpected gift, given before any ask, biases the recipient strongly toward saying yes to a subsequent request.

**Where to use:** Personal founder DM video (asymmetric reciprocity - unscalable founder hours are exactly what makes it credible). Founder-story email opening with a tangible guide or asset given upfront. P.S. line linking to a permanently-free resource ("The [guide] is always at [URL]. Free. No signup."). Unannounced unboxing bonus on top of the primary product.

**Where NOT to use:** Do not stack reciprocity with high-pressure urgency in the same touchpoint. The gift moves the relationship into social-norms; mixing it with market-norm urgency cancels the effect.

### 15. Status quo bias

**Canonical source:** Samuelson and Zeckhauser, "Status Quo Bias in Decision Making", Journal of Risk and Uncertainty 1988.

**One-line definition:** Once the customer is on subscription, they will stay on subscription unless something actively dislodges them.

**Where to use:** Subscription default architecture. Anniversary email framing renewal as continuation ("One box, done. The next one ships in N days."). Continuity gifts at predictable retention checkpoints (months 2 through 6).

**Where NOT to use:** Do not use cancellation friction as a status-quo defence. Commit to one-click cancel. Continuity gifts and content do the retention work instead of friction.

### 16. Phantom commitment manufacturing

**Canonical source:** Compound mechanic. Closest single sources: Freedman and Fraser foot-in-the-door, Journal of Personality and Social Psychology 1966. Cialdini commitment-and-consistency, _Influence_ Chapter 3. Ariely confabulation experiments, _Predictably Irrational_ Chapter 5.

**One-line definition:** Construct a phantom commitment state - "your cart", "your box", "your reserved code" - that exploits memory uncertainty, status-quo verbs ("continue"), and foot-in-the-door bridging to make the user feel they have already committed when they have not.

**Where to use:** ONLY via a transparency-engineered variant where the phantom-state attaches to things the brand genuinely has reserved (the code, the discount, the bonus), never to a fictional cart. See `02-funnel-architecture/cart-abandon-cascade.md` and the relevant `06-decisions/` record for the brand-safe implementation.

**Where NOT to use:** Direct copy of a competitor's "Your Cart" subject line when no cart actually exists. This is likely to breach consumer-protection law on misleading commercial practices in most jurisdictions. The mechanism is too valuable to skip; the literal deceptive copy is too exposed to use.

## The six-lever cocktail (a phantom-commitment hero case)

When a brand manufactures a phantom-commitment moment well, the cocktail typically stacks six BE principles in a single 60-90 word email:

1. Endowment via possessive ("Your [thing]")
2. Loss aversion via incompleteness ("Just one step left!")
3. Cialdini commitment-consistency (signup framed as the first half of a single decision)
4. Confabulation bait (memory uncertainty over the recent window)
5. Status-quo continuation verb ("CONTINUE")
6. Foot-in-the-door bridging (signup is the small commitment, checkout is the large commitment)

Each lever alone produces a modest conversion lift. Stacked, they produce a disproportionately large lift because the user's defences against each individual principle are different. Anchoring is defeated by experience with the category. Loss aversion is defeated by abundance mindset. Reciprocity is defeated by suspicion of motives. When an email simultaneously anchors a number, frames non-action as loss, and triggers reciprocity through a costly signal, the customer's defences are in three different fights at once. The composite resistance falls faster than any single defence.

See `01-canon/cocktail-recipes.md` for the full stacked-principle reference.

## Sources

- Sources cited above per principle. Ariely _Predictably Irrational_ (2008), Kahneman _Thinking Fast and Slow_ (2011), Thaler and Sunstein _Nudge_ (2008), Cialdini _Influence_ (1984), Kahneman and Tversky _Econometrica_ 1979, Thaler _Mental Accounting Matters_ 1999.

## What this file does not do

- It does not contain brand-specific copy upgrades. Those live in `02-funnel-architecture/` and per-touchpoint files in `03-touchpoint-copy/`.
- It does not contain anti-patterns. Those live in `07-anti-patterns/`.
- It does not contain unresolved open questions. Those live in `06-decisions/` once the brand owner resolves them.

## Version

- `voice-v0.1.0` aligned.
- `regulatory-v1.0.0` aligned (apply your brand's regulatory frames from `00-foundations/regulatory-frames.md`).
