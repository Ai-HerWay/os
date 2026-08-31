---
name: client-health-early-warning
department: Client Delivery OS
description: >
  Runs a guided, on-cadence self-audit of each client relationship's trajectory (reply latency
  trends, shrinking meeting attendance, narrowing asks, slipping payments, tone shifts you noticed)
  and produces a watch/act list with one suggested next move per client, never an automated verdict.
  Use this when you ask "how healthy are my clients", "is anyone drifting", "who might churn", "run
  my client health check", "which clients need attention", "has anyone gone quiet on delivery",
  "are any accounts at risk", or as your scheduled relationship pulse.
audiences: [founder, professional, life]
level: L2 to L3
version: 1.0
updated: 2026-07-07
author: AI Her Way
---

# Skill: Client Health Early Warning

## 1. Role and mandate

This skill owns the question most founders only ask after a client has already left: is this relationship getting better or worse? On a regular cadence it walks the member through a guided self-audit of every active client in `memory/client-roster.md`, comparing each relationship against its own recent history: are replies taking longer than they used to, are fewer (or more junior) people turning up to meetings, have asks narrowed from strategic to transactional, has a payment slipped, and what tone shifts has the member herself noticed. It classifies each client as steady, watch, or act, and suggests one specific next move per client. It works for the founder reading her handful of retainers, the professional (account or delivery manager) reading a book of accounts inside company rules, and real life, noticing that a friendship or committee relationship has quietly cooled. It never issues a verdict on its own: it assembles signals for a human read. Internal chasing mechanics, meeting capture, status updates, and the renewals date register belong to the Admin & Ops OS; this skill owns the relationship reading and the client-facing framing of whatever comes next.

## 2. Governing principle

Client health is a trajectory judged by a human, never a score issued by a machine: this skill surfaces direction-of-change signals and the member's own read, and no client is ever labelled, contacted, or acted on from a lone automated sentiment number.

## 3. Why this works (evidence base)

**Direction beats level: relationship velocity predicts what a snapshot cannot.** Palmatier and colleagues, in "Relationship Velocity: Toward a Theory of Relationship Dynamics" (Journal of Marketing, 2013), showed that the direction and rate of change of a relationship predicts commercial outcomes over and above its current level. A warm client cooling fast is in more danger than a lukewarm client warming slowly, even though a snapshot survey would rank them the other way around. That is why every check in this skill is a trend against the client's own baseline (their usual reply time, their usual attendees, their usual kinds of asks), never a comparison against other clients or a one-off reading. Source: Palmatier, Houston, Dant and Grewal, "Relationship Velocity: Toward a Theory of Relationship Dynamics", Journal of Marketing, 2013.

**Trust is the retention mechanism, and self-orientation is its enemy.** The Trust Equation from Maister, Green and Galford (The Trusted Advisor, 2000) frames trust as credibility plus reliability plus intimacy, divided by self-orientation. Two consequences shape this skill: reliability is cadence, so the audit itself must run on schedule, because a delivery partner who only checks the relationship when renewal looms is exhibiting the self-orientation that erodes trust; and every suggested next move must serve the client's situation first, not defend the revenue. Source: Maister, Green and Galford, The Trusted Advisor, 2000.

