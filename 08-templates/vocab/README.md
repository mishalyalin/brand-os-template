# Marketing Brain vocabulary

Owner: TBD - set during onboarding. Version: vocab-v1.0.0. Last updated: 2026-05-19.

This folder holds the Marketing Brain's vocabulary in editable JSON files. The Brain (`tools/marketing_brain.py`) loads these at import time and uses them to auto-tag cocktails / canon principles / Vault rows with the tactics + funnel stages + content vectors they apply to, and to flag rows for Wall-1 / Wall-2 hygiene.

## Why JSON, not a database

The vocabulary is small (61 canonical keys across 4 files, ~390 alias entries total at v1.0) and changes by hand, not by automation. JSON keeps the workflow:

- Git-diffable. Every alias change is a reviewable commit.
- GitHub-UI editable. A marketer can add a tactic alias from the browser without cloning the repo.
- No migration scripts. New tactic, append a line, re-run `rebuild-index`. Done.
- Stdlib only. `python3` + `git clone` and the Brain works.

A real database would add operational burden (server, migrations, ORM, dev-vs-prod drift) for negative value at this scale. The content (cocktails, canon principles, Vault rows) lives in Markdown + SQLite FTS5 - that part stays as-is.

## File layout

| File | What it holds | Used for |
|---|---|---|
| `tactics.json` | 41 behavioral / negotiation / influence tactics × aliases | Auto-tag rows with which tactic(s) they teach |
| `funnel-stages.json` | 10 stages × aliases | Auto-tag rows with which funnel stage(s) they fire in |
| `content-vectors.json` | content vectors (filled by onboard.py) × name + aliases + description | ICP segment routing (positioning.md Layer 0 gate) |
| `hygiene-vocab.json` | Wall-1 triggers + Wall-2 triggers + never-name-brands + voice-register-refs | Hygiene flagging on every retrieved row |

Each file follows a wrapped envelope:

```json
{
  "$schema": "<schema-id>",
  "_meta": { "version": "...", "description": "...", ... },
  "vocab": { ... }
}
```

The `_meta` block is documentation. The Brain loads only the data portion (`vocab` for tactics / stages, `vectors` for content-vectors, named arrays for hygiene).

## How to edit

### Adding a new tactic alias

```bash
# 1. Open tactics.json
# 2. Find the canonical tactic key (e.g. "pratfall_effect")
# 3. Append a new alias to its array
# 4. Re-build the index
python3 tools/marketing_brain.py rebuild-index
# 5. Verify the alias is matching as expected
python3 tools/marketing_brain.py search "<query that should trigger this alias>" --top 5
```

### Adding a new tactic

```bash
# 1. Open tactics.json
# 2. Add a new top-level key under "vocab":
#    "your_tactic_id": ["Canonical Name", "alias 1", "alias 2", ...]
# 3. Re-build the index
python3 tools/marketing_brain.py rebuild-index
# 4. Verify
python3 tools/marketing_brain.py tactic your_tactic_id
```

### Adding a new funnel stage

Same flow as adding a tactic, but edit `funnel-stages.json`. Verify with:

```bash
python3 tools/marketing_brain.py for-stage your_stage_id
```

### Adding a new content vector

Content vectors are locked in `00-foundations/positioning.md` as the strategic frame. **Do not add a new vector here without first updating positioning.md** - if positioning.md and this file disagree, positioning.md wins.

If positioning.md adds a 7th vector:

1. Edit `content-vectors.json` and add the new vector under `"vectors"` with `name` + `aliases` + `description`
2. Update `00-foundations/positioning.md` if not already done
3. `python3 tools/marketing_brain.py rebuild-index`
4. `python3 tools/marketing_brain.py for-vector your_vector_id`

### Adding a new hygiene trigger

```bash
# 1. Open hygiene-vocab.json
# 2. Append the new trigger word to the appropriate array (wall_1_triggers / wall_2_triggers / never_name_brands / voice_register_refs)
# 3. Re-build the index
python3 tools/marketing_brain.py rebuild-index
# 4. Verify - the Brain should now flag rows containing this word
python3 tools/marketing_brain.py search "<test query>" --top 5
```

## Matching rules

- **Tactic + stage + hygiene aliases:** case-insensitive substring match. Order matters within an alias list - the parser bails out of the inner loop on first hit, so put longer / more-specific phrases first to avoid greedy substring overlaps (e.g. "Pratfall Effect" before "Pratfall").
- **Content vector aliases:** multi-word aliases (contain space or hyphen) are matched as substrings. Single-word aliases are matched on word boundaries via `re.search(rf"\b{alias}\b", ...)` to avoid false positives like "avo" inside "available".

## Versioning

Bump the `_meta.version` field on any non-trivial vocabulary change. Patch bump (1.0.X) for alias additions / fixes. Minor bump (1.X.0) for new tactic / stage. Major bump (X.0.0) for structural schema changes (e.g. adding a `school` field to every tactic).

After bumping, update the `last_updated` field to today's ISO date.

## Source of truth precedence

If a file in this folder disagrees with a canonical source file in `00-foundations/`:

- `00-foundations/positioning.md` is the source of truth for content vectors + ICP + walls + founder anchor + never-name-brands + voice-register-refs
- `00-foundations/voice-anti-patterns.md` is the source of truth for wall-1 banned vocab
- `06-decisions/` records explain WHY the canonical files say what they say

The JSON files here are operational mirrors of the canonical content. The Brain parses them directly because the canonical files are prose-heavy and would slow down every Brain query if parsed live. When a canonical file changes, update the JSON file in the same PR.

## CI

The CI workflow `.github/workflows/brand-voice-check.yml` does not currently enforce JSON schema validity beyond syntactic parse. If the Brain fails to load a vocab file at import time, every CLI command fails fast - that's the de-facto validation.

## See also

- `tools/marketing_brain.py` - the Brain CLI that loads these files
- `skills/marketing-brain-query/SKILL.md` - how to invoke the Brain from a Claude session
- `01-canon/cocktail-recipes.md` + `01-canon/behavioral-economics.md` + `01-canon/nstd-tactics.md` + `01-canon/cialdini-sutherland.md` - the content the Brain indexes
- `01-canon/nudge-vault-raw-capture-2026-05-19.txt` - the 445 raw Vault rows
- `00-foundations/positioning.md` - the strategic frame (Layer 0)
