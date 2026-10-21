# CriticC2Scope — C2 claim versus amended targets, 27+3 cases, sampled real backend

Seat `MadoR22-2.CriticC2Scope` (UFO-FSD critic, read-only leaf). Production pinned
`f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` (tool `tools/mori-quota-surface.py` sha256
`e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92`, identical in working copy);
seal `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`; lane HEAD `6eb889c037163e4886eaa61501258910d6a529b9`.
Attack target: "C2 coverage strict target stays UNPROVABLE at 29/30".

## Verdict

The claim's number and its red identity hold. The wording "UNPROVABLE" is weaker than
the evidence supports: under the sealed rules the strict 30/30 target **cannot be met by
any conforming implementation**. Separately, the 29 passes hide one real false-negative
class in the production parser that no sealed case, selftest arm or oracle exercises. One
aggregate flag also mislabels the real backend as red. None of this needs any change to
frozen bytes. None of it promotes C2.

Axes: **correctness** (false confident verdict), **availability** (host-wide fail-closed),
**provenance** (basis tokens, aggregate flags, source-gate scope), **scope honesty**
(unprovable versus unsatisfiable; visible flag versus limit), and **independence**
(common-mode parser in tool and oracle).

## Method (static only)

- I read the contract, the pre-seal amendment, `frozen/case-decisions.json`,
  `frozen/seal-manifest.json`, all 30 `frozen/quota-cases/*.json`, `oracle-quota.py`
  (sha256 `f1f4a027…bec`), the sealed driver `build/MeasureDriver/measure-round23-v2.py`
  (sha256 `5c12fdc0…fcdefcd`), the `evidence/measure4/*` C2 receipts, `summary.json` (sha256
  `381e963e…2353`), `frozen-contradiction.json`, and sources S079/S085/S086 under `evidence/sources/`.
- I re-implemented the amended C2 rules independently, without importing or running the tool.
  I split mountinfo on `"\n"` and single ASCII `" "`. The script is
  `/fast/scratch/hyaku/mori-r23/CriticC2Scope/audit.py` (sha256 `f4eb8761…df2b`). It ran once
  over the frozen case JSON as data. It never invoked the tool, the oracle, the selftest, the
  driver or any host read.
- I ran no tool, test, selftest, oracle, driver or live host read. I made no installs or updates.
- I hashed all 30 frozen cases. Each equals its `case-decisions.json` `selected_sha256` and its
  `seal-manifest.json` entry.

## Findings

### F1 — The strict target is unsatisfiable under the sealed rules, not merely unprovable (scope honesty; confirms the red)

- My independent derivation reproduces the tool exactly: 29/30 OK, with the sole DIFF being
  `CaseEscapedSpace` (sha `8340738a…beea`). The other 26/26 primary and 3/3 discovery cases
  match on exit, finding and the six fields.
- The decisive counterexample is inside the frozen set. Two cases share one parent-ID shape:
  the selected mount's parent is present, and it equals the **shorter cover's own parent**
  rather than the shorter cover.

  | case | selected | its parent | longest shorter cover (parent) | frozen expected |
  |---|---|---|---|---|
  | `SupplementHiddenMount` | 70 `/home/x/y` | 65 | 80 `/home/x` (65) | `ambiguous_overmount` |
  | `CaseEscapedSpace` | 43 `/srv/my data` | 33 | 42 `/srv` (33) | `enabled` / `xfs_quota_option` |

  - Only mount-ID order (80>70 versus 42<43) or line order separates them.
  - The amendment forbids both: "Do not guess stack order from line order or reusable IDs".
  - So no amendment-conforming implementation can pass both rows.
- The fixture is also kernel-inconsistent. Mount 42 is visible at `/srv`, so path walk to
  `/srv/my data/sub dir` crosses into 42. A mount attached on 33's `srv/my data` dentry would be
  shadowed, and the path's `st_dev` would be 42's `0:44`, not the fixture's `0:45`. A mount created
  through the visible `/srv` would get parent 42, not 33. The expected row's case rationale
  (step 2) checks only the duplicate-mountpoint rule; it never applies the later parent-ID clause.
  The amendment's sentence "No existing case expectation changes beyond the already-corrected
  stack" was therefore false when written. [INFERENCE: the kernel path-walk and attach semantics
  are reasoned from S085/VFS behaviour, not from a host experiment.]
