# REFERENCE - Design Lab split pattern (visual authority lives outside the Brand OS)

Owner: this is a reference / pattern document, not a brand-specific decision. Status: **canonical pattern**, do not delete.

This file documents an architecture pattern: separating WHAT the customer reads (copy / voice / positioning, lives in this Brand OS repo) from HOW it looks (visual tokens / modules / composition, lives in a separate Design Lab repo). Brand OS routes visual asks to the Lab via a pointer file; Brand OS does not author visual tokens.

The pattern is optional. Use it when your brand has a designer who wants their own iteration loop, or when your visual system needs to update at a different cadence than your copy.

## What the pattern is

Two repos, two CI loops, two ownership domains, one pointer:

1. **Brand OS (this repo)** owns the WHAT. Copy, voice, positioning, walls, regulatory, evidence, founder story, decisions, anti-patterns. Source-of-truth for every line of text on every customer-facing surface.
2. **Design Lab (separate repo, served from a single URL)** owns the HOW. Tokens (colours, type, radii, spacing, shadows, components, breakpoints), modules (composable building blocks with copy budgets), composition rules, accessibility, motion. Source-of-truth for every visual decision.
3. **Brand OS holds a single pointer file** at `00-foundations/design-lab-authority.md` that names the Lab URL and explains the access pattern. Brand OS never mirrors Lab content.

## Why each piece is load-bearing

### Brand OS owns WHAT, Lab owns HOW

The two domains have different review velocities. Voice changes need brand-voice CI, copy hygiene, walls scan, language-rule enforcement. Visual changes need token-scale validation, copy-budget linting, accessibility AA, visual self-check. Coupling them slows both: a button radius edit waits for a brand-voice review; a verb change waits for a visual review.

Splitting them lets the copy domain ship copy at copy cadence and the visual domain ship visual at visual cadence. Sessions integrate the two surfaces at compose-time by reading both.

### Brand OS holds the pointer, not the mirror

A pointer ages well. A mirror drifts the moment the Lab ships a token change. Sessions reading a stale mirror think they have current tokens when they do not. The pointer pattern keeps the Lab as the single live source and forces every session to WebFetch the live URL.

### Single Lab URL is the discoverability anchor

The Lab serves an `AGENTS.md` contract from a single URL. Sessions land there, read the contract, then pull `tokens.json` + `modules.json` + per-module `artifact_url` HTML. One discoverable entry point means no archaeology, no "which folder has the tokens", no "did the designer push to main yet".

The Lab's URL goes in your Brand OS pointer file. If the Lab URL changes, you update one line in one file.

## How to set up the pattern in your Brand OS

### Step 1 - your designer ships a Design Lab

Your designer creates a separate repo (or any single-URL hosting surface - Vercel / Netlify / Cloudflare Pages / a static site server). The Lab serves:

- `AGENTS.md` - the contract. Reading order, non-negotiables, self-check, feedback channel.
- `tokens.json` - colours, type, radii, spacing, shadows, components, breakpoints. Machine-readable.
- `modules.json` - catalog of composable modules + narratives. Each entry has `slug`, `title`, `group`, `artifact_url`, `summary`, `when_to_use`, `copy_budget`, and optional `depends_on`.
- Per-module HTML at the `artifact_url` paths.

The Lab can do whatever it wants internally (Storybook / Figma exports / static-site build / hand-rolled). What matters is the three files at the URL root + the per-module HTML.

### Step 2 - your Brand OS ships a pointer file

In your Brand OS, create `00-foundations/design-lab-authority.md` with:

1. The Lab URL (single line)
2. The WHAT / HOW split statement (this repo owns copy, Lab owns visual)
3. The access pattern (WebFetch `AGENTS.md`, then `tokens.json`, then `modules.json`, then per-module `artifact_url`)
4. The non-extraction rule (do not pull Lab content into Brand OS as a local copy)
5. The feedback channel (Lab repo URL + feedback labels)
6. A legacy-files disposition table (what stays in Brand OS for audit / historical reference, what is now Lab-authoritative)
7. A "why this split exists" paragraph (two CI loops, two cadences, two ownership domains)

### Step 3 - update your Brand OS entry points

Your `CLAUDE.md` and `AGENTS.md` both have a "where are the visual tokens" question that fresh sessions ask. Update both to point at the Lab as the live source. Existing in-repo visual files (if any) become reference-only.

