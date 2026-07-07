# Hub Gap-Finder & Sync

Compare your AI skill library against the AI for Impact Hub catalogue: find the skills worth adding, sync the newer Hub versions into the ones you already have (without losing your customisations), and keep your own custom skills as your own.

## Install
1. Save the `.skill` file when prompted, or drop this folder into your skills directory
   (`.claude/skills/` for Claude Code, or install via Cowork).
2. In a new chat, say: **"compare my skills to the Hub"** or **"what am I missing"**. It reads your library, fetches the current Hub catalogue, and builds your report.

## What it does
- **Reads** your installed skills (the folder you point it at).
- **Fetches** the current Hub catalogue and compares.
- **Sorts** everything into: up to date, update available, gap to add, and your own custom skills.
- **Adds or syncs** with your approval and a backup, one file at a time. Syncing merges the Hub improvement in and keeps your customisations. It never overwrites your work.
- Builds an interactive **gap report** you open in any browser.

## Run the engine directly (optional)
The skill writes a `hub_gap_report.json`, then renders it:
```
python3 scripts/build_dashboard.py hub_gap_report.json --out Hub_Gap_Report.html
```

## What's inside
- `SKILL.md`: the gap-find-and-sync workflow Claude follows.
- `reference/matching-method.md`: how it matches your skills to the catalogue and tells a custom skill apart from a gap.
- `reference/sync-guidance.md`: how it brings a newer Hub version in without losing your customisations.
- `reference/hub-catalogue.json`: a bundled snapshot of the Hub catalogue, used only if the live fetch fails.
- `scripts/build_dashboard.py`: turns the report into the interactive dashboard.

## How it stays current
It fetches the live Hub catalogue (`ai-os-builder.vercel.app/templates/LIBRARY.json`) each run, so it compares against the Hub as it is now. The bundled snapshot is a fallback for when you are offline, and the report tells you which source was used.

Plain markdown and Python. Approval-gated, nothing uploaded. You own all of it. No lock-in.
