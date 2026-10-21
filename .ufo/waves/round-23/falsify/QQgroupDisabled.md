# Falsification seat QQgroupDisabled — round 23, C2, sealed fixture case `SupplementQgroupDisabled`

Verdict: **MATCH** (exit, finding_id and every ordered six-field tuple equal the sealed expectation).
No frozen case/rule/oracle byte was edited. Receipt: `.ufo/waves/round-23/falsify/QQgroupDisabled/scan.json`.

## 1. Axes

| axis | definition for this seat | result |
|---|---|---|
| A1 argument fidelity | exact argv, tool bytes, fixture bytes, wrapper limits preserved | PASS (4 pre-exec attempts recorded; 1 real invocation) |
| A2 process envelope | exit code, stderr emptiness, timeout | PASS (exit 0, stderr 0 bytes, <15 s) |
| A3 primary classification | exit + `finding_id` + ordered six-field tuples vs sealed `expected` | PASS (1/1 path, tuple-identical) |
| A4 supplementary metadata | `device_check`, `quota_option_keys`, `btrfs_qgroups_mode` vs amendment-derived values, reported separately from the primary denominator | PASS (3/3) |
| A5 information containment | no uuid / mount source / super-option values / filenames leaked in stdout | PASS (0 hits) |
| A6 isolation | fixture mode only, no host read, no other case, no driver | PASS |

## 2. What was executed (and nothing else)

* Sealed case: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/SupplementQgroupDisabled.json`
  * sha256 `f117bcb0b411cb2dd50910c62222481d8d283eeb49ff2169b40788b24dd09567`, 5171 bytes — identical to `frozen/seal-manifest.json` (sha256 + byte count) and to the committed git blob `a12e9e66caf47c0a0c937d88879fdd7eb1347808` at the pinned revision `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`.
  * `frozen/case-decisions.json` records it as `selected: cases-supplemental/SupplementQgroupDisabled.json`, `primary: false`, reason "Source-review discovery guard before candidate inspection/result". It is one of the 3 source-review supplemental C2 cases, **not** one of the 27 independent primary cases; it never enlarges the primary denominator.
* Candidate tool: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py`
  * sha256 `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92`, git blob `439ff4c1a68fc4f98182c6b855b3b4c790286851`.
  * `git diff f3dc07c0… HEAD -- tools/` is empty: the working-copy tool is byte-identical to the pinned production tool, so this measurement is on the pinned production bytes.
* Synthetic fixture: copied from `case["fixture"]` into `/fast/scratch/hyaku/mori-r23/QQgroupDisabled/fixture.json`
  (922 bytes, sha256 `3908b4e3f3eaa2ad9ba6875bfb7ee56109387a68fa7d2326c622e17d26c7a7aa`; `json.loads(fixture) == case["fixture"]` → True). The sealed case file itself was never written to.
* argv (given): `python3 -I <TOOL> --fixture /fast/scratch/hyaku/mori-r23/QQgroupDisabled/fixture.json`
  wrapper: `timeout 15 prlimit --as=402653184 --cpu=15 …` (402653184 B = 384 MiB).
