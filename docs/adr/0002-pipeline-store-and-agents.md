# ADR-0002: Fixed pipeline, single SQLite store, tiered development agents

Status: accepted

## Context
The project mixes fetching, scoring, LLM calls, DB writes and state mutation in one "agent" class, persists to two DBs plus `state.json`, and grows an unbounded summary into every prompt. The goal is also to show agents in the software development lifecycle.

## Decision
**Pipeline.** The data pipeline is a fixed sequence of plain functions (`ingest → relevance → classify → summarize → store`) with I/O injected at the edges, so tests run offline and `--dry-run` writes and spends nothing. It lives in a `deserto/` package with one `python -m deserto` entry point. The word "agent" is reserved for the development agents below.

**Store.** SQLite is the only persistence layer. Seen-items use the `source_id` unique index. Summaries are derived from events, with a bounded prompt context. DB files are not tracked in git; a small fixture dataset is.

**Development agents.** Finder, Implementer, Reviewer and Scribe run on GitHub Actions. Discovery proposes sources through a PR and is always human-reviewed, because it works from untrusted web content.

**Merge tiers for agent PRs.**
- Tier 0 (auto-merge): docs, summaries, lint fixes, dead-code deletion, patch-level dependency bumps. Needs CI green, Reviewer approval, under about 100 changed lines, an allowed path.
- Tier 1 (human merge): pipeline, backend, endpoint, UI, schema and prompt changes.
- Tier 2 (agents never touch): CI workflows, agent definitions and permissions, secrets and config, branch protection, the source registry.

**Rails, in place before the first agent PR.** Branch protection with required checks, CODEOWNERS and path allowlists, diff-size cap, `AGENTS_ENABLED` kill switch, per-agent monthly spend cap, append-only action log, agents cannot edit their own workflows. A human promotes `agent-found` to `agent-ready` except for Tier 0 categories.

## Consequences
Step 0 is a behavior-preserving restructure: no scoring or prompt changes until Step 2, so the eval set has a baseline. Tier 1 autonomy opens only once the eval set and tests exist.
