# Historical baseline: aggregator observations

Source: `corpus/evidence/baseline-r10-20261015T2231Z.json`.

- Source artifact SHA-256: `0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478`
- Baseline header `census_sha256` (line 2): `d7710981aa1c7571ff9d6fd7f75822811173010e5f4e298ac3c47fab274a0b20` (the header calls this informational).
- Pinned timestamp (line 3): `2026-10-15T22:26:29Z`.

Exactly two requested observation rows are present (source lines 26–27):

```text
26:FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=aggregator-r10 age_s=<V> threshold_s=7200 reg=<V> disp=<V> run=<V> settle=<V> ts=<V> script_sha256=<V>
27:FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=aggregator-r10-resume age_s=<V> threshold_s=7200 reg=<V> disp=<V> run=<V> settle=<V> ts=<V> script_sha256=<V>
```

Count is 2 matching observations: one for each identity above. Both are `WAVE_UNSETTLED_AGE` warnings with a recorded threshold of 7200 seconds. The exact age, row timestamp, registration/disposition/run/settlement values, and script hash are masked as `<V>` in these baseline rows; no numeric age or those underlying provenance values can be recovered from this file. This is the count within the requested pair, not a count of all waves. No live census was run.
