# REFERENCE - ABTS measurement architecture (the landing A/B testing system)

Owner: this is a reference / pattern document, not a brand-specific decision. Status: **canonical pattern**, do not delete.

This file documents the measurement half of a Brand OS: a source-agnostic engine that decides which landing / copy variant wins. The canon (the rest of this repo) says what the copy should be and why; the ABTS says which version actually wins. The template ships the pattern as a document, not as code - the source brand's implementation is ~2,000 lines of Python with numpy/scipy dependencies and brand-specific specs, personas, and golden data that do not scrub meaningfully. Build your own to this contract.

## The one design rule

Keep the LLM thin. Deterministic CODE owns every question with a closed-form answer - "is the arithmetic right", "is this legal under our walls", "are all required elements present", "did the traffic split evenly". The LLM owns exactly one question, the one with no closed-form answer: **"is this copy persuasive"**. Any stage that lets an LLM grade correctness or legality will eventually approve a broken or non-compliant variant with high confidence.

## The stages (each stage = one job, code-first)

| Stage | What it does | LLM? |
|-------|--------------|------|
| 0 - spec | One validated spec per variant (the contract). Prices, claims, and arithmetic re-checked deterministically. | no |
| 0.5 - annotations | Every element of the variant maps to Brand OS principle(s) + tactic + hypothesis + team decision + success metric. Refs are validated against the LIVE canon - a fabricated principle ID fails the build. | no |
| 2 - lint / walls | Zero-LLM brand-wall checks on the SERVED HTML: voice hygiene (dashes / exclamation / emoji), banned vocabulary, charm-price ban, required elements present, decoy structure intact. | no |
| 3 - CI | Visual regression + accessibility (axe-core) + performance budgets, wired as required checks. | no |
| 4 - judge | Disciplined persuasion judge: fixed rubric, debiased by construction (content-hash cache so identical copy always scores identically; golden dataset to detect drift). Output is a HYPOTHESIS ranking, not a verdict. | yes (one judgment per variant content-hash) |
| A - evaluate | The scoring engine: a single overall evaluation criterion (OEC) + Bayesian Beta-Binomial + sequential testing (always-valid, peeking-safe) + sample-ratio-mismatch guardrail + refund / cancel guardrails. Source-agnostic. | no |
| B - simulate | Persona traffic simulator: ICP-weighted synthetic population + one cached behaviour judgment per (persona x variant) + a deterministic session sampler. | cache only (a few dozen judgments, never one per visitor) |

## The fixed event contract

A small, fixed event schema (visit, scroll-depth, CTA click, add-to-cart, purchase, refund, cancel) decouples stage A from stage B and from real traffic. The same evaluation engine that scores the simulator scores real store events (e.g. commerce-platform webhooks) with no code change. This is the load-bearing piece: without it, your simulated results and your live results are computed by different code paths and can never be compared honestly.

## The annotations layer is the bridge to the canon

Stage 0.5 is what makes this a Brand OS subsystem rather than a generic A/B tool. Every headline, price block, badge, and CTA on a variant carries:

- which canon principle(s) it deploys (validated refs - no fabricated IDs)
- the hypothesis ("this element increases X because principle Y")
- the metric that would confirm or kill the hypothesis
- who decided to include it

When a variant wins, the annotations tell you WHICH principles won, and the learning flows back into `01-canon/` cocktails and `06-decisions/`. When a variant loses, you know which hypothesis died. Without annotations, a win teaches you nothing reusable.

## Honesty rules (non-negotiable)

1. Simulator output is a **HYPOTHESIS** grounded in your ICP personas, not a prediction of real conversion. Mark synthetic data as SYNTHETIC-PROVISIONAL in its provenance field.
2. The judge ranking is validated only against whatever golden dataset you built. It is a prioritization signal, not a truth signal.
3. Truth comes from live traffic through the same engine. Calibrate the behaviour model against real store data once it exists - that is the loop.
4. Publish results with the losers visible. A cumulative version registry (every variant ever shipped, winners first) keeps the team honest about hit rate.

## How to adopt

1. Start with stages 0 + 0.5 + 2 only - a spec format, an annotations format, and a deterministic lint over your served HTML. This is already more discipline than most brands have, and none of it needs an LLM or statistics.
2. Add stage A when you have real traffic: one OEC, Bayesian evaluation, SRM guardrail.
3. Add stages 4 + B only if you need to rank variants BEFORE you have traffic. Cache every LLM judgment by content hash.
4. Keep the ABTS offline from your web runtime. It ships only generated static artifacts (a results hub page) into your web layer.

## What NOT to do

- Do not let the LLM check arithmetic, legality, or element presence. Code owns those.
- Do not run one LLM judgment per simulated visitor - one cached judgment per (persona x variant) is the ceiling.
- Do not present simulator output to stakeholders as expected conversion.
- Do not skip the SRM guardrail; a broken traffic split silently invalidates everything downstream.
- Do not edit a variant after it enters evaluation - the content hash exists so the score always refers to exactly one artifact.
