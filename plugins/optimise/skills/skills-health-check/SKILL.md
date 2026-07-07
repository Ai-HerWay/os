---
name: skills-health-check
description: "Use this skill when a student wants to audit, clean up, or understand their own skill files: 'audit my skills', 'skills health check', 'check my skills', 'clean up my skills', 'are my skills any good', 'why is Claude ignoring my skill', 'show me how my skills connect', 'skill map'. It scans a folder of skill files, scores each one on hygiene and the EquiAI safety framework, suggests fixes you approve before anything is written, and builds an interactive network map of how your skills connect. Do NOT use it to write a brand-new skill from scratch (use skill-creator for that) or to build an agent card (use the role-card skills)."
---

# Skills Health Check

Audit, manage and map a library of Claude skill files against the AI Her Way global standard. Keep every skill clean, make sure none of them fight each other, score them for safety, and show the whole library as a network map.

## NON-NEGOTIABLE RULES
- **NEVER edit a student's skill file without showing the change and getting a clear yes first.** Suggest, then apply on approval, one file at a time.
- **NEVER invent a skill's contents.** Read the actual file. If you cannot read it, say so.
- **ALWAYS back up before writing.** Copy the original to a `.backup` before applying any fix.
- **NEVER use em dashes. Use a comma, full stop, or brackets.**
- **ALWAYS Australian English (organise, colour, realise).**

## What this skill is for
A student's skill library drifts. Skills pile up, two of them start competing for the same request, descriptions go thin, safety rules get assumed instead of written. This skill is the health check for your library: it takes stock, scores everything against one standard, tells you exactly what to fix, and draws you a map so you can see your whole library at a glance.

The standard it holds every file to lives in two reference files. Read them before you audit:
- `reference/global-standard.md`: hygiene + EquiAI, the full bar.
- `reference/equiai-scorecard.md`: the eight safety pillars, with the exact line to add when one is missing.

## Step 1: Find the skills
Ask the student where their skills live if it is not obvious. Common locations:
- a `skills/` or `.claude/skills/` folder, each skill in its own directory with a `SKILL.md`,
- a folder of standalone `*.md` skill files.

Confirm the path. Never guess and audit the wrong folder.

## Step 2: Run the audit engine
The engine does the heavy lifting: parses each file, scores it, finds overlap and references, clusters by domain, and writes one JSON file.

```
python3 scripts/audit_skills.py <skills_folder> --out skills_data.json
```

It prints a one-line summary (skills audited, average score, overlap links, fixes queued). If Python is not available, you can do the same audit by hand using the two reference files, but the engine is faster and consistent.

## Step 3: Build the map and dashboard
Turn the JSON into a single self-contained HTML file the student can open in any browser. It shows the network map, every skill scored, the EquiAI coverage gaps, and the fix queue.

```
python3 scripts/build_dashboard.py skills_data.json --out Skill_Map.html --title "My Skill Map"
```

Hand the student the HTML file. The map: red lines are trigger overlap (skills competing for the same prompt), dashed green lines are references (one skill calling another), node colour is the domain cluster, node size is how many skills it overlaps with, a red ring means a low grade.

## Step 4: Walk the fix queue, suggest then apply on approval
This is the heart of the skill and where the NON-NEGOTIABLE rules bite. Work the queue top down, P0 first.

For each fix:
1. **Show the problem** in plain language (the dashboard and JSON both list it).
2. **Draft the exact change.** For a description, write the new three-sentence version. For a missing safety pillar, paste the ready-made line from `equiai-scorecard.md`. For a missing rules block, draft the `## NON-NEGOTIABLE RULES` block.
3. **Ask: apply this?** Wait for a clear yes.
4. **On yes:** copy the original to `SKILL.md.backup`, then make the edit. Confirm what changed.
5. **On no or "let me think":** leave it, move on. The student owns the file.

Never batch-apply. Never apply without the yes. One file, one change, one confirmation.

## Step 5: Re-run and show the lift
After a batch of approved fixes, re-run Steps 2 and 3. The average score rises, overlap links drop, EquiAI coverage fills in. Show the before and after. That visible lift is the reward loop that makes a student keep their library clean.

## The grading, briefly
- **Hygiene (0 to 100):** description quality, working body, rules-at-top, a boundary line, clean structure, no stale facts or dead pointers.
- **EquiAI (0 to 100):** how many of the eight safety pillars the skill actually writes in.
- **Overall:** the average. A 90+, B 80+, C 65+, D 50+, F under 50. A grade is a prompt to act, not a verdict.

## Responsible use (EquiAI, applied to this skill itself)
- **Consent:** the student points you at their folder. You read only what they show you.
- **Human in the loop:** every change is drafted and waits for approval. This skill never writes silently.
- **A line it won't cross:** it never deletes a skill, never bulk-overwrites, never touches anything outside the skills folder.
- **Transparency:** say plainly that the scores are advisory heuristics, not a certification.
- **Honesty:** if a file cannot be read or a score is uncertain, say so. Do not fabricate a result.
- **Traceability:** keep the `.backup` files and tell the student a backup was made.

## Version & changelog
- v1.0: Built for AI Her Way students. Audits hygiene + EquiAI, suggests fixes on approval, maps the library. Plain markdown and Python, no lock-in, you own all of it.
