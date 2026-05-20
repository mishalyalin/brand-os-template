#!/usr/bin/env python3
"""
Marketing Brain - structured retrieval over the Brand OS canon.

What this is:
    A CLI that lets Claude (or any caller) query a Brand OS for
    evidence-backed marketing recommendations. The Brain searches
    multiple layers in priority order:

    Layer 0 - positioning anchors from `00-foundations/positioning.md`
              (ICP + content vectors + walls + founder anchor)
    Layer 1 - cocktails in `01-canon/cocktail-recipes.md`
              (the brand has already decided how a principle stacks here)
    Layer 1.5 - canon principles in
              `01-canon/{behavioral-economics,nstd-tactics,cialdini-sutherland}.md`
              (51 principles with Where-to-use / Where-NOT guidance)
    Layer 2 - optional raw research rows
              (`01-canon/nudge-vault-raw-capture-*.txt`, NV-NNN block format)

    Every answer carries (a) the recommended tactic, (b) the primary-source
    citation, (c) a link to the cocktail recipe if one exists, (d) a Wall-1
    / Wall-2 hygiene flag, (e) a one-line rationale tying back to positioning.

    Layer 2 raw rows are optional - the Brain works fine on Layers 0 + 1 + 1.5
    if no research corpus is present.

How to invoke:
    python3 tools/marketing_brain.py search "<natural language query>" [--top N]
    python3 tools/marketing_brain.py tactic "<tactic name>"
    python3 tools/marketing_brain.py for-stage "<funnel stage>"
    python3 tools/marketing_brain.py for-vector "<content vector>"
    python3 tools/marketing_brain.py explain "<question>"
    python3 tools/marketing_brain.py icp
    python3 tools/marketing_brain.py canon [school]
    python3 tools/marketing_brain.py list-tactics
    python3 tools/marketing_brain.py list-stages
    python3 tools/marketing_brain.py stats
    python3 tools/marketing_brain.py rebuild-index

Repo-relative paths are auto-resolved from this file's location.

Design rules:
- Stdlib only. No external API, no vector DB.
- Brand-agnostic. Brand-specific content lives in the canon and foundation
  files this script reads at index-build time.
- The Brain never fabricates. If a query has no hit in the corpus, it
  returns `no-match` explicitly and tells the caller to gather more
  evidence rather than guessing.
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_CAPTURE = REPO_ROOT / "01-canon" / "nudge-vault-raw-capture-2026-05-19.txt"
COCKTAIL_RECIPES = REPO_ROOT / "01-canon" / "cocktail-recipes.md"
MINING_WORKBOOK = REPO_ROOT / "01-canon" / "nudge-vaults-mined-2026-05.md"
INDEX_JSON = REPO_ROOT / "01-canon" / "_brain-index.json"
INDEX_DB = REPO_ROOT / "01-canon" / "_brain-index.db"

POSITIONING = REPO_ROOT / "00-foundations" / "positioning.md"
ANTI_PATTERNS = REPO_ROOT / "00-foundations" / "voice-anti-patterns.md"
REGULATORY = REPO_ROOT / "00-foundations" / "regulatory-frames.md"

POSITIONING_FILE = REPO_ROOT / "00-foundations" / "positioning.md"

# ---------------------------------------------------------------------------
# Vocabulary - loaded from editable JSON config files in 08-templates/vocab/
# ---------------------------------------------------------------------------
# Per the 19 May 2026 refactor: vocabulary used to live as ~250 lines of
# hardcoded Python dicts inside this file. That made every new alias a Python
# PR, hostile to marketer edits, and conflated infrastructure (parser config)
# with content (what words to look for). Moving the vocab to JSON in
# `08-templates/vocab/` keeps the Brain stdlib-only, git-diffable, editable
# from the GitHub UI, and unblocks non-engineer changes. See
# `08-templates/vocab/README.md` for the workflow.
#
# The loaders are intentionally fail-fast: if a vocab file is missing or
# malformed, every Brain command errors at import time rather than silently
# returning empty search results.

VOCAB_DIR = REPO_ROOT / "08-templates" / "vocab"
TACTICS_VOCAB_FILE = VOCAB_DIR / "tactics.json"
STAGES_VOCAB_FILE = VOCAB_DIR / "funnel-stages.json"
VECTORS_VOCAB_FILE = VOCAB_DIR / "content-vectors.json"
HYGIENE_VOCAB_FILE = VOCAB_DIR / "hygiene-vocab.json"


def _load_vocab_file(path: Path) -> dict[str, Any]:
    """Load a JSON vocab file. Fail fast with a clear error message."""
    if not path.exists():
        raise FileNotFoundError(
            f"Marketing Brain vocab file not found: {path}\n"
            f"Expected location is `08-templates/vocab/`. Run `git pull` and "
            f"try again, or recreate the file from the template in the README."
        )
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Marketing Brain vocab file is not valid JSON: {path}\n"
            f"Parse error at line {e.lineno} col {e.colno}: {e.msg}\n"
            f"Fix the syntax error before running the Brain."
        ) from e


def _require_key(data: dict[str, Any], key: str, path: Path) -> Any:
    if key not in data:
        raise KeyError(
            f"Marketing Brain vocab file {path} is missing the `{key}` block. "
            f"Top-level keys present: {list(data.keys())}"
        )
    return data[key]


# Load all vocab at module-import time. Constants below preserve the names
# and shapes the rest of the Brain code expects, so the refactor is invisible
# to query / scoring / formatting layers downstream.

_TACTICS_DATA = _load_vocab_file(TACTICS_VOCAB_FILE)
TACTICS: dict[str, list[str]] = _require_key(_TACTICS_DATA, "vocab", TACTICS_VOCAB_FILE)

_STAGES_DATA = _load_vocab_file(STAGES_VOCAB_FILE)
STAGES: dict[str, list[str]] = _require_key(_STAGES_DATA, "vocab", STAGES_VOCAB_FILE)

# Content vectors (your ICP sub-segments) - defined by the brand owner
# in positioning.md and mirrored in content-vectors.json. Every customer-facing
# creative must fit one of them. Edit `content-vectors.json` to add/remove/
# rename a vector AND update positioning.md in the same PR (positioning.md is
# the source of truth).
_VECTORS_DATA = _load_vocab_file(VECTORS_VOCAB_FILE)
CONTENT_VECTORS: dict[str, dict[str, Any]] = _require_key(_VECTORS_DATA, "vectors", VECTORS_VOCAB_FILE)

# Wall-1 (medicine/wellness) / Wall-2 (category comparison) hygiene triggers
# + never-name-brands + voice-register-refs (Aesop / Le Labo cadence-only refs).
# All four arrays sit in a single hygiene-vocab.json file - they're related
# (anti-pattern hygiene + brand safety) and small enough that four mini-files
# would be more overhead than value.
_HYGIENE = _load_vocab_file(HYGIENE_VOCAB_FILE)
WALL_1_TRIGGERS: list[str] = _HYGIENE.get("wall_1_triggers", [])
WALL_2_TRIGGERS: list[str] = _HYGIENE.get("wall_2_triggers", [])
NEVER_NAME_BRANDS: list[str] = _HYGIENE.get("never_name_brands", [])
VOICE_REGISTER_REFS: list[str] = _HYGIENE.get("voice_register_refs", [])


# ---------------------------------------------------------------------------
# Canon-file parser config - stays as code because it pairs file paths with
# regex markers and parser-specific labels. This is infrastructure ("which
# files do we parse and how"), not vocabulary ("what words do we look for").
# ---------------------------------------------------------------------------

CANON_FILES = [
    {
        "path": REPO_ROOT / "01-canon" / "behavioral-economics.md",
        "school": "behavioral_economics",
        "label": "BE canon",
        "source_marker": "Canonical source:",
    },
    {
        "path": REPO_ROOT / "01-canon" / "nstd-tactics.md",
        "school": "nstd_voss",
        "label": "NSTD / Voss canon",
        "source_marker": "Canon reference:",
    },
    {
        "path": REPO_ROOT / "01-canon" / "cialdini-sutherland.md",
        "school": "cialdini_sutherland",
        "label": "Cialdini & Sutherland canon",
        "source_marker": "Canon reference:",
    },
]

EXISTING_COCKTAILS_SECTION_RE = re.compile(
    r"^### (.+?)$", re.MULTILINE
)

# ---------------------------------------------------------------------------
# Index build + persistence
# ---------------------------------------------------------------------------


def parse_raw_capture() -> list[dict[str, Any]]:
    """Parse the raw NV-NNN block file into structured records.

    Each block looks like:
        --- NV-NNN ---
        <emoji> <Insight title> <Finding body...> <Takeaway> <tags...> <source...>

    Without column delimiters we use a heuristic split:
        - first whitespace-separated emoji = emoji
        - next ~70 chars up to first lowercase sentence boundary = title
        - rest = body
    """
    if not RAW_CAPTURE.exists():
        # Layer 2 raw research rows are optional - the Brain works fine on
        # Layers 0 (positioning) + 1 (cocktails) + 1.5 (canon) without them.
        # Drop a file named `01-canon/nudge-vault-raw-capture-<date>.txt`
        # with NV-NNN block format if you have a research corpus to add.
        return []

    text = RAW_CAPTURE.read_text(encoding="utf-8")
    blocks = re.split(r"--- (NV-\d+) ---\n", text)
    records: list[dict[str, Any]] = []

    # blocks alternates ['', 'NV-001', '<row1 text>', 'NV-002', '<row2 text>', ...]
    for i in range(1, len(blocks), 2):
        nv_id = blocks[i].strip()
        body = blocks[i + 1].strip()
        if not body:
            continue

        # split first emoji from rest
        parts = body.split(" ", 1)
        emoji = parts[0] if parts else ""
        rest = parts[1] if len(parts) > 1 else ""

        # title heuristic: up to ~80 chars or until a sentence break
        title_match = re.match(r"^(.{0,90}?)(?=\s[A-Z][a-z]+\s|\.\s|\sA\s\d{4}|\sIn\s\d{4})", rest)
        title = title_match.group(1).strip() if title_match else rest[:80].strip()
        if not title:
            title = rest[:80]

        body_full = rest
        body_lower = body_full.lower()

        # Tactic detection (multi-tag possible)
        detected_tactics: list[str] = []
        for tactic_key, aliases in TACTICS.items():
            for alias in aliases:
                if alias.lower() in body_lower:
                    detected_tactics.append(tactic_key)
                    break

        # Stage detection (multi-tag possible)
        detected_stages: list[str] = []
        for stage_key, aliases in STAGES.items():
            for alias in aliases:
                if alias.lower() in body_lower:
                    detected_stages.append(stage_key)
                    break

        # Ranking stars (count ⭐ near end of row)
        rank_stars = body_full.count("⭐")

        # Easy-to-apply flag
        easy_to_apply = "✅" in body_full

        # Wall hygiene flags
        wall_1_flag = any(t.lower() in body_lower for t in WALL_1_TRIGGERS)
        wall_2_flag = any(t.lower() in body_lower for t in WALL_2_TRIGGERS)

        # Source guess - look for common patterns near end
        source_match = re.search(
            r"([A-Z][a-zA-Z]+,?\s[A-Z]\.[A-Z]?\.?,?(?:\s&?\s?[A-Z][a-zA-Z]+,?\s[A-Z]\.[A-Z]?\.?,?)*\s\(?\d{4}\)?)",
            body_full,
        )
        primary_source = source_match.group(0) if source_match else ""

        vectors = detect_vectors(body_full)

        records.append({
            "id": nv_id,
            "emoji": emoji,
            "title": title,
            "body": body_full,
            "tactics": detected_tactics,
            "stages": detected_stages,
            "vectors": vectors,
            "rank_stars": rank_stars,
            "easy_to_apply": easy_to_apply,
            "wall_1_flag": wall_1_flag,
            "wall_2_flag": wall_2_flag,
            "primary_source": primary_source,
        })

    return records


def parse_positioning_anchors() -> list[dict[str, Any]]:
    """Chunk positioning.md into structured Layer 0 atoms.

    Layer 0 sits ABOVE cocktails / canon / Vault rows because it answers
    'WHO + WHERE we play' before 'HOW we persuade'. Any tactic that does
    not serve one of the 6 content vectors is rejected at this layer.

    Anchors produced:
      - positioning_line: "Make Healthy Food Taste Great"
      - icp_definition: the ICP bullet from positioning.md
      - content_vector_1..N: the ICP sub-segments
      - wall_1: the first brand-safety wall (typically regulatory)
      - wall_2: the second brand-safety wall (typically strategic positioning)
      - forbids_list: what positioning forbids in copy
      - licenses_list: what positioning licenses in copy
      - founder_anchor: founder credential paragraph
      - voice_register_refs: cadence reference brands
      - never_name_brands: brands not named in customer copy
    """
    if not POSITIONING_FILE.exists():
        return []
    text = POSITIONING_FILE.read_text(encoding="utf-8")
    anchors: list[dict[str, Any]] = []

    # The line
    line_match = re.search(r'> \*\*"([^"]+)"\*\*', text)
    if line_match:
        anchors.append({
            "id": "POS-LINE",
            "kind": "positioning_line",
            "name": "The positioning line",
            "body": line_match.group(1),
            "guidance": (
                "Single source of truth for every brand decision. "
                "Not a headline - the lens through which every creative choice is evaluated."
            ),
            "tags": ["positioning", "core"],
            "vectors": list(CONTENT_VECTORS.keys()),
        })

    # ICP definition - the bullet starting with "- ICP" in positioning.md,
    # captured until the next bullet at the same indent or section break.
    icp_match = re.search(
        r"^- ICP[^\n]*?:\s*(.+?)(?=\n- |\n\n|\Z)",
        text,
        re.DOTALL | re.MULTILINE,
    )
    if icp_match:
        anchors.append({
            "id": "POS-ICP",
            "kind": "icp_definition",
            "name": "Ideal Customer Profile",
            "body": icp_match.group(1).strip()[:1500],
            "guidance": (
                "The ideal customer profile is the gate. If a tactic does not "
                "serve this customer, reject it before going further. Edit "
                "00-foundations/positioning.md to refine the ICP, then rebuild "
                "the index."
            ),
            "tags": ["icp", "core"],
            "vectors": list(CONTENT_VECTORS.keys()),
        })

    # 6 Content Vectors - extract from the Content vectors section
    cv_section = re.search(
        r"## Content vectors.+?(?=\n## )",
        text,
        re.DOTALL,
    )
    if cv_section:
        cv_text = cv_section.group(0)
        for i, (key, vec) in enumerate(CONTENT_VECTORS.items(), 1):
            # Try to pull the exact line from positioning.md for citable provenance
            line_re = re.compile(rf"\d+\.\s+\*\*{re.escape(vec['name'])}\.\*\*\s+(.+?)$", re.MULTILINE)
            m = line_re.search(cv_text)
            body_text = m.group(1).strip() if m else vec["description"]
            anchors.append({
                "id": f"POS-CV-{i}",
                "kind": "content_vector",
                "name": vec["name"],
                "vector_key": key,
                "body": body_text,
                "aliases": vec["aliases"],
                "guidance": (
                    "Content vector. Every email / SMS / Instagram post / TikTok / ad / "
                    "PDP module must fit one of the 6 vectors. If a creative idea does "
                    "not fit any, the answer is no. Shared visual structure across all 6: "
                    "same food, same person, sachet appears, the person's face changes."
                ),
                "tags": ["content_vector", "creative_starter"],
                "vectors": [key],
            })

    # Wall 1 + Wall 2 from the table
    wall_match = re.search(r"\| Wall 1.+?\| Wall 2.+?\|", text, re.DOTALL)
    if wall_match:
        anchors.append({
            "id": "POS-WALL-1",
            "kind": "wall_rule",
            "name": "Wall 1 - we do not go here",
            "body": "Wall 1 - the first brand-safety register (typically regulatory). See positioning.md for what your brand does not say.",
            "guidance": (
                "Wall 1 is the regulatory or category-trust wall. Define yours "
                "in 00-foundations/positioning.md. The trigger words live in "
                "08-templates/vocab/hygiene-vocab.json and the Brain auto-flags "
                "any retrieved row that contains one."
            ),
            "tags": ["wall_1", "hygiene", "regulatory"],
            "vectors": list(CONTENT_VECTORS.keys()),
        })
        anchors.append({
            "id": "POS-WALL-2",
            "kind": "wall_rule",
            "name": "Wall 2 - we do not go here",
            "body": "Wall 2 - the second brand-safety register (typically strategic positioning). See positioning.md for what your brand does not say.",
            "guidance": (
                "Wall 2 is the strategic-positioning wall. Define yours in "
                "00-foundations/positioning.md. The trigger words live in "
                "08-templates/vocab/hygiene-vocab.json and the Brain auto-flags "
                "any retrieved row that contains one."
            ),
            "tags": ["wall_2", "hygiene", "category"],
            "vectors": list(CONTENT_VECTORS.keys()),
        })

    # What positioning forbids
    forbids_section = re.search(
        r"## What this positioning forbids in copy(.+?)(?=\n## )",
        text,
        re.DOTALL,
    )
    if forbids_section:
        forbids_body = forbids_section.group(1).strip()
        anchors.append({
            "id": "POS-FORBIDS",
            "kind": "forbids_list",
            "name": "What positioning forbids in copy",
            "body": forbids_body[:1500],
            "guidance": (
                "Hard list of copy rules. Apply before any external publication. "
                "Auto-fails CI brand-voice-check if violated."
            ),
            "tags": ["forbids", "hygiene", "anti_pattern"],
            "vectors": list(CONTENT_VECTORS.keys()),
        })

    # What positioning licenses
    licenses_section = re.search(
        r"## What this positioning licenses(.+?)(?=\n## )",
        text,
        re.DOTALL,
    )
    if licenses_section:
        licenses_body = licenses_section.group(1).strip()
        anchors.append({
            "id": "POS-LICENSES",
            "kind": "licenses_list",
            "name": "What positioning licenses in copy",
            "body": licenses_body[:1500],
            "guidance": (
                "Explicitly licensed phrases and frames. Cleared for use without further review."
            ),
            "tags": ["licensed", "approved_copy"],
            "vectors": list(CONTENT_VECTORS.keys()),
        })

    # Founder anchor - locked since 28 Apr 2026, revised 19 May 2026 PM
    # Accept either parenthesised form "Founder credential (Name...)" or
    # colon form "Founder credential: Name..."
    founder_match = re.search(
        r"Founder credential[:\s]*\(([^)]+)\)", text
    )
    if not founder_match:
        founder_match = re.search(
            r"Founder credential[:\s]+([^\n]+(?:\n(?!\s*-\s|\s*\n|\s*##|\s*###)[^\n]+)*)",
            text,
        )
    if founder_match:
        anchors.append({
            "id": "POS-FOUNDER",
            "kind": "founder_anchor",
            "name": "Founder credential anchor",
            "body": founder_match.group(1).strip()[:1200],
            "guidance": (
                "The founder credential is the authority anchor. State it "
                "factually, avoid hype. Full story in `00-foundations/founder-stories.md`. "
                "Edit there + rebuild the index when the framing changes."
            ),
            "tags": ["founder", "authority", "credential"],
            "vectors": list(CONTENT_VECTORS.keys()),
        })

    # Voice register references
    anchors.append({
        "id": "POS-VOICE-REGISTER",
        "kind": "voice_register",
        "name": "Voice register references",
        "body": (
            "Voice register references are cadence references only. Not category "
            "competitors. The brand does not sit next to them in any product sense. "
            "Borrow their period-terminated rhythm, their restraint, their "
            "unwillingness to oversell - not their semantic field."
        ),
        "guidance": (
            "Cadence reference only. Period-terminated declarative rhythm. "
            "Editorial restraint. Do not borrow their semantic field - "
            "only the cadence."
        ),
        "tags": ["voice", "register", "cadence"],
        "vectors": list(CONTENT_VECTORS.keys()),
    })

    # Reference brands we never name
    anchors.append({
        "id": "POS-NEVER-NAME",
        "kind": "never_name_brands",
        "name": "Reference brands we do NOT name in copy",
        "body": (
            "Reference brands the brand specifically does NOT name in customer copy. "
            "Defined per-brand in `08-templates/vocab/hygiene-vocab.json` under "
            "`never_name_brands`. They may appear in 05-evidence/ and "
            "07-anti-patterns/ for internal pattern analysis only."
        ),
        "guidance": (
            "These brands appear in evidence files for tactical pattern analysis. "
            "They never appear in customer-facing copy. If a Brain query surfaces a "
            "tactic described as 'do what brand X does on the cart', extract the "
            "mechanic but never name brand X in shipped copy."
        ),
        "tags": ["never_name", "anti_pattern", "category"],
        "vectors": list(CONTENT_VECTORS.keys()),
    })

    return anchors


def detect_vectors(text_blob: str) -> list[str]:
    """Detect which content vectors a piece of text serves.

    Uses word-boundary regex matching to avoid false positives
    (e.g. "avo" substring-matching "available" / "avoid").
    Multi-word aliases match as exact phrases.
    """
    blob_lower = text_blob.lower()
    hits = []
    for key, vec in CONTENT_VECTORS.items():
        for alias in vec["aliases"]:
            alias_lower = alias.lower()
            if " " in alias_lower or "-" in alias_lower:
                # Multi-word alias - match as substring (no false-positive risk on word boundaries)
                if alias_lower in blob_lower:
                    hits.append(key)
                    break
            else:
                # Single-word alias - require word boundaries
                if re.search(rf"\b{re.escape(alias_lower)}\b", blob_lower):
                    hits.append(key)
                    break
    return sorted(set(hits))


def parse_canon_principles() -> list[dict[str, Any]]:
    """Pull principles from BE / NSTD / Cialdini-Sutherland canon files.

    Each principle is a `### N. Name` block with structured subsections
    (Canonical/Canon source, One-line definition, Where to use, Where NOT).
    We capture the heading + body until the next `### ` heading or end of file,
    auto-tag with tactics + stages, and detect Wall-1 / Wall-2 trigger words.
    """
    principles: list[dict[str, Any]] = []
    for source in CANON_FILES:
        path: Path = source["path"]
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        # Match `### N. Title` or `### N.M Title` (Sutherland uses 2.1 / 2.2 / ...)
        matches = list(re.finditer(r"^### (\d+(?:\.\d+)?\.?\s+.+?)$", text, re.MULTILINE))
        for i, m in enumerate(matches):
            heading = m.group(1).strip()
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            body = text[start:end].strip()
            # Strip subsection labels but preserve content
            body_lower = body.lower()

            # Extract a one-line definition for the title field if present
            def_match = re.search(
                r"\*\*One-line definition:\*\*\s*(.+?)(?:\n|$)",
                body,
            )
            definition = def_match.group(1).strip() if def_match else ""

            # Primary source extraction (whichever marker the source file uses)
            src_match = re.search(
                r"\*\*(?:Canonical source|Canon reference):\*\*\s*(.+?)(?:\n\n|\n\*\*)",
                body,
                re.DOTALL,
            )
            primary_source = (src_match.group(1).strip() if src_match else "")[:300]

            tactics: list[str] = []
            for tactic_key, aliases in TACTICS.items():
                # Match against both heading (so "Anchoring" principle gets the anchoring tactic)
                # and body so cross-references catch
                searchable = (heading + " " + body_lower)
                if tactic_key.replace("_", " ") in heading.lower():
                    tactics.append(tactic_key)
                    continue
                for alias in aliases:
                    if alias.lower() in searchable:
                        tactics.append(tactic_key)
                        break

            stages: list[str] = []
            for stage_key, aliases in STAGES.items():
                for alias in aliases:
                    if alias.lower() in body_lower:
                        stages.append(stage_key)
                        break

            wall_1_flag = any(t.lower() in body_lower for t in WALL_1_TRIGGERS)
            wall_2_flag = any(t.lower() in body_lower for t in WALL_2_TRIGGERS)
            vectors = detect_vectors(body)

            # Strip the leading number from the canonical principle name
            name_clean = re.sub(r"^\d+(?:\.\d+)?\.?\s+", "", heading)

            principle_id = f"{source['school'][:2].upper()}-{i+1:02d}"
            principles.append({
                "id": principle_id,
                "school": source["school"],
                "school_label": source["label"],
                "source_file": path.name,
                "name": name_clean,
                "heading": heading,
                "definition": definition,
                "body": body[:1500],
                "tactics": sorted(set(tactics)),
                "stages": sorted(set(stages)),
                "vectors": vectors,
                "primary_source": primary_source,
                "wall_1_flag": wall_1_flag,
                "wall_2_flag": wall_2_flag,
            })
    return principles


def parse_cocktail_recipes() -> list[dict[str, Any]]:
    """Pull existing cocktails from cocktail-recipes.md.

    Each cocktail is a `### <Name>` block. We capture the heading + body until
    the next heading at level <= 3 or end of file.
    """
    if not COCKTAIL_RECIPES.exists():
        return []
    text = COCKTAIL_RECIPES.read_text(encoding="utf-8")
    cocktails: list[dict[str, Any]] = []
    matches = list(re.finditer(r"^(### .+?)$", text, re.MULTILINE))
    for i, m in enumerate(matches):
        heading = m.group(1)
        if heading.startswith("### "):
            name = heading[4:].strip()
        else:
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()

        body_lower = body.lower()
        tactics: list[str] = []
        for tactic_key, aliases in TACTICS.items():
            for alias in aliases:
                if alias.lower() in body_lower:
                    tactics.append(tactic_key)
                    break

        stages: list[str] = []
        for stage_key, aliases in STAGES.items():
            for alias in aliases:
                if alias.lower() in body_lower:
                    stages.append(stage_key)
                    break

        vectors = detect_vectors(body)
        cocktails.append({
            "name": name,
            "tactics": tactics,
            "stages": stages,
            "vectors": vectors,
            "body": body[:1200],
            "anchor": name.lower().replace(" ", "-").replace("/", "-"),
        })
    return cocktails


def build_index() -> dict[str, Any]:
    raw_rows = parse_raw_capture()
    cocktails = parse_cocktail_recipes()
    canons = parse_canon_principles()
    positioning = parse_positioning_anchors()

    index = {
        "version": "1.3.0",
        "built_at": "2026-05-19",
        "raw_row_count": len(raw_rows),
        "cocktail_count": len(cocktails),
        "canon_count": len(canons),
        "positioning_count": len(positioning),
        "tactic_vocab": list(TACTICS.keys()),
        "stage_vocab": list(STAGES.keys()),
        "vector_vocab": list(CONTENT_VECTORS.keys()),
        "rows": raw_rows,
        "cocktails": cocktails,
        "canons": canons,
        "positioning": positioning,
    }
    INDEX_JSON.write_text(json.dumps(index, ensure_ascii=False, indent=0), encoding="utf-8")

    # Also a SQLite index for fast lookup
    if INDEX_DB.exists():
        INDEX_DB.unlink()
    conn = sqlite3.connect(INDEX_DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE rows(
            id TEXT PRIMARY KEY,
            emoji TEXT,
            title TEXT,
            body TEXT,
            tactics TEXT,
            stages TEXT,
            rank_stars INTEGER,
            easy_to_apply INTEGER,
            wall_1_flag INTEGER,
            wall_2_flag INTEGER,
            primary_source TEXT
        )
    """)
    cur.execute("""
        CREATE VIRTUAL TABLE rows_fts USING fts5(
            id UNINDEXED, title, body, tactics, stages, content='rows'
        )
    """)
    for r in raw_rows:
        cur.execute(
            "INSERT INTO rows VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                r["id"], r["emoji"], r["title"], r["body"],
                ",".join(r["tactics"]), ",".join(r["stages"]),
                r["rank_stars"], int(r["easy_to_apply"]),
                int(r["wall_1_flag"]), int(r["wall_2_flag"]),
                r["primary_source"],
            ),
        )
        cur.execute(
            "INSERT INTO rows_fts(id, title, body, tactics, stages) VALUES (?, ?, ?, ?, ?)",
            (r["id"], r["title"], r["body"], ",".join(r["tactics"]), ",".join(r["stages"])),
        )

    cur.execute("""
        CREATE TABLE cocktails(
            name TEXT PRIMARY KEY,
            tactics TEXT,
            stages TEXT,
            body TEXT,
            anchor TEXT
        )
    """)
    for c in cocktails:
        cur.execute(
            "INSERT OR REPLACE INTO cocktails VALUES (?, ?, ?, ?, ?)",
            (c["name"], ",".join(c["tactics"]), ",".join(c["stages"]),
             c["body"], c["anchor"]),
        )

    cur.execute("""
        CREATE TABLE canons(
            id TEXT PRIMARY KEY,
            school TEXT,
            school_label TEXT,
            source_file TEXT,
            name TEXT,
            definition TEXT,
            body TEXT,
            tactics TEXT,
            stages TEXT,
            primary_source TEXT,
            wall_1_flag INTEGER,
            wall_2_flag INTEGER
        )
    """)
    cur.execute("""
        CREATE VIRTUAL TABLE canons_fts USING fts5(
            id UNINDEXED, name, definition, body, tactics, stages, content='canons'
        )
    """)
    for k in canons:
        cur.execute(
            "INSERT INTO canons VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                k["id"], k["school"], k["school_label"], k["source_file"],
                k["name"], k["definition"], k["body"],
                ",".join(k["tactics"]), ",".join(k["stages"]),
                k["primary_source"],
                int(k["wall_1_flag"]), int(k["wall_2_flag"]),
            ),
        )
        cur.execute(
            "INSERT INTO canons_fts(id, name, definition, body, tactics, stages) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (k["id"], k["name"], k["definition"], k["body"],
             ",".join(k["tactics"]), ",".join(k["stages"])),
        )

    cur.execute("""
        CREATE TABLE positioning(
            id TEXT PRIMARY KEY,
            kind TEXT,
            name TEXT,
            body TEXT,
            guidance TEXT,
            tags TEXT,
            vectors TEXT
        )
    """)
    cur.execute("""
        CREATE VIRTUAL TABLE positioning_fts USING fts5(
            id UNINDEXED, name, body, guidance, tags, vectors, content='positioning'
        )
    """)
    for p in positioning:
        cur.execute(
            "INSERT INTO positioning VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                p["id"], p["kind"], p["name"], p.get("body", ""),
                p.get("guidance", ""),
                ",".join(p.get("tags", [])),
                ",".join(p.get("vectors", [])),
            ),
        )
        cur.execute(
            "INSERT INTO positioning_fts(id, name, body, guidance, tags, vectors) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (p["id"], p["name"], p.get("body", ""), p.get("guidance", ""),
             ",".join(p.get("tags", [])), ",".join(p.get("vectors", []))),
        )

    conn.commit()
    conn.close()
    return index


