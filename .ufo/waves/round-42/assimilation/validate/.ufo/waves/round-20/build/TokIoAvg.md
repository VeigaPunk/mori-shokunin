# TokIoAvg: C1 classification of `io_avg_unavailable` (round 20)

Seat: MoriR20.TokIoAvg (leaf, read-only). Receipt: `.ufo/waves/round-20/evidence/c1-drift-entering.json` (rc 1, 50 tokens; `io_avg_unavailable` at lines 59 and 72). Measured commit `2061780` (census blob sha256 `87b8d680…ab28`; HEAD `e4d9384` carries the same blob).

**Verdict: `live-state`.** The census emits this key with the same code it had when the r10 baseline was pinned. The value changed because the host now mounts `/tmp` from a block device (`/dev/nvme0n1p1`, xfs) instead of tmpfs. The census reads that correctly and reports `none`.

## 1. Result (JSON-ready)

| token | class | reason | evidence |
|---|---|---|---|
| io_avg_unavailable | live-state | Unmeasured-target list went from `tmpfs:not-a-block-device` (r10 pin; r12 and r13 live receipts) to `none` because `/tmp` is now `/dev/nvme0n1p1` (xfs) via `/etc/fstab` (last modified 2026-10-20 09:48:47 -0300; current boot 2026-10-20 09:57:08 -0300). The disk-io code path is unchanged since d30b4e4, so `none` is its correct output for a now-measurable target. | tools/mori-census.sh:1974 (emit), :1946-1948 and :1959-1960 (reason sources), :2771 (key not volatile); corpus/evidence/baseline-r10-20261015T2231Z.json:12; .ufo/waves/round-20/evidence/c1-pin-probe-scratch.json:2,3,13; .ufo/waves/round-20/evidence/c1-drift-entering.json:59,72; corpus/evidence/roster-r12-20261019T220912Z-before-live.log:15; .ufo/waves/round-13/evidence/live-measurement.json:15; /etc/fstab:24-26; `findmnt -T /tmp`; `systemctl show tmp.mount`; /proc/diskstats `259 1 nvme0n1p1`; `git log -S io_avg_unavailable --oneline -- tools/mori-census.sh` = d30b4e4; SCORECARD.md:357-358; corpus/knowledge/drift-pin-r10.md:164-168 |

