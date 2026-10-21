# ReopenS081 — S081 source re-open, plus independent C1/C2 receipt check

Seat: MadoR22-2.ReopenS081 (read-only leaf). Lane:
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Measured revision
`f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`; seal
`22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`. No source, expectation, oracle,
registry, ref or lane-index bytes were changed.

## Verdict

- **S081 row: PASS as written.** Registry row is byte-identical between the seal
  and measured revision; the URL resolves to the pinned v7.2 file; the retained
  and freshly fetched bytes are identical to the declared SHA-256; the lesson23
  Gate quote is a 3-word exact line at 8246 inside `btrfs_getattr`; the row's
  claim is supported by those bytes.
- **One scope qualification (not a registry contradiction):** S081's bytes show
  the assignment to `root->anon_dev`, but not that the anonymous device has
  major 0. The note's "major 0 -> skipped check" sentence is probe policy from the
  preseal amendment, not evidence located in S081 (see Inference/Unresolved).
- **C1 independently verified: PASS.** 25/26 -> 26/26 original requirements,
  `misleading_alias_runs` 8 -> 0, all separate supplementary guards green.
- **C2 strict target: 29/30, UNPROVABLE as declared.** Exactly one unmet case:
  frozen `CaseEscapedSpace.json`, actual `ambiguous_overmount` versus frozen
  `enabled`. Driver exit 1 is expected from that red.
- **Additional retained failure:** driver check
  `C30.c2_oracle_real_control_agrees` is false because it tests aggregate
  `after_with_real_expected.unmet == 0`; that aggregate contains the
  `CaseEscapedSpace` red. The real-control entry itself is `pass`. Therefore
  `summary.real_controls_pass=false` is **not** a real-control mismatch.

## Observed facts

### S081 identity, scope and anchor

| Field | Observed | Match |
|---|---|---|
| Registry row (seal and measured) | `S081 | Linux btrfs stat device v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/inode.c | code | A | btrfs per-subvolume anonymous stat device | btrfs_getattr:8245-8246; tag v7.2; sha256 01a6ad07c09cd1a0 | btrfs overwrites stat device with root anon_dev; do not require ordinary mountinfo device equality on that path. | mined | 2026-10-21 | on-release | corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md |` — identical at `22772c10…` and `f3dc07c0…` | yes |
| Fresh fetch | `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/inode.c`, HTTP fetch into `/fast/scratch/hyaku/mori-r23/ReopenS081/inode.c` | 319,770 bytes, SHA-256 `01a6ad07c09cd1a05fbccab640c15362c91b57b85faa94c2fd9b9c0128110fdf` — equals the task's rawSHA and `evidence/sources-manifest.json` S081 `sha256` |
| Retained evidence copy | `evidence/sources/S081-fs_btrfs_inode.c` — same 319,770 bytes, same SHA-256; `cmp` against fresh fetch exit 0 | yes |
| Registry digest | row field is the 16-hex prefix `01a6ad07c09cd1a0` of the full digest (same truncation convention as S080/S082–S084) | yes |
| Anchor | file 1-based lines 8245–8246 are inside `static int btrfs_getattr(...)`, whose definition starts at line 8215 | yes |
| Quote | line 8246 is exactly `stat->dev = BTRFS_I(inode)->root->anon_dev;`; 3 whitespace tokens (≤25 words); `evidence/source-quotes.json` S081 records the same quote, `found_in_whitespace_normalized_source: true`, `word_count: 3`; lesson23 Gate row S081 records `8246: \`stat->dev = BTRFS_I(inode)->root->anon_dev;\`` | yes |

Adjacent-line context (retained bytes, lines 8245–8246):

```c
	generic_fillattr(idmap, request_mask, inode, stat);
	stat->dev = BTRFS_I(inode)->root->anon_dev;
```

`generic_fillattr` supplies the ordinary inode device and 8246 replaces it with
the btrfs root's `anon_dev`; that directly supports the row's claim "overwrites
stat device with root anon_dev" and the operational consequence "do not require
ordinary mountinfo device equality on that path." The field is root-scoped
(`BTRFS_I(inode)->root->anon_dev`); `inode.c:4872-4873` inside
`btrfs_delete_subvolume` frees `dest->anon_dev` while deleting that subvolume
root, corroborating a per-root/per-subvolume field. The row's scope "per-subvolume anonymous stat device" is therefore a fair
reading; the row does not claim quota enablement or other filesystems, and the
bytes support no such extension.

### New note claim-vs-source (`corpus/knowledge/quota-surface-r23.md`)

Paragraph "Resolve the mount before interpreting its mechanism":

1. **Supported:** "S081 assigns a btrfs path's stat device from its subvolume
   root's anonymous device, which can differ from mountinfo's superblock
   device." The assignment is verbatim at 8246, and the unconditional overwrite
   of `generic_fillattr`'s value at 8245 shows the stat device is not the
   superblock device value. "Can differ" is thus entailed at the granularity the
   sentence needs.
