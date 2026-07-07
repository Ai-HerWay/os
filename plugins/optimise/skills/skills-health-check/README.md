# Skills Health Check

Audit, clean and map your Claude skill library against one standard.

## Install
1. Save the `.skill` file when prompted, or drop this folder into your skills directory
   (`.claude/skills/` for Claude Code, or install via Cowork).
2. In a new chat, say: **"audit my skills"** and point it at your skills folder.

## What it does
- Scores every skill on **hygiene** (will Claude obey it) and **EquiAI** (is it safe and yours).
- Finds skills that **compete for the same prompt** (the main reason Claude picks the wrong one).
- Suggests fixes you **approve one at a time** before anything is written. Backups are kept.
- Builds an interactive **network map** of how your whole library connects.

## Run the engine directly (optional)
```
python3 scripts/audit_skills.py  <your_skills_folder>  --out skills_data.json
python3 scripts/build_dashboard.py  skills_data.json  --out Skill_Map.html
```
Open `Skill_Map.html` in any browser. No internet needed.

## What's inside
- `SKILL.md`: the health-check workflow Claude follows.
- `reference/global-standard.md`: the full bar: hygiene + the eight EquiAI pillars.
- `reference/equiai-scorecard.md`: each safety pillar with the exact line to add when missing.
- `scripts/audit_skills.py`: the scanner and scorer.
- `scripts/build_dashboard.py`: the map and dashboard builder.

Plain markdown and Python. You own all of it. No lock-in.
