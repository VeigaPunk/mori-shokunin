# CriticNoHarm — round23 fresh falsification (all-axis no-harm)

Seat `MadoR22-2.CriticNoHarm`, read-only critic. Pinned production
`f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`, seal `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`
(verified: strict ancestor of the pin). Lane HEAD at review time is `6eb889c` (evidence/payload
commit only: LOG.md +17 lines, no tool changes).

**What I did:** static reads of `contract.md`, `preseal-amendment.md`, frozen cases, sealed
decisions, `corpus/lessons/round-23.md`, the measure4 receipts, and the production sources via
`git show`. I also ran a read-only Python check of builtin `str.split` semantics, and a static
re-implementation of the retention line-scan over `git show` blobs.

**What I did not run:** the production tools, oracles, driver or selftests. There were no host
probes and no quota/sysfs/mountinfo reads, and nothing was installed.

The two fixture files under `falsify/CriticNoHarm/` are **unexecuted** synthetic data. Every
predicted tool output below is a static trace of the pinned source: `[INFERENCE]` until an
authorized seat runs it.

## Axes

The held scores are calibration 5 (C1), coverage 6 (C2), operability 7, depth 5, freshness 5 and
adjacency 6. These cross-cutting properties are also attacked:

- no false-disabled evidence;
- read and output fences;
- whether source claims match their sources;
- caller migration;
- whether the retained debt is preserved;
- whether any speculative Core movement has happened.

## Verdict summary

| # | Finding | Class | Axes |
|---|---|---|---|
| F1 | Unicode-whitespace field split in `parse_mountinfo` can turn an enabled btrfs mount into **QUOTA_DISABLED** (a false disabled) | fixable production defect, no sealed byte affected | C2 coverage/calibration, no-false-disabled |
| F2 | The sealed amendment's escape set omits the kernel's `\043` (`#`) for the source field, so any `#` source anywhere makes the whole real run fail as QUOTA_SETUP | source-claim defect **inside a sealed rule**; a tradeoff the judge must weigh, not a silent fix | freshness/source fidelity, operability |
| F3 | `real_controls_pass=false` / check C30 red comes only from CaseEscapedSpace riding inside the `--real-expected` run; the LOG says "real control matches" without naming C30 | reporting precision | calibration of the evidence |
| F4 | The SKILL.md quota row is published in production without stating that strict C2 is unadmitted (29/30) | speculative Core exposure (doc), fixable | adjacency/operability, admission discipline |
| F5 | Untracked `__pycache__` written into `.ufo/waves/round-22/frozen/` (14:00:23) and `tools/` (15:17:10) | output-fence debt (bytes of tracked/sealed files unchanged) | fences |
| F6 | `btrfs_device_unmapped` is also emitted when the device *was* mapped but `qgroups` stat failed (real mode only) | basis mislabel, fail-closed | calibration of the basis |
| F7 | Standalone `quota-selftest-corrected.json` records no env, so the no-/tmp fence is unproven for that run | receipt gap | fences |

These were held (attacked, not falsified):

- C1 source and byte guard, and C1 caller migration;
- retained debt of 4 hits and identities at the pin;
- the frozen-byte invariance;
- the strict-C2 UNPROVABLE disposition;
- the selftest-correction separation;
- the read fence of the real-mode readset.

## F1 — mountinfo split on Unicode whitespace yields a false disabled (counterexample)

**Evidence.** In `tools/mori-quota-surface.py@f3dc07c`, `parse_mountinfo` uses
`text.splitlines()` and then `fields = line.split()` (lines 313/317). The no-argument
`str.split()` splits on *all* Unicode whitespace.

The kernel (S085 `fs/proc_namespace.c:151`, `seq_path_root(..., " \t\n\\")`; `show_path`
likewise) escapes only space, tab, newline and backslash. It emits U+00A0, U+3000, U+2000–200A
and `\x1c`–`\x1f` raw.

I checked the builtin semantics (Python check, not a tool run):
`'50 33 0:52 /@x\u00a0y /data rw - btrfs /dev/sda2 rw'.split()` gives
`['50','33','0:52','/@x','y','/data',...]`, while `.split(' ')` keeps `'/@x\xa0y'` intact.
Because the separator check (`separator >= 6`) and the last-three-fields check still hold,
the shifted line parses "successfully": `mount_point = fields[4]` becomes the root-field
fragment (`"y"`).

**Counterexample** (`falsify/CriticNoHarm/nbsp-root-shift.fixture.json`,
sha256 `b82a00537197f20508c08ba2470cb72dc1125e361a9fb552a110d10f31ae9a7f`): btrfs root at `/` with qgroups absent (dm-0), plus a bind of directory
`/@data/my<NBSP>dir` of a *different* btrfs filesystem (dm-1) with qgroups enabled, mounted at
`/data`. The path is `/data/f` with an anonymous st_dev of `0:60`.

