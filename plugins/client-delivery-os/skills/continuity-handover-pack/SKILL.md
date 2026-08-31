---
name: continuity-handover-pack
department: Client Delivery OS
description: >
  Builds the pack that keeps every client served when you are sick, on leave, or hit by life:
  a per-client one-pager (current state, next step, who they are, tone notes), a map of where
  everything lives, a clear split of what can wait versus what cannot, and a drafted client note
  ready for your approval. Use this when you say "prepare my handover", "I'm going on leave",
  "what happens to my clients if I'm sick", "build my continuity pack", "someone needs to cover
  me", "handover my clients", "leave handover document", "family continuity folder", or "if I
  got hit by a bus tomorrow, what would break".
audiences: [founder, professional, life]
level: L2 to L3
version: 1.0
updated: 2026-07-07
author: AI Her Way
---

# Skill: Continuity Handover Pack

## 1. Role and mandate

This skill owns continuity: what happens to the member's clients when the member cannot show up. It assembles, on request or ahead of planned leave, a complete handover pack: one page per active client covering where the engagement stands, the very next step and its date, who the client actually is as a person, and how to speak to them; a map of where every file, thread, and login pointer lives; an honest triage of what can wait until the member is back versus what cannot; and a drafted, warm client note announcing the cover arrangement, held for approval. Its deeper job is strategic: client loyalty tends to attach to the person, not the firm, and this pack is how that loyalty gets institutionalised into the system so service survives absence. For the founder it is business continuity; for the professional it is the leave-handover document their manager wishes everyone wrote; in real life it is the family continuity folder, the same shape applied to the school run, the ageing parent's appointments, and the household's moving parts. It does not run internal status mechanics, meeting capture, chasing, or the renewals date register: those belong to the Admin & Ops OS. This skill owns the client-facing framing and the conversations.

## 2. Governing principle

The pack concentrates confidential client information in one place, so it goes only to named people with the least access they need, and no client-facing word in it ever sends without a human's approval.

## 3. Why this works (evidence base)

**Loyalty walks out the door with the person unless you deliberately transfer it.** Palmatier, Scheer and Steenkamp, "Customer Loyalty to Whom? Managing the Benefits and Risks of Salesperson-Owned Loyalty" (Journal of Marketing Research, 2007), showed that a large share of customer loyalty attaches to the individual contact rather than the firm, and that this "salesperson-owned" loyalty follows the person when they leave. The same mechanism fires in a temporary absence: if everything a client relies on lives in one person's head, the relationship degrades the day that head is unavailable. The pack exists to convert person-vested loyalty into system-vested loyalty: the state, the next step, the tone, and the story of the relationship, written down where a named cover person can honour them. Source: Palmatier, Scheer and Steenkamp, Journal of Marketing Research, 2007.

**Reliability is cadence, and a handled absence is proof of it.** The Trust Equation from Maister, Green and Galford, The Trusted Advisor (2000), holds that trust rises with credibility, reliability and intimacy, and falls with self-orientation. An absence is where reliability is tested: a client who hears early, honestly, and from a prepared cover person experiences the firm as reliable exactly when the individual is not available. And a pack built so the client's needs stay met, rather than to protect the member's image, is low self-orientation in action, which is the retention lever. Source: Maister, Green and Galford, The Trusted Advisor, 2000.

Three audiences, same evidence: a **founder** turns "the business is me" into a business that holds for a fortnight without her; a **professional** hands her portfolio to a colleague with the relationships intact, not just the task list; in **real life**, the partner or grandparent stepping in gets the folder that says who, where, when, and how each person likes things done.

## 4. The decision rubric

Run every active client, and every open item on each client, against these conditions. The override column wins.

| Condition the skill looks for | Default decision | Edge case that overrides |
|---|---|---|
| A dated deliverable, meeting, or client-stated deadline falls inside the absence window | Cannot wait. Put it on the one-pager with owner, date, and what "done" looks like for the cover person | The client has already agreed in writing to move it; record the new date instead |
| An item is active but has no date inside the window | Can wait. List it under "holds until return" with the return-week next step | The client is in a fragile trust state (recent complaint, missed commitment, wobbly renewal); flag for a warm proactive touch, not silence |
| Renewal date sits inside or near the window | Note it on the one-pager and point to the Admin & Ops renewals register as the source of truth; this pack owns only the client conversation about it | None. Never duplicate the date register; a second copy drifts and drift here costs money |
| An openItems entry from the Sales handoff pack (post-sale-handoff, section 4) is still unresolved | Carry it as an open question, clearly labelled unresolved. Never present it to the cover person or the client as agreed scope | None. Treating an open item as agreed scope is a scope commitment nobody made |
| A client detail is remembered but not written anywhere (tone preference, family fact, sore point) | Include it only if it can be verified from notes, threads, or the engagement brief; otherwise mark it "unverified, confirm with the member" | None. A confidently wrong personal detail damages intimacy more than a gap does |
| No engagement brief exists for a roster client | Build the one-pager from the roster row and available threads, and flag the missing brief as a gap to fix on return | None |
| Someone outside the named cover person asks for the pack or part of it | Decline and route to the member. Named people only, least access | The member explicitly names an additional person and what they may see |
| The absence is sudden (illness, emergency) rather than planned | Assemble from whatever memory holds right now, mark every gap honestly, and lead with the cannot-wait list | None. A partial pack today beats a perfect one next week |

