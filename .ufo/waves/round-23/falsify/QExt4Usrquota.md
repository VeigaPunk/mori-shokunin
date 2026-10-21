# QExt4Usrquota — falsification of the sealed C2 case `CaseExt4Usrquota.json`

Seat: `MadoR22-2.QExt4Usrquota` (leaf member; no subagent dispatch, no children).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Pinned production: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`.
Expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`.
Working HEAD: `6eb889c037163e4886eaa61501258910d6a529b9` (payload child of the pin).
Scratch (mine, unique): `/fast/scratch/hyaku/mori-r23/QExt4Usrquota/`.
Receipt: `.ufo/waves/round-23/falsify/QExt4Usrquota/scan.json`.

## Verdict

**MATCH — the sealed expectation for `CaseExt4Usrquota` reproduces exactly.** The one
fixture-mode execution of this case produced `exit 2`, `finding_id QUOTA_STATE_UNKNOWN`,
and both ordered six-field tuples equal to the frozen expected bytes. No frozen byte was
edited, no expected byte was edited, and no host quota state was read.

This is a per-case result only. It does **not** move the C2 population total: the
population-level strict red remains the frozen `CaseEscapedSpace` contradiction
(29/30), which is reported as a mismatch, not excused, and is a different seat's case.
The quota selftest arm (49/49 at `f3dc07c`) is a separate arm and is **not** conflated
with this fixture case.

## 1. What was read before executing

| input | path | note |
|---|---|---|
| contract | `.ufo/waves/round-23/contract.md` | §C2 table, §C2 output/verdict rules |
| pre-seal amendment | `.ufo/waves/round-23/preseal-amendment.md` | "C2 final rules superseding only erroneous/ambiguous original clauses"; ext clause; mount-resolution clause; device-mismatch clause; final pre-seal clarifications |
| sealed case | `.ufo/waves/round-23/frozen/quota-cases/CaseExt4Usrquota.json` | sha256 `4db2fcd87bb1a2efcfadaff13311426eb8a6fc129663cfa486190a93ac959cda` |
| case derivation | `.ufo/waves/round-23/build/CaseExt4Usrquota.md` | author seat `MadoR22-2.CaseExt4Usrquota-8`: original proposal + appended pre-seal CORRECTION |
| proposal (untouched) | `.ufo/waves/round-23/cases-proposed/CaseExt4Usrquota.json` | sha256 `ba8b7f2018a33c1e1c9b13c914b98dee5ee33b0a5bfd37c2b5b9d2a24fa70b87` |
| corrected | `.ufo/waves/round-23/cases-corrected/CaseExt4Usrquota.json` | sha256 `4db2fcd8…` — byte-identical to the frozen sealed copy |
| sealed oracle | `.ufo/waves/round-23/oracle-quota.py` | sha256 `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` |
| production tool | `tools/mori-quota-surface.py` | sha256 `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| source rows | `corpus/SOURCES.md:88-89` (S082, S083) | anchors `section3.5:1965-2002`, `quota options:261-271` |
| retained source bytes | `.ufo/waves/round-23/evidence/sources/S082-…proc.rst`, `S083-…ext4.rst` | sha256 `e760f716…`, `7929550f…` |
| lesson/registry | `corpus/lessons/round-23.md`, `corpus/knowledge/quota-surface-r23.md` | ext clause contested then corrected by S083 |
| pinned measure evidence | `.ufo/waves/round-23/evidence/measure4/c2-after-observed.json` | independent driver run of the same case |

Source-anchor check (read-only, against the retained pinned bytes):
`S083 ext4.rst:261-265` is literally `quota, noquota, grpquota, usrquota` / "These
options are ignored by the filesystem. They are used only by quota tools to recognize
volumes where quota should be turned on" — so a visible `usrquota` mount-option key is a
**hint**, not proof of runtime accounting. `S082 proc.rst:1973-1983` gives the field
layout the case's mountinfo uses. The frozen expectation follows the amendment's ext
clause, which follows S083.

## 2. Integrity of the pinned inputs (checked before the run)

- `git merge-base --is-ancestor 22772c10f6e3c1d8d3fe1b72083a6194e9f4e687 HEAD` → true;
  same check against `f3dc07c0…` → true. The seal strictly precedes the pinned production.
- Case bytes at the seal commit == case bytes in the working tree:
  both sha256 `4db2fcd87bb1a2efcfadaff13311426eb8a6fc129663cfa486190a93ac959cda`;
  `git diff <seal> HEAD -- …/CaseExt4Usrquota.json` is empty; `git status` for the file
  is empty (unmodified).
- Tool blob is identical at the pin and at HEAD:
  `git rev-parse f3dc07c0…:tools/mori-quota-surface.py` ==
  `git rev-parse HEAD:tools/mori-quota-surface.py` == `439ff4c1a68fc4f98182c6b855b3b4c790286851`,
  file sha256 `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92`. The run
  therefore measures the pinned production, not a drifted working copy.
- Recomputed the driver's `cases_sha256_combined` over the frozen directory:
  `3323f4246ee637dd030138db330e7125d9775cf1a35a5e6be357fc596818a0e8` == the value recorded
  in `evidence/measure4/c2-after-observed.json`. The sealed case population is unmodified.

## 3. Execution (fixture mode only; never real mode)

Fixture copied from `case["fixture"]` into my scratch as
`json.dumps(fixture, sort_keys=True, indent=2) + "\n"` → sha256
`8c2259a846eff1ba97e407f5ced28888a8a5f7841e3be52f2cd7bce8557314c8`, which is **byte-identical
to the fixture the pinned oracle wrote** for this case (`fixture_sha256` recorded in
`evidence/measure4/c2-after-observed.json`). Same bytes in, same bytes out.

Canonical argv (preserved verbatim in the receipt):

```
/usr/bin/prlimit --as=402653184 /usr/bin/timeout -s KILL 15 \
  /usr/bin/python3 -I \
  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
  --fixture /fast/scratch/hyaku/mori-r23/QExt4Usrquota/fixture.json
