# QTmpfsUsrquota — falsification of the sealed C2 case `CaseTmpfsUsrquota`

Wave: mori round 23 · claim: **C2** (coverage / FR2 quota-surface observability) ·
lane `/home/vgpnk/Projects/shokunin/mori-shokunin` · seat `MadoR22-2.QTmpfsUsrquota` ·
mode: **fixture only** (real mode never invoked).

**Verdict: MATCH.** The sealed case passes against the pinned production tool on exit,
`finding_id` and the ordered six-field tuple. 1/1 primary case matched; 9/9 sealed
supplementary checks passed (reported apart from the six-field denominator, not folded
into it). Zero mismatches.

Receipt: `.ufo/waves/round-23/falsify/QTmpfsUsrquota/scan.json`
(sha256 `c9a8764556df4968306cd8abf5a9efa097fda951b61cd7272056115d31ddca18`, 16496 bytes).

---

## 1. What was executed, exactly

One child, one case, fixture mode:

```
prlimit --as=402653184 --nofile=1024 --nproc=4096 --fsize=1048576 -- \
  timeout --signal=KILL 15s \
  python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
    --fixture /fast/scratch/hyaku/mori-r23/QTmpfsUsrquota/fixture.json
```

* argv as given: `python3 -I <tool> --fixture <abs fixture>`
* AS limit 402653184 B (= 384 MiB), timeout 15 s, one child at a time, `TMPDIR` inside
  this seat's scratch.
* `cwd` = `/fast/scratch/hyaku/mori-r23/QTmpfsUsrquota`.
* **No real-mode invocation.** `--path` and the bare (no-flag) real entry point were
  never used; no `--real-expected` was passed to the oracle.
* No `quotactl`/`ioctl`, no `btrfs qgroup`, no `xfs_quota`, no `repquota`, no `mount`,
  no qgroup/mode read, no host quota read of any kind.

**Wrapper deviation, stated plainly.** The first attempt used `--nproc=64` and the host
refused it: `timeout: fork system call failed: Resource temporarily unavailable` — the
account already owned 192 processes, so `RLIMIT_NPROC=64` blocked the fork before the
tool ever ran (exit 125, empty stdout, 67-byte stderr, both discarded as non-measurements).
The nproc ceiling was then raised to 4096 and the run repeated. The AS budget
(384 MiB), the 15 s timeout and the one-child discipline were **not** changed.

## 2. Byte identities (all read-only; none modified)

| artifact | sha256 | bytes | at pinned/seal revision |
|---|---|---|---|
| `tools/mori-quota-surface.py` (candidate) | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` | 66644 | identical at `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` (pinned production) and at HEAD `6eb889c`; `git diff f3dc07c HEAD -- tools/mori-quota-surface.py` is empty |
| `.ufo/waves/round-23/frozen/quota-cases/CaseTmpfsUsrquota.json` | `7ecc3503a5fd3aa4b6a1bb635ae34965f7a6f97466c4ff273e9bb836517ac800` | 5608 | identical at seal `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`; equals `frozen/case-decisions.json` `selected_sha256` and `frozen/seal-manifest.json` entry |
| `.ufo/waves/round-23/oracle-quota.py` (sealed oracle v3) | `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` | 25391 | identical at seal `22772c1`; equals the seal-manifest entry |
| scratch `fixture.json` (this seat) | `6fb72924706cb806ced46203135e322af10701a78b1109ccacc6cbb593ffdf74` | 922 | byte-identical to the fixture the sealed oracle itself serialized from the same `case["fixture"]` |

The frozen case is the **corrected** instance: `frozen/case-decisions.json` records
`original = cases-proposed/CaseTmpfsUsrquota.json`
(`6152062f45080ace9a1ca4b3121f15ebcb6ddc544f011a2a4e0c4e53959adc3f`, retained
unaltered) and `selected = cases-corrected/CaseTmpfsUsrquota.json` with the same
`7ecc3503…` hash as the frozen file. The only delta is the amendment-required
`qgroups_enabled: null` member on the single (inert, decoy) btrfs_sysfs record.

`git diff --stat` in the lane is empty: no tracked file was modified by this seat.

## 3. Measured result

stdout (957 bytes, sha256 `ff92522c618f5e37b29d51bdae4bdf294e3c3c47129d70e53f68e515a957207b`),
stderr empty (0 bytes, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`),
process exit **1**.

