#!/usr/bin/env python3
"""Brand OS onboarding wizard.

Interactive Q&A that fills the canonical foundation files (positioning,
brand voice, voice anti-patterns, regulatory frames, founder stories,
content-vectors JSON) from your answers. Save-as-you-go - you can quit
at any point and resume later by re-running.

What it touches:
    00-foundations/positioning.md
    00-foundations/brand-voice.md
    00-foundations/voice-anti-patterns.md
    00-foundations/regulatory-frames.md
    00-foundations/founder-stories.md
    08-templates/vocab/content-vectors.json
    08-templates/vocab/hygiene-vocab.json (wall-1 / wall-2 trigger lists)
    .brand-os-state.json (your answers, so you can resume)

What it does NOT do:
    - Write any cocktail recipes (cocktails earn their place from real use)
    - Touch the canonical persuasion canon files (BE / NSTD / Cialdini are universal)
    - Fetch data from external sources (interview-only Phase 1)
    - Push anything to git or any remote

How to use:
    python3 tools/onboard.py

You'll be asked ~25-30 questions across 6 sections. The wizard saves your
answers after every section, so quitting + resuming is safe. Multi-line
answers are supported via Ctrl+D (EOF) at end of input.

After onboarding:
    python3 tools/marketing_brain.py rebuild-index
    python3 tools/marketing_brain.py icp
    python3 web/app.py    # local web interface at http://127.0.0.1:8081

Author: brand-os-template, MIT licensed.
"""

from __future__ import annotations

import datetime as _dt
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = REPO_ROOT / ".brand-os-state.json"

POSITIONING_PATH = REPO_ROOT / "00-foundations" / "positioning.md"
BRAND_VOICE_PATH = REPO_ROOT / "00-foundations" / "brand-voice.md"
ANTI_PATTERNS_PATH = REPO_ROOT / "00-foundations" / "voice-anti-patterns.md"
REGULATORY_PATH = REPO_ROOT / "00-foundations" / "regulatory-frames.md"
FOUNDER_STORIES_PATH = REPO_ROOT / "00-foundations" / "founder-stories.md"
CONTENT_VECTORS_JSON = REPO_ROOT / "08-templates" / "vocab" / "content-vectors.json"
HYGIENE_VOCAB_JSON = REPO_ROOT / "08-templates" / "vocab" / "hygiene-vocab.json"

TODAY = _dt.date.today().isoformat()

# ---------------------------------------------------------------------------
# Terminal helpers
# ---------------------------------------------------------------------------

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
ACCENT = "\033[33m"  # yellow-ish for prompts


def _is_tty() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def _color(text: str, code: str) -> str:
    if not _is_tty():
        return text
    return f"{code}{text}{RESET}"


def banner(title: str) -> None:
    line = "-" * len(title)
    print()
    print(_color(line, DIM))
    print(_color(title, BOLD))
    print(_color(line, DIM))
    print()


def hint(text: str) -> None:
    print(_color(text, DIM))


def ask(
    prompt: str,
    *,
    multiline: bool = False,
    default: str | None = None,
    examples: list[str] | None = None,
    validate: Callable[[str], str | None] | None = None,
) -> str:
    """Prompt the user. Returns stripped string.

    `multiline=True` reads until EOF (Ctrl+D on Unix, Ctrl+Z+Enter on Windows).
    `default` is shown in [brackets]; pressing Enter accepts it.
    `examples` are printed as italic hints before the prompt.
    `validate` returns None if OK, otherwise an error string.
    """
    while True:
        print()
        print(_color(prompt, BOLD))
        if examples:
            for ex in examples:
                print(_color(f"    example: {ex}", ITALIC + DIM))
        if default is not None:
            hint(f"    default: {default}")
        if multiline:
            hint("    multi-line input - finish with an empty line, then Ctrl+D (or Ctrl+Z then Enter on Windows)")
            lines: list[str] = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            answer = "\n".join(lines).strip()
        else:
            answer = input(_color("> ", ACCENT)).strip()
        if not answer and default is not None:
            answer = default
        if validate is not None:
            err = validate(answer)
            if err:
                hint(f"    ! {err} - try again.")
                continue
        return answer


def confirm(prompt: str, default: bool = True) -> bool:
    suffix = " [Y/n]" if default else " [y/N]"
    while True:
        a = input(_color(prompt + suffix + " ", BOLD)).strip().lower()
        if not a:
            return default
        if a in {"y", "yes"}:
            return True
        if a in {"n", "no"}:
            return False
        print("  please answer y or n")


# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------


def load_state() -> dict[str, Any]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"version": "0.1.0", "started_at": TODAY, "sections_completed": [], "answers": {}}


def save_state(state: dict[str, Any]) -> None:
    state["last_saved_at"] = TODAY
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def remember(state: dict[str, Any], key: str, value: Any) -> None:
    state["answers"][key] = value


def recall(state: dict[str, Any], key: str, default: Any = None) -> Any:
    return state["answers"].get(key, default)


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------


def section_meta(state: dict[str, Any]) -> None:
    banner("1. About you")
    state["answers"].setdefault("your_name", "")
    your_name = ask(
        "Your name (the brand owner). Used as the owner field on every foundation file.",
        default=recall(state, "your_name") or None,
    )
    remember(state, "your_name", your_name)

    brand_name = ask(
        "Brand name. Used in the README and as a placeholder anchor across files.",
        default=recall(state, "brand_name") or None,
        examples=["e.g. NorthCove", "e.g. Bloomwell", "e.g. RuggedKettle"],
    )
    remember(state, "brand_name", brand_name)


def section_positioning(state: dict[str, Any]) -> None:
    banner("2. Positioning - the strategic frame")
    hint("The positioning section anchors everything. Take your time. The wizard saves after this section, so you can come back.")

    positioning_line = ask(
        "Your positioning line. One short sentence the brand can stand behind for years.",
        default=recall(state, "positioning_line") or None,
        examples=[
            "Make Healthy Food Taste Great.",
            "The boring fund that quietly beats the exciting funds.",
            "A bike that actually fits in the elevator.",
        ],
        validate=lambda s: None if 3 <= len(s) <= 80 else "keep it between 3 and 80 characters",
    )
    remember(state, "positioning_line", positioning_line)

    icp = ask(
        "Your ICP (ideal customer profile). One sentence that names them specifically enough you can picture them on a Tuesday afternoon. Demographics + psychographics + frustration.",
        multiline=True,
        default=recall(state, "icp") or None,
        examples=[
            "30-55 active urban UK + EU + US adult who has been struggling with bland disciplined eating for years.",
            "35-50 finance-curious professional who has tried Robinhood, lost interest, and now wants something they would not be embarrassed to recommend to their parents.",
        ],
    )
    remember(state, "icp", icp)

    banner("3. Content vectors - your 6 ICP sub-segments")
    hint("Six is the default cap. More than six and the brand loses focus. Each vector is one specific situation + person where your product fits. Give each a short name and a one-sentence description.")

    vectors = recall(state, "content_vectors", [])
    if not vectors:
        vectors = []
    for i in range(1, 7):
        existing = vectors[i - 1] if i - 1 < len(vectors) else {"name": "", "description": "", "aliases": []}
        print()
        print(_color(f"Vector {i}", BOLD))
        if i > 1 and not confirm(f"    add vector {i}?", default=(i <= 3)):
            break
        v_name = ask(
            f"Vector {i} - short name (one phrase, e.g. 'The bodybuilder' or 'The lunch-counter rescue')",
            default=existing.get("name") or None,
        )
        v_desc = ask(
            f"Vector {i} - one-sentence description of the situation + person",
            default=existing.get("description") or None,
            multiline=True,
        )
        v_aliases_raw = ask(
            f"Vector {i} - comma-separated trigger words the Brain should scan for (e.g. 'salad bar, airport lunch, pret salad')",
            default=", ".join(existing.get("aliases", [])) or None,
        )
        aliases = [a.strip() for a in v_aliases_raw.split(",") if a.strip()]
        if i - 1 < len(vectors):
            vectors[i - 1] = {"name": v_name, "description": v_desc, "aliases": aliases}
        else:
            vectors.append({"name": v_name, "description": v_desc, "aliases": aliases})
    remember(state, "content_vectors", vectors)

    banner("4. Walls - where you do not play")
    hint("Walls are brand-safety lines that hold even when a tactic technically works. Most brands have 2.")
    w1_name = ask("Wall 1 - short name (e.g. 'Medicine and wellness', 'Investment advice')",
                  default=recall(state, "wall_1_name") or None)
    remember(state, "wall_1_name", w1_name)
    w1_register = ask("Wall 1 - what register / vocabulary do you not use? One paragraph.", multiline=True,
                      default=recall(state, "wall_1_register") or None)
    remember(state, "wall_1_register", w1_register)
    w1_triggers_raw = ask("Wall 1 - comma-separated trigger words the Brain should scan for (e.g. 'wellness, remedy, healing, cure')",
                          default=", ".join(recall(state, "wall_1_triggers", [])) or None)
    remember(state, "wall_1_triggers", [t.strip() for t in w1_triggers_raw.split(",") if t.strip()])

    w2_name = ask("Wall 2 - short name (e.g. 'Category comparison', 'Aspirational lifestyle')",
                  default=recall(state, "wall_2_name") or None)
    remember(state, "wall_2_name", w2_name)
    w2_register = ask("Wall 2 - what register / framing do you not use? One paragraph.", multiline=True,
                      default=recall(state, "wall_2_register") or None)
    remember(state, "wall_2_register", w2_register)
    w2_triggers_raw = ask("Wall 2 - comma-separated trigger words (e.g. 'vs competitor, supermarket version, premium brand')",
                          default=", ".join(recall(state, "wall_2_triggers", [])) or None)
    remember(state, "wall_2_triggers", [t.strip() for t in w2_triggers_raw.split(",") if t.strip()])


