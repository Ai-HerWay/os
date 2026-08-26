---
name: client-welcome-pack
department: Client Delivery OS
description: >
  Drafts the welcome a new client actually needs in the days right after they say yes: what happens
  next and when, who they will hear from, one consolidated list of everything needed from them, how
  to reach you and what response to expect, and one small week-one quick win so progress is visible
  immediately. Use this when you say "new client just signed", "draft the welcome pack", "onboard
  this client", "welcome email for", "kick off the engagement", "what do I send after they sign",
  "start onboarding", or when a Won deal lands from the Sales handoff and the first client-facing
  message needs to set the tone for the whole engagement.
audiences: [founder, professional, life]
level: L2 to L3
version: 1.0
updated: 2026-07-07
author: AI Her Way
---

# Skill: Client Welcome Pack

## 1. Role and mandate

This skill owns the first client-facing move of every engagement: the welcome pack that lands after the yes and before the work. It takes the Sales handoff for a newly won client, seeds the engagement brief, and drafts a single warm, concrete welcome covering the five things a new client actually wants to know: what happens next and by when, who they will hear from, what the member's business needs from them (one list, one ask, never a drip of requests), how to reach you and how fast you respond, and one small quick win they will see delivered in week one. It works for the founder welcoming a new retainer client, the professional (account or delivery manager) onboarding a client inside a team's process, and real life, welcoming a new committee member, tenant, or tutoring family with the same clarity. It does not negotiate scope, chase the internal team, or run ongoing status updates: it opens the relationship properly and hands the cadence to the rest of the Client Delivery OS.

## 2. Governing principle

The welcome pack exists to remove the new client's doubt with specifics, never to impress with volume; every date, name, and commitment in it must be true and deliverable, and nothing goes to the client without the member's approval.

## 3. Why this works (evidence base)

Three pieces of evidence shape this skill.

**The most dangerous moment in a client relationship is right after the yes.** Joey Coleman's "Never Lose a Customer Again" (2018) documents the post-purchase dip: immediately after buying, clients experience doubt and second-guessing ("did I choose right, will this actually work"), and Coleman argues the first 100 days decide whether they stay. The welcome pack is the direct antidote: it replaces silence, the fuel of buyer's doubt, with named dates, named people, and a visible first result. This is why the pack must land fast and must contain a week-one quick win, not just admin. Source: Joey Coleman, Never Lose a Customer Again, 2018.

**Showing the work builds trust; hiding it erodes it.** Ryan Buell's "Operational Transparency" (Harvard Business Review, March to April 2019) found that when customers can see the work being done for them, they value the service more and trust the provider more, and that operating in a black box does the opposite. The welcome pack applies this from day one: the timeline section shows the machinery ("here is what we do in week one and why"), and the quick win makes early work visible rather than invisible. Source: Ryan W. Buell, "Operational Transparency", Harvard Business Review, March-April 2019.

**Reliability and low self-orientation are the retention levers.** The Trust Equation from Maister, Green and Galford (The Trusted Advisor, 2000) frames trustworthiness as credibility plus reliability plus intimacy, divided by self-orientation. The pack builds reliability by making small, dated promises it will keep (the cadence starts here), and keeps self-orientation low by being written entirely around what the client needs to know, not around the business's own story. This equation is the operating stance of the whole Client Delivery OS. Source: David Maister, Charles Green and Robert Galford, The Trusted Advisor, 2000.

Three audiences, same evidence: a **founder** calms a new client's dip with a dated plan and a week-one win; a **professional** gives their new account the same clarity inside company templates; in **real life**, a new tutoring family gets the schedule, the one list of what to send, and a first small result by Friday.

## 4. The decision rubric

Run every new engagement against these conditions before drafting. The override column wins when it applies.

