# OverlapTsukuroi — mori vs tsukuroi provinces: package transactions, pacman.log, boot-chain, OOM

Seat: MoriR17.OverlapTsukuroi-5 (connector, leaf — no subagent dispatch). Date: 2026-10-20.
Method: read-only `read`/`grep`/`glob` only. No pacman command, no journalctl, no selftest, no
VCS mutation, no writes outside this report. Installs/updates: **none** (tooling-directive
record: nothing installed; built-in tools sufficient).
Greps executed (all rc0 unless noted): `/var/log/pacman.log` pattern `\[2026-10-20 (09:15|13:23)`
→ **no matches** (log stamps are ISO `T`-form, e.g. `2026-10-20T09:15:30-0300`; retried with
`2026-10-20T…` → matches below); `zcode` on pacman.log; `2026-10-20T.*(synchronizing package
lists|starting full system upgrade|transaction started|transaction completed|Running 'pacman)`
on pacman.log; `09:15|13:23`, `earlyoom`, `tsukuroi`, `FR10` sweeps on both lane repos;
`ADJ-04|Owns|Refuses|pacman` and `Host memory|fleet correlation|mori` on tsukuroi PROVINCE.md;
`PLANE oom` on `tools/tsukuroi-census.sh`.

## 0. Axes (godspeed step 1)

Round-17 declared claims (contract.md:6-27): **C1** capability acquisition / coverage —
`tools/mori-seat-terminal.py` (lowest owned axis 6); **C2** operability — jj branch-anchored
census probes (axis 7). This item touches neither gate surface; it moves the
**evidence-currency frontier (FR10)** and the **adjacency/handoff plane** that both C1
interpretation and the kill-class alarms sit on.

## 1. The detections (primary evidence, this seat's own reads)

- `/var/log/pacman.log:2462` — `[2026-10-20T09:15:30-0300] [PACMAN] Running 'pacman -Syu
  --needed --noconfirm nvme-cli smartmontools fio xfsprogs pacman-contrib earlyoom iotop-c
  sysstat stress-ng btrbk linux-lts linux-lts-headers'`; `:2463` synchronizing package lists;
  `:2464` starting full system upgrade 09:15:31; transaction rows `:2479-2941`, completed
  09:16:47. 448 upgraded/installed rows (`:2462-3063` sweep count → 448, per tsukuroi
  `fresh-capture.txt:84`). `btrbk`, installed by this -Syu, was removed again 09:38
  (`pacman.log:3148`).
- `/var/log/pacman.log:3161` — `[2026-10-20T13:23:08-0300] [PACMAN] Running 'pacman -U
  --needed --noconfirm --config /etc/pacman.conf --
  /home/vgpnk/.cache/yay/zcode/zcode-3.16.2-1-x86_64.pkg.tar.zst'`; `:3164` installed zcode
  (3.16.2-1); `:3165` transaction completed; `:3169` `pacman -D --asexplicit zcode`.
