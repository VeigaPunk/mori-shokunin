# CaseBtrfsQgroup — C2 fixture case (btrfs qgroups enabled, mode "qgroup")

Seat: `MadoR22-2.CaseBtrfsQgroup-8` · item: `CaseBtrfsQgroup` · wave r23-w1 · claim **C2**
Case file (the only file written): `.ufo/waves/round-23/cases-proposed/CaseBtrfsQgroup.json`
Independence: derived **only** from `.ufo/waves/round-23/contract.md` §C2 and the kernel sources
named in the contract (proc.rst §3.5, fs/btrfs/sysfs.c, fs/btrfs/qgroup.c, fs/btrfs/inode.c).
No candidate implementation, no `build/ImplQuota/`, no `build/OracleQuota/`, no host probe was
read or run. No tools were installed (none needed).

## 1. Scenario and fixture

One path, one btrfs subvolume mount, one uuid, qgroups on in `qgroup` mode.

- `mountinfo`: five lines in proc.rst §3.5 field order (`ID parent MAJ:MIN root mountpoint
  mountopts [optional...] - fstype source superopts`):
  - `25 30 0:30 / / rw,relatime shared:1 - btrfs /dev/mapper/root rw,space_cache,subvolid=257,subvol=/`
  - `26 25 0:30 /@home /home rw,relatime shared:1 - btrfs /dev/mapper/root rw,space_cache,subvolid=256,subvol=/@home`
  - `27 25 0:31 / /proc … - proc proc rw`, `28 25 0:32 / /sys … - sysfs sysfs rw`
  - `29 25 0:33 / /tmp … - xfs /dev/mapper/data rw,attr2,inode64,noquota` (decoy; does not cover the path)
- `paths`: one entry `/home/quota/data`, `realpath` identical, `st_dev` `0:57`.
- `device_links`: `{"/dev/mapper/root": "dm-0"}`.
- `btrfs_sysfs`: one uuid `7e764e88d285609904089ade096888407eee028fe10b7df43dbe1d954c153d19`
  with `devices: ["dm-0"]`, `qgroups: true`, `qgroups_mode: "qgroup"`.

The uuid string is a fixed literal in the file (not host-derived); the fixture is synthetic and
the probe's `--fixture` mode reads no host state.

## 2. Derivation, step by step

**(a) Mount resolution.** Contract §C2 lines 96–100: candidate mounts are those whose mount
point equals the realpath, is `/`, or is a path prefix of the realpath; the **longest** mount
point wins (ties: last line). For realpath `/home/quota/data` the candidates are `/` (root) and
`/home`; `/home` is longer, so the chosen mount is the second line:
fstype `btrfs`, mount point `/home`, major:minor `0:30`, source `/dev/mapper/root`.
→ expected `fstype = "btrfs"`, `mount_point = "/home"`.

**(b) Device check.** Contract lines 100–103: for a non-btrfs fstype, `st_dev ≠ major:minor`
would give `unknown` / `device_mismatch`; **for btrfs a mismatch is expected** (per-subvolume
anonymous `st_dev`) and is only recorded as `device_check: "btrfs_subvolume_skipped"`.
Here `0:57 ≠ 0:30`, so the mismatch is benign and the quota classification still runs.
The kernel basis is S081 = `fs/btrfs/inode.c:8246` `stat->dev = BTRFS_I(inode)->root->anon_dev;`
— a btrfs subvolume reports its own anonymous device, not the superblock's.
`device_check` is **not** one of the six compared expected keys, so it does not enter `expected`;
it is still the branch this fixture exercises (an implementation that wrongly applied the
non-btrfs `device_mismatch` rule to btrfs would fail this case).

