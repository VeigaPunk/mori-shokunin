# QBtrfsQgroup — round-23 C2 falsification of the sealed case `CaseBtrfsQgroup`

Seat: `MadoR22-2.QBtrfsQgroup` · lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`
Scratch (all deliberate scratch): `/fast/scratch/hyaku/mori-r23/QBtrfsQgroup/`
Receipt: `.ufo/waves/round-23/falsify/QBtrfsQgroup/scan.json`
Claim under falsification: **C2** (coverage — FR2/EDQUOT quota-surface observability), strict six-field denominator.
Case under falsification: **exactly one** — `frozen/quota-cases/CaseBtrfsQgroup.json`.

**Headline: `CaseBtrfsQgroup` MATCHES. exit 1 / `QUOTA_ENABLED` / one six-field tuple identical to the sealed
expectation. No mismatch in this case.** This seat therefore contributes no red of its own to the C2 strict
denominator; it says nothing about the other 29 sealed cases (see *Scope and non-claims*).

---

## 1. Scope and non-claims

* Exactly one case was executed: `CaseBtrfsQgroup`. The sealed directory `frozen/quota-cases/` (30 files) was
  **not** run as a set; the sealed oracle was pointed at a scratch directory holding only this one case file.
* **Real mode was never invoked.** No `--path`, no default-path run, no `/proc/self/mountinfo` read, no
  `/sys/fs/btrfs` read, no `quotactl`/`btrfs qgroup`/`xfs_quota`/`repquota`/`mount`, no remediation.
* `CaseEscapedSpace` was **not** executed by this seat (single-case mandate). I make no claim about it; its
  expected strict red is outside my scope and is neither confirmed nor excused here.
* No build, test, lint, formatter, gate or full-suite run. No source, expectation, oracle or frozen byte was
  edited. `git diff HEAD -- .ufo/waves/round-23/frozen/quota-cases/CaseBtrfsQgroup.json` is empty.
* No subagent dispatch (leaf seat). No tool installs (nothing needed).

## 2. Bytes under test (exact identities)

| Object | Path | sha256 |
|---|---|---|
| Sealed case | `.ufo/waves/round-23/frozen/quota-cases/CaseBtrfsQgroup.json` | `38a7d5b94f8b08ddee9c7080cca8786db0cc6aa8423dcef75d8250c58d462188` |
| Production probe | `tools/mori-quota-surface.py` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| Sealed oracle | `.ufo/waves/round-23/oracle-quota.py` | `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` |
| Scratch fixture (`case["fixture"]` copied by value) | `/fast/scratch/hyaku/mori-r23/QBtrfsQgroup/fixture.json` | `595949af67dd1856795832f45fda3e2c3c6d09ed3ec06b4abe4158d7a3df149d` |

* Seal commit `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` ("seal all oracle inputs before production
  implementation") is a strict ancestor of the pinned production revision
  `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` (`git merge-base --is-ancestor` → 0).
* The production blob at `f3dc07c` is `439ff4c1a68fc4f98182c6b855b3b4c790286851`, byte-identical to the
  working-tree `tools/mori-quota-surface.py` at HEAD `6eb889c037163e4886eaa61501258910d6a529b9`. The bytes
  falsified here **are** the pinned production bytes.

## 3. The one execution (argv preserved)

```
argv = prlimit --as=402653184 -- timeout 15 python3 -I \
         /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
         --fixture /fast/scratch/hyaku/mori-r23/QBtrfsQgroup/fixture.json