- Disposition: Main's directive stands. Keep the case, the rule and the oracle bytes unchanged;
  no special case, exclusion or relabel.
- Smallest correction (wording only, in the round disposition): say the strict target is
  "unsatisfiable under the sealed rule set (two frozen rows with the same parent-ID shape require
  opposite outcomes)" rather than "unprovable". Cite `SupplementHiddenMount` beside
  `frozen-contradiction.json`. An outside closure may diagnose the oracle; it still cannot turn
  29/30 into a pass.

### F2 — Unicode-whitespace and non-UTF-8 mountpoints give a false confident verdict from the wrong filesystem (correctness; HIGH; fixable, harms no sealed target)

- Code:
  - `parse_mountinfo` uses `text.splitlines()` (line 313) and `line.split()` (line 317).
    Python treats 26 non-tab/space/newline code points as whitespace for `split()`
    (0x0b 0x0c 0x0d 0x1c–0x1f 0x85 0xa0 0x1680 0x2000–0x200a 0x2028 0x2029 0x202f 0x205f 0x3000).
    `splitlines()` also breaks on several of these.
  - The kernel escapes only `" \t\n\\"` in root and mountpoint (S085 `seq_path_root(..., " \t\n\\")`,
    line 151; `seq_dentry` via `show_path`). Those other code points are emitted raw and are legal
    in filenames.
  - Real mode reads mountinfo with `errors="replace"` (line 660), but `os.path.realpath` returns
    surrogate-escaped strings. Verified: `b"/srv/a\xffb"` becomes `'/srv/a\ufffdb'` versus `'/srv/a\udcffb'`.
- Counterexample: a fixture that is valid under the amended schema (every validator in
  `load_fixture` accepts it). `\u00a0` below is a literal U+00A0.

  ```text
  1 0 0:30 /@ / rw - btrfs /dev/mapper/root rw
  40 1 0:30 /@srv /srv rw - btrfs /dev/mapper/root rw
  41 40 0:50 / /srv/a\u00a0b rw - btrfs /dev/sdz rw
  paths: /srv/a\u00a0b/x (realpath same), st_dev 0:77
  device_links {/dev/mapper/root: dm-0}
  btrfs_sysfs: UUID-A {devices [dm-0], qgroups false, enabled null}
               UUID-B {devices [sdz],  qgroups true,  enabled true}
  ```

  - How the tool handles line 41:
    - It splits into 11 fields. The separator index is 7 (≥6) with 3 trailing fields, so the
      line is accepted.
    - The mount point is parsed as `/srv/a`, which does not cover `/srv/a\u00a0b/x`.
    - The best cover becomes 40 `/srv`, and the parent check passes (parent 1 = cover 1).
    - Path major 0 on btrfs takes the `btrfs_subvolume_skipped` branch, so no device
      corroboration happens.
    - UUID-A is classified, giving `disabled` / `btrfs_qgroups_dir_absent`, exit 0 `QUOTA_DISABLED`.
  - The amended rules give mount 41, UUID-B, `enabled` / `btrfs_qgroups_enabled`, exit 1. My
    audit's single-space splitter produces exactly that.
  - Real mode reaches the same wrong-filesystem attribution with any non-UTF-8 byte in a nested
    btrfs mountpoint, with no whitespace needed.
- Reach:
  - Operator-pinned `--path` targets: false enabled or disabled from a different filesystem.
  - Default run: a crafted name can only truncate to an ASCII ancestor such as
    `/home/vgpnk/Projects/shokunin\u00a0z`. That yields either a duplicate cover
    (`ambiguous_overmount`) or, for unprivileged fuse, `device_mismatch`. Both fail closed to
    UNKNOWN. [INFERENCE: whether fusermount accepts such mountpoint names is not verified.]
  - `splitlines()` on `\r`, `\x0b`, `\x0c`, `\x1c`–`\x1e`, `\x85`, `\u2028`, `\u2029` breaks one
    line into fragments with fewer than 10 fields. Any such mount anywhere turns the whole run
    into `QUOTA_SETUP`.
