# Round-23 C2 falsification — seat `QBtrfsSquota` (case `CaseBtrfsSquota`)

**Verdict: PASS — zero mismatches for this case.** One sealed C2 fixture-mode case
executed, in isolation. No real mode, no driver, no other case, no host quota read.

## 1. Scope and identity (sealed bytes)

| item | value |
|---|---|
| case file | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/CaseBtrfsSquota.json` |
| case sha256 | `b3a641541e536ce1f313b521ae25a33cd8296e2e2d8daf647bf24c168254240a` (4590 bytes) |
| same sha256 at seal `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` | yes |
| same sha256 at pinned production `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` | yes |
| same sha256 in worktree (`git status` clean for that path) | yes |
| only commit touching the case | `22772c1` "round-23: seal all oracle inputs before production implementation" |
| tool | `tools/mori-quota-surface.py`, sha256 `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| tool sha256 at `f3dc07c` and at HEAD `6eb889c` | identical → the run measured the pinned production bytes |
| production path present at seal commit | **no** (`git cat-file -e 22772c1:tools/mori-quota-surface.py` fails) → expectation precedes implementation |

Case decision (`frozen/case-decisions.json` → `decisions[3]`): selected =
`cases-corrected/CaseBtrfsSquota.json` (`b3a641…`, `primary: true`), superseding
`cases-proposed/CaseBtrfsSquota.json` (`db77e8…`) with reason "Independent
source-derived pre-measurement correction; exact author bytes, no L1 expectation
edits". The correction is exactly the pre-seal amendment's btrfs clause: basis token
`btrfs_qgroups_dir_present` → `btrfs_qgroups_enabled` and the required fixture member
`qgroups_enabled` added to the uuid record; `mountinfo` and path bytes unchanged.

## 2. Derivation / amendment read (no implementation-driven expectation)

`preseal-amendment.md`, C2 final rules: a btrfs **qgroups directory means INITIALIZED,
not enabled**; each `btrfs_sysfs` uuid record must carry `qgroups_enabled`
(true/false/null); present + `enabled=true` ⇒ `enabled` / `unknown` /
`btrfs_qgroups_enabled`; `qgroups_enabled=false` ⇒ `btrfs_qgroups_disabled`;
`null` ⇒ `btrfs_qgroups_enabled_unavailable`; absent dir keeps
`btrfs_qgroups_dir_absent` only on a successful parent inspection. Mode is
informational, only `qgroup`/`squota` accepted. Device mismatch preempts the
filesystem table, but btrfs skips the equality comparison when the **stat major is 0**.
Fixture source resolution looks up the raw decoded source in `device_links` and uses
the mapped basename. Mount resolution = longest component-prefix cover; a covering
mount point occurring twice is refused (`ambiguous_overmount`); a chosen mount whose
parent id is present in the snapshot but is not the longest strictly-shorter cover's
id is also refused.

Applied to this fixture: cover for `/srv/data` is `/srv` (btrfs, source
`/dev/mapper/srv` → `device_links` → `dm-3`), beating the shorter ext4 `/` cover;
parent id `25` equals the `/` mount's id `25`, so no parent-id refusal; `st_dev`
`0:57` has major `0`, so the btrfs device-skip applies and no mismatch preemption;
exactly one uuid (`6f0c9e42…`, devices `["dm-3"]`) lists `dm-3`, so the
zero/multiple-match branch is not reached; `qgroups` true + `qgroups_enabled` true ⇒
enabled branch; `qgroups_mode` `"squota"` is an accepted informational value.

## 3. Invocation (exactly one child)

```
argv:     python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
              --fixture /fast/scratch/hyaku/mori-r23/QBtrfsSquota/fixture.json
wrapper:  timeout -k 1 15 prlimit --as=402653184 -- <argv>
cwd/TMPDIR: /fast/scratch/hyaku/mori-r23/QBtrfsSquota
python 3.14.8; prlimit util-linux 2.42.4
```

`case["fixture"]` was copied verbatim into the seat scratch `fixture.json`
(sha256 `0e8897256d1ee545af6a585043e166df8f5a576d576a6e1383a8cbf721945539`, 817
bytes, top-level keys `btrfs_sysfs, device_links, mountinfo, paths, schema`); it was
not edited. Exit **1**; stdout 968 bytes
(sha256 `8671e2584b8f6ed4e5fbaaedc807b8e5a42515e13c6d327c70f142bd0840ebff`); stderr
0 bytes. No second child was run against the tool.

## 4. Comparison (primary vs supplementary kept separate)

* exit: actual `1` = expected `1` ✅
* finding_id: actual `QUOTA_ENABLED` = expected `QUOTA_ENABLED` ✅
* path rows: 1 actual = 1 expected ✅
* ordered six-field tuples `(path, fstype, mount_point, quota_state, enforcement, basis)`:

  | # | actual | expected | |
  |---|---|---|---|
  | 0 | `('/srv/data','btrfs','/srv','enabled','unknown','btrfs_qgroups_enabled')` | `('/srv/data','btrfs','/srv','enabled','unknown','btrfs_qgroups_enabled')` | ✅ |

  **Primary denominator for this seat: 1/1 rows matched, 0 mismatches.**

* Supplementary metadata (asserted apart, not part of the primary denominator):
  `device_check=btrfs_subvolume_skipped`, `quota_option_keys=[]` (btrfs mechanism is
  sysfs, not mount options), `btrfs_qgroups_mode="squota"`; top level
  `schema=mori-quota-surface-v1`, `exit_code=1`, `df_covers_quota=false`, `limits`
  present, no extra row keys.
