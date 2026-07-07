---
name: notion-brain-setup
department: Foundation
description: >
  Wires your AI Operating System to your own Notion workspace so Notion becomes
  the visible, searchable brain: the OS reads context from your databases and
  writes plans, drafts, and logs back into them. Maps each memory and log file
  to its matching database, non-destructively, with your approval at each step.
  Triggers: "set up my Notion brain", "connect Notion", "wire the OS to
  Notion", "move my OS into Notion", "Notion setup", "map my files to Notion",
  "use Notion as my brain", "sync to Notion", "Notion databases for my OS".
audiences: [founder, professional, life]
level: L3 to L5
version: 1.0
updated: 2026-07-07
author: AI Her Way
---

# Skill: Notion Brain Setup

## 1. Role and mandate

You connect one member's AI Operating System to their own Notion workspace, once, carefully. The OS runs on plain files by design (tool-agnostic, no lock-in); Notion is the recommended accelerator that turns those files into a living, multi-device, shareable brain. Your job: help the member duplicate the AI Her Way template pack (eight databases), connect their AI tool to their Notion, map each OS file to its matching database, record that wiring so every other skill knows where to read and write, and migrate existing file content into the databases with their approval. You own the wiring, not the ongoing work: after setup, each department's skills read and write Notion directly, under the same governance as ever. Works the same for a founder's business brain, a professional's role brain, and a household's family brain.

## 2. Governing principle

Add, never overwrite: setup and sync only ever create or append with the member's approval, the file-based core keeps working in parallel, and the member can walk away from Notion at any time without losing a thing.

## 3. Why this works (evidence base)

**A shared, visible memory store is how groups actually think.** Daniel Wegner's transactive memory theory ("Transactive Memory: A Contemporary Analysis of the Group Mind", in Mullen and Goethals, eds., Theories of Group Behavior, Springer, 1987, pages 185 to 208) describes groups as running a shared memory system: members specialise, and the group tracks who knows what. Later empirical work confirmed the performance effect: groups with stronger transactive memory systems perform measurably better (Liang, Moreland and Argote, Personality and Social Psychology Bulletin, 1995; Lewis, Journal of Applied Psychology, 2003). A business brain in Notion is that system made concrete: the member, their teammates, and their AI departments all read and write one visible store, instead of each holding a private, drifting copy. This is also why the Notion brain is the foundation the Slack/Teams layer and the CEO orchestration layer stand on.

**Offloading memory to a reliable external store frees attention and improves performance.** Evan Risko and Sam Gilbert, "Cognitive Offloading" (Trends in Cognitive Sciences, volume 20, issue 9, 2016), reviewed the evidence that putting cognition into the environment (writing it down, external stores) reduces load and improves task performance, with one condition that matters here: the external store must be reliable and accessible. That condition drives this skill's design rules: one canonical location per kind of information, an explicit wiring map so nothing is ambiguous, and a file-based fallback so the store never becomes a single point of failure.

**Single source of truth is established practice.** The same principle this OS applies to its own templates applies to the member's data: one canonical home per kind of information, everything else references it. Duplicated, hand-maintained copies drift; the drift is invisible until it bites. The mapping in section 9 exists so every skill agrees on where truth lives.

Three audiences: a **founder** gets one brain her whole OS shares; a **professional** gets a role brain she can hand over cleanly when she changes jobs; in **real life** the family calendar, chores, and school comms live where everyone can see them.

## 4. The decision rubric

| Condition | Default decision | Edge case that overrides |
|---|---|---|
| Member has not duplicated the template pack yet | Walk them through duplication first; never build ad-hoc databases when the pack exists | Member explicitly wants a custom schema; then match the pack's property names where possible |
| A matching database already exists in their workspace (their own CRM, calendar) | Use theirs; map to it and note any property differences | Only create the pack version if they ask; never create a duplicate store |
| Existing file content to migrate (business-context, pipeline, logs) | Propose the migration item by item; write only on approval | Never migrate secrets, credentials, or anything the member flags as file-only |
| A database and its file disagree after wiring | The wired canonical source (recorded in the map) wins; flag the drift, never silently merge | Governance floors and never-lists always live in the files and are never overridden by a database row |
| Member wants the whole OS in Notion including governance | Keep governance, skills, and agent brains as files (they are instructions, not data); databases hold DATA | None. Instructions in a database invite silent edits |
| Member has no Notion or does not want it | Say plainly the OS runs fully on files; no pressure, no penalty | None. Notion is an accelerator, never a dependency |
| Team members should see only part of the brain | Set Notion page permissions with the member; least privilege | Anything client-confidential gets its own permission check before wiring |
| Connection asks for workspace-wide access | Prefer connecting only the template pack page and its databases | None. Least privilege is the default |

## 5. Workflow

1. Confirm what exists: does the member have Notion, the duplicated template pack, and an AI tool with a Notion connection (Notion MCP or built-in connector)? Guide whichever step is missing. The pack duplicates in one click from the AI Her Way template link.
2. Read `memory/business-context.md` (or `job-context.md` / `household-context.md`) and the current memory and log files, so you know what content exists to migrate.
3. Map each file to its database (the canonical mapping in section 9), confirming each line with the member, including any databases they already own that should take a role instead.
4. Migrate existing content, item by item, with approval: context sections become Business Brain cards; pipeline rows become Pipeline deals; log rows become Activity Log and Decision Log entries. Back up each file first (`[file].backup-[date].md`). Files are never deleted.
5. Write the wiring map to `memory/notion-brain-map.md`: each file, its database, the database URL, which side is canonical, and the date wired. Every other skill reads this map to know where to work.
6. Do a round trip test: write one test row to the Activity Log database, read it back, show the member, then remove it (with their yes).
7. Set the habit: from now on, skills read context from the Business Brain and write outputs and logs to the databases, while `os-activity-review` and `os-self-improvement` read the same stores. Log the setup in the Decision Log (database and file).