The static trace goes like this:

1. Mount 50 parses with mount point `"dir"`, so it covers nothing.
2. Only `/` (id 33) covers the path, and there is no shorter cover, so the parent rule cannot fire.
3. The btrfs device check is skipped because the path's major is 0.
4. The source `/dev/mapper/root` maps to dm-0, whose qgroups are absent.
5. The result is `disabled`/`btrfs_qgroups_dir_absent`, **exit 0 QUOTA_DISABLED**.

The contract-correct parse resolves mount 50 at `/data` (its parent 33 is the longest shorter
cover, so it is consistent) to dm-1 with enabled true. That gives **exit 1 QUOTA_ENABLED**.

This is exactly the harm the knowledge note and SKILL forbid ("never fabricated disabled
evidence"). A NBSP in a mount point instead of the root field is caught by the device check or
a setup failure; the root-field and btrfs-skip combination is the escaping path. Characters
that are also line boundaries (`\r`, `\x0b`, `\x0c`, `\x1c`–`\x1e`, U+0085, U+2028/9) split the
line and fail as setup instead, which is safe.

**Sealed impact.** No frozen case or supplement depends on non-space separators. A static scan
found 0 lines where `split() != split(' ')`, so the correction changes no sealed outcome
`[INFERENCE: static]`.

**Smallest safe correction (fixable defect).**

- Split lines with `text.split("\n")`, skipping empty lines.
- Split fields with `line.split(" ")` and reject empty fields as `mountinfo_line_unparseable`.
- Add one co-evolved selftest arm for the NBSP root.
- Re-measure.

No frozen byte, rule or expectation changes. Until it is fixed, C2's "no false disabled"
property is falsified for this input class.

## F2 — the sealed escape rule contradicts S085 for the source field

**Evidence.** S085 `fs/proc_namespace.c:87-90`: `mangle()` is `seq_escape(m, s, " \t\n\\#")`.
It is applied to `mnt_devname` (the mountinfo source, line 180) and to the fstype (lines 94/97).
So a `#` is emitted as `\043`.

The amendment says to "Octal-decode root, mountpoint and source with exactly 040/011/012/134;
reject other backslash escapes as QUOTA_SETUP". `decode_octal` implements exactly that set
(`OCTAL_ESCAPES`, line 233) and runs on every line's source (line 337).

**Counterexample** (`falsify/CriticNoHarm/hash-source-escape.fixture.json`,
sha256 `6c7d33f760d0bc76e0915106ec8444958e333d8b4166b8e7daa453b2c23b7f51`): an unrelated classic FUSE mount with
`fsname` `sshfs#user@host:/`, which the kernel renders as `sshfs\043user@host:/`. The requested
path `/home/x` is on `/`.

The static trace: `mountinfo_escape_invalid` makes the **whole run exit 2 QUOTA_SETUP** with
`paths=[]`. Every default path loses its verdict, and the probe never opened the offending mount.

This fails closed (no false verdict), but it is an operability harm on any host with such a
mount, and it rests on a source claim that the admitted S085 row contradicts.

**Classification.** Production follows the *sealed* amendment, so silently accepting `\043`
would be a post-seal rule change. That makes this a **tradeoff the judge must weigh**, not a
fixable implementation bug this round. The correction is to pre-register for the next round:
decode `\043` in the source/fstype fields only, keep the mount-point/root set at four escapes,
and add a fixture. No sealed case exercises `\043` (grep: none).

## F3 — the real-control check is coupled to the strict red

The measure4 `summary.json` shows `checks[33]` `C30.c2_oracle_real_control_agrees` **false**, and
`real_controls_pass: false`. In `c2-after-real-observed.json` the only unmet result is
`results[7]` CaseEscapedSpace (case sha `8340738a…beea`). The direct comparison
`c2.real_control.match` is **true**: exit 0 QUOTA_DISABLED, `/home` btrfs
`btrfs_qgroups_dir_absent`/`btrfs_subvolume_skipped`, `/tmp` xfs `xfs_noquota_option`/`match`.

So the sealed real-control check can never pass while CaseEscapedSpace stays red.
LOG.md:1670 ("default real control matches") is true only for the direct row.

**Correction (disclosure only):** state that C30 and `real_controls_pass` are false solely
because of CaseEscapedSpace, while the direct row has `match=true`. Do not rewrite C30.

There are no other additional failures. Checks 0–30 and 32 are true, and C34 is the declared
strict red.

## F4 — speculative Core exposure in SKILL.md

SKILL.md `## Round23` (added in production commit `1979a9d`) registers "quota surface (r23)",
with an entry command and verdict map, as a current probe. No line in SKILL.md, or in
`corpus/knowledge/quota-surface-r23.md`, states that strict C2 is **unadmitted at 29/30** or
names CaseEscapedSpace. Grep of both found no `29/30`, `EscapedSpace`, `unadmitted` or `pending`.

LOG.md and the lesson do carry the disposition. But SKILL is the operational surface a fleet
reader acts on.

The probe's behaviour on the contradiction topology is conservative (unknown), so there is no
behavioural harm from that case. There is, however, from F1, which the SKILL row implicitly
vouches against.

**Correction:** add one SKILL line, "r23 C2 strict target unadmitted (sealed 29/30, frozen
CaseEscapedSpace contradiction); row is author-lane pending outside closure", or keep the row
out of SKILL until closure. That is fixable, with no judge conflict.

