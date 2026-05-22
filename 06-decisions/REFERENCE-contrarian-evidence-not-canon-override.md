# REFERENCE - capturing contrarian voices as evidence, not canon override

Owner: this is a reference / pattern document, not a brand-specific decision. Status: **canonical pattern**, do not delete.

This file documents the rule that governs how to capture stakeholder voices that contradict a locked canon decision. The pattern is captured here so future Claude sessions and contributors record dissent without confusing it with canon override, and so the brand has an audit trail for re-evaluation when relevant data lands.

## The rule

**When a stakeholder voice contradicts a locked canon decision, capture the dissent as evidence in `05-evidence/contrarian-hypotheses/<date>-<short-slug>.md`, not as a canon edit. The locked decision stands until the priority-hierarchy authority that locked it re-decides. Capture trigger conditions for re-evaluation so the contrarian voice gets honest reconsideration when those conditions land.**

The contrarian voice is honored by being captured, not by overriding. Honest record-keeping > silent burying or unauthorized override.

## When to use this pattern

Apply this pattern when ALL of the following are true:

1. A canon decision is locked in `06-decisions/` and reflects the authority that owns the brand voice (founder verbatim, top of priority hierarchy).
2. A stakeholder (designer, marketer, advisor, investor, customer-research finding) raises a contrarian gesture - either a hypothesis that contradicts the decision or evidence that the decision may be wrong.
3. The stakeholder is NOT the authority that locked the decision (their voice sits lower in the priority hierarchy than the locked record).
4. There is no immediate triggering data that justifies re-decision (otherwise it would be a re-decision, not a contrarian voice).

Without those four, the situation calls for a different response:

- If the authority that locked the decision is the one raising the contrarian view, that is a re-decision and the canon updates.
- If new triggering data already justifies re-decision, that is a re-decision in flight - capture it as a new decision record, not as evidence.
- If the stakeholder's voice sits at or above the authority that locked the decision in the priority hierarchy, fix the canon directly (do not capture as contrarian evidence).

## Why "evidence, not override" matters

Three failure modes follow from not having this rule:

1. **Silent burying** - the brand pretends the contrarian voice did not happen. Six months later, the same voice surfaces from a different stakeholder and nobody remembers it was raised before. The brand learns the same lesson twice.
2. **Unauthorized override** - someone who is not the authority that locked the decision quietly edits the canon to reflect the contrarian view. The brand's priority hierarchy is silently violated, and the canon now reflects a position that the brand owner did not sign off on.
3. **Conflict-avoidance dilution** - the canon decision gets edited to add hedging language ("on the other hand, ..." / "in some cases, ..."), which makes the canon mushy and provides no actionable guidance.

The "evidence, not override" rule prevents all three. Contrarian voices get full honest record (file in `05-evidence/contrarian-hypotheses/`, verbatim quote, reasoning), but the locked canon stays locked until the authority re-decides.

## What the evidence file should contain

Per the shape used in the example file:

1. **Header** with date captured + source attribution (name + role + channel)
2. **The contrarian quote verbatim** - in the original language if possible, with translation if non-English
3. **What the contrarian voice is observing** - charitable interpretation of the hypothesis
4. **Public-source evidence relevant to the hypothesis** - what does the market actually look like for this question
5. **Why the locked decision stands** - the priority-hierarchy reasoning + the specific reasons the contrarian view does not override the locked decision today
6. **Trigger conditions for re-evaluation** - specific data signals that would justify re-opening the decision. Be specific - "if subscription path underperforms" is not specific; "if Phase 1 launch shows <30% subscription-to-retail conversion or <50% 90-day retention" is.
7. **Decision authority** - explicit reference to the CLAUDE.md priority hierarchy + where the locked decision and the contrarian voice sit on that hierarchy
8. **Related canon** - cross-references to the decision record + any other relevant files
9. **Open follow-ups** - when does this evidence file get re-reviewed (typically quarterly or at a launch milestone)

## Banned approaches

