# InspectMountScope — round 23 mount-resolution falsification

- seat: `MadoR22-2.InspectMountScope` (leaf, read-only review; no subagents)
- lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`
- production pin: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`
- expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`
- question: does the final mount resolver follow the sealed amendment for the
  btrfs anonymous-device exception, conservative overmount refusal and
  normalization — and where does it stop short of complete topology?
- method: read-only inspection of pinned source, sealed case bytes and committed
  receipts. **No tool, oracle, driver or selftest was executed. No live
  `/proc/self/mountinfo`, sysfs, stat or quota read was made by this seat.**
  No source/frozen/oracle/driver edit, no mutation, no install.
- scratch: `/fast/scratch/hyaku/mori-r23/InspectMountScope/` contains one read
  copy of the pinned tool (`quota.py`, sha256
  `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92`, byte
  identical to `tools/mori-quota-surface.py`). No other scratch write.

Tags: **[OBSERVED]** = read from pinned bytes or a committed receipt;
**[INFERENCE]** = derived from code/source semantics, not exercised by a frozen
case.

## 1. Primary sources re-opened (stored bytes, hashes verified)

Raw sources are the retained copies in
`.ufo/waves/round-23/evidence/sources/` (registry rows S081/S082/S085 in
`corpus/SOURCES.md`, gate table in `corpus/lessons/round-23.md`).

| Row | Retained file + sha256 | Exact lines read | What it establishes |
|---|---|---|---|
| S081 | `evidence/sources/S081-fs_btrfs_inode.c` `01a6ad07c09cd1a05fbccab640c15362c91b57b85faa94c2fd9b9c0128110fdf` | 8246: `stat->dev = BTRFS_I(inode)->root->anon_dev;` | btrfs overwrites the stat device with the subvolume root's anonymous device; ordinary equality with the mount device is not guaranteed. It does **not** by itself teach that the major is 0 — the major-0 gate is the sealed amendment's rule. |
| S082 | `evidence/sources/S082-Documentation_filesystems_proc.rst` `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` | 1965–2002, field table 1973–1983, sentence 1985 | Field order (1) mount ID, (2) parent ID "or of self for the top of the mount tree", (3) major:minor "value of st_dev for files on filesystem", (4) root, (5) mount point, (6) mount options, (n…m) optional tag fields, separator, fstype, source, super options; unrecognised optional fields are ignored. No ordering/topology guarantee. |
| S085 | `evidence/sources/S085-fs_proc_namespace.c` `fd82c0db52055ae807ee0b46c7c9bc5d47a9239805eb8ca5c47d2ba81d695776` | `show_mountinfo` 135–193: header printf 143; parent ID 144; `seq_path_root(..., " \t\n\\")` 151; separator `seq_puts(m, " - ")` 172; source via `show_devname`/`mangle` | One line per mount; major:minor emitted from `sb->s_dev` (144); mount point escaping is exactly space, tab, newline, backslash (151); separator is a literal field (172). Field assembly is per mount; **line order is not a stack-order rule**. |

Consequence used below: a btrfs path can legitimately carry a stat device that
does not equal mountinfo's `sb->s_dev` (S081 vs S085:144), while the mountinfo
mount/root/source/super-options are still per-mount facts. The resolver must not
infer topology from line order (S082/S085), which the amendment turns into a
refusal rule rather than a guess.

## 2. Resolver identity and map

Production file at the pin: `tools/mori-quota-surface.py`, mode 100755, sha256
`e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92`.
[OBSERVED] `evidence/measure4/c2-after-observed.json` `tool.sha256` is the same
digest, so the measured C2 population used these exact bytes.

| Symbol | Lines (pinned) | Role |
|---|---|---|
| `decode_octal` | 290 | exactly `\040 \011 \012 \134`; any other backslash escape raises `Invalid` → `QUOTA_SETUP` |
| `parse_mountinfo` | 311 | per line: `fields[0..5]` then first `-` separator, exactly three post-separator fields; `fstype=fields[-3]`, `source=decode(fields[-2])`, `super_options=fields[-1]`; root decoded and validated (discarded); blank lines skipped |
| `covering_mounts` | 407 | equality, `/`, or component-boundary prefix `resolved.startswith(point + "/")` |
| `resolve_mount` | 421 | duplicate covering mount point → `ambiguous_overmount`; longest mount point wins; parent-ID consistency check at 449–461 |
| `evaluate` | 513 | sets preemption defaults, resolves, then device check (534–548) **before** classification; option-key extraction and `classify` after |
| `classify_btrfs` | 465 | enabled attribute is the witness; qgroups-inspection failure branch at 474–477 |
| `scan_btrfs_sysfs` | 571 | real-mode readset: `/sys/fs/btrfs/*/devices`, `qgroups` existence via `os.stat`, `qgroups/enabled`; **mode never opened** (comment 616–622) |
| `real_device_name` / `real_inputs` | 639 / 658 | realpath(source) basename; mountinfo read at 660; `stat` 668, `realpath` 674 |
| `load_fixture` | 695 | strict fixture key sets, normalized absolute path/realpath (720–721), unique given path, anchored canonical `MAJ:MIN` regex (725), plain basenames, UUID keys |
| `main` | 1894 | real `--path` validated only by `path.startswith("/")` (1904–1908) |

## 3. Checks against the sealed amendment — all [OBSERVED]

1. **Per-line mountinfo, last three fields.** Optional-field scanning is
   index-based per line; `CaseOptionalFields` (four optional fields on one line)
   passes: `xfs /srv/data disabled xfs_noquota_option`, exit 0. `CaseStacked`
   with optional fields on both duplicated lines also parses.
2. **Octal decoding.** Exactly the four kernel escapes of S085:151. The
   `CaseEscapedSpace` refusal itself proves the escaped mount point was decoded
   and mount id 43 selected (if `\040` were left literal, `/srv` would have
   matched and no parent refusal would fire).
3. **Component boundary.** `CaseBoundary` (`/a/bc` vs mount `/a/b`) passes with
   `btrfs /a ... btrfs_qgroups_dir_absent`, so `/a/b` did not cover `/a/bc`.
4. **No cover.** `CaseNoCover` → exit 2, `unknown`, `fstype=null`,
   `mount_point=null`, `no_covering_mount`, `device_check=not_checked`,
   `quota_option_keys=[]`, mode null.
5. **Duplicate covering mount point.** `CaseStacked` (`/data` twice) → exit 2,
   `unknown/n/a/ambiguous_overmount`, null fstype/mount point,
   `not_checked`, `[]`, null. Line order was not used.
6. **Parent-ID consistency.** `SupplementHiddenMount` (new tmpfs at `/home/x`
   parent 65 hiding older `/home/x/y` parent 65; longest shorter cover is
   `/home/x`) → `ambiguous_overmount`, exit 2, pass.
7. **Device mismatch preemption.** `CaseXfsDevMismatch` (mount 259:2 vs stat
   8:16) → exit 2, `xfs /mnt/xfsproj unknown/n/a/device_mismatch`,
   `device_check=mismatch`; fstype/mount point retained, keys `[]`, mode null.
   This is the amendment's "preempts the filesystem table" order.
8. **Btrfs anonymous-device exception.** `CaseBtrfsDevMatch` (stat major 0,
   equals mount 0:26) → `device_check=match`, exit 0. `CaseHostLike` (mount 0:30,
   stat 0:57) → `btrfs_subvolume_skipped`, exit 0. The frozen real control
   (`evidence/measure4/c2-real-control.json`) shows the same skipped value on the
   btrfs `/home` path and `match` on the xfs `/tmp` path. A nonzero btrfs stat
   major is not skipped by the code path (it falls to `device_mismatch`); no
   frozen case exercises that exact sub-arm.
9. **Normalization / realpath.** `CaseSymlinkRealpath` resolves `/tmp` from the
   realpath while echoing both given paths; both rows `xfs /tmp disabled ...
   match`. Fixture paths/realpaths are normalized absolute and unique by given
   path (699–727); `st_dev` is anchored `MAJ:MIN` without leading zeros
   (`DEVICE_RE`, 229).
10. **Frozen byte identity.** Recomputed sha256 of all 30
    `frozen/quota-cases/*.json` matches each `cases[].sha256` in
    `evidence/measure4/c2-after-observed.json` (zero mismatches);
    `cases_sha256_combined = 3323f4246ee637dd030138db330e7125d9775cf1a35a5e6be357fc596818a0e8`;
    oracle `oracle-quota.py` sha256
    `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` matches
    the receipt.
11. **No btrfs mode read in real mode.** `scan_btrfs_sysfs` reads only
    `qgroups/enabled`; `mode` is initialized to `None` and never assigned in the
    real path (571–627). Matches the "Real-mode safety correction before seal"
    section of `preseal-amendment.md`.

## 4. Finding 1 (blocking, expected red) — frozen `CaseEscapedSpace` contradicts the sealed parent rule

Sealed case bytes (unchanged): `frozen/quota-cases/CaseEscapedSpace.json`,
sha256 `8340738a509e474a94a815637e66b407dfb60c6449511e52db55296d844abeea`
(matches `frozen/case-decisions.json` `selected_sha256`, the measure4 case list
and `evidence/frozen-contradiction.json`).

Mountinfo lines (synthetic fixture):

```
26 33 0:24 / /proc           ... - proc  proc
33  2 0:30 / /               ... - btrfs /dev/mapper/root ...
42 33 0:44 / /srv            ... - xfs   ... ,noquota
43 33 0:45 / /srv/my\040data ... - xfs   ... ,usrquota
```

Path 1 `/srv/my data/sub dir` (st_dev `0:45`): covering mount points are `/`
(id 33), `/srv` (id 42), `/srv/my data` (id 43); all occur once, so no duplicate
refusal. Longest is id 43. Its parent ID is 33. The longest strictly-shorter
covering mount is id 42. 33 is present in the snapshot and 33 ≠ 42, so
`resolve_mount` returns `ambiguous_overmount` (421–461). [OBSERVED] at the pinned
tool (`evidence/measure4/c2-after-observed.json` and
`c2-after-real-observed.json`): exit 2, `QUOTA_STATE_UNKNOWN`; path 1
`fstype=null, mount_point=null, quota_state=unknown, enforcement=n/a,
basis=ambiguous_overmount, device_check=not_checked, quota_option_keys=[],
btrfs_qgroups_mode=null`; path 2 `/srv/plain` remains
`xfs /srv disabled n/a xfs_noquota_option match`. This equals the `actual` block
of `evidence/frozen-contradiction.json`.

Frozen expectation instead wants exit 1 `QUOTA_ENABLED` with path 1
`xfs /srv/my data enabled enforced xfs_quota_option`. Headline mismatch:
`exit_match=false, finding_match=false, paths_match=false`.

Why this is a fixture-expectation contradiction, not a resolver defect
[OBSERVED fixture bytes + rule; topology reading INFERENCE]: mount 43's parent
ID is 33 (the root mount), the same parent as mount 42. So the snapshot itself
says 43 is a sibling of 42 under the root mount, not a child of the `/srv` xfs
mount. That is consistent only with 43 having been mounted on a plain root-fs
directory before `/srv` was overmounted — i.e. exactly the hidden-mount shape the
parent rule refuses. A visible `/srv/my data` over `/srv` would carry parent 42.
The case scenario and the case mountinfo therefore disagree; the sealed rule is
what the resolver implements.

Accounting (all [OBSERVED], no rerun by this seat):
`c2-after-observed.json` counts `pass 29 / total 30 / unmet 1`, supplementary
`274/274`; the only unmet case is `CaseEscapedSpace.json`. `c2-after-real-observed.json`
(30 frozen + real expectation) is `30/31`, unmet 1, same case; its
`real_control` requirement itself matches. `evidence/measure4/summary.json` has
34 checks; the only failing checks are `C34.c2_after_every_case_matches` and
`C30.c2_oracle_real_control_agrees`, both caused by this case. `C29.c2_real_control_matches_frozen`
passes.

Disposition held by Main (quoted in
`evidence/parent-strict-target-disposition.txt`): keep the case, the expected
bytes and the parent rule unchanged; do not special-case, exclude or relabel;
record 29/30 and strict C2 unprovable. The resolver and oracle contain no
case-name special case (no `EscapedSpace`/`ambiguous_overmount` literal appears
in `oracle-quota.py`); the red is honest.

Receipt revision note [OBSERVED]: `evidence/frozen-contradiction.json` records
`measured_revision=5729e7ff889875d27ab0ead4385db551572892a9` (the initial red
measurement commit), not the pin. `git diff 5729e7f..f3dc07c0 -- tools/mori-quota-surface.py`
changes only `load_fixture` key/nonempty strictness and `selftest` arms — no
resolver function changed — and measure4 re-observes the same red with tool
sha256 `e4857413…` at `f3dc07c0`. So the receipt's output remains valid at the
pin, but its `measured_revision` field is not the pin and should not be cited as
one.

## 5. Finding 2 (residual rule scope, not a code divergence) — the parent refusal is one level deep

The amendment explicitly defers parent-ID graph resolution. The implemented
rule compares only the chosen mount's parent with the longest strictly-shorter
covering mount. A hidden subtree with an internally consistent two-level chain
therefore escapes [INFERENCE from 421–461 + S085:144]:

```
G at /a/x   parent root      (mounted on the root fs, before A)
H at /a/x/y parent G         (mounted before A)
A at /a     parent root      (later overmounts /a; G and H are now hidden)
path        /a/x/y/z
```

Covering mounts: `/`, `/a`, `/a/x`, `/a/x/y`; all mount points unique. Longest is
H; longest shorter is G; H's parent is G → no refusal, so H can be classified
even though `/a` (A) is the mount actually traversed. The verdict then describes
a mount that is not on the path (a possible false enabled/disabled, not merely a
wrong label); for btrfs the major-0 skip also removes the device check that
would otherwise catch a different filesystem. The "new mount on a plain
ancestor hiding an older nested mount" catch works for the one-level case
(`SupplementHiddenMount`) but not for a consistent hidden child chain. This is
within the sealed deferral, not a contradiction of it, but it means the probe
must not be described as resolving complete mount topology. A missing parent ID
likewise does not refuse (sealed clarification), so snapshots without parent
links can still classify.

Confidence: high for the code semantics; no frozen case exercises the chain
above, so this is not an observed C2 result.

## 6. Finding 3 (minor, real-mode only) — two distinct btrfs evidence classes share `btrfs_device_unmapped`

`classify_btrfs` returns `unknown/n/a/btrfs_device_unmapped` both when zero or
several UUIDs list the device (465–472) **and** when the qgroups path could not
be inspected (`record["qgroups"] is None`, 474–477). `scan_btrfs_sysfs` also
returns an empty map when `/sys/fs/btrfs` cannot be listed (581–584), which makes
every btrfs path take the same token. [OBSERVED code] The safety property is
correct — an inspection error is never reported absent/disabled — but the basis
token names the wrong evidence class. The sealed fixture schema requires
`qgroups` to be a bool (`type(qgroups) is bool`), so an uninspectable qgroups
directory cannot be expressed in the frozen population; no C2 case or real
control is affected. Severity: reporting-vocabulary precision, not a verdict
flip. Confidence: high.

## 7. Finding 4 (minor, real-mode fidelity) — mountinfo is decoded with U+FFFD replacement

`real_inputs` opens `/proc/self/mountinfo` with
`encoding="utf-8", errors="replace"` (660), while `os.stat`/`os.path.realpath`
use the filesystem-encoding string with surrogate escapes (668, 674). S085:151
shows only space, tab, newline and backslash are escaped, so arbitrary other
bytes in a mount point/source reach the file raw. [INFERENCE] A mount point with
a non-UTF-8 byte decodes to U+FFFD here, cannot equal the realpath, and the
resolver falls back to a shorter covering mount. For non-btrfs paths the device
check normally turns that fallback into `device_mismatch` (unknown) rather than a
false `disabled`; for a btrfs path the major-0 skip removes that guard, so a
fallback to a *different* btrfs filesystem could be classified instead of
refused. Separately, `text.splitlines()` (313) also splits on Unicode
line boundaries beyond `\n`; a real mount point containing e.g. U+000B would
produce a malformed line and exit 2 `QUOTA_SETUP` (safe direction). No frozen
fixture can express either shape. Confidence: high for the decoding/splitting
facts; the btrfs verdict consequence is bounded inference.

## 8. Finding 5 (cosmetic, outside mount logic) — production file still describes itself as the v3 candidate

Line 2 of `tools/mori-quota-surface.py` reads
`"""mori-quota-surface-v3.py — read-only quota-surface probe (FR2 / EDQUOT)."""`;
lines 4–6 call it "the round-23 pre-seal amendment candidate" and "a new
candidate authored alongside `mori-quota-surface.py` (the original, unaltered)".
[OBSERVED] Commit `1979a9d` landed the production path with that candidate-era
docstring, but the landed bytes are **not** identical to
`build/ImplQuota/mori-quota-surface-v3.py` in the same commit (build v3
`5199e97b…` vs landed `70191075…`): the landed file already emitted `limits` as
a joined string instead of build v3's list, and later commits changed the
classifier unpacking (`5729e7f`) and fixture strictness/selftest arms
(`f3dc07c0`). Output schema is the contract's `mori-quota-surface-v1`.
No behavioral effect on the resolver; flagging only so the docs cutover does not
describe the production file as the unmodified v3 candidate.

## 9. Normalization boundary (consistency note, not a defect)

- Fixture records are strict: normalized absolute `path`/`realpath`, no
  trailing slash except `/`, no empty/`.`/`..` component; unique given path;
  canonical `MAJ:MIN`; exact path-record key set (699–727). Real CLI paths are
  validated only by `startswith("/")` (1904–1908), so `/tmp/` or
  `/tmp/../tmp` are accepted and echoed unnormalized while resolution uses
  `realpath`. The amendment's normalization clause is fixture-scoped; the
  contract asks only for absolute real paths. No false verdict follows from a
  legal realpath, but raw real-mode output `path` is the caller's spelling.
- `parse_mountinfo` skips any blank line, not only trailing ones (313–315).
  Accepted fixtures are sealed and have no internal blank lines; this is laxer
  than the amendment's wording, with no effect on any case.
- No covering mount point is normalized/validated, so a fixture with a
  non-canonical mount point (trailing slash, `.`/`..`) is accepted and may fail
  to cover; the frozen population has none. All 30 sealed case hashes match the
  measured receipts, so this is a future-fixture concern only.

## 10. What this seat does not establish

- No claim of complete Linux mount topology, mount-namespace semantics,
  propagation or stack order. The resolver deliberately refuses some ambiguous
  shapes, defers parent-graph resolution, and says nothing about mounts it cannot
  see.
- No claim of quota enablement, limit/usage, capacity, health or EDQUOT
  attribution; those are the output's stated limits and remain unknown.
- No live host observation by this seat; the real control values are quoted from
  `evidence/measure4/c2-real-control.json` and the frozen expectation only.
- No C1 authority. Adjacent receipt values only (next section).

## 11. Adjacent receipts (not this seat's axis)

- C1, from `evidence/measure4/summary.json` and `c1-oracle-after.json`:
  original 26 before = 25/26, `misleading_alias_runs=8`; after = 26/26,
  `misleading_alias_runs=0`, oracle exit 0; C1 real control matches frozen v2
  receipt (`RETENTION_RECONCILED`, exit 0); `c1_supplementary.pass=true`
  (same-instance replay, selftest, source byte guard, source guard mutants).
- C2, same receipts: before 0/30 (capability absent), after 29/30, only
  `CaseEscapedSpace` unmet; real-inclusive 30/31; `c2_after_every_case_matches`
  and `c2_oracle_real_control_agrees` are the only two failed checks.
- Quota selftest: `evidence/quota-selftest-corrected.json`,
  `measured_revision=f3dc07c0…`, exit 0, `QUOTA_SELFTEST_OK`, `arms=49`. The
  `escaped-mount-point` selftest arm is a separate co-evolved fixture arm
  (path `st_dev` correction in `f3dc07c0`), not the frozen `CaseEscapedSpace`;
  49/49 must not be cited as evidence for or against the frozen case.
- Driver `measure-round23-v2.py` executed sha256
  `5c12fdc056309966d3e716d25e3427a7908056595383f0353655b42282fdfbcd` matches
  the sealed bytes; full-driver exit 1 is the expected consequence of the two
  C34/C30 failures above.
- Carried open debt unchanged: 4 unallowlisted retention hits, original
  permission control RED 11/12 retained un-rerun, two unknown historical
  dispositions, baseline acceptance blocked, `privacy_clearance=false`.

## 12. Receipts consulted

- `.ufo/waves/round-23/contract.md`, `preseal-amendment.md`
- `.ufo/waves/round-23/frozen/quota-cases/*.json` (30 files; sha256 recomputed)
- `.ufo/waves/round-23/frozen/case-decisions.json`, `c2-expected-real.json`
- `.ufo/waves/round-23/oracle-quota.py` (sha256 `f1f4a027…`; no case-name logic)
- `.ufo/waves/round-23/evidence/measure4/c2-after-observed.json`
- `.ufo/waves/round-23/evidence/measure4/c2-after-real-observed.json`
- `.ufo/waves/round-23/evidence/measure4/c2-real-control.json`
- `.ufo/waves/round-23/evidence/measure4/c1-oracle-after.json`,
  `c1-real-control.json`, `summary.json`
- `.ufo/waves/round-23/evidence/frozen-contradiction.json`,
  `parent-strict-target-disposition.txt`, `quota-selftest-corrected.json`
- `.ufo/waves/round-23/evidence/sources/S081-fs_btrfs_inode.c`,
  `S082-Documentation_filesystems_proc.rst`, `S085-fs_proc_namespace.c`
- `corpus/SOURCES.md` rows S081/S082/S085; `corpus/lessons/round-23.md`;
  `corpus/knowledge/quota-surface-r23.md`

## 13. Conclusion

The pinned resolver follows the sealed amendment for mountinfo parsing,
component-prefix selection, duplicate covering-mount refusal, the one-level
parent-ID refusal, device-mismatch preemption and the btrfs anonymous-device
exception (stat major 0 skip), with normalization applied where the amendment
requires it. No special case, exclusion or relabel was found.

The only C2 red is the pre-sealed `CaseEscapedSpace` contradiction: its
mountinfo says the chosen mount is parented to the root mount while the case
expectation assumes it is parented to `/srv`; the sealed rule must refuse and
does. **C2 strict target remains 29/30 (27 original-derived: 26/27; 3 discovery:
3/3) and is not a demonstrated pass** at the pin. Residual unknowns: one-level
parent rule (deeper hidden chains), real-mode basis vocabulary conflation, and
non-UTF-8 mountinfo decoding fidelity. None was repaired here, per the
read-only mandate and Main's no-special-case ruling.