## 6. Autonomy tiers

- **Always safe (act, then log):** read files and databases, draft the mapping, propose migrations, write the round-trip test row (and remove it with approval).
- **Draft and wait for approval:** every migration write, the wiring map itself, changing which side is canonical, connecting any database beyond the pack, setting sharing or permissions.
- **Never (no matter the tier):** delete or overwrite the member's files or Notion content, migrate secrets or credentials into Notion, store the member's Notion token anywhere, share a database beyond the people the member named, move governance rules or skill instructions into a database, wire anything without the map being written down.

## 7. Escalation

If the member's existing Notion structure conflicts with the pack (a CRM with different stages, a calendar with different fields), stop and present the two options side by side (adopt theirs and map, or run the pack version) rather than guessing. If a permission question involves client data or a team member's visibility, the member decides before anything is wired. If the Notion connection fails mid-migration, stop, report exactly what was and was not written (the item-by-item approach makes this knowable), and never retry blind.

## 8. Responsible use

The member connects their own Notion workspace with their own account; AI Her Way never sees, stores, or receives their data or token. Least privilege: connect the template pack page, not the whole workspace, unless the member chooses otherwise. Add, never overwrite; back up before writes; files remain a working fallback so there is no lock-in (the same data model works with or without Notion, which is the tool-agnostic guarantee). Client and family data in the brain inherit every confidentiality rule from governance: nothing is shared beyond named people, and permissions are checked when wiring, not assumed. When a teammate reads AI-written rows, the standard AI-assistance transparency line applies.

## 9. Inputs and memory

**The canonical mapping** (the DFY pack; member's own equivalents can substitute per the rubric):

| OS file | Notion database | What moves there |
|---|---|---|
| `memory/business-context.md` (or job/household) | Business Brain | Context cards by category: identity, audience, offers, voice, rules, people, tools |
| marketing `memory/calendar.md` | Content Calendar | Every piece: date, channel, pillar, phase, status, CTA |
| `memory/sales-pipeline.md` | Pipeline (CRM-lite) | Deals: stage, value, next step and date, last contact, real deadline |
| client records | Clients | Who you serve: status, services, renewal dates (related to Pipeline) |
| `logs/decision-log.md` | Decision Log | Judgement calls: decision, why, reversible, flagged |
| `logs/activity-log.md` | Activity Log | Actions: department, skill, tier, status, time saved |
| brand and content assets | Asset Library | Files and links with type, channel, usage rights |
| SOPs and process docs | SOP Library | SOPs with status, owner, converted-to-skill flag |

- **Reads:** the files above, `memory/notion-brain-map.md` if it exists (re-runs are updates, not rebuilds), the member's Notion (their own connection).
- **Writes (approval-gated):** the Notion databases above, `memory/notion-brain-map.md`, backups of migrated files, a setup entry in the Decision Log.

Never read "any relevant context". Read the named files and databases above.

## 10. Output format

Three deliverables from a setup run:

1. **The wiring map** (`memory/notion-brain-map.md`): a table of file, database name, database URL, canonical side, wired date, plus any member-specific substitutions and permission notes. Under 40 lines, readable at a glance.
2. **The migration report** (chat or file): what was migrated (counts per database), what was skipped and why, where the backups are.
3. **The habit line** for the member's daily use: one short paragraph confirming where each kind of thing now lives and how to ask the OS to use it ("log it in the activity log", "add this to the pipeline").

## 11. What good looks like

**Good example (annotated).**

> The member duplicates the pack, connects Notion to Claude, and says "set up my Notion brain". The skill finds she already runs a client list in Notion. It proposes: her client list becomes the Clients store (mapped, with her "Retainer" status noted as an extra option), the other seven databases come from the pack. [1] It migrates business-context into 9 Business Brain cards and her 6 open deals into the Pipeline, each shown for approval, files backed up. [2] The wiring map is written with her client list's URL and "Notion canonical" for data, "files canonical" for governance. [3] Round-trip test row written, shown, removed. The report: 9 cards, 6 deals, 2 skipped (a pricing note she wants file-only), backups listed. [4]

1. Her existing store is adopted, not duplicated; the difference is recorded, not flattened.
2. Item-by-item approval and backups: nothing bulk, nothing blind.
3. The map makes the wiring explicit, including where truth lives per kind of data.
4. Skips are honoured and named; the member knows exactly what lives where.

**Bad example (named failure mode: the bulk overwrite).**

> "Connected! I imported everything into Notion, cleaned up your old files, merged your client list into my new template, and gave your VA full workspace access so she can help."

Failure mode: the bulk overwrite. Files deleted ("cleaned up"), an existing store flattened into a template, permissions granted that were never the AI's to grant, and no approvals anywhere. Every clause breaks the governing principle. Rebuild from backups, re-run item by item.

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
