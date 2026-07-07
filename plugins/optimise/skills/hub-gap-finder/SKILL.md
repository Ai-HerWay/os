---
name: hub-gap-finder
description: "Use this skill when a student wants to compare their AI skill library against the AI for Impact Hub catalogue and close the gaps: 'what am I missing', 'compare my skills to the Hub', 'hub gap analysis', 'what skills should I add', 'are my skills up to date', 'sync the latest Hub versions', 'update my skills to the newest version', 'what's new in the Hub for me'. It reads the student's installed skills, fetches the current Hub catalogue, and produces a report of gaps to add, updates to sync, and their own custom skills to keep, then adds or updates files only with approval and a backup. Do NOT use it to score or clean existing skills (use skills-health-check) or to audit software subscriptions (use tool-stack-audit)."
---

# Hub Gap-Finder & Sync

Compare a student's AI skill library against the AI for Impact Hub catalogue, then close the gaps: recommend the Hub skills worth adding, sync the newer Hub versions into the skills they already have (without trampling their customisations), and clearly keep their own custom skills as their own. Research-informed, approval-gated, and adapted to the individual's goals.

The guiding belief: the student's library should grow toward what serves their goals, not toward "install everything". A gap only matters if it moves them forward, and an update is only worth syncing if it genuinely improves what they have.

## NON-NEGOTIABLE RULES
- **NEVER overwrite, replace, or delete a student's existing skill without showing the exact change and getting a clear yes first.** Back up the original to a `.backup` before any write. One file, one change, one confirmation.
- **NEVER blindly replace a customised skill with the Hub version.** Their customisations (their business-context references, their voice, their edits) are the point. Sync means merge the improvement in, not paint over their work. See `reference/sync-guidance.md`.
- **NEVER treat a scheduled task, a plugin or package name, or an example inside a skill as a skill.** Those are not skills and are not gaps. Ask for the student's scheduled-task and plugin names and exclude them.
- **NEVER invent a Hub skill, version, or "what's new".** Use the fetched catalogue. If you cannot fetch it, say so and use the bundled snapshot, and tell the student it may be out of date.
- **NEVER use em dashes. Use a comma, full stop, or brackets. ALWAYS Australian English.**

## What this is for
A member finishes a few Hub modules, builds some skills, then loses track: which Hub skills they never got to, which of theirs are now a version behind, and which are their own inventions that the Hub will never have. This skill draws the line between their library and the Hub catalogue and tells them exactly where they stand, then helps them act on it safely.

The standard it works to lives in two reference files. Read them before you run:
- `reference/matching-method.md`: how to match an installed skill to a catalogue entry, and how to tell a custom skill and a non-skill apart from a genuine gap.
- `reference/sync-guidance.md`: how to bring a newer Hub version into an existing skill without losing the student's customisations.

## Step 1: Understand the person and point at the library
Interview, one question at a time, warm and plain. Establish:
- Who they are (founder, professional, or home) and their top two or three goals for the quarter. Gaps are ranked against these, not against completeness.
- Which departments they are actually building (Marketing, Admin & Ops, Home, and so on), so you do not flag a whole department they have chosen not to run as a "gap".
- **Where their skills live.** In Cowork, request folder access or offer the common locations (`.claude/skills/`, a `skills/` folder). Point at their canonical source, not a deployed plugin cache that gets overwritten on rebuild. Confirm the path before reading.
- Their scheduled-task names and plugin/package name, so those are never mistaken for skills or gaps.

## Step 2: Read the installed library
List every installed skill (a folder with `SKILL.md`, or a standalone `.md` skill file). For each, read its name, description, and any version noted in the file. Exclude the scheduled tasks and plugin names from Step 1. This is the "have" side.

## Step 3: Fetch the Hub catalogue (the "on offer" side)
Fetch the current catalogue:
```
https://ai-os-builder.vercel.app/templates/LIBRARY.json
```
If the fetch succeeds, use it and note the version and date. If it fails (offline, blocked), fall back to the bundled `reference/hub-catalogue.json` and tell the student it is a snapshot that may be behind the live Hub. Never invent catalogue entries.