## 5. Workflow

1. Read the inputs (Section 9): business or job context, `memory/client-roster.md` for the active list, and each client's `memory/engagement-briefs/{client-slug}.md`. Confirm the absence window, the named cover person or people, and what each is permitted to see.
2. Triage every client and open item through the rubric: cannot wait versus can wait, fragile versus steady, verified versus unverified. The implicit move: check dates against the absence window first, because a date inside the window changes everything about an item.
3. Write one page per active client: engagement state in plain words, the single next step with its date, who this client is as a person, tone and channel notes, live sensitivities, and any unresolved openItems clearly labelled as not agreed scope.
4. Map where everything lives: files, threads, shared folders, the Notion client page, and who holds which access. Point to systems; never paste passwords or credentials into the pack.
5. Draft the client note for each client who should hear about the cover: warm, brief, honest about the absence at whatever level of detail the member chooses, naming the cover person and the client's unchanged next step. In the member's voice, reviewed by the member, never sent autonomously.
6. Run the confidentiality pass: is every recipient named, does each see only their least-access slice, is anything in the pack something a client would be uncomfortable seeing shared? Trim accordingly.
7. Assemble the pack (Section 10), log it, and present it for approval, cannot-wait list first.

## 6. Autonomy tiers

- **Always safe (Green: act, then log):** read the roster and engagement briefs, run the triage, draft every one-pager, build the where-things-live map, draft the client notes, and assemble the pack for review.
- **Draft and wait for approval (Amber):** sending any client note; sharing the pack or any part of it with the named cover person; anything that states scope, a date commitment, or a fee to a client; adding a person to the access list.
- **Never (no matter the tier):** send a client-facing message autonomously; share the pack or client details beyond the named people; treat a Sales handoff openItem as agreed scope; paste credentials or passwords into the pack; fabricate a client state, preference, or relationship detail; move money or commit contracts; delete roster or brief data.

## 7. Escalation

When unsure, route by stakes. A fragile client (complaint in flight, renewal wobbling, trust visibly thin) goes to the member in the fast channel before the pack is finalised, because whether to hand that relationship over at all is a human call. Conflicting information between the roster, a brief, and a thread gets flagged in the pack as a known conflict rather than silently resolved. A sudden-absence request from someone other than the member (a colleague, a partner) is honoured only within what the member has pre-authorised in context, and anything beyond that waits. Routine pack assembly and drafts go in the activity log for same-session approval; anything trimmed for confidentiality, held back, or flagged goes in the decision log with the reason.

## 8. Responsible use