```json
{"schema":"mori-quota-surface-v1","finding_id":"QUOTA_ENABLED","exit_code":1,
 "df_covers_quota":false,
 "paths":[{"path":"/dev/shm","fstype":"tmpfs","mount_point":"/dev/shm",
           "quota_state":"enabled","enforcement":"enforced","basis":"tmpfs_quota_option",
           "device_check":"match","quota_option_keys":["usrquota"],"btrfs_qgroups_mode":null}],
 "limits":"…"}
```

## 4. Comparison — primary (six-field) denominator

Primary fields, in the sealed order: `path, fstype, mount_point, quota_state,
enforcement, basis`.

| # | field | expected (given, frozen) | actual (measured) | match |
|---|---|---|---|---|
| — | `exit` | 1 | 1 | ✅ |
| — | `finding_id` | `QUOTA_ENABLED` | `QUOTA_ENABLED` | ✅ |
| 0 | `path` | `/dev/shm` | `/dev/shm` | ✅ |
| 0 | `fstype` | `tmpfs` | `tmpfs` | ✅ |
| 0 | `mount_point` | `/dev/shm` | `/dev/shm` | ✅ |
| 0 | `quota_state` | `enabled` | `enabled` | ✅ |
| 0 | `enforcement` | `enforced` | `enforced` | ✅ |
| 0 | `basis` | `tmpfs_quota_option` | `tmpfs_quota_option` | ✅ |

Ordered tuple — expected `('/dev/shm','tmpfs','/dev/shm','enabled','enforced','tmpfs_quota_option')`
— actual identical. **1/1 primary case matched; 0 mismatches.**

## 5. Supplementary metadata (reported apart, NOT scored)

The case file declares **no** `supplementary_expected` block, so nothing below enters the
six-field denominator. It is reported for the record:

* `device_check` = `match` (mount major:minor `0:26` equals the path's `st_dev` `0:26`)
* `quota_option_keys` = `["usrquota"]` — the bare kernel-printed key only; no values,
  no other options
* `btrfs_qgroups_mode` = `null` (tmpfs path; the btrfs_sysfs record is an inert decoy)

Sealed supplementary checks, as evaluated by the sealed oracle on the same tool bytes:
**9 pass / 0 unmet** — `schema`, `exit_consistency`, `output_keys_allowed`,
`output_key_set`, `error_token`, `path_key_set`, `df_covers_quota`, `limits_text`,
`no_leakage`. The `no_leakage` check found **0** hits against the 18 canaries the
oracle derives from this fixture (the btrfs UUID, both `/dev/…` mount sources, the
`key=value` option tokens and distinctive values, and the `dm-0` device basename): no
mount source, option value, UUID or device basename is echoed in the output.

## 6. Sealed oracle run (one case only)

The sealed oracle `oracle-quota.py` (v3, `f1f4a027…`) was executed over a one-case
directory containing **only** `CaseTmpfsUsrquota.json`, with `--real-expected` **omitted**
so no real-mode read could occur:

```
python3 -I …/oracle-quota.py --tool …/tools/mori-quota-surface.py \
  --cases /fast/scratch/hyaku/mori-r23/QTmpfsUsrquota/onecase \
  --output /fast/scratch/hyaku/mori-r23/QTmpfsUsrquota/oracle-onecase.json
```

Oracle exit 0; `finding_id` `R23_C2_QUOTA_CASES_MATCH`; counts
`{total 1, pass 1, unmet 0, capability_absent 0}`; supplementary
`{total 9, pass 9, unmet 0}`. The oracle's own fixture serialization is byte-identical
to this seat's (`6fb72924…`), and the oracle recorded the same tool sha256
(`e4857413…`). The oracle's row headline: `exit_match true, finding_match true,
paths_match true`.

## 7. Independent re-derivation (the case is not vacuously satisfied)

A **separate** re-implementation of the amendment's mount-resolution, device-check and
tmpfs-classification rules was written from `contract.md` + `preseal-amendment.md` text
only — it did not call the tool — and run against the case fixture:

* Covering mounts for realpath `/dev/shm`: `/` (id 29, ext4) and `/dev/shm` (id 30, tmpfs).
  Each mount point occurs exactly once → no `ambiguous_overmount` refusal.
* Longest component-prefix wins → id 30, fstype `tmpfs`, mount point `/dev/shm`.
* Longest strictly shorter cover = id 29 (`/`); the selected mount's parent id (29) is
  present in the snapshot **and equals** that ancestor's id → the amendment's extra
  parent-id refusal does **not** fire.
* Mount device `0:26` == path `st_dev` `0:26` → `device_check` = match, no preemption.
* tmpfs super options `rw,nosuid,nodev,noexec,relatime,size=402653184k,usrquota` → the
  quota-key set `{quota,usrquota,grpquota}` + the four documented hardlimit keys
  intersects at exactly `{usrquota}` → `enabled` / `enforced` / `tmpfs_quota_option`.
* Verdict precedence: no setup error, one `enabled` path → exit 1, `QUOTA_ENABLED`.

Independent tuple == frozen tuple; independent verdict == frozen verdict. The frozen
expectation is therefore reproduced from the sealed rules, not merely echoed by the tool.

## 8. Discrimination probes (synthetic fixture-input variants, own scratch only)

Two scratch copies of the fixture (frozen bytes untouched; **no mutant tool was
built**, no source was modified) confirm the case actually discriminates:

| probe | change to the scratch fixture | measured verdict |
|---|---|---|
| **A** | bare `usrquota` token removed from the tmpfs super-options column | `QUOTA_DISABLED`, exit 0, `disabled`/`n/a`/`tmpfs_quota_options_absent`, `quota_option_keys []` |
| **B** | `usrquota` replaced by the undocumented `zz_hardlimit` token | `QUOTA_DISABLED`, exit 0, `disabled`/`n/a`/`tmpfs_quota_options_absent` |

Interpretation: the `enabled` verdict is caused by the `usrquota` key itself — not by the
tmpfs fstype, the mount point, the device match or the presence of a quota-shaped
superblock. Probe B additionally shows the tool honours the amendment's rule that an
arbitrary `_hardlimit` suffix is **not** sufficient; the case's plain `usrquota` flag is
what carries the classification. Both probes are diagnostics of the *case*, and neither
is scored.

## 9. Isolation evidence

`strace -f -e trace=openat,open,readlink,statx,newfstatat,getdents64` over one
identical fixture-mode run (strace log sha256 recorded in the receipt):

* **Quota- or host-state paths opened: none.** No `/proc/self/mountinfo`, no
  `/sys/fs/btrfs/*`, no `/dev/mapper/*` readlink, no qgroup attribute.
* The only non-interpreter file opened was the scratch fixture itself
  (`/fast/scratch/hyaku/mori-r23/QTmpfsUsrquota/fixture.json`).
* Remaining opens are Python interpreter startup only (`/etc/ld.so.cache`,
  `/proc/sys/fs/nr_open`, `/etc/localtime`, `/proc/self/maps`, `/usr/bin/pyvenv.cfg` →
  ENOENT).

Fixture mode is a genuine synthetic mode: the tool's output for this case is a pure
function of the fixture bytes.

**Determinism:** a second identical fixture-mode invocation produced byte-identical
stdout (`cmp stdout.txt stdout2.txt` → identical).

## 10. Findings, residual risk, verification gaps

**Findings.**

1. **No defect found in the candidate's handling of this case.** Exit, `finding_id` and
   all six primary fields match the frozen expectation; the sealed oracle agrees
   (1/1, 9/9 supplementary); the expectation was independently re-derived from the
   sealed rules; the case discriminates under two counterfactual fixture inputs; and
   fixture mode performs no host read.
2. **Observational note on the candidate's own history (not a defect in this case).**
   The production file `tools/mori-quota-surface.py` carries the *v3* source, whose
   module docstring still identifies it as "mori-quota-surface-v3.py" and says it was
   "authored alongside `mori-quota-surface.py` (the original, unaltered)". The sibling
   build variants remain under `.ufo/waves/round-23/build/ImplQuota/`
   (`mori-quota-surface.py` `6b553154…`, `-v2.py`, `-v3.py` `5199e97b…`) and all differ
   from production. The production bytes are the post-`f3dc07c` repaired classifier
   (`(state, enforcement, basis), mode = classify(...)`, the empty-path-population and
   extra-path-record-key setup guards, `limits` as a joined string) — i.e. the shipped
   file is the corrected descendant of the v3 candidate, and the stale docstring
   self-reference is a documentation artefact only. It does not affect any measured
   value in this case and I did not edit it (no code edits are in scope for this seat).
   Flagging it for the owner of the candidate source, since a stale self-description in
   a shipped tool is a maintenance hazard for the next round.
3. **Wave-level strict red is not mine and does not touch this case.** The frozen
   contradiction in `evidence/frozen-contradiction.json` concerns
   `CaseEscapedSpace` (selected mount id 43, parent id 33, longest shorter cover id 42
   `/srv` → the sealed parent-id rule requires `unknown`/`ambiguous_overmount`, while
   the frozen expectation says `enabled`). That is a different case file and a
   different seat. Nothing was excluded, relabelled, special-cased or rewritten for it
   here, and `CaseTmpfsUsrquota` shares no fixture, no mount topology and no rule with
   it. Its red remains a red for the driver.

**Residual risk.**

* The frozen case exercises one path and one filesystem family. It pins the tmpfs
  `usrquota` → `enabled`/`enforced`/`tmpfs_quota_option` mapping, the longest
  component-prefix mount selection, and the exit-1 `QUOTA_ENABLED` precedence, but it
  does **not** pin the btrfs, ext, xfs, `ambiguous_overmount`, `device_mismatch` or
  setup-error families; those are other seats' cases.
* `enforcement = "enforced"` describes the **mechanism flag** only. The fixture sets no
  limit and no limit is read, so this case cannot and does not evidence that any
  per-user quota limit exists on a real tmpfs.
* The btrfs_sysfs record in this fixture is an inert decoy (`qgroups: false` paired
  with `qgroups_enabled: null` / `qgroups_mode: null`, as the amendment requires). This
  case therefore says nothing about the btrfs `qgroups/enabled` witness path, and
  nothing about the real-mode `qgroups/mode` non-read.
* The `quota_option_keys` content is **unpinned by the case** (no `supplementary_expected`
  block). The measured `["usrquota"]` is consistent with the amendment's tmpfs key
  set, but the case does not score it, so a change there would not flip this case.
* The `usrquota` fixture shape is kernel-faithful per the case author's out-of-band
  check (upstream v7.2 `mm/shmem.c` prints the bare `usrquota` key into the superblock
  super-options column). That check is registered as *not* part of the derivation
  (`sources` = `["S082","S084"]`), and the S-id binding for S077–S084 remains
  provisional — those rows are still draft-only in
  `.ufo/waves/round-23/build/DraftSourceRows/rows.md` and `corpus/SOURCES.md` still ends
  at S076. If L1 renumbers them, the `sources` array of this case file changes; the
  six scored fields and the expectation do not.

**Verification gaps (not closable by this seat).**

* No real-mode run of this tool was performed by me (explicitly out of scope: only
  `RerunPinnedDriver` may perform the declared DEFAULT quota live reads, and I was told
  never to run real mode). The frozen real control
  `frozen/c2-expected-real.json` is therefore **not** verified by this seat.
* The wave-level `29/30` primary population and the strict `CaseEscapedSpace` red were
  not re-measured here; this seat's denominator is exactly one case.
* The 49/49 quota selftest arm (`evidence/quota-selftest-corrected.json`, exit 0
  `QUOTA_SELFTEST_OK` at `f3dc07c`) is a **separate arm** and is not conflated with
  this frozen case; I did not re-run it.
* The kernel-side `mm/shmem.c` anchor behind the fixture's option string is outside the
  registered S077–S084 set, so the fixture's realism rests on a doc-level anchor
  (S084 `tmpfs.rst` quota option table) plus an unregistered code check.

## 11. Hygiene

Writes made by this seat, and nothing else:

* `.ufo/waves/round-23/falsify/QTmpfsUsrquota.md` (this report)
* `.ufo/waves/round-23/falsify/QTmpfsUsrquota/scan.json` (the receipt)

Everything else lived under `/fast/scratch/hyaku/mori-r23/QTmpfsUsrquota/`
(`fixture.json`, `stdout.txt`, `stderr.txt`, `stdout2.txt`, `strace.txt`, `matrix.json`,
`onecase/`, `oracle-onecase.json`, the two probe fixtures and their outputs). No
`/tmp` use, no background job, no subagent, no `git add`/`commit`/`push`, no `jj`
mutation, no production/frozen/oracle/rule edit, no tool install or upgrade, no
credential or `agent.db` access, no session-transcript read, no quota/quotactl/btrfs/
xfs_quota/repquota/mount call, and no live qgroup or mode read.
