# QExt4NoOptions — falsification of sealed C2 case `CaseExt4NoOptions`

Seat: `MadoR22-2.QExt4NoOptions` (leaf falsifier, no delegation). Wave: round-23, attempt 1.
Scope: exactly one sealed C2 case, fixture mode only, real mode never invoked.
Verdict: **MATCH** — the sealed expectation is reproduced byte-for-byte on the primary
six-field tuples, on exit code and on `finding_id`. No mismatch, therefore no mismatch to
report. This case is **not** the wave's strict-red case (`CaseEscapedSpace`); this seat makes
no claim about that population number either way.

Receipt: `.ufo/waves/round-23/falsify/QExt4NoOptions/scan.json` (schema `mori-falsify-scan-v1`).

---

## 1. Case identity (frozen bytes, unmodified)

| field | value |
|---|---|
| case path | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/CaseExt4NoOptions.json` |
| case sha256 | `816a5d9d321c6188eddfa373c50b51c1e70a1784fe0db3a6fbd104768c542ee9` |
| case bytes | 4648 |
| seal commit blob sha256 | `816a5d9d321c6188eddfa373c50b51c1e70a1784fe0db3a6fbd104768c542ee9` — identical |
| case id | `CaseExt4NoOptions` |
| declared sources | `S082`, `S083` |
| scenario | two ext4 mounts whose super options carry no quota-related key → superblock quota feature unobservable → `unknown`, enforcement `n/a`, never `disabled` |

The frozen file is byte-identical to the blob at the expectation seal
`22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`. **No expected byte was edited**; the only file I
wrote under the lane is this report and my own receipt.

## 2. Derivation and amendment actually read (before executing)

* `contract.md` §C2 — mount resolution (lines 95–99), device check (100–103), quota
  classification table (105–122), output path-row key set (124–128), verdict precedence
  (132–135), limits text (137–140).
* `preseal-amendment.md` — the clauses that supersede the original C2 text: ext2/3/4 clause
  ("quota_state ALWAYS unknown, enforcement n/a"; basis `ext_quota_option_unverified` when a
  quota-related option key is present, otherwise the retained
  `ext_quota_superblock_unobservable`); mount-resolution clause (separator + last three fields
  of each line, octal escapes `040/011/012/134` only, longest component-prefix wins, refusal
  `ambiguous_overmount` when a covering mount point repeats, plus the parent-ID refusal);
  device-mismatch preemption (btrfs skips equality only when the stat major is `0`);
  fixture source resolution (raw decoded source → `device_links` → basename → uuid `devices`);
  fixture-shape rules (normalized unique absolute paths, canonical `MAJ:MIN`, canonical UUID
  keys, exact record key sets, `qgroups_enabled` member required).
* `build/CaseExt4NoOptions.md` — the case author's derivation and its appended pre-seal
  correction; `build/` source anchors S082 (`Documentation/filesystems/proc.rst` §3.5, field
  table `(1)…(m+4)`, super options at `:1983`) and S083
  (`Documentation/admin-guide/ext4.rst:261-265`: the `quota, noquota, grpquota, usrquota`
  flags "are ignored by the filesystem … used only by quota tools").
* Derivation chain: `cases-proposed/CaseExt4NoOptions.json` → `cases-corrected/…` (identical
  to the frozen file) → frozen. The only fixture-level delta from the original proposal is the
  added `qgroups_enabled: null` on the btrfs_sysfs record; the rationale/scenario were
  rewritten to cite the governing amendment clauses. **The expectation itself did not move**
  across the correction.
* `oracle-quota.py` — headline denominator is exit code + `finding_id` + ordered
  `(path, fstype, mount_point, quota_state, enforcement, basis)` tuples (lines 23–30);
  supplementary metadata is counted separately and never folded into that denominator.

## 3. Selected quota implementation examined

`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py`,
sha256 `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92`, 66644 bytes.
The working copy is byte-identical to the pinned production revision
`f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` and to the worktree head
`6eb889c037163e4886eaa61501258910d6a529b9` (same sha256 at all three), so the measured
artifact is the pinned production artifact.

Relevant code paths read before execution: `parse_mountinfo` (:311), `option_keys` (:347),
`quota_option_keys` (:360), `covering_mounts` (:407), `resolve_mount` (:421, longest-prefix +
repeated-mountpoint refusal + parent-ID refusal), `classify` (:487, ext branch at :505-510),
`evaluate` (:513, device-mismatch preemption), `verdict` (:552), `probe_fixture` (:681),
`load_fixture` (:695), `payload`/`setup_payload` (:762).

## 4. Execution (one case, one child at a time, fixture mode)

Fixture mode only; `--selftest` was **not** invoked; real mode was **not** invoked; no quota
host read (`quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota`, qgroups/mode) was performed by
this seat.

Scratch (own seat directory, never `/tmp`):
`/fast/scratch/hyaku/mori-r23/QExt4NoOptions/`
`TMPDIR=/fast/scratch/hyaku/mori-r23/QExt4NoOptions/`

`case["fixture"]` was copied verbatim (parsed from the sealed case bytes) to
`/fast/scratch/hyaku/mori-r23/QExt4NoOptions/fixture.json`
(scratch file sha256 `70e54ba7c8f301283ae8de7d9cff9f3fbbca998cde63a9f992241e736b91381b`;
canonical fixture sha256 `5e619535fba959dcc4bc21d92798ba60aa5954304f9a5cd14bb72d84e92e3fc2`).
The scratch fixture parses equal to `case["fixture"]`.

argv (exact):

```
timeout -s KILL 15 prlimit --as=402653184 --cpu=15 --nproc=64 python3 -I \
  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
  --fixture /fast/scratch/hyaku/mori-r23/QExt4NoOptions/fixture.json