JSON form (one register entry; `schema` and the other 7 tokens are out of this seat's scope):

```json
{
  "token": "io_avg_unavailable",
  "class": "live-state",
  "reason": "/tmp moved from tmpfs to xfs on /dev/nvme0n1p1 via /etc/fstab (edited 2026-10-20 09:48:47 -0300, boot 09:57:08 -0300); census disk-io logic unchanged since d30b4e4, so none is the correct output for a measurable target",
  "evidence": "tools/mori-census.sh:1974,1946-1948,1959-1960,2771; corpus/evidence/baseline-r10-20261015T2231Z.json:12; .ufo/waves/round-20/evidence/c1-pin-probe-scratch.json:13; corpus/evidence/roster-r12-20261019T220912Z-before-live.log:15; .ufo/waves/round-13/evidence/live-measurement.json:15; /etc/fstab:24-26; corpus/knowledge/drift-pin-r10.md:164-168; SCORECARD.md:357-358"
}
```

## 2. Census lines that emit it now (`tools/mori-census.sh`, 4744 lines, sha `87b8d680…ab28`)

- `:1974` emits `io_avg_unavailable=${io_unmeas:-none}` inside the `emit_surface disk` row.
- `:1900` initialises `io_unmeas=''`. `:1946` calls `dev_of "$fs"`.
- `:1947-1948` (no block device, e.g. tmpfs) appends `<fs>:not-a-block-device`.
- `:1959` appends `<dev>:<reason>` for `unavailable:*` from `io_of`. `:1960` appends `<dev>:unknown`.
- `:1967-1968` emits `DISK_IO_UNMEASURED` only when no device yielded a rate. It is not emitted in the current state.
- Header contract `:74`: "every target it could not measure appears in `io_avg_unavailable=<dev>:<reason>` (never as 0 B/s)".
- Drift handling: the key is not in `DRIFT_VOLATILE_SPECIAL` (`:2771`, which lists `io_avg_since_boot` but not this key) and not in `DRIFT_COUNTER_KEYS` (`:2744-2764`). It is compared verbatim by `drift_field_report` (`:2849-2868`), which `drift_report` (`:2874-2918`) feeds and `run_drift` prints at `:3001`.

## 3. Baseline line and timeline (observed)

- 2026-10-15T22:26:29Z, r10 pin: `corpus/evidence/baseline-r10-20261015T2231Z.json:12` = `io_avg_unavailable=tmpfs:not-a-block-device`.
- 2026-10-19T22:03:55Z, r12 live: `roster-r12-20261019T220912Z-before-live.log:15` = tmpfs. Again at 22:38:11Z (`roster-r12-20261019T220912Z-live.log:10`). The r12 drift token list (`corpus/evidence/drift-r12-20261019T2204Z-classification.md:14`) has no io token.
- 2026-10-20T04:33:08Z, r13 live: `live-measurement.json:15` = tmpfs.
- 2026-10-20 09:48:47 -0300 (12:48:47Z): `/etc/fstab` mtime. `/etc/fstab:24-26` adds `UUID=<minimized>` on `/tmp` (xfs, nofail). The comment reads "Second NVMe (WD_BLACK SN8100…)" and "/tmp is emptied at every boot by /etc/tmpfiles.d/tmp.conf".
- 2026-10-20 09:57:08 -0300 (12:57:08Z, `TZ=UTC uptime -s`): current boot starts.
- 2026-10-21T10:22:12Z: pin-format scratch with census `87b8d680` gives `io_avg_unavailable=none` and `io_avg_since_boot=dm-0:<V>Bps/<V>s nvme0n1p1:<V>Bps/<V>s` (`c1-pin-probe-scratch.json:2,3,13`).
- Live now: `df -P /tmp` → `/dev/nvme0n1p1 134117380 … /tmp`. `findmnt -T /tmp` → `/tmp /dev/nvme0n1p1 xfs rw,nosuid,nodev,noatime,…`. `systemctl show tmp.mount` → `ActiveState=active`, `What=/dev/nvme0n1p1`, `Where=/tmp`, `FragmentPath=/run/systemd/generator/tmp.mount`. `lsblk` lists `nvme0n1p1` (xfs, 128G) at `/tmp`. `/proc/diskstats` row `259 1 nvme0n1p1` has sectors-written (field 10) = 746524704, which `io_of` reads (`:1879-1895`).
- Bracket: the change is after the 04:33:08Z receipt and lands at the 12:57:08Z boot, which follows the 12:48:47Z fstab edit.

## 4. Why the census logic is the same (`git show` / `git log`)

- `git log -S io_avg_unavailable --oneline -- tools/mori-census.sh` → `d30b4e4` only (2026-10-15, round-7 evidence, census r4 `c7c3569b`). That commit added the lines `io_unmeas` (+L792), `:not-a-block-device` (+L840), `unavailable:*` (+L851), `unknown` (+L852), `DISK_IO_UNMEASURED` (+L860) and the emit (+L866); line numbers are as of d30b4e4 and have since shifted.
- Function bodies extracted from `git show` and diffed: `dev_of` (6 lines), `io_of` (17), `probe_disk` (80), `emit_surface` (8), `emit_finding` (13), `cap` (6), `read_file` (5). All are identical across d30b4e4, `5be8943` (r10 pin, census `d7710981`) and `2061780` (measured, census `87b8d680`), 0 diff lines.
- `DISKSTATS`, `UPTIME_FILE`, `DF_BIN`, `DISK_TARGETS`, `DISK_WARN_PCT`, `DISK_CRIT_PCT` defaults are identical between `5be8943` and `2061780` (`:311-314`, `:321`, `:358`).
- The drift-side changes since r10 are: `boot` added to `DRIFT_VOLATILE_SPECIAL` (`:2771`), a `boot=<V>` mask in `drift_normalize` (`:2786`), and the volatile-note text in `run_pin`. None touches this key.
- `5be8943` changed only fixture lines (`MORI_DISK_TARGETS="$FX/root"`) among lines matching the io/disk patterns.
- Working-tree census sha equals the HEAD blob sha (`87b8d680…ab28`).

## 5. Intent (where stated)

- `SCORECARD.md:357-358` (Round 7 verdict, evidence `d30b4e4`): "disk row with `io_basis=since-boot io_avg_since_boot=dm-0:9433966Bps/12427s` + honest `io_avg_unavailable=tmpfs:not-a-block-device`".
- `corpus/knowledge/surfaces-r7.md:127-128`: "Non-block-device targets (tmpfs `/tmp`) get a reason, never a fake zero". Row 3 at `:31` is the same.
- `corpus/knowledge/drift-pin-r10.md:164-168`: `io_avg_unavailable=` "change legitimately when the host's state changes (… a device disappearing adds an `io_avg_unavailable=` entry). Those reports are *baseline aging*, not masking failure — the answer is the re-pin policy (§5), not a wider mask." This is the direct intent statement for this token class, and this case is its mirror image.
- LOG.md and SCORECARD.md: a grep for `nvme|fstab|tmp.mount|WD_BLACK|io_avg|tmpfs|/tmp` shows no entry recording the 2026-10-20 `/tmp` mount change. The only host-side statement of intent is the `/etc/fstab` comment at `:24-25`.

## 6. Agree / disagree with round-13 (`.ufo/waves/round-13/evidence/drift-classification.json`)

- **Not covered, so no agreement or disagreement on this token.** The round-13 register has 42 keys and `unclassified: []`. Its input (`drift-retained-baseline.json`) has 42 tokens, and `io_avg_unavailable` is not among them.
- The key appeared after round 13. The round-13 live receipt at 04:33:08Z still shows tmpfs. Round 13 was therefore not wrong about its own input.
- Round 13 used `[INFERENCE] … no re-pin/admission claim` labels for unexplained churn. I do not reuse that label, because the cause here is observed. The outcome is compatible: no census-regression claim, and nothing is suppressed.

## 7. Additional finding for L1 (not a token of this receipt): comparator blind to later elements of multi-valued keys

- Mechanism: `drift_scan` (`tools/mori-census.sh:2826-2843`) skips every whitespace-separated element that lacks `=` (`:2836`). Space-separated list values (`io_avg_since_boot`, `io_avg_unavailable`, `targets`) are therefore compared by their first element only. `drift_scan` is byte-identical between `5be8943` and `2061780`, so the gap is latent since r10.
- Replay (Python, same rules applied to the two normalized disk rows; the census was not run): the comparator names exactly `['io_avg_unavailable']`, which matches the receipt. It reports `io_avg_since_boot` as equal even though the current row adds `nvme0n1p1:<V>Bps/<V>s`. Synthetic rows: appending `/fast` to `targets=` or removing `/tmp` names nothing; appending a second unmeasured target to `io_avg_unavailable=` names nothing; changing the first target names `targets`.
- The receipt corroborates this. Its 50 tokens contain no `io_avg_since_boot` despite the added device.
- Conflicts with documented intent `corpus/knowledge/drift-pin-r10.md:97`: "device identity is *not* masked, so a device change is drift".
- Consequences: the 50-token count is a lower bound for disk-row drift, and the nvme0n1p1 addition is visible only through `io_avg_unavailable`. A re-pin would record both devices, and `--drift` would not guard the second device afterwards.
- My reading: unintended detector behavior against documented intent, so a candidate `census-regression` in the contract's vocabulary. It is latent, not introduced in r13 to r19. L1 must decide whether it blocks the re-pin. I did not classify it as a token, because no token is emitted, and I did not edit the census (the contract forbids that).

## 8. Bounds, checks and assumptions

- Did not run `tools/mori-census.sh`. The replay in section 7 was a Python re-implementation of `drift_scan`/`drift_normalize` masking on two text rows.
- Read-only host probes only: `df -P`, `findmnt`, `lsblk`, `cat /proc/diskstats`, `cat /proc/uptime`, `uptime -s`, `stat`, `systemctl show tmp.mount`, read of `/etc/fstab`.
- Git used only as `log -S`, `log -G`, `show`, `cat-file`, `rev-parse`. No mutating commands, no `git status`.
- No installs or updates. Tools used were already present: git, jq, python3, findmnt, df, lsblk, systemctl.
- No retained transcripts or `~/.omp` session logs were opened.
- [INFERENCE] The `/etc/fstab` edit is the cause of the mount change. The mtime is 9m21s before the boot, and the mount table and `tmp.mount` agree. I did not inspect a journal or change record, and who made the edit and why are not recorded in the lane.
- [INFERENCE] The census at the entering tip (bg_207, about 10:18Z) emitted `none`. I observed that value only in the scratch pin (10:22:12Z, same boot, same census sha).
- Not classified (out of this seat's scope): the other 7 unclassified tokens.

## 9. Checks for the main agent

1. `findmnt -T /tmp -no SOURCE` should still report `/dev/nvme0n1p1` before any pin, so the live state is stable.
2. Decide whether the section-7 comparator gap is a named limitation in the register or a blocker. Do not describe the re-pin as zero census-regression without naming it.
3. After any re-pin, `io_avg_unavailable` should be recorded as `none`. A later revert of `/tmp` to tmpfs would flip it again, which is the live-state behaviour documented at `drift-pin-r10.md:164-168`.
