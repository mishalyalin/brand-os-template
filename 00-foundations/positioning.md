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
