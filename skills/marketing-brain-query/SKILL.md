---
name: marketing-brain-query
description: Query the Marketing Brain before generating any customer-facing copy or marketing recommendation. The Brain wraps positioning, cocktails, canon principles, and any raw research rows into one search.
---

# Marketing Brain query

Use this skill when about to write or audit:

- Customer-facing copy of any length (email, SMS, social, hero, PDP, About, support reply)
- A marketing tactic recommendation
- A brand-voice question
- A funnel-stage design decision
- An affiliate or creator brief

## How to invoke

The Brain runs as a stdlib Python CLI at the repo root:

```bash
python3 tools/marketing_brain.py search "<natural-language question>" --top 5
python3 tools/marketing_brain.py explain "<question>"
python3 tools/marketing_brain.py tactic <tactic_name>
python3 tools/marketing_brain.py for-stage <funnel_stage>
python3 tools/marketing_brain.py for-vector <content_vector>
python3 tools/marketing_brain.py icp
python3 tools/marketing_brain.py canon [school]
```

## The four-layer architecture

The Brain returns results from up to four layers, ranked:

1. **Layer 0 - positioning anchors.** The strategic frame. If a tactic does not serve at least one content vector AND respect Wall 1 + Wall 2, reject it before going further.
2. **Layer 1 - cocktails.** Pre-vetted stacks with hygiene already applied. Use first if one matches.
3. **Layer 1.5 - canon principles.** 51 across Behavioral Economics, Voss/NSTD, Cialdini-Sutherland. Explicit Where-to-use / Where-NOT.
4. **Layer 2 - raw research rows.** Optional. Cite primary source.

## Output rules

When the Brain returns a recommendation, the output you produce for the user must:

1. Cite the primary source, never the Brain itself
2. Confirm Wall-1 and Wall-2 hygiene against the retrieved rows' flags
3. Follow the brand's hard rules in `00-foundations/brand-voice.md`
4. Stack from the top down: positioning frame -> cocktail -> canon -> evidence

## What the Brain will not do

- Fabricate studies or stats not in the corpus
- Contradict the canonical foundation files
- Generate copy that violates a hard rule

If the Brain returns no-match, do not invent. Tell the user the corpus does not cover the question and ask them where to gather more evidence.
