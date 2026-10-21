# QBoundary — round-23 falsification of the sealed C2 case `CaseBoundary`

Seat: `MadoR22-2.QBoundary` (reviewer, leaf; no delegation, no subagents).
Wave: mori round 23, claim **C2 — coverage** (FR2 quota/EDQUOT observability).
Production under test: `tools/mori-quota-surface.py` @ `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`.
Expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`.
Receipt: `.ufo/waves/round-23/falsify/QBoundary/scan.json`
(sha256 `d56dc60f8490f58412755e5bbdec3770859cc784d905254084ff8a066c2b6d4a`).

## Verdict

**MATCH — no falsification of this case.** The production tool reproduces the sealed
expectation of `CaseBoundary` exactly: exit `0`, `finding_id` `QUOTA_DISABLED`, and the
ordered six-field tuple
`('/a/bc', 'btrfs', '/a', 'disabled', 'n/a', 'btrfs_qgroups_dir_absent')`.

| facet | given (sealed expectation) | actual (observed) | match |
|---|---|---|---|
| exit | `0` | `0` | yes |
| `finding_id` | `QUOTA_DISABLED` | `QUOTA_DISABLED` | yes |
| ordered six-field tuple | `('/a/bc', 'btrfs', '/a', 'disabled', 'n/a', 'btrfs_qgroups_dir_absent')` | identical | yes |

Primary (scored, six-field denominator) and supplementary metadata were compared
**separately**; the six-field denominator was not widened by any supplementary field.
The sealed oracle's own supplementary checks: 9 pass / 0 unmet. No expected byte was
edited, no case file was rewritten, and no other sealed case was executed by this seat.

Scope note: this seat's case is **not** the known strict red. The frozen contradiction
(`evidence/frozen-contradiction.json`) is `CaseEscapedSpace` (selected mount 43, parent
33 vs shorter cover `/srv` 42 ⇒ the sealed rule demands `ambiguous_overmount` while the
frozen expected row says enabled). `CaseBoundary` is unaffected by that contradiction and
passes; nothing here excuses, rewrites or relabels `CaseEscapedSpace`.

## What was read before executing

| artifact | path | why |
|---|---|---|
| sealed case | `.ufo/waves/round-23/frozen/quota-cases/CaseBoundary.json` | the case under falsification |
| case derivation (author report) | `.ufo/waves/round-23/build/CaseBoundary.md` | how the expectation was derived; its ambiguities A1–A6 and discriminating-power list |
| original proposal / corrected case | `.ufo/waves/round-23/cases-proposed/CaseBoundary.json`, `.ufo/waves/round-23/cases-corrected/CaseBoundary.json` | verify the sealed file's claimed one-field delta |
| case decisions | `.ufo/waves/round-23/frozen/case-decisions.json` | L1's selection record for this case |
| seal manifest | `.ufo/waves/round-23/frozen/seal-manifest.json` | sealed digests of case, oracle, contract |
| amendment | `.ufo/waves/round-23/preseal-amendment.md` | the C2 final rules that supersede the contract's ambiguous clauses |
| contract | `.ufo/waves/round-23/contract.md` | §C2 fixture format, resolution rule, classification table, verdict precedence |
| implementation | `tools/mori-quota-surface.py` | the selected quota implementation (resolution + classification code read) |
| sealed oracle | `.ufo/waves/round-23/oracle-quota.py` | the sealed comparison logic (imported, not re-implemented) |
| lesson 23 (Gate, mistakes M1–M8) | `corpus/lessons/round-23.md` | the wave's source/lifecycle authority |
| source registry | `corpus/SOURCES.md` | S077–S084 rows now exist; the mapping matches the case's `sources` array |
| frozen contradiction | `.ufo/waves/round-23/evidence/frozen-contradiction.json` | context: the known strict red is a different case |

## Byte identities (verified, not asserted)

| object | sha256 | provenance check |
|---|---|---|
| sealed case file | `2e2ef692060105f054f2561091cb7603e77b1328b7954f63046ff57e7bea5d52` | `git hash-object` = `0d0614201301a586d46affdf6e37f320d75553ec` = blob at seal `22772c1` = blob at `HEAD` `6eb889c`; identical to `frozen/seal-manifest.json` entry and to `cases-corrected/CaseBoundary.json` |
| original proposal | `9a40c67f4c557e296582f07f9bdd0771b4fec6f84113f51c80c3cefce733c048` | unchanged proposal; differs from the sealed case by exactly the added `qgroups_enabled` member |
| tool | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` | worktree == `git show f3dc07c:tools/mori-quota-surface.py`; `git diff f3dc07c..HEAD -- tools/mori-quota-surface.py` is empty |
| oracle | `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` | worktree == blob `4fa8d52c285eaa69d7da6a77194c47454d031366` == blob at seal == blob at `HEAD` |
| fixture written for the run | `12515259cd1856a6a9e9ef2217bc7afd4cf3e4c91c82d72fe7f52cc2db8eb38b` (949 B) | `json.dumps(case["fixture"], indent=2, sort_keys=True) + "\n"` — the oracle's canonical fixture form; **byte-identical** to the fixture the oracle generated for its own run |
| observed stdout | `32b9f7376615fe13eadaf57ca7817c2707f3c9e86c4a831b3ae9ed91c36b46a0` | byte-identical across two independent bounded runs |

