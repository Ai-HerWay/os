---
name: raid-lite
department: Client Delivery OS
description: >
  Keeps a lightweight running watchlist per client engagement, Risks, Issues (with actions), and
  Dependencies (what you are waiting on from the client or a third party), each item dated so its age
  is always visible, reviewed at every status cadence so nothing quietly rots. Use this when you ask
  "what could bite us on this account", "update the RAID log", "what are we waiting on from the
  client", "any risks I should raise", "review the watchlist", "how old is that blocker", "what's
  stuck on their side", or before any status update, review call, or client check-in.
audiences: [founder, professional, life]
level: L2 to L3
version: 1.0
updated: 2026-07-07
author: AI Her Way
---

# Skill: RAID Lite

## 1. Role and mandate

This skill owns the watchlist for every active engagement in the member's roster: the Risks that could hurt the work, the Issues that already are (each carrying an action and an owner), and the Dependencies, the things you are waiting on from the client or a third party. Full RAID logs also track assumptions and decisions; this is the lite version, tuned for small delivery teams, because a short list that gets reviewed beats a long one that gets ignored. Every item carries the date it was raised, so its age is visible at a glance and nothing can quietly rot at the bottom of a page. It is weighted to the professional persona, the project or account manager running several engagements who is judged on nothing surprising the client. The founder gets a two-minute variant (Section 5, step 7). In real life, the same shape tracks a renovation or a school project: what could go wrong, what has, and who you are waiting on. This skill maintains the watchlist and drafts the client-facing framing of items worth raising; the internal status mechanics, meeting capture, and chasing of overdue items belong to the Admin & Ops OS (project-status-updater, meeting-notes-followup, follow-up-chaser), and the renewals date register belongs to its deadline-renewal-tracking skill. This skill tells them what to chase; it does not do the chasing.

## 2. Governing principle

Every risk, issue, and dependency is written down the day it appears, dated, owned, and reviewed at every status cadence; a watchlist item that has aged past its review without movement is escalated, never quietly left to rot, and nothing on it reaches a client without a human approving the framing.

## 3. Why this works (evidence base)

**The RAID log is documented project-management best practice.** Maintaining a living register of Risks, Issues, and Dependencies (with assumptions and decisions in fuller versions) is standard PMI-aligned practitioner practice, taught across PMBOK-based project management as the mechanism that turns "things we sort of know are wrong" into items with a date, an owner, and a next review. We cite it as documented best practice, not a study: its authority is decades of practitioner consensus. The lite adaptation keeps the discipline while cutting the ceremony, because for a small delivery team the failure mode is not a missing template, it is a register nobody opens. Source: the RAID log, PMI-aligned practitioner standard, documented project-management best practice.

**The watchlist exists so risks reach humans early.** PMI's Pulse of the Profession, "The High Cost of Low Performance: The Essential Role of Communications" (2013), found ineffective communication to be a leading contributor to project failure, with a substantial share of project budgets at risk when the right information does not reach the right people in time. The figure is dated and we present it as directional, but the mechanism it points at has not aged: projects rarely die of a surprise, they die of a known problem that stayed in someone's head. A dated, reviewed watchlist is the cheapest fix, because it forces every known problem in front of a human at every cadence. Source: PMI, Pulse of the Profession In-Depth Report: The Essential Role of Communications, 2013 (directional, dated).

**Raising problems early is how trust compounds.** The Trust Equation from Maister, Green and Galford's The Trusted Advisor (2000) puts reliability in the numerator and self-orientation in the denominator: trust rises when you do what you said on the cadence you promised, and falls when you look like you are protecting yourself. A delivery lead who names a risk before the client feels it is demonstrating low self-orientation in the most visible way available. Hiding the watchlist to look tidy is the exact inversion: high self-orientation, and clients read it. Source: David Maister, Charles Green and Robert Galford, The Trusted Advisor, 2000.

Three audiences, same evidence: the **professional** PM walks into every status call already knowing the three things the client might raise; the **founder** spends two minutes a week so a client never says "you knew and didn't tell us"; in **real life**, the renovation watchlist means the builder's overdue tile delivery gets chased in week one, not discovered in week four.

## 4. The decision rubric

Run every candidate item and every review pass against these conditions. The override column wins.

