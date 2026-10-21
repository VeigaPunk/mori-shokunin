# QOptionalFields — falsification of the sealed C2 case `CaseOptionalFields`

**Seat:** `QOptionalFields` (read-only reviewer seat, round 23, lane `/home/vgpnk/Projects/shokunin/mori-shokunin`)
**Verdict on this case:** **MATCH** — the pinned production tool reproduces the frozen expectation byte-for-byte on all three primary axes.
**Receipt:** `.ufo/waves/round-23/falsify/QOptionalFields/scan.json`
**Scratch:** `/fast/scratch/hyaku/mori-r23/QOptionalFields/` (fixture, stdout/stderr, mutants, helper scripts). No `/tmp` use, no fleet/sibling writes.

---

## 1. What was falsified, and how

One sealed fixture-mode case only, as assigned:

| item | value |
|---|---|
| case | `.ufo/waves/round-23/frozen/quota-cases/CaseOptionalFields.json` |
| case sha256 | `9e73da479ea14cc4b7ddfccf08816c7716842eb71325d7c8bd06541779c1daf0` |
| candidate executable | `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py` |
| tool sha256 (working tree) | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| tool blob sha256 at pinned production `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` (identical — the executed bytes *are* the pinned production bytes) |
| seal | `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` |
| fixture copy | `/fast/scratch/hyaku/mori-r23/QOptionalFields/fixture.json` (verbatim `case["fixture"]`, `json.dumps(indent=2, sort_keys=True)+"\n"`) |
| fixture sha256 | `8383025da65c2e79c0cd5a4e871a8accc3ecf58c405a377476ec1b6960d4dc61` (1146 bytes) |

Invocation (single child, fixture mode, never real mode):

```
timeout 15 prlimit --as=402653184 -- python3 -I \
  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
  --fixture /fast/scratch/hyaku/mori-r23/QOptionalFields/fixture.json
```

cwd `/fast/scratch/hyaku/mori-r23/QOptionalFields`, env `TMPDIR=/fast/scratch/hyaku/mori-r23/QOptionalFields`, `PATH=/usr/bin:/bin`.

**Observed:** exit `0`, stderr empty (0 bytes), stdout exactly one line (one JSON object, 1178 bytes, sha256 `c72ef4e8b2d062ce34af8cbefd7fd05fc0f749ea15efb0da56de701bebac9e0f`).
A repeat invocation produced a byte-identical stdout (`c72ef4e8…`), so the verdict is deterministic.

---

## 2. Primary comparison (scored six fields, ordered)

Primary = `exit`, `finding_id`, and the ordered six-field tuples `(path, fstype, mount_point, quota_state, enforcement, basis)`.

| axis | frozen expected | observed | result |
|---|---|---|---|
| exit | `0` | `0` | match |
| finding_id | `QUOTA_DISABLED` | `QUOTA_DISABLED` | match |
| path[0] tuple | `/srv/data, xfs, /srv/data, disabled, n/a, xfs_noquota_option` | identical | match |
| path[1] tuple | `/srv/data/reports, xfs, /srv/data, disabled, n/a, xfs_noquota_option` | identical | match |

`primary.exit_match = true`, `primary.finding_match = true`, `primary.paths_match = true`.

Observed rows (full output shape, `device_check`/`quota_option_keys`/`btrfs_qgroups_mode` shown because they are part of the emitted row, scored separately below):

```json
{"path":"/srv/data","fstype":"xfs","mount_point":"/srv/data","quota_state":"disabled",
 "enforcement":"n/a","basis":"xfs_noquota_option","device_check":"match",
 "quota_option_keys":["noquota"],"btrfs_qgroups_mode":null}
{"path":"/srv/data/reports","fstype":"xfs","mount_point":"/srv/data","quota_state":"disabled",
 "enforcement":"n/a","basis":"xfs_noquota_option","device_check":"match",
 "quota_option_keys":["noquota"],"btrfs_qgroups_mode":null}
```

Top-level output: `schema=mori-quota-surface-v1`, `exit_code=0` (consistent with the process exit), `df_covers_quota=false`, `limits` = one fixed boundary string. Output key set is exactly `{schema, finding_id, exit_code, paths, df_covers_quota, limits}`; each path row carries exactly the nine documented keys. No `error` token (not a setup error).

