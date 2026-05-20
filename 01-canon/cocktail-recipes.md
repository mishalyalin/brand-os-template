# Cocktail recipes

Owner: {{ YOUR_NAME }}. Status: TEMPLATE - add your first cocktail when a real use case demands it. Version: 0.1.0.

A "cocktail" is a pre-vetted stack of behavioral, negotiation, and influence tactics applied to a specific funnel moment, with the Wall-1 and Wall-2 hygiene checks already applied. The Brain treats cocktails as **Layer 1** - pre-curated answers that should be tried before generating a fresh stack from raw tactics.

The Brain parses this file at index-build time. Each `### <Name>` block becomes one cocktail in the index. After editing this file, run:

```bash
python3 tools/marketing_brain.py rebuild-index
```

## How to write a cocktail

Each cocktail entry should contain:

1. **Funnel stage** - where it fires (hero, cart abandon, welcome flow, PDP, founder section, retention email, etc.)
2. **Tactic stack** - which behavioral principles are layered (Anchoring + Loss Aversion + Identity Priming, etc.)
3. **Verbatim copy or template** - the actual sentence-level draft, ready to ship or fill-in
4. **Primary citations** - the canonical source for each principle (Kahneman, Voss, Cialdini, etc.)
5. **Wall-1 / Wall-2 hygiene confirmation** - explicit "this respects Wall 1 because..." sentences
6. **Notes on when NOT to use** - the situations where this cocktail fails

## Example cocktail (placeholder - replace with yours)

### {{ EXAMPLE_COCKTAIL_NAME }}

**Funnel stage:** {{ FUNNEL_STAGE }}.

**Tactic stack:** {{ TACTIC_1 }} + {{ TACTIC_2 }} + {{ TACTIC_3 }}.

**Verbatim copy:**

> {{ VERBATIM_COPY }}

**Why this cocktail fits the brand:**

{{ FIT_RATIONALE }}

**Primary citations:**

- {{ TACTIC_1 }}: {{ CITATION_1 }}
- {{ TACTIC_2 }}: {{ CITATION_2 }}
- {{ TACTIC_3 }}: {{ CITATION_3 }}

**Hygiene confirmation:**

- Wall 1: {{ WALL_1_NOTE }}
- Wall 2: {{ WALL_2_NOTE }}

**When NOT to use:** {{ WHEN_NOT_TO_USE }}.

---

Add additional cocktails below as the brand develops them. Cocktails are the most valuable layer of the Brain because each one represents a battle-tested combination - not theory, applied practice.
