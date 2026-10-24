# ConnSiblingOverlap — FR10 adjacency scan (mori round 26, wave 1)

Seat: `MoriR26.ConnSiblingOverlap` (connector, leaf). Date: 2026-10-22. Read-only throughout.
Lane tip seen: mori `5e5e86f` (2026-10-22 10:14:08 -0300); tsukuroi `e9f5356c` (child of `157ee255`).
Tools installed or updated: none.

## Verdict

Only tsukuroi holds earlyoom or systemd-oomd knowledge in a durable corpus. No sibling's current-use
statement contradicts the 2026-10-22 host reading (earlyoom active and enabled, systemd-oomd inactive and
disabled). Every negative earlyoom statement in tsukuroi is dated 2026-10-14 and carries tsukuroi's own
append-only supersession notice. Host diagnosis of the earlyoom unit belongs to tsukuroi. Mori holds the
fleet-facing evidence rule. Three findings bear on mori's round-26 wording and are set out below:
"active since" is not "enabled since"; earlyoom acted in the previous boot; and tsukuroi's anchor census
pins mori `userspace-oom-killers-r12.md:8`.

## 1. Scan method and per-lane counts

Command (read-only, committed bytes at each lane HEAD; mori excluded):

```sh
for d in *-shokunin; do git -C "$d" grep -i -c -E 'earlyoom|systemd-oomd|oomd|ManagedOOM' HEAD; done
```

| Lane @ HEAD | Hits | What they are |
|---|---|---|
| tsukuroi `e9f5356c` | 2069 in 191 files | Durable corpus, SKILL, SOURCES, tools, and round-25 wave receipts (detail in section 2) |
| game-dev-2d `7753d49b` | 14 | Byte matches inside 7 exported `fixture.x86_64` binaries under `corpus/live/r25-*`; noise, not knowledge |
| kengaku `1f3b0f1e` | 1 | Byte match inside `.ufo/waves/round-28/scratch/FBoundaryReleaseScope/arxiv-v4.pdf`; noise |
| kaidoku `0375717e` | 7 | Wave receipts only: `.ufo/waves/arc2-loop1-round8/E8.md:57`, `R1.md:68,104,162` (a kernel memcg OOM, "not systemd-oomd"; a `ManagedOOMMemoryPressure=auto` unit property); `.ufo/waves/round-17/w2/SentinelSessionResidue.md:75` (an earlyoom process in a process listing); the rest are a temporary-file name and a base85 patch byte run |
| kama `1560e4d8` | 5 | Wave receipt only: `.ufo/waves/round-18/build/advice/ConnectTsukuroi.md:58,60,66,74,83`, quoting tsukuroi; line 83: "earlyoom is active." |
| mado `8e5d9369` | 7 | Wave receipts only: `.ufo/waves/round-17/w2/reports/AttackVersionBinding.md:68` and `ReviewScorecardCorrections.md:62` (the package install command list that includes earlyoom); 5 session-store path strings in round-20 and round-21 sweep JSON (paths not reproduced here, per the privacy bound) |
| souji `4edb25df` | 1 | `census/operator-sweep-20261018/tmp-census.tsv:250`, a temporary-file name; noise |
| the 13 other lanes | 0 | — |

No sibling has untracked or modified working-tree files matching the same terms outside `.ufo/waves/`
(checked with `git ls-files -o --exclude-standard` and `git diff --name-only HEAD`, each piped to `rg -l -i`).

Privacy note for the L1: kaidoku `SentinelSessionResidue.md:75` describes earlyoom's argv content.
It is not reproduced here. Case fixtures for C2 should not echo it.

## 2. Lanes holding earlyoom or oomd knowledge (durable surfaces)

All in tsukuroi. Bytes are identical at `157ee255` and `e9f5356c` for the five files below
(`git diff --stat 157ee255 HEAD --` on `PROVINCE.md SKILL.md corpus/knowledge/memory-pressure-r25.md
corpus/knowledge/oom-event-plane.md corpus/knowledge/kill-event-deep-r8.md` printed nothing).

