# The AI Her Way OS

Your AI business departments, delivered as plugins that stay current.

This is the official plugin marketplace for the [AI Her Way](https://aiherway.com.au) AI Operating System. Add it once, install the departments you run, and every improvement we ship arrives automatically. No re-downloading, no stale files.

> **Please read first: these are templates, not pre-filled with your details.**
> Every skill here is generic on purpose. Out of the box it does not know your business, your voice, or your rules. It becomes yours when it reads your context at runtime. The fastest way: once you have installed a pack, just ask your AI to set it up for you, for example:
>
> ```
> Read the AI Her Way skills I just installed. Interview me to build my
> context (my business, who I serve, my voice, my rules), or use what you
> already know about me from our past work, and save it to
> memory/business-context.md so these skills run as me. Ask one question
> at a time, and show me the file before you save it.
> ```
>
> Or run the [OS Builder](https://ai-os-builder.vercel.app) interview, which writes your Foundation for you. Either way, do this once and every department reads it. See **Make it yours** below.

## Add it once

Open Claude Code or the Claude desktop app (Cowork) and type:

```
/plugin marketplace add Ai-HerWay/os
```

That is the whole setup. You only ever do this once.

## Install the departments you run

```
/plugin install foundation@aiherway
/plugin install marketing-os@aiherway
/plugin install sales-os@aiherway
/plugin install client-delivery-os@aiherway
/plugin install admin-ops-os@aiherway
/plugin install home-os@aiherway
/plugin install optimise@aiherway
```

Start with `foundation` (the shared spine: voice, checks, responsible AI review), then add the departments you actually use. You can install or remove any pack at any time with `/plugin`.

| Pack | What it is |
|---|---|
| `foundation` | The shared spine: brand voice, brand check, voice check, citation check, responsible AI review. |
| `marketing-os` | Your AI marketing department: strategy, campaigns, content, email, social, plus the Content Studio. |
| `sales-os` | Your AI sales department: qualification, fast inbound response, discovery, proposals, objection and pricing coaching, and the follow-up guardian. Honest urgency only. |
| `client-delivery-os` | Your AI client delivery department: onboarding, expectations, status on cadence, scope defended kindly, hard conversations, surprise and delight, case studies, and endings worth referring. |
| `admin-ops-os` | Your AI operations department: inbox, calendar, meetings, tasks, SOPs, travel. |
| `home-os` | The operating system for real life: family calendar, meals, chores, school comms. |
| `optimise` | Tune-up tools: Skills Health Check, Tool Stack Audit, Hub Gap-Finder & Sync. |

New departments join this list on their release month. Once you have added the marketplace, they will simply appear.

## Getting updates

Updates flow automatically if you turn on auto-update in `/plugin` (Marketplaces tab). Or pull them whenever you like:

```
/plugin marketplace update aiherway
```

## Make it yours

These skills are generic by design: they read who you are, your voice, your audience, and your rules from your own context files (`memory/business-context.md` and friends) at runtime. Until you set that up, they run on sensible defaults, not on you. Three ways to make them yours:

1. **Ask your AI to do it** (fastest): once a pack is installed, paste the prompt at the top of this page. Your AI interviews you (or uses what it already knows about you from past work) and writes your `memory/business-context.md`. One conversation, and every department reads it.
2. **The OS Builder** (most guided): [ai-os-builder.vercel.app](https://ai-os-builder.vercel.app) interviews you and generates your personalised Foundation: your AGENT.md brain file, voice rules, governance, and memory files. The skills here then read them automatically.
3. **By hand:** create `memory/business-context.md` describing your business, audience, offers, and voice. The skills will tell you anything else they need.

Whichever you choose, do it once. It is the difference between generic output and output that sounds and decides like you.

**Where to work: your AI-HQ folder.** Skills look for `memory/business-context.md` relative to where you are working. Open your AI-HQ (or the department folder inside it) as your working folder in Claude Code or Cowork, and every skill reads your files. This also means it does not matter whether a skill runs from this plugin or from a downloaded copy: no skill holds your data any more. Your context lives in exactly one place, your `memory/` folder, and whichever copy runs reads it. If a skill cannot find your memory files, it will ask rather than guess.

## The rules these skills live by

Everything here follows the AI Her Way EquiAI standard:

- **Human in the loop.** Anything that publishes, sends, or spends is drafted for your approval. Never automatic.
- **Never fabricate.** No invented statistics, testimonials, or urgency.
- **Your data stays yours.** Skills run in your own AI workspace with your own accounts. We store nothing.
- **Evidence-based.** Every skill cites the research or framework it is built on.

## Where everything else lives

- **The Hub and tool pages:** [os.aiherway.com.au](https://os.aiherway.com.au)
- **The OS Builder (personalised setup):** [ai-os-builder.vercel.app](https://ai-os-builder.vercel.app)
- **Membership and curriculum:** [aiherway.com.au](https://aiherway.com.au)

Prefer plain downloads? Every pack is also available as `.skill` file downloads from the Hub, if you would rather not subscribe. Subscribing is simply the version that keeps itself current.

## Questions or stuck?

Post in the Hub community first; that is where answers live and where others learn from your question. If it is urgent or a tech issue, email [hello@aiherway.com.au](mailto:hello@aiherway.com.au). If a skill misbehaves, run the Skills Health Check from the `optimise` pack; it usually finds the cause.

---

This repository is assembled automatically from our canonical templates. Please do not edit files here directly; changes land via the AI Her Way build pipeline.
