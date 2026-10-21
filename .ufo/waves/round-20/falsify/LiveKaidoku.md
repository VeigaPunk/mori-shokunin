# LiveKaidoku: C2 falsification, per-seat settlement accuracy on kaidoku-shokunin

**Verdict: HOLDS.** The live scan agrees with the wave-1 ground truth (`GtLaneKaidoku.md`) and with the committed fleet totals on every per-dispatch-file field (members, present, missing, misrooted, stub, state) and on all 135 missing names. An independent recomputation agrees on every member. There are **zero differences**, so there is nothing to explain as live lane change or tool error. The lane has not changed since either snapshot. No tool defect was reproduced on this lane. Four tool-level observations (T1-T4) are recorded in section 7, and none is triggered here.

Scope: read-only on kaidoku-shokunin, sibling lanes and the fleet. Scratch output only under `falsify/LiveKaidoku/`. No subagents. No installs or updates (python3 stdlib and `/usr/bin/jq` jq-1.8.2 only).

## 1. Scan run

```
python3 mori-shokunin/tools/mori-wave-settlement.py scan --lane-root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --fleet-root /home/vgpnk/Projects/shokunin --out .../falsify/LiveKaidoku/scan.json
exit 1  (by design: tools/mori-wave-settlement.py:363, because 7 waves are partial)
stdout bytes == --out bytes
sha256(scan.json) = b1302535c14a34c1c146d023cef7c9112dde9df415ff9b11a3ef676ffc10276b
second run to /tmp: exit 1, cmp identical (contract.md:85-86 byte-identical requirement holds)
```

## 2. Per-dispatch-file comparison

Tool = live scan. Mine = independent recomputation (`falsify/LiveKaidoku/compare.py`). GT = `GtLaneKaidoku.md` §2 and §6. All three agree on every row.

| # | Dispatch file (lane-relative) | Members | Present | Missing | Misrooted | Stub | State | Missing names vs GT §6 |
|---|---|---:|---:|---:|---:|---:|---|---|
| 1 | round-14/dispatch.json | 32 | 32 | 0 | 0 | 0 | settled | match |
| 2 | round-15/dispatch.json | 32 | 32 | 0 | 0 | 0 | settled | match |
| 3 | round-16/wave1-dispatch.json | 64 | 36 | 28 | 0 | 0 | partial | match (28) |
| 4 | round-16/wave2-dispatch.json | 32 | 32 | 0 | 0 | 0 | settled | match |
| 5 | round-17/wave1-dispatch.json | 78 | 78 | 0 | 0 | 0 | settled | match |
| 6 | round-17/wave2-dispatch.json | 69 | 67 | 2 | 0 | 0 | partial | match (2) |
| 7 | round-18/wave1-dispatch.json | 89 | 89 | 0 | 0 | 0 | settled | match |
| 8 | round-18/wave2-dispatch.json | 98 | 94 | 4 | 0 | 0 | partial | match (4) |
| 9 | round-19/wave1-dispatch.json | 90 | 48 | 42 | 0 | 0 | partial | match (42) |
| 10 | round-19/wave2-dispatch.json | 72 | 72 | 0 | 0 | 0 | settled | match |
| 11 | round-20/wave1-dispatch.json | 100 | 98 | 2 | 0 | 0 | partial | match (2) |
| 12 | round-20/wave2-dispatch.json | 71 | 71 | 0 | 0 | 0 | settled | match |
| 13 | round-21/wave1-dispatch.json | 64 | 26 | 38 | 0 | 0 | partial | match (38) |
| 14 | round-21/wave2-dispatch.json | 68 | 49 | 19 | 0 | 0 | partial | match (19) |
| | **Total** | **959** | **824** | **135** | **0** | **0** | 7 settled, 7 partial | 135/135 |

Empty, unparsed and unsafe are 0 in every row. GT's table has no stub column, so GT stub is "not reported". Stub is 0 in the tool and in the recomputation.

## 3. Totals against GT and the committed fleet snapshot

| Quantity | Tool scan | Recomputation | GT | Fleet `c2-live-fleet.json:259-271` |
|---|---:|---:|---:|---:|
| waves | 14 | 14 | 14 | 14 |
| members | 959 | 959 | 959 | 959 |
| present | 824 | 824 | 824 | 824 |
| missing | 135 | 135 | 135 | 135 |
| misrooted | 0 | 0 | 0 | 0 |
| ignored_json | 3358 | 3358 | 3358 | not in entry |
| unreadable_json | 39 | 39 | 39 | 39 |
| exit | 1 | 1 | not stated | 1 |

