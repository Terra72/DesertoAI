# Issues

Backlog of known issues and ideas. Not yet used for agent tasks; later each entry can be turned into one.

## How to add an issue

Copy the template below, give it the next ID, and append it under **Open**.

```markdown
### ISSUE-000: Short title
- **Status:** new | defined | in-progress | closed
- **Area:** ingest | analyze | db | agent | trigger | memory | ui | other
- **Priority:** low | medium | high
- **Description:** What is wrong or needed.
- **Acceptance criteria:**
  - [ ] Criterion
- **Notes:** Links, files, context.
```

### Status meanings

- **new:** created but not ready to be worked on; needs more info.
- **defined:** sufficiently detailed and available for work.
- **in-progress:** being worked on.
- **closed:** done or dropped.

## new

### ISSUE-001: Region Semantics Correction
- **Status:** new
- **Area:** ui/ingest
- **Priority:** medium
- **Description:** events seem to be missclassified to incorrect regions, some regions are lacking information as well
- **Acceptance criteria:**
  - [ ] Correctly classify every article to the actual geographic location grouping. 
  - [ ] Require every event to have a region assigned
- **Notes:** This needs some planning and adjustment to the approach.

## Closed

_None yet._