```

* address space limit 402653184 bytes = 384 MiB; CPU limit 15 s; wall timeout 15 s (SIGKILL);
  `python3 -I` (isolated); cwd = seat scratch dir; one child, no background jobs.
* **exit 2**
* stdout 1173 bytes, sha256 `0c720c9e7a79cd8c9dd451173bbccef324b2a33ddb93e1f78a00cdf3db4ea9ac`
* stderr 0 bytes, sha256 `e3b0c44298fc1c299afbf4b8996fb92427ae41e4649b934ca495991b7852b855`
  (empty-file digest)

A second sequential run of the same case from cwd `/` produced a byte-identical stdout
(same sha256, exit 2, empty stderr): the result is deterministic and cwd-independent.

## 5. Result — primary scored comparison (six-field denominator)

Primary fields, in order: `path, fstype, mount_point, quota_state, enforcement, basis`.

| # | expected tuple | actual tuple | match |
|---|---|---|---|
| 0 | `("/srv/data", "ext4", "/srv", "unknown", "n/a", "ext_quota_superblock_unobservable")` | `("/srv/data", "ext4", "/srv", "unknown", "n/a", "ext_quota_superblock_unobservable")` | yes |
| 1 | `("/var/log", "ext4", "/", "unknown", "n/a", "ext_quota_superblock_unobservable")` | `("/var/log", "ext4", "/", "unknown", "n/a", "ext_quota_superblock_unobservable")` | yes |

* exit: expected `2`, actual `2` — match.
* `finding_id`: expected `QUOTA_STATE_UNKNOWN`, actual `QUOTA_STATE_UNKNOWN` — match.
* row order matches `expected.paths` order, which matches `fixture.paths` order.
* output `exit_code` field (2) equals the process exit status (2).
* output top-level key set exactly `{schema, finding_id, exit_code, paths, df_covers_quota,
  limits}`; no `error` key (so this is not a `QUOTA_SETUP` payload); `schema` =
  `mori-quota-surface-v1`; `df_covers_quota` = `false`; `limits` = fixed boundary text.
* output path-row key set exactly the nine allowed keys
  `{path, fstype, mount_point, quota_state, enforcement, basis, device_check,
  quota_option_keys, btrfs_qgroups_mode}`.

**Primary match: true.** The case passes; there is no mismatch to report, so nothing is
excused or re-labelled.

Actual output (parsed; `limits` verbatim in the receipt):

```json
{"df_covers_quota": false, "exit_code": 2, "finding_id": "QUOTA_STATE_UNKNOWN",
 "paths": [
  {"path": "/srv/data", "fstype": "ext4", "mount_point": "/srv", "quota_state": "unknown",
   "enforcement": "n/a", "basis": "ext_quota_superblock_unobservable",
   "device_check": "match", "quota_option_keys": [], "btrfs_qgroups_mode": null},
  {"path": "/var/log", "fstype": "ext4", "mount_point": "/", "quota_state": "unknown",
   "enforcement": "n/a", "basis": "ext_quota_superblock_unobservable",
   "device_check": "match", "quota_option_keys": [], "btrfs_qgroups_mode": null}],
 "schema": "mori-quota-surface-v1"}