**CaseEscapedSpace:** not executed by this seat (assignment: this one case only). The wave-level strict red at 29/30 belongs to that case and is reported as a mismatch by its owner; it is not excused here and nothing in this seat's evidence softens it. This seat contributes one additional *passing* case and no new failure.

---

## 3. Supplementary metadata (reported apart, never folded into the primary denominator)

This case freezes **no** `supplementary_expected` block (`case_has_supplementary_expected: false`), so the three metadata fields carry no frozen expectation here; they are recorded as observations only:

| path | `device_check` | `quota_option_keys` | `btrfs_qgroups_mode` |
|---|---|---|---|
| `/srv/data` | `match` | `["noquota"]` | `null` |
| `/srv/data/reports` | `match` | `["noquota"]` | `null` |

These are consistent with the frozen derivation: chosen mount `0:25` equals the reported `st_dev` `0:25` (`match`); the xfs super options split to `rw, noquota, attr2, inode64`, so the quota-related key set is exactly `{noquota}`; the decoy btrfs uuid is never consulted, so `btrfs_qgroups_mode` stays `null`.

**Leakage probes (supplementary, both pass):**
- Sealed-oracle canary logic reused verbatim (`oracle-quota.py` sha256 `…`, `canaries()`/`leakage_hits()`): no mount source (`/dev/mapper/root`, `/dev/mapper/data`), no uuid (`2f0a1c6e-…`), no `key=value` option token, no distinctive option value, no device basename (`dm-0`, `dm-1`) appears in stdout.
- Independent stricter probe over the payload minus the fixed `limits` boilerplate: no `attr2`, `inode64`, `space_cache`, `subvol`, `size=`, `mode=`, `nosuid`, `nodev`, `relatime`, `proc`, `sysfs`, `tmpfs` token. (The `limits` string legitimately names `sysfs`; that is fixed tool text, not fixture echo.)

**Host independence:** `/srv/data` does not exist on this host (`ls: cannot access '/srv/data'`), yet the fixture-mode run returned a complete verdict for it — the resolution came from the fixture, not from host state. Real mode was never invoked.

---

## 4. Discrimination probes — the case is not vacuously satisfied

Two mutated **copies** of the pinned tool were written under this seat's scratch (production file untouched) and run against the same single case. Both mutants break the frozen expectation, so the case constrains what it claims to constrain:

| mutant | mutation | observed | primary comparison | still passes? |
|---|---|---|---|---|
| `M1-file-wide-super-options` | every mount takes the **last line's** super-option field instead of its own line's | exit `2`, `QUOTA_STATE_UNKNOWN`, rows `xfs_quota_options_absent` / `quota_state=unknown` | exit ✗, finding ✗, paths ✗ | **no** |
| `M2-first-covering-mount` | election returns the first covering mount in file order instead of the longest component-prefix mount | exit `0`, `QUOTA_DISABLED`, rows `btrfs, /, btrfs_qgroups_dir_absent` | exit ✓, finding ✓, **paths ✗** | **no** |

M1 attacks exactly the property the case scenario names ("a further tmpfs line follows it so the xfs super options are not the last field of the mountinfo text"); M2 attacks the longest-prefix election against the `/` btrfs and `/srv` tmpfs decoys. Note M2 keeps exit and `finding_id` identical to the expectation — **only the ordered six-field tuple comparison catches it**. The primary denominator therefore carries real discriminating power beyond exit/finding, which is exactly the separation the amendment demands.

---

## 5. Source derivation re-checked (the case's own citations)

The case's rationale cites S077 / S078 / S082. Each citation was re-read at the sealed source rows (`.ufo/waves/round-23/evidence/sources/`, hashes in `evidence/sources-manifest.json`):

- **S082 `proc.rst` 1973–1983 / 1988–1993** — field layout `(1)`–`(6)`, the optional block `tag[:value]`, the `-` separator and the last three fields; the optional-field table lists exactly `shared:X`, `master:X`, `propagate_from:X`, `unbindable`. The case's mountinfo line `31 29 0:25 / /srv/data rw,relatime shared:1 master:2 propagate_from:3 unbindable - xfs /dev/mapper/data rw,noquota,attr2,inode64` therefore parses as claimed (6 fixed fields + 4 optional fields + separator + 3 trailing fields).
- **S077 `xfs.rst` 171–173** — `noquota`: "Forcibly turns off all quota accounting and enforcement within the filesystem." → basis `xfs_noquota_option` is the documented meaning.
- **S078 `xfs_super.c` 239–254** — the kernel emits `,usrquota`/`,uqnoenforce`/`,prjquota`/`,pqnoenforce`/`,grpquota`/`,gqnoenforce` per scope and emits `,noquota` only under `if (!(mp->m_qflags & XFS_ALL_QUOTA_ACCT))` (guard at 252–253). A kernel-emitted super-option string therefore never pairs `noquota` with another quota key — the case's premise for the non-conflict classification holds.