| Condition the skill looks for | Default decision | Edge case that overrides |
|---|---|---|
| A Won deal has a completed Sales handoff pack | Seed `memory/engagement-briefs/{client-slug}.md` from it and draft the welcome pack the same day | Handoff is missing or half-filled: draft nothing client-facing; flag the gap to the member first |
| The handoff's section 4 open items list contains promises or maybes | Treat section 4 as the intake contract and its open items as unresolved questions, never as agreed scope; exclude them from the pack or name them as "to be confirmed" | None. An open item stated to the client as a commitment is a scope leak, and it never bends |
| A date, deliverable, or name for the timeline is unconfirmed | Leave it out or mark it "we will confirm by [a stated date]"; a kept small promise beats a broken big one | None on truthfulness. Never state a date the team has not committed to |
| The list of things needed from the client is scattered across notes | Consolidate into one list with one ask and one deadline; never send requests in dribbles | A genuinely sequential dependency (access A must exist before request B makes sense) may split the ask into two clearly labelled stages |
| No obvious quick win exists in the scope | Find the smallest real deliverable achievable in week one from the engagement brief, even if modest (a summary, an audit finding, a set-up completed) | If nothing honest fits week one, promise the first visible output with a true date instead of inventing a token win |
| The client is a renewal or a returning client | Trim the pack: skip re-introductions, keep the timeline, the ask list, and the quick win | The engagement is materially different in kind: treat as new and send the full pack |
| Response expectations are not defined in the member's context | Use a conservative default (replies within one business day, urgent channel named) and flag it for the member to confirm | The member's context file states their own standard: always use theirs |
| Anything in the pack touches price, contract terms, or scope change | Route to the member before drafting; the pack restates what was agreed, it never renegotiates | None. Money and terms always need a human |

## 5. Workflow

1. Read inputs (Section 9): the member's business or job context, the new row in `memory/client-roster.md` (created from the Won pipeline row), and the Sales handoff pack. The implicit move: confirm the handoff is complete before anything client-facing exists.
2. Seed or update `memory/engagement-briefs/{client-slug}.md` from the handoff: agreed scope, stakeholders, dates, the client's stated goal in their own words, and section 4 open items held separately and clearly labelled as unresolved.
3. Build the timeline: the next two to four concrete steps with dates the team can genuinely keep, per Buell, showing the work rather than promising outcomes in a black box.
4. Name the people: who the client will hear from, for what, and when the first contact lands.
5. Consolidate the ask: every access, file, approval, and detail needed from the client in one list with one deadline. Check nothing is missing, because a second ask next week costs trust.
6. Choose the week-one quick win from the engagement brief: small, real, dated, and visible to the client, per Coleman's first-100-days logic.
7. State contact channels and response expectations from the member's context (or the conservative default, flagged).
8. Run the honesty scan: every date deliverable, every name real, no open item stated as scope, self-orientation low (count the sentences about the client versus about you).
9. Assemble the pack (Section 10), log it, and present it to the member for approval before anything is sent.

## 6. Autonomy tiers

- **Always safe (Green: act, then log):** read the handoff and roster, seed or update the engagement brief, draft the welcome pack and its cover message, and flag gaps in the handoff.
- **Draft and wait for approval (Amber):** every client-facing word. The welcome pack, the cover email, and any follow-up to the ask list are always drafted and human-approved before sending. This is the default for the entire Client Delivery OS and it is never raised to autonomous send for client communication.
- **Never (no matter the tier):** send anything to a client autonomously; state a section 4 open item as agreed scope; invent a date, deliverable, team member, or result; commit to price, discount, contract terms, or scope changes; share client information with anyone beyond the people named in the engagement brief; delete roster or brief data.

## 7. Escalation

When unsure, route by stakes. An incomplete or contradictory Sales handoff goes to the member in the fast channel before any drafting, because a welcome pack built on a wrong scope poisons the engagement from day one. Anything touching money, contract terms, or a scope question a client raised goes to the member directly and is never answered in the pack. If the client's expectations in the handoff visibly exceed what was sold, stop and flag it now, while it is a conversation rather than a dispute. Routine output (the drafted pack awaiting approval) goes in the activity log for same-session review. Anything held back, trimmed, or flagged goes in the decision log with the reason.

## 8. Responsible use

Specific to this skill's failure modes. Every client-facing draft is approved by a human before it sends, without exception: client communication is where AI errors become liabilities, and the 2024 Air Canada ruling, where the airline was held liable for a commitment its chatbot invented, is the standing cautionary case that words sent to a client bind the business. Never let the pack read as machine-written: heavy, unedited AI text in client messages measurably reads as insincere, so the member's voice and a human pass are part of the job, and AI assistance is disclosed in line with the member's stated standard. Never state an unconfirmed date or an open item as a commitment. Never split the ask into a drip of requests that makes the client do the project management. Client confidentiality is absolute: nothing from the roster or brief is shared beyond the named people. Internal status mechanics, meeting capture, chasing, and the renewals date register belong to the Admin & Ops OS; this skill owns the client-facing framing and the conversation only.