## F5 — pycache writes into frozen and production trees (fence debt)

`.ufo/waves/round-22/frozen/__pycache__/fixture-builder-v2.cpython-314.pyc` has mtime
14:00:23-0300. It was produced by `oracle-rename.py:17-19` (`spec_from_file_location` plus
`exec_module` of the r22 frozen builder) run in-lane without `-B`.

`tools/__pycache__/mori-quota-surface.cpython-314.pyc` has mtime 15:17:10-0300. It matches the
`<cell>` import in `evidence/measure1-debug.txt`. Peers QSetupMalformed, QBtrfsDevMatch and
QBtrfsSquota saw these files; neither LOG.md nor the lesson discloses them.

The bytes of tracked and sealed files are unchanged: `summary.json` `worktree_comparison` is
all true, and `git diff 22772c1 6eb889c -- frozen oracles driver round-22/frozen` is empty. So
this is fence debt, not integrity loss.

**Correction:** disclose both writes. Future in-lane harness runs should use `python3 -I -B` or
`PYTHONDONTWRITEBYTECODE=1`. The cleanup is the parent's decision, not mine.

## F6 — basis mislabel on an unreadable qgroups stat (real mode only)

In `scan_btrfs_sysfs`, a non-ENOENT `OSError` on `qgroups` sets `qgroups=None` (lines 604-606).
`classify_btrfs` then returns `btrfs_device_unmapped` (line 477) even though exactly one UUID
matched. The state is correctly unknown (it fails closed, and the amendment's "never
absent/disabled" holds), but the basis claims a mapping failure that did not occur.

Fixture mode cannot reach this branch, because `qgroups` must be a bool, so no sealed case
covers it.

This is a tradeoff: the contract has no dedicated token, and adding one widens the output
vocabulary. Disclose it as a known basis limitation, and pre-register a distinct token next
round.

## F7 — standalone selftest receipt lacks env

`evidence/quota-selftest-corrected.json` records `argv` with the lane path, `-I` and
`--selftest`, but no environment. The selftest uses `tempfile.TemporaryDirectory`, so without
`TMPDIR` it falls back to `/tmp`. The driver-run receipts do set `TMPDIR` to the scratch root
(`measure-round23-v2.py:192-193`).

**Correction:** record the env, or re-receipt that run via the driver.

## Held claims (attacked, not falsified)

### C1 source/byte guard

At `1bfe708`, `tools/mori-retention-reconcile.py` has sha256 `0795bac9…de32`. At `f3dc07c` it
has `4599ee1a…9a36`, which equals `frozen/c1-source-delta.json` `transformed_sha256`. The mode
stays 100755.

`git diff` shows exactly the two frozen transforms: line 16 `SCHEMA` v1→v2 and the
`'raw_unallowlisted':len(unallowed),` deletion on line 234. The entering source had that key
only in the check producer (lines 231–234). The selftest (274) and setup (287/289) payloads
never carried it, and they now carry schema v2.

measure4 shows:

- `c1_original_26` before 25/26 (R25 red), `misleading_alias_runs` 8;
- after 26/26, with 0 alias runs;
- supplementary guards pass: `source_byte_guard` matches, 3 `source_guard_mutants` are all
  `guard_rejects:true`, 18 same-instance replay arms, and selftest schema v2 with
  `alias_present:false`;
- `c1_real_control.match:true`: raw 95, scanner 90, `receipt_match` true, identity pins match.

The line count is unchanged (in-place edits), so external line citations stay valid. For
example, `tameshi-shokunin/.ufo/waves/round-24/w1/OverlapKama.md` cites
`mori-retention-reconcile.py:20/:169/:175`.

### C1 caller migration

`git grep raw_unallowlisted f3dc07c -- . ':!.ufo'` finds only prose:

- LOG/SCORECARD/lessons (historical);
- SKILL.md:556 (an explicitly historical v1 caveat) and :570 (the removal notice);
- the knowledge note's appended v2 correction.

No tracked tool consumes the key or the v1 schema. A fleet-wide search (`--no-ignore`, excluding
`.git`/`.jj`/`.scratch`/interactive-sessions/mori) found only `MANIFEST.json`'s r22 closure text,
`.ufo/reports/round-22/mori.md` (historical) and the tameshi line citations above. There are
no executable consumers.

### Retained debt at the pin

The committed gate receipt `retention-floor-delivered.json` is at `56ac3ba`, not at the pin. It
shows metric 4, raw 95, allowlisted 86, non_author 5, 0 forbidden, 0 warnings.

Between `56ac3ba` and `f3dc07c`/`6eb889c`, `git diff --numstat` shows deletions only in the two
tool lines. Everything else is additions, and the allowlist and policy are unchanged, so no
allowlist row can go stale.

My static re-implementation of the gate's per-line class scan (policy classes from the
`56ac3ba` blob, receipt `falsify/CriticNoHarm/retention-delta-static.json`, sha256
`a00b6d1b…42c5`; script at
`/fast/scratch/hyaku/mori-r23/CriticNoHarm/retention-delta-static.py`, sha256 `bf1f8ba2…a28aa3`)
reports:

- `f3dc07c`: 59 changed files, **0 new hit keys**;
- `6eb889c`: 117 changed files, **0 new hit keys**;
- 0 removed hits in the changed production and docs files since `1bfe708`.

So the 4 retained hits and identities very likely hold at the pin `[INFERENCE]`. This is a
re-implementation, not the committed gate, so a gate receipt at `f3dc07c` would close it.

The other debt is byte-preserved: original permission RED 11/12, two unknown dispositions,
baseline blocked and `privacy_clearance=false`. `git diff --name-status 1bfe708 6eb889c` shows
no modified historical `.ufo` files, and `summary.carried_open_debt` matches. Probe visibility
is nowhere claimed as clearance.

### Frozen bytes and the strict-C2 disposition

`git diff 22772c1 6eb889c` over `frozen/`, both oracles, `contract.md`, `preseal-amendment.md`,
`build/MeasureDriver` and `round-22/frozen` is empty. CaseEscapedSpace has sha256
`8340738a…beea` at both the seal and the working tree.

The contradiction is genuine, and it is the expectation that is wrong, not the rule:

- mount 43 `/srv/my\040data` has parent 33 (`/`), while `/srv` (42) also hangs off 33;
- in real kernel topology, a 43 hanging off `/` means it was mounted before 42 covered `/srv`,
  so it is **hidden**;
- the frozen "enabled at `/srv/my data`" would therefore be a false positive, which the sealed
  rule correctly refuses.

So `UNPROVABLE at 29/30` is the only honest outcome without rewriting sealed bytes. There is no
special case: production has no path-specific code, and the post-measure diff touches no
classifier branch.

### Selftest-correction separation

The `56ac3ba` → `f3dc07c` change is exactly one line: `path_entry("/srv data", st_dev="259:2")`
in the co-evolved `escaped-mount-point` arm. It is input only, and its expected output is
unchanged.

That arm has a single mount with no shorter cover, so it cannot exercise the parent rule or
stand in for frozen CaseEscapedSpace. LOG and the lesson keep 49/49 separate from C2. The
earlier `56ac3ba` changes (non-empty population, exact path-record keys) implement the declared
amendment clauses, and C2 stays 29/30 across measures 2–4.

### Read fence

The real-mode readset is:

- `/proc/self/mountinfo`;
- `os.stat` and `realpath` of requested paths;
- `realpath` of the chosen mount's source;
- `listdir`/`isdir`/`stat` under `/sys/fs/btrfs`;
- the `qgroups/enabled` text.

`qgroups/mode` is never opened in real mode (lines 615-620). There is no subprocess outside the
selftest, no ioctl or quota command, and no writes besides stdout. The output emits only the
quota-related option keys; `error` is a fixed token.

## Smallest safe corrections (ordered)

1. **F1** (fix now, then re-measure): split on `" "`/`"\n"` with empty-field rejection, and add a
   selftest arm. No frozen change, and no sealed case outcome changes `[INFERENCE: static]`.
2. **F3, F4, F5, F7** (disclosure only): C30 is coupled to CaseEscapedSpace; add a SKILL
   unadmitted-status line; disclose both pycache writes and use `-B` going forward; record env on
   the standalone selftest receipt.
3. **F2, F6** (next-round pre-registration, judge tradeoff): `\043` source/fstype decoding per
   S085:89, and a distinct basis for an unreadable qgroups stat. Do not change them silently
   post-seal.

None of this alters C1 (26/26 plus guards, independent) or the strict-C2 UNPROVABLE disposition.
F1 does withdraw any claim that C2 never fabricates disabled evidence until it is fixed.

Tools installed or updated: none.