**(c) Quota classification.** Contract table row (line 115):
`btrfs | source basename maps to exactly one uuid whose qgroups is true | enabled | unknown | btrfs_qgroups_dir_present`.
The device basename for the mount source is `dm-0` (fixture `device_links` models the real-mode
`os.path.realpath(mount_source) basename` step; on this host `/dev/mapper/root` → `/dev/dm-0`).
Exactly one uuid lists `dm-0`, and its `qgroups` flag is `true` → the row applies.
→ `quota_state = "enabled"`, `enforcement = "unknown"`, `basis = "btrfs_qgroups_dir_present"`.

Kernel anchors behind the fixture's btrfs facts:
- S079 = `fs/btrfs/sysfs.c`: `qgroup_enabled_show` (`/sys/fs/btrfs/<uuid>/qgroups/enabled`,
  lines 2355–2368) and `qgroup_mode_show` (lines 2370–2395), whose `BTRFS_QGROUP_MODE_FULL`
  branch emits exactly `qgroup` — the fixture's `qgroups_mode` text is this literal, and
  `BTRFS_QGROUP_MODE_SIMPLE` emits `squota` (the sibling case's mode).
- S080 = `fs/btrfs/qgroup.c`: `btrfs_sysfs_add_qgroups()` is called at `qgroup.c:441` and
  `qgroup.c:1032` when qgroup support is turned on and `btrfs_sysfs_del_qgroups()` at
  `qgroup.c:620/:689/:1295` when it is turned off; `fs/btrfs/sysfs.c:2586` creates
  `/sys/fs/btrfs/<uuid>/qgroups/`. So "`qgroups` dir present" ⇔ qgroup support enabled — the
  fact the contract's basis name `btrfs_qgroups_dir_present` encodes.
- S082 = `Documentation/filesystems/proc.rst` §3.5 (lines ~1965–1990): the field list used to
  parse the fixture's mountinfo lines, including that the super options are the **last** field
  and that optional fields sit between field 6 and the `-` separator.

**(d) Verdict.** Contract lines 132–135: setup error → 2 `QUOTA_SETUP`; else any `enabled` →
1 `QUOTA_ENABLED`; else any `unknown` → 2 `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED`.
The single path is `enabled`, so → `exit = 1`, `finding_id = "QUOTA_ENABLED"`.

**(e) Self-check performed on the fixture** (pure text parsing of my own file, no probe run):
every mountinfo line splits into ≥10 fields with exactly one `-` at position ≥7 and three fields
after it; the longest-prefix rule selects `/home`; `device_links["/dev/mapper/root"] == "dm-0"`;
exactly one uuid lists `dm-0` and it has `qgroups: true`.

## 3. Expected (as written in the case file)

```
exit 1, finding_id "QUOTA_ENABLED"
paths[0] = {path: "/home/quota/data", fstype: "btrfs", mount_point: "/home",
            quota_state: "enabled", enforcement: "unknown",
            basis: "btrfs_qgroups_dir_present"}
```

All tokens are verbatim from the contract table / verdict list; no invented token appears.

## 4. Contract ambiguities found (for the critic and L1)

1. **"source basename" vs. the real-mode input list.** The quota table says the *source
   basename* maps to a uuid; the real-mode input list (§C2 lines 77–80) says the resolved
   name is `os.path.realpath(mount_source) basename`, and the fixture format provides
   `device_links` to model that resolution. On a `/dev/mapper/root` source these differ:
   raw basename `root`, resolved basename `dm-0`. The fixture's `device_links` key is the full
   device path and its value the resolved name, so the case assumes lookup by *resolved*
   basename. An implementation that instead compared the **raw** basename (`root`) against
   `btrfs_sysfs[*].devices` would classify this path `unknown` / `btrfs_device_unmapped` and
   fail. The contract's own example fixture (`device_links {"/dev/mapper/root":"dm-0"}`,
   `devices:["dm-0"]`) supports the resolved reading, but the table wording "source basename"
   is loose enough to be worth a one-line clarification in the frozen text.
