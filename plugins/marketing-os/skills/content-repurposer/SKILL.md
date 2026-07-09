---
name: content-repurposer
department: Marketing OS
description: >
  Atomises one non-written anchor piece (a video, podcast episode, webinar, keynote, workshop
  recording, or any audio or video source) into a multi-platform content pack: a timestamped clips
  list, quote card briefs, carousel briefs, captions, and an email snippet, then hands production
  to the studio skills. Triggers: "repurpose this video", "turn my podcast into content",
  "clips from my webinar", "atomise this recording", "content from my keynote", "what can I make
  from this talk", "chop up this workshop", "pull clips from this episode". Written sources
  (a newsletter, email, or blog post) belong to the newsletter-to-social skill, not this one.
audiences: [founder, professional, life]
level: L2 to L4
version: 1.0
updated: 2026-07-07
author: AI Her Way
---

# Skill: Content Repurposer (non-written anchor to multi-platform pack)

## 1. Role and mandate

This skill takes one non-written anchor piece for your business (a video, podcast or audio episode, webinar, keynote, or workshop recording) and atomises it into a structured, multi-platform content pack: a clips list with timestamps, quote card briefs, carousel briefs, platform captions, and an email snippet. It owns the mining and mapping end to end, then hands production to the studio skills (design briefs to the brand-graphics path, video work to the reel path, scheduling to the approval-and-queue path). It does not own written sources: a newsletter, email, or blog post going to social belongs to the newsletter-to-social skill, and this skill routes it there without drafting a word. It works the same for a founder atomising a podcast interview, a professional atomising a recorded team webinar or conference talk, and someone in real life atomising a community workshop or school presentation recording.

## 2. Governing principle

Never let an extracted piece change the speaker's meaning. Every clip, quote, and caption must be faithful to what was actually said in context; a stronger hook is never worth a distorted one, and nothing in the pack goes live without the member's sign-off.

## 3. Why this works (evidence base)

Three named practitioner frameworks (documented bodies of working practice, not academic studies, and we present them as such) underpin this skill.

**Pillar content atomisation.** Gary Vaynerchuk's GaryVee Content Model (published as a deck in 2019) documents the practice his team runs at scale: create one substantial pillar piece (a keynote, a podcast, a long video), then systematically atomise it into dozens of platform-native micro pieces (clips, quote graphics, stills, captions), each adapted to the platform it lands on rather than cross-posted identically. The model's core claim is directional but well evidenced by the practice itself: the pillar piece carries the thinking, and the micro content carries the reach. This is the named basis for the anchor-first workflow below. Source: Gary Vaynerchuk, "The GaryVee Content Model", 2019.

**Repurpose by design, not as an afterthought.** Amy Woods' "Content 10x" (2019) sets out a repeatable method for turning one piece of content into ten or more, arguing that repurposing should be planned when the anchor is made, that each derivative must be genuinely reworked for its format (a clip is not a carousel is not an email), and that the original's integrity must survive the cut. Her format-mapping discipline is the named basis for the rubric in Section 4. Source: Amy Woods, "Content 10x: More Content, Less Time, Maximum Results", 2019.

**Distribution outlives creation.** Ross Simmonds' "Create Once, Distribute Forever" (2024) documents the practitioner case that most content fails on distribution, not quality, and that a deliberate, repeated distribution system for existing assets outperforms a constant-creation treadmill. This is why the pack below is built for the member's active platforms and a staggered rollout, not a single-day dump. Source: Ross Simmonds, "Create Once, Distribute Forever", 2024.

Three audiences, same evidence: a **founder** atomises a podcast episode into a fortnight of content, a **professional** atomises a recorded webinar into internal and LinkedIn presence, and in **real life** the same method turns a recorded community workshop into clips and a recap email for the group.

## 4. The decision rubric

This is the psychology layer. Run every source and every extracted element through these conditions. The override column wins when it applies.

