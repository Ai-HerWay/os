# The AI Her Way OS

Your AI business departments, delivered as plugins that stay current.

This is the official plugin marketplace for the [AI Her Way](https://aiherway.com.au) AI Operating System. Add it once, install the departments you run, and every improvement we ship arrives automatically. No re-downloading, no stale files.

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
/plugin install admin-ops-os@aiherway
/plugin install home-os@aiherway
/plugin install optimise@aiherway
```

Start with `foundation` (the shared spine: voice, checks, responsible AI review), then add the departments you actually use. You can install or remove any pack at any time with `/plugin`.

| Pack | What it is |
|---|---|
| `foundation` | The shared spine: brand voice, brand check, voice check, citation check, responsible AI review. |
| `marketing-os` | Your AI marketing department: strategy, campaigns, content, email, social. |
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

These skills are generic by design: they read who you are, your voice, your audience, and your rules from your own context files (`memory/business-context.md` and friends) at runtime. Two ways to set that up:

1. **The OS Builder** (recommended): [ai-os-builder.vercel.app](https://ai-os-builder.vercel.app) interviews you and generates your personalised Foundation: your AGENT.md brain file, voice rules, governance, and memory files. The skills here then read them automatically.
2. **By hand:** create `memory/business-context.md` describing your business, audience, offers, and voice. The skills will tell you anything else they need.

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

---

This repository is assembled automatically from our canonical templates. Please do not edit files here directly; changes land via the AI Her Way build pipeline.

## Questions or stuck?

Email [nici@aiherway.com.au](mailto:nici@aiherway.com.au) or ask in the Hub community. If a skill misbehaves, run the Skills Health Check from the `optimise` pack; it usually finds the cause.