- `corpus/knowledge/memory-pressure-r25.md:40-42`: "The supplementary read-only capture shows `earlyoom.service` active and enabled on this host." MP1 to MP6 cover what systemd-oomd 262 would do if it ran. MP4 says `auto` units are not monitored. MP6 at `:312-328` says a userspace kill moves no kernel counter. Entry sha256 at `157ee255`: `ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25`.
- `SKILL.md:2303-2318` restates MP1 to MP6. `SKILL.md:2305` says enabling or tuning a userspace OOM killer "stays operator-owned".
- `corpus/knowledge/oom-event-plane.md:51,280,344-345`: dated 2026-10-14 rows (oomd "inactive+disabled"; earlyoom "not installed", "absent", "not-found"). These are superseded for current use by `:442-452` (R18 notices), `:467-469` (R18 precision), and `:471-475` (R25 notice on the `auto` point).
- `corpus/knowledge/kill-event-deep-r8.md:255-256`: dated 2026-10-14 rows. Superseded by `:350-355` (R18, earlyoom active and enabled, `ActiveEnterTimestamp=Tue 2026-10-20 09:57:11 -03` at `:354`) and `:379-381` (R25).
- `SKILL.md:810` ("`earlyoom` absent") is superseded by `SKILL.md:1938` (R18-FRESH-SUPPLEMENT-03).
- `corpus/knowledge/freshness-recheck-r18.json:408-520` holds the machine twin of those notices.
- `corpus/SOURCES.md:66` (S060, round-18 host capture with earlyoom state) and `:126-132` (S120 to S126, systemd v262 oomd pages and code). Tsukuroi has no earlyoom upstream source row. The only `rfjakob/earlyoom` row in any lane is mori `corpus/SOURCES.md:22` (S016, README at `8477c902`); command: `git grep -n rfjakob HEAD -- '*SOURCES*'` in each lane.
- `corpus/knowledge/degraded-triage-r4.md:656`, `host-health-report-r3.md:661`, `journal-boot-plane.md:466`: recheck commands (`systemctl show earlyoom.service -p ActiveState -p UnitFileState`).
- `corpus/knowledge/boot-chain-r17.md:196`, `tools/check-boot-chain.py:74,82`: earlyoom is named in a package install argv list.
- `corpus/knowledge/adjacency-anchors-r19.md:163,171`: inbound records IN-068 (mori `PROVINCE.md:66`) and IN-076 (mori `corpus/knowledge/userspace-oom-killers-r12.md:8`), both classified RESOLVES to `oom-event-plane.md:344`.
- `plans/round-8.plan.md:81,188` say "`earlyoom` absent" with no notice. These are planning files [INFERENCE: not current-use guidance].

## 3. Who owns host diagnosis of the earlyoom unit

Tsukuroi does.
- Mori: `PROVINCE.md:12-14` refuses "OS package, systemd unit, driver/firmware and boot state (→ tsukuroi)"; `PROVINCE.md:66` says tsukuroi "Owns host OS, package, systemd-unit, driver, firmware, and boot diagnosis".
- Tsukuroi: `PROVINCE.md:3-4` (domain: "package state, systemd"); `:25-28` (refuses to restart services; "the operator remediates"); `:30-33` ("fleet correlation belongs to mori"); `:49` (ADJ-04 sends kill signals that need fleet or wave attribution to mori).
- Tuning and enabling: the operator (`tsukuroi SKILL.md:2305`; mori `PROVINCE.md:53` "never enable or tune a killer").

