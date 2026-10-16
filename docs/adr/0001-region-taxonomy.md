# ADR-0001: Fixed region taxonomy, no "Global" fallback

Status: accepted (starting point, revisable through a new ADR)

## Context
Two competing region methods exist: keyword matching (4 regions) and embedding similarity (6 continents) with a "global" fallback below a score of 0.30. Events are misclassified, some regions lack data, and the fallback hides failures (ISSUE-001).

## Decision
- Every event gets exactly one region from a fixed, desertification-relevant list:
  Sahel and West Africa, Horn and East Africa, Southern Africa, Mediterranean and Southern Europe, MENA, Central Asia, South and East Asia, Australia, Americas drylands, `global`.
- `global` is used only when an item is genuinely global. `multi-region` is allowed only when an item truly spans several regions.
- An LLM classifies the region from this list. Embeddings may remain as a cheap pre-filter. The keyword matcher is deleted once the LLM classifier beats it on the eval set.
- Country and subregion columns are kept so the taxonomy can be refined without a schema change.
- Acceptance (Step 2): at least 85% region accuracy and 80% topic accuracy on the 40-article eval set, and 100% of events have a region.

## Consequences
Changing the list needs a new ADR and a re-run of the eval set. The classifier change is a Tier 1 (human-merged) PR.
