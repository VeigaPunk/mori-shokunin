# round-23 falsification — QEnabledPlusUnknown — CaseEnabledPlusUnknown

Seat: `QEnabledPlusUnknown` (leaf reviewer, no dispatch). Wave: round-23, claim C2
(coverage / FR2 quota observability). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

**Verdict for this seat: MATCH.** The sealed C2 case `CaseEnabledPlusUnknown` reproduces
exactly — exit `1`, `finding_id` `QUOTA_ENABLED`, and both ordered six-field path tuples
equal to the sealed expectation. No finding of defect, drift, or leakage. The frozen
`CaseEscapedSpace` red is **not** excused here (see §8).

Receipt: `.ufo/waves/round-23/falsify/QEnabledPlusUnknown/scan.json`
(`schema: mori-falsify-scan-v1`, 28 checks, 0 failed).

---

## 1. Exact identities (byte-level)

| Artifact | Path | SHA-256 | Bytes |
|---|---|---|---|
| Sealed case | `.ufo/waves/round-23/frozen/quota-cases/CaseEnabledPlusUnknown.json` | `77440e32054aef813df90b9a22d9e03b526496a3b103940df0ff601bec775828` | 6732 |
| Candidate tool | `tools/mori-quota-surface.py` (worktree) | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` | 66644 |
| Tool blob at pin `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` | `git show f3dc07c…:tools/mori-quota-surface.py` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` | 66644 |
| Scratch fixture (copy of `case["fixture"]`) | `/fast/scratch/hyaku/mori-r23/QEnabledPlusUnknown/fixture.json` | `72dcbb00e17f267833c7002002f5a75b9bd8d8f105fefaaab353b93175e26dc1` | 1135 |
| Canonical JSON of `case["fixture"]` (sorted, compact) | — | `62be529c2b594289b14033016161f544f3dc6a5d110a905fda66492bbd27d983` (recorded as `fixture_canonical_json_sha256` in the receipt) | — |
| Measured stdout | scratch `stdout.txt` | `518fa8f750e7242e4294381d1846dfdb78351373cab99f149a8295a492d040d3` | 1179 |
| Measured stderr | scratch `stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 (empty) |

Worktree tool bytes are **identical** to the pinned production revision blob
(`pin_matches_worktree: true`). `HEAD` in the lane is `6eb889c0` (one commit above the pin);
the tool file is byte-identical across `f3dc07c…`, `HEAD` and the worktree, so the
measurement is pinned regardless of which of the three is consulted.

## 2. Source derivation actually read

- `.ufo/waves/round-23/contract.md` §C2 — CLI, fixture schema `mori-quota-fixture-v1`,
  mount resolution, classification table, verdict precedence (setup → enabled → unknown →
  disabled), and the "positive evidence is never hidden by an unknown sibling" rule.
- `.ufo/waves/round-23/preseal-amendment.md` — C2 final rules that supersede only
  erroneous/ambiguous original clauses (tmpfs hardlimit vocabulary narrowed to the four
  documented keys; device-mismatch preemption; ambiguous-overmount refusal; per-line
  mountinfo field parsing; `qgroups_enabled` required fixture member and its pairing
  rules; supplementary-vs-primary field separation).
- Case `rationale` (full byte read) — the case states its own derivation: contract C2
  frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`, the amendment's C2
  final rules, and kernel sources **S082** (`Documentation/filesystems/proc.rst` v7.2
  §3.5, mountinfo field layout) and **S084** (`Documentation/filesystems/tmpfs.rst` v7.2
  quota mount-option table, lines 129–143).
- Implementation read (read-only, no edit): `tools/mori-quota-surface.py` — `parse_mountinfo`
  (per-line `-` separator, last three fields, octal decode of exactly `040/011/012/134`),
  `covering_mounts` / `resolve_mount` (longest covering mount point; repeated covering
  mount point ⇒ `ambiguous_overmount`; parent-id check against the longest strictly
  shorter cover), `classify` / `classify_btrfs`, `evaluate` (device check, with the
  btrfs-major-0 skip), `verdict`, `load_fixture` (exact key sets, pairing rules),
  `payload`.

The sealed case's stated delta from the original proposal is one member:
`btrfs_sysfs[uuid].qgroups_enabled = null` paired with `qgroups=false`. §6 negative
control C shows that delta is load-bearing, not cosmetic.

## 3. Invocation (fixture mode only, one child, bounded)

```
cwd    /fast/scratch/hyaku/mori-r23/QEnabledPlusUnknown
env    TMPDIR=/fast/scratch/hyaku/mori-r23/QEnabledPlusUnknown/
argv   prlimit --as=402653184 --cpu=15 timeout -s KILL 15 \
         python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
         --fixture /fast/scratch/hyaku/mori-r23/QEnabledPlusUnknown/fixture.json
limits AS = 402653184 bytes (384 MiB), CPU = 15 s, wall timeout 15 s (SIGKILL)
exit   1   (tool's own verdict exit; no timeout, no signal, no AS abort)
stderr empty (0 bytes)
```