## Step 4: Match, and sort into four buckets
Using `reference/matching-method.md`, compare installed skills to the catalogue and sort every item into exactly one bucket:
- **Matched and current:** they have it, at the current Hub version. Nothing to do.
- **Update available:** they have it, but the Hub version is newer. A sync candidate (Step 6).
- **Gap:** a Hub skill they do not have, that fits their goals, department, and audience. A candidate to add (Step 6).
- **Their own:** an installed skill with no Hub equivalent. This is their custom work. Keep it, celebrate it, never flag it as a gap or try to "correct" it.

Rank gaps by fit to their goals and department, not by catalogue size. A department they have chosen not to run is not a pile of gaps.

## Step 5: Build the report
Produce the report as JSON in the schema below, then render it:
```
python3 scripts/build_dashboard.py hub_gap_report.json --out Hub_Gap_Report.html --title "My Hub Gap Report"
```

### The JSON schema
```json
{
  "summary": {
    "generated": "7 July 2026",
    "owner_label": "Founder / Professional / Home",
    "goals": ["goal 1", "goal 2"],
    "catalogue_version": "1.0", "catalogue_date": "2026-06-10",
    "catalogue_source": "live | bundled snapshot",
    "installed_count": 0, "matched_current": 0, "update_count": 0, "gap_count": 0, "own_count": 0,
    "departments_present": ["Marketing OS"], "departments_available": ["Sales OS"]
  },
  "updates": [
    { "installed": "", "catalogue_id": "", "title": "", "your_version": "", "hub_version": "",
      "whats_new": "", "sync_note": "how to merge without losing customisations", "priority": "high|medium|low" }
  ],
  "gaps": [
    { "catalogue_id": "", "title": "", "department": "", "tags": [], "description": "",
      "why_relevant": "tied to their goal", "priority": "high|medium|low", "audience_fit": "" }
  ],
  "matched_current": [ { "installed": "", "title": "", "note": "up to date" } ],
  "your_own": [ { "name": "", "note": "custom, no Hub equivalent, keep" } ],
  "recommended_order": [ { "step": 1, "action": "", "why": "" } ]
}
```

Every version and "what's new" is from the fetched catalogue and the real files. Never fabricate. Mark the catalogue_source honestly.

## Step 6: Act, with approval, one file at a time
Walk the recommended order. For each move:
1. **Show it in plain language:** the gap to add, or the update to sync, and why it helps their goal.
2. **Draft the exact change.** For a gap, offer the Hub skill ready to drop in, personalised to their context. For an update, produce the precise merged file (Hub improvement plus their existing customisations preserved), shown inline. Never a vague "update this".
3. **Ask: apply this?** Wait for a clear yes.
4. **On yes:** back up the original to `.backup` (for updates), write the file, confirm what changed.
5. **On no:** leave it, move on. The student owns the library.

Never batch-apply. Never sync over a customised skill without showing the merge first.

## Responsible use (EquiAI, applied to this skill)
- **Human in the loop:** every add and every sync is drafted and waits for approval, with a backup. This skill never writes silently.
- **Respect their work:** custom skills are kept as-is. Syncing preserves customisations; it never paints over them.
- **Honesty:** the catalogue is fetched, not invented. If it is a snapshot, say so. Never fabricate a version or a "what's new".
- **Consent and privacy:** read only the folder they point you at. Nothing is uploaded anywhere. The comparison runs on their machine.
- **Goal-led, not completeness-led:** more skills is not the aim. Recommend only what serves their goals, and say plainly that a department they have chosen not to run is not a gap.

## Version and changelog
- v1.0: Built for AI Her Way students. Compares an installed library against the live Hub catalogue, finds gaps to add and updates to sync, keeps custom skills as their own, and acts only with approval and a backup. Plain markdown and Python, you own all of it.
