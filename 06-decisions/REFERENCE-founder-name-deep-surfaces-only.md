# REFERENCE - founder name in deep surfaces only (shallow-surface ban)

Owner: this is a reference / pattern document, not a brand-specific decision. Status: **canonical pattern**, do not delete.

This file documents an architecture pattern: the founder's NAME is banned from shallow customer-facing surfaces (hero, manifesto top, PDP h1, paid ad copy, IG bio, welcome modal, microcopy, captions, SMS, email subject, push notification, sticky CTA). The name is allowed in deep surfaces (About, founder essay body, welcome flow E3 founder pivot, monthly notes, podcast intro, Reddit AMA, internal docs) and at the sign-off close on long-form deep surfaces (e.g. `-<firstname>`).

The pattern is optional. Apply it when your founder is not celebrity-grade AND the brand name does not equal founder identity. KIND (Lubetzky), Patagonia (Chouinard), IM8 (Beckham) - founder name carries pre-loaded authority, so naming in shallow surfaces is a costly signal. LMNT, Olipop, Magic Spoon, Liquid Death, AG1 - founder lives deep, brand name carries the brand, name appears only after the reader has self-selected into wanting context.

## What the pattern is

Two surface tiers, two visibility rules:

1. **Shallow surfaces** are first-touch, no-context entries: hero block, manifesto opening line, PDP h1, IG bio line, welcome modal, push notification, SMS preview, email subject line, paid-ad creative, sticky CTA, microcopy that anyone sees before reading the brand arc. The founder name is BANNED in these surfaces.
2. **Deep surfaces** are second-or-third touch: About page body, founder essay long-form, welcome flow E3 founder-pivot email body, monthly founder notes, podcast intro, Reddit AMA, customer-support reply where the customer has asked who the founder is. The founder name is ALLOWED in these surfaces because the reader has self-selected into wanting that context.
3. **Sign-off close** on long-form deep surfaces (e.g. `-<firstname>` at the bottom of a 600-word founder essay) is the canonical identity-reveal-after-problem-frame pattern. The reader has earned the name by reading the arc; the name pays off the arc, does not precede it.

## Why each piece is load-bearing

### Founder name carries pre-loaded reference class

When a stranger sees a founder name in shallow copy, they auto-search their memory for that name. If the name has pre-loaded authority (Beckham, Chouinard, Lubetzky, Musk, Cuban), the reference class lands and the shallow-surface name acts as a costly-signal anchor. If the name has no pre-loaded authority (most founder names), the reader's auto-search returns no match, and the name reads as a stranger's name in a place where the brand should be carrying the load. The brand loses voice; the founder gets pushed where they do not yet carry weight.

### Deep surfaces have already earned the reader's attention

By the time the reader reaches an About page body or a founder essay, they have consented to wanting founder context. Naming the founder here serves the arc: WHO the brand is becomes a question the reader is asking, and the answer rewards their attention. The same name in a hero block would have arrived before the question existed.

### Sign-off close pays off the arc

`-<firstname>` at the bottom of a long-form essay is the moment of identity reveal. The reader has read the discipline arc, the founder's experience, the brand thesis; now the brand attributes the voice to a specific human. This pattern is documented in long-form direct-response copywriting (Caples, Ogilvy) and works because the name lands as resolution, not as introduction.

### Co-founder names get a stricter rule

Co-founder names (the COO, the technical co-founder, the family co-founder) carry less arc weight than the primary founder. Treat co-founder names as BANNED in customer copy entirely. Their roles can appear ("our COO" / "my co-founder" / "the founders"), but not their names. Apply this strictly unless the co-founder is celebrity-grade.

### Family names get an even stricter rule

Children's names, spouse's name, parents' names - BANNED in all customer copy. Children are not product-credential. The founder's family is their own story to tell, not the brand's leverage to use. If the brand wants to surface family context, do it generically ("his kids" / "her family" / "the founders' family"), not by name.

## How to apply the pattern in your Brand OS

### Step 1 - decide if the pattern fits your brand

Test: would a knowledgeable consumer recognise your founder's name on sight? If yes (celebrity-grade), the pattern is optional - founder name in shallow surfaces is a costly signal that pays off.

If no (most brands), apply the pattern. The founder name belongs in deep surfaces where the reader has consented to wanting it.

Test: does your brand name equal the founder's name (e.g. "Tory Burch", "Jenny Craig", "Bobbi Brown")? If yes, the pattern needs adaptation - the brand name surfaces the founder name by definition. In those cases, the founder name in the brand name is the founder reveal, and the actual person's first name still follows the shallow / deep rule.

### Step 2 - sweep your customer-copy surfaces

Audit every customer-facing file for founder name occurrences. The common places:

- Manifesto (top section, hero block)
- PDP credential block ("Built by [Founder]")
- About page intro (above the fold)
- Welcome modal copy
- Welcome flow emails (E1 + E2 in particular)
- Cart-abandon emails
- IG bio
- Press boilerplate
- Sticky CTA / chat-bubble greeting

For each occurrence, classify the surface as shallow or deep. Shallow surfaces get the name removed and replaced with brand-led language ("we" / "the founders" / "the brand" / role-based naming). Deep surfaces keep the name.

### Step 3 - rewrite the shallow-surface copy

Common rewrites:

