# Round-23 C2 falsification — seat `QSymlinkRealpath` (sealed case `CaseSymlinkRealpath`)

**Seat:** `QSymlinkRealpath` (read-only falsification seat, wave round-23, claim C2 coverage).
**Verdict:** **MATCH** — the pinned production tool reproduces the sealed expectation exactly for this one
fixture-mode case: exit `0`, `finding_id` `QUOTA_DISABLED`, and both ordered six-field tuples equal to the
frozen expectation. No production, frozen, oracle or expected byte was edited.

## 1. Scope and authorization

* Exactly one fixture-mode case was executed: `CaseSymlinkRealpath`.
  **Real mode was never invoked.** No `/proc/self/mountinfo` read, no `stat`/`realpath` on the host, no
  `quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota`, `mount`, write or remediation of any kind.
* One child at a time; address space capped at 384 MiB, wall clock capped at 15 s.
* Scratch, the fixture copy and the captured output all live under
  `/fast/scratch/hyaku/mori-r23/QSymlinkRealpath/` (never `/tmp`).
* Writes performed by this seat: this report and
  `.ufo/waves/round-23/falsify/QSymlinkRealpath/scan.json` only. No sibling, fleet, production, frozen or
  oracle path was touched; no `git add`/`commit`/`push`; no `jj` mutation; no subagent dispatch.

## 2. Pinned artifacts and byte identities

| artifact | path | sha256 |
|---|---|---|
| sealed case | `.ufo/waves/round-23/frozen/quota-cases/CaseSymlinkRealpath.json` | `275c360585a93e2f1bc7e2ded0f4cd42b07d5b0eeb16b9790d1980f456b0d07e` |
| selected case (decision record) | `.ufo/waves/round-23/cases-corrected/CaseSymlinkRealpath-final.json` | `275c360585a93e2f1bc7e2ded0f4cd42b07d5b0eeb16b9790d1980f456b0d07e` |
| tool at pinned production revision `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` | `tools/mori-quota-surface.py` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| tool in working tree | `tools/mori-quota-surface.py` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| fixture copy executed by this seat | `/fast/scratch/hyaku/mori-r23/QSymlinkRealpath/fixture.json` | `ba1491651f1f3936df2143996344ab559a8a7f75daa31136e8153891d5ee0617` |
| fixture bytes recorded by the sealed oracle run | — | `ba1491651f1f3936df2143996344ab559a8a7f75daa31136e8153891d5ee0617` |

* The working-tree tool is **byte-identical** to the pinned revision `f3dc07c` (same sha256), so the measured
  behaviour is the pinned production behaviour.
* The case file sha256 equals the value recorded in `frozen/case-decisions.json`
  (`selected_sha256` = `275c360585a93e2f1bc7e2ded0f4cd42b07d5b0eeb16b9790d1980f456b0d07e`) and in `frozen/seal-manifest.json`; the frozen bytes are the selected
  bytes. The superseded intermediates `cases-corrected/CaseSymlinkRealpath.json`
  (`ef8eeaa03fa2576d8c9e666acfa4b3c38f765d4cde0b6ff1cacda26a78e7eefb`, the self-inflicted
  `/tmp/mori-quota-target-dir` path rename) and `cases-proposed/CaseSymlinkRealpath.json`
  (`e7c4018a4044827873520dbcddc17508258122c97a23c2a3017a45020a772473`) were left untouched and were **not**
  executed.
* The fixture copy is `case["fixture"]` serialized as `json.dumps(fixture, indent=2, sort_keys=True) + "\n"`;
  it hashes to the same digest the sealed oracle recorded (`ba1491651f1f3936df2143996344ab559a8a7f75daa31136e8153891d5ee0617`), so the exact bytes the sealed oracle
  fed to the tool are the bytes this seat fed to the tool.

## 3. Invocation (argv preserved verbatim)

```
prlimit --as=402653184 -- timeout -k 2 15 \
  /usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
  --fixture /fast/scratch/hyaku/mori-r23/QSymlinkRealpath/fixture.json
```

