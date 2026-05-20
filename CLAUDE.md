# CLAUDE.md - Instructions for any Claude session loading this Brand OS as a plug-in

This file is read automatically by Claude Code (and any Claude-compatible agent) when this repository is loaded as a workspace or plug-in. Anything written here applies to every session that touches the Brand OS.

If you are a Claude session reading this, the rules below are mandatory, not advisory. The owner of this repo owns the brand voice. Get the voice right.

## First-time setup

If `00-foundations/positioning.md` still contains `{{ YOUR_POSITIONING_LINE }}` placeholders, the Brand OS has not been onboarded yet. Stop and run the wizard before generating anything else:

```bash
python3 tools/onboard.py
```

The wizard fills the canonical foundation files via interactive Q&A (about 25-30 questions, save-as-you-go, safe to interrupt and resume).

## What this repo is

The single source of truth for everything this brand says to a customer. Brand voice, positioning, persuasion canon (Behavioral Economics + Voss/NSTD + Cialdini-Sutherland), funnel architecture, touchpoint copy, evidence, decisions, anti-patterns.

If you are about to write or audit:

- An email or SMS
- A PDP, lander, or hero block
- A social caption (Instagram, TikTok)
- An affiliate brief or creator script
- A founder story or About page
- A confirmation, refund, or customer-service reply
- A press response
- An investor narrative that quotes customer-facing copy

then you are working inside this repo's domain. Read the rules below before generating anything.

## The Marketing Brain - ALWAYS query it first

Before answering any marketing question, drafting any customer copy, or proposing any tactic, invoke the Marketing Brain CLI:

```bash
python3 tools/marketing_brain.py search "<natural-language question>" --top 5
python3 tools/marketing_brain.py explain "<question>"
python3 tools/marketing_brain.py tactic <tactic_name>
python3 tools/marketing_brain.py for-stage <funnel_stage>
python3 tools/marketing_brain.py for-vector <content_vector>
python3 tools/marketing_brain.py icp
```

The Brain wraps three layers, each filtered through the layer above it:

- **Layer 0 - positioning anchors** (ICP + content vectors + Wall 1 + Wall 2 + founder anchor + forbids/licenses lists + voice register refs + never-name list). The strategic frame.
- **Layer 1 - cocktails** in `01-canon/cocktail-recipes.md`. Pre-vetted stacks with Wall-1 / Wall-2 hygiene applied. Use them first.
- **Layer 1.5 - canon principles** in `01-canon/behavioral-economics.md`, `nstd-tactics.md`, `cialdini-sutherland.md`. 51 principles with explicit Where-to-use / Where-NOT guidance.

Optionally a **Layer 2 - raw evidence rows** if you have a third-party research corpus. Drop it as `01-canon/nudge-vault-raw-capture.txt` (one block per `--- ID ---` line) and the Brain auto-indexes it.

Layer 0 is the GATE: any tactic that does not serve at least one of the content vectors AND respect both walls gets rejected. Beneath that gate, priority is cocktail > canon principle > raw evidence row.

The Brain never fabricates. If a query has no hit in the corpus, it returns `no-match` and tells the caller to gather more evidence rather than guessing.

## The seven hard rules

These are filled by the onboarding wizard into `00-foundations/brand-voice.md`. CI enforces them. A PR that violates one fails the Brand Voice Check workflow.

Examples of strong hard rules (replace with yours during onboarding):

- Short hyphens only - no em or en dashes
- No emojis in customer-facing copy
- No exclamation marks in customer-facing copy
- No medicinal vocabulary (food/supplement brands)
- Period-terminated declarative cadence
- Every external claim must trace to a primary source
- No fabricated numbers, dates, customer counts, or studies

Edit `00-foundations/brand-voice.md` and re-run `tools/marketing_brain.py rebuild-index` after onboarding to lock yours in.

## Names and identity

The onboarding wizard captures founder name + co-founder names + on-camera policy. Once filled into `00-foundations/founder-stories.md`, treat those names as immutable - misspelling or substituting them is a brand failure.

## When you produce customer copy

Workflow:

1. Run the Brain to find the right cocktail or tactic with evidence
2. Draft the copy stacking the recommended tactic(s)
3. Run the brand voice check (em-dash scan, exclamation scan, medicinal scan, jargon scan)
4. Run a regulatory exposure check if the copy makes any factual or pricing claim
5. Save to the appropriate `03-touchpoint-copy/` file
6. Open a PR; let CI run the same checks; the owner reviews

## When you produce a decision record

Save it as a date-stamped file in `06-decisions/`. Format: `YYYY-MM-DD-<slug>.md`. Append-only. Body should include: what was decided, when, why, what alternatives were considered, what the trigger event was.

## When you produce evidence

Save to `05-evidence/<topic>/` with a date-stamped filename. Append-only. Never edit or delete an evidence file - if it's superseded, add a new one referencing the old one.

## When you produce a new cocktail

Cocktails go in `01-canon/cocktail-recipes.md` as `### <Name>` blocks. Each cocktail must include:

- Tactic stack (which behavioral principles are layered)
- Funnel stage (where it fires)
- Verbatim copy or copy template
- Primary citation for each principle
- Wall-1 / Wall-2 hygiene confirmation
- Notes on when NOT to use

Re-run `python3 tools/marketing_brain.py rebuild-index` after adding a new cocktail.

## Loading this repo as a plug-in into a fresh Claude session

```bash
# 1. Clone (or use as template)
git clone <your-fork-url>
cd <repo>

# 2. First-time only: onboard the brand
python3 tools/onboard.py

# 3. Build / rebuild the Brain index
python3 tools/marketing_brain.py rebuild-index

# 4. Local web interface (optional)
python3 -m venv .venv
.venv/bin/pip install -r web/requirements.txt
.venv/bin/python web/app.py
# open http://127.0.0.1:8081/

# 5. Open Claude Code / Cursor / any agent in this dir
# CLAUDE.md (this file) auto-loads the rules
```

Stdlib only. No external API. No vector DB. `git clone` + `python3` + ready.

## License

MIT. See `LICENSE`. Anyone can fork, modify, deploy.
