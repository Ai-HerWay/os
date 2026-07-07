# The Global Standard for a Great Skill File

This is the bar every skill in your library is held to. It comes from the AI Her Way skills audit and the EquiAI framework. A skill that meets this standard triggers when it should, never blends with another, and has its safety written into the file rather than bolted on after.

There are two halves: **Hygiene** (does Claude understand and obey it) and **EquiAI** (is it safe, honest and yours). A great skill scores high on both.

---

## Part 1: Hygiene: so Claude actually follows it

### 1. One job per skill
A skill should be describable in one sentence with no "and also". If it needs an "and also", split it, or it will collide with its neighbours and Claude will pick the wrong one.

- Name it as a job: `verb-object` or `domain-function`. Good: `inbox-manager`, `hub-launch-scorecard`, `viral-hook-architect`.
- Avoid vague nouns. `marketing-head-agent` and `newsletter-generator` are too generic to fire reliably.
- Lowercase, hyphenated, distinct. If two skills could share a name fragment, one of them is too broad.

### 2. The three-sentence description
The description is the single most important line in the file. It is what Claude matches a request against. Write exactly three sentences, always in this order:

```
Use this skill when [the trigger situation + 4 to 6 real trigger phrases in quotes].
It does [the one job, in one line].
Do NOT use it for [the adjacent job], use [other-skill-name] for that.
```

Worked example:

> Use this skill when writing long-form sales assets: "sales page", "landing page", "VSL script", "ad copy", "opt-in page", "checkout copy". It writes high-converting copy in Nici's emotionally-led, authority-driven voice. Do NOT use it for emails (use ai-herway-email-marketing), opening hooks (use viral-hook-architect), or emotional reframes of existing copy (use make-them-feel-seen).

That third sentence is the boundary line. It is what stops two skills competing for the same prompt. Skills with no boundary line are the number-one cause of Claude picking the wrong skill.

### 3. NON-NEGOTIABLE RULES at the very top
Claude skims long bodies. The rules that must never be broken cannot live mid-paragraph on line 80. Open every skill, directly under the title, with this block:

```
## NON-NEGOTIABLE RULES
- **NEVER use em dashes. Use a comma, full stop, or brackets.**
- **NEVER auto-send. Draft only, then stop for approval.**
- **ALWAYS Australian English (organise, colour, realise).**
- [the 1 to 2 rules specific to this skill, in bold or CAPS]
```

Three to five rules, no more. Each one bold or CAPS, as a dot point. If everything is a rule, nothing is.

### 4. Positive directive, not just prohibition
Pair every "don't" with the "do". Claude follows instructions to act better than instructions to refrain.

- Weak: "No em dashes."
- Strong: "Use a comma, full stop, or brackets. Em dashes are BANNED."

### 5. Structure Claude can skim
- Steps are numbered, one action per line. No multi-action paragraphs.
- A heading every 10 to 15 lines.
- Tables for any "if X then Y" logic.
- No decorative emoji in structural headings. (A 💛 inside member-facing copy is fine. An emoji as a heading is not.)

### 6. No dead pointers, no stale facts
- If the skill tells Claude to read another skill or file, that skill or file must exist. Dangling references send Claude hunting and it loses the thread.
- Volatile facts (member counts, "as of March", current priorities) go in a dated reference file or memory, never hardcoded in the body. Claude will state a hardcoded fact as current truth long after it stops being true.

---

## Part 2: EquiAI: so it is safe, honest and yours

EquiAI is the AI Her Way ethics layer: **safety from the start, built in, not bolted on.** A skill is scored on how many of the eight pillars it actively writes into the file. You are not aiming to mention them. You are aiming to enforce them.

| Pillar | What a great skill does | The line that delivers it |
|---|---|---|
| **Consent & least privilege** | Starts read-only, asks before it touches more | "Read first, write with permission. Connect the minimum." |
| **Human in the loop** | Drafts and waits on anything that matters | An Amber tier: "Draft and stop for approval before sending." |
| **A line it won't cross** | A short, hard "never" list | A Red tier: "Never touch money, contracts, or send as me." |
| **Transparency** | Discloses AI assistance when it acts as you | "Disclose that AI assisted when sending on my behalf." |
| **Honesty** | Never invents facts, quotes or numbers | "Never fabricate. If you don't know, say so and flag it." |
| **Research-led** | Grounded in a named framework or method | "Based on the 5 Levels framework / the launch playbook." |
| **Portability** | Plain files the student owns, no lock-in | Plain markdown, dated, versioned, exportable. |
| **Traceability** | Reads its rules first, logs what it did after | "Reads business-context first. Writes to the log after." |

The most-missed pillar across real libraries is **Transparency**. Most skills remember "never fabricate" but forget "say an AI helped". If you fix one pillar everywhere, fix that one.

### The AI Traffic Light (use this language on every skill that acts)
- 🟢 **Green**: does it fully, then logs it (triage, label, draft, read for context).
- 🟡 **Amber**: drafts and waits for you (sending, committing time, quoting a price, anything client-facing).
- 🔴 **Red**: never without you (money, invoices, contracts, legal, permanent deletion).

---

## The scoring, in plain terms

- **Hygiene (0 to 100):** full marks, then points come off for a missing or thin description, a broken body, no NON-NEGOTIABLE block, no boundary line, emoji headings, em dashes, stale dates, and dead references.
- **EquiAI (0 to 100):** the share of the eight pillars the skill actively writes in.
- **Overall:** the average of the two. A = 90+, B = 80+, C = 65+, D = 50+, F below 50.

A grade is a prompt, not a verdict. The point is not the number. The point is the fix the number points you to.
