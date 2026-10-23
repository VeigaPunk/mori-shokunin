measured 2026-10-23T08:52:18Z
# Round 19 capability row — RowR19

VERDICT: supported
ROW: | rounds[398].capabilities_added[0] | Blob-bound content-review gate | Checks 10/10 frozen finite requirements; on the actual 194-path population, it exits 1 with 155 unresolved dispositions and does not certify privacy clearance. | `tools/mori-content-review.py` | 19 |

- The closure report names `tools/mori-content-review.py` as the implementation and says C1 was demonstrated by its CLI selftest and 10/10 match (`.ufo/reports/round-19/mori.md:23-27`).
- The closure report records 10/10 matched at the finite scope and the actual 194-path run as 194/194 blobs and rows, exit 1, 155 unresolved, not clearance (`.ufo/reports/round-19/mori.md:102-118`); the lesson explicitly says this is not a privacy-clearance claim (`corpus/lessons/round-19.md:235-240`).
- The tool binds the population/reviews and revision, reads blob contents, and marks stale or unresolved/provenance-only decisions (`tools/mori-content-review.py:213-240,273-329`). Its synthetic selftest contains ten named requirement cases (`tools/mori-content-review.py:419-429`). This is implementation evidence, not a fresh run.
- Candidate rationale: `tools/mori-content-review.py` directly implements the content-review gate; freeze-order is a distinct C2 tool. Both candidates changed in this closure, exist at closure and lane tip, and are named in the closure report (`.ufo/reports/round-19/mori.md:23-27`; history results below).

## Provenance and command outcomes

- Timestamp command: `date -u +%FT%TZ` → `2026-10-23T08:52:18Z`.
- Initial manifest lookup used the lane repo by mistake: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json | jq '.rounds[398]'` → `fatal: path 'MANIFEST.json' does not exist in '37b51a243302e8009c7067431e8a47f9a722fd14'`. Corrected lookup used the fleet root.
- Corrected command: `git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json | jq '{round: .rounds[398].round, capability: .rounds[398].capabilities_added[0], report: .rounds[398].report, commit: .rounds[398].commit, reviewer: .rounds[398].verification.reviewer, spotcheck: .rounds[398].verification.spotcheck, c1_recheck: (.rounds[398].verification.rechecks | match("Independently derived C1[^.]*\\.").string), actual_population: (.rounds[398].verification.rechecks | match("Actual committed-population receipt[^.]*\\.").string)}'`.
  Output: round 19; capability string exactly as in the row; report `.ufo/reports/round-19/mori.md`; commit `mori-shokunin@2061780117e6ca637725004897bd288d3ba7e988`; reviewer `CloseMori19` with independent read-only reviewers; C1 recheck says 10 cases, exact case-name parity, 10 pass/no issues; actual-population receipt says exit 1, 155 `CONTENT_REVIEW_UNRESOLVED`, red preserved, no privacy-clearance claim. The spotcheck field identifies the durable closure-row check and the round-19 lesson.
- Candidate source reads at the closure commit: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 2061780117e6ca637725004897bd288d3ba7e988:tools/mori-content-review.py` and the same command with `tools/mori-freeze-order.py` returned both source bodies. Read-only source inspection supports the implementation citations above; no tool was executed.
- History check: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --name-status 3786f3f1bde2fbcc5ce617e35e8c9becdbf9d9e8 2061780117e6ca637725004897bd288d3ba7e988 -- tools/mori-content-review.py tools/mori-freeze-order.py` → `A tools/mori-content-review.py`, `M tools/mori-freeze-order.py`. `git rev-parse` for each candidate at closure and HEAD returned identical blob IDs: content-review `b5c42df2b2bf2ce0476b39a03495206541669979`; freeze-order `fcd8a017378c600c5d9a47a9d40a171f3bf135c5`. Lane HEAD observed as `913df22e29f131ef9cb5de9dcb7e3e272256c5f0`.
- Provenance lookup confirmed the lesson blob is unchanged from closure to lane HEAD (`dec2b936bd5a9731a82b9d971d587ec83659fe74`). One attempt also asked the lane repository for its fleet-side report path and got a fatal path-not-found; the corrected fleet-root `git rev-parse` returned the same report blob at MANIFEST revision and fleet HEAD (`909ec09c3b101557f9a4837880cb142ed5de5137`). Thus the cited report lines are from the report named by the MANIFEST closure.

## Behavior, gates, and limits

- Finding: the closure record supports the capability running. The gate's real-population result is deliberately red, not a passing privacy review (`.ufo/reports/round-19/mori.md:115-118`; `corpus/lessons/round-19.md:235-240`).
- Gate work by this scribe: none. I inspected the frozen MANIFEST closure, closure report/lesson and closure-version candidate blobs; I did not rerun the counter, tests, or gate. The quoted 10/10 and 194-path results are closure evidence, not my execution evidence.
- Touched surface: this report only, `.ufo/waves/round-35/w1/RowR19.md`. Product files, MANIFEST, closure records, fleet report, and lane index were read-only.
- Out of scope: no C2 row, no claim of privacy clearance, no reclassification of the 155 unresolved dispositions, and no source or counter changes.
- Tool installs/updates: none. Scratch files: none. Background processes: none.