TMPDIR=/fast/scratch/hyaku/mori-r23/QBtrfsQgroup/
```

* exit = **1**, no timeout, stderr = **empty (0 bytes)**, stdout = 976 bytes, one JSON object.
* stdout (verbatim, full):

```json
{"df_covers_quota":false,"exit_code":1,"finding_id":"QUOTA_ENABLED","limits":"no per-user, per-group or per-project limit or usage is read. no NFS or server-side quota and no overlay or fuse quota is covered. a visible btrfs qgroups directory does not imply that any limit is set. an ext2/ext3/ext4 quota feature in the superblock is unobservable without privileged tools. sysfs and mountinfo races during quota enable, disable or remount are not excluded. df capacity percentages never cover quota exhaustion (FR2 / EDQUOT). QUOTA_DISABLED is not a capacity or health verdict; ENOSPC can coexist. the btrfs qgroups mode attribute is never read, so btrfs_qgroups_mode is null in real mode.","paths":[{"basis":"btrfs_qgroups_enabled","btrfs_qgroups_mode":"qgroup","device_check":"btrfs_subvolume_skipped","enforcement":"unknown","fstype":"btrfs","mount_point":"/home","path":"/home/quota/data","quota_option_keys":[],"quota_state":"enabled"}],"schema":"mori-quota-surface-v1"}
```

## 4. Primary comparison (scored denominator — six fields only)

| Field | Sealed expectation | Observed | Match |
|---|---|---|---|
| exit | 1 | 1 | ✅ |
| finding_id | `QUOTA_ENABLED` | `QUOTA_ENABLED` | ✅ |
| tuple 0 `path` | `/home/quota/data` | `/home/quota/data` | ✅ |
| tuple 0 `fstype` | `btrfs` | `btrfs` | ✅ |
| tuple 0 `mount_point` | `/home` | `/home` | ✅ |
| tuple 0 `quota_state` | `enabled` | `enabled` | ✅ |
| tuple 0 `enforcement` | `unknown` | `unknown` | ✅ |
| tuple 0 `basis` | `btrfs_qgroups_enabled` | `btrfs_qgroups_enabled` | ✅ |

Ordered tuple lists compared element-wise (`expected.paths` vs `paths`), one row per side → **paths_match true**.
**Verdict: MATCH.**

## 5. Supplementary metadata — observed, NOT scored

This sealed case carries **no** `supplementary_expected` block (`case_keys` = `schema,id,scenario,fixture,
expected,rationale,sources`). The values below are therefore observations only and are deliberately kept out of
the primary denominator:

| Supplementary field | Observed | Where it comes from |
|---|---|---|
| `device_check` | `btrfs_subvolume_skipped` | stat major 0 → btrfs equality skip (`tools/mori-quota-surface.py:536-539`) |
| `quota_option_keys` | `[]` | btrfs mechanism is sysfs, not mount options (`:360-372`) |
| `btrfs_qgroups_mode` | `qgroup` | fixture-mode projection of `qgroups_mode` (`:465-484`, `:753-765`) |
| output path key set | exactly the 9 documented keys | `OUTPUT_FIELDS` |
| output top-level key set | `df_covers_quota, exit_code, finding_id, limits, paths, schema` | no `error` token (not a setup error) |

## 6. Independent cross-check with the sealed oracle (single case only)

The sealed oracle `oracle-quota.py` (v3) was run against a scratch directory containing **only**
`CaseBtrfsQgroup.json` (sha256 identical to the frozen file), so no other sealed case was executed:

```
counts: {"capability_absent": 0, "pass": 1, "total": 1, "unmet": 0}
supplementary_counts: {"pass": 9, "total": 9, "unmet": 0}
finding_id: R23_C2_QUOTA_CASES_MATCH        oracle exit 0
case status: pass   headline: exit_match=true finding_match=true paths_match=true
supplementary: schema, exit_consistency, output_keys_allowed, output_key_set, error_token,
              path_key_set, df_covers_quota, limits_text, no_leakage  → 9/9 pass