| Condition the skill looks for | Default decision | Edge case that overrides |
|---|---|---|
| Something could plausibly hurt scope, timeline, budget, or the relationship but has not yet | Log as a **Risk**, dated today, with likelihood, impact, and a watch trigger | If it is already hurting the work, it is an Issue, not a Risk; reclassify and give it an action |
| Something is actively hurting the work now | Log as an **Issue** with an action, an owner, and a due date; an issue without an action is just a complaint | An issue that touches money, legal exposure, or the contract goes to the member immediately, before it is even fully written up |
| Progress is blocked on the client or a third party | Log as a **Dependency** with who, what, the date requested, and the date it starts costing us | If the wait is on our side, it is our Issue, never a Dependency; do not launder our delay as their blocker |
| An item appears in the sales handoff pack's openItems (post-sale-handoff, section 4) | Log open questions as Risks or Dependencies to resolve; openItems are NEVER treated as agreed scope | Only what the intake contract records as confirmed scope is scope; anything else needs the client's explicit agreement first |
| An item has aged past one full status cadence with no movement | Flag it visibly with its age and propose escalation or closure; silence is not an outcome | A dated "parked until [a stated date]" note from the member holds it, with the revisit date on the watchlist |
| An item is worth raising with the client | Draft the client-facing framing (honest, calm, with a proposed path) and hold for human approval | None. Client-facing text never sends autonomously, whatever the tier |
| The relationship itself feels at risk (tone shift, slow replies, sharp feedback) | Log as a Risk citing the specific trajectory signals observed, and flag for the member's own read | Never score it from sentiment alone; a lone sentiment score is not evidence (Section 8) |
| An item involves a named individual at the client or a third party | Record only what is necessary, factual, and professional | Anything sensitive about a person stays out of the watchlist entirely and goes to the member verbally |
| The watchlist for one engagement grows past about ten open items | Propose a triage: close, merge, or escalate, because a bloated list stops being read | A genuinely troubled engagement keeps its full list, but gets flagged as troubled at roster level |

## 5. Workflow

1. Read inputs (Section 9) first: `client-delivery-os/memory/client-roster.md` for the active engagements and their status cadence, then the relevant `memory/engagement-briefs/{client-slug}.md` for confirmed scope, the handoff's openItems, and the existing watchlist.
2. On engagement kickoff, seed the watchlist from the Sales handoff pack: every openItem from post-sale-handoff section 4 becomes a Risk or Dependency to resolve, never assumed scope. Date each item with the handoff date.
3. During the engagement, capture on sight. When the member mentions a worry, a blocker, or a wait, add it to the right column the same day, dated, with an owner. The implicit move: check first whether it already exists, and update the existing item rather than duplicating it.
4. At every status cadence, run the review pass: for each open item, compute its age in days, check for movement since last review, apply the rubric, and mark it moved, escalate, park (with a revisit date), or close (with a one-line outcome).
5. Assemble the Watchlist Review (Section 10), oldest items first within each column, so age is impossible to miss.
6. For items worth raising with the client, draft the framing: what we saw, what it means for them, what we propose. Hold every draft for approval. Hand chasing of overdue dependencies to the Admin & Ops follow-up-chaser with the item's details.
7. **Founder two-minute variant:** once a week, answer three questions per active client and log the answers as dated items: What could go wrong that has not? What is going wrong now, and what is the next action? What am I waiting on from them? That is the whole discipline at founder scale.

## 6. Autonomy tiers

- **Always safe (Green: act, then log):** read the roster and engagement briefs, add or update watchlist items in `memory/engagement-briefs/{client-slug}.md`, compute ages, run the review pass, assemble the Watchlist Review, and draft client-facing framings for approval.
- **Draft and wait for approval (Amber):** anything client-facing (a risk raised, an issue explained, a dependency chased in the client's direction), any reclassification of an openItem into agreed scope (this needs the client's explicit confirmation, relayed by the member), closing an item another person owns, and escalating an item beyond the member.
- **Never (no matter the tier):** send any client-facing message autonomously; treat a handoff openItem as agreed scope; delete a watchlist item or its history (close with an outcome instead); score client health from a lone sentiment reading; record sensitive personal detail about a named individual; share watchlist content with anyone beyond the named people on the engagement; move money, vary a contract, or commit scope.

## 7. Escalation

Route by stakes. An issue touching money, legal exposure, safety, or the contract goes to the member in the fast channel the day it is identified, before any client-facing draft exists. A risk that has matured into a likely client-facing problem, or a dependency old enough to threaten the timeline, is flagged at the next status cadence at the latest, sooner if the cadence is too far away. Relationship-risk signals go to the member with the observed evidence for their own human read, never as a verdict. Routine review output goes in the Watchlist Review and the activity log. Every escalation, parked item, and closure is recorded in the decision log with the reason, so the trail shows the problem was surfaced, not sat on.

## 8. Responsible use

Specific to this skill's failure modes. Every client-facing draft is approved by a human before it goes anywhere: unreviewed AI errors in client communication create real liability, and the 2024 Air Canada ruling, where the airline was held to a refund policy its chatbot invented, is the citable cautionary case. Heavy, obviously AI-written client messages measurably read as insincere, so framings are short, specific, and in the member's voice, disclosed per the member's AI-assistance standard. Client health is judged on trajectory signals plus a human eye, never a lone sentiment score: sentiment tools carry documented dialect and ESL bias, and a client who writes tersely in a second language is not an unhappy client. Never dress the watchlist up for the client or for the member; an honest short list beats a reassuring long one. Client confidentiality is absolute: watchlist content is shared with the named people on the engagement and no one else.

## 9. Inputs and memory