def section_forbids_licenses(state: dict[str, Any]) -> None:
    banner("5. Forbids and licenses - the copy hygiene gate")
    hint("Forbids are phrasings the brand never uses. Licenses are phrasings pre-cleared for use without review.")

    forbids_raw = ask("Forbidden phrasings - one per line. Things like 'any wellness claim', 'any category comparison', etc.",
                      multiline=True,
                      default="\n".join(recall(state, "forbids", [])) or None)
    forbids = [line.strip("- ").strip() for line in forbids_raw.splitlines() if line.strip()]
    remember(state, "forbids", forbids)

    licenses_raw = ask("Licensed phrasings - the things the brand always says. One per line.",
                       multiline=True,
                       default="\n".join(recall(state, "licenses", [])) or None)
    licenses = [line.strip("- ").strip() for line in licenses_raw.splitlines() if line.strip()]
    remember(state, "licenses", licenses)

    voice_refs = ask(
        "Voice register references - what brands sound the way you want to sound? Cadence references only, not category competitors.",
        multiline=True,
        default=recall(state, "voice_refs") or None,
        examples=["Aesop and Le Labo for restraint", "Stratechery for analytic cadence", "The Economist for newsroom register"],
    )
    remember(state, "voice_refs", voice_refs)

    never_name = ask(
        "Reference brands you specifically do NOT name in customer copy (comma-separated).",
        default=", ".join(recall(state, "never_name", [])) or None,
        examples=["AG1, LMNT, Liquid Death (for a food brand)", "Robinhood, eToro (for a fintech)"],
    )
    remember(state, "never_name", [b.strip() for b in never_name.split(",") if b.strip()])


def section_voice(state: dict[str, Any]) -> None:
    banner("6. Brand voice - the five-sentence statement")
    hint("Write five sentences that describe how the brand sounds. Each sentence answers one question.")

    five_sentence = ask(
        """The five-sentence voice. Address in order:
    1. Who is the voice (1 sentence)
    2. What they sound like (1 sentence)
    3. What they assume about the reader (1 sentence)
    4. What they reject in the category (1 sentence)
    5. What they swap in (1 sentence)""",
        multiline=True,
        default=recall(state, "five_sentence_voice") or None,
    )
    remember(state, "five_sentence_voice", five_sentence)

    banner("7. The seven hard rules")
    hint("CI-enforced. A PR that violates one fails the Brand Voice Check workflow. State each rule + the rationale.")
    hard_rules = recall(state, "hard_rules", []) or []
    for i in range(1, 8):
        existing = hard_rules[i - 1] if i - 1 < len(hard_rules) else {"rule": "", "rationale": ""}
        print()
        print(_color(f"Hard rule {i}", BOLD))
        rule = ask(f"Rule {i} - the rule itself in one sentence",
                   default=existing.get("rule") or None,
                   examples=["Short hyphens only - never em or en dashes.",
                             "No medicinal vocabulary.",
                             "Period-terminated declarative cadence.",
                             "Every external claim must trace to a primary source."])
        rationale = ask(f"Rule {i} - one-sentence rationale (why this rule exists)",
                        default=existing.get("rationale") or None)
        if i - 1 < len(hard_rules):
            hard_rules[i - 1] = {"rule": rule, "rationale": rationale}
        else:
            hard_rules.append({"rule": rule, "rationale": rationale})
    remember(state, "hard_rules", hard_rules)