def load_index() -> dict[str, Any]:
    if not INDEX_JSON.exists():
        return build_index()
    return json.loads(INDEX_JSON.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Query primitives
# ---------------------------------------------------------------------------


def score_row(row: dict[str, Any], query_lower: str, query_terms: list[str]) -> float:
    score = 0.0
    body_lower = row["body"].lower()
    title_lower = row["title"].lower()

    # title hit weight
    for term in query_terms:
        if term in title_lower:
            score += 5.0
        if term in body_lower:
            # count occurrences for weighting
            score += body_lower.count(term) * 0.5

    # tactic match
    for tactic in row["tactics"]:
        if tactic.replace("_", " ") in query_lower or any(
            alias.lower() in query_lower for alias in TACTICS.get(tactic, [])
        ):
            score += 3.0

    # stage match
    for stage in row["stages"]:
        if stage.replace("_", " ") in query_lower:
            score += 2.5

    # ranking boost (5-star insight)
    score += row.get("rank_stars", 0) * 0.3

    # easy-to-apply boost
    if row.get("easy_to_apply"):
        score += 0.4

    return score


def search(query: str, top_n: int = 5) -> list[dict[str, Any]]:
    idx = load_index()
    q_lower = query.lower()
    q_terms = [t for t in re.findall(r"[a-zA-Z][a-zA-Z0-9'-]+", q_lower) if len(t) > 2]
    scored = [(score_row(r, q_lower, q_terms), r) for r in idx["rows"]]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [r for s, r in scored if s > 0][:top_n]


def search_positioning(query: str, top_n: int = 5) -> list[dict[str, Any]]:
    """Search Layer 0 positioning anchors (ICP + content vectors + walls).

    Highest base weight - this is the strategic frame everything else is
    filtered through. Per positioning.md locked 28 Apr 2026 + sharpened 19 May 2026.
    """
    idx = load_index()
    q_lower = query.lower()
    q_terms = [t for t in re.findall(r"[a-zA-Z][a-zA-Z0-9'-]+", q_lower) if len(t) > 2]
    detected_vectors = detect_vectors(query)
    scored = []
    for p in idx.get("positioning", []):
        body_lower = p["body"].lower()
        name_lower = p["name"].lower()
        score = 0.0
        for term in q_terms:
            if term in name_lower:
                score += 7.0
            if term in body_lower:
                score += body_lower.count(term) * 0.5
        # Boost content vectors when query mentions their aliases
        if p["kind"] == "content_vector":
            vector_key = p.get("vector_key")
            if vector_key in detected_vectors:
                score += 10.0
            for alias in p.get("aliases", []):
                if alias.lower() in q_lower:
                    score += 8.0
                    break
        # Boost walls when query asks about hygiene / wellness / category comparison
        if p["kind"] == "wall_rule":
            wall_triggers = ["wellness", "medicine", "remedy", "heal", "cure",
                             "salt category", "spice category", "maldon", "tabasco",
                             "wall 1", "wall 2", "hygiene", "anti-pattern"]
            for trigger in wall_triggers:
                if trigger in q_lower:
                    score += 6.0
                    break
        # Boost founder anchor when query mentions credentials / authority / founder
        if p["kind"] == "founder_anchor":
            founder_triggers = ["founder", "credibility", "authority", "credential",
                                "non-chef", "non chef", "zeptolab", "cut the rope",
                                "misha"]
            for trigger in founder_triggers:
                if trigger in q_lower:
                    score += 6.0
                    break
        # ICP definition matches on home cook / UK / EU / icp / customer profile
        if p["kind"] == "icp_definition":
            icp_triggers = ["icp", "ideal customer", "home cook", "customer profile",
                            "target audience", "audience", "segment", "who buys"]
            for trigger in icp_triggers:
                if trigger in q_lower:
                    score += 8.0
                    break
        if score > 0:
            scored.append((score, p))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for s, p in scored][:top_n]


