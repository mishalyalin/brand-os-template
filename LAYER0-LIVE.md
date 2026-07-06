# LAYER0-LIVE - the one-page live fact sheet

How to use this repo: read this page first for the current facts, then `CLAUDE.md` for the full session contract, then query the Brain (`python3 tools/marketing_brain.py`) for canon.

Last updated: {{ YYYY-MM-DD }} by {{ PR / decision reference }}.

## The contract

This page is the single mandatory-read quick reference for the brand's CURRENT facts. Three rules keep it honest:

1. **Update this file IN PLACE in any PR that changes a fact below.** A PR that changes a price, a slogan, a product fact, or a positioning element without touching the matching row here is incomplete. Cite the decision file in the row.
2. **This page supersedes stale prose anywhere else in the repo** (README narrative, old foundation text, comments) for current facts. If you find a conflict between this page and prose elsewhere, this page wins and the stale prose should be fixed.
3. **The dated decision files in `06-decisions/` remain the ultimate source.** If a decision file disagrees with a row here, the decision file wins - and this page must be fixed in the same PR. Check `06-decisions/INDEX.md` for each decision's live status.

Why this file exists: repos rot. Facts change faster than prose. Without a single always-current page, every session (human or agent) re-derives the current state by archaeology across decision files - and sooner or later ships copy built on a superseded fact. One page, updated in place, closes that gap.

## The reconcile-sweep rule

When a Layer-0 element changes (slogan, product descriptor, hero hierarchy, a wall, a price), the change is not done until:

1. The decision record lands in `06-decisions/` (append-only, new file).
2. `06-decisions/INDEX.md` gets a row (and the superseded decision's row is updated to `AMENDED-by` / `SUPERSEDED-by`).
3. The matching row on THIS page is updated in the same PR.
4. A reconcile sweep propagates the new value across every surface that carried the old one - foundations, touchpoint copy, templates, web strings. Grep for the old value; the sweep is complete when the only remaining hits are inside dated decision records (which are never edited).

A Layer-0 change without the sweep is worse than no change: half the repo asserts the old fact, half the new one, and the Brain returns both.

## Brand axis

| Element | Value | Source |
|---|---|---|
| Primary slogan (hero emotional line) | {{ YOUR_SLOGAN }} | {{ decision file }} |
| Product descriptor (the "what is it" line) | {{ YOUR_DESCRIPTOR }} | {{ decision file }} |
| Hero hierarchy | {{ e.g. descriptor (top) -> slogan (middle) -> support line (bottom) }} | {{ decision file }} |
| Positioning thesis | {{ YOUR_POSITIONING_LINE }} | `00-foundations/positioning.md` |

## Product facts

| Fact | Value | Source |
|---|---|---|
| {{ e.g. composition }} | {{ value }} | {{ decision file }} |
| {{ e.g. unit / format }} | {{ value }} | {{ decision file }} |
| {{ e.g. usage anchor }} | {{ value }} | {{ decision file }} |

## Pricing ladder (locked values)

| Tier | {{ market A }} | {{ market B }} | Notes |
|---|---|---|---|
| {{ tier 1 }} | {{ price }} | {{ price }} | {{ note }} |
| {{ tier 2 }} | {{ price }} | {{ price }} | {{ note }} |

## Live corpus counts

Run `python3 tools/marketing_brain.py stats` and record the verified-live values here - never hand-estimate them:

| Metric | Value |
|---|---|
| Canon principles | {{ from stats }} |
| Cocktails | {{ from stats }} |
| Evidence rows | {{ from stats }} |