def section_founder(state: dict[str, Any]) -> None:
    banner("8. Founder story - your authority anchor")
    hint("The founder story is the brand's authority anchor. It appears in long-form, never in headlines. Write it as autobiography, not as a product claim.")

    f_name = ask("Founder name (the protagonist of the story)",
                 default=recall(state, "founder_name") or recall(state, "your_name") or None)
    remember(state, "founder_name", f_name)
    f_story = ask(
        "Founder story - one or two paragraphs. Lived experience, not product claims. The customer pain you personally faced. The proof that the underlying problem is real.",
        multiline=True,
        default=recall(state, "founder_story") or None,
    )
    remember(state, "founder_story", f_story)

    f_truth = ask(
        "Structural truth - one sentence that says what this story proves about the underlying problem.",
        multiline=True,
        default=recall(state, "founder_structural_truth") or None,
    )
    remember(state, "founder_structural_truth", f_truth)

    f_traps = ask(
        "Traps to avoid when telling this story - one per line (e.g. 'making it sound like a product testimonial', 'over-claiming the outcome')",
        multiline=True,
        default="\n".join(recall(state, "founder_traps", [])) or None,
    )
    remember(state, "founder_traps", [line.strip("- ").strip() for line in f_traps.splitlines() if line.strip()])


def section_regulatory(state: dict[str, Any]) -> None:
    banner("9. Regulatory frames")
    hint("Name the regulators that touch your category and the practical constraint each one imposes on customer copy.")

    category = ask(
        "Your category in one phrase (food, supplements, fintech, cosmetics, education, etc.)",
        default=recall(state, "category") or None,
    )
    remember(state, "category", category)

    regulators = recall(state, "regulators", []) or []
    while True:
        idx = len(regulators) + 1
        print()
        if idx > 1 and not confirm(f"    add regulator {idx}?", default=(idx <= 2)):
            break
        if idx == 1:
            hint(f"    regulator {idx} (the primary one - your jurisdiction's main rule for the category)")
        jurisdiction = ask("Jurisdiction (e.g. UK, EU, US-Federal, US-California)", default="")
        if not jurisdiction:
            break
        name = ask("Regulator name (e.g. UK HMRC, EU EFSA, US FDA, US FTC)")
        ruleset = ask("Rule set / regulation name (e.g. VATA 1994 Sch 8 Grp 1, EU 1924/2006, 21 CFR 101)")
        constraint = ask("Practical constraint on copy - one paragraph", multiline=True)
        regulators.append({
            "jurisdiction": jurisdiction,
            "name": name,
            "ruleset": ruleset,
            "constraint": constraint,
        })
        if len(regulators) >= 4:
            break
    remember(state, "regulators", regulators)


# ---------------------------------------------------------------------------
# Renderers - turn state into Markdown / JSON
# ---------------------------------------------------------------------------


def _fill(template_text: str, mapping: dict[str, str]) -> str:
    """Replace {{ KEY }} placeholders in template_text with mapping values."""
    out = template_text
    for key, value in mapping.items():
        token = "{{ " + key + " }}"
        out = out.replace(token, value)
    return out


def _render_vectors_section(vectors: list[dict[str, Any]]) -> str:
    """Render the six vector bullets for positioning.md."""
    lines = []
    for i, v in enumerate(vectors, 1):
        name = v.get("name", f"Vector {i} - unnamed")
        desc = v.get("description", "(no description)")
        lines.append(f"{i}. **{name}.** {desc}")
    # Pad to 6 if fewer
    while len(lines) < 6:
        i = len(lines) + 1
        lines.append(f"{i}. **Vector {i} - not yet defined.** Add via `python3 tools/onboard.py` or edit this file.")
    return "\n".join(lines)


def _render_hard_rules(hard_rules: list[dict[str, str]]) -> str:
    lines = []
    for i, r in enumerate(hard_rules, 1):
        rule = r.get("rule", f"Rule {i} - not defined")
        rationale = r.get("rationale", "(no rationale)")
        lines.append(f"{i}. **{rule}** ({rationale})")
    while len(lines) < 7:
        i = len(lines) + 1
        lines.append(f"{i}. **Rule {i} - not yet defined.** Add via `python3 tools/onboard.py` or edit this file.")
    return "\n".join(lines)


