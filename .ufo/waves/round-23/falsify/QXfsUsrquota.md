# Round-23 falsification seat QXfsUsrquota — sealed C2 case `CaseXfsUsrquota`

Seat: `MadoR22-2.QXfsUsrquota` (round-23, wave-2 falsification of the pinned C2 quota-surface probe).
Scope: **one** sealed fixture-mode case, `CaseXfsUsrquota`, executed exactly once against the pinned
production candidate. No real-mode probe, no `quotactl`/ioctl/`btrfs qgroup`/`xfs_quota`/`repquota`,
no mount, no write to any host path, no build, no lint, no full driver, no selftest execution, no
subagent dispatch.

Verdict for this seat: **PASS — the case reproduces exactly.** No blocking defect inside the
authorised scope. Two documentation-level observations are recorded below (severity: low, no
behavioural effect). The frozen `CaseEscapedSpace` red is **not** excused and **not** re-adjudicated
here; it remains a reported mismatch at parent level.

---

## 1. Case, source derivation and sealed bytes

| Item | Value |
|---|---|
| Case id | `CaseXfsUsrquota` (scenario: xfs mount whose super options carry the kernel token `usrquota`, no `noquota`, probed at the mount point and at a nested directory) |
| Frozen case file | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/CaseXfsUsrquota.json` |
| Case sha256 | `3e1620f745d7a1cc6fa497b1f61f991539809cd1bde67f86b73860baaaa4244b` (8139 bytes) |
| Seal cross-check | identical to `frozen/seal-manifest.json` entry for that path **and** to `frozen/case-decisions.json` `selected_sha256` for `CaseXfsUsrquota` |
| Original proposal | `cases-proposed/CaseXfsUsrquota.json`, sha256 `a8dc0a29e9c59256a861ede854e1907ec79b5a513d1d31768b72a37792afab19`, retained unaltered; decision entry marks it `primary: true`, reason "Independent source-derived pre-measurement correction; exact author bytes, no L1 expectation edits" |
| Delta vs proposal | exactly one fixture member: the decoy btrfs UUID record gains `qgroups_enabled: null`, paired with `qgroups: false` / `qgroups_mode: null` as the pre-seal amendment requires. **No expected value changed.** |
| Expected bytes | **unmodified** by this seat; the file was opened read-only and its sha256 was re-checked after execution |
| Sources cited by the case | S077 (`Documentation/admin-guide/xfs.rst` v7.2, option vocabulary), S078 (`fs/xfs/xfs_super.c` v7.2, emitted token semantics), S082 (`Documentation/filesystems/proc.rst`, mountinfo field layout) |

Independent re-derivation against the frozen rules (contract §C2 + `preseal-amendment.md`) confirms the
sealed expectation is reachable and is not a result-shaped artefact:

* **Mount resolution.** Two mountinfo lines: `29 25 0:30 /@root / … btrfs /dev/mapper/root …` (mount
  point `/`) and `31 29 259:2 / /srv/xfsquota … - xfs /dev/nvme0n1p2 rw,attr2,inode64,logbufs=8,logbsize=32k,usrquota`
  (mount point `/srv/xfsquota`). Each covering mount point occurs exactly once, so the
  `ambiguous_overmount` refusal cannot fire. The longest covering mount point is `/srv/xfsquota` for
  both probed paths (equality for `/srv/xfsquota`, component-prefix for `/srv/xfsquota/projects/data`).
  The chosen line's parent id is `29`, which is exactly the mount id of the longest strictly shorter
  covering mount (the `/` btrfs line), so the amendment's parent-consistency refusal also does not fire.
  The btrfs line is a decoy that is never selected.
* **Device check.** Chosen fstype is `xfs` (not btrfs) and the mount's `259:2` equals the paths'
  `st_dev` `259:2`, so no device mismatch preemption applies.
* **XFS precedence.** Super options split on commas give keys `rw, attr2, inode64, logbufs, logbsize,
  usrquota`; no `noquota`, so neither the conflict nor the noquota branch applies; `usrquota` is an
  enforced key → `quota_state=enabled`, `enforcement=enforced`, `basis=xfs_quota_option`.
* **Verdict.** Both probed rows are enabled → exit `1`, `finding_id=QUOTA_ENABLED`; positive evidence is
  not hidden by any unknown sibling.
* **Carried ambiguity (unchanged, not resolved by me).** `enforced` records the filesystem-level
  enforcement flag (S078: `,usrquota` is printed exactly when `XFS_UQUOTA_ENFD` is set), **not** the
  existence of any per-user/per-group limit or an armed EDQUOT. The case's own rationale records this
  as an ambiguity for L1; the tool's stated limits text concedes the same. This seat does not widen the
  claim.

## 2. Tool under test

| Item | Value |
|---|---|
| Candidate executable | `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py` |
| sha256 | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| Production pin | `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` |
| Pin check | `git -C <repo> rev-parse f3dc07c0…:tools/mori-quota-surface.py` = `439ff4c1a68fc4f98182c6b855b3b4c790286851` = `git hash-object tools/mori-quota-surface.py` → the working copy **is** the pinned production bytes (the later `6eb889c` commit changes no tool byte: `git diff f3dc07c0 -- tools/` is empty) |
| Mode | **fixture mode only** — `--fixture` given, no `--path`, no host filesystem read; the btrfs sysfs scan and `/proc/self/mountinfo` were never read |

## 3. Execution (given vs actual)

* **Given by the assignment:** `python3 -I TOOL --fixture ABS_FIXTURE` invoked through `prlimit`/`timeout`,
  one child at a time, 384 MiB address space, 15 s wall timeout, scratch under
  `/fast/scratch/hyaku/mori-r23/QXfsUsrquota/`, `TMPDIR` set to that directory, never `/tmp`.
* **Actual argv:** `prlimit --as=402653184 -- timeout 15 python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py --fixture /fast/scratch/hyaku/mori-r23/QXfsUsrquota/fixture.json`
* **cwd / TMPDIR:** `/fast/scratch/hyaku/mori-r23/QXfsUsrquota`
* **Children:** 1 (single case, single execution; no repetition run)
* **Fixture input:** `case["fixture"]` copied into my own scratch as `fixture.json` (file sha256
  `ca36a3e3c0e00498db9dbd20c073e6435b4f338c9be244308555bb02dd287880`; canonical JSON sha256
  `6b239e862d585db9ab3ed12c71cf43d31c5d756be2f50e6f19ccee57c9391db6`; content equality with
  `case["fixture"]` asserted in code, not by inspection)
* **Exit:** `1`
* **stdout:** 1205 bytes, sha256 `8ad79edd49988a3764bc5dd7a5aeda801b657972dc0bc596dfc49235be10073e`
  (one JSON object, `schema=mori-quota-surface-v1`)
* **stderr:** empty (0 bytes, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`)
* **Toolchain:** Python 3.14.8, `prlimit` from util-linux 2.42.4, coreutils `timeout`. **No tool was
  installed or updated by this seat** (nothing in the assignment needed a new tool), so no install
  record exists.

