# QTmpfsNoQuota — round-23 falsification of the sealed C2 case `CaseTmpfsNoQuota`

Seat: `MadoR22-2.QTmpfsNoQuota` (leaf falsifier, round 23 wave 2).
Scope: **exactly one** sealed case, executed in **fixture mode only**. No real mode, no
host reads, no quota interface, no code edit, no expectation edit, no sibling write.

## 1. Identities (byte-exact, no aggregate-only claim)

| item | value |
|---|---|
| sealed case file | `.ufo/waves/round-23/frozen/quota-cases/CaseTmpfsNoQuota.json` |
| case sha256 (working copy) | `7afd98c191a799e52bb9ac01b896b23eaa855b9e02ef1bc3f901aa13a03a49b5` |
| case sha256 at seal `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` | `7afd98c191a799e52bb9ac01b896b23eaa855b9e02ef1bc3f901aa13a03a49b5` (identical — frozen bytes unchanged) |
| candidate executable | `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py` |
| tool sha256 (working copy) | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| tool blob sha256 at pinned production `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` (identical — the run used the pinned production bytes; `f3dc07c0` is an ancestor of lane HEAD `6eb889c0`) |
| fixture bytes written by me | sha256 `a30857dea2a8caeed5146698d67d25ef4c21780d2f65bd4ab9d3cafabdef81ec` — byte-identical to the fixture the measure4 driver built for this case (`evidence/measure4/c2-after-observed.json` → `fixture_sha256`) |
| receipt | `.ufo/waves/round-23/falsify/QTmpfsNoQuota/scan.json` |
| scratch | `/fast/scratch/hyaku/mori-r23/QTmpfsNoQuota/` |

The frozen case carries **no** `supplementary_expected` member: the six scored fields are the
whole scored surface of this case. Supplementary metadata below is observation only and is
**not** folded into the scored denominator.

## 2. Source derivation and amendment read before execution

- Derivation doc: `.ufo/waves/round-23/build/CaseTmpfsNoQuota.md` (author
  `MadoR22-2.CaseTmpfsNoQuota-8`; original proposal in `cases-proposed/CaseTmpfsNoQuota.json`,
  sha256 `f4814c94a8a0f330df82caa46ef1695318e5b3b297545e3b2b888519c4dd4dbb`).
- Authority chain: `contract.md` §C2 (frozen at `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`) +
  `preseal-amendment.md` "C2 final rules superseding only erroneous/ambiguous original clauses".
- Kernel anchors quoted by the case: **S084** `Documentation/filesystems/tmpfs.rst` v7.2 lines
  129–143 (the complete tmpfs quota option set: `quota`, `usrquota`, `grpquota`,
  `usrquota_block_hardlimit`, `usrquota_inode_hardlimit`, `grpquota_block_hardlimit`,
  `grpquota_inode_hardlimit`; source sha256 `5ce3dffe9323912b9146a5f33744776ff623ef42cf8accd6b2dfbea0b9db5be6`),
  **S082** `Documentation/filesystems/proc.rst` v7.2 §3.5 lines 1965–1990 (mountinfo field
  layout; source sha256 `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`).
  Both quotes are registered and word-found in `evidence/source-quotes.json`.
- The amendment narrows the contract's tmpfs wording: only the three quota flags and the
  **four documented** hardlimit keys count (an arbitrary `_hardlimit` suffix does not), and
  option *values* are never emitted. The frozen fixture contains none of those seven keys.

## 3. The single execution

Fixture mode only. `case["fixture"]` was copied verbatim into my own scratch file
(`fixture.json`, sha256 above) and handed to the candidate with `--fixture`:

```
cd /fast/scratch/hyaku/mori-r23/QTmpfsNoQuota
TMPDIR=/fast/scratch/hyaku/mori-r23/QTmpfsNoQuota \
timeout 15s prlimit --as=402653184 --cpu=15 -- \
  /usr/bin/python3 -I \
  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
  --fixture /fast/scratch/hyaku/mori-r23/QTmpfsNoQuota/fixture.json
```

