# 06-decisions INDEX - status of every decision record

The decision files themselves are append-only and are never edited to reflect later supersessions. THIS index carries the live status. Add a row here in the same PR that adds a decision file.

(Optional hardening: add a CI step that fails any PR adding a `06-decisions/YYYY-MM-DD-*.md` file without a matching row here. The source brand runs this gate; the template leaves it as an exercise so forks can choose their own CI stack.)

Status vocabulary:

- **LIVE** - in force as written.
- **AMENDED-by-X** - core decision in force; a named clause was superseded by a later record (the row says which).
- **SUPERSEDED-by-X** - replaced wholesale; historical record only.
- **PROPOSED-awaiting-owner** - a recommendation, NOT canon; do not build on it until the brand owner signs off.
- **CLOSED-SUPERSEDED** - a proposal overtaken by later decisions before owner review concluded.

The `REFERENCE-*.md` files in this folder are architecture pattern documents, not dated decisions - they are canonical for the template and are not tracked here.

## Awaiting owner sign-off (do not treat as canon)

| Date | Decision | Status |
|---|---|---|
| {{ YYYY-MM-DD }} | {{ [Title](YYYY-MM-DD-slug.md) }} | **PROPOSED-awaiting-owner.** {{ one-line context }} |

## All decisions (newest first)

| Date | Decision | Status |
|---|---|---|
| {{ YYYY-MM-DD }} | {{ [Title](YYYY-MM-DD-slug.md) }} | LIVE |