```

`no_leakage` passed: the fixture's mount source `/dev/mapper/root`, the synthetic UUID
`7e764e88-d285-6099-0408-9ade09688840` and the option values (`subvolid=256`, `subvol=/@home`) appear nowhere in
stdout.

## 7. Independent re-derivation (read against the amendment + tool source, before trusting the run)

I re-derived the expectation from `preseal-amendment.md` and the tool source, then checked the run against it:

1. **Mount resolution** (`:311` `parse_mountinfo`, `:407` `covering_mounts`, `:421` `resolve_mount`).
   The five fixture lines all carry the separator with exactly three trailing fields (`btrfs`,
   `/dev/mapper/root`, `rw,space_cache,subvolid=256,subvol=/@home`); the trailing newline is ignored.
   Covering mount points for realpath `/home/quota/data` are `/` (id 25) and `/home` (id 26); both occur exactly
   once → no `ambiguous_overmount` refusal; longest wins → `/home`. The parent-id cross-check passes because the
   chosen mount's parent id (25) **is** the id of the longest strictly shorter covering mount (25).
2. **Device gate** (`:534-547`). `st_dev 0:57` ≠ mount `0:30`, but the stat major is 0, so the btrfs
   subvolume skip applies → `device_check btrfs_subvolume_skipped`, **no** `device_mismatch` preemption.
3. **Device → uuid** (`:681` `probe_fixture` → `device_names` closure, `:465` `classify_btrfs`). Raw decoded
   source `/dev/mapper/root` is looked up in `device_links` → `dm-0`; exactly one UUID record lists `dm-0` →
   the zero/multiple-match refusal does not apply.
4. **btrfs row** (`:474-484`). `qgroups: true` (initialized) + `qgroups_enabled: true` → `enabled` / `unknown` /
   `btrfs_qgroups_enabled`; `qgroups_mode: "qgroup"` projected as informational only.
5. **Verdict** (`:561` `verdict`). One path, enabled, no unknown sibling → exit 1, `QUOTA_ENABLED`.

The re-derivation and the frozen expectation agree on all six fields; the observed run agrees with both.
Note the case's `basis` token `btrfs_qgroups_enabled` is the amendment's rename of the original contract token
`btrfs_qgroups_dir_present` (the original contract's "directory present ⇒ enabled" reading is superseded by the
amendment's "present ⇒ initialized"); the case rationale cites exactly that supersession.

## 8. Discriminating probes (scratch copies only — frozen bytes untouched)

Five scratch variants of the same fixture were run to prove the case is not passing for an accidental reason
(one child at a time, same `prlimit`/`timeout` envelope):

| Probe (only this field changed) | exit | finding_id | quota_state | basis |
|---|---|---|---|---|
| `qgroups_enabled: false` | 0 | `QUOTA_DISABLED` | disabled | `btrfs_qgroups_disabled` |
| `qgroups_enabled: null` | 2 | `QUOTA_STATE_UNKNOWN` | unknown | `btrfs_qgroups_enabled_unavailable` |
| `qgroups: false` (dir absent) | 0 | `QUOTA_DISABLED` | disabled | `btrfs_qgroups_dir_absent` |
| `device_links` emptied | 2 | `QUOTA_STATE_UNKNOWN` | unknown | `btrfs_device_unmapped` |
| `st_dev: "259:1"` (nonzero major) | 2 | `QUOTA_STATE_UNKNOWN` | unknown | `device_mismatch` |

Every neighbouring state produces a different basis/finding/exit, exactly as the amendment prescribes. The
sealed expectation is therefore a discriminating constraint on the production probe, not a coincidence.

## 9. Findings (by severity)

**F1 — LOW (documentation / provenance; no behavioural effect). The shipped probe's module docstring is stale and
self-contradictory.**
`tools/mori-quota-surface.py:2` opens `"""mori-quota-surface-v3.py — …"""` and `:5-8` states it is "authored
alongside `mori-quota-surface.py` (the original, unaltered) and `mori-quota-surface-v2.py`". In the shipped tree
the *production* file **is** `tools/mori-quota-surface.py`, and it is byte-different from all three build
candidates (`.ufo/waves/round-23/build/ImplQuota/mori-quota-surface.py` `6b553154…`, `-v2.py` `5c8b251d…`,
`-v3.py` `5199e97b…`, production `e4857413…`). The production file additionally carries post-candidate fixes
relative to `-v3.py` (the `classify()` result-unpacking fix at `:551`, non-empty/exact-key fixture path validation
at `:711` and `:715-716`, `limits` emitted as one string at `:781`, and two added selftest arms). A reader of the shipped
file is told the shipped file is "the original, unaltered", which is false. No case expectation depends on this,
and I observed no behavioural effect (the case passes). Read-only seat: reported, not fixed. (Corroborated
independently by sibling seat `QBtrfsSquota`; same root cause, so this is a cross-seat duplicate, not a new
claim.)

**F2 — LOW (diagnostics precision; real mode only).** `classify_btrfs` (`:472`, `:477`) returns basis
`btrfs_device_unmapped` both for "no UUID lists this device" and for "the qgroups directory could not be
inspected" (`record["qgroups"] is None`). The second condition names a different fact than the token suggests.
The *state* is right (unknown, never absent/disabled, as the amendment demands) and the fixture schema cannot
express that state at all (`load_fixture` enforces `type(qgroups) is bool`, `:753`), so the case is unaffected;
only real-mode diagnostics would read imprecisely. Contract-compliant, worth a token rename in a later round.

**F3 — INFO (coverage gap in the sealed case, not a defect in the probe).** The sealed case pins no
`supplementary_expected` block, so `device_check`, `quota_option_keys` and `btrfs_qgroups_mode` are unasserted
for it. Consequences: (a) the btrfs stat-major-0 skip is constrained only *indirectly*, through `basis` — an
implementation that emitted `device_check: "mismatch"` while still classifying `enabled` would pass this case;
(b) the fixture-mode mode projection `"qgroup"` is unconstrained — an implementation that projected `null` in
fixture mode would also pass. The oracle's 9 supplementary checks for this case are generic (schema,
exit_consistency, key sets, `df_covers_quota`, `limits_text`, `no_leakage`); none is case-specific. The case
author declared the three supplementary facts in `build/CaseBtrfsQgroup.md` §4a.2, but sealing them into the
case file was not done. The primary six-field denominator is unaffected — the amendment's "never insert
supplementary keys into the independent six-field primary expectations" rule was honoured.

**F4 — INFO (lane hygiene).** An untracked `tools/__pycache__/mori-quota-surface.cpython-314.pyc` (mtime 15:17)
sits inside the tracked `tools/` directory. It predates this seat's first write (15:32:30) and was not produced
here (this seat only executed the probe as a script, which writes no bytecode). It is not in the frozen/case
bytes, but a naive `git add -A` in the lane would sweep it into a commit. No action taken (read-only seat, and
deleting files I did not create is out of scope).

## 10. Residual risk and verification gaps

* **Single-case coverage.** This seat falsified exactly one of the 30 sealed cases. The C2 strict denominator
  (29/30) and the `CaseEscapedSpace` red are **not** attested here — neither confirmed nor excused. Any claim
  that "the only remaining red is the frozen contradiction" requires the driver's own full-run record.
* **Real mode is unverified by this seat.** The amendment's real-mode safety correction (never read
  `qgroups/mode`; emit `btrfs_qgroups_mode: null`) is present in the source (`:571-650`, and the emitted limits
  text says so) but was not exercised: real mode is out of my mandate and the host's btrfs sysfs must not be
  read under the lane bounds.
* **No syscall-level proof of host isolation in fixture mode.** The evidence is code-path based:
  `main` → `probe_fixture` → `load_fixture` (`:695`) opens only the fixture file; `scan_btrfs_sysfs`,
  `real_inputs` and `real_device_name` are never reached; the fixture's UUID and device basename are synthetic
  literals that could not have come from the host. A `strace`-level capture was not taken (extra tooling not
  installed for this).
* **Probe confidence.** The five discriminating probes (§8) exercise the branches adjacent to this case, but the
  btrfs path is one of several; a defect in an unexercised branch would not show up here. That is precisely what
  the sibling seats (xfs / tmpfs / ext / btrfs-sibling / boundary) cover.

## 11. Evidence index

* Receipt: `.ufo/waves/round-23/falsify/QBtrfsQgroup/scan.json` (argv, exit, stdout, stderr, tool/case/fixture
  hashes, primary comparison, supplementary-observed block, oracle cross-check, all five probe records,
  explicit non-claims).
* Scratch (not part of the lane): `/fast/scratch/hyaku/mori-r23/QBtrfsQgroup/` — `fixture.json`, `stdout.txt`,
  `stderr.txt`, `one-case/CaseBtrfsQgroup.json`, `oracle-one-case.json`, `oracle-summary.json`,
  `probe-results.json`, `probe_*.json`.
* Files written by this seat: exactly two — the receipt above and this report. No code, expectation, oracle or
  frozen byte was touched.
