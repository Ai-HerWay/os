# Sync Guidance: bring a newer Hub version in without losing the student's work

This is the most delicate part of the skill. A member's installed skill is often not the pristine Hub file. They have personalised it: their business-context references, their voice, their thresholds, their added examples, sometimes whole extra sections. The Hub's newer version has improvements they want. Syncing means **merge the improvement in while keeping everything they made theirs.** It never means overwrite.

The failure to avoid: replacing a customised skill with the stock Hub version and silently deleting the member's customisations. That is a data-loss event, exactly the kind we have learned to guard against.

## The rule

Sync is a merge, shown and approved, with a backup. Never a blind replace.

## Before you sync anything

1. **Back up.** Copy the installed file to `SKILL.md.backup` first, every time.
2. **Read both files fully.** The installed (customised) version and the newer Hub version.
3. **Find the customisations.** Anything in the installed file that differs from stock Hub and is clearly the member's: their business name or context-file references, edited thresholds, added rules, extra examples, voice changes, notes. Treat these as precious.
4. **Find the improvement.** What the Hub version actually adds or changes: a better decision rubric, a new section, updated guidance, a fixed instruction, a framework refresh.

## The merge

Produce one merged file that:
- **Keeps every one of the member's customisations** identified above.
- **Brings in the Hub improvement**, adapted to sit alongside their customisations rather than replacing the section they edited.
- **Preserves their context-file references** (never swap `memory/business-context.md` links or their personalised values back to stock placeholders).
- **Flags any genuine conflict** (the member edited the exact thing the Hub also changed) rather than silently picking one. Show both and let the member choose.

## Show, then approve

- Show the merge as a clear before-and-after or a summary of exactly what will change: "brings in X from the Hub, keeps your Y and Z untouched, one conflict for you to decide on."
- Ask: apply this merge?
- On yes: write the merged file (the `.backup` already exists), confirm what changed and what was preserved.
- On no: leave the file exactly as it was.

## When NOT to sync

- If the member's version has diverged so far that it is really a different skill now, do not force the Hub version in. Offer the Hub version as a new, separate skill and let them keep theirs.
- If the only difference is a version number with no meaningful change, say so and skip it. Do not manufacture a reason to write.
- If you cannot confidently identify the customisations, stop and ask the member what they changed, rather than risk overwriting it.

## Adding a gap (the simpler case)

Adding a Hub skill the member does not have is lower risk, but still approval-gated:
- Offer the Hub skill personalised to their context (their business-context references, their voice), not the raw placeholder file.
- Do not overwrite an existing file when adding. If a name would collide, pause and ask.
- Confirm before writing, and confirm what was written after.
