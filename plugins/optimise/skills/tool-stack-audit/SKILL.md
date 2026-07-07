---
name: tool-stack-audit
description: "Use this skill when a student wants to audit their whole software and tool stack: 'audit my tools', 'tool stack audit', 'am I paying for too many tools', 'what can I cancel', 'are my tools worth it', 'streamline my software', 'what can AI replace', 'am I paying twice for AI'. It interviews them about their tools, goals, spend and real usage, researches each tool live to see what it can actually do and whether the AI tools they already pay for now cover it, then builds a stack-on-a-page audit with cut, streamline, maximise and add recommendations, a projected saving, and a 30-day plan. Do NOT use it to audit skill files (use skills-health-check for that) or to choose a single new tool from a blank page."
---

# Tool Stack Audit

Look at a student's entire software stack and give them clarity: what each tool is for, what it really costs, how much of it they actually use, where two tools do one job, what their AI tools now make redundant, and the smallest, sharpest stack that does the job. Research-led, vendor-neutral, and adapted to the individual.

The guiding belief: the best stack is the smallest one that does the job. Fewer tools, used well, beats more tools used barely.

## NON-NEGOTIABLE RULES
- **NEVER ask for or store passwords, card numbers, or account logins.** The audit only needs tool names, plans, and rough monthly costs. Nothing sensitive.
- **NEVER recommend a tool because of an affiliate, sponsorship, or commission.** Vendor-neutral always. Every recommendation is in the student's interest only.
- **NEVER invent a tool's features, pricing, or limits.** Research each one. If you cannot verify a fact, say so and flag it. A confident wrong claim about a tool is worse than "I could not confirm this".
- **ALWAYS advisory.** You recommend, the student decides. NEVER cancel a subscription, buy a tool, or change a plan. Tell them what to do; they do it.
- **NEVER use em dashes. Use a comma, full stop, or brackets. ALWAYS Australian English.**

## What this is for
Stacks grow by accident. A tool gets added for one job, another overlaps it, a subscription quietly renews for something barely opened, and meanwhile the AI workspace the student already pays for can now do half of it. This skill takes stock, researches what is really possible with each tool, and hands back a clear picture: keep, cut, streamline, maximise, add, with the money attached.

The standard it holds the stack to lives in two reference files. Read them before you audit:
- `reference/audit-framework.md`: the dimensions, the four lenses, the pay-twice-for-AI check, the security pass, and the scoring.
- `reference/ai-leverage-map.md`: which categories of tool an AI workspace can now replace or absorb, and how to judge whether someone is maximising a tool.

## Step 1: Understand the person and their goals
Interview, one question at a time, warm and plain. Adapt to their answers. Establish:
- Who they are: a founder, a professional in a role, or running a household.
- Their top two or three goals for the next quarter. The audit is judged against these, not against tidiness for its own sake.
- Their technical comfort, so recommendations match what they will actually do.
- **Which AI tools they already have** and which is their main AI workspace: Claude (and Cowork or Claude Code), ChatGPT (and Codex), Gemini, Copilot, others. This is the lens for everything that follows, so get it clearly.

## Step 2: Capture the stack
Ask them to list every tool they pay for or rely on, or ingest the intake brief from the web Tool Stack Audit page if they have one. For each tool capture: the name, the job it does, the plan or tier, the monthly cost, and roughly how much they actually use it (daily, weekly, rarely, almost never). Do not guess costs; ask.

## Step 3: Research each tool live
This is the heart of the skill and what makes it more than a worksheet. For each tool, research it (web search) and record, with a source for each claim:
- What it does at the student's tier, and its current capabilities (tools change fast, check the present, not your training memory).
- The AI features it now includes (many tools the student pays for already have AI built in).
- What power users do with it that this student may be missing.
- Its pricing tiers, so you can spot a cheaper tier that still does their job, or a more expensive tier they do not need.
- Whether it has been superseded or duplicated by an AI tool the student already pays for.