`prlimit --as=384M` was rejected by this util-linux build
(`prlimit: failed to parse AS limit`), so the same 384 MiB bound was applied as the byte
value `402653184`; this is recorded verbatim in the receipt (`invocation.note`).

**Real mode was never used.** No `--path` argument, no `--selftest`, no live host read:
`strace -f -e trace=openat,open,getdents64,statx` over an identical invocation shows **no**
open of `/proc/self/mountinfo` and **no** open of `/sys/fs/btrfs/*` (the only `/proc/self`
access in the trace is CPython's own `/proc/self/maps` at interpreter startup). The single
data open is the scratch fixture file.

The scratch fixture is a verbatim JSON copy of `case["fixture"]` (parsed equality asserted
in the receipt: `fixture_equals_case_fixture: true`). No expected byte was edited:
`expected_bytes_modified: false`, `sealed_bytes_modified: false`.

## 4. Primary comparison (the scored denominator)

Primary fields, in the contract's order: `path, fstype, mount_point, quota_state,
enforcement, basis`.

Expected (sealed):

| # | path | fstype | mount_point | quota_state | enforcement | basis |
|---|---|---|---|---|---|---|
| 0 | `/srv/quota/data` | tmpfs | `/srv/quota` | enabled | enforced | tmpfs_quota_option |
| 1 | `/mnt/nfs4/data` | nfs4 | `/mnt/nfs4` | unknown | n/a | unsupported_fstype |

Actual (measured stdout, order preserved as in the fixture `paths` array):

| # | path | fstype | mount_point | quota_state | enforcement | basis |
|---|---|---|---|---|---|---|
| 0 | `/srv/quota/data` | tmpfs | `/srv/quota` | enabled | enforced | tmpfs_quota_option |
| 1 | `/mnt/nfs4/data` | nfs4 | `/mnt/nfs4` | unknown | n/a | unsupported_fstype |

- `exit`: expected `1`, actual process exit `1`, stdout `exit_code` field `1` — all three agree.
- `finding_id`: expected `QUOTA_ENABLED`, actual `QUOTA_ENABLED`.
- Ordered tuple comparison: **equal** (`primary_match: true`), 2/2 rows, order preserved.
- Output shape: top-level key set exactly
  `{df_covers_quota, exit_code, finding_id, limits, paths, schema}`; each path row key set
  exactly `{basis, btrfs_qgroups_mode, device_check, enforcement, fstype, mount_point, path,
  quota_option_keys, quota_state}`; `schema` = `mori-quota-surface-v1`; `df_covers_quota`
  = `false`; `limits` is non-empty (611 chars); no `error` key (no setup error); stdout is a
  single JSON object on one line.

## 5. Supplementary metadata — reported separately, NOT scored

The sealed case asserts **only** the six primary fields per path. `device_check`,
`quota_option_keys` and `btrfs_qgroups_mode` are therefore *unasserted* supplementary
metadata in this case; they are recorded here and in the receipt with
`supplementary_asserted_by_case: false`, and they do **not** enter the primary denominator
(`primary_total` stays at the case's own two rows).

| path | device_check | quota_option_keys | btrfs_qgroups_mode |
|---|---|---|---|
| `/srv/quota/data` | `match` | `["usrquota"]` | `null` |
| `/mnt/nfs4/data` | `match` | `[]` | `null` |

These are consistent with the amendment (`quota_option_keys=[]` for unsupported fstypes;
`btrfs_qgroups_mode` null) and with the contract's "quota-related keys only, never values".

Leakage checks on the measured stdout (all negative): `192.0.2.10` (NFS source),
`/srv/nfs4` (source path), `dm-0` (device link), `9f3c1c2e…` (UUID), `/dev/mapper/root`,
`size=1626620k`, `nr_inodes=406655`, `inode64`, `subvolid=257`, `rsize=1048576`,
`wsize=1048576`, `space=error=on`, `vers=4.2`, `timeo=600`, `retrans=2` — none present.
Only the key `usrquota` appears (a key, not a value). No option values, mount sources or
UUIDs are echoed.

## 6. Non-vacuity / discriminating power (synthetic fixtures in my own scratch only)

The sealed expectation must actually depend on the sealed inputs. Three bounded negative
controls (each: one child, same AS/CPU/timeout envelope, my scratch directory only; no
repo or frozen byte touched):

| Control | Change to the synthetic fixture | Measured result | Interpretation |
|---|---|---|---|
| A | drop `,usrquota` from the tmpfs super-options | exit `2`, `QUOTA_STATE_UNKNOWN`; tmpfs row → `disabled`/`n/a`/`tmpfs_quota_options_absent` | the enabled branch is load-bearing; without the mechanism flag the verdict falls to the unknown sibling |
| B | remove the `/srv/quota/data` path entirely | exit `2`, `QUOTA_STATE_UNKNOWN` (only the nfs4 unknown row) | exit `1` of the sealed case is produced by the enabled tmpfs path, not by a default |
| C | remove the amendment-required `qgroups_enabled` member from the btrfs record (i.e. the original proposal shape) | exit `2`, `QUOTA_SETUP`, `error: fixture_btrfs_record_keys` | the case's one-field delta from the original proposal is enforced by the tool; the corrected sealed shape is the only accepted shape |

Controls A–C are **synthetic scratch fixtures**, not edits to the frozen case, the sealed
oracles or the tool.

## 7. Determinism

Two identical invocations (the canonical one and an earlier equivalent) produced
byte-identical stdout (`518fa8f7…`) and empty stderr; `cmp` reported no difference.
No timeout, no signal, no AS abort on any invocation.

## 8. Frozen `CaseEscapedSpace` red — reported as a mismatch, not excused

My seat's assignment is the single case `CaseEnabledPlusUnknown`; I did not execute
`CaseEscapedSpace` and make no claim about it beyond the retained lane evidence. The lane
record `.ufo/waves/round-23/evidence/frozen-contradiction.json` (seal
`22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`, measured revision `5729e7f…`) stands and is
**a mismatch, not an excuse**:

- population result 29/30 (primary 26/27, supplemental 3/3) — the failing case is
  `CaseEscapedSpace`;
- the sealed rule (pre-seal amendment: a chosen mount whose parent id is present in the
  snapshot but is not the id of the longest strictly shorter covering mount ⇒ refuse) requires
  `unknown / n/a / ambiguous_overmount` with `fstype=null, mount_point=null,
  device_check=not_checked`;
- the frozen expectation file instead asserts `xfs / /srv/my data / enabled / enforced /
  xfs_quota_option` for the same path (selected mount id 43, parent id 33, longest shorter
  cover id 42 at `/srv`);
- the measured tool output is the rule-conformant `ambiguous_overmount` verdict.

Both sides are kept unchanged: no special case, no exclusion, no relabelling, no rewriting
of the frozen expectation or the sealed rule. A full driver exit `1` is therefore the
EXPECTED outcome of the strict frozen contradiction and is reported as such.

The quota selftest arm (49/49 at `f3dc07c`, `evidence/quota-selftest-corrected.json`) is a
**separate** arm after the separate co-evolved fixture input correction; it is not this
frozen case and is not evidence for or against it. My seat ran no selftest.

## 9. Open debt and non-clearance (unchanged by this seat)

Four unallowlisted inherited hits (raw 95 / allowlisted 86 / non-author 5); original
permission control RED 11/12; two historical dispositions still unknown; baseline acceptance
blocked; `privacy_clearance=false`. This seat's MATCH is a per-case measurement only — it is
not clearance, not health, not admission, not promotion, and not a coverage lift. Probe
visibility and accounting consistency are never clearance.

## 10. Tooling / installs

No installs, no upgrades, no service restarts were needed or performed. Everything used was
already present: `python3` 3.14.8, `/usr/bin/prlimit`, `/usr/bin/timeout`, `/usr/bin/strace`
(Arch, system packages). Channel/reason: n/a.

## 11. Residual risk and verification gaps

1. **Fixture-mode only.** This seat exercised the synthetic fixture path exclusively. The
   real-mode path (`/proc/self/mountinfo`, `/sys/fs/btrfs/*`, `os.stat`) is unverified here;
   only the frozen default real control covers it, and by the lane bounds only the
   `RerunPinnedDriver` seat may perform live quota reads.
2. **Supplementary metadata is unscored in this case.** `device_check`,
   `quota_option_keys` and `btrfs_qgroups_mode` are reported but not asserted by the sealed
   case; they carry no claim of coverage.
3. **Single-tool measurement.** No independent oracle re-derivation was performed for this
   case (the sealed `oracle-quota.py` was not run by this seat, to avoid executing other
   frozen cases in my lane); the expected values were taken only from the sealed case bytes.
4. **Case-level, not population-level.** This MATCH covers 1 of the 30 sealed quota cases.
   It says nothing about the population, and nothing about `CaseEscapedSpace`.
5. The scratch fixture is a JSON re-serialization of `case["fixture"]`; parsed equality is
   asserted (`fixture_equals_case_fixture: true`) but the byte form differs from the raw
   slice inside the case file. The tool is insensitive to this (key order/whitespace are not
   semantically relevant), and both the canonical JSON digest and the file digest are
   recorded in the receipt.

## 12. Paths written by this seat

- Report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/QEnabledPlusUnknown.md`
- Receipt: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/QEnabledPlusUnknown/scan.json`
- Scratch (all under the seat dir): `/fast/scratch/hyaku/mori-r23/QEnabledPlusUnknown/`
  (`fixture.json`, `stdout.txt`, `stderr.txt`, `stdout.rerun.txt`, `stderr.rerun.txt`,
  `trace.txt`, `negA_no_usrquota.json/.stdout`, `negB_nfs4_only.json/.stdout`,
  `negC_missing_qgroups_enabled.json/.stdout`)

No source, expectation, oracle, frozen case, lane index, jj ref or production byte was
modified. `git status --porcelain` shows no tracked modification in the lane.
