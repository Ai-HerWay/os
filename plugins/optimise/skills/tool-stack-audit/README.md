# Tool Stack Audit

Audit your whole software stack against one standard: what each tool is for, what it really costs, how much you use it, what your AI tools now make redundant, and the smallest, sharpest stack that does the job.

## Install
1. Save the `.skill` file when prompted, or drop this folder into your skills directory
   (`.claude/skills/` for Claude Code, or install via Cowork).
2. In a new chat, say: **"audit my tool stack"**. It interviews you, researches each tool, and builds your audit.

## What it does
- **Interviews** you about your goals, your tools, what you pay, how much you use them, and which AI tools you already have.
- **Researches each tool live** so the advice reflects what the tool can really do now, not guesswork.
- **Audits the whole stack** across four lenses: keep, maximise, streamline, cut, with a projected saving.
- **Flags paying twice for AI**, runs a quick security pass, and gives you a dated 30-day plan.
- Builds an interactive **stack-on-a-page** dashboard you open in any browser.

## Run the engine directly (optional)
The skill writes a `tool_stack.json`, then renders it:
```
python3 scripts/build_dashboard.py tool_stack.json --out Tool_Stack_Audit.html
```
Open the HTML in any browser. No internet needed to view it.

## What's inside
- `SKILL.md`: the audit workflow Claude follows.
- `reference/audit-framework.md`: the standard, the four lenses, the pay-twice-for-AI check, the security pass.
- `reference/ai-leverage-map.md`: what an AI workspace can and cannot replace, and how to judge if a tool is maximised.
- `scripts/build_dashboard.py`: turns the audit into the interactive dashboard.

## The intake brief (from the web Tool Stack Audit page)
If you filled in the intake on the Hub's Tool Stack Audit page, paste the brief it gave you at the start and the skill will use it instead of asking you to list everything again. The brief looks like this:

```
# Tool Stack Audit intake
Owner: Founder | Professional | Home
Goals: <goal 1>; <goal 2>; <goal 3>
AI tools I have: Claude (Cowork), ChatGPT, ...
Main AI workspace: Claude

## Tools
- <name> | <category> | <job> | <tier> | <monthly cost> | <usage: daily/weekly/rarely/almost never>
- ...

Monthly total (my figure): <amount>
```

Plain markdown and Python. Vendor-neutral, advisory only. You own all of it. No lock-in.
