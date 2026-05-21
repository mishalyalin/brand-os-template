# Day-7 post-purchase: review request email

Owner: {{ YOUR_NAME }}. Voice register: Register A (founder narrative). Brand voice version: {{ BRAND_VOICE_VERSION }}.

This is the email that goes out 7 days after first delivery to solicit the first customer review. The email is written in the founder's voice (Register A) and asks the customer to fill the 5-beat honest-attribution formula (Register B template at `08-templates/testimonial-template.md`).

The email is the operational hand-off between Register A and Register B. The founder asks; the customer answers. The customer's answer is the testimonial.

## When this fires

- Day 7 after first delivery confirmation
- Triggered by the {{ ESP_PLATFORM }} delivery webhook
- Skipped if the customer has already left a review
- Skipped if the customer requested a refund or replacement

## The ask

The 5-beat formula is in the email body explicitly. The customer fills the beats they have language for. Most customers fill 3 of 5. That is fine.

## Three A/B/C variants

### Variant A - Short founder ask (under 80 words)

**Subject:** Quick favour - your story in 5 beats

**Body:**

> Hi {{ CUSTOMER_FIRST_NAME }},
>
> A week with {{ BRAND_NAME }}. Long enough to know if anything changed.
>
> Would you write a review in this shape:
>
> 1. What discipline you are doing and why
> 2. What you achieved through your own work (not us)
> 3. The specific moment {{ BRAND_NAME }} caught - where you would have quit
> 4. Optional: a treat that used to be a cheat and is now part of the routine
>
> Three minutes. Helps the next person decide.
>
> -{{ FOUNDER_SHORTNAME }}
>
> [Write your review]({{ REVIEW_LINK }})

### Variant B - Mid-length founder ask with worked example (~150 words)

**Subject:** A week in - tell us where we caught you

**Body:**

> Hi {{ CUSTOMER_FIRST_NAME }},
>
> You bought {{ BRAND_NAME }} {{ DAYS_AGO }} days ago. Long enough to have a real opinion.
>
> Most useful reviews are not "5 stars great product". The most useful reviews follow this shape:
>
> > "I have been {{ DISCIPLINE }} for {{ TIME }} to {{ GOAL }}. The {{ RESULT }} came from my work, not from {{ BRAND_NAME }}. What {{ BRAND_NAME }} caught was the moment I would have quit - {{ SPECIFIC_MOMENT }}. Now {{ ROUTINE_CHANGE }}."
>
> Fill the beats you have words for. Skip the ones you do not. We do not need every box ticked.
>
> Three minutes. Goes a long way for the next person who is on the fence.
>
> -{{ FOUNDER_SHORTNAME }}
>
> [Write your review]({{ REVIEW_LINK }})

### Variant C - Long-form founder ask with rationale (~250 words)

**Subject:** Why we ask for reviews in a weird way

**Body:**

> Hi {{ CUSTOMER_FIRST_NAME }},
>
> A week with {{ BRAND_NAME }}. Time for a review.
>
> Here is the thing. Most reviews are useless. "5 stars great product" tells no one anything. We do not need more of those.
>
> What we need is the structure that actually helps the next person decide.
>
> The structure is five beats:
>
> 1. **Your discipline and your goal.** What were you doing and why. We do not ask which diet, which training plan, which schedule - your business.
> 2. **What you achieved through your own work.** The number, the moment, the feeling. The credit is yours. {{ BRAND_NAME }} did not run the kilometres or count the macros.
> 3. **The moment {{ BRAND_NAME }} caught you.** Where would you have quit without it. Be specific - the third bland meal of the week, the hotel breakfast, the boring tofu, whatever it was.
> 4. **Optional - a treat that used to be a cheat.** If something you used to lie about is now part of the routine, that is worth saying.
> 5. **Optional - sign yourself as {{ COMMUNITY_NAME_SINGULAR }}** if it fits.
>
> Three minutes. The next person on the fence reads it and decides to start.
>
> -{{ FOUNDER_SHORTNAME }}
>
> [Write your review]({{ REVIEW_LINK }})

## Voice rules applied

- Short hyphens only
- No emojis
- No exclamation marks
- No medicinal vocabulary
- No category comparisons
- Founder signs `-{{ FOUNDER_SHORTNAME }}` (lowercase, short hyphen)
- All three variants pin to Register A (founder narrative)
- The customer is invited to reply in Register B (5-beat formula)

## What to A/B test

- Variant A vs Variant B: does the worked-example version raise review submission rate enough to justify the extra read time?
- Subject lines: "Quick favour - your story in 5 beats" vs "A week in - tell us where we caught you" vs "Why we ask for reviews in a weird way" - the third is highest open-rate hypothesis (curiosity gap) but lowest expected click-through.
- CTA placement: bottom-only (current) vs top + bottom

## Suppression rules

- Skip if customer has reviewed in the last 90 days
- Skip if customer requested a refund or replacement
- Skip if customer email previously bounced or complained
- Skip if customer marked unsubscribe on transactional emails (most platforms keep these separate from marketing; verify your ESP)