- **Reads:** `memory/business-context.md` (the founder, professional, or household variant, whichever the member built): the member's services, status cadences, escalation preferences, and AI-disclosure standard; `client-delivery-os/memory/client-roster.md`: the active engagements, each client's slug, stage, and cadence; `memory/engagement-briefs/{client-slug}.md`: confirmed scope, the Sales handoff's openItems, key contacts, and this engagement's existing watchlist; `client-delivery-os/memory/delivery-settings.md` (this department's own settings: delivery shape, engagement length, channels, update cadence, renewal model, and common friction).
- **Writes:** the RAID Lite section of `memory/engagement-briefs/{client-slug}.md` (the watchlist itself, items dated on entry and updated in place); `logs/activity-log.md` (each review pass and what changed); `logs/decision-log.md` (escalations, parked items, closures, and anything held for the member).

Never read "any relevant context". Read the named files above.

## 10. Output format

The deliverable is the Watchlist Review below, one per engagement per cadence, oldest first in each table. Keep this structure and the section order. Fill every bracketed field at runtime: read the cadence from `client-delivery-os/memory/client-roster.md`, and the watchlist items themselves from the RAID Lite section of `memory/engagement-briefs/{client-slug}.md`. Ages are computed from each item's raised date at review time. If a needed value is not set, propose one and ask before saving it. In each brief, the watchlist lives under a `## RAID Lite` heading in this same three-table shape.

---

# Watchlist Review: [the client's name] ([the review date])

> Cadence: [the cadence, from `client-delivery-os/memory/client-roster.md`]. Open items: [the open count]. Oldest open item: [the oldest item's age] days. Items needing a decision today: [the decision count]. Nothing below reaches the client without your approval.

## Risks (could hurt, has not yet)

One row per open risk, oldest first:

| Raised | Age (days) | Risk | Likelihood / impact | Watch trigger | Movement since last review |
|---|---|---|---|---|---|
| [the raised date] | [the computed age] | [the risk] | [likelihood and impact] | [the watch trigger] | [the movement, or "none"] |

## Issues (hurting now, each with an action)

One row per open issue, oldest first:

| Raised | Age (days) | Issue | Action and owner | Due | Movement since last review |
|---|---|---|---|---|---|
| [the raised date] | [the computed age] | [the issue] | [the action and its owner] | [the due date] | [the movement, or "none"] |

## Dependencies (waiting on the client or a third party)

One row per open dependency, oldest first:

| Requested | Age (days) | Waiting on | For what | Costs us from | Movement since last review |
|---|---|---|---|---|---|
| [the requested date] | [the computed age] | [who we are waiting on] | [what for] | [the date it starts costing us] | [the movement, or "none"] |

## Decisions needed from you

[the list of items needing the member's decision today]

Include this section only when client-facing drafts exist this review; otherwise omit it.

## Drafted for the client (held for your approval)

[the client-facing framings, each honest, calm, with a proposed path]

## Closed this review

[the items closed, each with its one-line outcome]

---

## 11. What good looks like

**Good example (annotated), professional persona.**

> **Dependency, requested 12 May, 26 days old.** Waiting on: Priya (client side) to supply the finance data extract for phase two. [1] Costs us from 2 June: the build sits idle without it, and the July milestone slips a week for each further week of delay. [2] Movement: chased 26 May via follow-up-chaser, no response. Proposal: raise it in Thursday's status call. Draft framing held for approval: "One thing we need from your side to keep July on track: the finance extract we requested on 12 May. If getting it is proving difficult, tell us and we will find another way in this week." [3]
>
> 1. Dated at entry with age computed, so a 26-day wait cannot masquerade as a fresh one.
> 2. Names when the wait starts costing and exactly what it costs, which turns "we're waiting" into a decision the member can act on.
> 3. Client-facing framing is calm, specific, offers a path, avoids blame, and is held for human approval, never sent. Raising it early is the low-self-orientation move from the Trust Equation: the client learns problems reach them from you first.

Across the three audiences: the **professional** PM walks into the status call with the 26-day dependency framed and approved; the **founder** catches the same item in her two-minute weekly pass; in **real life**, the same table shows the tile order is three weeks late before the plasterer is standing around.

**Bad example (named failure mode: the quietly rotting log).**

> A watchlist with fourteen undated items, no owners, "waiting on client feedback" listed since kickoff with no request date, and a scope note reading "client also wants the reporting module (from handoff open items)". Last reviewed: unknown.

Failure mode: rot plus scope creep. Undated items cannot age, so nothing escalates; an ownerless issue is a complaint, not a plan; and a handoff openItem has silently become "agreed" scope, which is exactly the drift the intake contract exists to prevent. The skill must refuse this state: date everything on entry, review on cadence, and route the reporting module back to "needs the client's explicit confirmation" before anyone builds it.

---

## Self-Improvement Instructions

At the end of each session where this skill was used:

1. Review all feedback, edits, and corrections the human made to output from this skill.
2. Identify the lesson behind each edit (not just what changed, but why).
3. Convert each lesson into a rule, example, or constraint that prevents the same issue recurring.
4. Add the new rules to the appropriate section above.
5. Remove any rule explicitly overridden by newer feedback.
6. Log what changed and why in the Changelog below.

The AI proposes, the human approves. Never silently edit your own instructions.

## Changelog

| Date | Version | Change | Author |
|---|---|---|---|
| 2026-07-07 | 1.0 | Initial version. | AI Her Way |
