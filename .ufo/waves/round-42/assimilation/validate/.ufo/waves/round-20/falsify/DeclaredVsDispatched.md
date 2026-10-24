BROKEN - DeclaredVsDispatched: tool-reported unsettled/partial waves vs spawn records

Verdict: BROKEN. Claim attacked: a member the tool counts `missing` in an unsettled/partial wave is a dispatched seat that spawned and left no report (C2 Problem; lesson M1 framing). In the four named waves, 80 of 89 tool-missing members (89.9%) were never spawned on record (declared-only). Fleet-wide, at least 164 of 708 tool-missing members in the 44 enumerated unsettled/partial waves (23.2%) are declared-only; 360 (50.8%) are unbound inside the read scope. The tool's per-member status reproduces the filesystem at scan time (section 3, item 3).

Snapshots (UTC): kama, kagi, tsukuroi scans 11:04Z; peer scans 11:00Z; mori 10:46Z. Counts move within minutes; see section 5.

## 1. Named waves (spawn evidence read from the named dirs)

| wave (dispatch) | tool state | spawn evidence | verdict |
|---|---|---|---|
| kama round-19/falsify/dispatch.json | unsettled, 0/66 | refused-attempt-1.json 06:39:21Z: seats 66, refused 66, spawned 0, "Background job limit reached (100)". No retry or spawn file in the dir (ls -la). advice/swarm-registry.json: 66 members, agentId null. | NEVER SPAWNED: 66/66 declared-only. No retry through 11:06Z (about 4.5 h). |
| kama round-21/build/dispatch.json | partial, 79/86 at 11:04Z; 80 from 11:05:44Z | dispatch-attempts.txt: attempts 1 to 5 refused 86/86 (10:29Z to 10:41Z); attempt 6 at 10:44:42Z refused 0/86. spawn-result.txt: "Spawned 86 background agents", 86 job lines KamaR21.<name>-6. (GtLaneKama at 10:34Z said unsettled; superseded.) | SPAWNED after 5 refusals. 0 declared-only. The 7 missing: 4 have reports off-path at out/<name>/<name>.md; 1 late; 2 unreported (RegressSkillGates, RevengeSpliceOrigin). |
| kagi round-25/build-dispatch.json | partial, 86/88 at 11:04Z | build-refusals.json: attempt 1 10:32:04Z refused 88, started 0; attempt 2 10:35:04Z refused 0. round-25/build-task-result.txt: "Spawned 88 background agents", 88 job lines KagiR25.<name>-2 (details.progress 88 pending). | SPAWNED after 1 refusal. 0 declared-only. XMeasureC2 landed 11:09Z; XReleaseClock unreported (job listed running in the MoriR20 roster). |
| tsukuroi round-20/build/dispatch.json | partial, 50/64 | native-task-result.json 08:25:44Z: all 64 names "Failed to start ... Background job limit reached"; details.results []. native-task-result-retry-2.json 09:18:02Z: refused-before-spawn, spawned 0. 50 reports written 09:20:36Z to 09:39:04Z; no success record in the dir; no subdirectories. swarm-registry.json 09:23:13Z binds 64 names to TsukuroiR19Recovery.<name>-2, not this wave's jobs. | NEVER SPAWNED ON RECORD: 14 declared-only. The 50 reports are unattributed. [INFERENCE] a partial spawn between 09:18:02Z and 09:20:36Z went unrecorded; not established. |

Decomposition of the 89 tool-missing members: declared-only 80 (89.9%); spawned, unreported 3; report present off-path 4; late 2. Among members with no report anywhere in the named dirs (83), declared-only is 96.4%.

## 2. Fleet population (tool outputs; V = verified in named dirs, S = second-hand, U = unbound)

| lane | waves | missing | declared-only V/S | spawned-no-report V/S | unbound U | state source |
|---|---|---|---|---|---|---|
| kama | 9 | 130 | 66/20 | 7/37 | 0 | scan 11:04Z; S = GtLaneKama s3 |
| kagi | 4 | 15 | 0/0 | 2/13 | 0 | scan 11:04Z; S = GtLaneKagi s4 |
| tsukuroi | 5 | 67 | 14/0 | 0/0 | 53 | scan 11:04Z |
| mori (own lane, unnamed) | 4 | 85 | 0 | 0 | 85 | c2-live-mori 10:46Z |
| kaidoku | 7 | 135 | 0 | 0/61 | 74 | peer scan 11:00Z; S = GtLaneKaidoku s5 |
| mado | 8 | 116 | 0/32 | 0 | 84 | peer scan 11:00Z; S = knowledge s4, GtLaneMado |
| kake | 3 | 64 | 0 | 0 | 64 | peer scan 11:00Z |
| kumitate | 2 | 44 | 0 | 0/44 | 0 | peer scan 11:00Z; S = lane accounting |
| kasegi | 1 | 20 | 0 | 0/20 | 0 | peer scan 11:00Z; S = GtLaneKasegi |
| revenger | 1 | 32 | 0/32 | 0 | 0 | peer scan 11:00Z; S = GtLaneRevenger |
| TOTAL | 44 | 708 | 80 V + 84 S = 164 (23.2%) | 9 V + 175 S = 184 (26.0%) | 360 (50.8%) | |