Flag anything you cannot verify. Never state a feature or price as current without checking it.

## Step 4: Assess against the framework
Using `reference/audit-framework.md`, give each tool one verdict and a plain reason:
- **Keep:** earns its place, used well, no overlap.
- **Maximise:** worth keeping, but the student is underusing it. Name the two or three features or AI capabilities they are missing (from your research).
- **Streamline:** overlaps another tool doing the same job. Name which one to keep and why.
- **Cut:** unused, not earning its cost, or now covered by an AI tool they already pay for.

Then run the **pay-twice-for-AI check** (is any new or existing AI subscription duplicating AI they already have) and the **security pass** (the checklist in the framework).

## Step 5: Build the audit
Produce the audit as JSON in the schema below, then render it:

```
python3 scripts/build_dashboard.py tool_stack.json --out Tool_Stack_Audit.html --title "My Tool Stack Audit"
```

Hand the student the HTML. It shows their whole stack on a page, the cost and projected saving, the four lenses, the AI-leverage map, the security pass, and the 30-day plan.

### The JSON schema
```json
{
  "summary": {
    "generated": "30 June 2026",
    "owner_label": "Founder / Professional / Home",
    "goals": ["goal 1", "goal 2"],
    "ai_workspace": "Claude (Cowork)",
    "monthly_total": 0, "annual_total": 0,
    "monthly_waste": 0, "projected_monthly_saving": 0,
    "currency": "AUD",
    "tool_count": 0, "cut_count": 0, "streamline_count": 0, "maximise_count": 0
  },
  "tools": [
    { "name": "", "category": "", "job": "", "tier": "", "monthly_cost": 0,
      "usage": "daily|weekly|rarely|almost never", "verdict": "keep|maximise|streamline|cut",
      "reason": "", "sources": ["url or note"] }
  ],
  "recommendations": {
    "cut": [ { "tool": "", "why": "", "monthly_saving": 0 } ],
    "streamline": [ { "tools": ["A","B"], "keep": "", "why": "", "monthly_saving": 0 } ],
    "maximise": [ { "tool": "", "missing": ["feature 1","feature 2"], "why": "" } ],
    "add": [ { "tool_or_feature": "", "fills_gap": "", "note": "only if a real gap" } ]
  },
  "ai_leverage": [ { "currently_paying_for": "", "your_ai_could_do_it": "", "tool": "", "confidence": "high|medium|low" } ],
  "pay_twice_for_ai": [ { "note": "" } ],
  "security": [ { "check": "", "status": "ok|action|unknown", "note": "" } ],
  "plan": [ { "action": "", "by_when": "", "impact": "" } ]
}
```

Every cost is the student's stated figure or a verified tier price. Never fabricate a number. Mark a cost as estimated if it is.

## Step 6: Walk the recommendations and the plan
Talk through the top moves in order of impact: the clear cuts, the overlaps to consolidate, the tools to maximise, and any real gap to add. Show the projected monthly and annual saving. Then agree the three dated actions in the 30-day plan. The student decides and makes every change themselves.

## Responsible use (EquiAI, applied to this skill)
- **Vendor-neutral:** no affiliate or sponsored recommendations, ever. The student's interest is the only interest.
- **Honesty:** research before you assert. Cite sources. Flag what you cannot verify. Never invent a feature, price, or saving.
- **Privacy:** tool names and costs only. Never passwords, card details, or logins. Remind the student of this if they start to share them.
- **Human in the loop:** advisory only. You never cancel, buy, or change a plan. The student acts.
- **Transparency:** say plainly that the audit is advice based on research at a point in time, and that tools and prices change, so re-run it each quarter.

## Version and changelog
- v1.0: Built for AI Her Way students. Interviews, researches each tool live, audits the whole stack across cut, streamline, maximise and add, with the AI-leverage lens and a 30-day plan. Plain markdown and Python, vendor-neutral, you own all of it.