### Step 4 - your Brand OS sessions follow the access pattern

When a session asks any of the visual triggers ("design me a page / hero / PDP / module / lander / colour / spacing"):

1. WebFetch Lab `AGENTS.md` - the contract
2. WebFetch Lab `tokens.json` - the visual scale
3. WebFetch Lab `modules.json` - the module catalog
4. For each module needed, pull HTML from its `artifact_url`
5. Source copy from this Brand OS via the Brain (`tools/marketing_brain.py invoke`)
6. Compose, respect copy budgets, respect Lab non-negotiables
7. Run the Lab self-check before ship

### Step 5 - the non-extraction rule

DO NOT pull Lab tokens, modules, or artifact HTML into this Brand OS or any other repo as a local copy. The Lab is the live source. WebFetch each session.

Single allowed exception: if WebFetch fails (Lab down or blocked), state explicitly that the Lab is unreachable. Do not fabricate visual specs from training-data memory. Do not fall back to legacy in-repo visual files as if they were live.

## When NOT to use the pattern

Three situations where the split is wrong:

1. **Your brand has no separate designer.** If the founder writes copy AND picks colours AND draws modules, splitting the system adds overhead with no benefit. Keep visual + copy in one Brand OS repo.
2. **Your visual system is locked and never iterates.** If tokens shipped in v1 and never change, a pointer to a Lab is dead weight. Keep tokens in this Brand OS.
3. **Your designer cannot ship a separate URL.** Pattern requires the Lab to be reachable by URL. If the designer's workflow does not produce a hostable surface (Figma-only, no exports), the pattern cannot work.

## How to verify the pattern is working

After setup:

- A fresh Claude session loading your Brand OS sees "visual lives at the Lab" in CLAUDE.md Q1 within the first 5 lines.
- WebFetch on the Lab URL returns `AGENTS.md` with reading order + non-negotiables.
- WebFetch on `tokens.json` returns valid JSON with your design tokens.
- WebFetch on `modules.json` returns valid JSON with at least one module entry containing the 8 required keys.
- A test design session ("compose a hero block") produces a result that pulls from the Lab and matches the Lab's quality bar.
- The Brand OS `tools/marketing_brain.py icp` still serves the copy / positioning side without referencing visual tokens.

If any step fails, fix the pointer file or the Lab contract before shipping any visual work.

## Relationship to other canon

| Sibling file | What it owns | Relationship to this pattern |
|---|---|---|
| `00-foundations/design-lab-authority.md` | The pointer to the Lab | The home of the pattern. Edit there, not here. |
| `00-foundations/visual-identity.md` | Markdown surface for legacy visual tokens | Reference-only after pattern adoption. Lab wins on disagreement. |
| `CLAUDE.md` | Plug-in contract for Claude sessions | Q1 "where are visual tokens" routes to the Lab. |
| `AGENTS.md` | Role-split + entry contract | Design-agent role + visual-tokens section route to the Lab. |
| `06-decisions/<date>-design-lab-becomes-visual-authority.md` | Locked decision | When you adopt the pattern, file a decision record. |

## How to extend the pattern

If your Brand OS grows a THIRD surface (e.g. a packaging-design system separate from web design), the pattern can extend to multiple Labs:

```
Brand OS  (WHAT)  -->  Web Lab    (HOW for web)
                  -->  Pack Lab   (HOW for packaging)
                  -->  Motion Lab (HOW for video / animation)
```

Each Lab gets its own pointer file under `00-foundations/<surface>-lab-authority.md`. The pattern scales horizontally without changing the core split.

## Reference implementation

Pranasalt adopted this pattern 2026-05-27. The Design Lab is at `https://pranasalt-design-lab.vercel.app` (Vercel-hosted, owned by `@ilyyyyyyya`). The pointer file lives at `00-foundations/design-lab-authority.md`. The decision record is `06-decisions/2026-05-27-design-lab-becomes-visual-authority.md`. The local Claude rule for any Misha-laptop session is `~/.claude/projects/-Users-mishalyalin-Desktop-claude/memory/feedback_design_lab_authority.md`.

Trigger: Misha verbatim 2026-05-27 PM: the Lab is now the authority; Brand OS routes to it; don't extract Lab content.