## 4. Primary comparison — exit, finding_id, ordered six-field tuples

`exit`: expected `1` / actual `1` → **match**
`finding_id`: expected `QUOTA_ENABLED` / actual `QUOTA_ENABLED` → **match**
Path count: expected `2` / actual `2`, same order.

| # | path | fstype | mount_point | quota_state | enforcement | basis |
|---|---|---|---|---|---|---|
| 0 | `/srv/xfsquota` | `xfs` ✔ | `/srv/xfsquota` ✔ | `enabled` ✔ | `enforced` ✔ | `xfs_quota_option` ✔ |
| 1 | `/srv/xfsquota/projects/data` | `xfs` ✔ | `/srv/xfsquota` ✔ | `enabled` ✔ | `enforced` ✔ | `xfs_quota_option` ✔ |

All 12 primary field comparisons match (6 fields × 2 rows), in fixture path order. **Primary result:
PASS.** The primary denominator is the six-field tuple set; supplementary metadata is reported apart
and never folded into it.

## 5. Supplementary metadata (observed, **not** scored)

The frozen case carries **no** `supplementary_expected` key, so no supplementary assertion is scored
for this case; the following are recorded as observed-only.

| path | device_check | quota_option_keys | btrfs_qgroups_mode |
|---|---|---|---|
| `/srv/xfsquota` | `match` | `["usrquota"]` | `null` |
| `/srv/xfsquota/projects/data` | `match` | `["usrquota"]` | `null` |