2. **`enforcement` token for btrfs.** The btrfs-enabled row uses `unknown` while the disabled /
   unmapped btrfs rows use `n/a`, and `unknown` is also a legal *quota_state* value. The two
   columns are therefore not drawn from disjoint vocabularies, and a reader could mistake
   `enforcement: "unknown"` for an unknown quota state. The expected object keeps the two
   fields distinct (quota_state `enabled`, enforcement `unknown`), which is what the contract
   table prescribes; the semantic ("btrfs qgroup presence ≠ enforcement of any limit", stated
   in the limits paragraph) supports `unknown` rather than `enforced`.
3. **"exactly one uuid whose `qgroups` is true" vs. "zero or several uuids list the device".**
   The three btrfs rows can be read as (i) count uuids listing the device, then read that
   uuid's flag, or (ii) count uuids with `qgroups: true`. This fixture contains exactly one
   uuid overall, so both readings coincide and the case is robust either way; the ambiguity
   only bites in the two-uuid case and should be disambiguated there.
4. **`device_check` is outside the compared tuple.** The oracle compares only
   `(path, fstype, mount_point, quota_state, enforcement, basis)`, so the `device_check` value
   itself is unobservable in a sealed case. This case still pins the *consequence* of a btrfs
   `st_dev` mismatch (classification proceeds, `btrfs_qgroups_dir_present`), which is the
   observable part; the `btrfs_subvolume_skipped` / `match` distinction remains unverified by
   the sealed-case mechanism and would need a separate assertion if it is to be held.
5. **Real-mode read set vs. this fixture.** The real-mode inputs include the *directory
   listing* of `/sys/fs/btrfs/<uuid>/devices/` and the *existence* of
   `/sys/fs/btrfs/<uuid>/qgroups`; the fixture models both with `btrfs_sysfs[*].devices` and
   `btrfs_sysfs[*].qgroups` (a boolean). The fixture cannot express a uuid whose `qgroups`
   directory exists but whose `enabled` attribute reads `0`, or a `mode` file that is absent
   while `qgroups` is true — the real kernel exposes `qgroups/enabled`, `qgroups/mode`,
   `qgroups/inconsistent` as separate attributes under the same directory. The boolean
   `qgroups` flag in the fixture therefore conflates "the qgroups directory exists" with
   "qgroup support is on", which the real sysfs does not guarantee to be the same thing.
   Not fatal for this case (both are true here), but it is a real ceiling on fixture
   expressiveness and worth stating in the limits text.
6. **Mode text is not a classification input.** The contract's btrfs rows classify on the
   `qgroups` boolean only; `qgroups_mode` is reported in the output
   (`btrfs_qgroups_mode`) but never changes `quota_state`/`basis`. Hence `qgroup` and `squota`
   (both full qgroup support) produce the same verdict and the same `basis`, differing only in
   the reported mode string. The sibling `CaseBtrfsSquota` case is therefore expected to have
   an identical expected tuple apart from the mode text, which is not a compared key — worth
   confirming that is intended before sealing both.

## 4a. CORRECTION (appended after `.ufo/waves/round-23/preseal-amendment.md`, before any candidate
## was opened or any C2 result observed)

**Corrected case file:** `.ufo/waves/round-23/cases-corrected/CaseBtrfsQgroup.json` (same
`id` = `CaseBtrfsQgroup`). The original proposal `cases-proposed/CaseBtrfsQgroup.json` is left
**byte-unchanged** as history; both are sealed as separate records.

### 4a.1 Delta applied to my case

