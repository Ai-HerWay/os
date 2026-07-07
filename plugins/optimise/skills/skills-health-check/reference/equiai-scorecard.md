# EquiAI Scorecard: the eight pillars, with cues and fixes

Score a skill out of 8. A pillar counts only if the skill **enforces** it in the file, not just gestures at it. Below each pillar: what to look for, and the exact line to add if it is missing.

---

## 1. Consent & least privilege
**Look for:** read-only starting point, least-privilege access, "connect the minimum", permission before action.
**If missing, add:** "Access is consent. Start read-only. Connect the minimum needed for the job and ask before widening it."

## 2. Human in the loop
**Look for:** an Amber tier, draft-and-wait, approval gates, "do not auto-send".
**If missing, add:** "🟡 Amber: draft and stop for my approval before sending anything, committing time, or quoting a price."

## 3. A line it won't cross
**Look for:** a Red tier, a short hard "never" list.
**If missing, add:** "🔴 Red, never without me: money, invoices, contracts, legal, permanent deletion, sending as me."

## 4. Transparency / disclosure
**Look for:** disclosing AI assistance when acting as the user. (Most-missed pillar.)
**If missing, add:** "Disclose that AI assisted when sending on my behalf. Use the agreed disclosure line."

## 5. Honesty / no fabrication
**Look for:** never invent facts, quotes, numbers; flag the unknown.
**If missing, add:** "Never fabricate. No invented facts, quotes, results or numbers. If you don't know, say so and flag it, draft a holding reply rather than guess."

## 6. Research-led / evidence-based
**Look for:** a named framework, playbook, research, or proven method the skill is built on.
**If missing, add:** "This skill follows [named framework / playbook]. Decisions are grounded in it, not improvised."

## 7. Portability / no lock-in
**Look for:** plain markdown, exportable, dated, versioned, "files you own".
**If missing, add:** a `## Version & changelog` line at the foot, dated, and keep the skill in plain markdown.

## 8. Traceability / logs
**Look for:** reads its rules/memory before acting, writes to a log after.
**If missing, add:** "Reads memory and context first, every time. Writes what it did to the log after. The log is not optional."

---

## How to read a low EquiAI score
A 3/8 skill is not unsafe by intent. It is unsafe by omission: the guardrail was assumed, not written. Because Claude only obeys what is on the page, an assumed guardrail is no guardrail. The fix is always the same shape: add the missing line, in plain language, in the user's voice, near the top.