`device_check=match` and `quota_option_keys=["usrquota"]` are consistent with the sealed
amendment rules; `btrfs_qgroups_mode=null` is correct here because the btrfs decoy record is never
selected (and, in fixture mode, mode is projected only when `qgroups_enabled` is true).

Output shape: top-level keys exactly `{schema, finding_id, exit_code, paths, df_covers_quota, limits}`;
path-row keys exactly `{path, fstype, mount_point, quota_state, enforcement, basis, device_check,
quota_option_keys, btrfs_qgroups_mode}`; `df_covers_quota=false`; `limits` a non-empty string. No
`error` token (not a setup error).

**Leakage check.** Substring scan of stdout for fixture-derived values that must never be echoed
(mount sources `/dev/nvme0n1p2` / `/dev/mapper/root`, the btrfs UUID, full `key=value` option tokens
`compress=zstd:3`, `logbufs=8`, `logbsize=32k`, and distinctive values/ device basenames `dm-0`,
`ssd`, `attr2`, `inode64`, …): **zero hits**. One apparent hit, `xfsquota/projects`, is a substring of
the case's own probed path, which the output is required to echo — discarded as a false positive and
recorded as such in the receipt.

## 6. Findings

### Blocker / major / minor
**None.** Inside the authorised scope (this one sealed case, fixture mode) the candidate reproduces
the sealed expectation byte-for-byte on every scored field, with a clean stderr and no output-shape
or leakage violation.

### Low severity — documentation / provenance only, no behavioural effect

**L1 — the shipped file's own docstring describes a family of sibling files that the shipped tree does
not contain, and names itself differently from its path.**
`tools/mori-quota-surface.py` (sha256 `e4857413…`) opens with `"""mori-quota-surface-v3.py — …"""`
and describes itself as "the round-23 pre-seal amendment candidate … authored alongside
`mori-quota-surface.py` (the original, unaltered) and `mori-quota-surface-v2.py` (preserved as the
rejected unsafe-read source evidence)". In the shipped tree, `tools/` contains only
`mori-quota-surface.py`; the named siblings exist only as wave-build artefacts under
`.ufo/waves/round-23/build/ImplQuota/` (`mori-quota-surface-v2.py` sha256 `5c8b251d…`,
`mori-quota-surface-v3.py` sha256 `5199e97b…`). The shipped bytes are also **not** the v3 draft: the
diff (`diff -u build/ImplQuota/mori-quota-surface-v3.py tools/mori-quota-surface.py`, 76 diff lines)
shows the four later production deltas — the `classify` return-shape fix
(`(state, enforcement, basis), mode = classify(...)`), the fixture-validation tightening
(non-empty `paths` list, exact path-record key set), `limits` changed from a list to a
`". ".join(LIMITS) + "."` string, and the co-evolved public-selftest input corrections
(`escaped-mount-point` arm now `st_dev="259:2"`, plus the two new setup arms
`setup-empty-path-population` / `setup-extra-path-record-key`). Those deltas are the round-23
history recorded in `corpus/lessons/round-23.md` (the `classify` unpacking counterexample, the
declared input guards, the co-evolved selftest device correction) and are consistent with commits
`5729e7f`, `56ac3ba`, `f3dc07c0`. Consequence: a reader of the shipped file cannot tell from its
docstring which draft it is or what the production deltas were. **Impact: documentation only; no
behavioural, contract or scoring effect.** Not fixed by this seat (read-only falsification seat, and
the file is production bytes under the pinned revision — editing it would break the pin).
*Note (not a defect):* the `limits` list→string change is the form the sealed oracle
`oracle-quota.py` checks (`limits_text`: non-empty `str`); the v3 draft's list form would have
failed that supplementary check, so the shipped form is the correct one.

