# Matching Method: installed library to Hub catalogue

How to compare what the student has installed against the Hub catalogue, and how to sort every item correctly. Getting this right is what stops the report being noisy. The failure to avoid: calling something a gap, an update, or a broken skill when it is really a custom skill, a scheduled task, or not a skill at all.

## First, what counts as an installed skill

A skill is one of:
- a directory containing a `SKILL.md`, or
- a standalone `.md` file written as a skill (it has a name and a description or clear instructions).

The following are NOT skills, and must be excluded before matching. Ask the student for these up front:
- **Scheduled tasks** (Cowork or ChatGPT tasks). They live outside the skills folder and are not catalogue skills.
- **The plugin or package name** itself.
- **Examples inside a skill** ("e.g. if the skill is X"). A back-ticked hyphenated word is not proof of a skill.
- Generic utility files (a format helper, a memory-consolidation utility). Tag these as utilities and set them aside.

If you are unsure whether a file is a real skill, ask. Never guess it into a bucket.

## Matching an installed skill to a catalogue entry

For each real installed skill, look for its match in the catalogue using, in order of confidence:
1. **Slug or path match.** The installed name equals a catalogue `id` or the file matches a catalogue `path`. Highest confidence.
2. **Title match.** The installed title equals or closely equals a catalogue `title`.
3. **Description and tag match.** The installed skill does the same job as a catalogue entry (its description and tags line up), even if renamed. Medium confidence. Confirm with the student before treating a fuzzy match as "the same skill", because a wrong match can trigger a wrong sync.

If no catalogue entry does the same job, it is the student's **own** skill. Keep it. It is not a gap and not an error.

## Sorting into the four buckets

| Bucket | Test |
|---|---|
| **Matched and current** | Installed skill matches a catalogue entry, and the installed version equals the catalogue `version`. Nothing to do. |
| **Update available** | Installed skill matches a catalogue entry, but the catalogue `version` is newer (or the catalogue `dateAdded` / update is later than the installed file). A sync candidate. |
| **Gap** | A catalogue skill with no installed match, that fits the student's goals, department, and audience. A candidate to add. |
| **Their own** | An installed skill with no catalogue match. Custom work. Keep as-is. |

## Version comparison (for the update bucket)

- Prefer an explicit version in the installed file's frontmatter against the catalogue `version`.
- If the installed file has no version, fall back to a content or date signal, and mark the confidence as lower. Never assert "you are behind" without a real signal. When unsure, present it as "worth checking", not "out of date".

## Ranking gaps (so the report is goal-led, not a catalogue dump)

A gap is only worth surfacing if it serves the student. Rank by:
- **Goal fit:** does it directly help a goal they named? High.
- **Department fit:** is it in a department they are actually building? A department they have chosen not to run is NOT a stack of gaps. Note the department is available, do not list every skill in it as missing.
- **Audience fit:** does its `audiences` include their persona (founder, professional, life)?
- **Foundational first:** a missing Foundation piece (brand voice, governance, a context file) usually outranks a niche departmental skill, because everything builds on it.

Present high-fit gaps clearly, group the rest by department as "also available", and never imply the student is behind for not having skills they do not need.