`git status --porcelain` over `.ufo/waves/round-23/frozen`, `.ufo/waves/round-23/oracle-quota.py`
and `tools/mori-quota-surface.py` is empty: no frozen, oracle or production byte was touched.

## Exact execution (fixture mode only; real mode never invoked)

Scratch (this seat's own tree, no `/tmp`): `/fast/scratch/hyaku/mori-r23/QBoundary/`
— `fixture.json`, `stdout.txt`, `stderr.txt`, `stdout2.txt`, `stderr2.txt`,
`cases/CaseBoundary.json`, `oracle-out.json`, `oracle-out-quota-fixtures/`,
`p1_contrast_a_b.json`, `p2_deeper.json`, `p4_decoy_device.json`, `p5_unmapped.json`
and their `.out`/`.err` captures. `TMPDIR=/fast/scratch/hyaku/mori-r23/QBoundary/`.

```
argv (given, canonical tool invocation):
  python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
          --fixture /fast/scratch/hyaku/mori-r23/QBoundary/fixture.json

argv (actual, as executed; one child at a time):
  prlimit --as=402653184 --cpu=15 --nofile=64 -- timeout --signal=KILL 15s \
    python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
    --fixture /fast/scratch/hyaku/mori-r23/QBoundary/fixture.json

cwd   /fast/scratch/hyaku/mori-r23/QBoundary
exit  0        stderr 0 bytes        timeout 15 s        AS cap 384 MiB
```

Resource-cap note for the record: util-linux `prlimit --as` takes **bytes**, not 1024-byte
blocks. Read as blocks (`--as=393216`) the interpreter cannot even start (loader error
`failed to map segment from shared object`, exit 127; with `timeout` in front, SIGSEGV
139) — that is a mis-specified cap, not a tool defect. The correct 384 MiB cap is
`--as=402653184`, under which the run above is clean and deterministic.

No live host read of any kind was performed by this seat: no `/proc/self/mountinfo`, no
`os.stat`, no sysfs listing, no `quotactl`/`btrfs qgroup`/`xfs_quota`/`repquota`/`mount`,
no qgroup or quota mode file, and the tool was never invoked in real mode. The real
control (`frozen/c2-expected-real.json`) was **not** executed here; only the single
fixture case was.

## Primary comparison (scored, six-field denominator)

Compared fields, in the sealed order (`oracle-quota.py: PATH_KEYS`):
`path, fstype, mount_point, quota_state, enforcement, basis`.

| # | given | actual | match |
|---|---|---|---|
| 1 | `('/a/bc', 'btrfs', '/a', 'disabled', 'n/a', 'btrfs_qgroups_dir_absent')` | `('/a/bc', 'btrfs', '/a', 'disabled', 'n/a', 'btrfs_qgroups_dir_absent')` | yes |

Two independent evaluations agree:

* imported sealed oracle — `oracle-quota.evaluate_case(case, parsed, exit=0, stdout)` →
  `ok=True`, `reason=None`, headline `exit_match/finding_match/paths_match` all true,
  9/9 supplementary checks pass, `leakage_hits=[]`;
* sealed oracle CLI restricted to a one-case directory
  (`--cases <scratch>/cases` containing only `CaseBoundary.json`, **no** `--real-expected`)
  → `R23_C2_QUOTA_CASES_MATCH`, `counts {total:1, pass:1, unmet:0, capability_absent:0}`,
  `supplementary_counts {total:9, pass:9, unmet:0}`, exit 0.

## Supplementary metadata (reported separately, NOT scored)

The sealed case carries **no** `supplementary_expected` block, so the three metadata fields
are unasserted by the six-field denominator. Observed values, recorded but not scored:

| path | `device_check` | `quota_option_keys` | `btrfs_qgroups_mode` |
|---|---|---|---|
| `/a/bc` | `btrfs_subvolume_skipped` | `[]` | `null` |

These agree with what the amendment implies for this path: btrfs with stat major `0` skips
the equality check (`0:30` mount vs `0:57` path), btrfs carries its mechanism in sysfs and
not in mount options (`[]`), and the selected device's qgroups directory is **absent**, so
no mode text exists (`null`). They are recorded here as reviewer observation only; they do
not enter the scored denominator and were not inserted into the expected bytes.

## Independent falsification probes (this seat's own synthetic variants)

Four own-fixture probes (scratch only, never frozen bytes) were run to test whether the
match is discriminating or vacuous. Each reuses the sealed fixture with exactly one
synthetic change:

| probe | change | observed | reading |
|---|---|---|---|
| P1 `0d66bfd4b1f03539…` | query `/a/b` instead of `/a/bc` (same mounts) | exit 1 `QUOTA_ENABLED`; `/a/b` → xfs, `/a/b`, enabled, enforced, `xfs_quota_option`, `device_check match` | the nested xfs `usrquota` mount **is** visible to the tool; the sealed expectation is not produced by an invisible mount |
| P2 `5c6de5abe60d83de…` | query `/a/bc/d` (deeper descendant) | exit 0 `QUOTA_DISABLED`; btrfs `/a` disabled | resolution is by component prefix and stays with `/a` for deeper descendants — a bare string-prefix implementation would have diverged here too |
| P4 `428e631fc01cc137…` | `device_links["/dev/sdb1"]` → `dm-0` (the decoy uuid: present + `qgroups_enabled` true + `squota`) | exit 1 `QUOTA_ENABLED`; btrfs `/a` enabled/unknown/`btrfs_qgroups_enabled`, `btrfs_qgroups_mode` `squota` | the sealed `disabled` verdict is positively sourced from *this* device's uuid, not from a default; the decoy uuid does not leak into the sealed case, and the amendment's present+enabled=true arm is reachable |
| P5 `689cc0c1b851c6fd…` | `device_links["/dev/sdb1"]` → `unmapped-dev` (negative control) | exit 2 `QUOTA_STATE_UNKNOWN`; btrfs `/a` unknown/n/a/`btrfs_device_unmapped` | an unmappable device yields `unknown`, never `disabled` — so the sealed `disabled` verdict cannot be an artefact of a fallback |

Consequence: the pass is discriminating on all four of the author's stated failure modes
that apply to this fixture — bare-prefix mount matching (P1/P2), wrong-device uuid
selection (P4) and unmapped/absent-surface defaulting (P5). The device-check-on-btrfs
failure mode is not separable here by probe (the fixture's stat major is `0` by design, so
the skip branch is taken); it is covered by the frozen real control instead.

## Residual risk / verification gaps

1. **The six-field expectation cannot assert `device_check`, `quota_option_keys` or
   `btrfs_qgroups_mode`** (author's A4). The observed values above are reviewer-recorded,
   not sealed assertions. The amendment's parent-ID refusal and the duplicate-covering-
   mountpoint refusal are exercised here only in the **non-refusal** direction (the
   chosen `/a` mount's parent id `28` equals the id of the longest strictly shorter
   covering mount `/` `28`), so this case cannot detect a regression in those refusal
   branches; that is `CaseEscapedSpace`'s domain, and that case is the frozen red.
2. **No host observation backs this fixture.** The mount lines, device names and UUIDs are
   synthetic; the case is a behavioural fixture, not a reproduction of this host's quota
   state. `QUOTA_DISABLED` is not a capacity/health verdict (ENOSPC can coexist), and the
   probe reads no limit or usage value at all.
3. **S-id binding is now resolved but was inferred at authoring time.** `corpus/SOURCES.md`
   now carries S077–S084, and the registry mapping (S077 xfs.rst, S078 xfs_super.c,
   S079 btrfs/sysfs.c, S080 btrfs/qgroup.c, S081 btrfs/inode.c, S082 proc.rst) matches the
   case's `sources` array `["S077","S078","S079","S080","S081","S082"]` exactly — the
   author's "registry rows not yet present" caveat no longer applies.
4. **One fixture-authoring rule is not asserted by any sealed case**: `device_links`
   lookup semantics (author's A3). This case is invariant under every reading (raw
   basename `sdb1` == linked value `sdb1`), which is why it passes; the amendment fixes
   "raw decoded source → mapped basename, else `basename(source)`", and the implementation
   follows that (`probe_fixture`/`device_names`), but the *sealed* expectation does not
   discriminate between the readings. P4/P5 exercise the mapping behaviour without
   asserting it as a case.
5. **This seat ran no build, lint, full suite, selftest or pinned driver**, and no quota
   or host read. The C1 arms and the strict frozen red are outside this seat's item and
   were not re-measured here; nothing in this report bears on them.

## Lane compliance

* Writes confined to this seat's report and receipt:
  `.ufo/waves/round-23/falsify/QBoundary.md` and `.ufo/waves/round-23/falsify/QBoundary/scan.json`.
  All other scratch lives under `/fast/scratch/hyaku/mori-r23/QBoundary/`; nothing under
  `/tmp`, nothing under the fleet root, no sibling seat, no lane index/jj/refs.
* No code edit, no mutation of frozen/case/oracle/production bytes, no `git add/commit/push`,
  no mutating `jj`, no synthetic repository created (no mutation clone was needed: this
  seat is read-only apart from its two deliverables).
* No live journal/journalctl query, no process/service/session probe, no credential/auth/
  config file read, no `agent.db`, no Documents/shell-history read; no transcript read of
  any kind (this wave permits none); `.git`, `.jj`, `.scratch` and the prohibited trees were
  excluded from every corpus search.
* No quota command or interface was called (`quotactl`, `btrfs qgroup`, `xfs_quota`,
  `repquota`, `mount`, `btrfs`, `xfs_quota`) and no actual qgroup/mode file was read;
  `quotactl`/ioctl/btrfs/xfs_quota/repquota/mount/remediation were not invoked in any form.
* **No tool was installed or updated by this seat** (no pacman/uv/cargo/npm action), so
  there is no tool/version/channel record to report; the only external programs used were
  the pre-existing `python3` 3.14.8, `prlimit` and `timeout` from the host.
* No special-casing, exclusion, relabelling or rewriting of any frozen case, rule or
  oracle byte; no aggregate-only pass claim — the exact exit, `finding_id`, ordered
  six-field tuple, byte identities and per-probe observations are recorded above and in
  the receipt.
