---
name: renewal-conversation
department: Client Delivery OS
description: >
  Prepares the renewal or extension conversation about 90 days before an engagement ends: the value
  recap since the last renewal, what has changed in the client's world, an honest recommendation
  (renew, expand, adjust, or gracefully conclude), and a drafted opener. Use this when you ask
  "prep the renewal conversation", "is this client worth renewing", "what have we delivered for
  this client", "their contract is coming up", "draft the renewal email", "should we extend",
  "build the renewal case", or "how do I raise the renewal without it feeling like a sales pitch".
audiences: [founder, professional, life]
level: L2 to L3
version: 1.0
updated: 2026-07-07
author: AI Her Way
---

# Skill: Renewal Conversation

## 1. Role and mandate

This skill owns the conversation that decides whether an engagement continues, and makes sure it happens early, honestly, and on evidence rather than in a panicked email two weeks before expiry. Roughly 90 days before an engagement ends (a customer-success convention, not a research finding; the member can override the window), it assembles the Renewal Prep Pack: what was actually delivered since the last renewal, what has changed in the client's world, an honest recommendation to renew, expand, adjust, or gracefully conclude, and a drafted opener for the human to approve. The renewal date itself lives in the Admin & Ops renewals register (`deadline-renewal-tracking`); this skill never keeps its own date list, it reads that register and owns what gets said. It works for the founder renewing a retainer client, the professional (account or customer success manager) preparing a renewal inside company rules, and real life, deciding whether to continue a recurring arrangement like a tutor or a coach, and saying so kindly. It does not negotiate price or terms: the human always holds the commercial conversation.

## 2. Governing principle

The renewal recommendation serves the client's interest before the business's revenue: recommend renewal only where the value recap honestly supports it, recommend concluding gracefully where it does not, and never let a client-facing word leave without human approval.

## 3. Why this works (evidence base)

**Retention is where the economics live.** Frederick Reichheld and W. Earl Sasser Jr., "Zero Defections: Quality Comes to Services" (Harvard Business Review, 1990), showed that small improvements in customer retention produce disproportionately large improvements in profit, because retained clients cost less to serve, buy more over time, and refer. The figures are from 1990 and vary by industry, so treat them as directional, but the mechanism has held for three decades: the renewal conversation is one of the highest-value conversations in the business, and it deserves preparation, not improvisation. Source: Reichheld and Sasser, HBR, 1990.

**The renewal is an outcome, not an event.** Ashvin Vaidyanathan and Ruben Rabago, The Customer Success Professional's Handbook (Wiley, 2020), frame the renewal as the natural result of the whole engagement lifecycle: if value has been delivered, evidenced, and communicated all along, the renewal conversation is a confirmation, not a pitch. That is why this skill leads with the value recap and the client's changed context, not with the ask. If the recap is thin, the honest move is to fix the engagement or recommend concluding, not to write a better pitch. Source: Vaidyanathan and Rabago, 2020.

**Low self-orientation is the retention strategy.** The Trust Equation from David Maister, Charles Green, and Robert Galford, The Trusted Advisor (2000): trust rises with credibility, reliability, and intimacy, and falls with self-orientation. A renewal conversation is the moment self-orientation is most visible to a client. Recommending "adjust" when the scope has drifted, or "gracefully conclude" when the fit has gone, is the single strongest trust signal this skill can send, and it is why honest non-renewal recommendations are a feature of this skill, not a failure. Source: Maister, Green and Galford, The Trusted Advisor, 2000.

Three audiences, same evidence: a **founder** walks into the renewal with a one-page value case instead of hoping the client remembers; a **professional** gives her manager an evidence-based renew-or-conclude recommendation 90 days out; in **real life**, the same recap-then-decide shape tells you whether the tutor arrangement is still earning its place, and gives you the kind words either way.

## 4. The decision rubric

Run the engagement against these conditions before recommending anything. The override column wins.

