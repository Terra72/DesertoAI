---
name: summarizer
description: Maintain the weekly summary of changes to the DesertoAI project. Use whenever the user asks for a weekly summary, status update, "what changed this week", changelog, or progress recap, or asks to update or refresh the weekly summary. Writes a short summary file only if the project actually changed that week.
---

# Weekly summarizer

Keep one short summary file per week in `summaries/`, named by ISO week: `summaries/YYYY-Www.md` (e.g. `summaries/2026-W42.md`). Weeks run Monday to Sunday.

## Steps

1. **Find the week's changes.** Use git, not memory:
   `git log --since="<Monday>" --until="<next Monday>" --no-merges --pretty="%h %s" --all`
   and `git diff --stat` over the same range if the subjects are unclear.
   Also check `issues/ISSUES.md` for items added or closed this week.
2. **Decide whether to write anything.** If there are no commits in the week and no issue changes, stop. Do not create or edit a file, and tell the user there were no changes. A summary of nothing is noise and hides weeks that mattered.
   Ignore changes that don't affect the project itself: the summary files, `__pycache__`, `.venv`, and database files.
3. **If the file for that week exists, update it** rather than creating a second one, so re-running stays idempotent. Replace its content with the current state of the week.
4. **Write the summary** in the format below.

## Format

Use exactly this template. Omit any section that has no entries.

```markdown
# Week YYYY-Www (Mon DD Mon – Sun DD Mon)
- <weekly title>
- <weekly random quote from Art of War>
## Done
- <what changed, one line, plain words> (<short hash or PR #>)

## Open
- <issue or follow-up still outstanding>

## Notes
- <only if a decision or risk the team must know about>
```

## Style rules
- Weekly title may ignore other style rules mentioned and be a line describing a random animal completing an inspiring action (e.g. The mother lion protects her cubs against the storm)
- One line per item. Say what changed and why it matters, not how it was coded.
- Group related commits into a single bullet; don't list every commit.
- Plain words. No adjectives like "significant" or "robust", no intro, no closing remarks.
- Name features and files as they appear in the repo (e.g. region map endpoint, `ISSUES.md`).
- Stay under about 15 lines total. If it's longer, merge or cut the least important items.
- Don't invent. Every line must trace to a commit.
