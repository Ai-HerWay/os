---
name: carousel-format
department: Marketing OS
description: >
  Generates social carousel content in the exact markdown format the carousel maker's batch parser understands, anchored to the member's brand, pillars, and revenue path. Use when the member asks to make a carousel, batch carousels, an Instagram carousel, a LinkedIn document post, a multi-slide post, slide content for a swipe post, or to turn a topic into a slide-by-slide deck. Australian English.
audiences: [founder, professional, life]
level: L1 to L2
version: 1.0
updated: 2026-06-09
author: AI Her Way
---

# Skill: Carousel Format

## 1. Role and mandate

This skill turns a topic into a ready-to-render social carousel, written in the precise markdown the carousel maker's batch parser reads. It owns the full path from idea to parseable file: choosing the platform (Instagram or LinkedIn), structuring the hook, content, and call-to-action slides, writing the copy in the member's voice, and producing valid markdown that the maker converts to branded slides. It works the same for a founder building authority for your business, a professional sharing expertise inside an organisation, and a person in real life documenting a project or cause. It does not design the slides (the maker applies the member's saved brand settings) and it does not publish.

## 2. Governing principle

The output must parse. Format fidelity beats cleverness: if a slide does not match the markdown contract in section 10, the carousel maker drops it, so every carousel this skill produces is valid markdown first and good copy second.

## 3. Why this works (evidence base)

Carousels and multi-slide formats outperform single posts because they buy time and second chances inside the platform's own ranking logic.

The strongest named source is Adam Mosseri, Head of Instagram. In an October 2024 explainer (reported by Social Media Today, "IG Chief Recommends Posting Carousels To Improve Reach", 2024), Mosseri said carousels often get more reach than photos for two reasons: "multiple pieces of media are going to mean more interactions with your carousel posts, and more interactions is going to mean more reach on average." He added that if someone sees a carousel but does not swipe, Instagram "will often give that carousel a second chance and automatically move to that second piece of media for the viewer." So a carousel earns two bites at attention from one post, and engagement compounds into reach.

On LinkedIn the mechanism is dwell time. Social Media Today ("Report shows document posts on LinkedIn see more engagement", 2024) reported that document posts (PDF carousels) draw more engagement than other formats, because swiping through slides holds a viewer on the post longer, and the LinkedIn feed rewards content that holds attention. A reader who taps through eight slides is signalling value, and the algorithm reads that signal.

The underlying principle is older than any platform: the Zeigarnik effect (Bluma Zeigarnik, 1927) shows people remember and feel pulled to finish incomplete tasks. A hook slide that opens a loop ("Here's what nobody tells you about X") creates an open task the reader wants to close by swiping. That is why slide 1 is treated as a dedicated hook and the last slide as a dedicated payoff or CTA: the format is engineered around the gap the reader wants to close.

Note on numbers: several engagement percentages circulate in marketing blogs (for example carousels at roughly 10 percent versus single images), but those figures come from third-party tool vendors with varying samples, so this skill cites the platform-level and psychological mechanisms above rather than any single unverified statistic.

## 4. The decision rubric

This is the psychology layer. It decides platform, length, and structure before any copy is written.

| Condition | Decision | Why |
|---|---|---|
| Member names Instagram, or content is visual/lifestyle/quick-tip | Use `IG` prefix, 1080x1350 portrait | Matches Instagram's swipe-and-second-chance behaviour (Mosseri 2024) |
| Member names LinkedIn, or content is professional/B2B/thought leadership | Use `LI` prefix, 1280x1600 portrait | Document posts win on dwell time in the LinkedIn feed (SMT 2024) |
| Member names both, or is unsure | Produce both an IG and an LI version of the same topic | One topic, two parsed sections, no extra effort for the member |
| Topic is broad or educational | Target 6 to 10 slides | Enough slides to build the swipe habit and dwell time without padding |
| Topic is a single sharp insight | 3 to 5 slides | Do not pad; a tight loop beats a long one |
| Slide 1 (always) | Write as a hook that opens a loop | Zeigarnik effect: an open question pulls the swipe |
| Last slide (always) | Write as the payoff or CTA tied to [your primary revenue path] | The reader who finished is the warmest reader you will get |
| A middle slide has more than one idea | Split it, or use `→` arrows for a clean list | One idea per slide protects readability and parse fidelity |
| Brand settings not configured | Proceed anyway; maker uses neutral default theme | Format is independent of brand; never block on missing colours |
| Any line risks breaking the parser (stray `##`, missing `**Slide N:**`) | Fix it before returning | Section 2: the output must parse |

## 5. Workflow

1. Read inputs (section 9): `memory/business-context.md` for voice, pillars, handles, revenue path, plus any working-memory brief the member supplied.
2. Apply the rubric (section 4) to choose platform(s) and slide count.
3. Pick the content pillar this carousel belongs to (from your content pillars). Every carousel anchors to one pillar.
4. Draft slide 1 as a hook that opens a loop. This is the slide that earns the swipe, so write it first and hardest.
5. Draft the middle content slides, one idea each, using `→` arrows for lists where it reads cleanly.
6. Draft the final slide as the payoff plus a CTA that supports [your primary revenue path].
7. Write the caption and a small number of relevant hashtags.
8. Assemble into the exact markdown contract (section 10). Check between steps that every carousel starts with `## ` containing "Carousel" and every slide uses a `**Slide N:**` marker.
9. Validate: re-read the file as the parser would. Strip anything that would silently break (see the rubric's last row).
10. Return the file and note which pillar and platform each carousel serves.

## 6. Autonomy tiers

- Always safe (act, then log): drafting carousel markdown, choosing platform and slide count, writing copy in the member's voice, producing both IG and LI versions of a topic.
- Draft and wait for approval: anything that names a specific person, client, or unverified result; any claim or statistic the member has not supplied; changing the member's saved CTA or revenue path.
- Never (no matter the tier): publishing or scheduling the carousel, inventing testimonials, results, or credentials, hard-coding brand hex values or fonts (the maker owns those), moving money, or committing the member to anything external.

## 7. Escalation

When the topic or a claim cannot be verified from the inputs, do not guess: flag it inline in the returned file with a short bracketed note (for example "[needs a source from the member]") and list those flags at the top of the response so the member sees them at a glance. For anything with legal, financial, or reputational weight, stop and ask the member directly before returning the file, rather than burying it in a digest.

## 8. Responsible use

Specific to this skill: never fabricate the proof a carousel leans on (no invented stats, case studies, client names, or "studies show" without a real named source). If a slide states a number or a result, it must trace to something the member provided or a verifiable public source. Never imply an outcome the member has not earned. When this skill drafts on the member's behalf, the member stays the author and approver; the AI proposes the slides, the human ships them. If a carousel will be published as the member's own thought leadership, that is the member's call to make, not the skill's.

## 9. Inputs and memory

Reads:
- `memory/business-context.md` (voice, content pillars, social handles, primary revenue path, lead magnets, hallmark phrases, English variant, emoji and CTA style)
- The member's working-memory brief or topic file for this batch, if supplied
- `memory/industry-context.md`, if the member uses one, for sector-specific framing

Writes:
- the carousel markdown file the member requested
- `logs/activity-log.md` (a one-line record: how many carousels, which platforms, which pillars)
- `logs/decision-log.md` only when the rubric made a non-obvious call (for example producing both platforms, or flagging a claim for review)

The skill never hard-codes a business, name, niche, or tool: every member-specific value comes from the placeholders below, resolved at runtime from the context file.

## 10. Output format

This is the markdown contract the carousel maker's batch parser understands. Follow it precisely when generating carousel content for your business.

### Default settings

- Primary handle: [your Instagram handle]
- Preferred platforms: Instagram + LinkedIn
- Brand colours and fonts: the carousel maker pulls these from the member's saved brand settings. Do not hard-code hex values or font names here. If brand settings have not been configured, the maker falls back to its neutral default theme.

### Section headers

Each carousel is a `## ` level-2 heading containing the word "Carousel". The heading determines the platform and title.

Instagram carousel:
```
## IG Carousel 1 – Educational (your first content pillar)
```

LinkedIn carousel:
```
## LI Carousel – your first content pillar
```

Format: `## [IG|LI] Carousel [optional number] [separator] [Title]`

- `IG` prefix produces an Instagram carousel (portrait 1080x1350).
- `LI` prefix produces a LinkedIn carousel (portrait 1280x1600).
- Everything after the title separator becomes the carousel title. The parser accepts three separator characters: an em dash, an en dash, or a plain hyphen. The examples above use an en dash; any of the three works. (This is the one place the parser tolerates an em dash; AI Her Way prose never uses one.)
- Sections without "Carousel" in the title are ignored. Text posts, reels, and stories are skipped.

### Slide content

Within each carousel section, slides are marked with `**Slide N:**` bold markers:

```
**Slide 1:** This is the hook headline for slide one
**Slide 2:** Main point headline → Supporting detail one → Supporting detail two → Supporting detail three
**Slide 3:** Another content headline with supporting text below
**Slide 4:** Follow [your Instagram handle] for more insights like this
```

Slide numbering:
- Slide 1 is always treated as the Hook slide (cover/intro).
- The last slide is always treated as the CTA slide (call to action).
- All middle slides are Content slides.

Arrow notation for bullet points: use `→` arrows to create a bullet list within a slide:

```
**Slide 3:** The headline text → First bullet point → Second bullet point → Third bullet point
```

Multi-line slide content: slides can also carry multi-line content between markers:

```
**Slide 2:** Headline Goes Here

Body text paragraph that appears below the headline.

- Bullet point one
- Bullet point two
```

### Optional metadata (ignored by parser)

These are commonly present in batch files but are stripped during parsing:

```
**Slide-by-slide content:**    ← Section intro, ignored
**Caption:** ...               ← Stripped from slide content
**Topic:** ...                 ← Stripped
**Post type:** ...             ← Stripped
---                            ← Section separators, stripped
```

### Voice and style notes

- Write all copy in your preferred variant of English.
- Emoji usage: your emoji preference.
- CTA style: your preferred style, from your context file.
- Weave in the member's hallmark phrases where they fit naturally: [your hallmark phrases].
- Keep every carousel anchored to one of the member's content pillars (listed in your context file).
- The closing CTA should support the primary revenue path: [your primary revenue path].

### Platform differences

| Platform | Prefix | Aspect Ratio | Dimensions |
|----------|--------|-------------|------------|
| Instagram | `IG` | Portrait | 1080 x 1350 |
| LinkedIn | `LI` | Portrait | 1280 x 1600 |

### Three-audience framing

The same contract serves all three audiences: a founder builds authority for your business (CTA to [your primary revenue path]), a professional shares an expertise carousel inside their organisation (CTA to a resource or a follow), and a person in real life documents a project or cause (CTA to follow [your Instagram handle]). One format, three uses, no editing of the skill.

## 11. What good looks like

### Good example (annotated)

```markdown
## IG Carousel 1 – Educational (your first content pillar)

**Slide-by-slide content:**

**Slide 1:** your first content pillar Is Changing Everything: Here's What You Need to Know
**Slide 2:** What is your first content pillar? → It's a practical approach you can apply today → It goes beyond the basics → Think of it as a transformative tool
**Slide 3:** Why This Matters for your ideal customer → Solve your biggest challenges → Scale your impact → Free up time for strategy
**Slide 4:** How to Get Started → Pick one area to focus on → Choose the right tools → Start small, iterate fast
**Slide 5:** Ready to get started? Follow [your Instagram handle] for weekly tips

**Caption:**
your first content pillar isn't the future. It's the present. Here's your quick guide to understanding what it means and how to use it in your work as your ideal customer.

Want to go further? Grab my free [your lead magnet], link in bio.


#your first content pillar #tips
```

Why this is good:
- Annotation 1: the heading contains "Carousel" and uses the `IG` prefix, so the parser renders it as a five-slide Instagram carousel (slide 1 Hook, slides 2 to 4 Content, slide 5 CTA).
- Annotation 2: slide 1 opens a loop ("Here's What You Need to Know") that the reader closes by swiping, which is the Zeigarnik mechanism from section 3 doing the work.
- Annotation 3: arrows turn dense slides into clean, swipe-friendly lists, one idea per arrow, which protects both readability and parse fidelity.
- Annotation 4: every member-specific value is a placeholder resolved from `business-context.md`, so the same file works for any member with no editing.

### Bad example (named failure: silent parser drop)

```markdown
# IG Carousel about productivity

Slide 1 - Productivity tips for busy people
Slide 2: Time blocking, batching, and saying no
```

Named failure mode: silent parser drop. The heading uses a single `#` and does not contain the word "Carousel", so the parser ignores the entire section and nothing renders. The slides use plain "Slide 1 -" text instead of the required `**Slide N:**` bold markers, so even if the heading were fixed, no slides would be detected. Slide 2 also crams three ideas into one line with no `→` arrows, which would render as an unreadable wall. This is exactly the outcome section 2's governing principle exists to prevent: the output did not parse, so the cleverness of the copy never mattered.

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
| 2026-06-09 | 1.0 | Retrofitted from the 7-section template to the 11-section DNA with researched evidence base. | AI Her Way |