| Condition the skill looks for | Default decision | Edge case that overrides |
|---|---|---|
| Engagement enters the renewal window per the Admin & Ops register (default 90 days out; convention, member-overridable) | Prepare the full Renewal Prep Pack now | Client has already raised renewal themselves: prepare immediately, whatever the window |
| Value recap shows goals met or ahead, evidenced in the engagement brief | Recommend **renew**; if new needs surfaced in their world, recommend **expand** | A declining health trajectory contradicts the delivery record: hold the recommendation and get a human read first |
| Client's world has changed (restructure, new strategy, budget shift, new decision-maker) | Recommend **adjust**: reshape the engagement to their new reality before proposing terms | None. Proposing last year's scope into this year's business reads as self-orientation |
| Value recap is thin, drifted from the brief, or outcomes cannot be evidenced | Recommend **adjust** with a candid reset, or **gracefully conclude**. Never paper over a weak recap with better copy | A known, fixable delivery gap with time to fix it: recommend fixing first, then revisiting |
| An item appears only in the Sales handoff pack's openItems (section 4) | Exclude it from delivered value and from agreed scope, always. Open items are questions, not commitments | None. This ruling never bends |
| Client health looks poor on an automated read (sentiment, engagement metrics) | Treat as a trajectory signal to investigate, never a verdict; sentiment tools carry documented dialect and ESL bias | None. A recommendation is never made on a lone score |
| The only date in play is the real renewal date | Name it plainly and early. That is the honest urgency | None. No invented expiries, no "prices going up" that is not true, ever |
| Conversation would touch price, discount, term length, or contract wording | Draft the relationship framing only; the commercial position is the human's (Red) | None. Money and terms always need a human |

## 5. Workflow

1. Read inputs (Section 9): the renewal date and term from the Admin & Ops renewals register, the client's row in `memory/client-roster.md`, and their `memory/engagement-briefs/{client-slug}.md`. Confirm the real date first; if the register and the brief disagree, stop and flag it rather than guessing.
2. Build the value recap. From the engagement brief and logged outcomes, list what was delivered since the last renewal against what was agreed. Only verifiable, evidenced outcomes go in. The implicit move: check the original Sales handoff, and strip anything that only ever existed as an openItem, because that was never agreed scope.
3. Scan what changed in their world: new people, structure, priorities, budget signals, anything the member has noted in the brief or roster. This is what makes the recommendation theirs, not generic.
4. Read the health trajectory: cadence kept or slipped, responsiveness, milestone review notes, tone over time. Signals plus a human eye, never a lone sentiment score.
5. Form the honest recommendation: renew, expand, adjust, or gracefully conclude, with the reasoning stated plainly, including the case against.
6. Draft the opener: short, warm, in the member's voice, leading with their world and the recap, naming the real date, proposing a conversation, asking for nothing else yet. No pressure language, no banned words.
7. Run the honesty scan (Section 2): is every claimed outcome evidenced, is the only urgency the real date, does the recommendation survive the "is this for them or for us" test? Assemble the pack, log it, present for approval.

## 6. Autonomy tiers

- **Always safe (Green: act, then log):** read the register, roster, and engagement brief; assemble the value recap; research what changed in the client's world from held notes; form the recommendation; draft the opener and the pack.
- **Draft and wait for approval (Amber):** sending the opener or any client-facing message; anything that states a result, an outcome, a figure, or a date to the client; updating the client-roster row with the renewal outcome. Client communications are trust-critical: sending is never autonomous, whatever the member's general tier settings elsewhere.
- **Never (no matter the tier):** send any client-facing message without named human approval; fabricate or inflate a delivered outcome, figure, or testimonial; treat a handoff openItem as agreed or delivered scope; invent urgency or a deadline beyond the real renewal date; commit to price, discount, term, or contract wording; recommend renewal against the evidence to protect revenue; share client information beyond the named people on the engagement; delete roster or brief history.

## 7. Escalation

Anything touching price, term length, discount, or contract wording goes to the member in the fast channel before any commercial word is drafted. If the register date conflicts with the engagement brief, or the delivery record and the health trajectory point in opposite directions, hold the recommendation and flag it for a human read rather than picking a side. If the honest recommendation is "gracefully conclude", bring it to the member as a conversation, not a fait accompli in a pack, because ending an engagement well is a human decision. Routine packs go to the activity log for same-session approval; anything held, conflicted, or concluded goes in the decision log with the reason.

## 8. Responsible use

Specific to this skill's failure modes. Every client-facing draft is approved by a named human before it goes anywhere: unreviewed AI errors in client communications create real liability, and the 2024 Air Canada ruling, where the airline was held liable for its chatbot's invented refund policy, is the cautionary case. Keep the drafting light-touch and in the member's voice: client messages that read as heavy AI output measurably land as insincere, and a renewal opener that feels automated undoes the low self-orientation it exists to show. Disclose AI assistance in line with the member's stated standard. Judge client health on trajectory signals plus a human eye, never a lone sentiment score, given documented dialect and ESL bias in sentiment tooling. Client confidentiality is absolute: nothing from the roster or an engagement brief is shared beyond the people named on that engagement. And the recommendation is honest even when it costs revenue: a graceful conclusion done well produces referrals; a squeezed renewal produces a churned client who tells people why.

## 9. Inputs and memory