- Coverage: no sealed case, selftest arm or oracle contains these code points. Grep of the
  frozen cases found none.
- Common mode: the oracle's canary extractor uses the same `splitlines()`/`split()` (lines
  127–128), so it shares the blind spot (an independence defect).
- Smallest safe correction (production only, future round; no frozen byte touched):
  - Read `/proc/self/mountinfo` as bytes and decode with `os.fsdecode`.
  - Iterate `split("\n")` and split fields with `split(" ")`.
  - My audit already uses this splitter and reproduces all 29 sealed passes and the one red, so
    the change improves correctness and regresses no sealed target.
  - Add a btrfs-major-0 corroboration gap note to the output limits. The skip means any
    resolution error on btrfs is accepted silently; the amendment's "btrfs-on-btrfs association
    unknown" is in prose only, not in output.

### F3 — `\043` (`#`) in any mount source makes every run `QUOTA_SETUP` (availability; MEDIUM; sealed-rule versus source contradiction)

- Evidence:
  - S085 line 89 shows `mangle()` is `seq_escape(m, s, " \t\n\\#")`. It is applied to the
    device name (`mangle(m, r->mnt_devname)`) and to the fstype subtype.
  - The amendment allows exactly 040/011/012/134 and makes every other escape `QUOTA_SETUP`.
  - The tool decodes the source of **every** line (line 337), not only chosen lines. One foreign
    mount with `#` in its device name (sshfs/rclone/fuse `fsname`) disables the probe for all
    paths.
- Status: this was found independently by `ReopenS085.md` D4. I confirm it from the source and
  add that it is host-wide, because of line 337. The tool conforms to the sealed rule; the rule
  contradicts S085. The lesson Gate row "S085 … Admit A for per-mount namespace field
  emission/escaping" overstates what the implemented escape set honours.
- Smallest correction: a next-round amendment adding `043→#`, and decoding/validating the source
  only for chosen lines. Not fixable this round without editing frozen rules; record it as open debt.

### F4 — `real_controls_pass=false` inherits the CaseEscapedSpace red; the real backend itself matched (provenance; MEDIUM)

- Evidence:
  - In `summary.json`, `C29.c2_real_control_matches_frozen` passes: exit 0, `QUOTA_DISABLED`, and
    both paths match on 7 fields.
  - The oracle's own `real_control.headline` in `c2-after-real-observed.json` is
    exit/finding/paths all true.
  - Its `real_control` result shows no failure, and the real-control supplementary checks pass
    (284/284 versus 274/274).
  - Yet `C30.c2_oracle_real_control_agrees` is computed as whole-run `unmet == 0` over 31 items
    (driver lines 1108–1112), so it fails only because of CaseEscapedSpace.
  - `C30` is in `REAL_CONTROL_CHECKS` (line 116–117), so the aggregate `real_controls_pass` is
    `false`. Its detail text ("no unmet real-control requirement") does not match its predicate.
- Impact: a reader of the aggregate would conclude the sampled real backend disagreed. It did
  not. There is no harm to the strict C2 red, which is correctly retained either way.
- Smallest correction: the driver is sealed, so do not edit it. State explicitly in the round
  disposition that C30 and `real_controls_pass=false` are the inherited CaseEscapedSpace unmet and
  that the C2 real control matched. A future driver should compute C30 from the oracle's
  `real_control.headline` only.

### F5 — Visible flag versus limit/usage/EDQUOT: output wording lags the amendment (scope honesty; LOW)

- Output `LIMITS`:
  - It still says "a visible btrfs qgroups **directory** does not imply that any limit is set".
    The amended witness is `qgroups/enabled`; the directory is only *initialized*.
  - Output carries no statement that `enforcement: "enforced"` (XFS and tmpfs) means a mechanism
    flag, never a nonzero limit. The amendment requires exactly that meaning. The knowledge note
    lines 38/83 say it, but the probe's own output, which consumers see, does not.
  - The supplementary `limits_text` check only requires a non-empty string, so the oracle cannot
    detect this.