def by_content_vector(vector_key: str) -> dict[str, list]:
    """Pull everything (cocktails / canon / Vault rows) tagged with this content vector."""
    idx = load_index()
    return {
        "cocktails": [c for c in idx.get("cocktails", []) if vector_key in c.get("vectors", [])],
        "canons": [k for k in idx.get("canons", []) if vector_key in k.get("vectors", [])],
        "rows": [r for r in idx.get("rows", []) if vector_key in r.get("vectors", [])],
        "anchor": next(
            (p for p in idx.get("positioning", [])
             if p.get("vector_key") == vector_key),
            None,
        ),
    }


def resolve_vector(vector_input: str) -> str | None:
    """Resolve a user-typed vector name to canonical key via aliases."""
    norm = vector_input.lower().replace("-", "_").replace(" ", "_")
    if norm in CONTENT_VECTORS:
        return norm
    for key, vec in CONTENT_VECTORS.items():
        if vector_input.lower() in [a.lower() for a in vec["aliases"]]:
            return key
        if vec["name"].lower() == vector_input.lower():
            return key
    return None


def search_canons(query: str, top_n: int = 5) -> list[dict[str, Any]]:
    """Search BE / NSTD / Cialdini-Sutherland canon principles.

    Higher base weight than raw Vault rows because these are pre-curated for
    the funnel application (each has Where-to-use / Where-NOT-to-use).
    """
    idx = load_index()
    q_lower = query.lower()
    q_terms = [t for t in re.findall(r"[a-zA-Z][a-zA-Z0-9'-]+", q_lower) if len(t) > 2]
    scored = []
    for k in idx.get("canons", []):
        body_lower = k["body"].lower()
        name_lower = k["name"].lower()
        def_lower = k.get("definition", "").lower()
        score = 0.0
        for term in q_terms:
            if term in name_lower:
                score += 6.0  # principle name match scores highest
            if term in def_lower:
                score += 2.0  # one-line definition match
            if term in body_lower:
                score += body_lower.count(term) * 0.5
        for tactic in k["tactics"]:
            if tactic.replace("_", " ") in q_lower or any(
                alias.lower() in q_lower for alias in TACTICS.get(tactic, [])
            ):
                score += 4.0
        for stage in k["stages"]:
            if stage.replace("_", " ") in q_lower:
                score += 3.0
        # School preference - if the query mentions "voss", "nstd", "voss tactic",
        # "behavioral economics", "cialdini", boost the matching school
        school_hints = {
            "nstd_voss": ["voss", "nstd", "never split", "negotiation"],
            "behavioral_economics": ["behavioral economics", "be canon", "kahneman", "ariely", "thaler", "sunstein"],
            "cialdini_sutherland": ["cialdini", "sutherland", "influence", "alchemy"],
        }
        for hint in school_hints.get(k["school"], []):
            if hint in q_lower:
                score += 5.0
                break
        if score > 0:
            scored.append((score, k))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [k for s, k in scored][:top_n]