2. **Not located in S081:** "A major0 btrfs mismatch is a recorded skipped
   check, not verified identity." This is accurate as a description of
   `tools/mori-quota-surface.py` (`elif mount.fstype == "btrfs" and
   path_device[0] == 0: ... "btrfs_subvolume_skipped"`), and it matches the
   preseal-amendment rule, but the major-0 property of an anonymous bdev is
   allocated by `get_anon_bdev` in `fs/super.c`, which is not one of the opened
   S077–S086 sources and is not in `evidence/sources/` or
   `sources-manifest.json`. No `get_anon_bdev`/`MKDEV(0, …)` text exists in the
   retained `inode.c` bytes. Treat this sentence as contract/probe policy, not as
   S081-derived evidence. This does not alter the row or any frozen byte; it is
   the only claim-vs-source gap found.

Lesson23 Gate statement "All source rows S077–S086 opened 2026-10-21; raw bytes
and SHA256 retained under `evidence/sources/` and `sources-manifest.json`" holds
for S081: retained bytes, manifest digest and Gate quote all agree.

### C1 — independently re-checked from receipts (not re-executed)

`evidence/measure4/c1-oracle-before.json` (measured revision `f3dc07c0…`, seal
`22772c10…`, argv staged-before tool + committed `frozen/c1-requirements.json`):

- `counts.pass = 25`, `counts.total = 26`, `counts.unmet = 1`,
  `counts.misleading_alias_runs = 8`, oracle `exit_code = 1`.
- `summary.c1_original_26.unmet_before = ["R25"]` — exactly the registered
  pre-cutover red.

`evidence/measure4/c1-oracle-after.json`:

- `counts.pass = 26`, `counts.total = 26`, `counts.unmet = 0`,
  `counts.misleading_alias_runs = 0`, `exit_code = 0`.

`summary.json` keeps the original denominator separate
(`c1_original_26.denominator = 26`, `pass = true`) from the supplementary guards
(`c1_supplementary.note`; `pass = true`):

- `source_byte_guard.matches = true`: entering SHA-256
  `0795bac9367c33e534b79599114c1635d83c4b0e4a57fbbe235644858a59de32`, exactly two
  frozen transformations (`SCHEMA` v1->v2 substitution occurrence 1; deletion
  of `'raw_unallowlisted':len(unallowed),` occurrence 1), transformed SHA-256
  `4599ee1aff95f21714e320a87fd31260f0435aa9c7a9884ac60ab952fe099a36`, mode
  `100755`, target v1-literal count 0, v2-literal count 1, alias-fragment
  count 0.
- `source_guard_mutants`: `appended_statement`, `removed_line`,
  `whitespace_only` all `guard_rejects = true`.
- `same_instance_replay`: 18 arms (`valid`, `drop`, `inject`, `digest`, `line`,
  `class`, `metric`, `forbidden`, `invalid-revision`, `diverged`,
  `policy-changed`, `allowlist-changed`, `malformed`, `bool-line`, `duplicate`,
  `bool-metric`, `valid` (second), `symlink`), every arm `same_instance: true`,
  `argv_equal: true`, `identical_apart_from_special_keys: true`; special keys are
  only `schema`, `raw_unallowlisted`, `tool_sha256`.
- `selftest`: entering schema v1 exit 0, measured schema v2 exit 0, `pass: true`.
- `c1_real_control.match = true` with every pinned field matching:
  `finding_id RETENTION_RECONCILED`, `scanner_unallowlisted 4`,
  `raw_not_allowlisted 9`, `raw_total 95`, `allowlisted 86`, `policy_excluded 5`,
  `scanner_total 90`, `retention_state red`, `privacy_clearance false`,
  `schema mori-retention-reconciliation-v2`, forbidden keys absent,
  `identity_pins.match = true`, `tool_sha256_match = true`,
  `inputs_sha256_match = true`.

C1 is therefore verified **separately** from C2's red: before-counts, after-counts,
alias counter and every supplementary guard are green, and the driver's aggregate
false result is attributable to C2's sealed case plus the C30 aggregation issue
below, not to C1.

### C2 — strict result and the one red

- `summary.after.c2 = {capability_absent: 0, pass: 29, total: 30, unmet: 1}`;
  before = `{capability_absent: 30, pass: 0, total: 30, unmet: 0}`;
  supplementary = `{pass: 274, total: 274, unmet: 0}`.
- `evidence/measure4/c2-after-observed.json` has 30 `results`; exactly one is
  `status: "unmet"`: `CaseEscapedSpace.json`, with
  `headline.exit_match = false`, `finding_match = false`, `paths_match = false`.
  No other case is unmet; no other additional behavioral failure exists in the
  sealed 30.
- Actual observed for that case: exit 2 `QUOTA_STATE_UNKNOWN`,
  `basis = "ambiguous_overmount"`, `fstype = null`, `mount_point = null`,
  `device_check = "not_checked"`, `quota_state = "unknown"`,
  `enforcement = "n/a"`, `quota_option_keys = []`, per
  `evidence/frozen-contradiction.json`.
- Frozen expected: exit 1 `QUOTA_ENABLED`, first path xfs `/srv/my data`
  `enabled/enforced/xfs_quota_option`.