```

Limits: 384 MiB address space (`402653184`), 15 s wall timeout with `SIGKILL`, one child at
a time. `TMPDIR=/fast/scratch/hyaku/mori-r23/QExt4Usrquota`, `PYTHONDONTWRITEBYTECODE=1`,
`PYTHONHASHSEED=0`.

Observed:

- exit code `2`
- stderr empty (sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`)
- stdout: one JSON object, sha256
  `c5df51e552a84b48cded236b4b517ab76173f7a715c88ba8da54c155b7229374`
- stdout parses as a JSON object; `schema mori-quota-surface-v1`, `df_covers_quota false`,
  `exit_code 2`, `finding_id QUOTA_STATE_UNKNOWN`, `limits` non-empty.

Repeat run (independent child, same limits) produced a **byte-identical** stdout. A third
run against the production path in the lane (rather than my scratch copy of the tool) also
produced the byte-identical stdout.

## 4. Comparison — primary six-field tuples

Primary fields (oracle `PATH_KEYS`): `path, fstype, mount_point, quota_state, enforcement, basis`.

| index | field | expected (frozen) | actual | match |
|---|---|---|---|---|
| 0 | path | `/srv/data` | `/srv/data` | ✔ |
| 0 | fstype | `ext4` | `ext4` | ✔ |
| 0 | mount_point | `/srv/data` | `/srv/data` | ✔ |
| 0 | quota_state | `unknown` | `unknown` | ✔ |
| 0 | enforcement | `n/a` | `n/a` | ✔ |
| 0 | basis | `ext_quota_option_unverified` | `ext_quota_option_unverified` | ✔ |
| 1 | path | `/srv/data/projects/app` | `/srv/data/projects/app` | ✔ |
| 1 | fstype | `ext4` | `ext4` | ✔ |
| 1 | mount_point | `/srv/data` | `/srv/data` | ✔ |
| 1 | quota_state | `unknown` | `unknown` | ✔ |
| 1 | enforcement | `n/a` | `n/a` | ✔ |
| 1 | basis | `ext_quota_option_unverified` | `ext_quota_option_unverified` | ✔ |