def _render_regulators_table(regs: list[dict[str, str]]) -> str:
    rows = ["| Jurisdiction | Regulator | Rule set | Relevance to copy |", "|---|---|---|---|"]
    for r in regs:
        rows.append(f"| {r.get('jurisdiction', '?')} | {r.get('name', '?')} | {r.get('ruleset', '?')} | {(r.get('constraint', '') or '').splitlines()[0] if r.get('constraint') else '?'} |")
    if not regs:
        rows.append("| (none yet) | | | |")
    return "\n".join(rows)


def render_positioning(state: dict[str, Any]) -> str:
    a = state["answers"]
    vectors = a.get("content_vectors", []) or []
    vectors_section = _render_vectors_section(vectors)
    forbids_section = "\n".join(f"- {f}" for f in a.get("forbids", [])) or "- (define your forbids - things this positioning forbids in copy)"
    licenses_section = "\n".join(f"- {l}" for l in a.get("licenses", [])) or "- (define your licenses - phrasings pre-cleared for use)"
    never_name = ", ".join(a.get("never_name", [])) or "(none specified)"

    body = f"""# Positioning

Owner: {a.get('your_name', 'TBD')}. Status: filled by `tools/onboard.py` on {TODAY}. Version: 0.1.0.

This file is the strategic frame for every customer-facing decision. The Marketing Brain treats it as **Layer 0** - the gate every tactic must pass before it can ship.

## The positioning line

> **"{a.get('positioning_line', 'TBD')}"**

The single source of truth for every brand decision.

## ICP - ideal customer profile

- ICP: {a.get('icp', 'TBD')}

## Content vectors

Every customer-facing creative must fit one of the vectors below. The vector key + aliases for the Brain parser live in `08-templates/vocab/content-vectors.json`.

{vectors_section}

## Walls - where we do not play

| Wall | What we do not say |
|---|---|
| **Wall 1 - {a.get('wall_1_name', 'TBD')}** | {(a.get('wall_1_register', 'TBD') or '').replace(chr(10), ' ')} |
| **Wall 2 - {a.get('wall_2_name', 'TBD')}** | {(a.get('wall_2_register', 'TBD') or '').replace(chr(10), ' ')} |

The Brain auto-flags retrieved rows for Wall-1 and Wall-2 trigger words. The trigger lists live in `08-templates/vocab/hygiene-vocab.json`.

## What this positioning forbids in copy

{forbids_section}

## What this positioning licenses

{licenses_section}

## Founder credential

{a.get('founder_story', 'See `00-foundations/founder-stories.md`.').split(chr(10))[0]}

Full story in `00-foundations/founder-stories.md`. The founder credential is the authority anchor. State it factually. Avoid hype.

## Voice register references

{a.get('voice_refs', 'TBD')}

These are cadence references only - not category competitors.

## Reference brands we do NOT name in customer copy

{never_name}

These brands may appear in `05-evidence/` and `07-anti-patterns/` for internal pattern analysis. They never appear in customer-facing copy.

## How this file connects to the Marketing Brain

```bash
python3 tools/marketing_brain.py rebuild-index
python3 tools/marketing_brain.py icp
```

## Source

Onboarding interview run on {TODAY} via `tools/onboard.py`.
"""
    return body


def render_brand_voice(state: dict[str, Any]) -> str:
    a = state["answers"]
    body = f"""# Brand voice

Owner: {a.get('your_name', 'TBD')}. Status: filled by `tools/onboard.py` on {TODAY}. Version: voice-v1.0.0.

## The five-sentence voice

{a.get('five_sentence_voice', 'TBD')}

## The seven hard rules (CI-enforced)

{_render_hard_rules(a.get('hard_rules', []))}

## Banned vocabulary

A growing list. Add to it every time a draft includes one of these and you have to cross it out.

(populate this section as bans emerge - or run `tools/onboard.py` again with more answers)

## How to use this file

Every touchpoint copy file pins to a brand voice version in its front matter. When you edit a touchpoint file, check which voice version it honours.
"""
    return body