def by_canon_school(school: str) -> list[dict[str, Any]]:
    idx = load_index()
    return [k for k in idx.get("canons", []) if k["school"] == school]


def search_cocktails(query: str, top_n: int = 3) -> list[dict[str, Any]]:
    idx = load_index()
    q_lower = query.lower()
    q_terms = [t for t in re.findall(r"[a-zA-Z][a-zA-Z0-9'-]+", q_lower) if len(t) > 2]
    scored = []
    for c in idx["cocktails"]:
        body_lower = c["body"].lower()
        name_lower = c["name"].lower()
        score = 0.0
        for term in q_terms:
            if term in name_lower:
                score += 5.0
            if term in body_lower:
                score += body_lower.count(term) * 0.5
        for tactic in c["tactics"]:
            if tactic.replace("_", " ") in q_lower or any(
                alias.lower() in q_lower for alias in TACTICS.get(tactic, [])
            ):
                score += 3.0
        for stage in c["stages"]:
            if stage.replace("_", " ") in q_lower:
                score += 2.5
        if score > 0:
            scored.append((score, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for s, c in scored][:top_n]


def by_tactic(tactic_name: str) -> list[dict[str, Any]]:
    idx = load_index()
    norm = tactic_name.lower().replace(" ", "_").replace("-", "_")
    # find canonical key
    canonical = None
    for key in TACTICS:
        if key == norm or key.replace("_", "") == norm.replace("_", ""):
            canonical = key
            break
        for alias in TACTICS[key]:
            if alias.lower() == tactic_name.lower():
                canonical = key
                break
        if canonical:
            break
    if not canonical:
        return []
    return [r for r in idx["rows"] if canonical in r["tactics"]]


def resolve_stage(stage_name: str) -> str | None:
    norm = stage_name.lower().replace(" ", "_").replace("-", "_")
    for key in STAGES:
        if key == norm:
            return key
        for alias in STAGES[key]:
            if alias.lower() == stage_name.lower():
                return key
    return None


def by_stage(stage_name: str) -> list[dict[str, Any]]:
    idx = load_index()
    canonical = resolve_stage(stage_name)
    if not canonical:
        return []
    return [r for r in idx["rows"] if canonical in r["stages"]]


def load_cocktails() -> list[dict[str, Any]]:
    return load_index()["cocktails"]


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------


def format_row(r: dict[str, Any], rank: int) -> str:
    out = [f"### Hit #{rank} - {r['emoji']} {r['title']}"]
    out.append("")
    out.append(f"**Vault ID:** `{r['id']}`")
    if r["tactics"]:
        out.append(f"**Tactics:** {', '.join(r['tactics'])}")
    if r["stages"]:
        out.append(f"**Funnel stages:** {', '.join(r['stages'])}")
    if r["rank_stars"]:
        out.append(f"**Phill's ranking:** {'⭐' * r['rank_stars']}")
    if r["easy_to_apply"]:
        out.append("**Easy to apply:** yes")
    if r["primary_source"]:
        out.append(f"**Primary source guess:** {r['primary_source']}")
    if r["wall_1_flag"]:
        out.append("⚠️ **Wall-1 hygiene flag** (medicinal-vocabulary risk) - keep copy culinary, not medicinal.")
    if r["wall_2_flag"]:
        out.append("⚠️ **Wall-2 hygiene flag** (salt/spice category comparison) - reframe to per-meal or within-customer anchor.")
    out.append("")
    out.append(f"**Body:** {r['body'][:600]}...")
    return "\n".join(out)


def format_cocktail(c: dict[str, Any], rank: int) -> str:
    out = [f"### Existing cocktail #{rank} - {c['name']}"]
    out.append("")
    out.append(f"**Location:** `01-canon/cocktail-recipes.md` §{c['name']}")
    if c["tactics"]:
        out.append(f"**Tactics stacked:** {', '.join(c['tactics'])}")
    if c["stages"]:
        out.append(f"**Funnel stages:** {', '.join(c['stages'])}")
    out.append("")
    out.append(f"**Excerpt:** {c['body'][:600]}...")
    return "\n".join(out)


def format_positioning(p: dict[str, Any], rank: int) -> str:
    out = [f"### Foundation #{rank} ({p['kind']}) - {p['name']}"]
    out.append("")
    out.append(f"**Anchor ID:** `{p['id']}`")
    out.append(f"**Location:** `00-foundations/positioning.md`")
    if p.get("tags"):
        out.append(f"**Tags:** {', '.join(p['tags'])}")
    if p.get("vectors"):
        labels = [CONTENT_VECTORS[v]["name"] for v in p["vectors"] if v in CONTENT_VECTORS]
        if labels and len(labels) < 6:
            out.append(f"**Content vectors served:** {', '.join(labels)}")
        elif labels:
            out.append(f"**Content vectors served:** all 6 (cross-cutting)")
    out.append("")
    out.append(f"**Anchor:** {p['body']}")
    if p.get("guidance"):
        out.append("")
        out.append(f"**Brain guidance:** {p['guidance']}")
    return "\n".join(out)


def format_canon(k: dict[str, Any], rank: int) -> str:
    out = [f"### Canon #{rank} ({k['school_label']}) - {k['name']}"]
    out.append("")
    out.append(f"**Location:** `01-canon/{k['source_file']}` §{k['heading'] if 'heading' in k else k['name']}")
    out.append(f"**Principle ID:** `{k['id']}`")
    if k["tactics"]:
        out.append(f"**Tactics:** {', '.join(k['tactics'])}")
    if k["stages"]:
        out.append(f"**Funnel stages:** {', '.join(k['stages'])}")
    if k.get("primary_source"):
        out.append(f"**Primary source:** {k['primary_source']}")
    if k["wall_1_flag"]:
        out.append("⚠️ **Wall-1 hygiene flag** (medicinal-vocabulary risk) - keep copy culinary, not medicinal.")
    if k["wall_2_flag"]:
        out.append("⚠️ **Wall-2 hygiene flag** (salt/spice category comparison) - reframe to per-meal or within-customer anchor.")
    out.append("")
    if k.get("definition"):
        out.append(f"**Definition:** {k['definition']}")
        out.append("")
    out.append(f"**Body (Where to use / Where NOT):**\n\n{k['body'][:900]}...")
    return "\n".join(out)


def cmd_search(args: argparse.Namespace) -> int:
    positioning_hits = search_positioning(args.query, top_n=3)
    cocktails = search_cocktails(args.query, top_n=3)
    canons = search_canons(args.query, top_n=args.top)
    rows = search(args.query, top_n=args.top)

    idx = load_index()
    print(f"# Marketing Brain search: \"{args.query}\"")
    print()
    print(f"Repository: {REPO_ROOT}")
    print(
        f"Index: {idx.get('positioning_count', 0)} positioning anchors (Layer 0) + "
        f"{idx.get('cocktail_count', 0)} cocktails (Layer 1) + "
        f"{idx.get('canon_count', 0)} canon principles BE/NSTD/Cialdini-Sutherland (Layer 1.5) + "
        f"{idx.get('raw_row_count', 0)} raw Vault rows (Layer 2)"
    )
    print()

    detected_vectors = detect_vectors(args.query)
    if detected_vectors:
        labels = [CONTENT_VECTORS[v]["name"] for v in detected_vectors if v in CONTENT_VECTORS]
        print(f"**ICP segments detected in query:** {', '.join(labels)}\n")

    if positioning_hits:
        print("## Layer 0 - Positioning anchors (ICP + content vectors + walls + founder)")
        print()
        print("These set the strategic frame. Every tactic below must serve at least one of the 6 content vectors AND respect both walls.")
        print()
        for i, p in enumerate(positioning_hits, 1):
            print(format_positioning(p, i))
            print()

    if cocktails:
        print("## Layer 1 - Existing cocktails (use first if relevant)")
        print()
        for i, c in enumerate(cocktails, 1):
            print(format_cocktail(c, i))
            print()
    else:
        print("## Layer 1 - Existing cocktails: NO MATCH")
        print()
        print("→ Net-new opportunity: if a canon principle or Vault row below scores well, propose a new cocktail in `01-canon/cocktail-recipes.md`.")
        print()

    if canons:
        print("## Layer 1.5 - canon principles (BE / NSTD / Cialdini-Sutherland)")
        print()
        print("These are the curated foundation principles with explicit Where-to-use / Where-NOT-to-use guidance for our funnel. Stack them into a cocktail; do not skip them for raw Vault rows.")
        print()
        for i, k in enumerate(canons, 1):
            print(format_canon(k, i))
            print()
    else:
        print("## Layer 1.5 - canon principles: NO MATCH")
        print()

    print("## Layer 2 - Raw Vault evidence")
    print()
    if not rows:
        if not cocktails and not canons:
            print("**no-match** - nothing across cocktails, canon principles, or Vault rows matches this query. Per `feedback_never_imagine_always_verify.md`, do NOT fabricate a study. Tell the user the corpus does not cover this question and gather more evidence first.")
            return 1
        print("No raw Vault row scored above threshold for this query. The canon principle and/or cocktail above is the ranked answer.")
        print()
    else:
        for i, r in enumerate(rows, 1):
            print(format_row(r, i))
            print()

    print("## Rationale framework")
    print()
    print("Per `feedback_marketing_panel_default.md`, the Brain enforces the 3-lens stack (BE + NSTD + DTC mechanics) on every answer. Before applying any tactic:")
    print("1. Verify it lands within Wall-1 (no medicine vocabulary) and Wall-2 (no category comparison)")
    print("2. Cite the primary source in copy, not Phill / Nudge / VaultsGPT")
    print("3. Cocktail > canon principle > raw Vault row when picking what to ship")
    print("4. Apply short hyphens only, no em-dashes")
    print("5. For B2C copy: run `skills/marketing-apply-brand-voice/SKILL.md` before publish")
    return 0


def cmd_tactic(args: argparse.Namespace) -> int:
    rows = by_tactic(args.name)
    norm = args.name.lower().replace(" ", "_").replace("-", "_")
    canonical = None
    for key in TACTICS:
        if key == norm:
            canonical = key
            break
    if not canonical and not rows:
        valid = ", ".join(sorted(TACTICS.keys()))
        print(f"**no-match** - tactic `{args.name}` not found. Valid tactics: {valid}")
        return 1
    canonical = canonical or norm

    # Canon principles tagged with this tactic
    idx = load_index()
    canon_hits = [k for k in idx.get("canons", []) if canonical in k["tactics"]]
    # Cocktails tagged with this tactic
    cocktail_hits = [c for c in idx.get("cocktails", []) if canonical in c["tactics"]]

    print(f"# Marketing Brain tactic lookup: {canonical}\n")

    if cocktail_hits:
        print(f"## Layer 1 - {len(cocktail_hits)} cocktail(s) stack this tactic\n")
        for i, c in enumerate(cocktail_hits, 1):
            print(format_cocktail(c, i))
            print()

    if canon_hits:
        print(f"## Layer 1.5 - {len(canon_hits)} canon principle(s) explain how this tactic lands\n")
        for i, k in enumerate(canon_hits, 1):
            print(format_canon(k, i))
            print()

    if rows:
        print(f"## Layer 2 - {len(rows)} Vault rows match this tactic. Top 10 by ranking:\n")
        rows.sort(key=lambda r: (r["rank_stars"], int(r["easy_to_apply"])), reverse=True)
        for i, r in enumerate(rows[:10], 1):
            print(format_row(r, i))
            print()
    elif not (canon_hits or cocktail_hits):
        print("**no-match** - tactic exists in vocabulary but nothing in cocktails / canon / Vault is tagged. Try a related tactic via `list-tactics`.")
        return 1
    return 0


def cmd_for_stage(args: argparse.Namespace) -> int:
    valid = ", ".join(sorted(STAGES.keys()))
    canonical = resolve_stage(args.stage)
    if not canonical:
        print(f"**no-match** - stage `{args.stage}` not in vocabulary. Valid stages: {valid}")
        return 1
    rows = by_stage(args.stage)
    idx = load_index()
    cocktails = [c for c in idx["cocktails"] if canonical in c["stages"]]
    canon_hits = [k for k in idx.get("canons", []) if canonical in k["stages"]]
    print(f"# Marketing Brain stage lookup: {canonical}\n")
    if cocktails:
        print(f"## Layer 1 - {len(cocktails)} cocktail(s) tagged for this stage\n")
        for i, c in enumerate(cocktails, 1):
            print(format_cocktail(c, i))
            print()
    if canon_hits:
        print(f"## Layer 1.5 - {len(canon_hits)} canon principle(s) with explicit guidance for this stage\n")
        for i, k in enumerate(canon_hits[:8], 1):
            print(format_canon(k, i))
            print()
    if not rows:
        print(f"## Layer 2 - 0 raw Vault rows tagged for `{canonical}`\n")
        print(f"This stage exists in vocabulary but no raw Vault rows are auto-tagged. The canon principles above carry the Where-to-use guidance. Valid stages: {valid}")
        return 0
    print(f"## Layer 2 - {len(rows)} raw Vault rows tagged. Top 10 by ranking:\n")
    rows.sort(key=lambda r: (r["rank_stars"], int(r["easy_to_apply"])), reverse=True)
    for i, r in enumerate(rows[:10], 1):
        print(format_row(r, i))
        print()
    return 0


def cmd_explain(args: argparse.Namespace) -> int:
    positioning_hits = search_positioning(args.question, top_n=3)
    cocktails = search_cocktails(args.question, top_n=1)
    canons = search_canons(args.question, top_n=3)
    rows = search(args.question, top_n=3)
    print(f"# Marketing Brain explain: {args.question}\n")

    detected_vectors = detect_vectors(args.question)
    if detected_vectors:
        labels = [CONTENT_VECTORS[v]["name"] for v in detected_vectors if v in CONTENT_VECTORS]
        print(f"**ICP segments detected in question:** {', '.join(labels)}\n")

    if positioning_hits:
        print("## Strategic frame (Layer 0 - positioning anchors)\n")
        print("Every recommendation below has to serve one of these. If it does not, reject it.\n")
        for i, p in enumerate(positioning_hits, 1):
            print(format_positioning(p, i))
            print()

    if cocktails:
        c = cocktails[0]
        print(f"## Recommended cocktail: {c['name']}\n")
        print(f"Location: `01-canon/cocktail-recipes.md` §{c['name']}\n")
        print(f"Tactics stacked: {', '.join(c['tactics']) if c['tactics'] else 'see body'}\n")
        print(f"Why this fits the brand: this cocktail is already pre-vetted against the positioning (Wall-1 + Wall-2 hygiene applied) and is wired to the funnel stages where it works. Use it as-is unless an owner-level override is documented in `06-decisions/`.\n")
        print(f"**Cocktail body excerpt:**\n\n{c['body'][:800]}\n")

    if canons:
        print("## Foundation principles to stack (BE / NSTD / Cialdini-Sutherland canon)\n")
        print("These principles carry explicit Where-to-use / Where-NOT-to-use guidance for our funnel. Stack them inside the cocktail before shipping copy.\n")
        for i, k in enumerate(canons, 1):
            print(format_canon(k, i))
            print()

    if rows:
        print("## Supporting evidence (raw Vault rows)\n")
        for i, r in enumerate(rows, 1):
            print(format_row(r, i))
            print()
    elif not (cocktails or canons):
        print("**no-match** - nothing across cocktails, canon, or Vault rows matches. Do not fabricate. Gather evidence first per `feedback_never_imagine_always_verify.md`.")
        return 1

    print("## Output contract for the caller\n")
    print("When the caller (Claude / human) uses this answer to ship customer copy:\n")
    print("1. Cite the primary source, not Phill / Nudge / VaultsGPT")
    print("2. Short hyphens only - run `skills/marketing-apply-brand-voice/SKILL.md`")
    print("3. Wall-1 check: no medicinal vocabulary (remedy / heal / wellness / cure)")
    print("4. Wall-2 check: no salt-category / spice-category comparisons - use per-meal anchors")
    print("5. Cocktail > canon principle > raw Vault row when picking what to ship")
    print("6. If proposing a NEW cocktail (Layer 1 returned no-match), add to `01-canon/cocktail-recipes.md` AFTER Misha review")
    return 0


def cmd_list_tactics(_args: argparse.Namespace) -> int:
    print("# Marketing Brain - tactic vocabulary\n")
    for key in sorted(TACTICS.keys()):
        print(f"- **{key}** - aliases: {', '.join(TACTICS[key][:4])}")
    return 0


def cmd_list_stages(_args: argparse.Namespace) -> int:
    print("# Marketing Brain - funnel-stage vocabulary\n")
    for key in sorted(STAGES.keys()):
        print(f"- **{key}** - aliases: {', '.join(STAGES[key][:4])}")
    return 0


def cmd_rebuild(_args: argparse.Namespace) -> int:
    idx = build_index()
    print(
        f"Index rebuilt. "
        f"{idx.get('positioning_count', 0)} positioning anchors + "
        f"{idx['cocktail_count']} cocktails + "
        f"{idx.get('canon_count', 0)} canon principles + "
        f"{idx['raw_row_count']} Vault rows indexed."
    )
    print(f"JSON: {INDEX_JSON}")
    print(f"SQLite: {INDEX_DB}")
    return 0


def cmd_icp(_args: argparse.Namespace) -> int:
    """Print the ICP definition + 6 content vectors + walls + founder anchor."""
    idx = load_index()
    positioning = idx.get("positioning", [])
    if not positioning:
        print("**no-match** - positioning anchors not in index. Run `rebuild-index`.")
        return 1
    print("# ICP + positioning anchors\n")
    print("Source: `00-foundations/positioning.md`. Run `python3 tools/onboard.py` first if it still contains placeholders.")
    print()
    # Render by kind so the output is structured
    order = [
        "positioning_line", "icp_definition", "content_vector",
        "wall_rule", "founder_anchor", "forbids_list", "licenses_list",
        "voice_register", "never_name_brands",
    ]
    by_kind: dict[str, list] = {}
    for p in positioning:
        by_kind.setdefault(p["kind"], []).append(p)
    rank = 0
    for kind in order:
        for p in by_kind.get(kind, []):
            rank += 1
            print(format_positioning(p, rank))
            print()
    return 0


def cmd_for_vector(args: argparse.Namespace) -> int:
    """Return all tactics/cocktails/canon/Vault rows that serve a specific content vector."""
    canonical = resolve_vector(args.vector)
    if not canonical:
        valid = ", ".join(CONTENT_VECTORS.keys())
        print(f"**no-match** - content vector `{args.vector}` not recognised. Valid: {valid}")
        return 1
    bundle = by_content_vector(canonical)
    vec = CONTENT_VECTORS[canonical]
    print(f"# Marketing Brain - tactics serving content vector: {vec['name']}\n")
    print(f"**Vector key:** `{canonical}`")
    print(f"**Description:** {vec['description']}")
    print(f"**Alias triggers:** {', '.join(vec['aliases'])}\n")

    if bundle["anchor"]:
        print("## Layer 0 - the canonical vector definition from positioning.md\n")
        print(format_positioning(bundle["anchor"], 1))
        print()

    if bundle["cocktails"]:
        print(f"## Layer 1 - {len(bundle['cocktails'])} cocktail(s) tagged for this vector\n")
        for i, c in enumerate(bundle["cocktails"], 1):
            print(format_cocktail(c, i))
            print()
    else:
        print("## Layer 1 - 0 cocktails currently tagged for this vector\n")
        print("Net-new opportunity: build a cocktail that serves this segment.\n")

    if bundle["canons"]:
        print(f"## Layer 1.5 - {len(bundle['canons'])} canon principle(s) tagged for this vector\n")
        for i, k in enumerate(bundle["canons"][:6], 1):
            print(format_canon(k, i))
            print()
    else:
        print("## Layer 1.5 - 0 canon principles currently auto-tagged for this vector\n")

    if bundle["rows"]:
        print(f"## Layer 2 - {len(bundle['rows'])} raw Vault rows tagged for this vector\n")
        bundle["rows"].sort(key=lambda r: r.get("rank_stars", 0), reverse=True)
        for i, r in enumerate(bundle["rows"][:8], 1):
            print(format_row(r, i))
            print()
    else:
        print("## Layer 2 - 0 raw Vault rows currently auto-tagged for this vector\n")
        print("This likely means the Vault corpus does not use the same vocabulary the vector aliases match against. Run `search` with a natural-language query about this segment to find related rows.\n")

    print("## Brain instruction\n")
    print("When proposing any tactic for this vector:\n")
    print("1. The tactic must respect Wall-1 (no medicine) + Wall-2 (no category comparison)")
    print("2. Cite the primary source, not Phill / Nudge / VaultsGPT")
    print("3. Short hyphens only - run `skills/marketing-apply-brand-voice/SKILL.md`")
    print("4. Visual structure for this vector: same food, same person, sachet appears, person's face changes")
    print("5. Use the founder as the protagonist by default; respect any on-camera policies in `00-foundations/founder-stories.md`")
    return 0


def cmd_canon(args: argparse.Namespace) -> int:
    idx = load_index()
    canons = idx.get("canons", [])
    schools = {"be": "behavioral_economics", "nstd": "nstd_voss", "voss": "nstd_voss",
               "cialdini": "cialdini_sutherland", "sutherland": "cialdini_sutherland"}
    if not args.school:
        # List all
        by_school: dict[str, list] = {}
        for k in canons:
            by_school.setdefault(k["school"], []).append(k)
        print("# Marketing Brain - canon principles\n")
        for school, items in by_school.items():
            label = items[0]["school_label"]
            print(f"## {label} ({len(items)} principles)\n")
            for k in items:
                print(f"- `{k['id']}` **{k['name']}** - {k.get('definition', '')[:120]}")
            print()
        print(f"Total: {len(canons)} principles across {len(by_school)} schools.")
        return 0
    school_key = schools.get(args.school.lower(), args.school)
    hits = [k for k in canons if k["school"] == school_key]
    if not hits:
        valid = ", ".join(sorted(schools.keys()))
        print(f"**no-match** - school `{args.school}` not found. Valid: {valid}")
        return 1
    print(f"# Marketing Brain - {hits[0]['school_label']} principles ({len(hits)})\n")
    for i, k in enumerate(hits, 1):
        print(format_canon(k, i))
        print()
    return 0


def cmd_stats(_args: argparse.Namespace) -> int:
    idx = load_index()
    print("# Marketing Brain - index stats\n")
    print(f"- Positioning anchors (Layer 0): {idx.get('positioning_count', 0)}")
    print(f"- cocktails (Layer 1): {idx['cocktail_count']}")
    print(f"- Canon principles BE/NSTD/Cialdini-Sutherland (Layer 1.5): {idx.get('canon_count', 0)}")
    print(f"- Raw Vault rows (Layer 2): {idx['raw_row_count']}")
    print(f"- Content vector vocab size: {len(idx.get('vector_vocab', []))}")
    print(f"- Tactic vocab size: {len(idx['tactic_vocab'])}")
    print(f"- Stage vocab size: {len(idx['stage_vocab'])}")
    # Content vector coverage
    vector_coverage: dict[str, dict] = {k: {"cocktails": 0, "canons": 0, "rows": 0} for k in CONTENT_VECTORS}
    for c in idx.get("cocktails", []):
        for v in c.get("vectors", []):
            if v in vector_coverage:
                vector_coverage[v]["cocktails"] += 1
    for k in idx.get("canons", []):
        for v in k.get("vectors", []):
            if v in vector_coverage:
                vector_coverage[v]["canons"] += 1
    for r in idx.get("rows", []):
        for v in r.get("vectors", []):
            if v in vector_coverage:
                vector_coverage[v]["rows"] += 1
    print("\n## Content vector coverage (how many tactics serve each ICP segment)\n")
    for vkey, counts in vector_coverage.items():
        label = CONTENT_VECTORS[vkey]["name"]
        print(f"- **{label}**: {counts['cocktails']} cocktails / {counts['canons']} canon / {counts['rows']} Vault rows")
    # Canon school breakdown
    canons = idx.get("canons", [])
    by_school: dict[str, int] = {}
    for k in canons:
        by_school[k["school_label"]] = by_school.get(k["school_label"], 0) + 1
    if by_school:
        print("\n## Canon principles by school\n")
        for label, n in sorted(by_school.items(), key=lambda x: -x[1]):
            print(f"- {label}: {n} principles")
    tactic_counts: dict[str, int] = {}
    stage_counts: dict[str, int] = {}
    for r in idx["rows"]:
        for t in r["tactics"]:
            tactic_counts[t] = tactic_counts.get(t, 0) + 1
        for s in r["stages"]:
            stage_counts[s] = stage_counts.get(s, 0) + 1
    print("\n## Top 15 tactics by Vault row count\n")
    for t, c in sorted(tactic_counts.items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"- {t}: {c} rows")
    print("\n## Top 10 stages by Vault row count\n")
    for s, c in sorted(stage_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"- {s}: {c} rows")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="marketing_brain",
        description="Marketing Brain - structured retrieval over the Brand OS canon.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_search = subparsers.add_parser("search", help="Natural-language search across Vault + cocktails.")
    p_search.add_argument("query", type=str)
    p_search.add_argument("--top", type=int, default=5)
    p_search.set_defaults(func=cmd_search)

    p_tactic = subparsers.add_parser("tactic", help="List all rows for a behavioral tactic.")
    p_tactic.add_argument("name", type=str)
    p_tactic.set_defaults(func=cmd_tactic)

    p_stage = subparsers.add_parser("for-stage", help="List all rows for a funnel stage.")
    p_stage.add_argument("stage", type=str)
    p_stage.set_defaults(func=cmd_for_stage)

    p_explain = subparsers.add_parser("explain", help="Question -> recommended cocktail + evidence + rationale.")
    p_explain.add_argument("question", type=str)
    p_explain.set_defaults(func=cmd_explain)

    p_icp = subparsers.add_parser(
        "icp",
        help="Print the ICP definition + 6 content vectors + walls + founder anchor (Layer 0).",
    )
    p_icp.set_defaults(func=cmd_icp)

    p_vector = subparsers.add_parser(
        "for-vector",
        help="Pull every tactic / cocktail / canon / Vault row that serves a specific content vector.",
    )
    p_vector.add_argument(
        "vector",
        type=str,
        help="vegan_bodybuilder / weight_loss_eater / sweet_pairing / avocado_moment / salad_bar_fix / chicken_rice_rescue",
    )
    p_vector.set_defaults(func=cmd_for_vector)

    p_canon = subparsers.add_parser(
        "canon",
        help="Browse canon principles (BE / NSTD / Cialdini-Sutherland).",
    )
    p_canon.add_argument(
        "school",
        nargs="?",
        default=None,
        help="Optional school filter: be / nstd / voss / cialdini / sutherland. Omit to list all.",
    )
    p_canon.set_defaults(func=cmd_canon)

    subparsers.add_parser("list-tactics", help="Print the tactic vocabulary.").set_defaults(func=cmd_list_tactics)
    subparsers.add_parser("list-stages", help="Print the funnel-stage vocabulary.").set_defaults(func=cmd_list_stages)
    subparsers.add_parser("rebuild-index", help="Rebuild the brain index from canon files.").set_defaults(func=cmd_rebuild)
    subparsers.add_parser("stats", help="Show index statistics.").set_defaults(func=cmd_stats)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