Not enumerated (no per-wave tool state in reach): chousa 16, kengaku 11, souji 120, tabi 561, tameshi 108 missing (10:46 fleet aggregate, evidence/c2-live-fleet.json). Fleet missing is 1,524 at mixed snapshots; 708 (46%) is enumerated.

Never-(fully)-spawned waves: 5 of 44. Verified: kama r19f; tsukuroi r20b (on record). Second-hand: kama r18 build-95 (20 of 95 never spawned, GtLaneKama); mado dispatch-preview.json and revenger rendered-undispatched.json (never dispatched; revenger's sibling routing-contract.json shows dispatched_lanes 0).

Refused, then spawned: at least 13 waves (2 V: kama r21, kagi r25; 11 S). A refusal record alone does not settle a wave.

Share of missing members that are declared-only: 80/89 = 89.9% in the named set, selected for refusals and not representative. Within the enumerated 708: 164 is a lower bound (23.2%) and 524 an upper bound (74.0%).

## 3. Findings

1. Premise fails. kama r19f was refused in full at 06:39:21Z and never retried, although its retry_policy says retry the same payload. It is the only named refused wave with no later attempt record. The knowledge note s4 already warns that unsettled can be never-spawned; the frozen C2 label does not carry that warning.
2. Tool blind spot. Four of kama r21's seven tool-missing members have reports at out/<name>/<name>.md (AuditErrataMutants 5859 B; AuditRegexMutants 5963 B; LinksGateMutants 4348 B; out/LinksGridMutants-6/LinksGridMutants.md 4429 B). The trailer path advice/<name>.md is absent. misrooted checks only the fleet root, so these count as missing.
3. Counts reproduce at scan time. Filesystem versus tool: 0 disagreements for kama r19f and tsukuroi r20b; 1 each for kama r21 and kagi r25, both files written after the scan.
4. counts.spawn is a plan. kama r19f: counts.spawn 66, spawned 0. kama r21's registry binds 86 names to KamaR21.<name>-6, matching the spawn text. tsukuroi r20b's registry binds to another wave's IDs.
5. Record conflict for tsukuroi r20b. No success record exists, yet 50 reports were written after both refusals. Reports mention TsukuroiR19Recovery in 9 and TsukuroiR20 in 8 of 50; 39 mention neither, so authorship is not attributable.
6. Stale second-hand. GtLaneKama (10:34Z) said round-21 was unsettled with no successful spawn. Attempt 6 (10:44:42Z) superseded that. knowledge/wave-settlement-r20.md s4 repeats the round-21 claim.
7. Listing hazard. read on kama round-21/ listed only sources/; ls -la shows build/ (07:45 local). Spawn-record checks here used ls, stat and parsed files.

## 4. Method, bounds, provenance

- Scans (read-only; rc=1 each, an observation, not an error): python3 mori-shokunin/tools/mori-wave-settlement.py scan --lane-root <lane> --fleet-root /home/vgpnk/Projects/shokunin --out mori-shokunin/.ufo/waves/round-20/falsify/DeclaredVsDispatched/scan-<lane>.json, for kama, kagi, tsukuroi. Each walks that lane's whole .ufo/waves JSON set, which is the tool's design and reaches beyond the four named dirs. Output holds statuses and names only.
- Spawn and refusal evidence: named dirs only (kama round-19/falsify, round-21/build; kagi round-25; tsukuroi round-20/build). Read via ls, stat, Python and /usr/bin/jq 1.8.2; quotes limited to status and job lines.
- Peer tool outputs in my falsify dir (LiveKaidoku, LiveMado, LiveKake, LiveKumitate, LiveKasegi, LiveRevenger scan.json) and evidence/c2-live-mori.json and c2-live-fleet.json were used as tool states, not re-derived.
- S items come from GtLane*.md, knowledge s4 and lesson M1, which other seats wrote. They are not re-verified against lane dirs. U = not classified.
- Not opened: .ufo/interactive-sessions/, .ufo/worktrees/, .jj/, ~/.omp logs. Globs only inside named wave dirs (kama round-21 out/, kagi round-25); no lane-wide or fleet-wide grep or glob.
- Installs or updates: none. Used python3 stdlib and /usr/bin/jq 1.8.2.
- Scratch: falsify/DeclaredVsDispatched/ holds scan-kama.json, scan-kagi.json, scan-tsukuroi.json and fleet-waves.tsv (44 rows: lane, dispatch_path, tool_state, members, present, missing, scan_mtime, class, grade, basis).

## 5. For L1

- Pin any count from one snapshot. Re-run the three scans together; kama and kagi moved within minutes.
- Split missing into declared-only, spawned-unreported, off-path and late before any coverage figure is claimed.
- Still unbound (360): tsukuroi r12, r17f, r18b, r19f; mori r18w1, r19w1, r19w2, r20w1; kaidoku r16w1, r18w2, r19w1; mado r13 to r21 (7 waves); kake r22w1, r22w2, r23w2. Each needs a reader scoped to its own lane wave dirs.