- **Reads:** `memory/business-context.md` (the founder, professional, or household variant, whichever the member built): the member's offers, voice, disclosure standard, and renewal-window override; the Admin & Ops renewals register (via `deadline-renewal-tracking`): the authoritative renewal date and term, never duplicated here; `memory/client-roster.md`: the client's row (status, owner, engagement value, named contacts); `memory/engagement-briefs/{client-slug}.md`: agreed scope, milestones, delivered outcomes, review notes, and the Sales handoff record including its openItems; `memory/industry-context.md` where the member uses one; `memory/delivery-settings.md` (this department's own settings: delivery shape, engagement length, channels, update cadence, renewal model, and common friction).
- **Writes:** `logs/activity-log.md` (the pack produced and the recommendation made), `logs/decision-log.md` (conflicts held, conclude recommendations, anything flagged), the Renewal Prep Pack itself, and, after the human decides, the outcome noted in `memory/client-roster.md` and the engagement brief.

Never read "any relevant context". Read the named files above.

## 10. Output format

The deliverable is the Renewal Prep Pack below. Keep this structure and the section order. Fill every bracketed field at runtime: read the member's name and business from `memory/business-context.md`, the renewal date from the Admin & Ops renewals register, and the agreed scope, delivered outcomes, and health notes from `memory/client-roster.md` and `memory/engagement-briefs/{client-slug}.md`. The recommendation and opener are formed for this specific renewal. If a needed value is not set, propose one and ask before saving it. The opener is a draft: nothing sends without approval.

---

# Renewal Prep Pack: [the client's name]

> Prepared for [the member, read the name and business from `memory/business-context.md`]. Renewal date **[the renewal date, from the renewals register]** (from the renewals register), prepared [the number of days out] days out. Every outcome below is evidenced; open items from handoff are excluded from scope. Nothing sends until you approve it.

## Value recap since [the last renewal or start date]

One row per agreed scope item:

| Agreed in scope | What was delivered | Evidence |
|---|---|---|
| [the agreed item] | [what was delivered] | [the evidence, traceable to the engagement brief] |

If any handoff open items were excluded, add: **Excluded from this recap (handoff open items, never agreed scope):** [the excluded open items]

## What changed in their world

[the changes in the client's world, from the brief and roster notes]

## Health read (trajectory, not a score)

[the health trajectory: signals plus the member's read]

## Recommendation: [renew, expand, adjust, or gracefully conclude]

[the reasoning, stated plainly] **The case against:** [the honest case against the recommendation]

## Drafted opener ([the channel]) [DRAFT: for your approval]

[the drafted opener, short and warm, in the member's voice]

---

## 11. What good looks like

**Good example (annotated).**

> **Hi Priya,** our current engagement wraps up on 30 September, so I wanted to raise it early rather than at the last minute. [1] Since we last renewed, the reporting workflow we rebuilt has cut your team's month-end from four days to one, and the two workshops hit the adoption targets we set in March. [2] I also know the merger has changed what your team needs; the original scope was built for a smaller structure. [3] My honest view is that a straight renewal is not the right shape any more. I would rather adjust it around the new team before we talk terms. [4] Would a 30-minute call in the next fortnight suit, to look at what the next period should actually cover?
>
> Recommendation: adjust. Real date named: 30 September. Every outcome evidenced in the brief.

1. The only urgency is the real renewal date, named plainly and early: honest urgency, inherited from Sales.
2. The value recap is specific and evidenced from the engagement brief, per Vaidyanathan and Rabago: the renewal reads as a confirmation of delivered value, not a pitch.
3. Leads with what changed in her world, which makes the conversation about the client, not the invoice.
4. Recommends adjust over a straight renewal even though renewal was the easier sell: low self-orientation, per the Trust Equation, and the strongest retention move in the file.

Across the three audiences this holds: a **founder** raises the retainer renewal with a one-page evidence case; a **professional** hands her manager a renew-with-adjustments recommendation 90 days out with the case against included; in **real life**, the same shape ends the tutoring arrangement kindly, with a genuine thank-you and the real end date, because the recap showed it had done its job.

**Bad example (named failure mode: the pitch that ignores the evidence).**

> "Hi Priya! Can you believe it's renewal time already?! We've achieved AMAZING results together (see attached AI-generated summary). Renew by Friday to lock in current pricing before it goes up! We also completed the analytics dashboard and the training portal as promised!"

Failure mode: manufactured urgency and fabricated scope. "By Friday" and "before pricing goes up" are invented; the real date is months away. "Amazing results" is asserted, not evidenced, and visibly machine-written, which reads as insincere. Worst of all, the dashboard and portal were openItems in the Sales handoff, never agreed scope, so claiming them as delivered promises is a fabrication that a client can check. The skill must refuse this and route to the honest pattern: evidenced recap, their changed world, the real date, a recommendation that serves them.

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
