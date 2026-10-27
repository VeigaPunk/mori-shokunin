# Round 57 lesson (L1 MoriR57)

Entering revision `53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`; claim freeze `618562c72a03dc4d17386b715357f863fd327274`. W1 was one v2 wave, 64 seats; results in `.ufo/waves/round-57/w1-results.json`, 64 outputs, 62 report files (Mo57Reviewer15 and Mo57MutationTester37 did not write report files; result outputs exist; no death/error status is available). Counter/control weaknesses found are retained as honest limits; frozen counters and predicates were not changed.

## Gate

### New source rows

| id | URL / source | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S548 | lane-owned `tools/mori-driver-liveness.py`, source copy `corpus/evidence/sources-r57/mori-driver-liveness.py` | 2026-10-27 | `row["open_launches"].append(key)` (`parse_log`:133) | admit, tier A own-work; directly grounds the parser transition cited by the eight claims in `corpus/knowledge/watchdog-unclosed-r57.md` |
| S549 | `../kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md`, source copy `corpus/evidence/sources-r57/kumitate-wave-lifecycle.md` | 2026-10-27 | `settlement is operator-supplied ufo-swarm-results-v1 input to collect.` (source copy:40-41) | reject, tier C; this source describes kumitate result collection, not mori's parser semantics; flip if a future claim is about authoritative settlement ownership rather than `unclosed` parsing |

### Gate decisions and spot-check

Admitted: S548 only. Rejected: S549 for adjacent ownership / wrong surface fit. The source copies are evidence artifacts and their source bytes are read-only. No new source rows other than S548/S549. S548 used-by points only at the new knowledge entry; S549 is unused. Both row changes are new appended rows, not in-place edits.

No non-author admit/reject spot-check was available before filing this lesson. The dispatched seats are the lane, not independent verifiers. The outside review duty remains open; discernment is reported unchanged pending that review.

## Mistakes

| class | evidence pointer | captured-by | fix / shown able to fail |
|---|---|---|---|
| claim-target drift / counter false green | `.ufo/waves/round-57/w1/Mo57Critic31.md`, `Mo57Critic32.md`, `Mo57Executor42.md`, `Mo57MutationTester33.md`; C1/C2 counter implementations in `.ufo/waves/round-57/count-c1.py` and `count-c2.py` | `AXES.md` calibration requirement plus the rule to name the actual target surface before freeze; **none** caught the stale first `## Capabilities` target before data | Frozen C1 targets the first, explicitly superseded `## Capabilities` table (`SCORECARD.md:1951-1961` says the current register supersedes it); the current register lacks the two r56 names. The mutation seats also showed false-green vectors. No post-score correction to predicates or counters is permitted; leave C1 unverified and route the next-round fix to pin the current register/table identity and resolve evidence paths. This fix is not claimed as landed. |
| source quote locator off by one | `verify-c2-source.py` initially returned `C2_SOURCE_CHECK unmet rows=8 mismatches=K3` | manual source-copy cross-check before accepting the entry | Corrected K3 locator from line 117 to line 118; after correction the checker reports `C2_SOURCE_CHECK ok rows=8 mismatches=0` exit 0. Shown able to fail by the initial K3 mismatch and by the mutation probe below. |

`verify-c2-source.py` mutation probe: after copying the pinned source into `/fast/scratch/hyaku/mori-r57/l1-probes/source.py`, deleting source line 118 in that scratch copy yielded `C2_SOURCE_CHECK unmet rows=8 mismatches=K1,K2,K3,K4,K5,K6,K7,K8`, exit 1. Scratch was removed after the probe. This is a deliberately conservative locator check: line shifts make every frozen locator fail, as intended.

## Census

Round-start command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` — output ended `mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`, exit 0; 23 existing W04 duplicate-URL warnings were emitted. The row counting command over the entering revision printed 320:

```sh
git show 618562c72a03dc4d17386b715357f863fd327274:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
```

Round-end command is the same census command; complete captured output and exit code are in `.ufo/waves/round-57/evidence/census-end.txt`: exit 0, with 24 W04 duplicate-URL warnings (the prior 23 plus S546). Row count command on committed working bytes prints 321. S548 and S549 are two appended rows, one admitted and one rejected; no older rows were touched; no frontier path was advanced.

## Assimilation and quarantine

Assimilation: none; no merge package entry was adopted. The S244/S262/S268 quarantine rows were not re-adjudicated this round; prior adjudication remains in `corpus/lessons/round-56.md` and its source trail. `considerthese/2026-10-26.md` was checked: no proposal was implemented; suggestion 2's carry-over ledger remains planned.

## Capability-register correction

The frozen C1 counter selects the first, superseded `## Capabilities` section, not the active register at `SCORECARD.md:1951-1988`; mutation seats proved pointer and duplicate-row false-green cases and the counter cannot be changed after scoring. The round-56 closure is admitted as `MANIFEST.json` rounds[832], with two capability strings. I appended those exact two rows as a current-register continuation at the end of `SCORECARD.md`. The fixed-scope count `grep -cE '^\| `rounds\[832\]\.capabilities_added\[[01]\]` \|' SCORECARD.md` is 0 at entering revision `618562c72a03dc4d17386b715357f863fd327274` and 2 after the continuation; the frozen C1 remains unmet on its false-negative target. It is an observed correction to the register, not a verified C1 verdict.