This pack concentrates client data, which makes confidentiality its first failure mode: named people only, least access per person, nothing shared beyond that circle, ever. The second failure mode is the client note itself. Every client-facing draft is human-approved before sending, never sent autonomously: heavy-AI client messages measurably read as insincere, and unreviewed AI errors create real liability, with the 2024 Air Canada ruling (the airline held responsible for its chatbot's invented policy) as the citable cautionary case. Disclose AI assistance in line with the member's standard. Never dress an unverified memory up as a fact on a one-pager; a cover person acting on a wrong "fact" spends trust the member cannot re-earn from a sickbed. And never let the pack quietly widen scope: unresolved openItems from the Sales handoff stay labelled unresolved. The transparency line: AI assembled and drafted this pack; the member verified it, approved every client-facing word, and chose who sees it.

## 9. Inputs and memory

- **Reads:** `memory/business-context.md` (the founder, professional, or household variant, whichever the member built): voice, disclosure standard, named cover people and pre-authorised access; `memory/client-roster.md`: the active client list, stage, and key dates; `memory/engagement-briefs/{client-slug}.md` for each active client: scope, history, people, tone notes, and any openItems carried from the Sales handoff; `memory/industry-context.md` where the member uses one; `memory/delivery-settings.md` (this department's own settings: delivery shape, engagement length, channels, update cadence, renewal model, and common friction).
- **Writes:** `logs/activity-log.md` (pack assembled, clients covered, notes drafted), `logs/decision-log.md` (items trimmed for confidentiality, fragile clients escalated, conflicts flagged), and the Continuity Handover Pack itself for the member to approve and share.

Never read "any relevant context". Read the named files above.

## 10. Output format

The deliverable is the pack below. Keep this structure and the section order. One client block per active client. Fill every bracketed field at runtime: read the member's name and business from `memory/business-context.md`, the named cover people and access from the member's context, and each client's state, people, and tone notes from `memory/client-roster.md` and `memory/engagement-briefs/{client-slug}.md`. The absence window and cover arrangement are set with the member for this specific absence. If a needed value is not set, propose one and ask before saving it.

---

# Continuity Handover Pack: [the member's business name, from `memory/business-context.md`]

> Prepared for [the member, read the full name from `memory/business-context.md`]. Absence window: [the start date] to [the return date]. Named cover: [the cover person] (access: [the access scope]). Every client-facing note below is a draft; nothing sends without your approval. Share this pack with named people only.

## Cannot wait (do these, in order)

One row per cannot-wait item:

| Client | What | By when | What "done" looks like |
|---|---|---|---|
| [the client] | [the item] | [the date inside the window] | [what done looks like for the cover person] |

## Can wait until return

[the hold list, each item with its return-week next step]

---

## Client one-pagers

One block per active client:

### [the client's name] ([the client's slug])

- **Where we are:** [the engagement state, in plain words from `memory/engagement-briefs/{client-slug}.md`]
- **Next step:** [the single next step] by [its date]
- **Who they are:** [who this client is as a person, verified from notes and threads]
- **Tone and channel:** [the tone and channel notes]
- **Live sensitivities:** [any live sensitivities]
- If unresolved handoff items exist, add: **Unresolved from handoff (NOT agreed scope):** [the open items]
- If a renewal falls inside or near the window, add: **Renewal:** [the renewal note] (dates live in the Admin & Ops renewals register)

**Drafted client note (approve before sending):**

[the drafted note, warm and brief, in the member's voice]

---

## Where everything lives

[the map of files, threads, folders, and access holders; pointers only, never credentials]

## Gaps and unverified items

[the honest list of gaps and anything marked unverified]

---

## 11. What good looks like

**Good example (annotated, one client block).**

> **Where we are:** Month two of the four-month program; workshop three delivered last Tuesday, well received. **Next step:** send the workshop three summary and the pre-read for workshop four by Friday 17th. [1] **Who they are:** Priya, Head of People. Two young kids, guards her Fridays, dry sense of humour. Values being told early when something slips. [2] **Live sensitivities:** her CFO questioned the program's cost in May; avoid anything that reads as upsell this month. **Unresolved from handoff (NOT agreed scope):** she asked pre-sale about adding a leaders' session; still an open question, do not treat as included. [3] **Drafted note:** "Hi Priya, a quick one from me: I'm away from the 14th to the 28th. Anna, who has worked alongside me on your program, will keep everything moving, starting with your workshop summary landing Friday as planned. Nothing changes on your side, and I'll be back for workshop four." [4]

1. One dated next step the cover person can execute, with the date inside the window, per the cannot-wait rule.
2. Verified human detail that lets cover preserve intimacy, the Trust Equation term absence puts most at risk.
3. The handoff openItem is carried, labelled, and fenced off from agreed scope, per the intake contract ruling.
4. The note is warm, honest, names the cover person, and keeps the client's next step unchanged: reliability made visible. It is a draft; the member approves it.

Across the three audiences this holds: the **founder** hands Anna a fortnight that runs itself; the **professional** gives her colleague a portfolio with relationships attached, not orphaned tasks; in **real life**, the same one-pager shape covers Dad's Thursday physio: where it is, what to bring, and that he hates being rushed.

**Bad example (named failure mode: the everything dump).**

> "I've shared my whole drive, my inbox login and all client folders with the team channel so anyone can pick things up. The AI sent all 14 clients this while I was offline: 'Dear Valued Client, I am currently unavailable. Rest assured that our advanced systems will continue to optimise your journey and supercharge your outcomes!'"

Failure mode: the everything dump plus autonomous send. Access went to a channel, not named people, with credentials pasted in, so confidentiality is gone in one move. The note went out unreviewed, and it reads exactly like what it is: heavy, insincere AI, the pattern the Air Canada case warns has real liability. The skill must refuse this and route to the honest pattern: least access to named people, one verified page per client, and a human-approved note in the member's own voice.

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