def render_voice_anti_patterns(state: dict[str, Any]) -> str:
    a = state["answers"]
    forbids = a.get("forbids", [])
    body = f"""# Voice anti-patterns

Owner: {a.get('your_name', 'TBD')}. Status: filled by `tools/onboard.py` on {TODAY}.

The complement to `brand-voice.md`. Brand voice says what we sound like. Anti-patterns say what we never sound like.

## Forbidden phrasings (from positioning)

{chr(10).join('- ' + f for f in forbids) if forbids else '- (none defined yet - re-run onboard.py or edit this file)'}

## Wall-1 triggers

These exact strings are scanned by the Brain on every retrieved row. A row containing one gets the Wall-1 hygiene flag.

The current list lives in `08-templates/vocab/hygiene-vocab.json`. To edit, change the JSON file, then run `python3 tools/marketing_brain.py rebuild-index`.

## Wall-2 triggers

Same mechanism as Wall-1, different content.
"""
    return body


def render_regulatory(state: dict[str, Any]) -> str:
    a = state["answers"]
    regulators_table = _render_regulators_table(a.get("regulators", []))
    body = f"""# Regulatory frames

Owner: {a.get('your_name', 'TBD')}. Status: filled by `tools/onboard.py` on {TODAY}.

## Category

{a.get('category', 'TBD')}

## Applicable regulators

{regulators_table}

## What this means for copy

For each regulator above, the practical constraint is stated in the table. Detailed register guidance:

"""
    for r in a.get("regulators", []):
        body += f"\n### {r.get('name', '?')} - {r.get('ruleset', '?')}\n\n{r.get('constraint', '?')}\n"
    body += """

## Trace requirements

Every external-facing factual claim must trace to one of:

- A primary source (regulatory filing, government register, lab report)
- A cited evidence file in `05-evidence/`
- A Brain Vault row with an `NV-NNN` ID
- An explicit `[INFERRED]` tag with reasoning

Claims that cannot trace fail the Claims Trace CI check.
"""
    return body


def render_founder_stories(state: dict[str, Any]) -> str:
    a = state["answers"]
    traps = a.get("founder_traps", [])
    body = f"""# Founder stories

Owner: {a.get('your_name', 'TBD')}. Status: filled by `tools/onboard.py` on {TODAY}.

## {a.get('founder_name', 'TBD')}

{a.get('founder_story', 'TBD')}

The structural truth this story carries: {a.get('founder_structural_truth', 'TBD')}.

### How to use this story

**Use in:** long-form founder-interview content; long-form podcast appearances; the Founder section of the website; the founder-pivot welcome email; founder's own DMs and replies when warranted.

**Do not use in:** tagline library; hero headlines; paid-ad creative as the primary hook; affiliate-creator briefs; brand-guidelines summary lines.

### Traps to avoid in the telling

{chr(10).join('- ' + t for t in traps) if traps else '- (none recorded yet)'}
"""
    return body