- Source nuance (S086 4881–4892): tmpfs `*_hardlimit` keys are printed only when the default limit
  is nonzero. The tool's conservative "mechanism only" reading is safe but stricter than the
  source; no defect.
- FR2 scope: the default real verdict is `QUOTA_DISABLED` on both default paths. The only known
  quota-enabled host mount (`/dev/shm` tmpfs `usrquota`) is outside the defaults. SKILL.md (line
  597) and lesson23 disclose this, so it is a declared tradeoff, not a defect. But the sampled real
  backend exercises only two bases (`btrfs_qgroups_dir_absent`, `xfs_noquota_option`), both
  `disabled`. The real-only branches have **zero** real observations:
  - the `qgroups/enabled` read,
  - the `real_device_name` mapping beyond `dm-0`,
  - `path_stat_failed`,
  - `mountinfo_unreadable`.
- Fixture `btrfs_qgroups_mode` supplementary passes (for example squota) exercise a projection
  that real mode never performs (mode is never read). They are fixture facts, not backend facts.
- Smallest correction: next-round wording in `LIMITS` ("btrfs qgroups enabled …", "enforced = flag,
  not a limit"). Keep C2 claims phrased as fixture-verified classification plus a two-branch
  real sample.

### F6 — Real-only basis tokens claim the wrong cause (provenance; LOW; unscored)

- `classify_btrfs` returns basis `btrfs_device_unmapped` when `qgroups is None` (lines 474–476),
  that is, when the qgroups stat failed with a non-ENOENT error after a **successful** unique
  device mapping. A full `/sys/fs/btrfs` listing failure (`scan_btrfs_sysfs` returns `{}`) also
  reports `btrfs_device_unmapped`.
- A per-UUID `devices` listing error is silently `[]` (lines 593–596). That can turn a true
  two-UUID ambiguity into a unique match.
- The state is correctly `unknown` in the first two cases, so these are not false-disabled. The
  amendment's "parent listing error is unknown, NEVER absent/disabled" holds.
- Fixture mode cannot express `qgroups: null`, so no sealed case covers these branches.
- Smallest correction (future round): a distinct basis (for example
  `btrfs_sysfs_unavailable`), and treating a devices-listing error as unknown rather than empty.

## Not attacked successfully (holds)

- The before/after C2 counts in `measure4` are consistent: 0/30 with `capability_absent=30`
  before, then 29/30 (unmet 1) after. With the real expected it is 30/31. Supplementary checks
  are 274/274 and 284/284.
- The selftest correction `56ac3ba→f3dc07c` is a one-line change to the selftest arm
  `escaped-mount-point` `st_dev` (`259:1→259:2`). It matches that arm's own mount line. It is
  separate from the frozen CaseEscapedSpace, whose bytes are unchanged.
- The real-mode readset never opens `qgroups/mode` (lines 615–620), and the output fence emits no
  source, UUID or option values.
- Device mismatch preemption, the XFS precedence, ext always-unknown, tmpfs four hardlimit names
  and the verdict precedence all match the amendment in code and in my independent derivation.

## Provenance note

`case-decisions.json` names `cases-corrected/CaseTmpfsNoQuota.json` as the selected file for
`CaseTmpfsNoQuota` (sha `7afd98c1…49b5`). No such path exists in `4dc80c1`, `c1e8b81`, `22772c1`
or the working tree. The bytes exist only as `frozen/quota-cases/CaseTmpfsNoQuota.json`, and the
seal manifest pins them. `cases-proposed/CaseTmpfsNoQuota.json` has different bytes (sha
`f4814c94…`). The selected bytes are sealed, so the strict count is unaffected, but the
author-bytes chain for this one primary case is not reproducible from the named path.

## Open debt (unchanged, not cleared)

- Four unallowlisted inherited hits (raw95 / allowlisted86 / non-author5).
- Original permission control RED 11/12.
- Two unknown dispositions.
- Baseline acceptance blocked.
- `privacy_clearance=false`.

This review is critic advice only. It is not admission, closure or promotion authority.