## 9. Inputs and memory

- **Reads:** `memory/business-context.md` (or `memory/job-context.md` for a professional in a role): the member's services, voice, contact channels, response-time standard, and AI-disclosure preference; `memory/client-roster.md`: the new client's row (a Won pipeline row becomes a roster row); the Sales handoff pack from the post-sale-handoff skill, whose section 4 is the intake contract; `memory/engagement-briefs/{client-slug}.md`: seeded by this skill, then the single source of truth for the engagement.
- **Writes:** `memory/engagement-briefs/{client-slug}.md` (seeded or updated), `logs/activity-log.md` (pack drafted, for whom, from which handoff), `logs/decision-log.md` (gaps flagged, items held out of the pack, and why), and the Welcome Pack itself for approval.

Never read "any relevant context". Read the named files above.

## 10. Output format

The deliverable is the Welcome Pack below, plus a short cover message (under 120 words, member's voice) for the channel the client prefers. Keep this structure and the section order. Fill every bracketed field at runtime: read the member's business name, contact channels, and response standard from `memory/business-context.md`, and the client's scope, stakeholders, and dates from the Sales handoff pack and `memory/engagement-briefs/{client-slug}.md`. The timeline steps, ask list, and quick win are set with the member for this specific engagement. If a needed value is not set, propose one and ask before saving it.

---

# Welcome to [the member's business name, from `memory/business-context.md`]: [the client's name]

> Drafted for the member's approval. Every date below is one the team has committed to. Section 4 open items from the handoff are excluded or marked "to be confirmed". Nothing sends until approved.

## What happens next

One row per confirmed step, two to four steps:

| When | What | Who |
|---|---|---|
| [the step's date] | [what happens] | [who does it] |

## Who you will hear from

[the named people the client will hear from, for what, and when the first contact lands]

## What we need from you (one list, one ask)

[the consolidated list of every access, file, approval, and detail needed from the client]

**By [the ask deadline], please.** That is everything: we will not drip-feed requests at you.

## Your first result

By [the quick win date], you will have [the week-one quick win, from the engagement brief] in your hands.

## Reaching us

[the contact channels, from `memory/business-context.md`]. We reply within [the response standard, from `memory/business-context.md` or the flagged conservative default]. For anything urgent: [the urgent channel].

Include this section only when something is genuinely still unconfirmed; otherwise omit it.

## Still being confirmed

[the items still being confirmed] (we will come back to you by [the confirmation date])

---

## 11. What good looks like

**Good example (annotated).**

> **Hi Priya, welcome aboard.** Here is exactly what happens next. [1] This Thursday, Sam sets up your workspace and runs the content audit; next Tuesday at 10am we meet to walk you through what we found. [2] One thing from you: the access list below, all in one go, by Wednesday, and that is everything we will ask for this month. [3] By Friday you will have the audit summary in your inbox, so you will see movement in week one, not week six. [4] Reach us any time at the studio address; we reply within one business day.
>
> Timeline: dated and named. Ask: consolidated with a deadline. Quick win: the Friday audit summary.

1. Opens with what the client gets to know, not the provider's story: low self-orientation, per the Trust Equation.
2. Shows the actual work in progress with names and dates, per Buell's operational transparency.
3. One consolidated ask with a deadline and an explicit promise not to drip-feed: the client is not doing the project management.
4. A small, real, dated week-one result that counters the post-purchase dip, per Coleman.

Across the three audiences this holds: a **founder** sends this to her new retainer client; a **professional** adapts the same five parts to her company's onboarding template; in **real life**, a new tutoring family gets the term schedule, one list of what to send, and the first progress note by Friday.

**Bad example (named failure mode: the brochure that answers nothing).**

> "We're SO thrilled to have you!! Our award-winning team uses a synergistic approach to deliver game-changing results. We'll be in touch soon with next steps, and someone will reach out about access when we need it. Also, per your call with our sales team, we'll include the extra training sessions discussed!"

Failure mode: all self-orientation, no information. No dates, no names, no consolidated ask ("when we need it" guarantees a drip of requests), no quick win, banned filler language, and worst of all it states a section 4 open item (the "extra training sessions" that were discussed, not agreed) as committed scope. That last line creates the exact bound-by-your-own-words liability the Air Canada case warns about. The skill must refuse this and route to the honest pattern above: dated steps, named people, one ask, one real week-one result, open items held out or marked "to be confirmed".

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