| Condition the skill looks for | Default decision | Edge case that overrides |
|---|---|---|
| The source is written (newsletter, email, blog post) | Route to the newsletter-to-social skill. This skill does not touch written sources | None. Ownership is by source type, not destination platform |
| No transcript exists for the source | Stop and get or produce one first (member's transcription tool, or transcribe in-session). Never atomise from memory of a recording | A source under 3 minutes the member has verified line by line |
| A candidate clip reads differently out of context than in context | Reject the clip, whatever its hook strength. Integrity rule | Widen the clip boundaries until the meaning survives on its own; if it cannot, it stays rejected |
| A strong moment involves a guest, client, or audience member | Draft and hold; do not include without the member confirming consent | The person is the member themselves |
| Deciding which platforms the pack targets | Read the member's active platforms from `memory/business-context.md`. Never all platforms by default | The member explicitly asks to trial a new platform this pack |
| A moment fits more than one format (clip and quote card and carousel) | Pick the format whose revenue function matches the member's current priority in `business-context.md` | A genuinely landmark moment can carry two formats if reworked, not duplicated |
| A statistic or claim in the recording cannot be traced or verified | Quote it as the speaker's spoken claim with a flag for the member, or cut it. Never launder it into a stated fact | The figure is verified in the member's context files |
| The member asks for "AI-generated reels" from the source | Reframe honestly: offer AI b-roll plus a reel blueprint (Section 10). Never promise a fully generated reel | None. This positioning rule never bends |
| The pack is ready | Queue everything as drafts behind approval. Nothing schedules live | None. Approval before live is Content Studio law |

## 5. Workflow

1. Read inputs (Section 9) first: business context, brand kit, the source recording and its transcript. Confirm the source is non-written; if it is written, route to newsletter-to-social now and log the routing.
2. Secure the transcript. No transcript, no atomisation. Timestamped transcripts are best; produce timestamps if missing.
3. Mine the anchor: the big idea, 3 to 5 supporting points, stories, quotable lines with their timestamps, teachable frameworks, and the honest revenue angle of each. The implicit move: re-read each candidate in its surrounding context before extracting it, so the integrity rule is applied at the source.
4. Map every element through the rubric to a platform (member's active platforms only) and a format: clip, quote card, carousel, caption, or email snippet.
5. Build the pack in the Section 10 format: timestamped clips list, quote card briefs, carousel briefs, captions per platform, one email snippet, and a suggested staggered rollout.
6. Hand production off: design briefs go to the brand-graphics path ({{designTool}} or Claude-rendered HTML/SVG from `memory/brand-kit.md`); any reel work goes out as AI b-roll plus a reel blueprint, never a promised finished reel.
7. Queue, do not publish. Everything lands in the OS as a held package. Only after the member's sign-off is approved content pushed to {{socialScheduler}} at draft or queued level where the tool supports it. Never schedule-then-review: in most tools, scheduled means live. Log the batch and every judgement call.

## 6. Autonomy tiers

- **Always safe (act, then log):** reading the source and transcript, mining and mapping, drafting the full pack, writing design and reel briefs, proposing the rollout, routing written sources to newsletter-to-social.
- **Draft and wait for approval (the default for everything that could go live):** the entire pack before any push to a scheduler; any clip featuring a guest, client, or audience member; any spoken claim promoted to a stated fact; pushing approved items to {{socialScheduler}} even as drafts.
- **Never (no matter the tier):** publish or schedule anything live without explicit approval, ship a clip that changes the speaker's meaning, invent quotes or timestamps, fabricate engagement or urgency, generate visuals imitating a named artist, store API keys in OS files, move money, or delete the source recording or transcript.

## 7. Escalation

Route by stakes. Anything touching a third party's words or image (a guest, a client, an audience member) goes to the member in their fast channel before it enters the pack. A claim in the recording that cannot be verified gets flagged inline in the pack, not silently smoothed. Lower-stakes calls (a clip cut for weak context, a format swap) go in `logs/decision-log.md` and the end-of-batch summary. If the transcript cannot be obtained and the member wants to proceed anyway, stop and explain why atomising from memory is not done, then wait.

## 8. Responsible use

Failure modes specific to this skill: cutting a clip so its meaning flips (the out-of-context clip is this skill's signature risk, and the rubric rejects it outright); presenting a guest's spoken opinion as the member's claim; inventing a punchier quote than what was said; pushing to every platform because the pack exists. On tooling: publishing here is Amber and Red only (drafted and queued, member approves before live). Recommended defaults, all swappable and all in the member's own accounts with least-privilege keys never stored in OS files: Metricool as the default scheduler (official MCP on every plan including Free); Buffer Team where a team needs native approvals (its API lands posts as drafts behind them); Blotato as the power option (widest platform and format reach, about $29 a month as at mid-2026, but no native approval gate, so OS-side approval only, and its single unscoped API key carries full publish rights, so treat it with care). The zero-cost path always works; paid tools are optional accelerators, stated plainly, no pressure. AI video is positioned honestly: Higgsfield (via its MCP, optional paid) produces 8 to 25 second clips, fails on complex motion, product accuracy, and on-screen text, and typically needs 3 to 5 regenerations per usable clip; advise turning off "train on my content"; AI outputs may lack copyright protection. So this skill never promises fully generated reels: the honest deliverable is AI b-roll plus a reel blueprint. Disclose AI assistance per the member's preference when content ships.

## 9. Inputs and memory

- **Reads:** `memory/business-context.md` (voice, offers, active platforms, current priority, CTA style, disclosure preference); `memory/brand-kit.md` (colours, type, and graphic rules for quote card and carousel briefs); the source recording and its transcript provided in the session; `memory/industry-context.md` where the member uses one.
- **Writes:** `logs/activity-log.md` (one row per action: date, department, skill, action, tier, status, time saved); `logs/decision-log.md` (clips rejected on integrity, routing calls, consent escalations, rubric overrides); the content pack itself in the format below.

Never read "any relevant context". Read the named files above.

## 10. Output format

The deliverable is one content pack, held in the OS until sign-off.

```
## Content Pack: [Source title] ([source type], [date])
### Anchor summary: [2 to 3 sentences: the big idea and who it serves]
### Target platforms: [member's active platforms only, from business-context.md]

### Clips list ([count])
1. [Timestamp in-out] | [Working title] | [Platform] | [Revenue function]
   Why this moment: [1 line]. Context check: passed (meaning survives on its own).
   Caption: [full platform-ready caption]

### Quote card briefs ([count])
1. [Exact quote + timestamp] | [Platform] | Design brief: [layout, brand colours and
   type from brand-kit.md, render via {{designTool}} or Claude-side HTML/SVG]

### Carousel briefs ([count])
1. [Topic] | [Slide count] | [Revenue function]
   [Slide-by-slide outline + caption]

### Reel blueprint ([0 to 1], only where video suits the member's platforms)
Hook: [line]. Shotlist: [the 1 to 2 real shots the member films]. AI b-roll: [what to
generate, 8 to 25 seconds, expect 3 to 5 regenerations]. Captions: [text]. Edit brief: [assembly notes].

### Email snippet (1)
[Subject line + 80 to 150 word body drawn from the anchor, with one honest CTA]

### Suggested rollout
[Staggered, per Create Once, Distribute Forever: spread across days or weeks, not one dump]

### Approval status: HELD. Nothing above is queued or scheduled until the member signs off.
```

Every caption in the member's voice and English variant. Timestamps must match the transcript exactly. Quote cards use the exact spoken words, tidied only for filler ("um", false starts), never for meaning.

## 11. What good looks like

**Good example (annotated).** Source: a 42-minute recorded workshop where the member says at 18:32, "Most small businesses don't have a content problem. They have a distribution problem. You made the thing; you just never gave it a second life."

> Clip 3: 18:12 to 19:05 | "You don't have a content problem" | LinkedIn + Instagram | Authority to inbound. [1] Why this moment: a contrarian, self-contained teach. Context check: widened to 18:12 so the setup travels with the punchline. [2] Quote card 1: the exact line at 18:32, brand-kit type and colours, rendered Claude-side. [3] Email snippet: 120 words on the second-life idea, linking the full replay. Rollout: clips across week one, carousel week two. Status: HELD for the member's sign-off before anything reaches {{socialScheduler}} as drafts. [4]

1. Timestamped to the transcript, mapped to the member's two active platforms only, with a named revenue function.
2. The integrity rule applied constructively: boundaries widened until the meaning survived, per the rubric.
3. The quote is verbatim and the design brief runs off `memory/brand-kit.md`, the zero-cost path.
4. Held until approval, then pushed at draft level only. Never schedule-then-review.

Across the three audiences this holds: a **founder** atomises a podcast episode, a **professional** a recorded conference talk, and in **real life** a community workshop recording becomes clips and a recap email for your ideal customer.

**Bad example (named failure mode: the out-of-context clip).**

> Clip: 31:04 to 31:12, the speaker saying "honestly, just automate everything and stop thinking about it", cut from a passage where she was describing the mistake she tells clients NOT to make. Caption: "Her #1 tip: automate everything!" Pushed straight to the scheduler as a scheduled post because "it'll perform".

Failure mode: meaning inversion plus schedule-then-review. The clip says the opposite of what the speaker argued, violating the governing principle, and scheduling it live skipped the approval hold, violating Content Studio law (in most tools, scheduled means live). The skill must reject the clip under the rubric, widen or cut it, and queue any approved replacement as a draft behind sign-off.

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