* Leak check on stdout: no mount source (`/dev/mapper/srv`, `/dev/sda1`), no device
  basename (`dm-3`), no uuid, no super-option values (`compress`, `zstd`), no `st_dev`
  string. The only `subvol` substring is inside the fixed token
  `btrfs_subvolume_skipped`.

## 5. Findings

**F1 — severity: none — `CaseBtrfsSquota` PASSES.** Exit, finding_id and every
ordered six-field tuple equal the sealed expectation. This case surfaced no defect.

Observations (no expectation byte touched; no source edit):

* **O1 — stale original contract text.** `contract.md` §C2's btrfs row still names
  `btrfs_qgroups_dir_present` (and `btrfs_qgroups_dir_absent` for `qgroups` false),
  while the sealed corrected case and the implementation use
  `btrfs_qgroups_enabled` / `btrfs_qgroups_disabled` / `btrfs_qgroups_enabled_unavailable`.
  `preseal-amendment.md` explicitly supersedes exactly those clauses, so the drift is
  in the original contract prose, not in the sealed expectation. Documentation
  item for the parent; nothing was relabelled or rewritten by this seat.
* **O2 — co-evolution proximity / discrimination limit.** The implementation's own
  selftest arm `btrfs-qgroups-enabled` (`tools/mori-quota-surface.py:1133-1163`) uses
  the same btrfs-enabled branch with the same expected tuple family (path `/home`,
  mount `/home`, uuid `1d02a454…`, `dm-0`). It is a *different* fixture (not a
  byte-duplicate of the sealed case), and the sealed case keeps real independent
  value in the **mount-resolution** path (nested `/srv` cover over an ext4 `/` cover,
  parent-id identity, no repeated mount point) and in the **btrfs device-skip** rule
  (stat major `0` ⇒ no mismatch preemption). But this case alone cannot discriminate
  a correct general classifier from one that hard-codes the btrfs-enabled branch.
  Provenance is clean (amendment-derived, production path absent at seal), so the
  case is valid; the limit is discriminative power, not authorship.
* **O3 — old-shape proposal is (statically) rejected as designed.** The superseded
  original proposal's uuid record lacks `qgroups_enabled`, and the loader requires
  the exact record key set `devices, qgroups, qgroups_enabled, qgroups_mode`
  (`fixture_btrfs_record_keys`) ⇒ that fixture would exit 2 `QUOTA_SETUP`, which is
  the amendment's stated intent ("original proposals are preserved rejected
  old-shape evidence, not valid final inputs"). [INFERENCE from source lines; not
  executed — a second tool invocation was not authorised.]
* **O4 — cosmetic.** The shipped probe's module docstring labels the file
  `mori-quota-surface-v3.py` while the artifact is `tools/mori-quota-surface.py` and
  `SCHEMA = "mori-quota-surface-v1"`. No behavioural effect; the contract's required
  artifact path is satisfied.

## 6. Scope discipline

Only the one named fixture-mode case was executed; never real mode; no
`quotactl`/`btrfs qgroup`/`xfs_quota`/`repquota`/mount/qgroup reads; no driver,
oracle, selftest, build, lint or test run; no source or expected bytes edited (case
sha256 unchanged at seal, at pinned production and in the worktree). All scratch
(including the copied fixture) lives under
`/fast/scratch/hyaku/mori-r23/QBtrfsSquota/`, `TMPDIR` pointed there, no `/tmp`
use. Writes are limited to this report and the receipt
`.ufo/waves/round-23/falsify/QBtrfsSquota/scan.json`; no fleet-root, sibling, lane
index, `jj`, ref or production write. No installs were needed (no tool, package or
system change) — nothing to record under the tooling directive.

Untracked litter observed in the lane but **not** produced by this seat (mtimes
precede/parallel my run; my invocation was `python3 -I script.py`, which caches
nothing): `tools/__pycache__/mori-quota-surface.cpython-314.pyc` (15:17) and
`.ufo/waves/round-23/__pycache__/oracle-quota.cpython-314.pyc` (15:33). Flagged for
the parent only so that no commit picks them up (same class as the untracked
`.scratch/` exclusion in the contract); this seat did not delete them because a
sibling seat may still own the process that wrote them.

`CaseEscapedSpace` was **not** executed by this seat (out of scope). Its strict red
is a genuine expected-output mismatch that the driver seat must report as a
mismatch, not excuse; it is a different artifact from the separately corrected
co-evolved selftest arm (49/49) and is not conflated with it here.

## 7. Residual risk and verification gaps

* This seat's evidence covers **one** case: it says nothing about the other 26
  primary C2 cases, the 3 supplemental C2 cases, the real-mode control
  (`c2-expected-real.json`), or the quota selftest (49/49).
* Single run, no repetition: no determinism/repeatability evidence for this case
  (the probe is read-only and deterministic by construction, but that is an
  inference, not a measurement).
* The sealed `oracle-quota.py` was not executed; the comparison was made directly
  against the sealed `expected` bytes, field by field, with primary and
  supplementary metadata kept apart.
* O2's discrimination limit means this case alone cannot rule out a hard-coded
  btrfs-enabled branch; that risk needs the other btrfs cases (disabled /
  unavailable / unmapped / two-uuids / device-mismatch) and mutation arms to close.
* Wave-level items unchanged by this seat: the four unallowlisted inherited hits
  (raw 95 / allowlisted 86 / non-author 5), the original permission control RED
  11/12, the two unknown dispositions, blocked baseline acceptance and
  `privacy_clearance=false`. Probe visibility/accounting consistency is not
  clearance, health or admission.