- exit `0`; stderr empty (0 bytes); stdout is one JSON object, sha256
  `8bbf2b3ef09b701b845c0e0d1164e5b831cdd935be497a397e92f39e81d71113`.
- One child at a time; 384 MiB address-space cap; 15 s wall cap. No other case, no real
  mode, no `--selftest`, no driver, no build/lint/test run.
- Determinism: one repeat of the *same* case produced a byte-identical stdout
  (same sha256) and exit `0`.

## 4. Result — verdict: PASS (primary six-field denominator)

Exit code, `finding_id`, and both ordered six-field tuples match the frozen expectation
exactly. Twelve of twelve field values equal; no field differs; the tuple **order** is the
frozen order.

| # | path | fstype | mount_point | quota_state | enforcement | basis |
|---|---|---|---|---|---|---|
| 0 | `/run/user/1000` | tmpfs | /run/user/1000 | disabled | n/a | tmpfs_quota_options_absent |
| 1 | `/run/user/1000/mori` | tmpfs | /run/user/1000 | disabled | n/a | tmpfs_quota_options_absent |

Expected == actual for every cell above (frozen `expected.paths` vs observed `paths`).
`exit` 0 == 0, `finding_id` `QUOTA_DISABLED` == `QUOTA_DISABLED`.

**Supplementary metadata (observed, unscored — the case asserts none of it):**
`device_check` `match` / `match`; `quota_option_keys` `[]` / `[]`; `btrfs_qgroups_mode`
`null` / `null`. `quota_option_keys` empty is correct: the chosen tmpfs super options are
`rw,size=1622592k,nr_inodes=405648,mode=700,uid=1000,gid=1000,inode64`, whose keys are
`rw, size, nr_inodes, mode, uid, gid, inode64` — none of the seven documented quota keys,
and `size`/`nr_inodes`/`mode` are capacity and permission settings, not quota mechanisms.

## 5. Independent re-derivation (contract + amendment rules, no tool code)

Before trusting the tool output I re-derived the expectation from the frozen contract and
the amendment with my own resolver (`scratch/independent_check.py`, output kept in the
receipt under `independent_rederivation`). Result: **every derived row equals the frozen
expected row and the derived verdict equals the frozen verdict** (exit 0,
`QUOTA_DISABLED`). The derivation confirms, for both probed realpaths:

- covering mount points = `/`, `/run`, `/run/user/1000`, **each occurring exactly once** in
  the fixture, so the amendment's repeated-mountpoint refusal (`ambiguous_overmount`) is
  **not** triggered;
- longest component-prefix selection chooses mount id 31, mount point `/run/user/1000`,
  fstype `tmpfs` (the ext4 root, btrfs `/home`, xfs `/tmp`, proc and sysfs are shorter or
  unrelated);
- the amendment's **parent-ID topology check passes**: chosen mount id 31, parent id 30;
  the parent id is present in the snapshot and *is* the id of the longest strictly shorter
  covering mount `/run` (id 30) → no second `ambiguous_overmount` refusal;
- device check: chosen mount `0:52` == path `st_dev` `0:52` → `match` (tmpfs is not btrfs,
  so no major-0 skip applies);
- classification: no quota key among the tmpfs vocabulary → `disabled` / `n/a` /
  `tmpfs_quota_options_absent`; verdict precedence → exit 0 `QUOTA_DISABLED`.

This is the case where the amendment's stricter parent-ID rule **is** satisfied, in contrast
to the frozen `CaseEscapedSpace` contradiction (chosen id 43 / parent 33 while the longest
strictly shorter cover `/srv` is id 42), which the strict red owns.

## 6. Output discipline (checked, unscored)

- Output key set is exactly `{schema, finding_id, exit_code, paths, df_covers_quota, limits}`
  — no extra key, none missing; `schema` = `mori-quota-surface-v1`; `exit_code` 0 is
  consistent with the process exit 0; `df_covers_quota` is `false`.