| # | Amendment rule | Change in the corrected case |
|---|---|---|
| 1 | "Add required fixture member `qgroups_enabled` to each btrfs_sysfs UUID record: true/false/null" | uuid record now carries exactly `devices`, `qgroups`, `qgroups_enabled`, `qgroups_mode`; `qgroups_enabled: true` |
| 2 | "Present plus enabled=true → enabled/unknown/`btrfs_qgroups_enabled`" | `basis` changed `btrfs_qgroups_dir_present` → **`btrfs_qgroups_enabled`**; `quota_state` `enabled` and `enforcement` `unknown` unchanged |
| 3 | "UUID keys canonical UUIDs" | key changed from the 64-hex `7e764e88d285…c153d19` (a btrfs fsid shape) to canonical **`7e764e88-d285-6099-0408-9ade09688840`** |
| 4 | "Fixture source resolution: lookup RAW decoded source in `device_links`; use its mapped basename when present, otherwise basename(source)" | unchanged fixture already satisfies it: raw source `/dev/mapper/root` → `device_links` → `dm-0` → matches the single uuid's `devices` list |
| 5 | "Device mismatch PREEMPTS the filesystem table … Btrfs skips equality only when stat major is 0" | the path's stat major **is 0** (`st_dev 0:57`, the anonymous btrfs subvolume device), so the btrfs skip applies and the mismatch against mount `0:30` does **not** preempt the btrfs table; the path still classifies as `enabled`. Had the stat major been nonzero, the expected tuple would have become `unknown`/`n/a`/`device_mismatch` |
| 6 | "Parse separator and the last THREE fields of EACH chosen line"; "ignore empty trailing lines" | the fixture's five lines all carry `-` plus exactly three trailing fields; the trailing newline is ignored, so no change to the expected tuple |
| 7 | "if ANY covering mountpoint occurs more than once → unknown/n/a/`ambiguous_overmount`, fstype=null, mount_point=null" | the covering mountpoints here are `/` and `/home`, each occurring **once** in the file, so the refusal does not trigger; `fstype`/`mount_point` stay `btrfs`/`/home` |
| 8 | "ext2/3/4: quota_state ALWAYS unknown … basis `ext_quota_option_unverified`" | not applicable — this case is btrfs only |
| 9 | "duplicated-covering-point case becomes unknown/null fstype+mountpoint/ambiguous_overmount" | not applicable — this case has no duplicated covering point |
| 10 | "Paths nonempty, unique, normalized absolute … st_dev canonical decimal MAJ:MIN" | already conformant: one path `/home/quota/data`, realpath identical, no dot/dotdot components, `0:57` canonical |

### 4a.2 Corrected expectation

```
exit 1, finding_id "QUOTA_ENABLED"
paths[0] = {path: "/home/quota/data", fstype: "btrfs", mount_point: "/home",
            quota_state: "enabled", enforcement: "unknown",
            basis: "btrfs_qgroups_enabled"}
```

Six scored fields only — unchanged set, unchanged `path`/`fstype`/`mount_point`/`quota_state`/
`enforcement`; only `basis` was renamed by the amendment. Supplementary facts implied by this
case (not part of the six-field tuple): `device_check` = `btrfs_subvolume_skipped` (stat major 0
skip), `quota_option_keys` = `[]` (btrfs mechanism is sysfs, not options; the super options
`rw,space_cache,subvolid=256,subvol=/@home` carry no quota key), `qgroups_mode` = `qgroup`
(informational; real mode reads `qgroups/enabled` first and reads mode only when enabled is 1,
which holds here).

### 4a.3 Re-derivation under the amended rules (self-check, no implementation read, nothing run)

1. **Covering set.** Realpath `/home/quota/data`; candidate mountpoints = `/` (root) and `/home`
   (component prefix). Neither mountpoint string occurs twice across the five records → no
   `ambiguous_overmount`. Longest component-prefix wins → `/home`.
2. **Line parsing.** Chosen line `26 25 0:30 /@home /home rw,relatime shared:1 - btrfs
   /dev/mapper/root rw,space_cache,subvolid=256,subvol=/@home`; separator `-` present; last
   three fields = `btrfs`, `/dev/mapper/root`, `rw,space_cache,subvolid=256,subvol=/@home`.
   No backslash escapes, so no escape rejection.
3. **Device gate.** fstype is btrfs and stat major is 0 → skip equality → no preemption →
   btrfs table row applies. (Non-btrfs fstypes would still preempt on mismatch.)
4. **Device → uuid.** Raw decoded source `/dev/mapper/root` found in `device_links` → `dm-0`;
   exactly one uuid lists `dm-0` → zero/multiple-match refusal does not apply.