The fleet entry (`c2-live-fleet.json:259-271`) carries kaidoku totals only: no per-wave data, no stub, no states and no ignored_json. A per-file comparison against it is therefore impossible, and I compared totals only.

## 4. Differences

None. Member-level diffs (tool vs recomputation): 0. Field diffs: 0. GT diffs, including missing-name lists: 0. Fleet diffs: 0. No explanation is required.

## 5. Live-change evidence (mtimes, local -0300)

- GT file `GtLaneKaidoku.md`: 2026-10-21 07:37:32.200. Fleet `c2-live-fleet.json`: 07:46:53.060. `scan.json`: 08:00:28.370. [INFERENCE] The GT start time is not recorded, so file mtimes are the only bound on the change window.
- Walk of `.ufo/waves` (21,284 entries, no symlink following): **0 entries newer than 07:37:32.200**. `.ufo/waves` directory mtime 05:07:07.462. Latest dispatch files: round-21/wave2 05:53:14.384 and round-21/wave1 05:25:24.818.
- All 14 report directories are older than the GT snapshot. All 824 present reports are older than the snapshot and newer than their own dispatch file (`PRESENT_REPORTS_OLDER_THAN_DISPATCH: 0`).
- Dispatch file sha256 matches the scan recorded hash in 14/14 cases.
- Round-21 spawn records, checked against GT §5: `round-21/wave1-dispatch-attempts.json` 05:25:59 (first start refused, "Background job limit reached (100)"); `wave1-registration-recovery.json` 05:38:59 ("Spawned 64 background agents..."); `wave2-attempts.json` 06:01:05 (second attempt "Spawned 68 background agents...").

## 6. Adversarial checks (all negative)

a. **Discovery bypass.** A raw-bytes search of all 3,411 `.json` files under `.ufo/waves` for `ufo-swarm-wave-dispatch-v1` returns exactly the tool's 14 files. None of the 39 unreadable files contains the schema string. Identity: 14 + 3358 + 39 = 3411.

b. **Trailer rule.** Each of 959 tasks has exactly one trailer line, and it is the final line. The GT rule (final segment) and the tool's R1 (`tools/mori-wave-settlement.py:208-211`) agree on 959/959.

c. **Present vs stub.** The 824 present reports have a minimum size of 1,738 bytes and a maximum of 56,189. None is under 200 bytes. None contains "STATUS" in its first 64 bytes. The R2 stub class (`:226-228`) has no effect here.

d. **Paths and duplicates.** 959 trailers, 959 distinct paths. Each wave maps to exactly one report directory, and the 14 directories map one-to-one to the 14 dispatch files. R4 and R5 are 0. Every member name equals its trailer file stem (959/959).

e. **Symlinks.** There are 11 symlink entries under `.ufo/waves`. None is JSON-named and none sits in a report directory. 0 members resolve through a symlink.

f. **Member list.** `taskCall` keys are exactly {context, tasks}. No other non-empty list exists in any dispatch file. In 14/14 files, `counts.total` = `counts.spawn` = member count and `counts.resume` = 0. `resumeSends` is an empty array in 14/14 files.