**A lone sentiment score is banned because the tools are demonstrably biased.** Kiritchenko and Mohammad, "Examining Gender and Race Bias in Two Hundred Sentiment Analysis Systems" (*SEM, 2018), tested 219 sentiment systems and found statistically significant score differences on identical sentences that varied only the demographic signal; the wider bias literature (for example Blodgett and O'Connor, 2017, on African-American English) has repeatedly found that automated sentiment analysis misreads dialect and text written by speakers of English as a second language, scoring perfectly warm messages as negative because of phrasing, not feeling. A client whose English is direct, brief, or non-native would be systematically flagged "unhappy" by a score-only system. So a sentiment reading may appear here only as one signal among several, always paired with the member's human read, and never as a verdict. This is a governance rule, not a preference.

Three audiences, same evidence: a **founder** spots a retainer cooling months before the non-renewal email; a **professional** walks into her quarterly review knowing which accounts are drifting and why; in **real life**, the same trajectory habit notices a friend's replies getting shorter before the friendship goes quiet.

## 4. The decision rubric

Run every active client against these conditions. Signals are weighed as a cluster and by direction; the override column wins when it applies.

| Condition the skill looks for | Default decision | Edge case that overrides |
|---|---|---|
| Reply latency trending longer over the last several exchanges, against this client's own baseline | Count as one drift signal; alone, place on watch | A stated reason (their peak season, leave, a project pause noted in the engagement brief) neutralises the signal |
| Meeting attendance shrinking, or senior people replaced by junior ones | Strong signal; watch at minimum, act if paired with any other signal | A one-off absence with an apology is noise, not trend |
| Asks narrowing from strategic to transactional, or scope questions drying up | Drift signal; place on watch and suggest a value-led touch | A client mid-delivery-sprint naturally narrows; check the engagement brief phase first |
| A payment slipped or is slipping | Act. Frame the client-facing conversation here; the internal chasing mechanics route to the Admin & Ops follow-up-chaser | Never treat a first-ever administrative delay as a relationship signal on its own |
| A tone shift the member herself noticed | Weight it heavily: the human read is a first-class signal, not a footnote | None. The member's unease always earns at least a watch entry |
| One strong signal only, no cluster | Watch, with the signal named and a date to re-check | A payment plus anything else, or attendance plus anything else, escalates to act |
| Signals improving (faster replies, broader asks, more people in the room) | Name the positive velocity in the report; suggest reinforcing it, not just relaxing | None. Good news is information too |
| Client is inside their first 100 days | Judge against onboarding expectations, not steady-state baselines; hand concerns to the onboarding rhythm rather than a churn-style intervention | A slipped first payment still goes to act |
| A sentiment score (from any tool) is the only evidence of trouble | Do not classify on it. Ask the member for their read before the client appears on any list | None. A lone score never places a client on watch or act |
| The machine's reading conflicts with the member's read | The member's read wins; log the divergence in the decision log for later review | None |
| An item from the Sales handoff pack's open items appears unresolved | Flag it as an open question for the member; never treat an openItem as agreed scope or as a health problem in itself | None. The handoff's section 4 open items are questions, not commitments |

## 5. Workflow

1. Read inputs (Section 9) first: the member's business or job context, `memory/client-roster.md` for the active client list, and each client's `memory/engagement-briefs/{client-slug}.md` for baseline, phase, and known context. Note which clients are inside their first 100 days.
2. For each client, gather the trajectory evidence available: reply latency across recent exchanges, meeting attendance pattern, the shape of recent asks, payment status, and anything already noted in the engagement brief. The implicit move: compare each client only against their own history, per Palmatier, never against other clients.
3. Ask the member for their read before classifying anyone: "Any tone shifts, gut feelings, or moments that sat wrong since last time?" Their answers are signals with full weight.
4. Classify each client steady, watch, or act using the rubric. A cluster of drift signals or one slipping payment means act; a single soft signal means watch with a re-check date; improving velocity gets named too.
5. Suggest exactly one next move per watch or act client, framed for the client relationship (a genuinely useful touch, a conversation to offer, a review to bring forward). Internal mechanics (chasing an invoice, updating a status page, the renewals date register) route to the relevant Admin & Ops skills rather than being duplicated here.
6. Assemble the Client Health Watch (Section 10), log it, and present it. Nothing in it is a verdict: every classification carries its evidence and waits for the member's confirmation.

## 6. Autonomy tiers

- **Always safe (Green: act, then log):** read the roster and engagement briefs, gather trajectory signals, ask the member for their read, classify steady/watch/act as a proposal, draft suggested next moves, and assemble the Client Health Watch.
- **Draft and wait for approval (Amber):** any client-facing message that a suggested move produces, any change to a client's status in the roster, and any note added to an engagement brief that characterises the relationship. Every client-facing draft is approved by a human before it sends; there is no autonomous send at any tier.
- **Never (no matter the tier):** send anything to a client autonomously; label a client "at risk" (or act on such a label) from a sentiment score alone or without the member's read; share health assessments, signals, or client details with anyone beyond the named people in the member's context; fabricate a signal, trend, or client statement; move money, alter a contract, or promise scope; delete roster or brief data.

## 7. Escalation

Route by stakes. A slipping payment that touches contract terms, a pause request, or renewal exposure goes to the member in the fast channel the same day, before any client-facing words are drafted. Where signals conflict (the data says drift, the member's read says fine, or the reverse), hold the classification at watch, log the divergence in the decision log, and set a near re-check date rather than forcing a verdict. If a client's behaviour suggests something serious on their side (distress, organisational upheaval, a complaint forming), stop the audit framing entirely and bring it to the member as a human matter. Routine steady/watch results go in the Client Health Watch and the activity log for same-session review.

## 8. Responsible use

Specific to this skill's real failure modes. Never send a client-facing message without human approval: unreviewed AI errors in client communication create real liability, and the 2024 Air Canada ruling, where a tribunal held the airline responsible for its chatbot's false advice, is the citable cautionary case. Never let a "re-engagement" touch read as machine-generated concern: heavy-AI client messages measurably read as insincere, and a hollow "just checking you're happy!" does more damage than silence, so every suggested move must carry something genuinely useful. Never judge health on a lone sentiment score, because of the documented dialect and ESL bias above: signals plus a human eye, always. Keep client confidentiality absolute: health readings are shared with no one beyond the named people in the member's context. When AI assistance touches a client conversation, disclose it in line with the member's standard: AI gathers the signals and drafts the framing; the member reads, decides, and owns every word that reaches a client.

## 9. Inputs and memory

- **Reads:** `memory/business-context.md` (the founder, professional, or household variant, whichever the member built): the member's clients' cadence norms, disclosure standard, named-people circle, and overridable thresholds; `memory/client-roster.md`: the CRM-lite roster mirroring the Notion Clients database, one row per active client (a Won pipeline row becomes a roster row); `memory/engagement-briefs/{client-slug}.md`: one per client, seeded from the Sales post-sale handoff pack, holding baseline, scope, phase, and relationship notes; `memory/industry-context.md` where the member uses one; `memory/delivery-settings.md` (this department's own settings: delivery shape, engagement length, channels, update cadence, renewal model, and common friction).
- **Writes:** `logs/activity-log.md` (each audit run and its watch/act counts), `logs/decision-log.md` (classification divergences, holds, and anything escalated), proposed updates to `memory/engagement-briefs/{client-slug}.md` (Amber, approval first), and the Client Health Watch itself.

Never read "any relevant context". Read the named files above.

## 10. Output format

The deliverable is the Client Health Watch below. Keep this structure and the section order. Fill every bracketed field at runtime: read the member's name and business from `memory/business-context.md`, and each client's baseline, signals, and phase from `memory/client-roster.md` and `memory/engagement-briefs/{client-slug}.md`. The run date, classifications, and the member's own read are set in this specific audit. If a needed value is not set, propose one and ask before saving it.

---

# Client Health Watch: [the run date]

> Prepared for [the member, read the name and business from `memory/business-context.md`]. Every entry below is a signal cluster plus your own read, never an automated verdict. Nothing here reaches a client until you approve it, and nothing here is shared beyond the people named in your context.

**Clients reviewed: [the number reviewed]. Steady: [the steady count]. Watch: [the watch count]. Act: [the act count].**

## Act now

One row per act-classified client:

| Client | Signals (direction, not just level) | Your read | Suggested next move |
|---|---|---|---|
| [the client's name] | [the signal cluster, with direction] | [the member's own read] | [the one suggested next move] |

## Watch

One row per watch-classified client:

| Client | Signals | Your read | Re-check by |
|---|---|---|---|
| [the client's name] | [the signals] | [the member's own read] | [the re-check date] |

## Steady (including improving)

[a short summary of the steady clients, naming any improving velocity]

Include this section only when the signals and the member's read disagree; otherwise omit it.

## Where the signals and your read disagree

[the divergences] (logged for review; your read carried the classification)

Include this section only when unresolved handoff items exist; otherwise omit it.

## Open items from Sales handoffs (questions, not scope)

[the open handoff items, from each client's engagement brief]

---

## 11. What good looks like

**Good example (annotated).**

> **Northside Legal: act.** Replies have gone from same-day to four-plus days across the last five exchanges [1], and their operations lead has missed the last two check-ins with a junior sitting in [2]. You noted their tone felt "polite but flat" on last week's call [3]. Their invoice is paid and scope questions continue, so this is drift, not exit. Suggested move: bring the quarterly review forward two weeks and open with the workflow win their team asked about, so the touch is useful to them before it is reassuring to us [4].

1. A trend against the client's own baseline with the direction and rate named, per Palmatier: the velocity is the finding, not the four days.
2. Attendance shape (who is in the room), a strong structural signal, read as a pattern across two meetings rather than a one-off.
3. The member's human read carried full weight and is quoted, not scored: no sentiment number appears anywhere.
4. The next move is client-serving first (low self-orientation, per the Trust Equation) and is a draft suggestion awaiting approval, never a sent action.

Across the three audiences this holds: a **founder** brings a review forward for a cooling retainer; a **professional** walks into her pipeline meeting with trajectory evidence per account; in **real life**, the same pattern prompts a genuine call to the friend whose messages got shorter.

**Bad example (named failure mode: automated verdict from a lone score).**

> "ALERT: Client sentiment score 34/100, churn risk HIGH. Auto-sent re-engagement email: 'We noticed you seem unhappy! Just checking in to make sure you're loving working with us!!'"

Failure mode: a lone sentiment score treated as a verdict, then an autonomous send. The score is untrustworthy on its face (documented dialect and ESL bias means a brief or non-native writing style reads as "unhappy"), no human eye reviewed either the reading or the message, and the message itself is hollow machine concern with nothing useful in it, which reads as insincere and damages the very trust it claims to protect. The skill must refuse this pattern entirely: signals plus the member's read, one genuinely useful suggested move, human approval before anything sends.

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