**Contested scope.** No lane contests earlyoom ownership. Two seams are reported, not resolved:
1. Tsukuroi's explicit Owns bullet names "systemd user units & timers (`systemctl --user` ...)" (`tsukuroi PROVINCE.md:10`). `earlyoom.service` and `systemd-oomd.service` are system units. Tsukuroi's ownership of them rests on its domain line `:3-4`, its package-state surface (the earlyoom package), and its corpus practice (`degraded-triage-r4.md:656`). It does not rest on a named system-unit surface. Mori's `PROVINCE.md:66` paraphrase ("systemd-unit ... diagnosis") is broader than tsukuroi's own Owns text.
2. MP6 (`tsukuroi memory-pressure-r25.md:312-328`) restates mori's held ground, `userspace-oom-killers-r12.md:6` (userspace kill paths do not increment the kernel OOM counters, verified 2026-10-19), and does not cite mori. The `mori` mentions in that entry are at `:35,38,90,139,192,368,384`, none of them in MP6. Tsukuroi's own round-25 connector had advised a pinned mori pointer for MP6 (`tsukuroi .ufo/waves/round-25/w1/ConnSiblingOverlap.md:31,53`). The two statements agree, so this is overlap and not contradiction. Wording hazard: `:316` says `oom_kill` counts processes "killed by any kind of OOM killer" (the kernel's own wording), and `:317` then excludes userspace killers. Mori's new entry should not quote `:316` without the kernel-only qualifier.

## 4. Sibling statements against the 2026-10-22 host reading

Host reading (this seat, 2026-10-22T10:15:06-03:00):
`systemctl show earlyoom.service -p LoadState,ActiveState,UnitFileState,ActiveEnterTimestamp,ActiveEnterTimestampMonotonic,NRestarts`
printed `loaded`, `active`, `enabled`, `Thu 2026-10-22 04:55:44 -03`, `19964362`, `0`.
`systemctl show systemd-oomd.service -p LoadState,ActiveState,UnitFileState` printed `loaded`, `inactive`, `disabled`.
`pacman -Q earlyoom systemd` printed `earlyoom 1.9.0-1`, `systemd 262-1`.

- **No current-use contradiction.** No sibling says systemd-oomd is active. A tsukuroi search for `oomd ... active|enabled|running`, excluding inactive, disabled and conditional wording, returned nothing. Every negative earlyoom statement is a 2026-10-14 measurement with a superseding notice (section 2). The only exceptions are the plan file lines.
- **Stale "active since" value (dated, not contradictory).** Tsukuroi's "active since 2026-10-20 09:57:11 -03" (`oom-event-plane.md:448`, `kill-event-deep-r8.md:354`, `freshness-recheck-r18.json:420`) belongs to boot -1. `journalctl --list-boots` shows boot -1 `3e7084f4…` starting Tue 2026-10-20 09:57:09 and boot 0 `6a7f4fdf…` starting Thu 2026-10-22 04:55:41. Tsukuroi's round-25 capture already reads the current value (`tsukuroi .ufo/waves/round-25/capture/capture-earlyoom.txt:16`, `ActiveEnterTimestamp=Thu 2026-10-22 04:55:44 -03`).
- **Mori's own wording conflicts with sibling precision.** Mori `LOG.md:1824` says "active and enabled since 04:55:44 -03", and the wave-1 context repeats it. Tsukuroi's rule is "earlyoom active-since is distinct from enabled-since" (`tsukuroi corpus/lessons/round-18.md:115`), and "the date of enablement itself was not captured" (`oom-event-plane.md:469`). The host agrees with tsukuroi:
  - `grep -n 'installed earlyoom' /var/log/pacman.log` → `2514:[2026-10-20T09:16:28-0300] [ALPM] installed earlyoom (1.9.0-1)`.
  - `journalctl -q -b <n> -u earlyoom.service -o json --output-fields=_BOOT_ID | wc -l` → boot -2: 8, boot -1: 252, boot 0: 13. So earlyoom ran in all three boots.
  - 04:55:44 is the start of the current invocation, about 20 s after boot (monotonic 19964362 µs).
- **Previous-boot actions, recorded by no lane.** These are counts only, from `journalctl -q -b <n> -u earlyoom.service -o cat`, prefix-matched on the contract grammar; no message text was kept:

  | boot | version lines | sending SIGTERM | sending SIGKILL | escalations | kill failed | low-memory warnings |
  |---|---|---|---|---|---|---|
  | -2 | 1 | 0 | 0 | 0 | 0 | 0 |
  | -1 | 1 | 38 | 1 | 0 | 0 | 40 |
  | 0 | 1 | 0 | 0 | 0 | 0 | 0 |

  A search of all siblings for `sending SIG(TERM|KILL) to process` or earlyoom kill or action wording found only tsukuroi `.ufo/waves/round-18/build/SrcEarlyoom.md:3,7`, which describes the semantics and records no host action. [INFERENCE] The C2 tool, scoped to the current invocation, will report `KILLERS_QUIET` today even though earlyoom acted 39 times in the previous boot. C1 does not claim kill history (contract `:47`), but the r26 entry must not say or imply that earlyoom has not acted.

## 5. Proposed move (one, bounded)

**Pin, scope, and keep line 8 still.** This is a synthesis with `DraftR12Corrections.md`.
- (a) The r26 entry carries the adjacency sentence below. It cites tsukuroi at `157ee255` in the `@rev`-qualified form, which mori already uses for souji (`PROVINCE.md:69`). It points to tsukuroi's superseding notices, not the superseded 2026-10-14 rows. Tsukuroi's inbound census excludes `@rev`-qualified citations (`tsukuroi adjacency-anchors-r19.md:19`), so the new pointer adds no record that can drift.
- (b) The entry separates three dates: the start of the current invocation, the unknown enablement date, and the install time.
- (c) The r12 rewrite keeps line 8 at line 8. F1 is at `userspace-oom-killers-r12.md:6`, above the line that tsukuroi IN-076 pins (`adjacency-anchors-r19.md:171`), so the F1 rewrite must stay on one line. `DraftR12Corrections.md:180-191` appends to line 8 in place, which is compatible. Its optional `superseded-in-part-by:` header "placed as line 4" (`:194-198`) would push the pinned line to 9; prefer the in-place append.

Affected axes: freshness (C1) improves, because the wording is accurate to the host. Adjacency (held at 6) is not harmed: no new drifting pointer, and IN-076's sibling locus stays put. Calibration (held at 5) is not harmed: there is no enablement-date or "never acted" overclaim.

Adjacency sentence for `corpus/knowledge/userspace-oom-killers-r26.md`:

```
Adjacent: host OS, package and systemd-unit diagnosis, including the earlyoom and systemd-oomd units, is tsukuroi's (`tsukuroi-shokunin@157ee255:PROVINCE.md:3-4,25-33`). Its round-25 entry reads what the installed systemd-oomd 262 would do if it ran and records `earlyoom.service` active and enabled (`tsukuroi-shokunin@157ee255:corpus/knowledge/memory-pressure-r25.md:40-42,312-328`), and its dated 2026-10-14 earlyoom-absent rows are superseded for current use by its own notices (`tsukuroi-shokunin@157ee255:corpus/knowledge/oom-event-plane.md:442-452,467-475`); mori cites these and absorbs none. Mori's claim is the fleet-facing evidence rule only: earlyoom state, the thresholds earlyoom logs at start, and counts of its action lines in the current invocation, with a killer that is not running reported as unavailable, never zero; diagnosing, configuring, enabling or tuning either killer stays with tsukuroi and the operator.
```

Dating sentence for the same entry:

```
`earlyoom.service` entered active at 2026-10-22 04:55:44 -03, about 20 s after the current boot began; that is the start of the current invocation, not the date it was enabled, which no capture holds (`tsukuroi-shokunin@157ee255:corpus/knowledge/oom-event-plane.md:469`). The package was installed at 2026-10-20T09:16:28-03:00 (`/var/log/pacman.log`, line 2514), and earlyoom unit records exist in each of the last three boots, so a quiet verdict for the current invocation says nothing about earlier boots.
```

## 6. Risks

- The `@157ee255` pins are stale by design once tsukuroi commits again. The bytes stay fixed and the cited lines do not move. Tsukuroi's gate will not see these pointers (`adjacency-anchors-r19.md:19`), so it raises no drift alarm, and none is needed.
- Citing the boot -1 action counts in a committed mori file would need a committed capture and a SOURCES row. This report is not that capture; if the L1 uses them, the scout or executor seat should re-take them as counts only.
- `pacman.log` is host state, not a public source; if cited in the entry, it needs an own-work SOURCES row, like tsukuroi S060.
- Seam 1 (user units versus system units) is tsukuroi's to word. Mori's `PROVINCE.md:66` paraphrase stays accurate in practice; this report proposes no edit to any sibling.

## 7. Verification for the L1 (not run as passes by this seat)

```sh
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 157ee255:corpus/knowledge/memory-pressure-r25.md | sed -n '40,42p;312,328p'
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 157ee255:corpus/knowledge/oom-event-plane.md | sed -n '442,452p;467,475p'
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 157ee255:PROVINCE.md | sed -n '3,4p;25,33p'
R=<landed>; git -C /home/vgpnk/Projects/shokunin/mori-shokunin show "$R:corpus/knowledge/userspace-oom-killers-r12.md" | sed -n '8p' | grep -c '^Adjacent: `tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:344–346,353–367`'   # expect 1
git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -E 'enabled since|never acted|has not acted' "$R" -- corpus/knowledge/userspace-oom-killers-r26.md   # expect no output
```