- Frozen case bytes: SHA-256
  `8340738a509e474a94a815637e66b407dfb60c6449511e52db55296d844abeea`, matching
  `frozen-contradiction.json.case_sha256` and `summary.sealed_artifacts`.
- Rule/geometry: selected mount id 43 (`/srv/my\040data`, parent 33); longest
  strictly-shorter covering mount id 42 (`/srv`); 33 != 42, so the sealed
  parent-consistency rule requires `ambiguous_overmount`. The case's own
  rationale text says the parent rule is untriggered because mountpoints are
  unique — that rationale is inconsistent with the sealed parent-ID clause; the
  expected bytes and the rule both remain unchanged, as Main directs.
- Seal proof: `ancestry.seal_is_strict_ancestor_of_revision = true`,
  `seal_equals_revision = false`; reconciler entering bytes unchanged and quota
  production path absent at seal (`seal_proof`).

### Checks beyond the single case red

- `summary.checks` contains exactly two `pass: false` entries:
  - `C34.c2_after_every_case_matches` (index 31): `pass_count 29 / total 30`,
    `unmet 1` — the intended strict red.
  - `C30.c2_oracle_real_control_agrees` (index 33): `counts
    {pass: 30, total: 31, unmet: 1}`, `oracle_exit 1`.
- C30's condition (driver lines 1109–1112) is
  `after_with_real_expected.unmet == 0`. The oracle's `--real-expected` count adds
  the real-control row to the 30 case rows (`oracle-quota.py` lines 529–539).
  `evidence/measure4/c2-after-real-observed.json` shows
  `real_control.status = "pass"` and `real_control.headline = {exit_match: true,
  finding_match: true, paths_match: true}`, with the sole `unmet` result still
  `CaseEscapedSpace.json`. `C29.c2_real_control_matches_frozen` is `pass: true`.
  Hence `summary.real_controls_pass = false` is a check-attribution artifact of
  the known case red, not evidence that the frozen real control disagrees.
  Retained as an additional failure of the driver's boolean even though the
  underlying real-control observation matches.
- All other checks 0–33 are `pass: true`, including `C29` (C2 real control),
  `C25` (C1 real control), `C35` (C1 real identity pins), `C21`/`C22` (source
  guard and discrimination), `C23` (same-instance output equivalence), `C26`
  (alias present before / absent after), `C19`/`C20` (alias removed, schema v2),
  and both before/after C1 count checks (`C17`/`C18`).

### Quota public selftest — separate arm, not the frozen case

- `evidence/quota-selftest-corrected.json`: argv `python3 -I
  tools/mori-quota-surface.py --selftest`, measured revision `f3dc07c0…`,
  `exit 0`, stdout `{"arms":49,"exit_code":0,
  "finding_id":"QUOTA_SELFTEST_OK","schema":"mori-quota-surface-v1"}`.
- `evidence/quota-selftest-delivered.json` is an earlier, different receipt at
  measured revision `56ac3badb4d84ed5b0b117d6295fc832341e01f3`, exit 1, whose
  five failures are the `escaped-mount-point` selftest arm
  (`rc=2 want=1`, `basis='device_mismatch' want='xfs_quota_option'`, etc.).
  lesson23 records that this arm combined mount `259:2` with default helper stat
  `259:1`; correcting its input to explicit `259:2` yields the 49/49 receipt.
- This is a co-evolved synthetic fixture arm. It neither changes nor repairs the
  frozen `CaseEscapedSpace` topology case; the frozen case remains red at 29/30.

## Inference

- The registry's 16-hex digest is deliberate truncation, not a different file:
  the full 64-hex value appears in `sources-manifest.json` and
  `source-quotes.json` and matches both the retained and remote bytes.
- The note's "can differ" sentence is a weaker, defensible reading of the
  unconditional overwrite; the major-0 sentence is tool policy. Neither warrants
  a registry edit in this read-only seat.
- C1's and C2's observations are receipt-level: this seat did not re-run the
  pinned driver or any oracle, per lane limits.

## Unresolved / limits

- **Major-0 provenance:** `get_anon_bdev`/anonymous-bdev allocation is not in
  S077–S086 or retained evidence; if future documentation claims major 0 as a
  source fact of S081, it needs its own opened source row (e.g. `fs/super.c`).
  Current note wording can be read as probe policy, so no contradiction is
  charged here.
- **No live host reads** in this seat: C2 real-control agreement is taken from
  committed receipts (`c2-real-control.json`, `summary.json`), not re-observed.
- **C30 attribution** is a driver-boolean issue only; it does not add a case
  failure and does not change the 29/30 denominator or frozen bytes.
- No source, expectation, oracle, registry, case, lane index, jj or Git ref was
  modified. Scratch used only
  `/fast/scratch/hyaku/mori-r23/ReopenS081/inode.c`; no `/tmp`. No tool was
  installed or updated.

## Confidence

High for byte identity, hash, line/anchor and quote (two independent byte
copies). High for C1/C2 counts and check statuses (direct receipt fields). Medium
only on how to classify the note's major-0 sentence (policy vs. source claim); the
located S081 claim itself is confirmed.