```

## 6. Supplementary metadata — asserted apart, never folded into the primary denominator

Per `oracle-quota.py:23-30` the scored denominator is the six-field tuple list; the following
three fields are supplementary and are reported separately here (they are **not** part of the
case's frozen expectation, which asserts only the six primary fields):

| path | device_check | quota_option_keys | btrfs_qgroups_mode |
|---|---|---|---|
| `/srv/data` | `match` | `[]` | `null` |
| `/var/log` | `match` | `[]` | `null` |

These are consistent with the sealed rules: the ext super options carry only `rw` and
`errors`, so no quota-related key exists and `quota_option_keys` is empty; `btrfs_qgroups_mode`
is null because neither path resolves to the btrfs mount at `/home`.

## 7. Which sealed clauses this case actually exercised

| clause | exercised here | observed |
|---|---|---|
| longest component-prefix mount selection | yes | `/srv/data` → `/srv` (len 4) over `/` (len 1); `/var/log` → `/` only (`/home` is not a prefix) |
| repeated-covering-mountpoint refusal (`ambiguous_overmount`) | **no** | mount points `/`, `/home`, `/srv` each occur once; refusal correctly did not fire |
| parent-ID refusal | **no** | the `/srv` mount's parent id `29` **is** the id of the longest strictly shorter cover `/` (id `29`), so no refusal; `/var/log` has no shorter cover |
| device-mismatch preemption / btrfs major-0 skip | **no** | both `st_dev` values equal their chosen mount's `major:minor` (`8:2`, `8:1`) → `device_check: match`; the btrfs line is never selected |
| ext2/3/4 classification | yes | no quota-related key → `unknown` / `n/a` / `ext_quota_superblock_unobservable` (the retained arm) |
| ext `ext_quota_option_unverified` arm | **no** | no quota-related key present, so that basis is not reachable from this case |
| fixture source resolution (`device_links` → basename → uuid) | partially | `/dev/mapper/root` → `dm-0` matches the single uuid's `devices`; the btrfs record is a decoy here (never selected) |
| fixture shape validation | yes | fixture accepted: canonical uuid key, exact 4-key record set, `qgroups:false` paired with `enabled:null`/`mode:null`, canonical `MAJ:MIN`, normalized absolute unique paths |
| verdict precedence | yes | no `enabled` path, ≥1 `unknown` path → exit 2 `QUOTA_STATE_UNKNOWN` |
| output minimization | yes | no mount source (`/dev/sda1`, `/dev/sdb1`, `/dev/mapper/root`), no device basename (`dm-0`), no uuid, no option value (`errors=remount-ro`, `space_cache=v2`, `subvolid=5`), and no raw `MAJ:MIN` appears anywhere in stdout |

Independent corroboration that fixture mode read no host state: `/srv/data` does not exist on
this host (`os.path.exists('/srv/data') == False`) yet the tool returned a complete
classification for it, so no host `stat`/`realpath`/mountinfo/sysfs read contributed.
Source-level corroboration: `probe_fixture` (:681) calls only `load_fixture` (:695), which
opens only the fixture file; `real_inputs`/`scan_btrfs_sysfs` are on the real-mode branch only.

## 8. Findings by severity

**No behavioral defect was found for this case.** The two axes the case tests — (a) ext4
superblock-quota unobservability must never degrade to `disabled`, and (b) longest-prefix
mount resolution plus device-match gating on a decoy-bearing mountinfo — are both correct in
the measured production artifact.

### LOW — production module docstring self-identifies as a candidate (`tools/mori-quota-surface.py:2-8`)

The shipped file's module docstring opens `"""mori-quota-surface-v3.py — read-only
quota-surface probe (FR2 / EDQUOT).` and then states "This is the round-23 pre-seal amendment
candidate … authored alongside `mori-quota-surface.py` (the original, unaltered) and
`mori-quota-surface-v2.py`". In the production tree this file *is* `mori-quota-surface.py`, so
the deployed artifact describes itself as a differently-named candidate that was authored
beside a file at its own path. Evidence:

* `git ls-tree -r f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` → the only production path is
  `tools/mori-quota-surface.py`; the three named candidates live only under
  `.ufo/waves/round-23/build/ImplQuota/` (`mori-quota-surface.py`,
  `mori-quota-surface-v2.py`, `mori-quota-surface-v3.py`).
* The production file is **not** byte-identical to any of the three candidates
  (production `e48574…`; candidates `6b5531…`, `5c8b25…`, `5199e9…`): production carries the
  later classifier-unpacking repair (`(state, enforcement, basis), mode = classify(...)`),
  the stricter path-entry key check, `limits` as a joined string rather than a list, and the
  corrected selftest arms.
* Impact: no behavioral effect on this case (schema, exit, tuples all match); the risk is
  provenance/traceability — a reader of the shipped tool is told it is an unlanded candidate
  and is pointed at sibling files that do not exist next to it. The wave's own expectation
  that a shipped artifact describe its own identity is not met. The three candidate copies
  themselves are preserved as history under `build/ImplQuota/`, which is the right place for
  them; the production file's header should not claim to be one of them. **Reported, not
  edited** (no source edits are in scope for this seat).

### LOW — exit code 2 is overloaded between `QUOTA_SETUP` and `QUOTA_STATE_UNKNOWN`

The measured verdict for this case is exit 2 with `finding_id QUOTA_STATE_UNKNOWN`; the setup
failure path also exits 2 (`QUOTA_SETUP`). They are distinguishable only by `finding_id` /
the presence of the `error` key, which this case confirms is absent. This is exactly what the
sealed contract prescribes (precedence table, contract lines 132–135), so it is an observation
about the contract's exit-code vocabulary, not a defect in the tool — and this case's exit-2
is the **expected** verdict, not a failure indication. No change requested.

### INFORMATIONAL — `limits` payload type differs from the v3 candidate

The production tool emits `limits` as one joined string (611 chars here); the rejected v3
candidate emitted a JSON list. The sealed real control `frozen/c2-expected-real.json` does not
constrain the `limits` representation (no `limits` key in the control), and the case's oracle
compares only exit, `finding_id` and the six-field tuples, so nothing is violated. Recorded so
the parent knows the production artifact is not a byte-copy of any candidate.

## 9. Residual risk and verification gaps

1. **Population coverage is not established by this seat.** I executed exactly one case, as
   instructed. The wave-level C2 number (29/30 with the single strict red at
   `CaseEscapedSpace`) rests on `evidence/measure4-invocation.json` and the committed driver;
   my single-case result is consistent with it but does not independently confirm it, and it
   says nothing about the red. I do not excuse, exclude, relabel or re-derive that red.
2. **Unexercised sealed branches remain unexercised by me:** the ext
   `ext_quota_option_unverified` arm, the `ambiguous_overmount` refusal (repeated mount point
   and the parent-ID variant), the device-mismatch preemption, the btrfs enabled/disabled/
   unavailable arms, xfs precedence rows, tmpfs rows, octal-escape rejection, and every
   fixture-validation rejection path. Those are sibling seats' cases; my case only reaches the
   ext "no quota key" arm.
3. **No syscall-level trace of the fixture-mode read set.** The claim "fixture mode reads only
   the fixture file" is established by source reading plus the `/srv/data` non-existence
   argument, not by `strace`. `strace` is not installed on this host and all pacman
   transactions are paused host-wide, so no tool was installed (no install was performed by
   this seat).
4. **Real mode was not exercised and must not be** — it is outside this seat's authorization
   (`RerunPinnedDriver` owns the declared DEFAULT quota live reads). The real control
   `frozen/c2-expected-real.json` therefore remains unverified by me.
5. **Host-state drift.** The measurement used a frozen synthetic fixture, so the result is
   independent of host quota state; no drift caveat applies to this case (unlike the real
   control, whose own note says a later differing run is a drift observation).
6. **Case-authoring provenance gap, inherited:** `corpus/SOURCES.md` still ends at S076, so
   the `S082`/`S083` ids cited by this case are the wave's draft mapping, not registry rows.
   This affects the case's `sources` array only, not its expectation, and is outside my
   scope to fix.

## 10. Incident record (harness, not tool observations)

Two aborted attempts preceded the measurement; neither produced a tool observation and neither
is counted as a case result:

1. `prlimit … --timeout 15 …` — util-linux 2.42.4's `prlimit` has no `--timeout` option; it
   exited 1 with empty stdout/stderr before any child was started. Corrected by using
   `timeout -s KILL 15` as the outer wrapper (the argv in §4).
2. `prlimit --as=393216 …` — my own unit error: `prlimit --as` takes **bytes**, so this set
   384 KiB, not 384 MiB; the interpreter died with SIGSEGV (exit 139, empty stdout/stderr).
   Corrected to `--as=402653184` (384 MiB). The crash is an artifact of an over-tight address
   space limit, not of the tool.

Both attempts are also recorded in the receipt under `harness_incidents`.

## 11. Attestations

* Exactly one fixture-mode case was executed (`CaseExt4NoOptions`), one child at a time,
  384 MiB address space and 15 s limits; real mode never invoked; `--selftest` never invoked.
* No expected, oracle, frozen or production byte was edited; the frozen case hash still equals
  the seal-commit blob hash. No code edit was made anywhere.
* Only two lane paths were written: this report and
  `.ufo/waves/round-23/falsify/QExt4NoOptions/scan.json`. All heavy scratch lives under
  `/fast/scratch/hyaku/mori-r23/QExt4NoOptions/`; `/tmp` was not used.
* No quota interface was called and no actual qgroup/mode/quota state was read; no journal,
  journalctl, process/session probe, credential/auth file, `agent.db`, Documents or shell
  history was read; **no session transcript was read at all** this wave.
* No fleet-root writes, no sibling writes, no lane index/jj/refs touch, no subagent dispatch.
* This report asserts a case result only. It carries no claim of baseline acceptance, privacy
  clearance, quota-configuration authority, remediation or promotion; quota configuration and
  diagnosis remain operator/tsukuroi work.
