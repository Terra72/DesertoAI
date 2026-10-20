# Eval set

Hand-labelled articles used to measure classification accuracy (ADR-0001 acceptance bar: 85% region, 80% topic, 100% of events have a region).

**Labels are written by a human, never by the classifier.** This directory is a protected path: agents do not edit it and changes are human-merge only (ADR-0003).

## Files
- `candidates.jsonl`: unlabelled articles pulled from the feeds. Pick from these or add your own.
- `eval_set.jsonl`: the labelled set, about 40 rows. One JSON object per line:

```json
{"id": "abc123", "title": "...", "summary": "...", "source": "...", "link": "...", "region": "sahel-west-africa", "topic": "fmnr"}
```

## Allowed values
`region` (ADR-0001): `sahel-west-africa`, `horn-east-africa`, `southern-africa`, `mediterranean-southern-europe`, `mena`, `central-asia`, `south-east-asia`, `australia`, `americas-drylands`, `global`, `multi-region`.

`topic`: `fmnr`, `agroforestry`, `water`, `soil`, `policy`, `funding`, `technology`, `ecosystem`.

Aim for coverage: several rows per region, and some genuinely `global` and `multi-region` rows. Include a few irrelevant articles with `"relevant": false` and no region/topic, so relevance can be measured too.
