VERDICT: HOLDS. All three class labels AGREE with live-state under this item's rule (class = cause; a class is wrong only if its cause pointer fails). Every cause pointer I checked holds. Four register-text corrections are required (C1-C4, section 5), one of them a false factual claim ("non-author" receipts). The wave-2 AdjudicateWaves verdict BROKEN on -FINDING:WAVE_UNSETTLED_AGE argues a different standard (unproven settlement => census-regression); I do not adopt it under this rule (section 4). The pin-gate decision stays with L1.

Register read for this report: corpus/evidence/drift-classification-r20.json, sha256 f43baf5255fe711d3b7e3b172bf9bd79f14fd2668f888319d34d50067ef7c088, mtime 2026-10-21 08:13:06 -0300. It changed during my run. My first read showed class counts 29/19/2; the current file shows 26/19/5 (lane.audio, game-dev-2d, game-dev-3d moved census-schema-change -> roster-change by another seat; not analysed here). Dissent line 18 now reads "the script as a whole changed in seven commits" (my first objection is already fixed; its STALE-rule clause is out of this item and unchecked). Census tools/mori-census.sh: sha256 87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28, equal to the measured commit 2061780 blob and the HEAD 8f8c58e blob. Not run (not in this item).

## 1. Verdicts

| token (register lines) | class | verdict | cause pointer |
|---|---|---|---|
| -FINDING:WAVE_UNSETTLED_AGE (210-215) | live-state | AGREE | Holds: emitter identical r3->HEAD; fleet commit e20f4fa deleted both aggregator markers; new aged wave w24. The "non-author" receipts wording is false (C1). |
| obs (267-271) | live-state | AGREE | Holds: same wave-set change; my replay reproduces exactly this token pair. "positional pairing" is imprecise (C2). |
| io_avg_unavailable (261-266) | live-state | AGREE | Holds: /tmp is xfs on /dev/nvme0n1p1 after the 2026-10-20 fstab edit and boot; disk code unchanged since d30b4e4. fstab pointer needs the UUID hop (C3); blind_spot incomplete (C4). |

Leads read and not relied on: seat reports build/TokWaves.md, build/TokSilenceB.md, build/TokIoAvg.md, falsify/AdjudicateWaves.md. Every claim I cite below was re-derived.

## 2. -FINDING:WAVE_UNSETTLED_AGE

