# Regulatory frames

Owner: {{ YOUR_NAME }}. Status: TEMPLATE - fill in via `python3 tools/onboard.py` or edit directly.

## Category

{{ CATEGORY }}

## Applicable regulators

| Jurisdiction | Regulator | Rule set | Relevance to copy |
|---|---|---|---|
| {{ JURISDICTION_1 }} | {{ REGULATOR_1 }} | {{ RULE_SET_1 }} | {{ RELEVANCE_1 }} |

## What this means for copy

### {{ REGULATOR_1 }}

- Banned phrasings: {{ BANNED_PHRASINGS_1 }}
- Required disclosures: {{ REQUIRED_DISCLOSURES_1 }}
- Safe register: {{ SAFE_REGISTER_1 }}

## Trace requirements

Every external-facing factual claim must trace to one of:

- A primary source (regulatory filing, government register, lab report)
- A cited evidence file in `05-evidence/`
- A Brain Vault row with an `NV-NNN` ID
- An explicit `[INFERRED]` tag with reasoning

Claims that cannot trace fail the Claims Trace CI check.