**L2 — no in-file provenance record of the production deltas.** The shipped file carries no
`CHANGELOG`-style record of the four deltas above, and `tools/` has no companion note. The only
record is `corpus/lessons/round-23.md` (round history) plus the wave-build directory. Same impact
class as L1: traceability, not behaviour.

## 7. Not executed here / not excused

* **`CaseEscapedSpace` was NOT executed by this seat** (only one fixture case was authorised). The
  known parent-level C2 strict red — the frozen `CaseEscapedSpace` expected `enabled` row versus the
  sealed parent-consistency rule that yields `ambiguous_overmount` for that topology — **remains an
  open reported mismatch and is not excused, not re-labelled, not special-cased and not rewritten
  here.** Consequently the strict C2 target stays **UNPROVABLE at 29/30**; this seat's green case does
  not change that number, and it does not weaken the frozen expectation bytes of the red case. The
  full-driver exit-1 is likewise untouched by this seat (no driver was run).
* The quota **selftest** arm set (including the co-evolved `escaped-mount-point` arm) was **not**
  executed: reading or implementing a selftest is not permission to run it, and this item authorised
  only the one fixture case.
* No real-mode run, so this seat says nothing about live host quota state, `df` coverage claims,
  privacy clearance, health, capacity, EDQUOT attribution or admission.

## 8. Residual risk and verification gaps

1. **Single execution, no repetition.** The case was run exactly once (one child, one fixture case) as
   authorised; determinism of the candidate under repeated invocation is not demonstrated by this
   seat. The candidate is a pure function of the fixture bytes (no clock, no randomness, no host
   reads in fixture mode), so non-determinism is implausible but unmeasured here.
2. **Only one branch of the rule space is exercised by this seat.** The mount-resolution
   `ambiguous_overmount` refusal, the device-mismatch preemption, the btrfs `qgroups/enabled`
   tri-state, the ext "always unknown" rule and the tmpfs hardlimit vocabulary are **not** exercised
   by `CaseXfsUsrquota`; the btrfs line in this fixture is a decoy that is never selected. Coverage
   of those rules rests on the other sealed cases, not on this receipt.
3. **The recorded ambiguity survives.** `enforcement=enforced` evidences the XFS mechanism flag only
   (S078), not a per-user/per-group limit or an armed EDQUOT; the case's own rationale and the
   tool's limits text agree on that boundary. Any downstream reader must not upgrade "enforced" into
   "a limit exists".
4. **Supplementary metadata is unscored here.** `device_check=match`, `quota_option_keys=["usrquota"]`
   and `btrfs_qgroups_mode=null` are observed, not asserted by the frozen case; they are consistent
   with the sealed amendment but carry no sealed weight.
5. **Timeout asymmetry (informational).** The sealed oracle uses `TIMEOUT_S = 30` while this seat's
   authorisation was a 15 s wall timeout. The run finished in well under the limit, so the
   asymmetry is not exercised, but a future seat comparing timeouts should note it.
6. **Frozen-byte immutability is asserted by hash, not by a diff against a prior seal snapshot**
   beyond the seal manifest and `case-decisions.json` cross-check, which agreed exactly.

## 9. Artifacts

* Receipt: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/QXfsUsrquota/scan.json`
  (case/tool/fixture/stdout/stderr hashes, given vs actual argv, rlimits, exit, full stdout/stderr,
  per-field primary comparison, supplementary observed metadata, leakage check, verdict).
* Scratch (own, under the mandated root): `/fast/scratch/hyaku/mori-r23/QXfsUsrquota/`
  (`fixture.json`, `stdout.txt`, `stderr.txt`). Nothing was written under `/tmp`, nothing outside my
  seat's assigned report and receipt paths, and no repository file, frozen byte, oracle or expectation
  was modified.
* This report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/QXfsUsrquota.md`

**Verdict: PASS (case `CaseXfsUsrquota` reproduces the sealed expectation exactly).** Findings L1/L2 are
documentation-traceability observations for the parent to route; nothing here blocks, and nothing here
clears the frozen `CaseEscapedSpace` red.