5. **btrfs row.** Record: `qgroups` (directory present) = true, `qgroups_enabled` = true →
   `enabled` / `unknown` / `btrfs_qgroups_enabled`. `qgroups_mode` `qgroup` is carried through
   as informational only.
6. **Verdict.** Single path, enabled, no unknown sibling → exit `1`, finding_id
   `QUOTA_ENABLED`.

Kernel anchors unchanged: S079 = `fs/btrfs/sysfs.c` (`qgroup_enabled_show` 2355–2368,
`qgroup_mode_show` 2370–2395 emitting `qgroup` for `BTRFS_QGROUP_MODE_FULL`, `btrfs_sysfs_add_qgroups`
2586); S080 = `fs/btrfs/qgroup.c` (`btrfs_sysfs_add_qgroups` call sites 441 and 1032,
`btrfs_sysfs_del_qgroups` 620/689/1295 — i.e. the qgroups directory exists from *initialization*,
which is exactly why the amendment separates presence from `enabled`); S081 = `fs/btrfs/inode.c`
(inode.c:8246 `stat->dev = BTRFS_I(inode)->root->anon_dev` — the anonymous-subvolume device whose
major is 0); S082 = `Documentation/filesystems/proc.rst` §3.5 field layout.

### 4a.4 How the amendment resolves the ambiguities I reported in §4

| §4 ambiguity | Amendment disposition |
|---|---|
| 1. "source basename" vs. realpath basename | **Resolved** — "lookup RAW decoded source in `device_links`; use its mapped basename when present, otherwise basename(source)" |
| 2. `enforcement: "unknown"` token overlap with `quota_state` | **Resolved** — the btrfs rows now name enforcement explicitly per row (`unknown` for enabled, `n/a` for disabled/unknown) |
| 3. "exactly one uuid whose `qgroups` is true" vs. "uuids list the device" | **Resolved** — device→uuid matching is by the mapped basename against UUID `devices` lists; zero/multiple matches stay unknown |
| 4. `device_check` outside the compared tuple | **Kept as a supplementary check** — the amendment adds `device_check`, `quota_option_keys`, `qgroups_mode` to the supplementary sealed checks, separate from the six-field denominator |
| 5. fixture `qgroups` boolean conflates "dir exists" with "enabled" | **Resolved** — a required `qgroups_enabled` member now separates initialized from enabled, and directory-absent vs. inspection-error are distinguished |
| 6. `qgroups_mode` is not a classification input | **Confirmed** — "Mode remains informational"; additionally real mode may read mode only when `enabled` is 1 |

### 4a.5 Residual notes carried forward (amendment-relative)

- The six scored fields remain the denominator; my case asserts nothing about `device_check`,
  `quota_option_keys` or `qgroups_mode` as *scored* values — those are supplementary sealed
  checks per the amendment, and this case is consistent with them.
- The amendment's btrfs rule set has no row for "qgroups directory absent but the parent listing
  failed" other than the explicit "A parent sysfs permission/listing error is unknown, NEVER
  absent/disabled"; my case cannot exercise that (its uuid record is complete), so the
  absent/permission distinction stays untested by this seat.
- `qgroups_mode` remains informational in the classification: a `squota` sibling case would
  produce the identical six-field tuple apart from the mode text, which is not scored.

## 4b. SUPPLEMENTAL CASES (appended after L1's supplemental request; still before any candidate
## was opened and before any C2 result was observed)

Two new preseal supplemental cases authored under `cases-supplemental/`, covering the two btrfs
states that the corrected `CaseBtrfsQgroup` does not reach. Originals and the corrected file are
untouched (hashes in §4b.4).

### 4b.1 `SupplementQgroupDisabled`

File: `.ufo/waves/round-23/cases-supplemental/SupplementQgroupDisabled.json`