def render_content_vectors_json(state: dict[str, Any]) -> str:
    vectors = state["answers"].get("content_vectors", [])
    out_vectors = {}
    for v in vectors:
        if not v.get("name"):
            continue
        # slugify name as key
        key = re.sub(r"[^a-z0-9]+", "_", v["name"].lower()).strip("_") or f"vector_{len(out_vectors) + 1}"
        out_vectors[key] = {
            "name": v["name"],
            "aliases": v.get("aliases", []) or [v["name"].lower()],
            "description": v.get("description", ""),
        }
    data = {
        "$schema": "content-vectors-vocab-v1",
        "_meta": {
            "version": "1.0.0",
            "last_updated": TODAY,
            "description": "Content vectors are your ICP sub-segments. Every customer-facing creative must fit one of them. Generated by tools/onboard.py - edit by hand or re-run the wizard.",
            "source_of_truth": "00-foundations/positioning.md is the source of truth for vector definitions.",
            "owner": state["answers"].get("your_name", "TBD"),
            "loaded_by": "tools/marketing_brain.py at module-import time",
        },
        "vectors": out_vectors or {
            "example_segment": {
                "name": "Example segment - replace me",
                "aliases": ["example"],
                "description": "Re-run onboard.py to populate, or edit this JSON.",
            }
        },
    }
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def update_hygiene_vocab_json(state: dict[str, Any]) -> None:
    """Update wall_1_triggers + wall_2_triggers + never_name_brands in hygiene-vocab.json."""
    if not HYGIENE_VOCAB_JSON.exists():
        return
    data = json.loads(HYGIENE_VOCAB_JSON.read_text(encoding="utf-8"))
    a = state["answers"]
    w1 = a.get("wall_1_triggers", []) or []
    w2 = a.get("wall_2_triggers", []) or []
    never = a.get("never_name", []) or []
    if w1:
        data["wall_1_triggers"] = w1
    if w2:
        data["wall_2_triggers"] = w2
    if never:
        data["never_name_brands"] = never
    data.setdefault("_meta", {})
    data["_meta"]["last_updated"] = TODAY
    HYGIENE_VOCAB_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def write_all(state: dict[str, Any]) -> list[Path]:
    written: list[Path] = []
    POSITIONING_PATH.write_text(render_positioning(state), encoding="utf-8")
    written.append(POSITIONING_PATH)
    BRAND_VOICE_PATH.write_text(render_brand_voice(state), encoding="utf-8")
    written.append(BRAND_VOICE_PATH)
    ANTI_PATTERNS_PATH.write_text(render_voice_anti_patterns(state), encoding="utf-8")
    written.append(ANTI_PATTERNS_PATH)
    REGULATORY_PATH.write_text(render_regulatory(state), encoding="utf-8")
    written.append(REGULATORY_PATH)
    FOUNDER_STORIES_PATH.write_text(render_founder_stories(state), encoding="utf-8")
    written.append(FOUNDER_STORIES_PATH)
    CONTENT_VECTORS_JSON.write_text(render_content_vectors_json(state), encoding="utf-8")
    written.append(CONTENT_VECTORS_JSON)
    update_hygiene_vocab_json(state)
    written.append(HYGIENE_VOCAB_JSON)
    return written


SECTIONS = [
    ("meta", "About you", section_meta),
    ("positioning", "Positioning, ICP, content vectors, walls", section_positioning),
    ("forbids_licenses", "Forbids, licenses, voice references", section_forbids_licenses),
    ("voice", "Brand voice + seven hard rules", section_voice),
    ("founder", "Founder story", section_founder),
    ("regulatory", "Regulatory frames", section_regulatory),
]


def main() -> int:
    print()
    print(_color("Brand OS onboarding wizard", BOLD))
    print()
    print("This wizard fills the canonical foundation files in `00-foundations/` and the")
    print("content-vectors / hygiene JSON in `08-templates/vocab/` from your answers.")
    print()
    print("It is interview-only. Nothing leaves your machine. No external services touched.")
    print()
    print(_color("Save-as-you-go:", DIM) + " the wizard writes after each section. You can quit (Ctrl+C)")
    print(_color("at any time and re-run to pick up where you left off.", DIM))
    print()
    if not confirm("Ready to begin?", default=True):
        print("Aborted. State preserved in .brand-os-state.json.")
        return 0

    state = load_state()

    for key, label, fn in SECTIONS:
        if key in state.get("sections_completed", []):
            if not confirm(f"  section already completed: {label}. Redo it?", default=False):
                continue
        try:
            fn(state)
        except KeyboardInterrupt:
            print()
            print(_color("Interrupted. State saved - re-run to continue.", DIM))
            save_state(state)
            return 1
        state.setdefault("sections_completed", []).append(key)
        save_state(state)
        print()
        print(_color(f"  section saved: {label}", DIM))

    print()
    print(_color("All sections complete. Writing canonical files...", BOLD))
    written = write_all(state)
    print()
    for p in written:
        try:
            rel = p.relative_to(REPO_ROOT)
        except ValueError:
            rel = p
        print(_color(f"  wrote {rel}", DIM))

    print()
    print(_color("Done.", BOLD))
    print()
    print("Next steps:")
    print("    1. Review the files in 00-foundations/ - edit by hand where needed.")
    print("    2. Rebuild the Brain index:")
    print("           python3 tools/marketing_brain.py rebuild-index")
    print("    3. Confirm the index sees your ICP:")
    print("           python3 tools/marketing_brain.py icp")
    print("    4. Start adding cocktails as real use cases arise:")
    print("           edit 01-canon/cocktail-recipes.md, then rebuild-index")
    print("    5. Local web interface:")
    print("           python3 -m venv .venv && .venv/bin/pip install -r web/requirements.txt")
    print("           .venv/bin/python web/app.py")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
