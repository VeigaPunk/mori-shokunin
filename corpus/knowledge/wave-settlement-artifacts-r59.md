source: S553 — committed wave-results artifact `.ufo/waves/round-54/w1-results.json` (own-work copy `corpus/evidence/sources-r59/w1-results-r54.json`, opened 2026-10-28)
source: S554 — `.ufo/waves/round-55/w1-results.json` (copy `corpus/evidence/sources-r59/w1-results-r55.json`, opened 2026-10-28)
source: S555 — `.ufo/waves/round-56/w1-results.json` (copy `corpus/evidence/sources-r59/w1-results-r56.json`, opened 2026-10-28)
source: S556 — `.ufo/waves/round-57/w1-results.json` (copy `corpus/evidence/sources-r59/w1-results-r57.json`, opened 2026-10-28)
source: S557 — `.ufo/waves/round-58/w1-results.json` (copy `corpus/evidence/sources-r59/w1-results-r58.json`, opened 2026-10-28)
source: S558 — `.ufo/waves/round-58/evidence/w1-settlement.json` (copy `corpus/evidence/sources-r59/w1-settlement-r58.json`, opened 2026-10-28)
source: S559 — `.ufo/waves/round-53/w1-results.json` (copy `corpus/evidence/sources-r59/w1-results-r53.json`, opened 2026-10-28)
verified-at: 2026-10-28 — artifacts re-read from the lane working tree at freeze revision 60b3a76ad0524c8978cc51922940be1c8c388915; copies sha256-verified equal to the committed `.ufo` artifacts (counter arm `tree=ok`)
recheck: `python3 .ufo/waves/round-59/count-c2.py R`
coverage-map: Core — fleet wave-settlement artifacts (FR5-adjacent observability of the inline spawn handoff); deepens the wave-lifecycle surface without advancing frontier

# Wave-settlement result artifacts: recorded shape facts (rounds 53–58)

This entry records byte-located facts about the orchestrator's committed `<wave>-results.json`
settlement artifacts — the file the inline spawn handoff writes beside `<wave>-dispatch.json`
when every seat settles — and about the lane's own `mori-wave-settlement-v1` settlement summary.
They are shape facts of committed artifacts, not settlement semantics: `seats` says how many
seats the file lists, `output` is the captured final seat output, `note` is free-form metadata;
nothing here proves a seat ran, judged, or agreed. The round-53 member `report_file` key is a
writer-version difference (its drift is *recorded*, not repaired).

## Claims

- **K1** — the settlement artifact's `seats` field holds 74 for the round-54 wave. Quote: ` "seats": 74,` (corpus/evidence/sources-r59/w1-results-r54.json:line:5; pin ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f)
- **K2** — the settlement artifact's `seats` field holds 64 for the round-55 wave. Quote: ` "seats": 64,` (corpus/evidence/sources-r59/w1-results-r55.json:line:5; pin 2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b)
- **K3** — the settlement artifact's `seats` field holds 64 for the round-56 wave. Quote: ` "seats": 64,` (corpus/evidence/sources-r59/w1-results-r56.json:line:5; pin 19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761)
- **K4** — the settlement artifact's `seats` field holds 64 for the round-57 wave. Quote: ` "seats": 64,` (corpus/evidence/sources-r59/w1-results-r57.json:line:5; pin 29e7a35df544315d3bb6ac2f0da96235342d77a1f8306ab25b8a27675669beb1)
- **K5** — the settlement artifact's `seats` field holds 64 for the round-58 wave. Quote: ` "seats": 64,` (corpus/evidence/sources-r59/w1-results-r58.json:line:5; pin a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc)
- **K6** — every member entry carries a `note` field and it is null in r58's first member. Quote: `   "note": null` (corpus/evidence/sources-r59/w1-results-r58.json:line:11; pin a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc)
- **K7** — every member entry carries a `note` field and it is null in r57's first member. Quote: `   "note": null` (corpus/evidence/sources-r59/w1-results-r57.json:line:11; pin 29e7a35df544315d3bb6ac2f0da96235342d77a1f8306ab25b8a27675669beb1)
- **K8** — the top-level `lane` field names mori in the round-54 artifact. Quote: ` "lane": "mori",` (corpus/evidence/sources-r59/w1-results-r54.json:line:2; pin ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f)
- **K9** — the top-level `wave` field names w1 in the round-58 artifact. Quote: ` "wave": "w1",` (corpus/evidence/sources-r59/w1-results-r58.json:line:4; pin a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc)
- **K10** — member `agent` carries a taxonomy role name (reviewer) in r58 member[0]. Quote: `   "agent": "reviewer",` (corpus/evidence/sources-r59/w1-results-r58.json:line:9; pin a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc)
- **K11** — the round-53 artifact's member entries carry a report_file field — a key absent from r54-r58 members. Quote: `   "report_file": ".ufo/waves/round-53/w1/Mo53Fr01.md"` (corpus/evidence/sources-r59/w1-results-r53.json:line:16; pin 0d644e0fb9c50101a00f47c4ef95e637bb1b1cf1168b5e49bdd19c2f0e584260)
- **K12** — the settlement scanner's committed summary names schema mori-wave-settlement-v1. Quote: `mori-wave-settlement-v1` (corpus/evidence/sources-r59/w1-settlement-r58.json:offset:89; pin b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588)
- **K13** — the round-58 settlement summary totals record 26 partial waves. Quote: `"partial":26` (corpus/evidence/sources-r59/w1-settlement-r58.json:offset:224; pin b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588)
- **K14** — the round-58 settlement summary totals record 36 settled waves. Quote: `"settled":36` (corpus/evidence/sources-r59/w1-settlement-r58.json:offset:237; pin b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588)

## Limits

K1–K5 and K8–K10 are line-exact observations of committed bytes; `seats`==member count is a
writer invariant this entry does not assert beyond what the frozen counter's scan arm re-derives
(members==seats on the five r54–r58 files). K11's absence claim is bounded to r54–r58 first
members and to the frozen counter's drift arm (r53 fails strict member keys; `report_file` is the
extra key class). K12–K14 quote a lane-written summary (own-work, not orchestrator bytes) and say
only what that summary records. Claims over `output` strings are excluded by design: their JSON
escaping is not byte-stable across quote extraction.
