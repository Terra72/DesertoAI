# ADR-0003: Project goals, quality gates and failure policy

Status: accepted

## Context
ADR-0001 and ADR-0002 define the taxonomy, pipeline and agent tiers but not the project's goal, plan order or stop conditions. A grilling session settled them.

## Decision
**Goal.** DesertoAI is a showcase of agents in the software development lifecycle, using a desertification tracker as the workload. Done means the Step 2 bar from ADR-0001 is met and one full Finder → Implementer → Reviewer → merge loop has run with the ADR-0002 rails on.

**Plan order.** Step 0 restructure (no behaviour change), Step 1 offline tests and the eval set, Step 2 LLM classifier against the eval set, Step 3 `sources.yaml`. Agents start on Tier 0 once the rails exist. Tier 1 autonomy opens after the eval set and tests exist. Discovery is built last.

**Quality gates.**
- The eval set is hand-labelled by a human, never by the classifier. It is a protected path: agents cannot edit it and changes are human-merge only.
- Once Step 2 lands, the eval score is a required, non-regressing CI check on Tier 1 PRs.
- The UI and endpoints are frozen (read-only view of the store) until Step 2 is done. After that they are Tier 1 work.

**Models.** Haiku 5.5 for relevance, classify and summarize. Sonnet 5.5 for the agents. Model IDs live in `config.py`, not in code.

**Runtime.** The pipeline runs daily on GitHub Actions and publishes the SQLite DB as an artifact or release asset. The app runs locally from that DB. Hosting is out of scope. A fixture dataset in git keeps tests and demos working offline. Budget is about $5 per agent per month.

**Failure policy.** A failed item (feed down, LLM error, malformed output) is skipped and logged. No invented region, no fallback to `global`. If more than 20% of items fail in a run, the run goes red and opens a Finder issue.

**Discovery exception.** ADR-0002 puts `sources.yaml` in Tier 2. Discovery may open PRs against it but never merge them. This is the only agent exception to Tier 2, and it is for proposing only.

**Measurement.** The Scribe reports weekly in `summaries/`: PRs opened, merged, rejected and reverted by tier, spend against cap, and eval score over time. Two reverted Tier 0 PRs in a month turn Tier 0 auto-merge off until a human re-enables it.

## Consequences
Out-of-scope items are listed in `docs/scope.md`, and the Finder must not file them as `agent-found`. Changing a gate or the failure policy needs a new ADR.