* stdout: `/fast/scratch/hyaku/mori-r23/QQgroupDisabled/stdout.txt` (975 B, sha256 `81d9301d2e051f145fe94afb0c8928927e67c4fe881d01962be0db1f66857231`)
  stderr: `…/stderr.txt` (0 B, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` — empty).

### Given vs actual envelope (recorded, not normalised away)

* **given**: mode `fixture`, address-space limit 384 MiB, timeout 15 s, one child at a time, real mode forbidden.
* **actual**: children spawned 4; successful tool invocations **1**; pre-exec failures 3, none of which reached the interpreter or produced tool output:
  1. `prlimit --as=393216` — util-linux here parses raw bytes, so this was **384 KiB**, not 384 MiB: `/bin/echo` and `python3` both died with SIGSEGV, exit **139**, empty stdout/stderr.
  2. `prlimit --as=1048576` (1 MiB): loader error `failed to map segment from shared object`, exit **127**.
  3. `prlimit --as=384M`: `prlimit: failed to parse AS limit`, exit **1** (no `M` suffix accepted by this build).
  4. `prlimit --as=402653184` (384 MiB) → the measurement run: exit **0**.
  Only attempt 4 executed the case. Measured interpreter footprint (17.6 MB VmPeak) confirms 384 MiB is ample; the three failures were unit/parsing errors in my wrapper, not tool behaviour.
* No background jobs, no subagents, no driver, no selftest, no build/lint.

## 3. Primary comparison (six scored fields, ordered)

Expected (sealed `expected.paths[0]`) vs actual (tool stdout `paths[0]`), field order
`(path, fstype, mount_point, quota_state, enforcement, basis)`:

| # | field | expected | actual | = |
|---|---|---|---|---|
| 1 | path | `/home/quota/disabled` | `/home/quota/disabled` | ✅ |
| 2 | fstype | `btrfs` | `btrfs` | ✅ |
| 3 | mount_point | `/home` | `/home` | ✅ |
| 4 | quota_state | `disabled` | `disabled` | ✅ |
| 5 | enforcement | `n/a` | `n/a` | ✅ |
| 6 | basis | `btrfs_qgroups_disabled` | `btrfs_qgroups_disabled` | ✅ |

* exit: expected `0` → actual `0` ✅ (`stdout.exit_code` field also `0`, consistent with the process exit).
* finding_id: expected `QUOTA_DISABLED` → actual `QUOTA_DISABLED` ✅.
* path count: expected 1 → actual 1 ✅ (order preserved; single path).
* output schema `mori-quota-surface-v1`; top-level key set exactly `{df_covers_quota, exit_code, finding_id, limits, paths, schema}`; `df_covers_quota: false` ✅.

**Primary verdict: MATCH (1/1 path, 6/6 fields, exit and finding_id equal).**

## 4. Supplementary metadata (reported separately, never folded into the primary denominator)

Derived from `preseal-amendment.md` §C2 final rules (btrfs bullet, mount-resolution bullet, device-mismatch bullet,
"quota_option_keys=[] / btrfs_qgroups_mode=null on preemption", XFS/btrfs option-leak rule):

| field | expected (from rules) | actual | = |
|---|---|---|---|
| `device_check` | `btrfs_subvolume_skipped` (fixture `st_dev 0:57` ⇒ stat major 0 ⇒ btrfs equality skipped) | `btrfs_subvolume_skipped` | ✅ |
| `quota_option_keys` | `[]` (btrfs mechanism is sysfs, not mount options) | `[]` | ✅ |
| `btrfs_qgroups_mode` | `null` (fixture `qgroups_enabled:false` ⇒ mode must be null; real mode never reads mode) | `null` | ✅ |

Supplementary verdict: 3/3 match. These are *not* scored against the sealed six-field expectation and do not change it.

## 5. Rule-path audit (why the match is a real derivation, not a coincidence)

* Mount resolution (tool `resolve_mount`, `tools/mori-quota-surface.py:440-468`): covering mountpoints for realpath
  `/home/quota/disabled` are `/` (id 25) and `/home` (id 26); each occurs once ⇒ no repeated-mountpoint
  `ambiguous_overmount` refusal; longest component-prefix wins ⇒ `/home` (id 26); the trailing empty line is ignored.
  Parent-ID guard: chosen mount's parent id `25` **is** the id of the longest strictly-shorter covering mount `/` (25) ⇒ no
  `ambiguous_overmount` refusal on that axis either. Correct line parsed: `26 25 0:30 /@home /home … - btrfs /dev/mapper/root rw,space_cache,subvolid=256,subvol=/@home`.
* Device check: fstype is btrfs and the fixture stat major is 0 ⇒ equality is skipped, not a `device_mismatch` preemption ⇒ `btrfs_subvolume_skipped`.
* Source resolution: raw decoded source `/dev/mapper/root` is looked up in `device_links` ⇒ mapped basename `dm-0` ⇒ compared against each UUID's `devices` list ⇒ exactly one UUID (`3c8f5a71-…`) lists `dm-0` ⇒ one match, not zero/several ⇒ `btrfs_device_unmapped` does not apply.
* btrfs state (tool `classify_btrfs`, `tools/mori-quota-surface.py:470-484`): `qgroups: true` (directory present = INITIALIZED) with `qgroups_enabled: false` ⇒ `disabled / n/a / btrfs_qgroups_disabled`, mode null — the amendment's "present plus enabled=false" branch, not the older `btrfs_qgroups_dir_absent` branch (that one is reserved for an absent directory on a successful parent inspection).
* Verdict precedence: no `enabled` path, no `unknown` path ⇒ exit `0` `QUOTA_DISABLED` (not a capacity, health, clearance or admission verdict; ENOSPC can coexist).
* Containment: stdout contains no uuid, no `/dev/mapper/root`, no `dm-0`, no `space_cache`/`subvolid`, no `@home`; only the path, fstype, mount point, states, basis and the fixed `limits` text are emitted (grep over stdout: 0 hits).

## 6. Findings / defects

**None.** No mismatch in exit, finding_id, path count, ordered six-field tuples or supplementary metadata; no leakage;
no frozen byte touched; the fixture-mode invocation stayed inside the declared envelope (one child, 384 MiB, 15 s).

## 7. Explicitly not excused by this seat

* The frozen **`CaseEscapedSpace`** strict red (selected `/srv` parent 33 vs the shorter `/srv` 42 conflict with its expected
  enabled row) is **a separate reported mismatch**, not a pass and not excused here. This seat did not execute that case and
  does not claim anything about it; the full-driver exit 1 caused by that strict red stays a failure to be reported by the
  driver owner.
* `QUOTA_DISABLED` here is a *visible-disabled* classification of one synthetic path only. It is not a capacity verdict, not
  a health verdict, not privacy clearance, not admission, and not evidence that any limit is or is not set.
* Open debt is unchanged by this seat: four unallowlisted inherited hits, original permission control RED 11/12, two unknown
  dispositions, baseline acceptance blocked, `privacy_clearance=false`.

## 8. Residual risk and verification gaps

1. **Single case, single mode.** Only one supplemental case of the 3, in fixture mode only. The other two supplemental cases
   (`SupplementHiddenMount`, `SupplementQgroupUnknown`) and all 27 primary cases, plus the real-mode control
   (`frozen/c2-expected-real.json`), were not exercised by this seat — they are other seats' scope. This result says nothing
   about them.
2. **Fixture-only fidelity.** The tool's real-mode btrfs path (reads `qgroups`/`qgroups_enabled`, never `qgroups/mode`) and its
   `/proc/self/mountinfo` parsing are not exercised here; only the fixture parser and classifier ran. Real-mode safety claims
   (enabled-first, mode never read, permission error ⇒ unknown) remain unmeasured by this seat.
3. **Amended-rule reading.** The `btrfs_qgroups_disabled` basis, `qgroups_enabled` fixture member and `btrfs_qgroups_mode`
   output spelling were taken from `preseal-amendment.md` §C2 final rules (the amendment supersedes the original contract's
   btrfs bullet). The tool implements those same rules, so agreement is expected by construction; it confirms
   implementation⇄rule consistency, not independent rule correctness.
4. **Wrapper failures are mine, not the tool's.** Three pre-exec failures came from my `prlimit` unit/parse errors and produced
   no tool output; they are recorded in the receipt (`pre_exec_failure_note`) rather than discarded. Any other seat that used
   `prlimit --as=<KiB>` silently measured nothing (exit 139, empty output) — worth flagging to the driver owner, since an empty
   stdout could be mistaken for a tool result.
5. **Not verified here:** `df_covers_quota` semantics beyond the literal `false`; the `limits` text against the amendment's
   required boundary wording; the 27-case primary denominator arithmetic; the C1 calibration arm (separate seats).

## 9. Tooling

No installs, updates or system changes were needed or performed by this seat (only `python3` 3.14.8, `prlimit`, `timeout`,
`sha256sum`, `git` read-only subcommands). No `pacman` transaction was attempted. TMPDIR/scratch under
`/fast/scratch/hyaku/mori-r23/QQgroupDisabled/` only; no `/tmp` use, no `/fast` fallback elsewhere, no writes outside
this seat's report and receipt.