| fixture field | value |
|---|---|
| `btrfs_sysfs["3c8f5a71-4d92-4b60-9e17-2a6c85d0f3b4"]` | `devices: ["dm-0"]`, `qgroups: true`, `qgroups_enabled: false`, `qgroups_mode: null` |
| `device_links` | `{"/dev/mapper/root": "dm-0"}` |
| path | `/home/quota/disabled`, realpath identical, `st_dev "0:57"` |
| mountinfo | same five-line btrfs/proc/sys/xfs layout as the corrected case |

**Expected:** exit `0`, finding_id `QUOTA_DISABLED`, path tuple
`path=/home/quota/disabled, fstype=btrfs, mount_point=/home, quota_state=disabled,
enforcement=n/a, basis=btrfs_qgroups_disabled`.

Derivation: covering mountpoints for the realpath are `/` and `/home`, each appearing once, so no
`ambiguous_overmount`; longest component-prefix → `/home`; fstype `btrfs` from the line's last
three fields (`btrfs`, `/dev/mapper/root`, `rw,space_cache,subvolid=256,subvol=/@home`). The path's
stat major is **0** (the anonymous btrfs subvolume device, S081 `inode.c:8246
stat->dev = BTRFS_I(inode)->root->anon_dev`), so the btrfs equality skip applies and the mismatch
against the mount's `0:30` does not preempt the btrfs table — a nonzero stat major would have
produced `unknown`/`n/a`/`device_mismatch` instead. Raw source `/dev/mapper/root` → `device_links`
→ `dm-0`; exactly one uuid record lists `dm-0`, so the zero/multiple-match refusal does not
apply. The record's qgroups directory is present (initialized) but `qgroups_enabled` is **false**,
which is exactly the amendment's row *Present plus enabled=false → disabled/n/a/
`btrfs_qgroups_disabled`*; directory presence alone would have meant only *initialized*, which is
why the enabled attribute is now a required fixture member. `qgroups_mode` is null because real
mode reads `qgroups/enabled` first and reads mode only when enabled is 1 — and the kernel's mode
reader is additionally guarded by `ASSERT(btrfs_qgroup_enabled(fs_info))` (S079
`qgroup_mode_show`), so mode must not be consulted for a disabled qgroups state. Kernel support:
the enabled bit is read exactly 0/1 by `qgroup_enabled_show` from
`BTRFS_QGROUP_STATUS_FLAG_ON` (S079 `fs/btrfs/sysfs.c:2355-2368`); the directory's existence is
the initialization artifact of `btrfs_sysfs_add_qgroups` (S080 `fs/btrfs/qgroup.c:441`, `:1032`;
creation in `sysfs.c:2586`) with removal by `btrfs_sysfs_del_qgroups` (`qgroup.c:620`, `:689`,
`:1295`), so directory presence and enabled state are distinct facts. Verdict: no enabled and no
unknown path → exit `0`, `QUOTA_DISABLED` (per the amendment's boundary text, not a capacity or
health verdict).

### 4b.2 `SupplementQgroupUnknown`

File: `.ufo/waves/round-23/cases-supplemental/SupplementQgroupUnknown.json`

| fixture field | value |
|---|---|
| `btrfs_sysfs["5b1d7e04-9a36-4f82-8c05-3e7f2b9d6a15"]` | `devices: ["dm-0"]`, `qgroups: true`, `qgroups_enabled: null`, `qgroups_mode: null` |
| `device_links` | `{"/dev/mapper/root": "dm-0"}` |
| path | `/home/quota/unknown`, realpath identical, `st_dev "0:58"` |
| mountinfo | same five-line layout |

**Expected:** exit `2`, finding_id `QUOTA_STATE_UNKNOWN`, path tuple
`path=/home/quota/unknown, fstype=btrfs, mount_point=/home, quota_state=unknown,
enforcement=n/a, basis=btrfs_qgroups_enabled_unavailable`.