- `exit_match`: 2 == 2 ✔
- `finding_id_match`: `QUOTA_STATE_UNKNOWN` ✔
- `primary_tuple_match`: true (both rows, ordered) ✔
- path count actual 2 == expected 2; no extra, no missing row.

**Primary vs supplementary separation.** The scored primary denominator for this case is
the six fields above (12 field comparisons across two ordered rows) plus exit and
finding_id. Supplementary metadata is scored apart and never widens that denominator.

- The sealed case carries **no** `supplementary_expected` block, so the oracle's
  per-path supplementary assertions for this case are **0** — `read_supplementary()`
  returns an empty index map, `supplementary_note_present: false`. The nine generic
  supplementary checks the oracle still runs (schema, exit_consistency,
  output_keys_allowed, output_key_set, error_token, path_key_set, df_covers_quota,
  limits_text, no_leakage) all pass on the captured output.
- Supplementary metadata observed (not oracle-scored for this case), against the values
  the case rationale states in prose: `device_check = match` (rationale: match) ✔,
  `quota_option_keys = ["usrquota"]` (rationale: `['usrquota']`) ✔,
  `btrfs_qgroups_mode = null` (rationale: null) ✔.

### Independent oracle re-evaluation (offline, no re-execution of the suite)

Loading the sealed `oracle-quota.py` and feeding it the captured stdout and exit code
for this case: `evaluate_case` → `headline_ok True`, headline
`{exit_match: true, finding_match: true, paths_match: true}`, reason `None`,
supplementary 9/9 pass, `leakage_hits: []`. The canary set drawn from this fixture
(the btrfs UUID, the four mount sources, the `key=value` option tokens and distinctive
option values, the `dm-0` device basename) appears nowhere in stdout — no mount source,
no option value, no UUID leaked.

## 5. Why the result is the honest one (independent static trace)

I re-derived the decision statically from the sealed rules against the fixture text
(no tool execution), to confirm the tool reached the ext clause by the intended path
rather than by accident:

- **Covering mounts** for realpath `/srv/data` and `/srv/data/projects/app`: `/` (ext4
  8:1, id 25), `/srv` (tmpfs 0:41, id 30), `/srv/data` (ext4 8:2, id 31). Each mount
  point occurs exactly once → the amendment's repeated-mountpoint
  `ambiguous_overmount` refusal does not fire.
- **Longest component-prefix** selection → `/srv/data` (9 chars) over `/srv` (4) and `/`
  (1); the same mount covers the nested path by the prefix rule, so both rows report
  `mount_point /srv/data`.
- **Parent-ID rule** (final pre-seal clarification): the chosen mount's parent id is 30,
  which is present in the snapshot and *is* the id of the longest strictly shorter
  covering mount (`/srv`, id 30) → no refusal. (This is exactly the condition that the
  frozen `CaseEscapedSpace` expectation violates; it does not apply here.)
- **Device check**: chosen fstype is ext4, so the btrfs major-zero exemption does not
  apply; mount `8:2` == path `st_dev 8:2` → `device_check match`, no mismatch
  preemption.
- **Classification**: super options (last mountinfo field) are `rw,usrquota`; the key
  before `=` is `usrquota`, a quota-related ext key → `unknown` / `n/a` /
  `ext_quota_option_unverified`. Per S083 the option is a hint only.
- **Verdict precedence**: no setup error, no enabled path, at least one unknown → exit
  `2`, `QUOTA_STATE_UNKNOWN`.
- The `btrfs_sysfs` record in the fixture is an inert decoy (`qgroups false` paired with
  `qgroups_enabled null` / `qgroups_mode null`, as the amendment requires); the chosen
  fstype is not btrfs.

The tool's behaviour therefore follows the sealed rule chain, and the observed output
equals the frozen expectation for the right reasons.

## 6. Host-read fence and hygiene

- `strace -f -e trace=openat,open` over the same fixture-mode invocation: **no**
  `/proc/self/mountinfo` open, **no** `/sys/fs/btrfs/*` open, no `stat` of any probed
  path, no `ioctl`/`socket`/`mount`/`quotactl`-style privileged syscall. The only
  payload open is `<scratch>/fixture.json`; the rest are the CPython interpreter's own
  library loads. Fixture mode read no host filesystem state.