| Anti-pattern | Why it fails |
|---|---|
| Silently ignoring the contrarian voice | Brand learns the same lesson twice |
| Unauthorized canon edit to reflect contrarian view | Violates priority hierarchy; brand owner has not signed off |
| Adding hedging language to canon ("on the other hand...") | Canon becomes mushy and unactionable |
| Capturing contrarian view as a NEW canon decision (rather than evidence) | Implies parity with the locked decision; reader cannot tell which one is canonical |
| Refusing to capture the contrarian voice in writing at all | Loses the audit trail |

## Pattern in practice

Example flow:

1. Founder verbatim locks decision in `06-decisions/<date>-<decision-slug>.md` (level 1 in CLAUDE.md priority hierarchy).
2. Designer / advisor / investor raises contrarian view in WhatsApp / Slack / email (level 8 in priority hierarchy - third-party voice).
3. Capture contrarian view in `05-evidence/contrarian-hypotheses/<date>-<stakeholder>-<short-slug>.md` per the structure above.
4. Locked decision stands.
5. Quarterly review surfaces the evidence file at the next scheduled checkpoint.
6. If trigger conditions have landed, escalate to founder for re-decision (which becomes a NEW decision record).
7. If trigger conditions have not landed, evidence file stays open; next review at next checkpoint.

## How to verify the rule is working

Three checks:

1. **Contrarian voices that surfaced in the last 90 days are captured**. Scan WhatsApp / Slack / email for the language of contrarian gestures ("contrarian hypothesis", "playing devil's advocate", "but consider that...", "I am not sure about..."). Each one should map to a file in `05-evidence/contrarian-hypotheses/` (or to a re-decision if it earned one).

2. **Locked decisions reflect their priority-hierarchy authority**. The decision records have a clear authority attribution at the bottom. The contrarian evidence files reference but do not contradict the decision records.

3. **Quarterly review happens**. A scheduled task (calendar event, dream-v2 task, manual review) opens the `05-evidence/contrarian-hypotheses/` directory every quarter and re-reads each file. Reviews close any obsolete files and open any that have new triggering data.

## Relationship to other canon

| Sibling file | What it owns | Relationship to this pattern |
|---|---|---|
| `CLAUDE.md` priority hierarchy | The priority order of sources of truth | The "decision authority" section of every contrarian evidence file references this. |
| `06-decisions/` | Append-only locked decision records | Contrarian evidence files cross-reference the decision they sit alongside. |
| `05-evidence/` | Third-party evidence captures | The contrarian-hypotheses subdirectory sits inside this folder. |
| Brand voice + manifesto / positioning canon | Locked brand voice + positioning | Contrarian views about voice / positioning / pricing / strategy all use this pattern. |

## How to extend the rule

If your brand later has more than ~10 active contrarian evidence files at any time, consider grouping them by topic (pricing contrarians / positioning contrarians / category contrarians) inside `05-evidence/contrarian-hypotheses/` for easier review.

If your brand later has contrarian voices from stakeholders who are AT priority hierarchy level 2-3 (memory feedback rules / CLAUDE.md), those are not contrarian-evidence cases - they are conflicts inside the priority hierarchy that need resolution upstream (founder re-decision or hierarchy reordering).

If a contrarian voice gets validated by data and triggers a re-decision, the original evidence file gets a "Status: validated, decision re-opened" header update + cross-reference to the new decision record. The file is not deleted - it remains as the audit trail of when the brand learned what.

## Sources

- Cialdini _Influence_ ch. 6 (Authority) - authority works when authority is consistent; capturing contrarian voices as evidence preserves the consistency of the locked decision while honoring the dissent
- Bohner-Einwiller-Erb-Siebler 2003 _JCP_ 13(4) (Pratfall) - acknowledging weaknesses and trade-offs of a decision (in writing, not in copy) builds trust over time with the team
- Kahneman _Thinking, Fast and Slow_ ch. 22 (Expert intuition: When can we trust it?) - intuitions of stakeholders below the decision authority are signal, not override; this pattern operationalises that
- Hugo Mercier and Dan Sperber - the argumentative theory of reasoning: capturing dissent in writing makes the brand's reasoning auditable to itself over time
