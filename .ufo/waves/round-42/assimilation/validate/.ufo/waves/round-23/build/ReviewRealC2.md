# ReviewRealC2 — independent re-derivation of `frozen/c2-expected-real.json`

Seat: `MadoR22-2.ReviewRealC2-8`
Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md` (frozen lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`), §C2.
Target under review: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/c2-expected-real.json`
Tool installs: none (no install/update performed; nothing required beyond `awk`, `readlink`, `ls`, `python3 os.stat`, all preinstalled).

Verdict: **AGREE on every field of the frozen real control.** No disagreement found.
Two implementation hazards and one coverage gap are recorded below as advisory items (they are
not disagreements with the frozen file — the frozen file is right and the hazards are things a
future implementer of `tools/mori-quota-surface.py` can get wrong).

---

## 1. Method — permitted live reads only

Permitted set (wave bounds): `/proc/self/mountinfo`, `os.stat` of the fleet root and `/tmp`,
`readlink` of `/dev/mapper/*`, and directory listings / the `qgroups`+`mode` file under
`/sys/fs/btrfs`. No `quotactl`, no `btrfs`/`xfs_quota`/`repquota`, no `mount`, no privileged or
mutating call, no session/journal/process/service probe, nothing written outside my report file.

Reads actually performed:

| # | Read | Command |
|---|------|---------|
| R1 | mountinfo lines for `/`, `/home`, `/tmp` | `awk '$5=="/"||$5=="/home"||$5=="/tmp"' /proc/self/mountinfo` (+ a full field-split of those three lines) |
| R2 | deeper mount-point census | `awk '$5 ~ /^\/home\// {print $5}' /proc/self/mountinfo` → empty; `awk` count of exact `/`, `/home`, `/tmp` → 1 each |
| R3 | `st_dev` of the two paths | `python3 os.stat(...)` → fleet root `st_dev=57` (major 0, minor 57), `/tmp` `st_dev=66305` (major 259, minor 1); `os.path.realpath` of both = themselves |
| R4 | device-mapper links | `readlink -f /dev/mapper/root` → `/dev/dm-0`; `readlink -f /dev/mapper/*` (root → `/dev/dm-0`, control → itself) |
| R5 | btrfs sysfs | `ls -d /sys/fs/btrfs/*/` → `1d02a454-c549-4a35-b567-89d60902af8e/` and `features/`; `ls /sys/fs/btrfs/1d02a454-.../devices/` → `dm-0` (symlink → `../../../../devices/virtual/block/dm-0`); `ls -d /sys/fs/btrfs/*/qgroups` → **No such file**; `qgroups/mode` → **No such file** |

Disclosure: one line of `/proc/self/mountinfo` outside the three enumerated mount points
(`/dev/shm`) was read **only** to test the frozen file's `note` claim. It did not enter the
derivation of any expected field. The file `/proc/self/mountinfo` is a permitted read; only the
*derivation inputs* were restricted to `/`, `/home`, `/tmp`.

Raw R1 output (verbatim, three lines):

```
33 2 0:30 /@ / rw,noatime shared:1 - btrfs /dev/mapper/root rw,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=256,subvol=/@
65 33 0:30 /@home /home rw,noatime shared:183 - btrfs /dev/mapper/root rw,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=257,subvol=/@home
244 33 259:1 / /tmp rw,nosuid,nodev,noatime shared:207 - xfs /dev/nvme0n1p1 rw,inode64,logbufs=8,logbsize=256k,noquota
```

---

## 2. Re-derivation from the contract's rules (contract §C2, lines ~95–135)

### 2.1 Mount resolution (contract "Mount resolution (per path)")

Candidate rule: mount point equals realpath, or is `/`, or realpath starts with mount point + `/`;
choose the **longest** mount point; among equal mount points the **last** line wins.

| Path | realpath | Candidates | Chosen | fstype | mount point | source | super options (last mountinfo field) |
|---|---|---|---|---|---|---|---|
| `/home/vgpnk/Projects/shokunin` | same (no symlink component, R3) | `/` (btrfs), `/home` (btrfs); no deeper mount exists under `/home` (R2) | `/home` (longer) | `btrfs` | `/home` | `/dev/mapper/root` | `rw,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=257,subvol=/@home` |
| `/tmp` | `/tmp` | `/` (btrfs), `/tmp` (xfs) | `/tmp` (longer) | `xfs` | `/tmp` | `/dev/nvme0n1p1` | `rw,inode64,logbufs=8,logbsize=256k,noquota` |

No tie occurred (R2: exactly one line each for `/`, `/home`, `/tmp`), so the last-line-wins rule
is not exercised by this control.

### 2.2 Device check (contract "…device_check")

| Path | mount major:minor (field 3) | path `st_dev` | equal? | fstype btrfs? | derived `device_check` |
|---|---|---|---|---|---|
| fleet root | `0:30` | `0:57` | no | yes | `btrfs_subvolume_skipped` (mismatch is *expected* for btrfs; classification continues, **not** `device_mismatch`) |
| `/tmp` | `259:1` | `259:1` | yes | no | `match` |

### 2.3 Quota classification (contract table)

**fleet root, btrfs** — mount source `/dev/mapper/root`; `readlink -f` → `/dev/dm-0`, basename
`dm-0` (this is the device name the sysfs `devices/` directory lists — R4/R5). Exactly **one**
uuid directory lists `dm-0`: `1d02a454-c549-4a35-b567-89d60902af8e/`. Its `qgroups` directory is
**absent** → row "exactly one uuid, `qgroups` false" → `quota_state=disabled`,
`enforcement=n/a`, `basis=btrfs_qgroups_dir_absent`.
(`/sys/fs/btrfs/features/` is a non-uuid sibling with no `devices/` subdirectory; it lists no
device and is not counted.)

**`/tmp`, xfs** — super options `rw,inode64,logbufs=8,logbsize=256k,noquota`. Key set (text before
`=`, comma-split) = `{rw, inode64, logbufs, logbsize, noquota}`. `noquota` present; **no** quota
key (`usrquota,uquota,quota,grpquota,gquota,prjquota,pquota`) present → row 1 → `quota_state=disabled`,
`enforcement=n/a`, `basis=xfs_noquota_option`.

### 2.4 Run-level verdict (contract "Verdict precedence")

No path `enabled`, no path `unknown`, no setup error → **exit 0, `QUOTA_DISABLED`**.

---

## 3. Field-by-field comparison against the frozen file

### 3.1 Primary expected fields

| Frozen field | Frozen value | Re-derived | Result |
|---|---|---|---|
| `expected_exit` | `0` | `0` | **AGREE** |
| `expected_finding_id` | `QUOTA_DISABLED` | `QUOTA_DISABLED` | **AGREE** |

### 3.2 `expected_paths[0]` — `/home/vgpnk/Projects/shokunin`

| Field | Frozen | Re-derived | Result |
|---|---|---|---|
| `path` | `/home/vgpnk/Projects/shokunin` | same | AGREE |
| `fstype` | `btrfs` | `btrfs` | AGREE |
| `mount_point` | `/home` | `/home` | AGREE |
| `quota_state` | `disabled` | `disabled` | AGREE |
| `enforcement` | `n/a` | `n/a` | AGREE |
| `basis` | `btrfs_qgroups_dir_absent` | `btrfs_qgroups_dir_absent` | AGREE |
| `device_check` | `btrfs_subvolume_skipped` | `btrfs_subvolume_skipped` | AGREE |

### 3.3 `expected_paths[1]` — `/tmp`

| Field | Frozen | Re-derived | Result |
|---|---|---|---|
| `path` | `/tmp` | `/tmp` | AGREE |
| `fstype` | `xfs` | `xfs` | AGREE |
| `mount_point` | `/tmp` | `/tmp` | AGREE |
| `quota_state` | `disabled` | `disabled` | AGREE |
| `enforcement` | `n/a` | `n/a` | AGREE |
| `basis` | `xfs_noquota_option` | `xfs_noquota_option` | AGREE |
| `device_check` | `match` | `match` | AGREE |

Order check: frozen order is fleet root then `/tmp`, which equals the contract's default path
order ("the fleet root `/home/vgpnk/Projects/shokunin` then `/tmp`"). The oracle compares
**ordered** tuples, so this order is load-bearing and it is correct. **AGREE.**

### 3.4 `observed` block (provenance, not compared by the oracle)

| Frozen field | Frozen value | Re-derived | Result |
|---|---|---|---|
| `observed.fleet_root.st_dev` | `0:57` | `0:57` | AGREE |
| `observed.fleet_root.mountinfo_line_fields` | `65 33 0:30 /@home /home ... - btrfs /dev/mapper/root rw,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=257,subvol=/@home` | fields 1–6 = `65 33 0:30 /@home /home rw,noatime`; fields 9–11 identical | AGREE (middle optional fields elided with `...`, faithfully) |
| `observed.fleet_root.sysfs` | "one uuid lists dm-0; no qgroups dir" | exactly one uuid dir lists `dm-0`; `qgroups` absent | AGREE |
| `observed.tmp.st_dev` | `259:1` | `259:1` | AGREE |
| `observed.tmp.mountinfo_line_fields` | `244 33 259:1 / /tmp ... - xfs /dev/nvme0n1p1 rw,inode64,logbufs=8,logbsize=256k,noquota` | fields 1–6 = `244 33 259:1 / /tmp rw,nosuid,nodev,noatime`; fields 9–11 identical | AGREE |
| `observed_utc` | `2026-10-21` | observation date 2026-10-21 | AGREE |
| `schema` | `mori-r23-c2-real-expected-v1` | frozen-file schema (distinct from the tool's own output schema `mori-quota-surface-v1`) | AGREE (see advisory A3) |
| `note` | drift clause + "`/dev/shm` (tmpfs usrquota) is observed but outside the default paths" | `/dev/shm` → `tmpfs tmpfs rw,size=8388608k,inode64,huge=advise,usrquota` — `usrquota` present, outside the default path set | AGREE (verified) |

### 3.5 `observation_commands` reproducibility

All five commands named in the frozen file were run and produced exactly what the file claims:
the `awk` filter yields the three lines above; `os.stat` yields `0:57` / `259:1`;
`ls -d /sys/fs/btrfs/*/qgroups` → `No such file`; `ls -l /sys/fs/btrfs/1d02a454-…/devices/` →
`dm-0`; `readlink -f /dev/mapper/root` → `/dev/dm-0`. The uuid hard-coded in the command list
is the live uuid. **AGREE.**

### 3.6 Frozen-file integrity

`git show 4dc80c1:.ufo/waves/round-23/frozen/c2-expected-real.json` is byte-identical to the
worktree copy (`diff` clean); both SHA-256 `9cbb69c03d284c4aa240d5cc9c627cef37e85306bf13a92ea2284fbd65087398`.
The file landed in `4dc80c1`, i.e. **before** any implementation commit; `tools/mori-quota-surface.py`
is absent both in the worktree and at `4dc80c1`, so the contract's "expected/oracle land before the
implementation" ordering holds as of this review. **AGREE.**

### 3.7 Contract-vs-frozen-file consistency

Contract §C2 ("Real control … frozen now from independent host observation") states: exit 0
`QUOTA_DISABLED`; fleet root → btrfs, `/home`, disabled, `btrfs_qgroups_dir_absent`,
`btrfs_subvolume_skipped`; `/tmp` → xfs, `/tmp`, disabled, `xfs_noquota_option`, `match`.
The frozen file matches that prose field-for-field. **AGREE.**

### 3.8 Consumability by the sealed oracle

`oracle-quota.py` (`REAL_PATH_FIELDS = ("path","fstype","mount_point","quota_state","enforcement","basis","device_check")`)
reads the frozen file via `EXIT_KEYS`/`FINDING_KEYS`/`PATHS_KEYS`, which contain
`expected_exit`, `expected_finding_id`, `expected_paths` — exactly the spellings the frozen file
uses. `expected_paths` entries are objects keyed by the seven field names, so
`norm_expected_paths` recognises them. The frozen file is directly consumable as `--real-expected`.
**AGREE.**

---

## 4. Advisory items (not disagreements with the frozen file)

**A1 — `mount_point` is the single field that can flip `/` ↔ `/home` (implementation hazard).**
Both `/` and `/home` are btrfs mounts of the *same* source `/dev/mapper/root` and both yield
`quota_state=disabled` / `basis=btrfs_qgroups_dir_absent`. Only the longest-mount-point rule
distinguishes them. An implementation that resolves by "first candidate" or by "mount whose root
prefix matches" would emit `mount_point="/"`, `device_check=btrfs_subvolume_skipped` — same
quota verdict, wrong `mount_point`, and the real control fails while the verdict stays `0`.
The other eight path fields are robust to this error; `mount_point` is not.

**A2 — `noquota` must be matched as an exact key, not a substring (implementation hazard).**
`/tmp`'s super options contain `noquota`, whose text contains `quota`. Matching by substring
would see a quota key present together with `noquota` and take the
`xfs_conflicting_quota_options` row → `quota_state=unknown` → run verdict
`QUOTA_STATE_UNKNOWN` / exit 2 instead of exit 0. This is the single highest-impact parsing
hazard in the real control.

**A3 — btrfs `device_mismatch` must not be raised for the fleet root (implementation hazard).**
The fleet root's `st_dev` is `0:57` while the `/home` mount reports `0:30`. Under a non-btrfs
rule this mismatch would be `unknown` / `device_mismatch`; the contract explicitly exempts btrfs
(mismatch expected, `device_check=btrfs_subvolume_skipped`, classification continues). A
generic mismatch check placed before the fstype branch would turn the whole run into
`QUOTA_STATE_UNKNOWN` / exit 2.

**A4 — `/sys/fs/btrfs/features` is a non-uuid sibling directory.**
A naive glob of `/sys/fs/btrfs/*/` yields `features/` as well as the uuid. `features/` has no
`devices/` subdirectory and lists no device, so the "exactly one uuid lists `dm-0`" count is
unaffected — but a glob-based implementation that treats every `/sys/fs/btrfs/*/` entry as a uuid
candidate must tolerate entries without `devices/`. (For the record, `features/simple_quota`
exists, i.e. the *kernel* supports the simple-quota feature; enablement is still off — no
`qgroups` directory. Feature support must not be read as quota enabled.)

**A5 — coverage gap: the real control does not pin `quota_option_keys` or `btrfs_qgroups_mode`.**
The contract's output schema (§C2) includes both per path, but `expected_paths` pins only the
seven fields the oracle compares. The sealed fixture cases (`frozen/quota-cases/`) are therefore
the only place these two are constrained. Related ambiguity for the case authors: whether
`noquota` belongs in `quota_option_keys` for xfs is not stated in the contract table (the
sibling `SimplifyRules` seat's reading includes it in the xfs key set). The real control cannot
adjudicate this; the sealed cases must, or the ambiguity survives into the implementation.

**A6 — `btrfs_qgroups_mode` is null in the real control by construction.** The `qgroups` directory
does not exist, so `/sys/fs/btrfs/<uuid>/qgroups/mode` cannot be read and the field must be
`null` (not `""`, not an error string).

---

## 5. Saturation / honesty of the claim

The frozen file's `note` is honest about the control's nature and about drift: host state may
change (remount, quota enable) and a later differing run is a drift observation, not an oracle
rewrite. That matches the wave's "a later differing run is a drift observation, not an oracle
rewrite" clause and the bounds' "keep original evidence byte-unchanged".

Drift that would invalidate the frozen control (all outside the frozen file's fault, all
recorded here so L1 can classify a future divergence):

| Drift | Effect on a live run | Detectable by |
|---|---|---|
| `qgroups` dir appears under the uuid (btrfs quota enabled) | fleet root → `enabled`, run → exit 1 `QUOTA_ENABLED` | `ls -d /sys/fs/btrfs/*/qgroups` |
| `/tmp` remounted, or `noquota` dropped from its super options | `/tmp` → `unknown` or `enabled` | mountinfo line for `/tmp` |
| `/home` ceases to be a separate mount (e.g. plain `/` only) | `mount_point` becomes `/` | mountinfo census (R2) |
| `/tmp` or the fleet root replaced by another fstype | per-fstype table row applies | mountinfo |

No claim of exhaustive coverage is made here: this review covers exactly the real control
(`frozen/c2-expected-real.json`) against the permitted live reads. The sealed fixture cases and
the `oracle-quota.py` implementation were **not** falsified by this seat (no implementation exists
yet at `4dc80c1`), so C2's measured before/after (capability_absent → per-case match) remains
unmeasured by me.

---

## 6. Invariant checks from the reviewer role

- **One canonical runtime / same-identity rerouting.** C2 introduces a single new read-only tool
  (`tools/mori-quota-surface.py`) with one contract-defined CLI (`--path` / `--fixture` /
  `--selftest`). No second runtime, no alias, no rerouting path is pre-registered. Nothing in the
  frozen file implies a reroute. **No violation found.**
- **`resume_continuity_v1` (failed preflight ⇒ zero mutation).** C2 has **no resume path**: the
  probe is stateless and read-only, and the contract defines no preflight→resume state machine
  for it. The invariant is therefore not applicable to C2. (For the record,
  `resume_continuity_v1` appears in the round-14/15/18 material only; it is not part of round 23's
  C1/C2 surface.)
- **Honest saturation claims.** The frozen file claims a real control at one frozen moment with an
  explicit drift clause; it does not claim permanence, does not claim privacy clearance, does not
  claim quota is *not* configured on the host beyond what the visible surface shows. **No
  overstatement found.**

---

## 7. Residual risk / verification gaps

1. The frozen real control is a **single-host snapshot**; it pins two paths only. The tmpfs
   `usrquota` surface at `/dev/shm` is visible to a human but is not exercised by the default
   paths, so the real control cannot detect an implementation that mis-classifies tmpfs. That is
   left to the sealed fixture cases.
2. `quota_option_keys` and `btrfs_qgroups_mode` remain unverified here (A5, A6).
3. The "among equal mount points the last line wins" branch of the mount-resolution rule is not
   exercised by the real control (no duplicate mount points exist); it is only reachable from
   fixture cases.
4. The `xfs_quota_option` / `accounting_only` / `xfs_conflicting_quota_options` /
   `btrfs_qgroups_dir_present` / ext / tmpfs-enabled rows are all unexercised by the real
   control, by construction (both live paths are visibly quota-disabled).
5. I did not read the candidate implementation (none exists at `4dc80c1`) and did not read
   `oracle-quota.py`'s comparison semantics beyond what is needed to confirm the frozen file is
   consumable — I read that oracle's normalisation code, not any implementation under test.
6. `ls -d /sys/fs/btrfs/*/qgroups` also matched the non-uuid `features/` path; the frozen
   command list's phrasing is accurate for the uuid path and the extra `features` miss is
   harmless.

## 8. Files

- Read: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md`,
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/c2-expected-real.json`
  (worktree + `git show 4dc80c1:…`, identical),
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/SimplifyRules.md` (sibling report),
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/sources-start.txt`.
- Wrote: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/ReviewRealC2.md`
  (this file, my uniquely assigned report path).
- No production edits, no delegation, no background jobs, no VCS mutation in the lane.
