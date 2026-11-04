# ADR-0004: Two-level region taxonomy

Status: accepted. Amends ADR-0001.

## Context
ADR-0001 requires one leaf region per event. Many articles are about a continent as a whole (the Great Green Wall spans the Sahel and the Horn), so forcing a leaf makes the eval label arbitrary and penalises a correct classifier.

## Decision
- Regions are two-level. Parents: `north-america`, `south-america`, `africa`, `north-asia`, `east-asia`, `europe`, `oceania`, `middle-east`. A leaf may sit under more than one parent. Mapping, as in `eval/taxonomy.py`:
  - `africa`: `sahel-west-africa`, `horn-east-africa`, `southern-africa`, `mena`
  - `middle-east`: `mena`
  - `north-america`, `south-america`: both contain `americas-drylands`
  - `north-asia`: `central-asia`; `east-asia`: `south-east-asia`
  - `europe`: `mediterranean-southern-europe`; `oceania`: `australia`
  - `global` and `multi-region` have no parent.
- An eval label may be a parent or a leaf. A prediction is correct if it equals the label, or the label is a parent that contains the prediction. A parent prediction against a leaf label is wrong.
- The classifier still outputs a leaf where the article supports one. It may output a parent only when no sub-region is identifiable. Every event still has exactly one region, and there is still no `global` fallback.
- `mena` is a leaf under both `africa` and `middle-east`, because it covers North Africa and the Middle East.
- Scoring lives in `eval/taxonomy.py` (`region_correct`).

## Consequences
The Step 2 bar (85% region accuracy) is measured with `region_correct`. Changing the parents needs a new ADR.
