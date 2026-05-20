# Brand OS - template

A working starter kit for building a single source of truth for everything your brand says to a customer. Brand voice. Positioning. Persuasion canon (51 principles across Behavioral Economics + Voss/NSTD + Cialdini/Sutherland). Funnel architecture. Cocktail recipes for specific funnel moments. Anti-patterns. Decision records. Evidence library.

The included Marketing Brain CLI searches across all of it in one query and returns evidence-backed answers. Drop the repo into a Claude session and the `CLAUDE.md` plug-in contract tells the agent: query the Brain before generating any customer copy, respect the walls, cite primary sources, never fabricate.

This is the public template version. It is brand-agnostic. The interview wizard fills in your brand's specifics on first run.

## Use this template

1. Click **Use this template** at the top of the [GitHub page](https://github.com/mishalyalin/brand-os-template) and create your own repo.
2. Clone your new repo:
   ```bash
   git clone git@github.com:<you>/<your-brand-os>.git
   cd <your-brand-os>
   ```
3. Run the onboarding wizard:
   ```bash
   python3 tools/onboard.py
   ```
   You'll answer ~25-30 questions across six sections (positioning, content vectors, walls, voice, founder story, regulatory frames). Save-as-you-go - interrupt with Ctrl+C and re-run to resume.
4. Build the Brain index:
   ```bash
   python3 tools/marketing_brain.py rebuild-index
   ```
5. Confirm the Brain sees your positioning:
   ```bash
   python3 tools/marketing_brain.py icp
   ```
6. Optional - start the local web interface:
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r web/requirements.txt
   .venv/bin/python web/app.py
   # open http://127.0.0.1:8081/
   ```

That's it. You can now query the Brain for any marketing decision and get evidence-backed answers grounded in your specific positioning.

## What's in the repo

```
.
├── CLAUDE.md                       # plug-in contract for any Claude session
├── README.md                       # this file
├── LICENSE                         # MIT
├── 00-foundations/                 # the strategic frame
│   ├── positioning.md              # filled by onboard.py
│   ├── brand-voice.md              # filled by onboard.py
│   ├── voice-anti-patterns.md      # filled by onboard.py
│   ├── regulatory-frames.md        # filled by onboard.py
│   └── founder-stories.md          # filled by onboard.py
├── 01-canon/                       # the persuasion library
│   ├── behavioral-economics.md     # 16 BE principles, public academic
│   ├── nstd-tactics.md             # 21 Voss/NSTD tactics, public academic
│   ├── cialdini-sutherland.md      # 14 Cialdini/Sutherland principles, public academic
│   └── cocktail-recipes.md         # your applied stacks - empty until you add one
├── 03-touchpoint-copy/             # rendered customer copy by channel
├── 04-content-rules/               # operational rules (launch plan, content calendar)
├── 05-evidence/                    # append-only evidence library
├── 06-decisions/                   # append-only decision records
├── 07-anti-patterns/               # the "do not do this" library
├── 08-templates/
│   └── vocab/                      # editable JSON: tactics, stages, vectors, hygiene
├── tools/
│   ├── marketing_brain.py          # the Brain CLI
│   └── onboard.py                  # the interview wizard
├── web/                            # local Flask interface to the Brain
├── skills/
│   └── marketing-brain-query/      # SKILL.md for any Claude agent loading this repo
└── .github/workflows/              # CI: brand-voice-check, claims-trace, privacy-scrub
```

## The Marketing Brain

A stdlib-only Python CLI that searches your Brand OS in one query. Three (optionally four) layers, each filtered through the layer above it:

- **Layer 0** - positioning anchors (ICP + content vectors + walls + founder anchor + forbids/licenses lists). Locked when you finish onboarding.
- **Layer 1** - your cocktails. Pre-vetted stacks of behavioral, negotiation, and influence tactics for specific funnel moments.
- **Layer 1.5** - canon principles (51 across BE + Voss + Cialdini). Universal persuasion knowledge with explicit Where-to-use / Where-NOT guidance.
- **Layer 2** - raw research rows (optional - drop a `01-canon/nudge-vault-raw-capture.txt` if you have one).

Layer 0 is the GATE: any tactic that does not serve at least one of your content vectors AND respect both walls gets rejected. Beneath that gate, priority is cocktail > canon principle > raw row.

The Brain never fabricates. If a query has no hit in the corpus, it returns `no-match` and tells the caller to gather more evidence rather than guessing.

## CLI commands

```bash
python3 tools/marketing_brain.py search "<question>" --top 5
python3 tools/marketing_brain.py explain "<question>"
python3 tools/marketing_brain.py tactic <tactic_name>
python3 tools/marketing_brain.py for-stage <funnel_stage>
python3 tools/marketing_brain.py for-vector <content_vector>
python3 tools/marketing_brain.py icp
python3 tools/marketing_brain.py canon [school]
python3 tools/marketing_brain.py list-tactics
python3 tools/marketing_brain.py list-stages
python3 tools/marketing_brain.py stats
python3 tools/marketing_brain.py rebuild-index
```

## Adding cocktails

Cocktails are the most valuable layer because each one is a battle-tested combination, not theory. Add one when you've shipped real copy that worked. Format goes in `01-canon/cocktail-recipes.md` as a `### <Name>` block with:

- Funnel stage
- Tactic stack
- Verbatim copy or template
- Primary citations
- Wall-1 / Wall-2 hygiene confirmation
- When NOT to use

Then `python3 tools/marketing_brain.py rebuild-index` and your cocktail is searchable.

## Adding a tactic / stage / hygiene trigger

The Brain's vocabulary lives in `08-templates/vocab/` as four editable JSON files:

- `tactics.json` - 41 tactics × ~5 aliases each
- `funnel-stages.json` - 10 stages × ~6 aliases each
- `content-vectors.json` - your 6 content vectors (filled by onboard)
- `hygiene-vocab.json` - wall-1 / wall-2 / never-name / voice-register lists

Edit the JSON directly (or via GitHub UI in the browser). Then rebuild the index. New aliases become searchable immediately.

## CI checks

The workflows in `.github/workflows/` run on every PR:

- **`brand-voice-check.yml`** - scans for hard-rule violations in customer copy files
- **`claims-trace.yml`** - verifies external-facing factual claims trace to evidence
- **`privacy-scrub-check.yml`** - blocks placeholder strings (`{{ YOUR_NAME }}` etc) from landing in production files

Customize the rules for your brand by editing `.github/workflows/brand-voice-check.yml` after onboarding.

## Architecture notes

- Stdlib only. No external API. No vector DB. Search is composite-scored substring matching over an FTS5 SQLite index built from Markdown + JSON sources.
- Brand-agnostic. The Brain, web interface, and CI are all category-neutral. Your specifics live in `00-foundations/` + `08-templates/vocab/content-vectors.json`.
- Append-only by convention. Decisions, evidence, anti-patterns never delete - they accumulate, and supersession is explicit.
- CLAUDE.md is the plug-in contract. Any Claude-compatible agent reads it on session start and follows the rules.

## Provenance and credits

This template is derived from a working brand operating system built in May 2026 for a real DTC food brand. All brand-specific content has been scrubbed - the template ships only the brand-agnostic architecture and the universal persuasion canon.

Persuasion canon attribution:

- Behavioral Economics principles cite Daniel Kahneman, Dan Ariely, Richard Thaler, Cass Sunstein, Robert Cialdini, George Loewenstein, Amos Tversky, and others. See `01-canon/behavioral-economics.md` for source per principle.
- Voss / NSTD tactics cite Chris Voss + Tahl Raz's "Never Split the Difference" (2016). See `01-canon/nstd-tactics.md`.
- Cialdini-Sutherland principles cite Robert Cialdini's "Influence" + "Pre-Suasion" + Rory Sutherland's "Alchemy". See `01-canon/cialdini-sutherland.md`.

## License

MIT. Fork freely. Build your own. If you do, send me the URL - I'd love to see what brands are doing with it.

## Roadmap

- Phase 2: MCP integrations for Notion, Google Drive, Gong, Fireflies - feed existing brand materials into the onboarding wizard so it generates first drafts of foundation files instead of starting blank
- Phase 2: web interface deploy templates (VPS, Vercel, Cloudflare Workers)
- Phase 2: optional Layer 2 raw research rows (template needs a license-clear corpus)
- Phase 2: editorial CI (e.g. AI-grader that scores draft copy against the brand voice file)

Pull requests welcome.