| Shallow-surface original | Shallow-surface fix |
|---|---|
| `Built by [Founder Name]` | `Built by the founders of [previous credential]` |
| `[Founder Name] writes them by hand` | `We write them by hand` or `Every email is written by hand` |
| `Replies go straight to [Founder]` | `Replies go straight to us` or `We read every reply` |
| `[Founder]'s family recipe` | `An [origin]-rooted recipe` or `A recipe [we / the founders] spent N years developing` |
| `Hi, I'm [Founder]` (hero) | `Welcome` or `You're in` or no greeting at all |

### Step 4 - keep the deep-surface name + sign-off

Do NOT remove the founder name from the About page, founder essay body, founder-pivot email E3, podcast intros, or sign-off close. Those surfaces earn the name.

The sign-off close convention is `-<firstname>` at the bottom of long-form deep-surface essays. Keep short hyphen, lowercase first name (or however the founder signs their name; consistency matters). The dash is a signature mark, not punctuation.

### Step 5 - document the rule in your voice-anti-patterns.md

Add an anti-pattern entry for "Founder name in shallow customer-facing surfaces" with a banned-to-safe before-after table covering 6-8 patterns. This makes the rule CI-scannable and visible to future contributors.

### Step 6 - lock the decision

File a date-stamped decision record in `06-decisions/<date>-founder-name-deep-surfaces-only.md`. Include the trigger event, the rule, the shallow / deep / sign-off surface lists, alternatives considered, cross-brand precedents (KIND / Patagonia / IM8 vs LMNT / Olipop / Magic Spoon / Liquid Death / AG1), trigger conditions for re-evaluation.

## When NOT to apply the pattern

Three situations where the pattern is wrong:

1. **Your founder is celebrity-grade.** Beckham at IM8, Chouinard at Patagonia, Musk at Tesla, Cuban at Mavericks-adjacent ventures. The name carries authority; shallow-surface naming is a costly signal that pays off.
2. **Your brand name equals founder identity.** KIND (Daniel Lubetzky's grandfather lineage), Bobbi Brown, Tory Burch, Jenny Craig. The brand IS the founder; the name surfaces by definition.
3. **Your brand voice is intentionally founder-first.** A small-batch artisan brand where the founder is the product (a sommelier's wine label, a chef's hot sauce, a luthier's guitars). The founder name is the brand asset; shallow-surface visibility serves the product positioning.

If none of these apply to your brand, apply the pattern.

## How to verify the pattern is working

After setup:

- `grep -i '<founder firstname>' 00-foundations/manifesto.md 03-touchpoint-copy/**/*.md 08-templates/*.md` returns zero hits in shallow-surface sections.
- The same grep returns expected hits in About / founder-essay / welcome-flow E3 / `-<firstname>` sign-off close lines.
- A fresh customer session reaches the founder's name only after reading the brand arc (manifesto + hero + What we do), not before.
- The voice-anti-patterns.md entry exists with the banned-to-safe table.
- A decision record exists in `06-decisions/`.

If any check fails, fix the surface or the rule definition before shipping more customer copy.

## Relationship to other canon

| Sibling file | What it owns | Relationship to this pattern |
|---|---|---|
| `00-foundations/positioning.md` POS-FORBIDS | Forbidden phrasings and constructions | Founder-name shallow-surface ban + family-protect rule lives here. |
| `00-foundations/voice-anti-patterns.md` | Anti-pattern catalogue with banned-to-safe tables | Add an entry for the founder-name shallow-surface ban with 6-8 banned-to-safe examples. |
| `00-foundations/founder-stories.md` | The founder narrative source-of-truth | Deep-surface founder content lives here. Reference from About + founder essay + welcome flow E3. |
| `00-foundations/manifesto.md` | The 7-section brand manifesto | Apply the pattern to the manifesto: founder name NEVER in the top sections, allowed only at `-<firstname>` sign-off close. |
| `01-canon/cocktail-recipes.md` | Cocktails for specific funnel moments | The "Club + Community" or equivalent cocktail Recipe layers use "we" / "members" / "the founders", never the founder name in shallow surfaces. |
| `06-decisions/<date>-founder-name-deep-surfaces-only.md` | Locked decision | File when you adopt the pattern. |

## How to extend the pattern

If your brand grows to a multi-founder profile (the original founder + a high-profile partner / advisor), the rule applies to each founder's name individually based on celebrity-grade test. The strictest variant: only the original founder appears in deep surfaces and the sign-off close; partners and advisors appear only by role ("our advisor [role]", "our co-founder").

If your brand evolves into celebrity-grade founder territory (founder becomes a public figure during the brand's life), re-open the decision via the trigger-conditions table. Add the founder name to shallow surfaces incrementally; do not rip the pattern out wholesale.

## When a brand adopts this pattern, the artefacts to ship

- `06-decisions/<date>-founder-name-deep-surfaces-only.md` locked decision record
- `00-foundations/voice-anti-patterns.md` new anti-pattern entry with a banned-to-safe before-after table covering 6-8 shallow surfaces
- `00-foundations/positioning.md` POS-FORBIDS extended with the shallow-surface ban + co-founder-name ban + family-name ban
- Customer-copy sweep across: manifesto, PDP, founder statement template, testimonial template, welcome-flow SMS + emails, cart-abandon emails, About page intro, IG bio line, press boilerplate, brand-guidelines HTML

Typical first-PR sweep covers 8-12 files. Decision-record body should cite cross-brand precedents (which brands name founder in shallow surfaces vs which keep founder deep), alternatives considered, and trigger conditions for re-evaluation.

The pattern is brand-agnostic - any brand whose founder is not celebrity-grade can adopt it.