- Every path row carries exactly the nine documented keys
  (`path, fstype, mount_point, quota_state, enforcement, basis, device_check,
  quota_option_keys, btrfs_qgroups_mode`).
- No leakage: none of the fixture's must-never-be-echoed strings appears in stdout — mount
  sources (`/dev/mapper/root`, `/dev/nvme0n1p3`, `/dev/nvme0n1p1`), full `key=value` option
  tokens, distinctive option values (`zstd:3`, `/@home`), the device basename `dm-0`, and
  the btrfs UUID `1d02a454-c549-4a35-b567-89d60902af8e` are all absent. No option value,
  mount source or UUID is echoed.

## 7. Honest scope, expected red, and residual risk

- **This seat adds no failure.** `CaseTmpfsNoQuota` passes on the primary six-field
  denominator, on exit, and on `finding_id`.
- The wave's **full-driver exit 1 is EXPECTED** and is caused by the frozen strict red in
  `CaseEscapedSpace` (sealed expectation vs the sealed parent-ID rule). That case is a
  different case, owned by seat `QEscapedSpace`; I did **not** execute it, did **not**
  exclude it, did **not** relabel it and did **not** excuse it. The frozen bytes of
  `CaseEscapedSpace` are untouched by this seat, and the contradiction recorded in
  `evidence/frozen-contradiction.json` stands exactly as sealed. My receipt adds no
  exception, no special case and no exclusion for it.
- Nothing was changed to make any count green: no source, expectation, oracle, frozen
  case or driver byte was touched. The only files I wrote are this report and my named
  synthetic receipt under `falsify/QTmpfsNoQuota/`, plus scratch under
  `/fast/scratch/hyaku/mori-r23/QTmpfsNoQuota/`.
- **Verification gaps / residual risk (explicitly not covered by this seat):**
  1. Real mode was not exercised — every live host read is forbidden for this seat, so the
     tool's real `/proc/self/mountinfo` + `/sys/fs/btrfs` path, the btrfs `qgroups/enabled`
     read, and the frozen real control (`c2-expected-real.json`) remain unverified here.
  2. Only the negative tmpfs direction was executed. The tmpfs *enabled* direction
     (`tmpfs_quota_option`, `enforced`) and the hardlimit vocabulary belong to
     `CaseTmpfsUsrquota` / `CaseTmpfsHardlimit`, which I did not execute.
  3. The `ambiguous_overmount` refusal path and the device-mismatch preemption were not
     exercised here; they are the subjects of other seats' cases.
  4. `QUOTA_DISABLED` is not a capacity or health verdict (ENOSPC can coexist) and this
     seat does not clear, admit or promote anything.
- Carried open debt is unchanged by this seat: the four unallowlisted inherited hits, the
  original permission control RED 11/12, the two unknown dispositions, the blocked baseline
  acceptance and `privacy_clearance=false`. Probe visibility and accounting consistency
  are not clearance, health or admission.

## 8. Tooling

No tool was installed or updated in this seat; no package transaction was performed (all
pacman transactions are paused host-wide for this wave). Only `python3` (system),
`timeout` and `prlimit` (coreutils/util-linux) were used.

## 9. Artifacts

- Receipt: `.ufo/waves/round-23/falsify/QTmpfsNoQuota/scan.json` — schema
  `mori-r23-falsify-scan-v1`, contains case/tool/fixture hashes, the exact argv and
  wrapper, exit code, full stdout and stderr, the per-row six-field comparison, the
  supplementary observation, the discipline checks, the independent re-derivation and the
  determinism record.
- Scratch (not part of the deliverable): `/fast/scratch/hyaku/mori-r23/QTmpfsNoQuota/`
  (`fixture.json`, `stdout.json`, `stdout2.json`, `stderr.txt`, `stderr2.txt`, `run.json`,
  `compare.py`, `independent_check.py`, `independent_check.json`, `scan.json`).