2.1 Emitter identity. Function bodies extracted from `git show <rev>:tools/mori-census.sh` (line `name() {` to first `}`), sha256 prefixes:
- probe_waves c9ae4b72 at 5be8943 (r10 pin), fe9fa90 (HEAD blob) and every census commit since 1439c47 (r3).
- emit_finding 05bb1362 (since 3d7aadc, r1); emit_surface 1e0e3d7c and cap b99ea1ce (since 7ca17b1, r1); drift_scan 2f188adb, drift_field_report 1bd9c767, drift_report 788e6943: identical 5be8943 <-> HEAD.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin blame -s -L 865,932 HEAD -- tools/mori-census.sh`: 15 lines from 1439c47, 15 from 486a4e3, 38 from 7ca17b1. Nothing after the pin.
- Inputs: WAVES_DIR (:303, `${MORI_WAVES_DIR:-$UFO/waves}`), UFO (:296), WAVE_UNSETTLED_S (:352, default 7200): text identical 5be8943 <-> HEAD.
- Caveat for the register text only: the whole file is NOT identical. sha256 d7710981 at 5be8943 vs 87b8d680 at HEAD; `git log --oneline 5be8943..HEAD -- tools/mori-census.sh` lists 7 commits (1f07f1d, 18d7d55, 8d22d18, 26f6589, 273aa74, 2be8294, fe9fa90). drift_normalize and probe_silence changed among them.

2.2 Baseline rows. baseline-r10-20261015T2231Z.json lines 26-36 are 11 WAVE rows: aggregator-r10 (26), aggregator-r10-resume (27), shokunin12h-20261014-p1-audit .. p5-chousa-r1 (28-32), shokunin-train-20261013, -w2, -w3, -w4 (33-36). Confirmed.

2.3 Fleet commit. `git -C /home/vgpnk/Projects/shokunin show -s --format='%H %an <%ae> %ci %s' e20f4fa` gives e20f4fa3fd3fc9550641af38da3eddcf3d35f528, souji-shokunin <souji@shokunin.local>, 2026-10-18 23:58:39 -0300, "souji: remove 96 pushed-receipt checkpoint artifacts (operator sweep 2026-10-18)". `git -C ... show --name-status --format= e20f4fa -- .ufo/waves/aggregator-r10 .ufo/waves/aggregator-r10-resume | wc -l` gives 18 (D rows: 10 under -resume, 8 under aggregator-r10, dispatch.json in both), exit 0. Lead TokSilenceB and r12:30 say 17: wrong.
- stat: both aggregator dirs mtime 2026-10-18 23:56:16 -0300.
- r10-era state: corpus/knowledge/observability-surfaces-r2.md:60-61, both `reg=0 disp=1 run=0` at 2026-10-15T15:27:57Z.
- Now: replica of probe_waves (c1-replay.py section 2) finds no regular files in either directory, so the empty branch (:926-927) applies and nothing is emitted.

2.4 Live aged set (replica, run at 2026-10-21 ~11:1x Z): 10 rows = shokunin-train-20261013, -w2, -w3, -w4; shokunin-train-20261016-w24 (new; dispatch.json is its only census marker; age about 4.1e5 s); shokunin12h-20261014-p1-audit .. p5-chousa-r1. Every aged row exceeds 7200 s by more than 400000 s, so no boundary effect. The r20 pin carries the same 10 rows (corpus/evidence/baseline-r20-20261021T1051Z.json:54-63, census 87b8d680).

2.5 Receipts pointer, new in the register (token evidence line 213): souji-shokunin/census/operator-sweep-20261018/approval-list.tsv:56-73. Lines 56-73 hold 18 rows, each `pushed`, and the paths are exactly the 18 deleted files. Content holds. Authorship does not:
- The same file is committed in the nested souji repo as 2f303dc, author `souji-shokunin <souji@shokunin.local>`, 2026-10-19 00:02:43 -0300. `git show 2f303dc:census/operator-sweep-20261018/approval-list.tsv | cmp - <working file>` gives rc 0. Its author matches the author of the deletion commit e20f4fa.
- The working file's mtime is 2026-10-19 00:01, after the 23:56:16 deletions and the 23:58:39 commit. The receipts are post-hoc.
- So "non-author cleanup receipts" is false (C1). The register's own dissent calls them "souji cleanup receipts".
- [INFERENCE] `pushed` is the sweep's preservation criterion; the file does not define it.

2.6 Pairing. drift_report (:2874-2918) runs three passes. Replay (c1-replay.py section 2): 9 baseline rows match a live row exactly after drift_normalize masks (age_s, ts, script_sha256, reg/disp/run/settle). aggregator-r10 (26) pairs with w24, the only leftover WAVE row, and the only differing key is `obs`. aggregator-r10-resume (27) has no partner and becomes `-FINDING:WAVE_UNSETTLED_AGE`. Replayed tokens: ['-FINDING:WAVE_UNSETTLED_AGE', 'obs'], identical to the entering tokens (c1-drift-entering.json:49 and :60).

## 3. obs

- :424 (`FINDING ... obs=$obs`) puts obs into every FINDING line; :923 (`emit_finding WAVE_UNSETTLED_AGE warn "wave=$base ..."`) carries the wave name. Both confirmed.
- Count 11 -> 10 and the pairing are as in 2.4-2.6. The obs change is the single pair aggregator-r10 <-> w24.
- Lead TokSilenceB says "pairing by id shifts every obs value". Wrong: 9 rows match exactly.

## 4. io_avg_unavailable

- Emitter: :1946-1948 (`dev_of` empty -> `<fs>:not-a-block-device`, the r10 tmpfs case); :1959-1960 (`unavailable:*` branch); :1974 (`io_avg_unavailable=${io_unmeas:-none}`). Confirmed.
- baseline-r10 line 12: `... io_basis=since-boot io_avg_since_boot=dm-0:<V>Bps/<V>s io_avg_unavailable=tmpfs:not-a-block-device; ...`. Confirmed.
- Host state, all observed: /etc/fstab:26 `UUID=1f8a5361-4f35-449a-bb30-63669df878d1 /tmp xfs ...` (fstab mtime 2026-10-20 09:48:47 -0300). `readlink -f /dev/disk/by-uuid/1f8a5361-4f35-449a-bb30-63669df878d1` gives /dev/nvme0n1p1. /proc/mounts:27 `/dev/nvme0n1p1 /tmp xfs ...`. `df -P /tmp` gives /dev/nvme0n1p1. `findmnt -no SOURCE,FSTYPE,TARGET /tmp` gives `/dev/nvme0n1p1 xfs /tmp`. `uptime -s` gives 2026-10-20 09:57:08, after the edit.
- Why `none`: dev_of (:1872-1877) gives `nvme0n1p1`; io_of (:1879-1895) matches the /proc/diskstats row `259 1 nvme0n1p1 ...` on field 3, and field 10 is sectors written, giving `<n>Bps`. io_unmeas stays empty, so the value is `none`. [INFERENCE] the emitted string was not produced by running the census; the replay is consistent with it.
- "Disk code unchanged since d30b4e4": `git log --oneline -S io_avg_unavailable -- tools/mori-census.sh` gives d30b4e4 only. `git blame -s -L 1872,1976 HEAD` touches only 7ca17b1 (50 lines) and d30b4e4 (55 lines). probe_disk e923a0eb, dev_of 86b6c9ff and io_of a9f12ab7 are identical at d30b4e4, 5be8943 and fe9fa90. DISKSTATS, UPTIME_FILE, DF_BIN, DISK_TARGETS, DISK_WARN_PCT and DISK_CRIT_PCT defaults are text-identical 5be8943 <-> HEAD (HEAD :311, :312, :314, :321, :358, :359).
- Blind spot (blind_spot line 265), confirmed and under-stated. drift_scan skips tokens without `=` (:2836). Replay section 3: an appended `nvme0n1p1:<V>Bps/<V>s` element is not compared; the only compared change is io_avg_unavailable; dropping /tmp from `targets=` changes nothing.
- Intent: drift-pin-r10.md:97 says "device identity is not masked, so a device change is drift". That is violated for elements after the first. drift-pin-r10.md:164-168 says io_avg_unavailable changes with host state are baseline aging. That supports live-state.

## 4a. Dissent: AdjudicateWaves BROKEN (falsify/AdjudicateWaves.md:1-7)

- Its argument: the fleet change explains why inputs disappeared but does not establish that the waves settled; the contract gives no class semantics; census-regression is the safe class and blocks the pin.
- Accepted: the contract gives no semantics (the only text is the four names and "census-regression blocks the re-pin"); the receipts are not settlement evidence; the blind spot is real.
- Rejected under this item's rule. A class is a cause label. The cause is observed: identical emitter, marker-less directories counted empty under a rule unchanged since r1-r3, markers deleted by e20f4fa. A census-regression label would assert a census-side cause that the evidence does not show. "Settlement unknown" has no slot in the closed set. That is a scheme gap to name explicitly, not a reason to mislabel the cause.
- Consequence: the pin gate is L1's decision. The committed re-pin (HEAD 8f8c58e, message "C1 classified register and re-pin (baseline-r20)"; corpus/evidence/baseline-r20-20261021T1051Z.json, pinned 2026-10-21T10:53:07Z) already carries these ten WAVE rows.

## 5. Required corrections (register text; no class changes)

- C1 (WAVE evidence line 213; token row). Delete "non-author". Replace with: "post-hoc operator-sweep receipts written by the sweep lane: souji-shokunin/census/operator-sweep-20261018/approval-list.tsv:56-73, all `pushed`, committed as 2f303dc by souji-shokunin 2026-10-19 00:02:43 -0300, after e20f4fa; author-independent accounting not established." The dissent already says "souji cleanup receipts"; the token row must agree with it.
- C2 (obs reason line 269). "positional pairing" -> "exact-line match, then same-id pairing of the two leftover aggregator rows with the one new row (drift_report :2874-2918)".
- C3 (io evidence line 264). Add the hop: "/etc/fstab:26 UUID=1f8a5361... -> /dev/disk/by-uuid -> /dev/nvme0n1p1; /proc/mounts:27". fstab alone does not name nvme0n1p1.
- C4 (io blind_spot line 265). Add: (i) elements after the first in io_avg_since_boot. The committed r20 pin already records `nvme0n1p1:<V>Bps/<V>s` there (baseline-r20 line 13). (ii) `targets=` elements after the first (removing /tmp from targets= is invisible). Consequence: a future /tmp device swap between two measurable devices is invisible to --drift, and io_avg_unavailable does not change.

Lead errors (owners should fix their reports; register text is unaffected):
- TokSilenceB obs section: (a) "aggregator dirs lost swarm-registry, dispatch and run" is wrong; only dispatch.json existed, reg=0 run=0 at r10 (observability-surfaces-r2.md:60-61). (b) "removed 17 stat lines" is wrong; it is 18. (c) "the census never saw those markers" is wrong; it saw disp=1 at r10. (d) "pairing by id shifts every obs value" is wrong; 9 rows match exactly.
- TokWaves E6: "dispatch.json only" for w24 is ambiguous; w24 has other files, and its only census marker is dispatch.json. Minor.
- r12:30 "17" should be 18.

## 6. Residual risks (not tokens; for L1)

- X1 Disk-row comparator (C4). drift_scan has been identical since its introduction at 5be8943. This is a pin-time design defect, not a regression in r13-r19. It should be named as a limitation before the post-pin `none` is relied on for the disk row.
- X2 WAVE false-clean. A marker-less directory cannot be told apart from a settled one (:926-927). Already in blind_spot; a design residual.
- X3 Outside this item, observed: DRIFT_COUNTER_KEYS at HEAD no longer contains kill_signal, segfault or unit_failure, which were in the r10 list (set difference 5be8943 vs fe9fa90). Their values are now compared verbatim. Not analysed against the journal tokens.

## 7. Reproduction

- `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/FamWavesIo/c1-replay.py; echo rc=$?` gives rc=0. Key output:
  - [1] whole-file sha256 5be8943=d7710981 fe9fa90(HEAD blob)=87b8d680; probe_waves c9ae4b72 IDENTICAL, emit_finding, emit_surface, cap, probe_disk, dev_of, io_of, drift_scan, drift_field_report, drift_report all IDENTICAL.
  - [2] baseline WAVE lines 26-36: 11 | live aged-unsettled (replica): 10; exact-matched lines: 9; replayed WAVE-family drift tokens: ['-FINDING:WAVE_UNSETTLED_AGE', 'obs'].
  - [3] io_avg_since_boot first-element equal=True; keys whose compared value changed: ['io_avg_unavailable']; dropping /tmp from targets= compared-value changes: [].
  - [4] register entries=50, declared == computed = {census-schema-change 26, live-state 19, roster-change 5}; entering tokens missing: []; entries without evidence: []; the three tokens are live-state.
- Other commands (read-only): `git -C <lane> show 5be8943:tools/mori-census.sh | sha256sum` -> d7710981...; `git -C <lane> show HEAD:tools/mori-census.sh | sha256sum` -> 87b8d680...; `git -C <lane> merge-base --is-ancestor 2061780 HEAD` -> rc 0.

## 8. Bounds, tooling, scratch

- No installs or updates. Tools used: git (show, log, blame, ls-tree, ls-files, rev-parse, merge-base), python3 (stdlib, read-only), stat, sha256sum, cmp, readlink, df, findmnt, uptime, cat /proc/uptime.
- Census not run. No git status, diff, add, commit or checkout. No mutating git or jj command.
- Not read: .ufo/interactive-sessions/, .ufo/worktrees/, .jj/, ~/.omp. Searches were limited to named files: census script, register, contract, lesson, /proc/diskstats.
- Sibling reads (read-only): souji-shokunin census/operator-sweep-20261018/approval-list.tsv and its git log in the nested souji repo; fleet .ufo/waves named dirs; /etc/fstab; /proc/mounts.
- Written: this report and falsify/FamWavesIo/c1-replay.py (read-only replay).
- [INFERENCE] items: the exact emitted io string `none` at the entering run; the meaning of `pushed`; the reason for the fstab edit and the sweep beyond the commit message.