- Real mode was **never** invoked by this seat. No quota command, no mount, no
  remediation, no privileged interface, no qgroup/mode read.
- No `quotactl`/`btrfs qgroup`/`xfs_quota`/`repquota`/`mount` call was made anywhere.
- Writes are limited to: my scratch tree `/fast/scratch/hyaku/mori-r23/QExt4Usrquota/`,
  my receipt `.ufo/waves/round-23/falsify/QExt4Usrquota/scan.json`, and this report.
  No lane index, jj ref, frozen case, oracle, expectation or production file was touched.
- No live journal / journalctl / process / service / credential / agent.db / session
  transcript read. No transcript was opened at all.
- Tooling installs/updates performed: **none**. `prlimit`, `timeout`, `python3` (3.14.8),
  `strace` and `git` were already present; no `pacman`, `uv`, `cargo` or `npm` channel was
  used, so there is nothing to record against the operator tooling directive.

## 7. Residual risk and verification gaps (not defects in this case)

1. **Per-path supplementary metadata is unscored for this case.** Because the sealed
   case has no `supplementary_expected` block, the oracle asserts nothing about
   `device_check`, `quota_option_keys` or `btrfs_qgroups_mode` here. I verified them by
   hand against the case rationale and they agree, but a machine-checked guarantee does
   not exist for this case; only 1 of the 30 sealed cases (`CaseBtrfsDevMatch`) carries
   `supplementary_expected`. If the wave wants the amendment's "supplementary sealed
   checks" to bind for the ext family, the cases would need those blocks — which cannot
   be added now without editing frozen bytes, so this is a note to L1, not an action here.
2. **Exit code 2 is overloaded.** `QUOTA_STATE_UNKNOWN` and `QUOTA_SETUP` share exit 2
   and are distinguishable only by `finding_id`. This matches the contract's own
   exit-code table, so it is not a deviation, but a consumer keying on the exit code
   alone cannot separate an unknown-state verdict from a setup failure.
3. **Case-vs-driver agreement is confirmed, but the driver run is not re-run here.**
   My stdout is byte-identical to the stdout the pinned measure4 driver recorded for
   this case (`c5df51e5…`), and my recomputed `cases_sha256_combined` matches the
   driver's, so the population state is unchanged. The population-level total was not
   re-measured by this seat (no full-suite run was authorised).
4. **The `prjquota` key in the tool's ext vocabulary is not S083-backed.** It comes from
   the contract/amendment vocabulary, not from the ext4 doc (S083 documents
   `quota, noquota, grpquota, usrquota` and `jqfmt=, usrjquota=, grpjquota=`). It cannot
   change this case's outcome (`usrquota` is present) and it changes only the basis token
   between two `unknown`/`n/a` ext rows; the same observation was already raised
   independently by the S083 re-open seat.
5. **Population-level truth is unchanged by this seat.** The C2 strict target remains
   **UNPROVABLE at 29/30**: the frozen `CaseEscapedSpace` expectation conflicts with the
   sealed parent-ID rule (selected mount id 43, parent id 33, versus the strictly shorter
   `/srv` cover with id 42), and the tool correctly emits `ambiguous_overmount`. That
   contradiction is preserved unchanged in `evidence/frozen-contradiction.json`; no
   special-casing, exclusion, relabelling or rewriting was applied, and no exception was
   sought for it.

## 8. Reproduction

```
cd /fast/scratch/hyaku/mori-r23/QExt4Usrquota
/usr/bin/prlimit --as=402653184 /usr/bin/timeout -s KILL 15 \
  /usr/bin/python3 -I \
  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
  --fixture /fast/scratch/hyaku/mori-r23/QExt4Usrquota/fixture.json
# exit 2; stdout sha256 c5df51e552a84b48cded236b4b517ab76173f7a715c88ba8da54c155b7229374
# stderr empty
```

Machine-readable receipt with argv, exit, stdout/stderr and their hashes, tool/case/fixture
hashes, the given (expected) and actual objects, the per-path primary comparison and the
separately-held supplementary metadata:
`.ufo/waves/round-23/falsify/QExt4Usrquota/scan.json`.