Derivation confirmed against the cited lines; no citation drift.

---

## 6. Findings by severity

**Low — production file's module docstring misstates its own identity and provenance (documentation, not behaviour).**
`tools/mori-quota-surface.py:2` opens with `"""mori-quota-surface-v3.py — read-only quota-surface probe (FR2 / EDQUOT).` and lines 4–8 state it "is the round-23 pre-seal amendment candidate for contract §C2 … a new candidate authored alongside `mori-quota-surface.py` (the original, unaltered) and `mori-quota-surface-v2.py`". The shipped file *is* `tools/mori-quota-surface.py`, the path named by the contract and by the assignment; the actual v3 sibling lives at `.ufo/waves/round-23/build/ImplQuota/mori-quota-surface-v3.py` (sha256 `5199e97b5ac89a39b3f047586a6e624d7e95041415390750a93f91bf15d55129`) and differs from the shipped bytes (29 differing lines: the classifier unpacking repair, stricter path-record validation, `limits` as a string, two extra selftest arms). The shipped file therefore presents itself as a different file and as a pre-seal candidate. Behaviourally harmless for C2 (the file's own docstring is never read by the CLI), but it is a false provenance statement in a production artifact and it understates that the shipped bytes are post-v3. No production or frozen byte was edited by this seat.

**No blocking or behavioural defect was found for this case.** The primary axes match exactly, the case is discriminating against two plausible mutations of the exact properties it claims to test, the derivation citations are accurate, and no leakage or host-state dependence was observed.

---

## 7. Residual risk and verification gaps

1. **Scope:** exactly one case, one mode. The other 29 sealed quota cases and the real-mode control were not executed by this seat; C2's 29/30 headline and the strict red at `CaseEscapedSpace` are other seats'/the driver's observations, not mine.
2. **Supplementary metadata is unfrozen for this case.** `device_check=match`, `quota_option_keys=["noquota"]`, `btrfs_qgroups_mode=null` are observations only. If the amendment's supplementary sealed checks are meant to score these fields for `CaseOptionalFields`, the case file does not carry them (`supplementary_expected` absent) — a coverage note, not a mismatch.
3. **The elected mount's topology was not adversarially stressed here.** The case's parent-id/ancestor relation (`parent 29` == the `/srv` mount id `29`) happens to satisfy the amendment's parent-refusal rule. A fixture where the parent id is present but differs would exercise `ambiguous_overmount`; that variant is not this case and was not executed.
4. **Not executed by this seat, and therefore unverified here:** the `noquota`+quota-key conflict row, the accounting-only (`uqnoenforce`) row, the btrfs enabled/disabled/unavailable rows, ext rows, tmpfs rows, `device_mismatch`, `ambiguous_overmount`, and setup-error rows — all belong to other sealed cases.
5. **Fixture-mode only.** No real-mode reading was performed or authorised from this seat; the real control remains the driver's/other seats' observation.
6. **Mutation probes are scratch copies, not evidence about production.** They show the case's discriminating power; they say nothing about the shipped bytes beyond the two specific mutants.

---

## 8. Scope compliance

- Executed only the assigned case, only in fixture mode (`real_mode_invoked: false`).
- One child at a time; `timeout 15` + `prlimit --as=384MiB` on every tool invocation.
- All scratch under `/fast/scratch/hyaku/mori-r23/QOptionalFields/`; `TMPDIR` pointed there; no `/tmp` fallback.
- No builds, no linters, no formatters, no full suite, no quota tools, no host quota reads, no mount/remediation.
- No production, frozen, oracle or expectation byte was modified; no lane index/jj/ref touched; no sibling or fleet-root writes. The only writes are this report, the assigned receipt `falsify/QOptionalFields/scan.json`, and scratch files under this seat's directory.
- No transcript/session reads, no credential/auth/agent.db reads, no live journal or process probes.
