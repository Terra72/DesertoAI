---
name: ui-issue
description: Create a GitHub issue for a basic UI task that the weekly UI agent can pick up. Use whenever the user asks to create, file or log a UI issue or UI task, or a small frontend change in templates/ or static/.
---

# UI issue

Files a UI issue with the `agent-ui` label, which the weekly agent (`.github/workflows/weekly-ui-agent.yml`) picks up.

## Steps

1. Check the task is small and self-contained, and only touches `templates/` or `static/` (plus tests). If not, create a normal issue without the label and tell the user why.
2. Write the body with the same sections as `.github/ISSUE_TEMPLATE/ui-task.yml`: **What should change**, **Done when** (checkable criteria), **Files or hints**.
3. Create it:
   `gh issue create --label agent-ui --title "<short title>" --body "<body>"`
4. Report the issue number and URL.
