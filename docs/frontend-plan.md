# Frontend plan (v1)

Stack: Flask, Leaflet, vanilla JS. Pin markers, no GeoJSON boundaries, no build step.
Out of scope: see `docs/scope.md`.

## Goal
A map where each region shows its recent events. Users filter by topic and signal type, and each event links to its source.

## Today
- One `templates/index.html` with inline JS and 6 hard-coded markers using old continent names.
- Hover calls `/region/<region>`, which returns only the latest event by exact region match.
- A parent region such as `africa` returns nothing for events stored under a leaf.
- A 404 renders "undefined". No styling, topic, or source link.

## Steps
Each step is one issue and one PR. Step 1 comes first, the rest follow in order.

1. **API: hierarchical region queries.** `GET /api/events` (region, topic, signal_type, limit) and `GET /api/regions` (counts). Parents include their leaves via `eval/taxonomy.py`. Keep `/region/<region>`. Add tests.
2. **Split the frontend.** Move JS and CSS to `static/`. No build step.
3. **Region pins.** Pins for the ADR-0004 parents and leaves, loaded from `/api/regions`. Size or colour by event count.
4. **Detail panel.** Click a pin to list recent events with title, summary, topic, signal badge, date and source link. Loading, empty and error states.
5. **Filters.** Topic and signal-type controls that refetch and update pin counts.
6. **Polish.** Responsive layout, accessibility, legend.
7. **Docs.** Frontend section in `DEVGUIDE.md`.

## Rules for agent PRs
- CI stays green and the eval score does not drop. The work should not touch `deserto/classify` or `eval/`.
- Visual steps: run the app and screenshot it before opening the PR.
- A human promotes each issue to `agent-ready` before the Implementer starts (ADR-0002).