| field | value |
|---|---|
| exit code | `0` |
| timed out | no (timeout exit `124` not observed) |
| signal | none |
| stderr | empty (0 bytes, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`) |
| stdout | 1205 bytes, sha256 `55808286de04cf7e09b30b99fc7aa29010b00d4c610ca7bc2bbd686b9d636a0d` (verbatim below) |
| cwd | `/fast/scratch/hyaku/mori-r23/QSymlinkRealpath` |
| env override | `TMPDIR=/fast/scratch/hyaku/mori-r23/QSymlinkRealpath` |
| limits | AS 402653184 B (384 MiB), wall 15 s, kill-after 2 s |

Verbatim stdout:

```json
{"df_covers_quota":false,"exit_code":0,"finding_id":"QUOTA_DISABLED","limits":"no per-user, per-group or per-project limit or usage is read. no NFS or server-side quota and no overlay or fuse quota is covered. a visible btrfs qgroups directory does not imply that any limit is set. an ext2/ext3/ext4 quota feature in the superblock is unobservable without privileged tools. sysfs and mountinfo races during quota enable, disable or remount are not excluded. df capacity percentages never cover quota exhaustion (FR2 / EDQUOT). QUOTA_DISABLED is not a capacity or health verdict; ENOSPC can coexist. the btrfs qgroups mode attribute is never read, so btrfs_qgroups_mode is null in real mode.","paths":[{"basis":"xfs_noquota_option","btrfs_qgroups_mode":null,"device_check":"match","enforcement":"n/a","fstype":"xfs","mount_point":"/tmp","path":"/home/vgpnk/Projects/shokunin/link-to-tmp","quota_option_keys":["noquota"],"quota_state":"disabled"},{"basis":"xfs_noquota_option","btrfs_qgroups_mode":null,"device_check":"match","enforcement":"n/a","fstype":"xfs","mount_point":"/tmp","path":"/tmp/mori-quota-target","quota_option_keys":["noquota"],"quota_state":"disabled"}],"schema":"mori-quota-surface-v1"}
```

## 4. Primary comparison — exit, finding_id, ordered six-field tuples

Denominator preserved exactly as sealed: **exit code + `finding_id` + ordered
`(path, fstype, mount_point, quota_state, enforcement, basis)` tuples**. The six-field denominator is not
redefined, widened or narrowed by this report.

| field | given (sealed expectation) | actual (this run) | match |
|---|---|---|---|
| exit | `0` | `0` | yes |
| finding_id | `QUOTA_DISABLED` | `QUOTA_DISABLED` | yes |

Given rows (sealed):

| # | path | fstype | mount_point | quota_state | enforcement | basis |
|---|---|---|---|---|---|---|
| 0 | `/home/vgpnk/Projects/shokunin/link-to-tmp` | `xfs` | `/tmp` | `disabled` | `n/a` | `xfs_noquota_option` |
| 1 | `/tmp/mori-quota-target` | `xfs` | `/tmp` | `disabled` | `n/a` | `xfs_noquota_option` |

Actual rows (this run):

| # | path | fstype | mount_point | quota_state | enforcement | basis | row match | per-field |
|---|---|---|---|---|---|---|---|---|
| 0 | `/home/vgpnk/Projects/shokunin/link-to-tmp` | `xfs` | `/tmp` | `disabled` | `n/a` | `xfs_noquota_option` | yes | basis=ok, enforcement=ok, fstype=ok, mount_point=ok, path=ok, quota_state=ok |
| 1 | `/tmp/mori-quota-target` | `xfs` | `/tmp` | `disabled` | `n/a` | `xfs_noquota_option` | yes | basis=ok, enforcement=ok, fstype=ok, mount_point=ok, path=ok, quota_state=ok |

Ordered comparison of the two tuple lists: **equal** (row count given `2` = row count actual `2`,
order preserved, no row dropped or duplicated).

Verdict precedence re-derived from the actual rows: both rows are `disabled`, therefore no `enabled` and no
`unknown` row exists, therefore exit `0` with `QUOTA_DISABLED` — the observed exit/`finding_id` are the
precedence-correct ones, not a coincidence.

## 5. Supplementary observations (reported separately, never folded into the six-field denominator)

The sealed case file deliberately carries **no** `supplementary_expected` block: the amendment keeps the
original six-field denominator intact and puts the supplementary metadata in the case report only. The values
below are therefore *observations*, checked against the rationale-stated values, and are **not** part of the
scored comparison.

| # | path | device_check | quota_option_keys | btrfs_qgroups_mode |
|---|---|---|---|---|
| 0 | `/home/vgpnk/Projects/shokunin/link-to-tmp` | match | ["noquota"] | null |
| 1 | `/tmp/mori-quota-target` | match | ["noquota"] | null |

The rationale states `device_check` `match` for both rows, `quota_option_keys` `["noquota"]` for both rows and
`btrfs_qgroups_mode` `null` for both rows: all three observed values equal them. `quota_option_keys` is
sorted, contains only the quota-related key `noquota`, and carries no option **values**; `btrfs_qgroups_mode`
is `null` as required for a non-btrfs mount.

Output-shape and leakage checks (also supplementary, all satisfied):

* top-level key set exactly `{df_covers_quota, exit_code, finding_id, limits, paths, schema}` — no
  `error` token was emitted (not a setup error).
* `schema` = `mori-quota-surface-v1`; `exit_code` field = `0`, consistent with the process exit `0`;
  `df_covers_quota` = `false`.
* per-path key set exactly the nine allowed keys for both rows.
* leakage: 24 canaries derived from the fixture (the btrfs UUID, both full mount sources, every
  `key=value` super-option token, distinctive option values, and the `dm-0` device basename) — **0 hits** in
  stdout. No mount source, no option value, no UUID and no device basename was echoed.

## 6. Static discrimination analysis (no execution; explains *why* the case is a real test)

Computed directly from the fixture's own `mountinfo` text and `paths`:

* parsed mounts: `21 /proc`, `22 /sys`, `23 /dev`, `25 /` (btrfs), `65 /home` (btrfs), `82 /dev/shm`
  (tmpfs), `244 /tmp` (xfs, `259:1`, super options `rw,inode64,logbufs=8,logbsize=256k,noquota`).
* covering mounts of the **realpath** `/tmp/mori-quota-target` are `/` (id 25) and `/tmp` (id 244); longest
  wins → `/tmp` (xfs). Every covering mount point occurs exactly once, so the amendment's
  `ambiguous_overmount` refusal is not triggered.
* the `/tmp` mount's `parent_id` is `33`, and **33 is not a mount id present in the snapshot** (ids are
  21, 22, 23, 25, 65, 82, 244). Per the amendment, a missing parent id is unknown topology and must **not**
  trigger the extra overmount refusal. The tool implements exactly that (`best.parent_id in known` guard), so
  the case's expected outcome depends on that clause and is consistent with it.
* device check: chosen fstype is xfs (not btrfs) and its `259:1` equals both rows' `st_dev` `259:1` →
  `device_check` `match`, no `device_mismatch` preemption.
* quota classification: super-option keys `{rw, inode64, logbufs, logbsize, noquota}`; `noquota` is present
  alone, with no quota/enforcement/noenforce key, so the amended XFS precedence selects
  `disabled / n/a / xfs_noquota_option`.
* **Discriminating power:** a resolver that resolved the mount from the *given* path instead of the realpath
  would take `/home` (id 65, btrfs, `0:30`) for row 1, and since `st_dev` is `259:1` (nonzero major, so no
  btrfs subvolume skip) it would report `device_check` `mismatch`, `quota_state` `unknown`,
  `basis` `device_mismatch` — a different tuple, so the case would fail. Row 2 has `path == realpath` and is
  therefore a consistency pin (both paths reach the same mount and must report the same five
  mount-derived fields under their own given path), not a second discriminating row.

## 7. Findings by severity

No blocking, major or minor defect was found for this case; the sealed expectation is reproduced exactly.

* **INFO-1 — supplementary metadata is not machine-asserted in the sealed case file.** `device_check`,
  `quota_option_keys` and `btrfs_qgroups_mode` exist only in the case rationale prose; the sealed file
  asserts only the six-field primary tuple. This is the amendment's explicit instruction (keep the original
  denominator separate), not a defect, but it means the three supplementary values are only pinned by this
  seat's observation, not by the sealed oracle's case file.
* **INFO-2 — the parent-id overmount refusal branch is not exercised here.** The `/tmp` mount's parent id
  `33` is absent from the snapshot, so the "parent id present in the snapshot but not the longest strictly
  shorter cover" refusal is never entered by this fixture. Its coverage must be attributed to another case.
* **INFO-3 — only row 1 discriminates realpath-vs-given-path resolution.** Row 2's given path equals its
  realpath, so an implementation that resolved from the given path would still match row 2 and fail only
  row 1. The ordered two-row comparison therefore carries one discriminating row, not two.
* **INFO-4 — the btrfs branch is never entered.** The chosen mount is xfs, so `classify_btrfs` is not called;
  the fixture's `btrfs_sysfs` record is exercised only by the fixture validator (exact record key set,
  `qgroups` false paired with `qgroups_enabled` null and `qgroups_mode` null). The btrfs enabled/disabled/
  unavailable states are not covered by this case.
* **INFO-5 — rule-dependency worth recording.** This case's expected result is sensitive to the amendment
  clause "a missing parent id remains unknown topology but does not trigger this extra refusal". An
  implementation that refused on an absent parent id would report
  `unknown / n/a / ambiguous_overmount` here and fail — correctly, since the sealed expectation says
  otherwise. The clause is exercised here only in its permissive direction.

## 8. Residual risk and verification gaps

* **Single-case coverage.** This seat executed exactly one fixture case, as authorized. Nothing here speaks
  for the other 29 sealed quota cases, for the fixture-validation branches, or for the driver-level count
  (the wave brief records the driver-level state as 29/30 with the one unmet case being `CaseEscapedSpace`,
  which is a different seat's subject and is not re-measured, re-scored or excused here).
* **Real mode unexercised.** The real-mode path (host `mountinfo`, `stat`, `realpath`, btrfs sysfs reads) is
  untested by this seat, and by contract only the pinned driver may perform the declared default real reads.
  The frozen real control `frozen/c2-expected-real.json` is therefore not corroborated by this seat.
* **Rule-branch gaps listed above** (parent-id refusal, btrfs qgroups states, ext classification, tmpfs
  hardlimits, xfs conflict/absent, no-cover/ambiguous preemption) are outside this one case.
* **The adversarial question this seat could not close:** whether some *other* fixture could make the tool
  resolve from the given path while still satisfying this case. This seat ran no mutants (read-only seat; no
  clone, no mutant repository, no extra child beyond the single authorized fixture invocation), so the
  discrimination claim above is analytic, not mutation-proven. `CaseSymlinkRealpath` is *by construction*
  discriminating for the given-path/realpath confusion, but that is a property of the fixture, not a
  demonstrated failure of any specific alternative implementation.
* **Host state drift:** the run is a pure function of the sealed fixture bytes and the pinned tool bytes; both
  are recorded by digest above, so the result is reproducible independently of current host mount state.

## 9. `CaseEscapedSpace` (explicitly out of this seat's scope)

The wave brief states that the frozen `CaseEscapedSpace` row (selected `/srv` parent 43 versus a shorter
`/srv` 42 conflict) is expected to stay red under the strict rule and that the full driver exit `1` is
therefore expected. That case was **not** executed by this seat — my authorization covers exactly one
fixture-mode case — and this report neither excuses nor re-scores it. It is recorded here only so the parent
integrator does not read this seat's green as contradicting the strict driver red. The quota selftest arm
(49/49 after the separate co-evolved fixture input correction) is a different arm from the frozen
`CaseEscapedSpace` case and was likewise not run here.

## 10. Tool / install record

* No package was installed or updated by this seat; no `pacman` transaction was attempted (all pacman
  transactions are paused host-wide). Nothing in the task required a new tool.
* Pre-existing tooling used, with versions: `/usr/bin/python3` **3.14.8**; `/usr/bin/prlimit` —
  util-linux **2.42.4**; `/usr/bin/timeout` — GNU coreutils **9.12**; `git` **2.56.0** (read-only
  `show`/`status`/`rev-parse`/`log` against the lane repository).

## 11. Receipt

Machine-readable receipt: `.ufo/waves/round-23/falsify/QSymlinkRealpath/scan.json`
(schema `mori-r23-falsify-seat-receipt-v1`), carrying the verbatim argv, exit, stdout, stderr, the
tool/case/fixture digests, the given-vs-actual six-field tuples per row, the separate supplementary
observations, the leakage canary list and the verdict.