g. **Misrooted.** The fleet-root check finds 0. A bounded lstat of the 135 missing relative paths under 20 sibling lanes (named paths only, no search) finds one hit: `souji-shokunin/.ufo/waves/round-16/w1/SiblingOverlap.md` (11,446 bytes, mtime 2026-10-20 11:24:10). That file is souji's own. Souji's `round-16/w1-dispatch.json` lists SiblingOverlap as its member with that exact trailer (line 771; that dispatch file's mtime is 11:19). It is not a kaidoku misroute, and the kaidoku member is correctly `missing`.

h. **Cross-wave basenames.** Ten exact-basename files in other kaidoku waves match six missing members (the GT §4.6 set). Each file is trailer-owned by a present member of its own wave. Each was written after its own dispatch, and each header names its own round or topic: `round-14/w1/SiblingOverlap.md` "Round 14"; `round-18/w1/SentinelSandbox.md` "round 18, w1"; `round-20/w1/ReviewSkillRegistry.md` "round 20". No wrong-wave misfile was found.

i. **Recovery-suffix names.** No entry in the 14 report directories contains "-2". The 25 substring hits are different seat names, for example `ClaimSeparation.md`.

j. **Subdirectories of report directories.** Five exist: `round-17/w2/predict-java-diff`, `round-17/w2/temporal-attack`, `round-19/w1/patches`, `round-19/w1/inherited` and `round-20/w1/patches`. Six `.patch` artifacts share stems with missing members (VerifyR19; ValidatorDigestGuard, CitationDriftAliases, JjRedBeforeSafety, ProvincePinsTool, HeadRevLintNested). None is the expected `.md` report, so each stays `missing` under the contract.

## 7. Tool observations (none triggered on kaidoku)

- **T1. Silent drops in discovery.** `tools/mori-wave-settlement.py:108-111` skips JSON-named entries whose lstat fails with a non-ENOENT error. `:117` collects only regular files, so a JSON symlink is counted in neither `ignored_json` nor `unreadable_json`. The contract's accounting (`contract.md:64-67`) implies every JSON file is counted. Kaidoku: `not_regular` = 0.
- **T2. Errors reported as missing.** `:191-192` returns `unavailable` on any non-ENOENT OSError, and `:199-200` returns `other` for a non-regular leaf. Both reach `_member_status` (`:221-234`) and come out as `missing` (`:234`), with no error signal. A permission-denied report reads as "missing". Kaidoku: 0 such errors.
- **T3. Frozen-text deviations.** Contract wording at `contract.md:70-73` ("the LAST line of a task matching ...") is ambiguous. GT reads it as the final line. Tool R1 (`:208-211`) reads it as the last matching line. R2 (`:226-228`) adds a `stub` class: a 16-byte `STATUS: started` file is not `present`, while `contract.md:74-75` defines present as a regular non-symlink file with size > 0. Both are disclosed at `:5-16` as co-evolved after dispatch. Kaidoku: 0 trailer disagreements and 0 stubs.
- **T4. Sibling-lane writes are out of scope.** `misrooted` checks only `--fleet-root` (`:230-233`), as the contract specifies (`contract.md:74-77`). A same-path file in a sibling lane is therefore never flagged. This is correct here (item 6g).
- Exit 1 is the designed "not all settled" signal (`:363`), not a failure.

## 8. GT observations (no tool error)

- G1. GT §2 (line 38) says `resumeSends` is 0. It is `[]` in 14/14 files. This is a wording slip with no effect on counts.
- G2. GT §4.7 (line 70) checks the report directory only, not subdirectories. Item 6j is the gap; under the contract it does not change any classification.
- G3. GT §4.8 (line 71) counts 70 regular files, including the 14 `swarm-registry.json` files. The five directory entries (item 6j) are not counted. Consistent as stated.
- G4. GT §5 round-21 claims and GT §4.6 cross-wave claims were verified (sections 5 and 6h).

## 9. Residual risk

- Presence is shape-only, as the contract defines it. Content substance is not verified. Section 6c covers only stub-like heads.
- `missing` is not "never spawned" and is not "dead". Wave 1 has 38 missing seats after a recovery spawn of 64 recorded at 05:38:59. Wave 2 has 19 missing after a spawn of 68 at about 06:01. The tool does not read the attempts records. [INFERENCE] Some of these seats may still be running or may have failed silently. The lane shows no writes since 07:37:32.
- Not run: `--selftest`, the census, and any scan of other lanes. The R1-R5 wording in the round lesson was not reviewed, since it is outside kaidoku scope.

## Artifacts (scratch)

- `falsify/LiveKaidoku/scan.json` (tool output, sha256 b1302535...276)
- `falsify/LiveKaidoku/compare.py` → `compare.json` (independent recomputation, member-level)
- `falsify/LiveKaidoku/extra.py` (second pass: present-report sizes and heads, report-directory ownership, sibling-lane lstat, orphans)
- `falsify/LiveKaidoku/verify2.py` (raw-bytes discovery bypass test, live-change sweep, sha256 check)
- `/tmp/LiveKaidoku-scan-run2.json` and `/tmp/LiveKaidoku-stdout-run2.json` (determinism run)