Derivation: identical mount-resolution and device-gate chain as §4b.1 (covering `/` and `/home`,
each once → no `ambiguous_overmount`; longest prefix `/home`; stat major 0 → btrfs skip, no
preemption; raw source → `dm-0` → exactly one matching uuid record). The distinguishing state is
`qgroups_enabled: null`, which the amendment defines as an unreadable or invalid enabled
attribute, so the row *Present plus enabled=null (unreadable/invalid enabled) → unknown/n/a/
`btrfs_qgroups_enabled_unavailable`* applies. This is deliberately **not** the
`btrfs_qgroups_dir_absent` row, which the amendment permits only on a successful parent
inspection, and it must never be reported as disabled. `qgroups_mode` is null because mode is
read only when enabled is exactly 1 — with enabled null the attribute is not consulted at all, and
the kernel's mode reader is guarded by `ASSERT(btrfs_qgroup_enabled(fs_info))` (S079
`qgroup_mode_show`), so no trustworthy mode text exists in this state. Verdict: the single path is
unknown with no enabled sibling → exit `2`, `QUOTA_STATE_UNKNOWN`. The exit code alone does not
separate this from a setup error (also exit 2); the finding_id does (`QUOTA_SETUP` vs
`QUOTA_STATE_UNKNOWN`), and a setup error additionally yields `paths=[]` with a fixed error
token, whereas this case produces a classified path tuple.

### 4b.3 Shared fixture-format conformance (both supplemental cases)

Top-level keys exactly `schema`/`id`/`scenario`/`fixture`/`expected`/`rationale`/`sources`;
`fixture` keys exactly `schema`/`mountinfo`/`paths`/`device_links`/`btrfs_sysfs`; each uuid record
exactly `devices`/`qgroups`/`qgroups_enabled`/`qgroups_mode` with bool / bool-or-null /
mode-or-null types; canonical UUID keys; one nonempty, unique, normalized absolute path with an
identical realpath and no dot/dotdot components; canonical decimal `MAJ:MIN` st_dev with no
signs or leading zeros; plain nonempty device basenames with no slashes; no quota key in the
btrfs super options, so `quota_option_keys` is empty by the btrfs rule. Sources cited: S079, S080.

### 4b.4 Hashes and preservation

```
38a7d5b94f8b08ddee9c7080cca8786db0cc6aa8423dcef75d8250c58d462188  cases-corrected/CaseBtrfsQgroup.json
f117bcb0b411cb2dd50910c62222481d8d283eeb49ff2169b40788b24dd09567  cases-supplemental/SupplementQgroupDisabled.json
22f77b779845660b131dc0b19f3e02ddf203165734dfda040c52f08a06755f56  cases-supplemental/SupplementQgroupUnknown.json
b7ae7632aca4f30a6defc9a5a41d9f5c6fac49dfe2ca21a18f09933e3387581e  cases-proposed/CaseBtrfsQgroup.json  (untouched)
```

Report hash (this file, after appending §4b) is recomputed at the end of the turn and reported to
L1; the report is edited after hashing the case files, so the case hashes above are final.

## 5. Boundaries observed

- Files written by this seat: the original proposal
  `.ufo/waves/round-23/cases-proposed/CaseBtrfsQgroup.json` (left byte-unchanged as
  history), the corrected case `.ufo/waves/round-23/cases-corrected/CaseBtrfsQgroup.json`
  and the two supplemental cases `.ufo/waves/round-23/cases-supplemental/SupplementQgroupDisabled.json`
  and `.ufo/waves/round-23/cases-supplemental/SupplementQgroupUnknown.json`
  (explicitly authorized output paths), and this report. No production code, no
  `tools/` change, no delegation, no background jobs, no test/build/lint execution.
- No VCS mutation in the lane (read-only inspection only).
- No `quotactl`, `btrfs`, `xfs_quota`, `repquota`, `mount` or any privileged/mutating command;
  no live host probe of the quota surface was performed.
- No credential, agent.db or session-transcript access; `/proc/self/mountinfo` was not read
  (the fixture's mountinfo is hand-authored from proc.rst §3.5 field layout).
- Tool installs: none (no tooling was required for this task).
