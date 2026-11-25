# Glossary

Domain language for DesertoAI. Use these terms in code, issues, PRs and prompts.

**Event**: One news or research item that passed the relevance step, classified and summarized. The unit stored in the database. Not a raw feed entry.

**Item**: A raw feed entry as fetched by ingest, before any filtering. An item becomes an event, or is ignored.

**Source**: A feed we ingest from (RSS URL plus metadata). Listed in the source registry (`sources.yaml`, from Step 3).

**Source registry**: The reviewed list of sources, a file in the repo. Changed only through a PR.

**Relevance**: Whether an item is about desertification, land degradation or dryland restoration. Decided before classification.

**Region**: The single geographic grouping of an event, from the two-level taxonomy in ADR-0001 and ADR-0004 (parent regions such as `africa` and `middle-east` contain leaf regions). Every event has exactly one. `global` is an explicit value for genuinely global items, never a fallback. `multi-region` is allowed only when an item truly spans several.

**Topic**: The theme of an event (e.g. fmnr, agroforestry, water, soil, policy, funding, technology, ecosystem).

**Signal type**: Whether an event is `new` information or a `reinforcement` of what is already known.

**Pipeline**: The fixed sequence `ingest → relevance → classify → summarize → store`. Not agentic.

**Agent**: An autonomous LLM-driven worker with its own trigger and permissions (Finder, Implementer, Reviewer, Scribe, Discovery). The pipeline is not an agent.

**Finder / Implementer / Reviewer / Scribe / Discovery**: The agent roles. See ADR-0002.

**UI agent**: The weekly agent that takes one small UI task (`agent-ui` issue) and opens a PR. It never merges and stays out of protected paths.

**Weekly summary**: A short file recording what changed in the project that week (`summaries/`). Not the global summary of events.

**Global summary**: The running summary of what is known about desertification, updated only when an item brings something new.

**Weekly scrape**: The scheduled run of the pipeline that collects new items and produces an export.

**Export**: The weekly file of events stored by a scrape, committed through a PR. It holds only events not exported before.

**Rollup**: Counting a leaf region's events under its parent region.

**Pin**: The map marker for a region. Selecting it opens the detail panel.

**Detail panel**: The map view of one region's events, opened from a pin.

**Eval set**: The hand-labelled articles (about 40) with expected region and topic, used to measure classification accuracy.

**Tier 0 / 1 / 2**: Merge policy for agent PRs. Tier 0 auto-merges, Tier 1 needs a human merge, Tier 2 is never touched by agents. See ADR-0002.

**Agent-found / agent-ready**: Issue labels. `agent-found` is filed by the Finder (status `new`). A human promotes it to `agent-ready` (status `defined`) before the Implementer may work on it.

**Quality gate**: The required, non-regressing eval-score CI check on Tier 1 PRs, active once Step 2 lands. See ADR-0003.

**Protected path**: A path agents cannot edit and only a human merges, such as the eval set. See ADR-0003.

**Failure policy**: A failed item is skipped and logged, never defaulted. More than 20% failures in a run turns it red. See ADR-0003.