- Context: 13 further 2026-10-20 transactions 01:06-09:39 (`pacman.log:2410-3159`, inventoried
  in mori's sibling draft `build/PacmanTxnToday.md:38-42`); pre-staging download-only
  `pacman -Sw --cachedir /tmp/pkgcheck limine-mkinitcpio-hook plymouth mkinitcpio` at 08:20:52
  (`pacman.log:2461`).

Both detections are plain-file reads of `/var/log/pacman.log` — no journal, no pacman
invocation — so they are inside seat rules as *detection*.

## 2. Province comparison on the four surfaces

| Surface | mori PROVINCE.md | tsukuroi PROVINCE.md | Net boundary |
|---|---|---|---|
| Host package transactions | No owned surface; Refuses OS package state `→ tsukuroi` (`mori:12-14`); "Detection and report only — never remediation" (`mori:16`) | Owns pacman state, read-only probes (`tsukuroi:8-10`); "Never installs, upgrades, or removes packages… Detection and report; the operator remediates" (`tsukuroi:27-28`) | mori may report dated transaction *events*; every OS-state reading (what the packages/units now are, health, gate compliance) is tsukuroi's |
| pacman.log | Not named as an owned surface; this round read once, wave-scoped (`build/ProvinceNotesDraft.md:105-109`) | pacnew-plane boundary: "Pair pacman-log history with current readable filesystem findings" (`tsukuroi:21`) — log-vs-filesystem *pairing* is tsukuroi's | Timestamped event reading is unowned detection space (both lanes used it today); standing log-pairing surfaces would duplicate tsukuroi's plane — mori must not add one |
| Boot-chain | Refuses (`mori:12-14`) | Owns journal/boot triage + initramfs-v42 surface (`tsukuroi:11,22`); r17 deliverable `corpus/knowledge/boot-chain-r17.md` exists (glob-verified) | mkinitcpio/UKI/hook risk analysis is exclusively tsukuroi's; mori records only liveness correlation around a boot |
| OOM/kill evidence | Owns fleet-facing kill/OOM journal classes + cgroup counters (`mori:24-25`); FR10 userspace-killers frontier (`mori:53`; `corpus/README.md:341`) | "Host memory and kill-event measurements support OS triage; they do not establish which fleet wave caused pressure… fleet correlation belongs to mori" (`tsukuroi:30-33`); ADJ-04 hands fleet attribution to mori (`tsukuroi:49`) | mori = fleet attribution of kill *events*; tsukuroi = OS cause/unit diagnosis. Journal diagnosis overlaps by design; the ADJ-04 channel is the splitter |

## 3. Adjacency boundary for mori reporting the 09:15 -Syu / 13:23 -U detections

**MAY (detection + report):** emit the dated transaction rows (§1) as host events in the r17
report; correlate the timestamps with fleet timeline evidence (watchdog ticks, wave activity,
seat transcripts under C1's field limits); request tsukuroi-side analysis when OS-state
interpretation is needed.

**MUST NOT:** run any pacman command (binding wave context, `wave1-context.txt:6`);
evaluate boot-chain compatibility, hook behaviour, or whether the operator's update-safety
gate ran (`[UNKNOWN]`, already flagged in `build/ProvinceNotesDraft.md:108-109`); read package
or unit health from the log; infer pause compliance or actor identity from pacman.log alone
(pacman.log carries no invoking user — attribution needs tsukuroi's sudo-journal capture, §4);
add a standing pacman.log census surface (second convention over tsukuroi's pairing plane).

**Handoff shape:** tsukuroi's checklist fields — trigger, UTC capture time, boot/time window,
exact read-only command, exit code, observed value; closure states `prepared/reported/
acknowledged/accepted/resolved` (`tsukuroi:56-65`). Working precedent: packet
TSUKUROI-F1-MEM-01 received and placed by mori (`mori:71-73`). In-lane consistency: sibling
`build/ProvinceNotesDraft.md:105-109` already drafts this exact split ("Mori detected and
reports these only. OS package, systemd-unit and boot-chain state belong to tsukuroi"); my
comparison finds no conflict with either province.

**Reverse channel (ADJ-04, `tsukuroi:49`):** when tsukuroi needs fleet/wave attribution for a
kill or pressure signal it sends mori capture time, boot/window, counter/PSI evidence — the
same packet mori should mirror when handing the §1 detections over: timestamps + log lines +
"request correlation", never an OS-state claim.

## 4. What tsukuroi already owns (mori must cite, not re-derive)

- L1 captures 2026-10-20: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt`
  (12:35:07-03:00) and `fresh-capture.txt` (12:38:12-03:00) — SOURCES S051/S052
  (`tsukuroi .ufo/waves/round-17/build/sources-rows.md:22`, `SourcesRecheckDraft.md:28-29`).
- Boot-chain risk: `corpus/knowledge/boot-chain-r17.md` — 42.2 images whose late hooks target
  unmounted `/new_root` while installed UKIs reference `/sysroot` (`build/ConnL0Thread.md:3`;
  `boot-chain-capture.txt:175`, hooks `:20-21`); 7.2.11 + linux-lts UKIs built 09:18
  (`boot-chain-capture.txt:2984-3046`).
- Freshness rechecks invalidating mori-visible dated claims: 413-pending superseded,
  sync marker now `pacman.log:2463` (`build/FreshPartialUpgradeRecheck.md:6-15`);
  `-Syu INERT` superseded (`build/fresh/update-safety-v3.json:5-9`).
- L0 thread verdicts (`build/ConnL0Thread.md:9-12`): `:54` moot-not-resolved (gate bypassed),
  `:55` "host-wide pause was not operative (13 operator pacman runs)… only the agent-side
  pause holds", `:57` pause = post-upgrade containment, `:60` live pre-reboot guard.
- Actor attribution: sudo-journal capture inside `boot-chain-capture.txt:76-96` — `vgpnk`
  ran the 09:15 -Syu from `~/Documents/nvhelpme`; mori's sibling `build/PacmanActorTrace.md:53-57`
  adds that the operator's session notes planned a targeted `-S`, executed as full `-Syu`.
- Memory/OOM plane: `build/FreshMemoryPlaneSweep.md:11-14` — oomd disabled, earlyoom enabled,
  zswap on, sysstat staged by the 09:15 -Syu; census `PLANE oom` emitter landed at
  `tools/tsukuroi-census.sh:2659` (grep-verified) plus `PLANE update-safety`.
- Stale-cell tracking: `build/falsify/FxUnflaggedMem.md:5` already marks tsukuroi's own
  `oom-event-plane.md` / `kill-event-deep-r8.md` earlyoom-absent cells affirmatively false.

## 5. Contradictions (stated, not smoothed)

1. **Pause scope.** Mori's binding wave context says "all pacman transactions are paused
   host-wide" (`wave1-context.txt:6`); pacman.log shows 16 transactions on 2026-10-20
   including the -Syu (`:2410-3169`). Tsukuroi's resolution (`ConnL0Thread.md:10-11`): the
   pause was never operative for the operator; only the agent-side pause holds, now as
   post-upgrade containment. Both statements are true in their scopes; mori must keep the
   seat rule and stop treating it as a host-state claim.
2. **earlyoom state.** mori r12 (verified 2026-10-19): `systemctl is-active earlyoom.service`
   → inactive, `is-enabled` → `not-found` (`corpus/knowledge/userspace-oom-killers-r12.md:14`).
   tsukuroi capture 2026-10-20 12:38: earlyoom-1.9.0-1 installed and `is-enabled` → `enabled`
   (`fresh-capture.txt` package list + is-enabled block; `FxUnflaggedMem.md:5`). Both were
   true at capture time — a dated state flip, not an error. The -Syu names `earlyoom`
   (`pacman.log:2462`) but [INFERENCE] Arch's earlyoom package does not auto-enable the
   service, so who enabled it is [UNKNOWN] and belongs to tsukuroi's unit-state plane.
3. **Journal-diagnosis ownership.** mori reads journal/cgroup events as fleet evidence,
   "never owning OS state" (`mori:13-14`); tsukuroi ADJ-04 simultaneously retains "OS memory,
   journal and boot diagnosis" (`tsukuroi:49`). The operative split both provinces already
   encode: mori owns event *attribution to fleet activity*, tsukuroi owns OS *cause*
   (`mori:66` calls the overlap "adjacent host diagnosis, not contested fleet ownership").
   Keep the split verbal in every report; a scalar ownership merge would break ADJ-04 routing.

## 6. Proposed move (one, bounded)

**Move:** add a dated FR10 currency + routing note to mori's r17 report (frontier-line update
at most, no code): *"As of the tsukuroi capture 2026-10-20T12:38:12-03:00, earlyoom is
installed and enabled on this host (tsukuroi-owned unit state, cited not re-probed);
consequences for mori: (a) every `unavailable (inactive)` userspace-killer rendering
(`userspace-oom-killers-r12.md:6,14`, SKILL.md:30) is date-scoped to its capture, not current
state; (b) earlyoom kills carry no catalog MESSAGE_ID (`round-13/build/CatalogSource.md:168`;
S016 README SIGTERM/SIGKILL path), so a future earlyoom SIGKILL of a seat process surfaces
only via the `98e32220…` unit-SIGKILL class / exit-status fields / C1 terminal classes — never
the `d989611b…` oomd or kernel-OOM notice classes. Route the enabling-actor and unit-health
questions to tsukuroi (ADJ-04 reverse channel); keep journal-class observation in mori."*

- **Affected axes:** improves coverage/evidence currency of the C1 interpretive layer and the
  kill-class alarms (axis 6/7 context) and FR10 truthfulness; prevents a future
  "no userspace killer configured" comfort read. **Harms none:** no C1/C2 code or gate change,
  no new standing surface, no ownership absorption, no pacman/journal execution.
- **Why non-obvious:** the transaction mori is merely *reporting* silently flipped mori's own
  FR10 premise (killer inactive→active) and activated the one kill path mori's catalog-ID
  classes cannot see — visible only by crossing the two provinces and the r12/r17 captures.
- **Risks:** (i) enablement cause is [UNKNOWN] — keep dated-state wording, never "the -Syu
  enabled it"; (ii) drift temptation to probe earlyoom units in mori — forbidden, tsukuroi's;
  (iii) C1 misattribution: an earlyoom-killed seat ends `incomplete`/`aborted`/`dead_error_other`,
  never `dead_rate_limit` — an interpretive note only, no contract change.

**Verification:** every claim is path:line-cited above; a reviewer re-reads those lines — no
execution, no probes, no new captures required. All cited captures are 2026-10-20; province
and census lines re-read today.

## 7. Execution record

Commands run by this seat: `grep` (pacman.log ×3, both repos ×6, tsukuroi-census.sh ×1) and
`read`/`glob` on the cited paths; one grep returned no matches due to timestamp format and was
retried with the correct pattern (§ Method). Exit-status note: greps returning matches are
rc0; the no-match retry was rc1-as-expected before the corrected pattern. No selftest, no
build, no installs, no scratch writes, no /tmp writes, no journal or pacman contact.
