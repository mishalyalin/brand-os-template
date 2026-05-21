# Founder statement - three length cuts

Owner: {{ YOUR_NAME }}. Status: TEMPLATE - fill in via `python3 tools/onboard.py` or edit directly.

This file holds three length variants of the founder statement. Each variant compresses the same chronologically-corrected arc (founder succeeded WITHOUT the product, built the product for others). Pick the variant that matches the surface.

The arc must follow `00-foundations/founder-stories.md` Rule 1 (chronological correctness) and Rule 2 (ICP-defensiveness on founder labels). Verify both before locking each cut.

## Short-form (under 50 words)

For: Instagram bio, podcast intro line, conference speaker bio, paid-ad creative one-liner.

> {{ FOUNDER_1_NAME }} {{ DID_THE_HARD_THING }} the hard way for years. {{ FOUNDER_1_NAME }} tried to bring people along; most quit by week {{ N }} because {{ SPECIFIC_FAILURE_MODE }}. {{ FOUNDER_1_NAME }} built {{ BRAND_NAME }} for them. The tool {{ FOUNDER_1_NAME }} did not have.

## Mid-form (75-150 words)

For: About page intro paragraph, press boilerplate, welcome flow E2 email, investor deck "Founder slide" body copy.

> {{ FOUNDER_1_NAME }} spent {{ TIMEFRAME }} doing {{ THE_HARD_THING }} the hard way. {{ FOUNDER_1_NAME_PRONOUN_CAP }} got there - {{ MEASURABLE_RESULT_THE_HARD_WAY }} - through {{ DISCIPLINE_INPUTS }}.
>
> {{ FOUNDER_1_NAME_PRONOUN_CAP }} kept trying to help people on theirs. Friends, family, colleagues with their own goals and their own reasons. They all started. Most quit by week {{ N }}.
>
> Not because of willpower. Because {{ SPECIFIC_FAILURE_MODE }}.
>
> {{ FOUNDER_1_NAME }} built {{ BRAND_NAME }} as the tool {{ FOUNDER_1_NAME_PRONOUN }} did not have, for everyone {{ FOUNDER_1_NAME_PRONOUN }} tried to bring along.

## Long-form (300-500 words)

For: full About page, founder-led podcast intro, long-form Substack / newsletter founder note, investor narrative.

> {{ LONG_FORM_PARAGRAPH_1_ORIGIN_AND_DISCIPLINE_AT_LENGTH }}
>
> {{ LONG_FORM_PARAGRAPH_2_TRIED_TO_BRING_PEOPLE_ALONG_AND_WATCHED_THEM_QUIT }}
>
> {{ LONG_FORM_PARAGRAPH_3_THE_SPECIFIC_FAILURE_MODE_NAMED_CONCRETELY }}
>
> {{ LONG_FORM_PARAGRAPH_4_THE_TOOL_BUILT_AND_WHY_IT_LOOKS_THE_WAY_IT_DOES }}
>
> {{ LONG_FORM_PARAGRAPH_5_WHO_THIS_IS_FOR_AND_WHO_THIS_IS_NOT_FOR }}
>
> -{{ FOUNDER_SHORTNAME }}

## Verification checklist before locking each cut

- [ ] Chronological correctness: founder succeeded WITHOUT the product (Rule 1)
- [ ] ICP-defensiveness: no specific lifestyle label that polarizes the ICP (Rule 2)
- [ ] No medicinal vocabulary (no "wellness" / "ritual" / "healing" / "remedy" / "boost" / "energy" / etc)
- [ ] No category comparisons ("better than {{ COMPETITOR }}")
- [ ] Short hyphens only (no em-dashes, no en-dashes)
- [ ] No exclamation marks
- [ ] No co-founder names if their on-camera policy is by-equity-only
- [ ] Sign-off is `-{{ FOUNDER_SHORTNAME }}` (lowercase, short hyphen)

## How to use these cuts

Pin every surface that uses founder voice to one of the three cuts in its front matter. If you need a length between the three, use the next cut up and trim - do not interpolate. The cuts are deliberately discrete so the founder voice stays consistent.

If the founder voice evolves (new credential, new public moment, new chapter), bump the version and write a new decision record in `06-decisions/` capturing what changed.
